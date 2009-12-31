#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import utils

TIRAGE = -1
NUL    = 0
TEMP   = 1
PREPOSE = 2
POSE   = 3

#Fichier définition class
class jeton :
    pts={'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,      \
         'J':8,'K':10,'L':1,'M':2,'N':1,'O':1,'P':3,'Q':8,'R':1,     \
         'S':1,'T':1,'U':1,'V':4,'W':10,'X':10,'Y':10,'Z':10,'?':0}

    def __init__(self, lettre, skin, status) :
        self.skin = skin
        self.lettre = lettre
        self.status = status

    def __str__(self) :
        return self.lettre

    def is_joker(self) :
        return 'a' <= self.lettre <='z' or self.lettre == '?'

    def get_bmp(self) :
        memory = wx.MemoryDC()
        memory.SetFont(self.skin.get_font())
        l,h = memory.GetTextExtent(self.lettre.upper())
        if self.status in (TEMP, PREPOSE) :
            #Sur la grille en temporaire
            bmp =  self.skin.get_img_copy("temp")
            memory.SelectObject(bmp)
            if self.is_joker() :
                memory.SetTextForeground(self.skin.get_fontcol("tempjoker"))
            elif 'A' <= self.lettre <='Z' :
                memory.SetTextForeground(self.skin.get_fontcol("tempnorm"))
        elif self.lettre in ('+','-') :
            #Dans le tirage pour +,-
            bmp =  self.skin.get_img_copy("temp")
            memory.SelectObject(bmp)
            memory.SetTextForeground(self.skin.get_fontcol("signes"))
        else :
            #Sur le tirage ou sur la grille en fixe
            bmp =  self.skin.get_img_copy("norm")
            memory.SelectObject(bmp)
            if self.is_joker() :
                memory.SetTextForeground(self.skin.get_fontcol("fixejoker"))
            else :
                memory.SetTextForeground(self.skin.get_fontcol("fixenorm"))
        size = self.skin.get("size")
        memory.DrawText(self.lettre.upper(),(size-l)/2,(size-h)/2)
        le = utils.lettre_joker(self.lettre)
        if le == "" :
            p = ""
        else :
            p = str(self.pts[le])
            # p = str(self.status)
        memory.SetFont(self.skin.get_pointfont())
        memory.SetTextForeground(self.skin.get_fontcol("points"))
        l,h = memory.GetTextExtent(p)
        memory.DrawText(p, size-1-l, size- 1-h)
        memory.SelectObject(wx.NullBitmap)
        return bmp
