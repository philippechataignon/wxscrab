#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import coord
import jeton

class case(wx.Window) :
    """ Cette classe représente une case qui peut être sur la grille
        ou dans le tirage
    """
    def __init__(self, parent) :
        self.app = parent.app
        self.settings = self.app.settings
        self.size = self.settings["size_case"]
        wx.Window.__init__(self, parent, size=(self.size, self.size))
        self._jeton = None
        self._fleche = None
        self._buffer = wx.EmptyBitmap(self.size, self.size)
        self.font_jeton = wx.Font(self.settings['size_font_jeton'],
                wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_point = wx.Font(self.settings['size_font_point'],
                wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.SetDropTarget(casedroptarget(self))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.app.OnKey)

    def OnPaint(self, evt):
        """ Fonction gérant le dessin de la case : fond de cases, jeton ou flèche éventuel
        """
        s = self.settings
        dc = wx.BufferedPaintDC(self, self._buffer)
        dc.SetBrush(wx.Brush(self.col_fond))
        # trace le carré de fond
        dc.SetPen(wx.Pen(s['col_neutre'], 1, wx.SOLID))
        dc.DrawRectangle(0, 0, self.size, self.size) 
        # puis le jeton éventuel
        if not self.is_vide() :
            dc = wx.PaintDC(self)
            if self.get_jeton_status() in (jeton.TEMP, jeton.PREPOSE) :
                col = s['col_temp']
                font = "fontcol_tempjoker" if self._jeton.is_joker() else "fontcol_tempnorm"
            else :
                col = s['col_pose']
                font = "fontcol_fixejoker" if self._jeton.is_joker() else "fontcol_fixenorm"
            dc.SetBrush(wx.Brush(col))
            dc.SetTextForeground(s[font])
            dc.SetPen(wx.Pen(s['col_neutre'], 1, wx.TRANSPARENT))
            size_jeton = self.size - 2
            if s['jeton_carre'] :
                dc.DrawRectangle(1, 1, size_jeton, size_jeton)
            else :
                dc.DrawRoundedRectangle(1, 1, size_jeton , size_jeton, s['size_arrondi'])
            dc.SetFont(self.font_jeton)
            text = self._jeton.get_lettre().upper()
            l,h = dc.GetTextExtent(text)
            dc.DrawText(text, (size_jeton - l)/2 + 1 , (size_jeton - h)/2 + 1)
            dc.SetFont(self.font_point)
            dc.SetTextForeground(s["fontcol_points"])
            text = self._jeton.get_point()
            l,h = dc.GetTextExtent(text)
            dc.DrawText(text, size_jeton-l, size_jeton-h)
        # ou la flèche
        elif self._fleche in (coord.HOR, coord.VER) :
            dc.SetBrush(wx.Brush(s['col_cercle']))
            dc.SetPen(wx.Pen(s['col_cercle'], 1, wx.TRANSPARENT))
            dc.DrawCircle(self.size/2, self.size/2, self.size/2-2)
            dc.SetBrush(wx.Brush(s['col_fleche']))
            dc.SetPen(wx.Pen(s['col_fleche'], 1, wx.TRANSPARENT))
            pts = [(2.0,6.5), (5,6.5), (5,8), (8.5,5), (5,2), (5,3.5), (2.0,3.5)]
            if self._fleche == coord.HOR :
                pts_reel = [(x*self.size/10, y*self.size/10) for (x,y) in pts]
            elif self._fleche == coord.VER :
                pts_reel = [(y*self.size/10, x*self.size/10) for (x,y) in pts]
            dc.DrawPolygon(pts_reel) 

    def is_vide(self) :
        """ Renvoit True si la case est vide (pas de jeton)
        """
        return self._jeton is None

    def get_jeton_status(self) :
        """ Renvoie le status du jeton de la case ou jeton.NUL
        """
        if self.is_vide() :
            return jeton.NUL
        else :
            return self._jeton.get_status()

    def get_jeton_lettre(self) :
        """ Renvoie la lettre du jeton de la case ou ""
        """
        if self.is_vide() :
            return ""
        else :
            return self._jeton.get_lettre()

    def pose(self, j) :
        """ Pose un jeton sur la case
        La case doit obligatoirement être vide
        """
        assert self.is_vide(), "Pose un jeton sur une case non vide"
        self._jeton = j
        self.Refresh()

    def prend(self) :
        """ Appelé quand on prend un jeton sur une case
        Renvoie le jeton éventuel, sinon None
        """
        j = self._jeton
        self._jeton = None
        self.Refresh()
        return j

class casedroptarget(wx.PyDropTarget) :
    def __init__(self, case) :
        wx.PyDropTarget.__init__(self)
        self.case = case
        self.app = case.app
        self.data = wx.TextDataObject()
        self.SetDataObject(self.data) 

    def OnData(self, x, y, d) :
        if self.GetData() :
            pos = int(self.data.GetText())
            t = self.app.frame.tirage
            dep = t.cases[pos]
            if not dep.is_vide() :
                self.case.traite_drop(dep)

