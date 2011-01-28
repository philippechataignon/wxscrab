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
    def __init__(self, parent, x, y, mult) :
        case.case.__init__(self, parent)
        self.coord = coord.coord(x,y)
        self.mult = mult
        self.fleche = None
        self.col_fond = self.app.settings['col_grille'][self.mult]
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickCase)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnClickCase)
     
    def OnClickCase(self, evt) :
        # si pas de tour en cours, on sort
        if self.app.tour_on == False :
            return
        g = self.app.frame.grille
        # si la case est vide, on met une fleche horizontale
        if self.fleche is None : 
            g.reinit_saisie()
            self.init_saisie(coord.HOR)
        elif self.fleche == coord.HOR and g.entry == False:
            self.init_saisie(coord.VER)
        else  :
            g.reinit_saisie()
        g.SetFocus()

    def init_saisie(self, dir) :
        f = self.app.frame
        self.set_fleche(dir)
        self.coord.set_dir(dir)
        f.grille.coord_ini = self.coord
        f.set_status_coo( "%s" % self.coord )

    def set_fleche(self, dir) :
        self.fleche = dir
        self.redraw()

    def efface_fleche(self) :
        self.set_fleche(None)

    def convert_prepose(self) :
        if self.get_status() == jeton.PREPOSE : #si jeton prepose
            self.jeton.set_status(jeton.POSE) #met status pose
            self.redraw()
