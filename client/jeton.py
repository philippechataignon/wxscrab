#! /usr/bin/env python
# -*- coding: utf-8 -*-
import utils

NUL = 0
TEMP = 1
PREPOSE = 2
POSE = 3

pts={'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,
     'J':8,'K':10,'L':1,'M':2,'N':1,'O':1,'P':3,'Q':8,'R':1, 
     'S':1,'T':1,'U':1,'V':4,'W':10,'X':10,'Y':10,'Z':10,'?':0}

#Fichier définition class
class jeton :
    def __init__(self, lettre, status, settings) :
        self.settings = settings
        self.lettre = lettre
        self.status = status
        if self.is_joker() :
            self.point = str(pts['?'])
        else :
            self.point = str(pts[self.lettre])

    def __str__(self) :
        return self.lettre

    def is_joker(self) :
        return 'a' <= self.lettre <='z' or self.lettre == '?'

    def get_status(self) :
        return self.status

    def set_status(self, status) :
        self.status = status

    def deplace(self, dep, arr) :
        """ Déplace un jeton de la case dep vers la case arr
            Avec le statut d'arrivée status
        """
        if dep.tirage :
            if arr.tirage :
                "Départ et arrivée dans tirage : on swap"
                dep.jeton, arr.jeton = arr.jeton, dep.jeton 
                dep.redraw()
                arr.redraw()
            elif arr.is_vide() :
                "Arrivée sur la grille"
                if not self.is_joker() : #ne pas poser le joker
                    dep.jeton.set_status(TEMP)
                    arr.pose(dep.jeton)
                    dep.vide()
