#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import xml.etree.cElementTree as ET
import time
import os
import subprocess

import coord
import tirage

class partie:
    def __init__(self, options) :
        self.options = options
        if self.options.game is None :
            pgm = '../gen/gen_part'
            rep = "partie"
            nom_partie = "p_%s.partie" % time.strftime("%Y%m%d%H%M%S")
            self.file_partie = os.path.join(rep, nom_partie)
            f = open(self.file_partie, "w")
            subprocess.call([pgm, '-d', self.options.dico], stdout = f)
            f.close()
        else :
            self.file_partie = self.options.game
        tree = ET.parse(self.file_partie)
        self.liste = []
        tour = 0
        for e in tree.findall("tour"):
            n = e.find("tirage")
            ttt = tirage.tirage(n.text)
            n = e.find("coord")
            ccc = coord.coord()
            ccc.fromstr(n.text)
            n = e.find("mot")
            mmm = str(n.text)
            n = e.find("points")
            pts = int(n.text)
            tour += 1
            self.liste.append( (ttt, ccc, mmm, pts, tour) )

    def get_nom_partie(self) :
        return  os.path.basename(self.file_partie)

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
        controle, scrab = g.controle(c, m, t)
        print tour, c,m,t, controle
        if controle == 0 :
            print pts, g.point(c, m, scrab, d)
        else:
            print ">>> Controle non NUL"
        g.pose(c, m)
        print g
