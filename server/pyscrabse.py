# -*- coding: utf-8 -*-
import time

import xml.etree.cElementTree as ET

from twisted.internet import reactor, defer
from twisted.internet.task import LoopingCall

import dico
import partie
import joueur
import logger
import msg
import grille
import tirage
import coord
import net

class main():
    def __init__(self, options) :
        self.options = options
        self.dic = dico.Dico(self.options.dico)
        self.jo = joueur.joueurs()
        self.categ_vote = ('restart', 'next', 'chrono')
        self.delta_calllater = 1
        self.votes = {}
        self.votants = {}

    def debut_game(self, attente=2) :
        self.partie_on = True
        self.tour_on = False
        self.chrono_on = False
        self.tirage = tirage.tirage("")
        self.points_top = 0
        self.chrono = self.options.chrono
        self.init_vote()
        self.pa = partie.partie(self.options)
        self.options.game = None
        if self.options.log :
            self.log = logger.logger(self.pa.get_nom_partie())
        self.gr = grille.grille()
        self.jo.score_raz()
        self.info("Prochaine partie dans %d secondes" % attente)
        reactor.callLater(attente, self.first_tour)

    def first_tour(self) :
        self.envoi_all(msg.msg("new"))
        print("-"*20, self.pa.get_nom_partie(),"-"*20)
        print(time.strftime('%A %d %B %Y %H:%M'))
        print(self.options)
        reactor.callLater(self.delta_calllater, self.debut_tour)

    def debut_tour(self) :
        if self.pa.liste :
            self.tirage, self.coord_mot_top, self.mot_top, self.pts_mot_top, self.num_tour = self.pa.liste.pop(0)
        else :
            self.fin_partie()
        self.jo.score_tour_zero()
        self.info("------------------------")
        self.info("Tour n°%d" % self.num_tour)
        if self.options.topping :
            self.info("Le top fait %d points" % self.pts_mot_top)
            self.points_top = self.pts_mot_top
        if self.options.log :
            self.log.debut_tour(self.num_tour)
        m = msg.msg("tirage", self.tirage.get_mot())
        self.envoi_all(m)
        self.tour_on = True
        self.init_vote()
        self.chrono = self.options.chrono
        self.loop_chrono = LoopingCall(self.decr_chrono)
        self.loop_chrono.start(1)

    def decr_chrono(self) :
        self.envoi_all(msg.msg("chrono", self.chrono))
        self.chrono -= 1
        if self.chrono >= 0 :
            self.chrono_on = True
        else :
            self.stop_chrono()
            reactor.callLater(self.delta_calllater, self.fin_tour)

    def fin_tour(self) :
        self.tour_on = False
        self.jo.check_tick()
        self.envoi_all(msg.msg("mot_top",(str(self.coord_mot_top), self.mot_top)))
        self.info("Top retenu : %s-%s (%d pts)" % (self.coord_mot_top, self.mot_top, self.pts_mot_top))
        if self.options.log :
            self.log.fin_tour(self.coord_mot_top, self.mot_top, self.pts_mot_top)
        print("%d/%d : %s - %s" % (len(self.jo.liste_actif()), len(self.jo), self.coord_mot_top, self.mot_top))
        self.gr.pose(self.coord_mot_top, self.mot_top)
        message = self.jo.score_fin_tour(self.pts_mot_top)
        if message != "" :
            self.info(message)
        self.envoi_all(msg.msg("score", self.jo.tableau_score()))
        if self.pa.liste :
            reactor.callLater(self.options.inter, self.debut_tour)
        else :
            reactor.callLater(self.delta_calllater, self.fin_partie)

    def fin_partie(self) :
        self.info("Fin de la partie")
        if self.options.log :
            self.log.fin_partie()
        if len(self.jo.liste_actif()) > 0  : # il y a des joueurs en début de tour
            reactor.callLater(self.delta_calllater, self.debut_game, self.options.attente)
        else :
            self.partie_on = False
            print("En attente")

    def traite_joueur(self, xxx_todo_changeme) :
        (channel, mm) = xxx_todo_changeme
        proto_client = mm.param[0]
        ret = self.jo.add_joueur(mm.nick, proto_client, channel)
        return channel, mm, ret

    def traite_joueur_ret(self, xxx_todo_changeme1) :
        (channel, mm, ret) = xxx_todo_changeme1
        proto_serv = net.PROTOCOL
        if ret == 1 :
            proto_client = mm.param[0]
            m = msg.msg("connect",(1,"Connexion OK", proto_serv))
            self.info("Connexion de %s" % mm.nick)
            if proto_client < proto_serv :
                txt = "Attention : mettre le programme à jour (%d/%d)" % (proto_client, proto_serv)
                channel.envoi(msg.msg("info", txt))
            elif proto_serv < proto_client :
                txt = "Attention : serveur ancien protocole (%d/%d)" % (proto_serv, proto_client)
                channel.envoi(msg.msg("info", txt))
        elif ret == 0 :
            m = msg.msg("connect",(0,"Erreur : nom existant", proto_serv))
            self.info("Tentative de %s" % mm.nick)
        elif ret == 2 :
            m = msg.msg("connect",(2,"Reconnexion", proto_serv))
            self.info("Reconnexion de %s" % mm.nick)
        return channel, m

    def traite_propo(self, xxx_todo_changeme2) :
        # une proposition active le 'tick'
        (channel, mm) = xxx_todo_changeme2
        self.jo.set_tick(mm.nick, channel)
        coo_str = mm.param[0]
        mot = mm.param[1]
        tir = self.tirage
        coo = coord.coord(coo_str=coo_str)
        controle = self.gr.controle(coo, mot, tir)
        return channel, mm, controle, coo

    def traite_propo_controle(self, xxx_todo_changeme3) :
        (channel, mm, controle, coo) = xxx_todo_changeme3
        mot = mm.param[1]
        if controle <= 0 :
            point, mot_nonex  = self.gr.point(coo, mot, controle == -1, self.dic)
            self.jo.set_msg_fin_tour(mm.nick, mot_nonex)
            score = point
            m = msg.msg("valid",(str(coo), mot, point))
            if len(mot_nonex) > 0 :
                # met le score a 0 si non existant
                score = 0
            self.jo.set_points_tour(mm.nick, score)
            if self.options.log :
                self.log.add_prop(mm.nick, coo, mot, score, self.options.chrono - self.chrono)
        else:
            m = msg.msg("error","Erreur %d : %s" % (controle, self.gr.aff_erreur(controle)))
        return channel, m

    def traite_askall(self, xxx_todo_changeme4) :
        (channel, mm) = xxx_todo_changeme4
        tree = ET.Element("all")
        elt = ET.SubElement(tree, "grille")
        elt.text = str(self.gr)
        elt = ET.SubElement(tree, "tour_on")
        elt.text = str(self.tour_on)
        elt = ET.SubElement(tree, "partie_on")
        elt.text = str(self.partie_on)
        elt = ET.SubElement(tree, "tirage")
        if self.tour_on :
            elt.text = self.tirage.get_mot()
        elt = ET.SubElement(tree, "points_top")
        elt.text = str(self.points_top)
        xml = ET.tostring(tree)
        m = msg.msg("all", xml)
        return channel, m

    def traite_askinfo(self, xxx_todo_changeme5) :
        (channel, mm) = xxx_todo_changeme5
        proto, score, top, pct, message = self.jo.get_infos_joueur(mm.nick)
        if self.tour_on :
            message = []
        m = msg.msg("infojoueur", (score, top, pct, message))
        return channel, m

    def traite_askscore(self, xxx_todo_changeme6) :
        (channel, mm) = xxx_todo_changeme6
        m = msg.msg("score", self.jo.tableau_score())
        return channel, m

    def traite_chat(self, xxx_todo_changeme7) :
        (channel, mm) = xxx_todo_changeme7
        m = msg.msg("info", mm.param, mm.nick)
        self.envoi_all(m)

    def traite_tick(self, xxx_todo_changeme8) :
        (channel, mm) = xxx_todo_changeme8
        self.jo.set_tick(mm.nick, channel)

    def traite(self, cmd) :
        if cmd == 'joueur' :
            self.traite_joueur
            self.traite_joueur_ret
            self.envoi_msg
        elif cmd == 'propo' and self.tour_on :
            self.traite_propo
            self.traite_propo_controle
            self.envoi_msg
        elif cmd == 'askscore' :
            self.traite_askscore
            self.envoi_msg
        elif cmd == 'askinfo' :
            self.traite_askinfo
            self.envoi_msg
        elif cmd == 'askall' :
            self.traite_askall
            self.envoi_msg
        elif cmd == 'chat' :
            self.traite_chat
        elif cmd == "vote" :
            self.traite_vote
        elif cmd == "tick" :
            self.traite_tick

    def deconnect(self, channel) :
        nick = self.jo.deconnect(channel)
        if nick is not None :
            self.info("Déconnexion de %s" % nick)

    def info(self, txt) :
        m = msg.msg("info", txt)
        self.envoi_all(m)

    def envoi_msg(self, xxx_todo_changeme9) :
        (channel, message) = xxx_todo_changeme9
        channel.envoi(message)

    def envoi_all(self, message) :
        d = defer.Deferred()
        for j in self.jo.liste_envoi() :
            d.addCallback(j.channel.envoi)
        reactor.callLater(0, d.callback, message)

    def stop_chrono(self) :
        self.chrono_on = False
        if self.loop_chrono.running :
            self.loop_chrono.stop()

    def traite_vote(self, xxx_todo_changeme10) :
        (channel, mm) = xxx_todo_changeme10
        categ = mm.param[0]
        # vote inactif hors des tours de jeu
        if not self.tour_on :
            return
        # vote hors catégorie
        if categ not in self.categ_vote :
            return
        # a déjà voté dans cette catégorie, on dégage
        if channel in self.votants[categ] :
            return
        # plus de vote à moins de 2s de la fin du tour
        if self.chrono < 2 :
            return
        # pour qu'un vote next ou restart passe,
        # il faut qu'il y ait plus de voix que d'actifs au début du tour
        # et d'actifs au moment du vote (et plus de 1)
        limite = max(1, len(self.jo.liste_actif()))
        self.votes[categ] += 1
        self.votants[categ].add(channel)
        m = msg.msg("okvote", (categ, self.votes[categ]))
        self.envoi_all(m)

        if self.votes['restart'] >= limite :
            # vote restart accepté
            self.stop_chrono()
            self.tour_on = False
            reactor.callLater(self.delta_calllater, self.debut_game)
        if self.votes['next'] >= limite :
            self.stop_chrono()
            self.envoi_all(msg.msg("chrono", 0))
            reactor.callLater(self.delta_calllater, self.fin_tour)
        if self.votes['chrono'] >= 1:
            self.chrono += 15
            self.raz_vote('chrono')

    def init_vote(self) :
        for categ in self.categ_vote :
            self.raz_vote(categ)

    def raz_vote(self, categ) :
        if categ in self.categ_vote :
            self.votes[categ] = 0
            self.votants[categ] = set()
            m = msg.msg("okvote", (categ, self.votes[categ]))
            self.envoi_all(m)
