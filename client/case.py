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
    def __init__(self, parent) :
        wx.StaticBitmap.__init__(self, parent)
        self.app = parent.app
        self.jeton = None
        self.tirage = False
        self.SetDropTarget(dnd.casedroptarget(self))

    def redraw(self) :
        if self.jeton is not None :
            self.SetBitmap(self.jeton.get_bmp())
        elif self.tirage :
            self.SetBitmap(self.app.settings.get_img("vide"))
        elif self.fleche == coord.HOR :
            self.SetBitmap(self.app.settings.get_img('fl_r'))
        elif self.fleche == coord.VER :
            self.SetBitmap(self.app.settings.get_img('fl_b'))
        elif self.mult == grille.OO :
            self.SetBitmap(self.app.settings.get_img('base'))
        elif self.mult == grille.LD :
            self.SetBitmap(self.app.settings.get_img('ld'))
        elif self.mult == grille.LT :
            self.SetBitmap(self.app.settings.get_img('lt'))
        elif self.mult == grille.MD :
            self.SetBitmap(self.app.settings.get_img('md'))
        elif self.mult == grille.MT : 
            self.SetBitmap(self.app.settings.get_img('mt'))

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
