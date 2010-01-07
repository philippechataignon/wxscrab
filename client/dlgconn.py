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

class dlgconnframe(wx.Frame):
    def __init__(self, parent, app) :
        wx.Frame.__init__(self, parent, -1, "wxScrab Connexion", pos=(350,250))
        self.app = app
        self.liste_skin = ("default", "tiny", "big", "mega")
        panel = wx.Panel(self, -1)
        self.settings = app.settings
        icon = wx.Icon('images/wxscrab.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        conn = wx.FlexGridSizer(rows=3, cols=3, hgap=15, vgap=15)
        space = (10,10)

        conn.Add(space)
        conn.Add(space)
        conn.Add(space)

        b = wx.ALIGN_CENTER
        conn.Add(wx.StaticText(panel, -1, "Serveur : "),-1, b)
        self.txtaddr = wx.ComboBox(panel, -1, self.settings.get("servers")[0], size=(200, -1), choices=self.settings.get("servers"))
        self.txtaddr.SetFocus()
        conn.Add(self.txtaddr)

        saddrport = wx.BoxSizer(wx.HORIZONTAL)
        saddrport.Add(wx.StaticText(panel, -1, "Port : "), -1, b)
        self.txtport = wx.TextCtrl(panel, -1, self.settings.get("port"), size=(50,-1))
        saddrport.Add(self.txtport)
        conn.Add(saddrport)

        conn.Add(wx.StaticText(panel, -1, "Pseudo  : "), -1, b)
        self.txtnom  = wx.TextCtrl(panel, -1, self.settings.get("pseudo"), size=(200,-1))
        conn.Add(self.txtnom)
        conn.Add(space)

        conn.Add(wx.StaticText(panel, -1, "Email  : "), -1, b)
        self.txtemail  = wx.TextCtrl(panel, -1, self.settings.get("email"), size=(200,-1))
        conn.Add(self.txtemail)
        conn.Add(space)

        conn.Add(wx.StaticText(panel, -1, "Skin  : "), -1, b)
        self.box_skin = wx.ComboBox(panel, -1, style=wx.CB_READONLY, choices=self.liste_skin)
        self.box_skin.SetStringSelection(self.settings.get("skin"))
        self.Bind(wx.EVT_COMBOBOX, self.skin_click, self.box_skin)
        conn.Add(self.box_skin)
        conn.Add(space)

        conn.Add(space)
        conn.Add(space)
        bok = wx.Button(panel,-1, "OK")
        bok.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.conn, bok)
        conn.Add(bok,0,b|wx.ALIGN_RIGHT)

        border = wx.BoxSizer()
        border.Add(conn,0,wx.ALL,10)
        panel.SetSizerAndFit(border)
        self.SetSize(self.GetBestSize())

        self.Show()

    def conn(self, evt) :
        nick = str(self.txtnom.GetValue()).strip()
        host = str(self.txtaddr.GetValue()).strip()
        email = str(self.txtemail.GetValue()).strip()
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
            self.settings.set("port",str(port))
            self.settings.set("pseudo",nick)
            self.settings.set("email",email)
            self.settings.insert_list("servers", host)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try :
                sock.connect((host,port))
                # numéro de protocole = 1
                m = msg.msg("joueur", (1, email), nick)
                sock.send(pickle.dumps(m) + net.net.term)
                recv  = sock.recv(1024)
                ret = pickle.loads(recv)
                # print "Ret %s %s %s" % (ret.cmd, ret.param, ret.id)
                if ret.cmd == "connect" :
                    if ret.param[0] == 0 :
                        sock.close()
                        utils.errordlg(ret.param[1],"Erreur")
                    else :
                        self.settings.write()
                        sock.setblocking(0)
                        self.Close()
                        self.app.cree_all(nick, sock, ret.param[0])
                else :
                    sock.close()
                    utils.errordlg("Erreur retour connexion","Pickle error")
            except socket.error, (errno, errmsg) :
                sock.close()
                utils.errordlg(errmsg, "Erreur de connexion")
 
    def skin_click(self, e) :
        p = self.box_skin.GetSelection()
        skin = self.liste_skin[p]
        self.app.settings.set("skin", skin)

    def quit(self,evt) :
        self.Close()

if __name__ == '__main__' :
    class App(wx.App):
        def OnInit(self) :
            wx.InitAllImageHandlers()
            self.dlgconn = dlgconnframe(None)
            self.dlgconn.Show()
            return True
    app = App()
    app.MainLoop()
