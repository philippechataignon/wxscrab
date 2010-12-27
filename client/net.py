﻿#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import utils
import asyncore, asynchat
import socket
import msg
import cPickle as pickle

class net(asynchat.async_chat) :
    term = "\r\n\r\n"
    def __init__(self, app, host, port) :
        asynchat.async_chat.__init__(self)
        self.app = app
        self.buffer = []
        self.set_terminator(net.term)
        self.debug = False
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def handle_connect(self):
        m = msg.msg("joueur", (1, self.app.email), self.app.nick)
        self.envoi_net(m)

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self) :
        txt = "".join(self.buffer)
        self.buffer = []
        m = pickle.loads(txt)
        if self.debug == True :
            print m.cmd, m.param, m.id
        self.app.traite(m)

    def handle_error(self) :
        pass

    def handle_close(self) :
        self.close()
        self.app.frame.grille.saisie_ok = False
        utils.errordlg("Serveur déconnecté","Erreur Socket")

    def handle_expt(self) :
        self.close()
        self.app.frame.grille.saisie_ok = False
        utils.errordlg("Exception socket","Erreur Socket")

    def envoi_net(self, m):
        if self.debug == True :
            print m.cmd, m.param, m.id
        self.push(pickle.dumps(m, 2)+net.term)
