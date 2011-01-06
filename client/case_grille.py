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
        self.fleche = coord.NUL
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickCase)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnClickCase)
     
    def OnClickCase(self, evt) :
        f = self.app.frame
        g = f.grille
        if g.saisie_ok == False :
            return

        if self.fleche == coord.NUL :
            g.reinit_saisie()
            f.home_props()
            self.fleche = coord.HOR
            self.coord.set_hor()
            g.entry = 0
            g.coord_ini = self.coord
            f.set_status_coo( "%s" % self.coord )
        elif self.fleche == coord.HOR :
            self.fleche = coord.VER
            self.coord.set_ver()
            g.coord_ini = self.coord
            f.set_status_coo( "%s" % self.coord )
        else  :
            self.fleche = coord.NUL
            g.coord_ini = coord.coord()
            f.set_status_coo( "" )
        self.redraw()
        g.SetFocus()
