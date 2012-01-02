#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol, Factory
from twisted.protocols import basic
import msg
import utils

PROTOCOL = 3

class ScrabbleProtocol(basic.NetstringReceiver):
    def connectionMade(self):
        self.factory.channel = self
        m = msg.msg("joueur", (PROTOCOL, self.factory.app.email), self.factory.app.nick)
        self.envoi(m)

    def stringReceived(self, mm):
        if self.factory.app.settings['debug_net'] :
            print "<- %s" % mm
        m = msg.msg(dump=mm)
        self.factory.app.traite(m)

    def envoi(self, mm):
        if self.factory.app.settings['debug_net'] :
            print "-> %s" % mm
        self.sendString(mm.dump())

class ScrabbleFactory(ClientFactory):
    protocol = ScrabbleProtocol
    def __init__(self, app, nick):
        self.nick = nick
        self.app = app
        self.channel = None

    def clientConnectionFailed(self, connector, reason):
        utils.errordlg("Le serveur ne répond pas", "Connexion impossible")
        reactor.stop()

    #def clientConnectionLost(self, connector, reason):
    #    if not self.app.onExit :
    #        utils.errordlg("La connexion avec le serveur s'est interrompue", "Connexion perdue")

    def envoi(self, mm) :
        if self.channel is not None :
            self.channel.envoi(mm)
