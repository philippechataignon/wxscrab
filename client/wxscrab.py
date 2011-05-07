#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Reglage encoding
import sys
sys.path.append('../common')
import wx
import xml.etree.ElementTree as ET

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
import net

from twisted.internet import reactor

class App(wx.App):
    def OnInit(self) :
        wx.InitAllImageHandlers()
        self.connected = False
        self.settings = settings.settings()
        # Crée la frame principale
        self.frame = frame.frame(None, self)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        self.score = frame_score.frame_score(self.frame)
        self.score.Show(False)
        self.son = son.son()
        self.tour_on = False
        self.t1 = wx.Timer(self)
        # Appelle la frame de connexion au début
        self.d = dlgconn.dlgconnframe(self.frame, self)
        self.d.Show()
        self.d.MakeModal(True)
        self.reliquat = reliquat.reliquat()
        self.onExit = False
        return True

    def lance_net(self) :
        # Appelé en sortie de la dlgconn
        self.net = net.ScrabbleFactory(self, self.nick)
        reactor.connectTCP(self.host, self.port, self.net)

    def OnExit(self) :
        self.onExit = True
        reactor.stop()

## Gestion des évenements clavier
    def OnKey(self, e) :
        """ Gère les événements clavier en provenance de la case_grille
        Raccourcis clavier ou lettre
        """
        f = self.frame
        g = f.grille
        l = e.GetKeyCode()
        if l is None or self.tour_on == False :
            return
        if l == wx.WXK_RETURN or l == wx.WXK_NUMPAD_ENTER :
            self.envoi_mot()
        elif l == wx.WXK_BACK :
            g.recule_case()
        elif l == wx.WXK_ESCAPE :
            g.reinit_saisie()
        elif l == wx.WXK_DELETE :
            f.button_pose_last(e)
        # control
        elif e.ControlDown() :
            if l == 88 : # ctrl-x
                f.button_pose_last(e)
            elif l == 78 : #ctrl-n
                f.button_next(e)
            elif l == 65 : #crtl-a
                f.button_alpha(e)
            elif l == 82 : #crtl-r
                f.button_random(e)
            elif l == 83 : #crtl-s
                f.show_score(e)
        elif (ord('A') <= l <= ord('Z') or ord('a') <= l <= ord('z')):
            if e.ShiftDown() :
                l += 32
            g.traite_keycode(chr(l))

## Fonctions basiques
    def envoi(self, txt) :
        txt.set_id(self.nick)
        self.net.envoi_net(txt)

    def envoi_mot(self) :
        "Envoie le mot courant au serveur"
        g = self.frame.grille
        debut, mot = g.get_mot_temp()
        if mot is not None :
            m = msg.msg("propo", (str(debut), mot, 0))
            self.envoi(m)
        g.reinit_saisie()
        
    def info_serv(self, txt, color = wx.BLACK) :
        self.frame.info_serv(txt, color)


## Traitement des messages reçus
    def traite(self, dump) :
        m = msg.msg(dump=dump)
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
            self.envoi(msg.msg("askall"))
            self.envoi(msg.msg("askinfo"))
            self.envoi(msg.msg("askscore"))

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
            coo, mot = m.param
            g.pose_mot(coo, mot, status=jeton.PREPOSE)
            #Questionner serveur pour pts et message mot
            self.envoi(msg.msg("askinfo"))
        elif m.cmd == 'new' :
            self.info_serv("="*20, wx.NamedColor("DARK GREEN"))
            self.info_serv("Nouvelle partie", wx.NamedColor("DARK GREEN"))
            self.score.Show(False)
            g.vide_grille()
            self.envoi(msg.msg("askinfo"))
            self.envoi(msg.msg("askscore"))

        elif m.cmd == 'score' :
            self.score.Destroy()
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
        elif m.cmd == "okvote" :
            categ, num = m.param
            if categ  == "next" :
                f.set_status_next(num)
            elif categ == "restart" :
                f.set_status_restart(num)
        elif m.cmd == "all" :
            # vide tirage pour mettre jeton dans reliquat
            t.vide_tirage()
            tree = ET.XML(m.param)
            gr = tree.find("grille")
            # read_grille met les jetons de la grille dans le reliquat
            # puis les reprend pour créer la grille
            g.read_grille(gr.text)
            gr = tree.find("points_top")
            pts_top = int(gr.text)
            if pts_top > 0 :
                self.info_serv("Le top fait %d points" % pts_top)
            gr = tree.find("tour_on")
            self.tour_on = (gr.text == 'True')
            gr = tree.find("tirage")
            if gr.text is not None :
                t.cree_tirage(str(gr.text))
            if self.tour_on :
                f.buttonpose.Enable(True)
                f.home_props()
                f.set_status_reliq()
            else :
                self.info_serv("En attente du prochain tour")
