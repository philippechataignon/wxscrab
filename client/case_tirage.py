#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import coord
import dnd

class case_tirage(wx.StaticBitmap) :
    def __init__(self, pos, app, *bitarg) :
        wx.StaticBitmap.__init__(self, *bitarg)
        self.pos = pos
        self.app = app
        self.jeton = None
        self.allowdrag = False
        self.SetDropTarget(dnd.tiragedroptarget(self.pos, self.app))
        self.Bind(wx.EVT_LEFT_DOWN, self.drag)
        self.Bind(wx.EVT_RIGHT_DOWN, self.shift)
        self.redraw()

    def redraw(self) :
        """Redessine une case"""
        j = self.jeton
        if j is None :
            self.SetBitmap(self.app.skin.get_img("vide"))
        else:
            self.SetBitmap(j.get_bmp())

    def is_vide(self) :
        return self.jeton is None

    def get_status(self) :
        if self.jeton is None :
            return jeton.NUL
        else :
            return self.jeton.status

    def met(self, j) :
        """Appelé par pose_jeton dans grille"""
        self.jeton = j
        self.redraw()

    def enleve(self) :
        """Appelé quand on enlève un jeton d'une case"""
        self.jeton = None
        self.redraw()

    def shift(self, e) :
        """ Appelée par l'évenement RIGHT_CLICK """
        self.app.frame.tirage.shift(self.pos)

    def drag(self, evt) :
        """ Utilisée pour le drag and drop depuis la classe dnd
        Le data stocke la position pos de la case de départ
        """
        if self.allowdrag:
            data = wx.TextDataObject()
            data.SetText(str(self.pos))
            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            dropSource.DoDragDrop(True)
