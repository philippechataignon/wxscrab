# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import xml.etree.cElementTree as ET
import time

import dico

import partie
import joueur
import logger
import msg
import grille
import tirage

class Stop(Exception) :
    pass

class Restart(Exception) :
    pass

class Next(Exception) :
    pass

class main():
    def __init__(self, options) :
        self.options = options
        self.dic = dico.dico(self.options.dico)
        self.jo = joueur.joueurs()
        self.chrono = self.options.chrono
        self.tirage = tirage.tirage("")
        self.tour_on = False
        self.points_top = 0
        self.categ_vote = ('restart', 'next', 'stopchrono')
        self.votes = {}
        self.votants = {}
        self.init_vote()
        self.stop = False

    def boucle_game(self, f_attente=True) :
        while True :
            try :
                self.pa = partie.partie(self.options)
                self.options.game = None
                self.log = logger.logger(self.pa.get_nom_partie())
                self.gr = grille.grille()
                self.points_top = 0
                self.jo.score_raz()
                if f_attente :
                    self.info("Prochaine partie dans %d secondes" % self.options.attente)
                    self.attente(self.options.attente)
                self.jo.envoi_all(msg.msg("new"))
                print "-"*20, self.pa.get_nom_partie(),"-"*20
                print self.options
                tour = 0
                for self.tirage, coord_mot_top, mot_top, pts_mot_top, num_tour in self.pa.liste :
                    tour +=1
                    if self.options.tour is not None and tour < self.options.tour :
                        self.debut_tour(coord_mot_top, mot_top, pts_mot_top, num_tour, 1)
                    else :
                        self.debut_tour(coord_mot_top, mot_top, pts_mot_top, num_tour, self.options.chrono)
                        self.attente(self.options.inter)
                self.info("Fin de la partie")
                self.log.fin_partie()
                self.options.tour = None        # tour ne s'applique qu'au premier lancement
            except Restart :
                f_attente = False
            except Next :
                pass
            except Stop :
                print "Sortie thread partie (loop)"
                break
            else :
                f_attente = True

    def attente(self, tps) :
        if self.stop :
            raise Stop
        if len(self.jo)>= 1 :
            if self.votes['restart'] == len(self.jo) :
                self.raz_vote('restart')
                raise Restart
            elif self.votes['next'] == len(self.jo) and self.tour_on :
                self.raz_vote('next')
                raise Next
        time.sleep(tps)
        if self.votes['stopchrono'] > 0 :
            self.raz_vote('stopchrono')
            self.info("Le chrono est stoppé")
            while (self.votes['stopchrono'] == 0) :
                time.sleep(0.5)
            self.raz_vote('stopchrono')
            self.info("Le chrono est reparti")

    def debut_tour(self, coord_mot_top, mot_top, pts_mot_top, num_tour, chrono_total) :
        self.jo.score_tour_zero()
        self.info("------------------------")
        self.info("Tour n°%d" % num_tour)
        if self.options.topping :
            self.info("Le top fait %d points" % pts_mot_top)
            self.points_top = pts_mot_top
        self.log.debut_tour(num_tour)
        m = msg.msg("tirage", self.tirage.get_mot())
        self.jo.envoi_all(m)
        self.tour_on = True
        self.chrono = chrono_total
        self.init_vote()
        on = (self.chrono >= 0)
        while on :
            self.jo.envoi_all(msg.msg("chrono", self.chrono))
            try :
                self.attente(1)
            except Next :
                self.chrono = 1
            self.chrono -= 1
            on = (self.chrono >= 0)
        self.tour_on = False
        self.jo.envoi_all(msg.msg("mot_top",(coord_mot_top, mot_top)))
        self.info("Top retenu : %s-%s (%d pts)" % (coord_mot_top, mot_top, pts_mot_top))
        self.log.fin_tour(coord_mot_top, mot_top, pts_mot_top)
        print("%s - %s" % (coord_mot_top, mot_top))
        self.gr.pose(coord_mot_top, mot_top)
        message = self.jo.score_fin_tour(pts_mot_top)
        if message != "" :
            self.info(message)
        self.jo.envoi_all(msg.msg("score", self.jo.tableau_score()))
        return False

    def traite(self, channel, mm) :
        c = mm.cmd
        nick  = mm.id
        # print "Traite %s %s %s" % (mm.cmd, mm.param, mm.id)
        if c == 'joueur' :
            proto_serv = 2
            proto_client = mm.param[0]
            ret = self.jo.add_joueur(nick, proto_client, channel)
            if ret == 1 :
                m = msg.msg("connect",(1,"Connexion OK", proto_serv))
                channel.envoi(m)
                self.info("Connexion de %s" % nick)
                if proto_client < proto_serv :
                    m = msg.msg("info", "Attention : le protocole de votre programme (%d) est plus ancien que celui du serveur (%d)."  % (proto_client, proto_serv))
                    channel.envoi(m)
                    m = msg.msg("info", "Il faut mettre votre programme à jour dès que possible")
                    channel.envoi(m)
                elif proto_serv < proto_client : 
                    m = msg.msg("info", "Info : le protocole du serveur (%d) est plus ancien que celui de votre programme. (%d)" % (proto_serv, proto_client))
                    channel.envoi(m)
            elif ret == 0 :
                m = msg.msg("connect",(0,"Erreur : nom existant", proto_serv))
                channel.envoi(m)
                self.info("Tentative de %s" % nick)
            elif ret == 2 :
                m = msg.msg("connect",(2,"Reconnexion", proto_serv))
                channel.envoi(m)
                self.info("Reconnexion de %s" % nick)
        elif c == 'propo' and self.tour_on :
            coo = mm.param[0]
            mot = mm.param[1]
            tir = self.tirage
            controle, scrab = self.gr.controle(coo, mot, tir)
            if controle == 0 :
                point, mot_nonex  = self.gr.point(coo, mot, scrab, self.dic)
                self.jo.set_msg_fin_tour(nick, mot_nonex)
                score = point
                if len(mot_nonex) > 0 :
                    # met le score a 0 si non existant
                    score = 0
                m = msg.msg("valid",(coo, mot, point))
                channel.envoi(m)
                self.jo.set_points_tour(nick, score)
                self.log.add_prop(nick, coo, mot, score, self.options.chrono-self.chrono)
            else:
                m = msg.msg("error","Erreur %d : %s" % (controle, self.gr.aff_erreur(controle)))
                channel.envoi(m)
        elif c == 'askscore' :
            channel.envoi(msg.msg("score", self.jo.tableau_score()))
        elif c == 'askinfo' :
            proto, score, top, pct, message = self.jo.get_infos_joueur(nick) 
            if self.tour_on :
                message = []
            if proto >= 1 :
                m = msg.msg("infojoueur", (score, top, pct, message))
            else :
                txt = message[0] if len(message) > 0 else ""
                m = msg.msg("infojoueur", (score, top, pct, txt))
            channel.envoi(m)
        elif c == 'asktirage' :
            channel.envoi(msg.msg("tirage",self.tirage.get_mot()))
        elif c == 'askall' :
            tree = ET.Element("all")
            elt = ET.SubElement(tree, "grille")
            elt.text = str(self.gr)
            elt = ET.SubElement(tree, "tour_on")
            elt.text = str(self.tour_on)
            elt = ET.SubElement(tree, "tirage")
            if self.tour_on :
                elt.text = self.tirage.get_mot()
            elt = ET.SubElement(tree, "points_top")
            elt.text = str(self.points_top)
            xml = ET.tostring(tree)
            channel.envoi(msg.msg("all", xml))
        elif c == 'chat' :
            m = msg.msg("info", mm.param, nick)
            self.jo.envoi_all(m)
        elif c == "restart" :
            self.vote("restart", channel)
        elif c == "next" :
            self.vote("next", channel)
        elif c == "stopchrono" :
            self.vote("stopchrono", channel)
        elif c == 'askgrille' :
            channel.envoi(msg.msg("grille", str(self.gr)))
        elif c == 'asktour' :
            channel.envoi(msg.msg("tour", self.tour_on))

    def deconnect(self, channel) :
        nick = self.jo.deconnect(channel)
        if nick is not None :
            self.info("Deconnexion de %s" % nick)

    def info(self, txt) :
        m = msg.msg("info", txt)
        self.jo.envoi_all(m)

    def vote(self, categ, channel) :
        if categ in self.categ_vote :
            if channel not in self.votants[categ] :
                self.votes[categ] += 1
                self.votants[categ].append(channel)
                m = msg.msg("ok%s" % categ, self.votes[categ])
                self.jo.envoi_all(m)

    def init_vote(self) :
        for categ in self.categ_vote :
            self.raz_vote(categ)

    def raz_vote(self, categ) :
        if categ in self.categ_vote :
            self.votes[categ] = 0
            self.votants[categ] = []
            m = msg.msg("ok%s" % categ, self.votes[categ])
            self.jo.envoi_all(m)
