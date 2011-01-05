#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import coord
import dnd
import jeton
import grille

class case(wx.Window) :
    def __init__(self, parent) :
        self.app = parent.app
        size = self.app.settings.get("size_jeton")
        wx.Window.__init__(self, parent, size=(size,size))
        self.jeton = None
        self.tirage = False
        self.SetDropTarget(dnd.casedroptarget(self))
        # self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)

    def OnKey(self, e) :
        self.app.frame.grille.OnKey(e)

    def OnSize(self, evt):
        pass

    def OnPaint(self, evt):
        self.redraw()

    def redraw(self) :
        if self.jeton is not None :
            self.buffer=self.jeton.get_bmp()
        elif self.tirage :
            self.buffer=self.app.settings.get_img("vide")
        elif self.fleche == coord.HOR :
            self.buffer=self.app.settings.get_img('fl_r')
        elif self.fleche == coord.VER :
            self.buffer=self.app.settings.get_img('fl_b')
        elif self.mult == grille.OO :
            self.buffer=self.app.settings.get_img('base')
        elif self.mult == grille.LD :
            self.buffer=self.app.settings.get_img('ld')
        elif self.mult == grille.LT :
            self.buffer=self.app.settings.get_img('lt')
        elif self.mult == grille.MD :
            self.buffer=self.app.settings.get_img('md')
        elif self.mult == grille.MT : 
            self.buffer=self.app.settings.get_img('mt')
        dc = wx.BufferedPaintDC(self, self.buffer)

    def is_vide(self) :
        return self.jeton is None

    def get_status(self) :
        if self.is_vide() :
            return jeton.NUL
        else :
            return self.jeton.status

    def pose(self, j) :
        if not self.is_vide() :
            self.app.frame.tirage.remet(self.jeton)
        self.jeton = j
        self.redraw()

    def vide(self) :
        """Appelé quand on enlève un jeton d'une case"""
        self.jeton = None
        self.redraw()
