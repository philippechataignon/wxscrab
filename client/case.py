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
        self.settings = self.app.settings
        self.size = self.settings["size_jeton"]
        wx.Window.__init__(self, parent, size=(self.size, self.size))
        self.jeton = None
        self.tirage = False
        self.SetDropTarget(dnd.casedroptarget(self))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        self.fleche = None

    def OnKey(self, e) :
        self.app.frame.grille.OnKey(e)

    def OnSize(self, evt):
        pass

    def OnPaint(self, evt):
        self.redraw()

    def redraw(self) :
        s = self.settings
        dc = wx.PaintDC(self)
        if self.tirage :
            dc.SetBrush(wx.Brush(s['col_tirage']))
        else :
            dc.SetBrush(wx.Brush(s['col_grille'][self.mult]))
        # trace le carré de fond
        dc.SetPen(wx.Pen(s['col_neutre'], 1, wx.SOLID))
        dc.DrawRectangle(0, 0, self.size, self.size) 
        # puis le jeton éventuel
        if self.jeton is not None :
            dc = wx.PaintDC(self)
            dc.SetPen(wx.Pen(s['col_tour_jeton'], 1, wx.SOLID))
            if self.jeton.status in (jeton.TEMP, jeton.PREPOSE) :
                col = s['col_temp']
                font = "fontcol_tempjoker" if self.jeton.is_joker() else "fontcol_tempnorm"
            else :
                col = s['col_pose']
                font = "fontcol_fixejoker" if self.jeton.is_joker() else "fontcol_fixenorm"
            dc.SetBrush(wx.Brush(col))
            dc.SetTextForeground(s[font])
            dc.DrawRoundedRectangle(1, 1, self.size-2, self.size-2, 5)
            font = wx.Font(s['size_font_jeton'], wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            dc.SetFont(font)
            l,h = dc.GetTextExtent(self.jeton.lettre.upper())
            dc.DrawText(self.jeton.lettre.upper(),(self.size-l)/2,(self.size-h)/2)
            font = wx.Font(s['size_font_point'], wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            dc.SetFont(font)
            dc.SetTextForeground(s["fontcol_points"])
            l,h = dc.GetTextExtent(self.jeton.point)
            dc.DrawText(self.jeton.point, self.size-2-l, self.size-2-h)
        # ou la flèche
        elif self.fleche in (coord.HOR, coord.VER) :
            dc.SetBrush(wx.Brush(s['col_neutre']))
            dc.SetPen(wx.Pen("black", 1, wx.SOLID))
            dc.DrawCircle(self.size/2, self.size/2, self.size/2-2)
            dc.SetBrush(wx.Brush("blue"))
            dc.SetPen(wx.Pen("black", 1, wx.SOLID))
            pts = [(2.0,6.5), (5,6.5), (5,8), (8.5,5), (5,2), (5,3.5), (2.0,3.5)]
            if self.fleche == coord.HOR :
                pts_reel = [(x*self.size/10, y*self.size/10) for (x,y) in pts]
            elif self.fleche == coord.VER :
                pts_reel = [(y*self.size/10, x*self.size/10) for (x,y) in pts]
            dc.DrawPolygon(pts_reel) 


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
