# -*- coding: utf-8 -*-

#Reglage encoding
import sys
sys.path.append('../common')
import wx
import xml.etree.ElementTree as ET

from twisted.internet import reactor, defer,  _threadedselect

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


class App(wx.App):
    title = "wxScrab"
    def OnInit(self) :
        wx.InitAllImageHandlers()
        self.connected = False
        self.settings = settings.settings()
        # Crée la frame principale
        self.frame = frame.frame(None, self, App.title)
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
        self.net = net.ScrabbleFactory(self)
        reactor.connectTCP(self.host, self.port, self.net)

    def exit(self, evt=None) :
        self.onExit = True
        reactor._stopping = True
        reactor.callFromThread(_threadedselect.ThreadedSelectReactor.stop, reactor)

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
    def envoi(self, msg) :
        msg.set_nick(self.nick)
        self.net.envoi(msg)


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
    def traite_info(self, m) :
        txt = m.param
        nick  = m.nick
        if nick is None :
            self.info_serv(txt)
        elif nick == "" :
            self.info_serv(txt, wx.BLUE)
        else :
            self.info_serv("[%s] %s" % (nick, txt), wx.NamedColor("DARK GREEN"))

    def traite_tirage(self, m) :
        self.score.Show(False)
        self.frame.tirage.cree_tirage(m.param)
        return m

    def traite_tirage_grille(self, m) :
        f = self.frame
        f.grille.reinit_saisie()
        f.grille.convert_prepose()
        f.buttonpose.Enable()
        f.home_props()
        f.set_status_reliq()
        reactor.callLater(0.2, self.envoi_msg, "tick")

    def traite_chrono(self, m) :
        f = self.frame
        temps = m.param
        if temps > 0 :
            self.tour_on = True
        f.timer.SetLabel(utils.convert_time(temps))
        if temps == 0 :
            reactor.callLater(0.2, self.envoi_msg, "tick")
            
    def traite_mot_top(self, m) :
        f = self.frame
        #Fin du tour
        self.tour_on = False
        f.buttonpose.Enable(False)
        f.grille.reinit_saisie()
        coo, mot = m.param
        f.grille.pose_mot(coo, mot, status=jeton.PREPOSE)
        reactor.callLater(0.2, self.envoi_msg, "askinfo")

    def traite_new(self, m) :
        f = self.frame
        self.info_serv("="*20, wx.NamedColor("DARK GREEN"))
        self.info_serv("Nouvelle partie", wx.NamedColor("DARK GREEN"))
        self.score.Show(False)
        f.grille.vide_grille()
        reactor.callLater(0.2, self.envoi_msg, "askinfo")
        reactor.callLater(0.4, self.envoi_msg, "askscore")

    def traite_score(self, m) :
        self.score.Destroy()
        self.score = frame_score.frame_score(self.frame, m.param)
        if not self.tour_on :
            self.score.Show(True)

    def traite_valid(self, m) :
        coo, mot, pts = m.param
        txt ="%s - %s  (%s pts)" % (coo, mot, pts)
        self.info_serv(">>  " + txt, wx.BLUE)
        f = self.frame
        f.insert_props(txt, (coo, mot))

    def traite_infojoueur(self, m) :
        f = self.frame
        total, top, prc, mess = m.param
        f.score.SetLabel("%s/%s - %5.1f%%" % (total, top, prc))
        for m in  mess :
            self.info_serv("Mot non existant : %s" % m, wx.RED)

    def traite_okvote(self, m) :
        f = self.frame
        categ, num = m.param
        if categ  == "next" :
            f.set_status_next(num)
        elif categ == "restart" :
            f.set_status_restart(num)

    def traite_all(self, m) :
        # vide tirage pour mettre jeton dans reliquat
        f = self.frame
        f.tirage.vide_tirage()
        tree = ET.XML(m.param)
        gr = tree.find("grille")
        # read_grille met les jetons de la grille dans le reliquat
        # puis les reprend pour créer la grille
        f.grille.read_grille(gr.text)
        gr = tree.find("points_top")
        pts_top = int(gr.text)
        if pts_top > 0 :
            self.info_serv("Le top fait %d points" % pts_top)
        gr = tree.find("tour_on")
        self.tour_on = (gr.text == 'True')
        gr = tree.find("tirage")
        if gr.text is not None :
            f.tirage.cree_tirage(str(gr.text))
        if self.tour_on :
            f.buttonpose.Enable()
            f.home_props()
            f.set_status_reliq()
        else :
            self.info_serv("En attente du prochain tour")

    def traite_error(self, m) :
        utils.errordlg(m.param,"Erreur")

    def traite_serverok(self, m) :
        self.info_serv("Serveur OK", wx.NamedColor("DARK GREEN"))
        self.frame.SetTitle(App.title + ' - ' + self.nick)

    def traite_connect(self, m) :
        f = self.frame
        if m.param[0] == 0 :
            utils.errordlg(m.param[1],"Erreur : nom existant")
            f.Close()
        elif m.param[0] == 1 :
            self.info_serv("Connexion établie", wx.NamedColor("DARK GREEN"))
        elif m.param[0] == 2 :
            self.info_serv("Reconnexion établie", wx.NamedColor("DARK GREEN"))
        self.settings.write()
        self.connected = True
        reactor.callLater(0.1, self.envoi_msg, "askall")
        reactor.callLater(0.2, self.envoi_msg, "askinfo")
        reactor.callLater(0.4, self.envoi_msg, "askscore")

    def envoi_msg(self, cmd) :
        self.envoi(msg.msg(cmd))

    def traite(self, cmd) :
        d = defer.Deferred()
        if cmd == 'serverok' :
            d.addCallback(self.traite_serverok)
        elif cmd == 'connect' :
            d.addCallback(self.traite_connect)
        # analyse des commandes si connecté (sauf connect et serverok)
        if self.connected :
            if cmd == 'info' :
                d.addCallback(self.traite_info)
            elif cmd == 'tirage' :
                d.addCallback(self.son.play_debut)
                d.addCallback(self.traite_tirage)
                d.addCallback(self.traite_tirage_grille)
            elif cmd == 'chrono' :
                d.addCallback(self.traite_chrono)
            elif cmd == 'error' :
                d.addCallback(self.traite_error)
            elif cmd == 'mot_top' :
                d.addCallback(self.son.play_fin_tour)
                d.addCallback(self.traite_mot_top)
            elif cmd == 'new' :
                d.addCallback(self.traite_new)
            elif cmd == 'score' :
                d.addCallback(self.traite_score)
            elif cmd == 'valid' :
                d.addCallback(self.son.play_valid)
                d.addCallback(self.traite_valid)
            elif cmd == 'infojoueur' :
                d.addCallback(self.traite_infojoueur)
            elif cmd == "okvote" :
                d.addCallback(self.traite_okvote)
            elif cmd == "all" :
                d.addCallback(self.traite_all)
        return d
