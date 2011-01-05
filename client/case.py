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
    colors=["#ccc2b8", "#95a5dd", "#6673a1", "#dd9595", "#a16767"]
    # "#ebe5d4"
    def __init__(self, parent) :
        self.app = parent.app
        self.settings = self.app.settings
        self.size = self.settings.get("size_jeton")
        wx.Window.__init__(self, parent, size=(self.size, self.size))
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
        bmp = False
        if not self.tirage :
            if self.fleche == coord.HOR :
                self.buffer=self.app.settings.get_img('fl_r')
                bmp = True
            elif self.fleche == coord.VER :
                self.buffer=self.app.settings.get_img('fl_b')
                bmp = True

        if bmp :
            wx.BufferedPaintDC(self, self.buffer)
        else :
            dc = wx.PaintDC(self)
            if self.tirage :
                dc.SetBrush(wx.Brush("#e9e4e0"))
            else :
                dc.SetBrush(wx.Brush(self.colors[self.mult]))
            dc.SetPen(wx.Pen("#eeeeee", 1, wx.SOLID))
            dc.DrawRectangle(0, 0, self.size, self.size) 
            if self.jeton is not None :
                dc = wx.PaintDC(self)
                dc.SetPen(wx.Pen("#b2a56b", 1, wx.SOLID))
                if self.jeton.status in (jeton.TEMP, jeton.PREPOSE) :
                    dc.SetBrush(wx.Brush("#ebe5d4"))
                    if self.jeton.is_joker() :
                        dc.SetTextForeground(self.settings.get("fontcol_tempjoker"))
                    else :
                        dc.SetTextForeground(self.settings.get("fontcol_tempnorm"))
                else :
                    dc.SetBrush(wx.Brush("#f6e594"))
                    if self.jeton.is_joker() :
                        dc.SetTextForeground(self.settings.get("fontcol_fixejoker"))
                    else :
                        dc.SetTextForeground(self.settings.get("fontcol_fixenorm"))
                dc.DrawRoundedRectangle(1, 1, self.size-2, self.size-2, 4)
                dc.SetFont(self.settings.get_font())
                l,h = dc.GetTextExtent(self.jeton.lettre.upper())
                dc.DrawText(self.jeton.lettre.upper(),(self.size-l)/2,(self.size-h)/2)
                dc.SetFont(self.settings.get_pointfont())
                dc.SetTextForeground(self.settings.get("fontcol_points"))
                l,h = dc.GetTextExtent(self.jeton.point)
                dc.DrawText(self.jeton.point, self.size-2-l, self.size-2-h)

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
