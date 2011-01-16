#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import case_grille
import coord
import jeton
import msg

OO = 0
LD = 1
LT = 2
MD = 3
MT = 4

mult =   ((MT,OO,OO,LD,OO,OO,OO,MT,OO,OO,OO,LD,OO,OO,MT),
          (OO,MD,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,MD,OO),
          (OO,OO,MD,OO,OO,OO,LD,OO,LD,OO,OO,OO,MD,OO,OO),
          (LD,OO,OO,MD,OO,OO,OO,LD,OO,OO,OO,MD,OO,OO,LD),
          (OO,OO,OO,OO,MD,OO,OO,OO,OO,OO,MD,OO,OO,OO,OO),
          (OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO),
          (OO,OO,LD,OO,OO,OO,LD,OO,LD,OO,OO,OO,LD,OO,OO),
          (MT,OO,OO,LD,OO,OO,OO,MD,OO,OO,OO,LD,OO,OO,MT),
          (OO,OO,LD,OO,OO,OO,LD,OO,LD,OO,OO,OO,LD,OO,OO),
          (OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO),
          (OO,OO,OO,OO,MD,OO,OO,OO,OO,OO,MD,OO,OO,OO,OO),
          (LD,OO,OO,MD,OO,OO,OO,LD,OO,OO,OO,MD,OO,OO,LD),
          (OO,OO,MD,OO,OO,OO,LD,OO,LD,OO,OO,OO,MD,OO,OO),
          (OO,MD,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,MD,OO),
          (MT,OO,OO,LD,OO,OO,OO,MT,OO,OO,OO,LD,OO,OO,MT))

class grille(wx.Panel) :
    def __init__(self, parent, app) :
        wx.Panel.__init__(self, parent, -1)
        self.app = app
        self.cases = {}
        self.coord_ini = coord.coord()   # coord_ini est récupéré depuis case (OnClickCase)
        self.coord_cur = coord.coord()   # coordonnée courante 
        self.saisie_ok = False           # flag indiquant si on peut saisir (depend chrono)
        self.entry = False          # flag saisie en cours
        size = self.app.settings["size_jeton"]
        fill = self.app.settings["size_fill"]
        sizer = wx.GridBagSizer(hgap=0, vgap=0)
        sizer.Add( (2*fill,2*fill), pos=(0,0))
        sizer.Add( (fill,fill), pos=(16,16))
        for i in xrange(15) :
            t = str(i+1)
            sizer.Add(wx.StaticText(self, -1, t), pos=(0,i+1), flag=wx.ALIGN_CENTER)
            t = chr(65+i)
            sizer.Add(wx.StaticText(self, -1, t), pos=(i+1,0), flag=wx.ALIGN_CENTER)
        for y in range(15) :
            for x in range(15) :
                self.cases[(x,y)] = case_grille.case_grille(self, x, y, mult[x][y])
                sizer.Add(self.cases[(x,y)], pos=(y+1, x+1))
        self.SetSizer(sizer)
        self.Fit()

## Fonctions basiques

    def case_coord(self, coord) :
        "Renvoit la case correspond à la référence alpha, None si coord incorrecte"
        if coord.isOK():
            return self.cases[(coord.x(),coord.y())]
        else:
            return None

    def case_coord_vide(self, coord) :
        "Renvoit True si case OK et vide"
        if coord.isOK():
            return self.cases[(coord.x(),coord.y())].is_vide()
        else:
            return False 

    def case_coord_occ(self, coord) :
        "Renvoit True si case OK et occupee"
        if coord.isOK():
            return not self.cases[(coord.x(),coord.y())].is_vide()
        else:
            return False

## Fonctions utilitaires

    def convert_prepose(self) :
        "Les jetons préposés (reçus du serveur) sont mis en fixe"
        for case in self.cases.itervalues() :
            case.convert_prepose()

    def get_mot_temp(self) :
        """
        Convertit la position de début de saisie en coord debut et mot
        
        Appelé uniquement depuis envoi_mot

        Remonte les lettres situées à gauche pour le début ; idem à droite
        Renvoit None en cas de saisie incorrecte : mot vide ou début partie
        """
        mot = [] 
        if not self.coord_ini.isOK() :
            return (None, None)
        else :
            cur = self.coord_ini
            # Lettres à gauche
            while self.case_coord_occ(cur.prev()) :
                cur = cur.prev()
            debut = cur
            # Lettres à droite
            while self.case_coord_occ(cur) :
                mot.append(self.case_coord(cur).jeton.lettre)
                cur = cur.next()
            if mot == [] :
                return (None, None)
            else :
                return (debut, "".join(mot))

