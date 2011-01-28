#! /usr/bin/env python2
# -*- coding: utf-8 -*-

pts={'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,
     'J':8,'K':10,'L':1,'M':2,'N':1,'O':1,'P':3,'Q':8,'R':1, 
     'S':1,'T':1,'U':1,'V':4,'W':10,'X':10,'Y':10,'Z':10,'?':0}

class jeton :
    """
    Définit la notion de jeton

    Utile surtout pour le tableau points qui permet de connaitre
    les points d'une lettre et le 0 pour le joker

    Utilisé par : case, grille, tirage
    """
    def __init__(self, lettre) :
        self.lettre = lettre
        if self.lettre in pts :
            self.point = pts[self.lettre]
        else :
            self.point = 0

    def __str__(self) :
        return self.lettre

if __name__ == "__main__" :
    j = jeton('J') 
    print j,j.lettre, j.point
