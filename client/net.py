#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import basic
import cPickle as pickle
import msg
import utils

class ScrabbleProtocol(basic.LineReceiver):
    delimiter = '\r\n\r\n'
    def connectionMade(self):
        #print "Connect %s" % self.transport.getPeer()
        self.factory.channel = self
        protocol = 2
        m = msg.msg("joueur", (protocol, self.factory.app.email), self.factory.app.nick)
        self.envoi(m)

    def lineReceived(self, line):
        mm = pickle.loads(line)
        # print "Received : %s" % mm
        self.factory.app.traite(mm)

    def envoi(self, mm):
        # print "Send : %s" % mm
        msg = pickle.dumps(mm)
        self.sendLine(msg)

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
