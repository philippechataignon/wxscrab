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
import skin
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
        self.settings = settings.settings()
        # Appelle la frame de connexion au début
        dlgconn.dlgconnframe(None, self)
        return True

## Création

    def cree_all(self, nick, sock, status) :
        """
        Crée les objets de base du client

        Fonction appelée en sorte de dlgconn
        """
        self.skin = skin.skin(self.settings.get("skin"))
        self.nick = nick
        self.frame = frame.frame(None, self)
        self.frame.Show()
        self.net  = net.net(sock, self)
        self.son = son.son()
        self.t1 = wx.Timer(self)
        self.t1.Start(100)
        self.Bind(wx.EVT_TIMER, self.watchnet)
        self.score = frame_score.frame_score(self.frame, "")
        self.score.Show(False)
        if status == '1' :
            self.info_serv("Connexion établie", wx.NamedColor("DARK GREEN"))
        elif status == '2' :
            self.info_serv("Reconnexion établie", wx.NamedColor("DARK GREEN"))
        self.tour_on = False
        self.debut_partie()

## Fonctions basiques

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

    def OnClickCase(self, case) :
        f = self.frame
        g = f.grille
        if g.saisie_ok == False :
            return
        t = f.tirage

        if case.fleche == coord.NUL :
            g.reinit_saisie()
            f.home_props()
            case.fleche = coord.HOR
            case.coord.set_hor()
            g.entry = 0 
            g.coord_ini = case.coord
            f.set_status_text( "%s" % case.coord ) 
        elif case.fleche == coord.HOR :
            case.fleche = coord.VER
            case.coord.set_ver()
            g.coord_ini = case.coord
            f.set_status_text( "%s" % case.coord ) 
        else  :
            case.fleche = coord.NUL
            g.coord_ini = coord.coord()
            f.set_status_text( "" )
        case.redraw()
        g.SetFocus()

    def OnExit(self) :
        try :
            self.t1.Stop()
        except :
            pass
