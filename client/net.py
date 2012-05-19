# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols import basic
import msg
import utils

PROTOCOL = 3

class ScrabbleProtocol(basic.NetstringReceiver):
    def __init__(self, app) :
        self.app = app

    def connectionMade(self):
        m = msg.msg("joueur", (PROTOCOL, self.app.email), self.app.nick)
        self.envoi(m)

    def stringReceived(self, mm):
        if self.app.settings['debug_net'] :
            print "<- %s" % mm
        m = msg.msg(dump=mm)
        d = self.app.traite(m.cmd)
        reactor.callLater(0, d.callback, m)

    def envoi(self, mm):
        if self.app.settings['debug_net'] :
            print "-> %s" % mm
        self.sendString(mm.dump())

class ScrabbleFactory(ClientFactory) :
    def __init__(self, app):
        self.app = app

    def buildProtocol(self, addr):
        self.proto = ScrabbleProtocol(self.app)
        return self.proto

    def clientConnectionFailed(self, connector, reason):
        utils.errordlg("Le serveur ne répond pas", "Connexion impossible")
        self.app.exit()

    def clientConnectionLost(self, connector, reason):
        if not self.app.onExit :
            utils.errordlg("La connexion avec le serveur s'est interrompue", "Connexion perdue")
            self.app.exit()

    def envoi(self, mm) :
        if self.proto is not None :
            self.proto.envoi(mm)
        elif self.app.settings['debug_net'] :
            print "X Non ENVOI X : %s" % mm
