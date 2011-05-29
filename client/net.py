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
        #try :
        self.connect((host, port))
        #except socket.error, (errno, errmsg) :
        #    utils.errordlg(errmsg, "Erreur de connexion")

    def handle_connect(self):
        if self.app.settings['debug_net'] :
            print "connect"
        protocol = 4
        m = msg.msg("joueur", (protocol, self.app.email), self.app.nick)
        self.envoi(m)

    def handle_read(self):
        data = self.recv(4096)
        if data :
            for packet in self.decoder.feed(data):
                if self.app.settings['debug_net'] :
                    print "<- %s" % packet
                self.app.traite(packet)

    def writable(self):
        print len(self.send_list) > 0
        return len(self.send_list) > 0

    def handle_write(self):
        out = self.send_list.popleft()
        if self.app.settings['debug_net'] :
            print "-> %s" % out
        self.sendall(out)

    #def handle_expt(self):
    #    self.close()

    #def handle_close(self):
    #    self.close()

    def handle_error(self):
        self.close()
        utils.errordlg("handle_error", "Erreur socket")

    def envoi(self, m):
        txt = netstring.encode(m.dump())
        self.send_list.append(netstring.encode(m.dump()))

    def watchnet(self, e) :
        asyncore.poll()
