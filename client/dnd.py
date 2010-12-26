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
            dep = self.app.frame.tirage.cases[pos]
            j = dep.jeton
            if j is not None : 
                j.deplace(dep, self.case)
