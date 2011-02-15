#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import case
import coord
import jeton

class case_grille(case.case) :
    """ Représente une case de la grille
    """
    def __init__(self, parent, x, y, mult) :
        case.case.__init__(self, parent)
        self.coord = coord.coord(x,y)
        self.mult = mult
        self.col_fond = self.app.settings['col_grille'][self.mult]
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickCase)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnClickCase)
     
    def OnClickCase(self, evt) :
        """ Si on clique sur une case, on amorce une saisie
        ou on passe d'horizontal à vertical si on reclique
        """
        # si pas de tour en cours, on sort
        if self.app.tour_on == False :
            return
        g = self.app.frame.grille
        # si la case est vide , on met une fleche horizontale
        if not self.is_fleche() : 
            g.reinit_saisie()
            self.init_saisie(coord.HOR)
        # la flèche passe verticale que s'il n'y a pas de saisie en cours (g.entry)
        elif self._fleche == coord.HOR and g.entry == False:
            self.init_saisie(coord.VER)
        else  :
            g.reinit_saisie()
        g.SetFocus()

    def init_saisie(self, dir) :
        """ Initialise la saisie d'un mot
        dans la direction donnée
        """
        f = self.app.frame
        self.set_fleche(dir)
        self.coord.set_dir(dir)
        f.grille.coord_ini = self.coord
        f.set_status_coo( "%s" % self.coord )

    def set_fleche(self, dir) :
        """ Définit la flèche
        """
        self._fleche = dir
        self.Refresh()

    def efface_fleche(self) :
        """ Efface la flèche
        """
        self.set_fleche(None)

    def is_fleche(self) :
        return self._fleche is not None

    def convert_prepose(self) :
        """ Convertit le status du jeton de PREPOSE à POSE
        Appelé depuis la fonction convert_prepose de la grille
        """
        if self.get_jeton_status() == jeton.PREPOSE : #si jeton prepose
            self._jeton.set_status(jeton.POSE) #met status pose
            self.Unbind(wx.EVT_LEFT_DOWN)
            self.Unbind(wx.EVT_LEFT_DCLICK)
            self.Refresh()

    def pose(self, j) :
        """ Pose un jeton
        Gère le Bind de la souris
        """
        case.case.pose(self, j)
        # si le jeton a le statut POSE, on enlève le Bind
        if self.get_jeton_status() == jeton.POSE :
            self.Unbind(wx.EVT_LEFT_DOWN)
            self.Unbind(wx.EVT_LEFT_DCLICK)

    def prend(self) :
        """ Prend un jeton
        Gère le Bind de la souris
        """
        j = case.case.prend(self)
        # on remet le Bind
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickCase)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnClickCase)
        return j

    def traite_drop(self, dep) :
        """ Appelé quand on drop sur la case
        """
        if self.is_vide() :
            j = dep.prend()
            if j.is_joker() :
                dep.pose(j)
            else :
                j.set_status(jeton.TEMP)
                self.pose(j)
