#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import coord
import dnd
import jeton
import grille
import case

class case_grille(case.case) :
    """ Représente une case de la grille
    """
    def __init__(self, parent, x, y, mult) :
        case.case.__init__(self, parent)
        self.coord = coord.coord(x,y)
        self.mult = mult
        self.fleche = None
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
        # si la case est vide, on met une fleche horizontale
        if self.fleche is None : 
            g.reinit_saisie()
            self.init_saisie(coord.HOR)
        # la flèche passe verticale que s'il n'y a pas de saisie en cours (g.entry)
        elif self.fleche == coord.HOR and g.entry == False:
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
        self.fleche = dir
        self.Refresh()

    def efface_fleche(self) :
        """ Efface la flèche
        """
        self.set_fleche(None)

    def convert_prepose(self) :
        """ Convertit le status du jeton de PREPOSE à POSE
        Appelé depuis la fonction convert_prepose de la grille
        """
        if self.get_jeton_status() == jeton.PREPOSE : #si jeton prepose
            self.jeton.set_status(jeton.POSE) #met status pose
            self.Refresh()
