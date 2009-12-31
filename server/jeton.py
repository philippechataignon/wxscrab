#! /usr/bin/env python
# -*- coding: utf-8 -*-
class jeton :
    """
    Définit la notion de jeton

    Utile surtout pour le tableau points qui permet de connaitre
    les points d'une lettre et le 0 pour le joker

    Utilisé par : case, grille, tirage
    """
    p = (1,3,3,2,1,4,2,4,1,8,10,1,2,1,1,3,8,1,1,1,1,4,10,10,10,10)
    l = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    points = dict(zip(l,p)) #{'A': 1, 'B': 3...}

    def __init__(self, lettre) :
        self.lettre = lettre
        if self.lettre in jeton.l : 
            self.point = jeton.points[self.lettre]
        else :
            self.point = 0
    def __str__(self) :
        return self.lettre

if __name__ == "__main__" :
    j = jeton('J') 
    print j,j.lettre, j.point
