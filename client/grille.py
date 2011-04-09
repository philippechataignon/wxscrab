#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import case_grille
import coord
import jeton

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
    """ Représente la grille de jeu

    Une grille est composée, pour l'essentiel, d'une matrice 15x15 de case_grille
    """
    def __init__(self, parent, app) :
        wx.Panel.__init__(self, parent, -1)
        self.app = app
        self.coord_ini = coord.coord()   # coord_ini est récupéré depuis case (OnClickCase)
        self.coord_cur = coord.coord()   # coordonnée courante 
        self.entry = False          # flag saisie en cours
        fill = self.app.settings["size_fill"]
        sizer = wx.GridBagSizer(hgap=0, vgap=0)
        sizer.Add( (2*fill,2*fill), pos=(0,0))
        sizer.Add( (fill,fill), pos=(16,16))
        for i in xrange(15) :
            t = str(i+1)
            sizer.Add(wx.StaticText(self, -1, t), pos=(0,i+1), flag=wx.ALIGN_CENTER)
            t = chr(65+i)
            sizer.Add(wx.StaticText(self, -1, t), pos=(i+1,0), flag=wx.ALIGN_CENTER)
        self.cases = {}
        for y in range(15) :
            for x in range(15) :
                self.cases[(x,y)] = case_grille.case_grille(self, x, y, mult[x][y])
                sizer.Add(self.cases[(x,y)], pos=(y+1, x+1))
        self.SetSizer(sizer)
        self.Fit()

    def __iter__(self) :
        """ L'itérateur de la grille parcourt l'ensemble des cases
        """
        return self.cases.itervalues()

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
        for c in self :
            if c.get_jeton_status() == jeton.PREPOSE : #si jeton prepose
                j = c.prend()
                j.set_status(jeton.POSE) #met status pose
                c.pose(j)

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
                mot.append(self.case_coord(cur).get_jeton_lettre())
                cur = cur.next()
            if mot == [] :
                return (None, None)
            else :
                return (debut, "".join(mot))

## Principales fonctions publiques

    def reinit_saisie(self) :
        "Enleve la fleche et les jetons temporaires de la grille (remis dans le tirage)"
        for c in self :
            if c.is_fleche() :
                c.efface_fleche()
            if c.get_jeton_status() == jeton.TEMP :
                self.app.frame.tirage.move_to(c)
        self.entry = False
        self.app.frame.set_status_coo("")
        self.coord_ini = coord.coord()

    def pose_mot(self, coo, mot, status) :
        """ Pose un mot sur la grille 
        Appelé pour le mot du Top pour permettre de le repérer (status = PREPOSE)
        Appelé depuis la box des propositions (status = TEMP)
        """
        t = self.app.frame.tirage
        for l in mot :
            t.move_from(self.case_coord(coo), status, l)
            coo = coo.next()
        
# Traitement evt clavier, appelé depuis app.OnKey
    def traite_keycode(self, l) :
        """ Traite le cas où une lettre est demandée dans le cas
        d'une saisie en cours

        Prend le jeton dans le tirage, le pose et fait avancer la flèche
        """
        if not self.entry :          # si pas de saisie en cours
            self.coord_cur = self.coord_ini # coord_cur=coord_ini=coord de la case cliquée 
                                            # sinon, la coord courante existe
        if not self.coord_cur.isOK() :      # si coord incorrecte, on sort
            return
        c = self.case_coord(self.coord_cur)
        if not c.is_vide() : # si case occupée, on sort
            return
        # prend le jeton dans le tirage
        ok = self.app.frame.tirage.move_from(c, jeton.TEMP, l)
        if ok :                 # si c'est possible
            c.efface_fleche()   # efface la fleche
            self.entry = True   # passe le flag saisie en cours à True
            # avance coord_cur en sautant les cases occupées
            while self.case_coord_occ(self.coord_cur) : 
                self.coord_cur = self.coord_cur.next()
            # met la fleche si possible
            if self.coord_cur.isOK() :      
                c = self.case_coord(self.coord_cur)
                c.set_fleche(self.coord_ini.dir())

    def recule_case(self) :
        """ Gestion de la touche Backspace (depuis OnKey)
        """
        if not self.entry : #Pas de saisie en cours
            return

        if not self.coord_cur.isOK() : # Coord incorrecte, on sort
            return

        # si on est revenu au départ, on reinit et on sort
        if self.coord_cur == self.coord_ini :
            self.reinit_saisie()
            return

        # efface la fleche case en cours
        c = self.case_coord(self.coord_cur)
        if  c.is_vide() :
            c.efface_fleche()

        # on recule en sautant les jetons posés
        while True :
            self.coord_cur = self.coord_cur.prev()
            c = self.case_coord(self.coord_cur)
            if c.get_jeton_status() != jeton.POSE :
                break

        # on remet le jeton temp dans le tirage
        # et on remet la fleche (cas standard)
        if not c.is_vide() :
            self.app.frame.tirage.move_to(c)
        c.set_fleche(self.coord_ini.dir())

## Initialisation de la grille
    def read_grille(self, txt_grille) :
        """ Initialise la grille à partir du texte renvoyé par le serveur
        """
        self.reinit_saisie()
        r = self.app.reliquat
        # remet les jetons dans le reliquat
        for case in self :
            r.move_to(case)
        # prend les jetons dans le reliquat
        # et les pose sur la grille
        for y, ligne in enumerate(txt_grille.split("\n")) :
            for x, lettre in enumerate(ligne) :
                if lettre != "." :
                    c = coord.coord(x, y)
                    r.move_from(self.case_coord(c), jeton.POSE, lettre)
