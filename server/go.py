#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import optparse
import sys
reload(sys)
sys.setdefaultencoding("utf8")

if sys.platform[:5] == 'linux' :
    from twisted.internet import epollreactor
    epollreactor.install()

from twisted.internet import reactor

import pyscrabse
import net

usage = "usage: %prog [options]"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-g", "--game", dest="game", default=None,
        help="indique le fichier partie (défaut partie générée)")
parser.add_option("-d", "--dico", dest="dico", default="../dic/ods5.dawg",
        help="indique le fichier dictionnaire (defaut ../dic/ods5.dawg)")
parser.add_option("-c", "--chrono", dest="chrono",type="int",default=120,
        help="indique le temps par tour en secondes (defaut 120, soit 2mn)")
parser.add_option("-i", "--inter", dest="inter", type="int", default=15,
        help="indique le temps entre chaque tour en secondes (defaut 15s)")
parser.add_option("-p", "--port", dest="port", type="int", default=1989,
        help="indique le port du serveur (defaut 1989)")
parser.add_option("-a", "--attente", dest="attente", type="int", default=30,
        help="temps attente pour debut de partie (defaut 30s)")
parser.add_option("-o", "--topping", dest="topping", action="store_true",
        help="indique le score du top au debut du tour")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", 
        help="sortie des echanges reseau")
parser.add_option("-l", "--log", dest="log", action="store_true", help="crée un ficher log")
(options, args) = parser.parse_args()

g = pyscrabse.main(options)
factory = net.ScrabbleFactory(g)
factory.protocol = net.ScrabbleProtocol
reactor.callWhenRunning(g.debut_game, options.attente)
reactor.listenTCP(options.port, factory)
print "Lancement reactor"
reactor.run()
