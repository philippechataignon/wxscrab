#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import optparse
import sys
import threading
import asyncore

import dico

import partie
import joueur
import logger
import msg
import grille
import net
import time

#Reglage encoding
reload(sys)
sys.setdefaultencoding('utf8')

class Stop(Exception) :
    pass

class Restart(Exception) :
    pass

class Next(Exception) :
    pass

class main(threading.Thread):
    def __init__(self, options) :
        threading.Thread.__init__(self)
        self.options = options
        self.net = net.net(self.options.port, self)
        self.dic = dico.dico(self.options.dico)
        self.jo = joueur.joueurs()
        self.chrono = self.options.chrono
        self.tour_on = False
        self.attention = threading.Event()
        self.categ_vote = ('restart', 'next')
        self.votes = {}
        self.votants = {}
        self.lock_vote = threading.Lock()
        self.init_vote()
        self.stop = False

    def run(self, f_attente=True) :
        self.boucle_game()

    def boucle_game(self, f_attente=True) :
        while True :
            try :
                self.pa = partie.partie(self.options)
                self.options.game = None
                self.log = logger.logger(self.pa.get_nom_partie())
                self.gr = grille.grille()
                self.jo.score_raz()
                if f_attente :
                    self.info("Prochaine partie dans %d secondes" % self.options.attente)
                    self.attente(self.options.attente)
                self.net.envoi_all(msg.msg("new"))
                for self.tirage, coord_mot_top, mot_top, pts_mot_top, num_tour in self.pa.liste :
                    self.debut_tour(coord_mot_top, mot_top, pts_mot_top, num_tour)
                    self.attente(self.options.inter)
                self.info("Fin de la partie")
                self.log.fin_partie()
            except Restart :
                f_attente = False
            except Next :
                pass
            else :
                f_attente = True

    def attente(self, tps) :
        self.attention.wait(tps)
        if self.attention.isSet() :
            self.attention.clear()
            if self.stop :
                raise Stop
            if self.votes['restart'] == len(self.jo) :
                self.lock_vote.acquire()
                self.votes['restart'] = 0
                self.lock_vote.release()
                raise Restart
            if self.votes['next'] == len(self.jo) and self.tour_on :
                self.lock_vote.acquire()
                self.votes['next'] = 0
                self.lock_vote.release()
                raise Next

    def debut_tour(self, coord_mot_top, mot_top, pts_mot_top, num_tour) :
        self.jo.score_tour_zero()
        self.info("------------------------")
        self.info("Tour n°%d" % num_tour)
        self.log.debut_tour(num_tour)
        m = msg.msg("tirage", self.tirage.get_mot())
        self.net.envoi_all(m)
        self.tour_on = True
        self.chrono = self.options.chrono
        self.init_vote()
        while self.chrono >= 0 :
            self.net.envoi_all(msg.msg("chrono", self.chrono))
            try :
                self.attente(1)
            except Next :
                self.chrono = 1
            self.chrono -= 1
        self.tour_on = False
        self.net.envoi_all(msg.msg("mot_top",(coord_mot_top, mot_top)))
        self.info("Top retenu : %s-%s (%d pts)" % (coord_mot_top, mot_top, pts_mot_top))
        self.log.fin_tour(coord_mot_top, mot_top, pts_mot_top)
        print("%s - %s" % (coord_mot_top, mot_top))
        self.gr.pose(coord_mot_top, mot_top)
        message = self.jo.score_fin_tour(pts_mot_top)
        if message != "" :
            self.info(message)
        self.net.envoi_all(msg.msg("score", self.jo.tableau_score()))
        return False

    def traite(self, channel, mm) :
        c = mm.cmd
        nick  = mm.id
        # print "Traite %s %s %s" % (mm.cmd, mm.param, mm.id)
        if c == 'joueur' :
            if mm.param == mm.id :
                proto = 0
            else :
                proto = mm.param[0]
            ret = self.jo.add_joueur(nick, proto, channel)
            if ret == 1 :
                m = msg.msg("connect",(1,"Connexion OK"))
                channel.envoi(m)
                self.info("Connexion de %s" % nick)
            elif ret == 0 :
                m = msg.msg("connect",(0,"Erreur : nom existant"))
                channel.envoi(m)
                self.info("Tentative de %s" % nick)
            elif ret == 2 :
                m = msg.msg("connect",(2,"Reconnexion"))
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
        elif c == 'askgrille' :
            channel.envoi(msg.msg("grille", str(self.gr)))
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
        elif c == 'asktour' :
            channel.envoi(msg.msg("tour", self.tour_on))
        elif c == 'chat' :
            m = msg.msg("info", mm.param, mm.id)
            self.net.envoi_all(m)
        elif c == "restart" :
            self.vote("restart", channel)
        elif c == "next" :
            self.vote("next", channel)

    def deconnect(self, channel) :
        nick = self.jo.deconnect(channel)
        if nick is not None :
            self.info("Deconnexion de %s" % nick)

    def info(self, txt) :
        m = msg.msg("info", txt)
        self.net.envoi_all(m)

    def vote(self, categ, channel) :
        if categ in self.categ_vote :
            self.lock_vote.acquire()
            if channel not in self.votants[categ] :
                self.votes[categ] += 1
                self.votants[categ].append(channel)
            self.lock_vote.release()
            self.attention.set()
        else :
            print "Erreur categ vote"

    def init_vote(self) :
        self.lock_vote.acquire()
        for categ in self.categ_vote :
            self.votes[categ] = 0
            self.votants[categ] = []
        self.lock_vote.release()

if __name__ == '__main__' :
    usage = "usage: %prog [options] [fichier_partie]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-g", "--game", dest="game",default=None,
                      help="indique le fichier partie (defaut partie generee)")
    parser.add_option("-d", "--dico", dest="dico",default="../dic/ods5.dawg",
                      help="indique le fichier dictionnaire (defaut ../dic/ods5.dawg)")
    parser.add_option("-c", "--chrono", dest="chrono",type="int",default=120,
                      help="indique le temps par tour en secondes (defaut 2mn)")
    parser.add_option("-i", "--inter", dest="inter",type="int",default=15,
                      help="indique le temps entre chaque tour en secondes (defaut 15s)")
    parser.add_option("-p", "--port", dest="port",type="int",default=1989,
                      help="indique le port du serveur (defaut 1989)")
    parser.add_option("-a", "--attente", dest="attente",type="int",default=15,
                      help="temps attente pour debut de partie (defaut 15s)")
    parser.add_option("-v", "--verbose", dest="verbose",  \
            action="store_true", help="sortie des echanges reseau")
    (options, args) = parser.parse_args()
    print options
    g = main(options)
    g.start()
    delai = 0.1
    while not g.stop :
        try :
            g.net.lock.acquire()
            asyncore.poll()
            g.net.lock.release()
            time.sleep(delai)
        except KeyboardInterrupt:
            g.attention.set()
            g.stop = True
            print "KeyboardInterrupt"
