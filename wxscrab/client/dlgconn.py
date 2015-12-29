# -*- coding: utf-8 -*-
import wx
import utils

class TooMuchTry(Exception) :
    pass

class dlgconnframe(wx.Frame):
    def __init__(self, parent, app, complet=False) :
        wx.Frame.__init__(self, parent, title="wxScrab Connexion")
        panel = wx.Panel(self)
        icon = wx.Icon('images/wxscrab.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.app = app
        self.settings = app.settings
        fill = self.settings["size_fill"]

        conn = wx.FlexGridSizer(rows=2, cols=4, hgap=fill, vgap=fill)
        # conn = wx.GridBagSizer(hgap=fill, vgap=fill)
        space = (fill,fill)
        # conn.Add(space)
        # conn.Add(space)
        # conn.Add(space)
        # conn.Add(space)

        b = wx.ALIGN_RIGHT | wx.ALIGN_CENTER
        conn.Add(wx.StaticText(panel, label="Serveur : "), flag=b, border = fill)
        self.txtaddr = wx.ComboBox(panel, value=self.settings["server_servers"][0], size=(200, -1), choices=self.settings["server_servers"])
        self.txtaddr.SetFocus()
        conn.Add(self.txtaddr, flag=wx.EXPAND)

        conn.Add(wx.StaticText(panel, label="Port : "), flag=b)
        self.txtport = wx.TextCtrl(panel, value=str(self.settings["server_port"]))
        conn.Add(self.txtport, flag=wx.EXPAND)

        conn.Add(wx.StaticText(panel, label="Pseudo  : "), flag=b)
        self.txtnom  = wx.TextCtrl(panel, size=(150,-1), value=self.settings["user_pseudo"])
        conn.Add(self.txtnom, flag=wx.EXPAND)
        conn.Add(space)
        bok = wx.Button(panel, size=(100, 28), label="OK")
        bok.SetDefault()
        conn.Add(bok, flag=wx.ALIGN_RIGHT)
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(conn,0,wx.ALL,10)
        panel.SetSizerAndFit(border)
        # self.SetSize(self.GetBestSize())
        self.Bind(wx.EVT_BUTTON, self.click_button_ok, bok)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.Show()

    def click_button_ok(self, evt) :
        nick = self.txtnom.GetValue().strip()
        host = self.txtaddr.GetValue().strip()
        email = ""
        porterror = False
        try:
            port = int (self.txtport.GetValue())
        except ValueError:
            porterror = True
            utils.errordlg("Port invalide", "Erreur")

        if porterror :
            pass
        elif len(nick) == 0 :
            utils.errordlg("Vous n'avez pas reglé de pseudo", "Erreur")
        elif len(nick) > 20 :
            utils.errordlg("Pas plus de 20 caractères pour le pseudo", "Erreur")
        else :
            self.Unbind(wx.EVT_CLOSE)
            self.settings["server_port"] = port
            self.settings["user_pseudo"] = nick
            self.settings["user_email"]  = email
            self.settings.insert_list("server_servers", host)
            self.app.nick = nick
            self.app.host = host
            self.app.port = port
            self.app.email = email
            self.MakeModal(False)
            self.app.lance_net()
            self.Destroy()

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