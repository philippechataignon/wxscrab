#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import coord
import dnd
import case

class case_tirage(case.case) :
    def __init__(self, parent, pos)  :
        case.case.__init__(self, parent)
        size = self.app.settings.get("size_jeton")
        self.tirage = True
        self.pos = pos
        self.allowdrag = False
        self.Bind(wx.EVT_LEFT_DOWN, self.drag)
        self.Bind(wx.EVT_RIGHT_DOWN, self.shift)
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
