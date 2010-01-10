#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import wx
import utils
import grille
import tirage
import jeton
import msg
import coord

class frame(wx.Frame):
    def __init__(self, parent, app, tiny = False) :
        wx.Frame.__init__(self, parent, -1, "wxScrab - " + app.nick, size=(app.skin.get("frame_h"), app.skin.get("frame_v")))
        self.SetIcon(wx.Icon(app.skin.get("icone"), wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self, -1)
        self.app = app
        self.tiny = tiny
        self.max_props = 8
        self.tour = 0
        fill = self.app.skin.get("fill")

        #Creation et dessin du timer
        self.timer = wx.StaticText(self.panel, -1, str(utils.convert_time(0)))
        font = wx.Font(self.app.skin.get("size_chrono"), wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.timer.SetFont(font)
        timer_box  = wx.StaticBox(self.panel,-1, "Temps")
        timer_sizer = wx.StaticBoxSizer(timer_box)
        timer_sizer.Add((fill,0),0)
        timer_sizer.Add(self.timer, 0, wx.ALL|wx.EXPAND, fill) 
        timer_sizer.Add((fill,0),0)

        #Creation et dessin du tirage
        self.tirage = tirage.tirage(self.panel, self.app)
        bouton_alpha = wx.Button(self.panel, 30, "A", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.alpha_click, bouton_alpha)
        bouton_rand = wx.Button(self.panel, 31, "R", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.rand_click, bouton_rand)
        tirage_box = wx.StaticBox(self.panel,-1, "Tirage")
        tirage_sizer = wx.StaticBoxSizer(tirage_box)
        tirage_sizer.Add((2*fill,0),0)
        tirage_sizer.Add(self.tirage, 0, wx.ALL|wx.EXPAND, fill)
        boutons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        boutons_sizer.Add(bouton_alpha, 0, wx.EXPAND, 0)
        boutons_sizer.Add((fill,0),0)
        boutons_sizer.Add(bouton_rand, 0, wx.EXPAND, 0)
        tirage_sizer.Add((20,0),0)
        tirage_sizer.Add(boutons_sizer, 0, wx.ALIGN_CENTRE_VERTICAL, 0)
        tirage_sizer.Add((2*fill,0),0)

        #Creation et dessin de la grille
        self.grille = grille.grille(self.panel, self.app)
        grille_box = wx.StaticBox(self.panel,-1, "Grille")
        grille_sizer = wx.StaticBoxSizer(grille_box)
        grille_sizer.Add(self.grille, 0, wx.ALL|wx.EXPAND, 0)

        #Creation des items dans la box messages
        self.msgs = wx.TextCtrl(self.panel, -1, "", size=(-1, -1), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
        self.msgs.SetDefaultStyle(wx.TextAttr(font=wx.Font(self.app.skin.get("size_def"), wx.SWISS, wx.NORMAL, wx.NORMAL)))
        msgs_box   = wx.StaticBox(self.panel,-1, "Messages")
        msgs_sizer = wx.StaticBoxSizer(msgs_box, wx.VERTICAL)
        msgs_sizer.Add(self.msgs, 1, wx.ALL|wx.EXPAND, fill)

        #Creation box proposition
        self.props = wx.ComboBox(self.panel, -1, style=wx.CB_READONLY) 
        #self.props.Insert("", 0, "")
        self.buttonpose = wx.Button(self.panel, 11,"Poser le mot")
        self.buttonpose.Enable(False)
        self.Bind(wx.EVT_COMBOBOX, self.props_click, self.props)
        self.Bind(wx.EVT_BUTTON, self.pose, self.buttonpose)
        props_box  = wx.StaticBox(self.panel,-1, "Propositions")
        props_sizer = wx.StaticBoxSizer(props_box, wx.HORIZONTAL)
        props_sizer.Add(self.props, 1, wx.ALL, fill) 
        props_sizer.Add(self.buttonpose, 0, wx.ALL|wx.ALIGN_RIGHT, fill) 
        self.buttonpose.SetDefault()

        #Creation box score
        self.score = wx.StaticText(self.panel, -1, "")
        font = wx.Font(self.app.skin.get("size_score"), wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.score.SetFont(font)
        buttscore = wx.Button(self.panel, 12, "Scores")
        self.Bind(wx.EVT_BUTTON, self.show_score, buttscore)
        score_box  = wx.StaticBox(self.panel,-1, "Score")
        score_sizer = wx.StaticBoxSizer(score_box, wx.HORIZONTAL)
        score_sizer.Add(self.score, 1, wx.ALL, fill) 
        score_sizer.Add(buttscore, 0, wx.ALL|wx.ALIGN_RIGHT, fill) 

        #Creation du chat
        self.txtchatin = wx.TextCtrl(self.panel, -1, "")
        self.buttonchat = wx.Button(self.panel, fill, "Ok")
        self.Bind(wx.EVT_BUTTON, self.chat_click, self.buttonchat)
        self.txtchatin.Bind(wx.EVT_SET_FOCUS,self.chat_focus)
        self.txtchatin.Bind(wx.EVT_KILL_FOCUS, self.chat_nofocus)
        chat_box = wx.StaticBox(self.panel, -1, "Chat")
        chat_sizer = wx.StaticBoxSizer(chat_box, wx.HORIZONTAL)
        chat_sizer.Add(self.txtchatin,1, wx.ALL, fill)
        chat_sizer.Add(self.buttonchat,0, wx.ALL|wx.ALIGN_RIGHT, fill)

        #Barre de menu
        if not self.tiny :
            menubar = wx.MenuBar()

            menu1 = wx.Menu()
            menu1.Append(101,"Quitter\tCtrl-Q")
            self.Bind(wx.EVT_MENU, self.quit, id=101)

            menubar.Append(menu1,"Fichier")
            menupol = wx.Menu()
            for i in range(8,14) :
                menupol.Append(200+i,str(i),"Changer la police des messages serveur", wx.ITEM_RADIO)
                self.Bind(wx.EVT_MENU, self.menu_police, id=200+i)
            pset = int(self.app.settings.get("policeserv"))
            menupol.Check(200+pset, True)
            self.set_police_msgs(pset)

            menuskin = wx.Menu()
            for i, t in enumerate(self.app.settings.liste_skin):
                menuskin.Append(400+i, t, "Taille de la grille", wx.ITEM_RADIO)
                self.Bind(wx.EVT_MENU, self.menu_skin, id=400+i)
            #pset = int(self.app.settings.get("skin"))
            # menupol.Check(400+pset, True)
            #self.set_police_msgs(pset)

            menu2 = wx.Menu()
            menu2.AppendMenu(299,"Taille police", menupol)
            menu2.AppendMenu(499,"Skin", menuskin)
            menubar.Append(menu2,"Options")

            menu3 = wx.Menu()
            menu3.Append(301,"A propos\tCtrl-A")
            menubar.Append(menu3,"Aide")
            self.Bind(wx.EVT_MENU, self.about, id=301)

            self.SetMenuBar(menubar)

            #Barre de status
            self.st = self.CreateStatusBar()
            self.st.SetFieldsCount(2)
            self.st.SetStatusWidths([-1, -5])

        #Sizers
        if self.tiny :
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(tirage_sizer,1, wx.EXPAND|wx.ALIGN_RIGHT)
            sizer1.Add(timer_sizer, 0, wx.EXPAND)

            sizer3 = wx.BoxSizer(wx.VERTICAL)
            sizer3.Add(grille_sizer, 0, wx.EXPAND|wx.ALIGN_RIGHT)

            sizer2a = wx.BoxSizer(wx.VERTICAL)
            sizer2a.Add(props_sizer, 0, wx.EXPAND)
            sizer2a.Add(score_sizer, 0, wx.EXPAND)
            sizer2a.Add(chat_sizer, 0, wx.EXPAND)
            sizer2a.Add(sizer1, 0, wx.EXPAND)
        else :
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(timer_sizer, 0, wx.EXPAND)
            sizer1.Add( (fill,fill), 0)
            sizer1.Add(tirage_sizer,0, wx.EXPAND|wx.ALIGN_RIGHT)

            sizer3 = wx.BoxSizer(wx.VERTICAL)
            sizer3.Add(sizer1, 0)
            sizer3.Add(grille_sizer, 0, wx.EXPAND|wx.ALIGN_RIGHT)

            sizer2a = wx.BoxSizer(wx.VERTICAL)
            sizer2a.Add(props_sizer,0, wx.EXPAND)
            sizer2a.Add(score_sizer,0,wx.EXPAND)
            sizer2a.Add(chat_sizer,0,wx.EXPAND)

        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(msgs_sizer,1, wx.EXPAND)
        sizer2.Add(sizer2a,1, wx.EXPAND)

        border=wx.BoxSizer(wx.HORIZONTAL)
        border.Add(sizer3, 0, wx.EXPAND|wx.ALL, fill)
        border.Add(sizer2, 1, wx.EXPAND|wx.ALL, fill)
        self.panel.SetSizerAndFit(border)

# Gestionnaires evenement
    def alpha_click(self, e) :
        self.tirage.alpha()

    def rand_click(self, e) :
        self.tirage.shuffle()

    def chat_click(self, e) :
        if self.txtchatin.GetValue() != "" :
            m = msg.msg("chat", self.txtchatin.GetValue())
            self.app.envoi(m)
            self.txtchatin.SetValue("")

    def chat_focus(self, e):
        self.buttonchat.SetDefault()

    def chat_nofocus(self, e) :
        self.buttonpose.SetDefault()

    def props_click(self, e) :
        if self.grille.saisie_ok :
            self.grille.reinit_saisie()
            p = self.props.GetSelection()
            if p == -1 :
                return
            coo, mot = self.props.GetClientData(p)
            self.grille.pose_mot(coo, mot, jeton.TEMP)
        else :
            self.home_props()

    def pose(self, e) :
        p = self.props.GetSelection()
        if p < 0 : 
            self.grille.envoi_mot()
        else :
            coo, mot = self.props.GetClientData(p)
            m = msg.msg("propo",(coo, mot, 0))
            self.app.envoi(m)
            self.grille.reinit_saisie()
            self.home_props()

    def show_score(self, e) :
        self.app.bascule_score()

## Evts Menu

    def menu_police(self, e) :
        i = e.GetId()-200
        self.app.settings.set("policeserv", str(i))
        self.set_police_msgs(i)

    def menu_skin(self, e) :
        i = e.GetId()-400
        skin = self.app.settings.liste_skin[i]
        self.app.settings.set("skin", skin)
        self.app.settings.write()
        utils.errordlg("Relancer le programme pour prendre en compte le nouveau skin","Attention")

    def about(self, e):
        info = wx.AboutDialogInfo()
        info.Name = "wxScrab"
        info.Copyright = "Build : %s\nDate : %s" % (347, "4 mai 2009")
        info.Description = '   Client Scrabble(r) Duplicate   '
        info.WebSite = ("http://wxscrab.ath.cx", "Site wxScrab")
        info.Developers = [ "Xouillet",
                            "PhC"
                          ]
        f=open('GPL.txt')
        license = f.read()
        f.close()
        info.License = license
        wx.AboutBox(info)

    def quit(self,e) :
        self.Close()

# Fonctions accés

    def set_police_msgs(self, i) :
        self.msgs.SetStyle(0, self.msgs.GetLastPosition(), wx.TextAttr(font=wx.Font(i, wx.SWISS, wx.NORMAL, wx.NORMAL)))
        self.msgs.SetDefaultStyle(wx.TextAttr(font=wx.Font(i, wx.SWISS, wx.NORMAL, wx.NORMAL)))

    def info_serv(self, msg, color = wx.BLACK) :
        self.msgs.SetDefaultStyle(wx.TextAttr(color))
        self.msgs.AppendText("%s\n" % msg)
        self.msgs.ScrollLines(-1)

    def efface_msgs(self) :
        self.msgs.SetValue('')

    def set_status_text(self, text) :
        if not self.tiny :
            self.SetStatusText(text)

    def upd_status(self) :
        if not self.tiny :
            self.st.SetStatusText(str(self.app.reliquat), 1)

    def home_props(self) :
        self.props.SetValue('')
        self.props.SetSelection(-1)
        
    def insert_props(self, label, data) :
        # pos = self.props.FindString(label, casesensitive = True)
        pos = self.props.FindString(label)
        if ( pos != wx.NOT_FOUND ) :
            self.props.Delete(pos)
        self.props.Insert(label, 0, data)
        # Si plus de x props, on vire
        if self.props.GetCount() > self.max_props :
            self.props.Delete(self.max_props)
        self.home_props()
