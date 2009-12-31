#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import coord

class case :
    """
    Définit la notion de case

    La case est utilisée par la grille.
    Elle possède une coordonnée, un multiplicateur et peut accueillir un jeton

    Utilisé par : grille
    """

    def __init__(self, x, y, mult) :
        self.coord = coord.coord(x,y)
        self.mult = mult
        self.jeton = None

    def isVide(self) :
        return self.jeton is None

    def isJoker(self) :
        if self.isVide() :
            return False
        else :
            return 'a' <= self.jeton.lettre <= 'z'
