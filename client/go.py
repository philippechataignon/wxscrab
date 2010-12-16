#!/usr/bin/env python2
# -*- coding: UTF8 -*-
#Reglage encoding
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import wx
wx.SetDefaultPyEncoding("utf8")
import wxscrab
app = wxscrab.App()
app.MainLoop()
