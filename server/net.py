#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import basic
import cPickle as pickle

class ScrabbleProtocol(basic.NetstringReceiver):
    def connectionMade(self):
        print "Connect %s" % self.transport.getPeer()

    def connectionLost(self, reason):
        self.factory.parent.deconnect(self)
        print "Deconnect %s" % self.transport.getPeer()

    def stringReceived(self, line):
        print "<- : %s" % line
        mm = pickle.loads(line)
        self.factory.parent.traite(self, mm)

    def envoi(self, mm):
        print "-> : %s" % mm
        msg = pickle.dumps(mm)
        self.sendString(msg)

class ScrabbleFactory(Factory):
    protocol = ScrabbleProtocol
    def __init__(self, parent):
        self.parent = parent
