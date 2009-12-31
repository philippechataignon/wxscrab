#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import coord
import dnd
import jeton
import grille

class case(wx.StaticBitmap) :
    def __init__(self, x, y, mult, app, *bitarg) :
        wx.StaticBitmap.__init__(self, *bitarg)
        self.coord = coord.coord(x,y)
        self.mult = mult
        self.app = app
        self.fleche = coord.NUL
        self.jeton = None
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickCase)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnClickCase)
        self.SetDropTarget(dnd.casedroptarget(self, self.app))
        self.redraw()
     
    def redraw(self) :
        if self.jeton is not None :
            self.SetBitmap(self.jeton.get_bmp())
        elif self.fleche == coord.HOR :
            self.SetBitmap(self.app.skin.get_img('fl_r'))
        elif self.fleche == coord.VER :
            self.SetBitmap(self.app.skin.get_img('fl_b'))
        elif self.mult == grille.OO :
            self.SetBitmap(self.app.skin.get_img('null'))
        elif self.mult == grille.LD :
            self.SetBitmap(self.app.skin.get_img('ld'))
        elif self.mult == grille.LT :
            self.SetBitmap(self.app.skin.get_img('lt'))
        elif self.mult == grille.MD :
            self.SetBitmap(self.app.skin.get_img('md'))
        elif self.mult == grille.MT : 
            self.SetBitmap(self.app.skin.get_img('mt'))

    def is_vide(self) :
        return self.jeton is None

    def get_status(self) :
        if self.jeton is None :
            return jeton.NUL
        else :
            return self.jeton.status

    def pose(self, j) :
        """Appelé par pose_jeton dans grille"""
        self.jeton = j
        self.Unbind(wx.EVT_LEFT_DOWN)
        self.Unbind(wx.EVT_LEFT_DCLICK)
        self.redraw()

    def vide(self) :
        """Appelé quand on enlève un jeton d'une case"""
        self.jeton = None
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickCase)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnClickCase)
        self.redraw()

    def OnClickCase(self, evt) :
        self.app.OnClickCase(self)
