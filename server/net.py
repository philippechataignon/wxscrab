#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols import basic
import cPickle as pickle

class ScrabbleProtocol(basic.LineReceiver):
    delimiter = '\r\n\r\n'
    def connectionMade(self):
        print "Connect %s" % self.transport.getPeer()

    def connectionLost(self, reason):
        self.factory.parent.deconnect(self)
        print "Deconnect %s" % self.transport.getPeer()

    def lineReceived(self, line):
        #print "Received : %s" % line
        mm = pickle.loads(line)
        self.factory.parent.traite(self, mm)

    def envoi(self, mm):
        #print "Send : %s" % mm
        msg = pickle.dumps(mm)
        reactor.callFromThread(self.sendLine, msg)

class ScrabbleFactory(Factory):
    protocol = ScrabbleProtocol
    def __init__(self, parent):
        self.parent = parent
