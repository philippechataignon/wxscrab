# -*- coding: utf-8 -*-
#Reglage encoding
import wx
class son :
    def __init__(self) :
        self.sons = {
            'debut':wx.Sound("sound/debut.wav"),
            'fin_tour':  wx.Sound("sound/fin_tour.wav"),
            'valid':wx.Sound("sound/valid.wav")
        }

    def play(self, nom) :
        if nom in self.sons :
            self.sons[nom].Play()
