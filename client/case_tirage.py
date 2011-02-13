#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import case

class case_tirage(case.case) :
    """ Repésente une case du tirage
    """
    def __init__(self, parent, pos)  :
        case.case.__init__(self, parent)
        self.pos = pos
        self.col_fond = self.app.settings['col_tirage']
        self.Bind(wx.EVT_LEFT_DOWN, self.drag)
        self.Bind(wx.EVT_RIGHT_DOWN, self.shift)

    def shift(self, e) :
        """ Décale les jetons
        Appelée par l'évenement RIGHT_CLICK 
        """
        self.app.frame.tirage.shift(self.pos)

    def drag(self, e) :
        """ Utilisée pour le drag and drop depuis la classe dnd
        Le data stocke la position pos de la case de départ
        """
        if self.app.tour_on :
            data = wx.TextDataObject()
            data.SetText(str(self.pos))
            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            dropSource.DoDragDrop(True)
