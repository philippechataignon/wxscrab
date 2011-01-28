#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Reglage encoding
import sys
sys.path.append('../common')
import wx
import settings
import frame
import frame_score
import dlgconn
import son
import net
import utils
import reliquat
import jeton
import msg

class App(wx.App):
    def OnInit(self) :
        wx.InitAllImageHandlers()
        self.connected = False
        self.settings = settings.settings()
        # Crée la frame principale
        self.frame = frame.frame(None, self)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        self.score = frame_score.frame_score(self.frame, "")
        self.score.Show(False)
        self.son = son.son()
        self.tour_on = False
        self.t1 = wx.Timer(self)
        # Appelle la frame de connexion au début
        self.d = dlgconn.dlgconnframe(self.frame, self)
        self.d.Show()
        self.d.MakeModal(True)
        self.reliquat = reliquat.reliquat()
        return True

    def lance_net(self) :
        # Appelé en sortie de la dlgconn
        self.net  = net.net(self, self.host, self.port)
        self.t1.Start(100)
        self.Bind(wx.EVT_TIMER, self.net.watchnet)

## Fonctions basiques
    def envoi(self, txt) :
        txt.set_id(self.nick)
        self.net.envoi_net(txt)
        
    def bascule_score(self) :
        if self.score.IsShown() :
            self.score.Show(False)
        else :
            self.score.Show(True)

    def info_serv(self, txt, color = wx.BLACK) :
        self.frame.info_serv(txt, color)

    def debut_partie(self) :
        # vide tirage pour mettre jeton dans reliquat
        self.frame.tirage.vide_tirage()
        # pour la grille, les jetons sont remis dans le reliquat par read_grille
        self.envoi(msg.msg("askgrille"))
        self.envoi(msg.msg("askinfo"))
        self.envoi(msg.msg("askscore"))

## Traitement des messages reçus
    def traite(self, m) :
        # print "Traite %s %s %s" % (m.cmd, m.param, m.id)
        f = self.frame
        g = f.grille
        t = f.tirage
        if m.cmd == 'connect' :
            if m.param[0] == 0 :
                utils.errordlg(m.param[1],"Erreur : nom existant")
                f.Close()
            elif m.param[0] == 1 :
                self.info_serv("Connexion établie", wx.NamedColor("DARK GREEN"))
            elif m.param[0] == 2 :
                self.info_serv("Reconnexion établie", wx.NamedColor("DARK GREEN"))
            self.settings.write()
            self.connected = True
            self.debut_partie()
            self.envoi(msg.msg("asktour"))

        # pas d'analyse des commandes si non connecté (sauf connect)
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
            f.buttonpose.Enable(True)
            f.home_props()
            f.set_status_reliq()
        elif m.cmd == 'chrono' :
            temps = m.param
            if temps > 0 :
                self.tour_on = True
            f.timer.SetLabel(utils.convert_time(temps))
            if temps == 0 :
                self.envoi(msg.msg("tick"))
        elif m.cmd == 'error' :
            utils.errordlg(m.param,"Erreur")
        elif m.cmd == 'mot_top' :
            #Fin du tour
            self.tour_on = False
            f.buttonpose.Enable(False)
            g.reinit_saisie()
            self.son.play("fin_tour")
            coord, mot = m.param
            g.pose_mot(coord, mot, status=jeton.PREPOSE)
            #Questionner serveur pour pts et message mot
            self.envoi(msg.msg("askinfo"))
        elif m.cmd == 'grille' :
            g.read_grille(m.param)
        elif m.cmd == 'new' :
            self.info_serv("="*20, wx.NamedColor("DARK GREEN"))
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
            self.score = frame_score.frame_score(f, m.param)
            if not self.tour_on :
                self.score.Show(True)
        elif m.cmd == 'valid' :
            self.son.play("valid")
            coo, mot, pts = m.param
            txt ="%s - %s  (%s pts)" % (coo, mot, pts)
            self.info_serv(">>  " + txt, wx.BLUE)
            f.insert_props(txt, (coo, mot))
        elif m.cmd == 'infojoueur' :
           total, top, prc, mess = m.param
           f.score.SetLabel("%s/%s - %5.1f%%" % (total, top, prc))
           for m in  mess :
               self.info_serv("Mot non existant : %s" % m, wx.RED)
        elif m.cmd == "oknext" :
            f.set_status_next(int(m.param))
        elif m.cmd == "okrestart" :
            f.set_status_restart(int(m.param))
