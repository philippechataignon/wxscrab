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

    def pose(self, j) :
        """ Pose un jeton
        La case doit obligatoirement être vide
        Gère le drag dans le tirage
        """
        case.case.pose(self, j)
        # s'il y a un jeton, autorise le drag
        if not self.is_vide() :
            self.Bind(wx.EVT_LEFT_DOWN, self.drag)

    def prend(self) :
        """ Appelé quand on prend un jeton sur une case
        Renvoie le jeton éventuel, sinon None
        """
        j = case.case.prend(self)
        self.Unbind(wx.EVT_LEFT_DOWN)
        return j

    def traite_drop(self, other) :
        """ Appelé quand on drop sur la case
        """
        if self is not other :
            mon_j = self.prend()
            son_j = other.prend()
            other.pose(mon_j)
            self.pose(son_j)
