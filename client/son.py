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

    def play_debut(self, m) :
        self.sons['debut'].Play()
        return m

    def play_valid(self, m) :
        self.sons['valid'].Play()
        return m

    def play_fin_tour(self, m) :
        self.sons['fin_tour'].Play()
        return m
