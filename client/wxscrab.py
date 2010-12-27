#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Reglage encoding
import sys
sys.path.append('../common')
import wx
import settings
import frame
import net
import dlgconn
import frame_score
import utils
import reliquat
import asyncore
import jeton
import son
import time
import msg
import coord

class App(wx.App):
    def OnInit(self) :
        wx.InitAllImageHandlers()
        self.connected = False
        self.t1 = wx.Timer(self)
        self.settings = settings.settings()
        #self.skin = skin.skin(self.settings.get("skin"))
        # Appelle la frame de connexion au début
        self.frame = frame.frame(None, self)
        self.d = dlgconn.dlgconnframe(None, self)
        self.d.Show()
        self.d.MakeModal(True)
        return True

## Fonctions basiques
    def cree(self) :
        self.frame.Show()
        self.d.Close()
        self.net  = net.net(self, self.host, self.port)
        self.son = son.son()
        self.t1.Start(100)
        self.Bind(wx.EVT_TIMER, self.watchnet)
        self.score = frame_score.frame_score(self.frame, "")
        self.score.Show(False)
        self.tour_on = False


    def envoi(self, txt) :
        txt.set_id(self.nick)
        self.net.envoi_net(txt)
        
    def watchnet(self, e) :
        asyncore.poll()

    def bascule_score(self) :
        if self.score.IsShown() :
            self.score.Show(False)
        else :
            self.score.Show(True)

    def info_serv(self, txt, color = wx.BLACK) :
        self.frame.info_serv(txt, color)

    def debut_partie(self) :
        # vide tirage pour eviter pb reliquat
        self.frame.tirage.vide_tirage()
        self.reliquat = reliquat.reliquat()
        self.envoi(msg.msg("askgrille"))
        self.envoi(msg.msg("askinfo"))
        self.envoi(msg.msg("askscore"))
        self.envoi(msg.msg("asktour"))

## Traitement des messages reçus

    def traite(self, m) :
        # print "Traite %s %s %s" % (m.cmd, m.param, m.id)
        g = self.frame.grille
        t = self.frame.tirage
        if m.cmd == 'connect' :
            if m.param[0] == 0 :
                utils.errordlg(m.param[1],"Erreur : nom existant")
                self.frame.Close()
            elif m.param[0] == 1 :
                self.info_serv("Connexion établie", wx.NamedColor("DARK GREEN"))
            elif m.param[0] == 2 :
                self.info_serv("Reconnexion établie", wx.NamedColor("DARK GREEN"))
            self.settings.write()
            self.connected = True
            self.debut_partie()

        # analyse pas les commandes si non connecté
        if not self.connected :
            return

        if m.cmd == 'info' :
            txt = m.param
            id  = m.id
            if id is None :
                self.info_serv(txt)
            elif id == "" :
                self.info_serv(txt, wx.BLUE)
            else :
                self.info_serv("[%s] %s" % (id, txt), wx.NamedColor("DARK GREEN"))
        elif m.cmd == 'tirage' :
            self.score.Show(False)
            self.son.play("debut")
            g.reinit_saisie()
            g.convert_prepose()
            t.cree_tirage(m.param)
            self.frame.buttonpose.Enable(True)
            self.frame.home_props()
            t.allowdrags(True)
            self.frame.upd_status()
        elif m.cmd == 'chrono' :
            temps = m.param
            if temps > 0 :
                g.saisie_ok = True
                self.tour_on = True
            self.frame.timer.SetLabel(utils.convert_time(temps))
            if temps == 0 :
                self.envoi(msg.msg("tick"))
        elif m.cmd == 'error' :
            utils.errordlg(m.param,"Erreur")
        elif m.cmd == 'mot_top' :
            #Fin du tour
            self.tour_on = False
            t.allowdrags(False)
            g.saisie_ok = False
            self.frame.buttonpose.Enable(False)
            g.reinit_saisie()
            self.son.play("fin_tour")
            coord, mot = m.param
            g.pose_mot(coord, mot, status=jeton.PREPOSE)
            #Questionner serveur pour pts et message mot
            self.envoi(msg.msg("askinfo"))
        elif m.cmd == 'grille' :
            g.read_grille(m.param)
        elif m.cmd == 'new' :
            self.frame.efface_msgs()
            self.info_serv("Nouvelle partie", wx.NamedColor("DARK GREEN"))
            self.score.Show(False)
            self.debut_partie()
        elif m.cmd == 'tour' :
            self.tour_on = m.param
            if self.tour_on :
                self.envoi(msg.msg("asktirage"))
            else:
                self.info_serv("En attente du prochain tour")
        elif m.cmd == 'score' :
            self.score.Close()
            self.score = frame_score.frame_score(self.frame, m.param)
            if not self.tour_on :
                self.score.Show(True)
        elif m.cmd == 'valid' :
            self.son.play("valid")
            coo, mot, pts = m.param
            txt ="%s - %s  (%s pts)" % (coo, mot, pts)
            self.info_serv(">>  " + txt, wx.BLUE)
            self.frame.insert_props(txt, (coo, mot))
        elif m.cmd == 'infojoueur' :
           total, top, prc, mess = m.param
           self.frame.score.SetLabel("%s/%s - %5.1f%%" % (total, top, prc))
           for m in  mess :
               self.info_serv("Mot non existant : %s" % m, wx.RED)
        elif m.cmd == "oknext" :
            self.frame.set_status_next(int(m.param))
        elif m.cmd == "okrestart" :
            self.frame.set_status_restart(int(m.param))

## Gestionnaires événements

    def OnExit(self) :
        self.t1.Stop()
