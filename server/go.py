#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import pyscrabse
import optparse
import asyncore
import time

usage = "usage: %prog [options] [fichier_partie]"
parser = optparse.OptionParser(usage=usage)
parser.add_option("-g", "--game", dest="game", default=None,
                    help="indique le fichier partie (defaut partie generee)")
parser.add_option("-t", "--tour", dest="tour", type="int", default=None,
                    help="indique tour de debut si -g actif")
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
parser.add_option("-v", "--verbose", dest="verbose",  \
        action="store_true", help="sortie des echanges reseau")
(options, args) = parser.parse_args()
print options
g = pyscrabse.main(options)
g.start()
delai = 0.02
while not g.stop :
    try :
        g.net.lock.acquire()
        asyncore.poll()
        g.net.lock.release()
        time.sleep(delai)
    except KeyboardInterrupt:
        g.stop = True
        print "KeyboardInterrupt"
