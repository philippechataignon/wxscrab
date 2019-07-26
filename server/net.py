#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import basic
import msg

PROTOCOL = 3

class ScrabbleProtocol(basic.NetstringReceiver):
    def connectionMade(self):
        print("Connect %s" % self.transport.getPeer())
        m = msg.msg("serverok", (PROTOCOL,))
        self.envoi(m)
        app = self.factory.parent
        if not app.partie_on :
            reactor.callLater(0, app.debut_game, app.options.inter)

    def connectionLost(self, reason):
        self.factory.parent.deconnect(self)
        print("Deconnect %s" % self.transport.getPeer())

    def stringReceived(self, dump):
        mm = msg.msg.load(dump)
        if self.factory.parent.options.verbose :
            print("<- %s" % mm)
        self.factory.parent.traite(self, mm)

    def envoi(self, mm):
        if self.factory.parent.options.verbose :
            print("-> %s" % mm)
        self.sendString(mm.dump())
        return mm

class ScrabbleFactory(Factory):
    protocol = ScrabbleProtocol
    def __init__(self, parent):
        self.parent = parent
