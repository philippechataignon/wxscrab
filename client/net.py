#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import basic
import msg
import utils

class ScrabbleProtocol(basic.NetstringReceiver):
    def connectionMade(self):
        self.factory.channel = self
        protocol = 3
        m = msg.msg("joueur", (protocol, self.factory.app.email), self.factory.app.nick)
        self.envoi(m)

    def stringReceived(self, mm):
        if self.factory.app.settings['debug_net'] :
            print "<- %s" % mm
        self.factory.app.traite(mm)

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
        utils.errordlg(reason.getErrorMessage(), "Connexion impossible")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        if not self.app.onExit :
            utils.errordlg(reason.getErrorMessage(), "Connexion perdue")

    def envoi_net(self, mm) :
        if self.channel is not None :
            self.channel.envoi(mm)