## Principales fonctions publiques

    def reinit_saisie(self) :
        "Enleve la fleche et les jetons temporaires de la grille (remis dans le tirage)"
        for case in self.cases.itervalues() :
            if case.fleche is not None :
                case.efface_fleche()
            if case.get_status() == jeton.TEMP : #si jeton temp
                self.app.frame.tirage.remet(case.jeton)
                case.vide()
        self.entry = False
        self.app.frame.set_status_coo("")
        self.coord_ini = coord.coord()

    def pose_mot(self, coo, mot, status) :
        """ Pose un mot sur la grille 
        Appelé pour le mot du Top pour permettre de le repérer (status = PREPOSE)
        Appelé depuis la box des propositions (status = TEMP)
        """
        for l in mot :
            if self.case_coord_vide(coo) :
                j = self.app.frame.tirage.retire_jeton(l)
                if j is not None :
                    j.set_status(status)
                    self.case_coord(coo).pose(j)
            coo = coo.next()

    def envoi_mot(self) :
        "Envoie le mot courant au serveur"
        debut, mot = self.get_mot_temp()
        if mot is not None :
            m = msg.msg("propo", (debut,mot,0))
            self.app.envoi(m)
        self.reinit_saisie()

## Gestion des évenements clavier
    def OnKey(self, e) :
        # en provenance de la case
        l = e.GetKeyCode()
        if l is None or self.saisie_ok == False :
            return
        if l == wx.WXK_RETURN or l == wx.WXK_NUMPAD_ENTER :
            self.envoi_mot()
        elif l == wx.WXK_BACK :
            self.recule_case()
        elif l == wx.WXK_ESCAPE :
            self.reinit_saisie()
        elif l == wx.WXK_DELETE :
            self.app.frame.button_pose_last(e)
        # control
        elif e.ControlDown() :
            if l == 88 : # ctrl-x
                self.app.frame.button_pose_last(e)
            elif l == 78 : #ctrl-n
                self.app.frame.button_next(e)
            elif l == 65 : #crtl-a
                self.app.frame.button_alpha(e)
            elif l == 82 : #crtl-r
                self.app.frame.button_random(e)
            elif l == 83 : #crtl-s
                self.app.frame.show_score(e)
        elif (ord('A') <= l <= ord('Z') or ord('a') <= l <= ord('z')):
            if e.ShiftDown() :
                l += 32
            self.traite_keycode(chr(l))
        
    def traite_keycode(self, l) :
        if not self.coord_ini.isOK() :  #pas de fleche en cours (ex : apres envoi d'un mot)
            return
        if (self.entry == False) :          # si pas de saisie en cours
            self.coord_cur = self.coord_ini # coord_cur=coord_ini=coord de la case cliquée 
        if not self.coord_cur.isOK() :  # si coord incorrecte, on sort
            return
        if self.case_coord_occ(self.coord_cur) : # si case occupée, on sort
            return
        j = self.app.frame.tirage.retire_jeton(l)   # prend le jeton dans le tirage
        if j is not None :                          # si c'est possible
            j.set_status(jeton.TEMP)
            ca = self.case_coord(self.coord_cur)
            ca.efface_fleche()   # efface la fleche
            ca.pose(j)  # pose le jeton en temp
            self.entry = True                      # passe le flag saisie en cours à 1

            if self.coord_cur.next().isOK() :   # avance coord_cur en sautant les lettres
                self.coord_cur = self.coord_cur.next()
                while self.case_coord_occ(self.coord_cur) :
                    self.coord_cur = self.coord_cur.next()
                if self.coord_cur.isOK() :      # remet la fleche
                    ca = self.case_coord(self.coord_cur)
                    ca.set_fleche(self.coord_ini.dir())

    def recule_case(self) :
        "Gestion de la touche Backspace (depuis OnKey)"
        if self.entry == False : #Pas de saisie en cours
            return

        if not self.coord_cur.isOK() : # Coord incorrecte, on sort
            return

        # si on est revenu au départ, on reinit et on sort
        if self.coord_cur == self.coord_ini :
            self.reinit_saisie()
            return

        # efface la fleche case en cours
        if  self.case_coord_vide(self.coord_cur) : 
            self.case_coord(self.coord_cur).efface_fleche()
            self.coord_cur = self.coord_cur.prev()

        # on recule en sautant les jetons posées
        while self.case_coord_occ(self.coord_cur) and self.case_coord(self.coord_cur).get_status() == jeton.POSE :
            self.coord_cur = self.coord_cur.prev()

        # on retire le jeton temp et on remet la fleche (cas standard)
        c = self.case_coord(self.coord_cur)
        if not c.is_vide() :
            self.app.frame.tirage.remet(c.jeton)
        c.set_fleche(self.coord_ini.dir())
        c.vide()

## Fonctions globales pour la grille

    def vide(self) :
        "Vide complétement la grille"
        self.reinit_saisie()
        for case in self.cases.itervalues() :
            case.vide()

    def read_grille(self, txt_grille) :
        """
        Initialise la grille à partir du texte renvoyé par le serveur
        """
        self.vide()
        for y, ligne in enumerate(txt_grille.split("\n")) :
            for x, char in enumerate(ligne) :
                if char != "." :
                    case = self.case_coord(coord.coord(x,y))
                    j = self.app.reliquat.retire(char, jeton.POSE)
                    case.pose(j)

if __name__ == '__main__' :
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1)
    panel = wx.Panel(frame)
    g = grille(panel, app)
    frame.Show()
    app.MainLoop()
