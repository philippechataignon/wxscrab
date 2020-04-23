#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import time
import os
import random
import urllib.request

import coord
import tirage

class partie:
    def __init__(self, options) :
        r = random.SystemRandom()
        num = r.randrange(0,2**32)
        seed = r.randrange(0,2**16)
        contents = urllib.request.urlopen(f"http://localhost:1964/gen_part/{options.dico}/{options.minpoint}/{options.mintour}/{options.maxtour}").read()
        tree = ET.fromstring(contents)
        self.liste = []
        tour = 0
        for e in tree.findall("tour"):
            n = e.find("tirage")
            ttt = tirage.tirage(n.text)
            n = e.find("coord")
            ccc = coord.coord(coo_str=n.text)
            n = e.find("mot")
            mmm = str(n.text)
            n = e.find("points")
            pts = int(n.text)
            tour += 1
            self.liste.append((ttt, ccc, mmm, pts, tour))

if __name__ == '__main__' :
    import dico
    import grille
    class options :
        def __init__(self) :
            self.dico = "../dic/ods7.dico"
            self.gen = "/home/philippe/wxscrab_gen/gen/gen_part"
            self.game = "partie/p_20101231164246.partie"
            self.minpoint = 18
            self.maxtour = 24
            self.mintour = 18
            self.game = None

    d = dico.Dico("../dic/ods7.dico")
    g = grille.grille()
    c = coord.coord()
    o = options()
    pa = partie(o)
    for t, c, m, pts, tour in pa.liste :
        controle = g.controle(c, m, t)
        print(tour, c,m,t, controle)
        if controle <= 0 :
            print(pts, g.point(c, m, controle == -1, d))
        else:
            print(">>> Controle non NUL")
        g.pose(c, m)
        print(g)
