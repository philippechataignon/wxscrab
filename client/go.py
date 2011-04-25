#!/usr/bin/env python2
# -*- coding: UTF8 -*-
#Reglage encoding
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import wx
wx.SetDefaultPyEncoding("utf8")
from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor
import wxscrab
app = wxscrab.App()
reactor.registerWxApp(app)
#app.MainLoop()
reactor.run()
