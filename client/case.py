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
        self.size = self.settings["size_case"]
        wx.Window.__init__(self, parent, size=(self.size, self.size))
        self.jeton = None
        self.fleche = None
        self.font_jeton = wx.Font(self.settings['size_font_jeton'],
                wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_point = wx.Font(self.settings['size_font_point'],
                wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.SetDropTarget(dnd.casedroptarget(self))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)

    def OnKey(self, e) :
        self.app.frame.grille.OnKey(e)

    def OnPaint(self, evt):
        s = self.settings
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.col_fond))
        # trace le carré de fond
        dc.SetPen(wx.Pen(s['col_neutre'], 1, wx.SOLID))
        dc.DrawRectangle(0, 0, self.size, self.size) 
        # puis le jeton éventuel
        if self.jeton is not None :
            #size_jeton = self.settings["size_jeton"]
            dc = wx.PaintDC(self)
            if self.jeton.get_status() in (jeton.TEMP, jeton.PREPOSE) :
                col = s['col_temp']
                font = "fontcol_tempjoker" if self.jeton.is_joker() else "fontcol_tempnorm"
            else :
                col = s['col_pose']
                font = "fontcol_fixejoker" if self.jeton.is_joker() else "fontcol_fixenorm"
            dc.SetBrush(wx.Brush(col))
            dc.SetTextForeground(s[font])
            dc.SetPen(wx.Pen(s['col_neutre'], 1, wx.TRANSPARENT))
            size_jeton = self.size - 2
            if s['jeton_carre'] :
                dc.DrawRectangle(1, 1, size_jeton, size_jeton)
            else :
                dc.DrawRoundedRectangle(1, 1, size_jeton , size_jeton, s['size_arrondi'])
            dc.SetFont(self.font_jeton)
            text = self.jeton.get_lettre().upper()
            l,h = dc.GetTextExtent(text)
            dc.DrawText(text, (size_jeton - l)/2 + 1 , (size_jeton - h)/2 + 1)
            dc.SetFont(self.font_point)
            dc.SetTextForeground(s["fontcol_points"])
            text = self.jeton.get_point()
            l,h = dc.GetTextExtent(text)
            dc.DrawText(text, size_jeton-l, size_jeton-h)
        # ou la flèche
        elif self.fleche in (coord.HOR, coord.VER) :
            dc.SetBrush(wx.Brush(s['col_cercle']))
            dc.SetPen(wx.Pen(s['col_cercle'], 1, wx.TRANSPARENT))
            dc.DrawCircle(self.size/2, self.size/2, self.size/2-2)
            dc.SetBrush(wx.Brush(s['col_fleche']))
            dc.SetPen(wx.Pen(s['col_fleche'], 1, wx.TRANSPARENT))
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
            return self.jeton.get_status()

    def pose(self, j) :
        assert self.is_vide(), "Pose un jeton sur une case non vide"
        self.jeton = j
        self.Refresh()

    def vide(self) :
        """Appelé quand on enlève un jeton d'une case"""
        j = self.jeton
        self.jeton = None
        self.Refresh()
        return j

    def swap(self, other) :
        self.jeton, other.jeton  = other.jeton, self.jeton
        self.Refresh()
        other.Refresh()
