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
        conn.Add(wx.StaticText(panel, -1, "Complet : "), -1, b, )
        self.check_complet = wx.CheckBox(panel, -1, )
        self.check_complet.SetValue(complet)
        self.Bind(wx.EVT_CHECKBOX, self.complet_click, self.check_complet)
        conn.Add(self.check_complet)

        if complet :
            conn.Add(wx.StaticText(panel, -1, "Email  : "), -1, b)
            self.txtemail  = wx.TextCtrl(panel, -1, self.settings.get("email"), size=(200,-1))
            conn.Add(self.txtemail)
            conn.Add(space)
            conn.Add(space)

            conn.Add(wx.StaticText(panel, -1, "Skin  :"), -1, b)
            self.box_skin = wx.ComboBox(panel, -1, style=wx.CB_READONLY, choices=self.settings.liste_skin, size=(200,-1))
            self.box_skin.SetStringSelection(self.settings.get("skin"))
            self.Bind(wx.EVT_COMBOBOX, self.skin_click, self.box_skin)
            conn.Add(self.box_skin)
            conn.Add(wx.StaticText(panel, -1, "Tirage  :"), -1, b)
            self.box_case = wx.ComboBox(panel, -1, style=wx.CB_READONLY, choices=self.settings.liste_case, size=(50,-1))
            self.box_case.SetStringSelection(self.settings.get("tirage_nbpos"))
            self.Bind(wx.EVT_COMBOBOX, self.case_click, self.box_case)
            conn.Add(self.box_case)

        conn.Add(space)
        conn.Add(space)
        bok = wx.Button(panel,-1, "OK")
        bok.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.conn, bok)
        conn.Add(bok,0,b|wx.ALIGN_RIGHT)

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(conn,0,wx.ALL,10)
        panel.SetSizerAndFit(border)
        self.SetSize(self.GetBestSize())

        self.Show()

    def conn(self, evt) :
        nick = str(self.txtnom.GetValue()).strip()
        host = str(self.txtaddr.GetValue()).strip()
        if self.check_complet.GetValue() :
            email = str(self.txtemail.GetValue()).strip()
        else :
            email = self.settings.get("email")
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
                proto = 1
                m = msg.msg("joueur", (proto, email), nick)
                sock.send(pickle.dumps(m) + net.net.term)
                ok = False
                essai = 0
                while not ok  :
                    recv  = sock.recv(4096)
                    ret = pickle.loads(recv)
                    # print "Ret %s %s %s" % (ret.cmd, ret.param, ret.id)
                    if ret.cmd == "connect" :
                        if ret.param[0] == 0 :
                            ok = True
                            sock.close()
                            utils.errordlg(ret.param[1],"Erreur : nom existant")
                        else :
                            self.settings.write()
                            sock.setblocking(0)
                            self.Close()
                            self.app.cree_all(nick, sock, ret.param[0])
                            ok = True
                    else :
                        essai += 1
                        if essai > 10 :
                            raise TooMuchTry
            except socket.error, (errno, errmsg) :
                sock.close()
                utils.errordlg(errmsg, "Erreur de connexion")
            except TooMuchTry :
                sock.close()
                utils.errordlg("Limite essais atteinte", "Erreur : connect non reçu")
 
    def skin_click(self, e) :
        p = self.box_skin.GetSelection()
        skin = self.settings.liste_skin[p]
        self.app.settings.set("skin", skin)

    def case_click(self, e) :
        p = self.box_case.GetSelection()
        case = self.settings.liste_case[p]
        self.app.settings.set("tirage_nbpos", case)

    def complet_click(self, e) :
        self.Close()
        dlgconnframe(None, self.app, complet=self.check_complet.GetValue())

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
