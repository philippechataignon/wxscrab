#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import net
import frame
import utils
import socket
import msg
import cPickle as pickle

class TooMuchTry(Exception) :
    pass

class dlgconnframe(wx.Frame):
    def __init__(self, parent, app, complet=False) :
        wx.Frame.__init__(self, parent, -1, "wxScrab Connexion", pos=(350,250))
        self.app = app
        panel = wx.Panel(self, -1)
        self.settings = app.settings
        icon = wx.Icon('images/wxscrab.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        conn = wx.FlexGridSizer(rows=3, cols=4, hgap=15, vgap=15)
        space = (10,10)
        conn.Add(space)
        conn.Add(space)
        conn.Add(space)
        conn.Add(space)

        b = wx.ALIGN_RIGHT
        conn.Add(wx.StaticText(panel, -1, "Serveur : "),-1, b)
        self.txtaddr = wx.ComboBox(panel, -1, self.settings.get("servers")[0], size=(200, -1), choices=self.settings.get("servers"))
        self.txtaddr.SetFocus()
        conn.Add(self.txtaddr)

        conn.Add(wx.StaticText(panel, -1, "Port : "), -1, b)
        self.txtport = wx.TextCtrl(panel, -1, self.settings.get("port"), size=(50,-1))
        conn.Add(self.txtport)

        conn.Add(wx.StaticText(panel, -1, "Pseudo  : "), -1, b)
        self.txtnom  = wx.TextCtrl(panel, -1, self.settings.get("pseudo"), size=(200,-1))
        conn.Add(self.txtnom)
        conn.Add(space)
        conn.Add(space)
        conn.Add(space)
        conn.Add(space)
        conn.Add(space)
        bok = wx.Button(panel,-1, "OK")
        bok.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.click_button_ok, bok)
        conn.Add(bok,0,b|wx.ALIGN_RIGHT)

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(conn,0,wx.ALL,10)
        panel.SetSizerAndFit(border)
        self.SetSize(self.GetBestSize())
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.Show()

    def click_button_ok(self, evt) :
        nick = str(self.txtnom.GetValue()).strip()
        host = str(self.txtaddr.GetValue()).strip()
        email = ""
        porterror = False
        try:
            port = int (self.txtport.GetValue())
        except ValueError:
            porterror = True
            utils.errordlg("Port invalide", "Erreur")

        if porterror :
            pass
        elif nick == "" :
            utils.errordlg("Vous n'avez pas reglé de pseudo", "Erreur")
        elif len(nick) > 20 :
            utils.errordlg("Pas plus de 20 caractères pour le pseudo", "Erreur")
        else :
            self.Unbind(wx.EVT_CLOSE)
            self.settings.set("port",str(port))
            self.settings.set("pseudo",nick)
            self.settings.set("email",email)
            self.settings.insert_list("servers", host)
            self.app.nick = nick
            self.app.host = host
            self.app.port = port
            self.app.email = email
            self.MakeModal(False)
            self.app.cree()

    def OnClose(self,evt) :
        self.app.frame.Close()

if __name__ == '__main__' :
    class App(wx.App):
        def OnInit(self) :
            wx.InitAllImageHandlers()
            self.dlgconn = dlgconnframe(None)
            self.dlgconn.Show()
            return True
    app = App()
    app.MainLoop()
