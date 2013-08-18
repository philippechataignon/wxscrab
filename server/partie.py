#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import xml.etree.cElementTree as ET
import time
import os
import subprocess
import random

import coord
import tirage

class partie:
    def __init__(self, options) :
        self.options = options
        while True :
            tree = self.gen_part()
            tot = int(tree.find("resume/total").text)
            nbtour = int(tree.find("resume/nbtour").text)
            if tot >= 900 and 16 <= nbtour <= 24 :
                break
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
            self.liste.append( (ttt, ccc, mmm, pts, tour) )

    def get_nom_partie(self) :
        return  os.path.basename(self.file_partie)

    def gen_part(self):
        r = random.SystemRandom()
        pgm = '../gen/gen_part'
        rep = "partie"
        num = r.randrange(0,2**32)
        seed = r.randrange(0,2**16)
        nom_partie = "p_%d_%d.partie" % (num, seed)
        self.file_partie = os.path.join(rep, nom_partie)
        f = open(self.file_partie, "w")
        subprocess.call([pgm, '-d', self.options.dico, '-n', str(num), '-s', str(seed)], stdout = f)
        f.close()
        tree = ET.parse(self.file_partie)
        return tree

if __name__ == '__main__' :
    import dico
    import grille
    class options :
        def __init__(self) :
            self.dico = "../dic/ods5.dawg"
            self.game = "partie/p_20101231164246.partie"
            self.game = None

    d = dico.dico("../dic/ods5.dawg")
    g = grille.grille()
    c = coord.coord()
    o = options()
    pa = partie(o)
    for t, c, m, pts, tour in pa.liste :
        controle = g.controle(c, m, t)
        print tour, c,m,t, controle
        if controle <= 0 :
            print pts, g.point(c, m, controle == -1, d)
        else:
            print ">>> Controle non NUL"
        g.pose(c, m)
        print g
