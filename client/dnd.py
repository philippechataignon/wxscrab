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
                try :
                    tirage = True
                    self.case.pos
                except AttributeError :
                    tirage = False
                if tirage :
                    # départ et arrivée dans tirage : on swap"
                    self.case.swap(dep)
                elif self.case.is_vide() :
                    j = dep.prend()
                    if j.is_joker() :
                        dep.pose(j)
                    else :
                        j.set_status(jeton.TEMP)
                        self.case.pose(j)
