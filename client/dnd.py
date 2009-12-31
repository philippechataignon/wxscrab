#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import utils
import jeton

class casedroptarget(wx.PyDropTarget) :
    def __init__(self, case, app) :
        wx.PyDropTarget.__init__(self)
        self.case = case
        self.app = app
        self.data = wx.TextDataObject()
        self.SetDataObject(self.data) 

    def OnData(self,x,y,d) :
        if self.GetData() :
            pos = int(self.data.GetText())
            t = self.app.frame.tirage
            g = self.app.frame.grille
            c = t.cases[pos]
            if c.is_vide() :
                return
            j = c.jeton
            if j.is_joker() :
                return
            if self.case.is_vide() :
                g.raz_fleche()
                j.status = jeton.TEMP
                g.pose_jeton(self.case, j)
                c.enleve()

class tiragedroptarget(wx.PyDropTarget) :
    def __init__(self, pos, app) :
        wx.PyDropTarget.__init__(self)
        self.pos = pos
        self.app = app
        self.data = wx.TextDataObject()
        self.SetDataObject(self.data) 

    def OnData(self,x,y,d) :
        if self.GetData() :
            old = int(self.data.GetText())
            self.app.frame.tirage.swap(old, self.pos)
