#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import utils
import jeton

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
                j = dep.jeton
                tirage = True
                try :
                    self.case.pos
                except AttributeError :
                    tirage = False
                if tirage :
                    "Départ et arrivée dans tirage : on swap"
                    t.swap_cases(dep, self.case)
                elif self.case.is_vide() and not j.is_joker():
                    j.set_status(jeton.TEMP)
                    self.case.pose(j)
                    dep.vide()
