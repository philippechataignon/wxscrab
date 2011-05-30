#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import asyncore
import socket
import json
from collections import deque

import msg
import netstring
import utils

class net(asyncore.dispatcher):
    def __init__(self, app, host, port):
        asyncore.dispatcher.__init__(self)
        self.app = app
        self.decoder = netstring.Decoder()
        self.send_list = deque()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            self.connect((host, port))
        except socket.error, (errno, errmsg) :
            utils.errordlg(errmsg, "Erreur de connexion")
            self.app.exit(None)

    def handle_connect(self):
        self.connected = True
        if self.app.settings['debug_net'] :
            print "Connect"
        protocol = 3
        m = msg.msg("joueur", (protocol, self.app.email), self.app.nick)
        self.envoi(m)

    def handle_read(self):
        data = self.recv(4096)
        if data :
            for packet in self.decoder.feed(data):
                if self.app.settings['debug_net'] :
                    print "<- %s" % packet
                m = msg.msg(dump=packet)
                self.app.traite(m)

    def writable(self):
        return len(self.send_list) > 0

    def handle_write(self):
        out = self.send_list.popleft()
        if self.app.settings['debug_net'] :
            print "-> %s" % out
        self.sendall(out)

    #def handle_expt(self):
    #    self.close()

    def handle_close(self):
        utils.errordlg("Connexion perdue", "Erreur réseau")
        self.close()

    #def handle_error(self):
    #    utils.errordlg("Erreur socket", "Erreur réseau")
    #    self.close()

    def envoi(self, m):
        txt = netstring.encode(m.dump())
        self.send_list.append(txt)

    def watchnet(self, e) :
        asyncore.poll()
