#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import xml.dom.minidom
import time
import os

import coord
import tirage

class partie:
    def __init__(self, options) :
        self.options = options
        if self.options.game is None :
            rep = "partie"
            nom_partie = "p_%s.partie" % time.strftime("%Y%m%d%H%M%S")
            self.file_partie = os.path.join(rep, nom_partie)
            os.system("../gen/gen_part -d %s > %s" % (self.options.dico, self.file_partie))
        else :
            self.file_partie = self.options.game
        self.dom = xml.dom.minidom.parse(self.file_partie)
        self.liste = []
        tour = 0
        for e in self.dom.getElementsByTagName("tour"):
            for node in e.getElementsByTagName("tirage"):
                for n in node.childNodes:
                    if n.nodeType == node.TEXT_NODE:
                            tt = n.data.strip()
            for node in e.getElementsByTagName("coord"):
                for n in node.childNodes:
                    if n.nodeType == node.TEXT_NODE:
                            cc = n.data.strip()
            for node in e.getElementsByTagName("mot"):
                for n in node.childNodes:
                    if n.nodeType == node.TEXT_NODE:
                            mm = n.data.strip()
            for node in e.getElementsByTagName("points"):
                for n in node.childNodes:
                    if n.nodeType == node.TEXT_NODE:
                            pts = int(n.data.strip())
            ttt = tirage.tirage(tt)
            ccc = coord.coord()
            ccc.fromstr(cc)
            mmm = str(mm)
            tour += 1
            self.liste.append( (ttt, ccc, mmm, pts, tour) )
        self.num = 0


    def get_nom_partie(self) :
        return  os.path.basename(self.file_partie)

    def get_tour(self, num) :
        if self.num < len(self.liste) :
            return self.liste[self.num]
        else :
            return None

    def get_next_tour(self) :
        if self.num < len(self.liste) :
            l = self.liste[self.num]
            self.num += 1
            return l
        else :
            return None

if __name__ == '__main__' :
    import dico
    import grille
    class options :
        def __init__(self) :
            self.dico = "../dic/ods5.dawg"
            self.game = "partie/p_20101231164246.partie"

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
