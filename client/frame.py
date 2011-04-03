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

ST_COORD = 0
ST_RELIQ = 1
ST_RESTART = 2
ST_NEXT = 3

class frame(wx.Frame):
    def __init__(self, parent, app) :
        wx.Frame.__init__(self, parent, title = "wxScrab")
        self.app = app
        s = self.app.settings
        self.SetIcon(wx.Icon(app.settings["files_icone"], wx.BITMAP_TYPE_ICO))
        self.panel = wx.Panel(self)
        self.max_props = app.settings["max_props"]
        self.tour = 0
        fill = s["size_fill"]

        #Creation et dessin du timer
        timer_sizer  = self.cree_box_sizer("Temps")
        self.timer = wx.StaticText(self.panel, -1, str(utils.convert_time(0)))
        font = wx.Font(s["size_font_chrono"], wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.timer.SetFont(font)
        timer_sizer.Add(self.timer, 0, wx.ALL|wx.EXPAND, fill)

        #Creation et dessin du tirage
        self.tirage = tirage.tirage(self.panel, self.app)
        tirage_sizer = self.cree_box_sizer("Tirage")
        tirage_sizer.Add((fill,0),0)
        tirage_sizer.Add(self.tirage, 1, wx.ALL|wx.EXPAND, fill)
        tirage_sizer.Add((fill,0),0)

        #Creation et dessin de la grille
        self.grille = grille.grille(self.panel, self.app)
        grille_sizer = self.cree_box_sizer("Grille")
        grille_sizer.Add(self.grille, 0, wx.ALL|wx.EXPAND, 0)

        #Creation des items dans la box messages
        msgs_sizer = self.cree_box_sizer("Messages")
        self.msgs = wx.TextCtrl(self.panel, -1, "", size=(app.settings["size_chat_size"], -1), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
        self.set_police_msgs(s["size_font_msgs"])
        msgs_sizer.Add(self.msgs, 1, wx.ALL|wx.EXPAND, fill)

        #Creation box proposition
        props_sizer = self.cree_box_sizer("Propositions", flag = wx.HORIZONTAL)
        self.props = wx.ComboBox(self.panel, -1, style=wx.CB_READONLY) 
        props_sizer.Add(self.props, 1, wx.ALL, fill) 
        self.buttonpose = wx.Button(self.panel, -1, "Poser", size=app.settings["size_button"])
        self.buttonpose.Enable(False)
        self.buttonpose.SetDefault() # important pour Windows pour capter la touche Entrée
        props_sizer.Add(self.buttonpose, 0, wx.ALL|wx.ALIGN_RIGHT, fill) 
        self.Bind(wx.EVT_COMBOBOX, self.props_click, self.props)
        self.Bind(wx.EVT_BUTTON, self.pose, self.buttonpose)

        #Creation box score
        score_sizer = self.cree_box_sizer("Score", flag = wx.HORIZONTAL)
        self.score = wx.StaticText(self.panel, -1, "")
        font = wx.Font(s["size_font_score"], wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.score.SetFont(font)
        score_sizer.Add(self.score, 1, wx.ALL, fill) 
        buttscore = wx.Button(self.panel, -1, "Scores", size=app.settings["size_button"])
        score_sizer.Add(buttscore, 0, wx.ALL|wx.ALIGN_RIGHT, fill) 
        self.Bind(wx.EVT_BUTTON, self.show_score, buttscore)

        #Creation du chat
        chat_sizer = self.cree_box_sizer("Chat", flag = wx.HORIZONTAL)
        self.txtchatin = wx.TextCtrl(self.panel, -1, "", style=wx.TE_PROCESS_ENTER)
        chat_sizer.Add(self.txtchatin,1, wx.ALL, fill)
        self.Bind(wx.EVT_TEXT_ENTER, self.chat_enter, self.txtchatin)

        # cadres boutons 
        bouton_sizer = self.cree_box_sizer("Commandes", flag = wx.HORIZONTAL)
        #box = wx.StaticBox(self.panel, label = "Commandes")
        boutons = [ ("Alpha", self.button_alpha),
                    ("Random", self.button_random),
                    ("Restart", self.button_restart),
                    ("Next", self.button_next),
                    ("Précédent", self.button_pose_last),
                ]
        if s["user_admin"] :
            boutons.insert(2, ("Chrono", self.button_chrono))
        bouton_in_sizer = wx.GridSizer(rows=1, cols=len(boutons), hgap=fill, vgap=fill)
        for label, handler in boutons :
            bouton = wx.Button(self.panel, label=label, size=app.settings["size_button"])
            bouton_in_sizer.Add(bouton, flag = wx.ALIGN_CENTER)
            self.Bind(wx.EVT_BUTTON, handler, bouton)
        bouton_sizer.Add(bouton_in_sizer, proportion=1, flag = wx.EXPAND)

        #Barre de menu
        if  s["view_menu"] :
            menubar = wx.MenuBar()

            menu1 = wx.Menu()
            menu1.Append(101,"Quitter\tCtrl-Q")
            self.Bind(wx.EVT_MENU, self.quit, id=101)

            menubar.Append(menu1,"Fichier")
            menupol = wx.Menu()
            for i in range(8,14) :
                menupol.Append(200+i,str(i),"Changer la police des messages serveur", wx.ITEM_RADIO)
                self.Bind(wx.EVT_MENU, self.menu_police, id=200+i)
            pset = s["size_font_msgs"]
            menupol.Check(200+pset, True)
            self.set_police_msgs(pset)

            menu2 = wx.Menu()
            menu2.AppendMenu(299,"Taille police", menupol)
            menubar.Append(menu2,"Options")

            menu3 = wx.Menu()
            menu3.Append(301,"A propos")
            menubar.Append(menu3,"Aide")
            self.Bind(wx.EVT_MENU, self.about, id=301)

            self.SetMenuBar(menubar)

        #Barre de status
        if  s["view_status"] :
            self.st = self.CreateStatusBar()
            self.st.SetFieldsCount(4)
            self.st.SetStatusWidths(s['size_status'])
            self.set_status_next(0)
            self.set_status_restart(0)

        #Sizers
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(msgs_sizer,   1, wx.EXPAND)
        sizer2.Add(props_sizer,  0, wx.EXPAND)
        sizer2.Add(score_sizer,  0, wx.EXPAND)
        sizer2.Add(bouton_sizer, 0, wx.EXPAND)
        sizer2.Add(chat_sizer,   0, wx.EXPAND)
        sizer2.Add( (fill,fill), 0)

        sizer = wx.GridBagSizer(hgap=fill, vgap=fill) 

        if  s["view_layout"] == "alt" :
            sizer1.Add(tirage_sizer, 1, flag = wx.EXPAND)
            sizer1.Add( (fill,fill))
            sizer1.Add(timer_sizer, flag = wx.EXPAND)
            sizer.Add(grille_sizer, pos=(0,0))
            sizer2.Add(sizer1, flag = wx.EXPAND)
            sizer.Add(sizer2, pos=(0,1),  flag = wx.EXPAND)
            sizer.AddGrowableCol(1) 
        else :
            sizer1.Add(timer_sizer, flag = wx.EXPAND)
            sizer1.Add((fill,fill))
            sizer1.Add(tirage_sizer, 1, flag = wx.EXPAND)
            sizer.Add(sizer1, pos=(0,0), flag = wx.EXPAND)
            sizer.Add(grille_sizer, pos=(1,0))
            sizer.Add(sizer2, pos=(0,1), span=(2,1), flag = wx.EXPAND)
            sizer.AddGrowableCol(1)

        self.panel.SetSizer(sizer) 
        sizer.Fit(self)

# Utilitaires
    def cree_box_sizer(self, titre, flag = wx.VERTICAL) :
        box = wx.StaticBox(self.panel, label = titre)
        sizer = wx.StaticBoxSizer(box, flag)
        return sizer

# Gestionnaires evenement
    def button_restart(self, e) :
        m = msg.msg("restart")
        self.app.envoi(m)

    def button_next(self, e) :
        m = msg.msg("next")
        self.app.envoi(m)

    def button_chrono(self, e) :
        m = msg.msg("stopchrono")
        self.app.envoi(m)

    def button_alpha(self, e) :
        self.tirage.alpha()

    def button_random(self, e) :
        self.tirage.shuffle()

    def chat_enter(self, e) :
        if self.txtchatin.GetValue() != "" :
            m = msg.msg("chat", self.txtchatin.GetValue())
            self.app.envoi(m)
            self.txtchatin.SetValue("")

    def props_click(self, e) :
        if self.app.tour_on :
            self.grille.reinit_saisie()
            p = self.props.GetSelection()
            if p == -1 :
                return
            self.buttonpose.SetFocus()
            coo, mot = self.props.GetClientData(p)
            self.grille.pose_mot(coo, mot, jeton.TEMP)
        else :
            self.home_props()

    def button_pose_last(self, e) :
        if self.props.Count >= 2 and self.app.tour_on :
            self.grille.reinit_saisie()
            coo, mot = self.props.GetClientData(1)
            m = msg.msg("propo",(coo, mot, 0))
            self.app.envoi(m)

    def pose(self, e) :
        p = self.props.GetSelection()
        if p < 0 : 
            self.app.envoi_mot()
        else :
            coo, mot = self.props.GetClientData(p)
            m = msg.msg("propo",(coo, mot, 0))
            self.app.envoi(m)
            self.grille.reinit_saisie()
            self.home_props()

    def show_score(self, e) :
        self.app.score.Show(not self.app.score.IsShown())

## Evts Menu

    def menu_police(self, e) :
        i = e.GetId()-200
        self.app.settings["size_font_msgs"] = i
        self.app.settings.write()
        self.set_police_msgs(i)

    def about(self, e):
        info = wx.AboutDialogInfo()
        with open("tag.file") as f :
            ll = f.readline()
            l = ll[:-1].split("\t")
        info.Name = "wxScrab"
        info.Copyright = l[2]
        info.Description = "Client Scrabble(r) Duplicate\nRevision: %s\nTag: %s" % (l[0], l[1])
        info.WebSite = ("http://wxscrab.ath.cx", "Site wxScrab")
        info.Developers = [l[3], 'xouillet']
        with open('GPL.txt') as f :
            license = f.read()
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

    def set_status_text(self, text, num) :
        if self.app.settings["view_status"] :
            self.SetStatusText(text, num)

    def set_status_coo(self, text) :
        self.set_status_text(text, ST_COORD)

    def set_status_next(self, num) :
        self.set_status_text("Next : %d" % num, ST_NEXT)

    def set_status_restart(self, num) :
        self.set_status_text("Restart : %d" % num, ST_RESTART)

    def set_status_reliq(self) :
        self.set_status_text(str(self.app.reliquat), ST_RELIQ)

    def home_props(self) :
        self.props.SetValue('')
        self.props.SetSelection(-1)
        
    def insert_props(self, label, data) :
        pos = self.props.FindString(label)
        if ( pos != wx.NOT_FOUND ) :
            self.props.Delete(pos)
        self.props.Insert(label, 0, data)
        # Si plus de x props, on vire
        if self.props.GetCount() > self.max_props :
            self.props.Delete(self.max_props)
        self.home_props()
