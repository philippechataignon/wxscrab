#! /usr/bin/env p_ython
# -*- coding: utf-8 -*-
NUL = 0
HOR = 1
VER = 2
class coord :
    """
    Définit la coordonnée

    Une coordonnée est définie par une position 0<=x<=14 et 0<=y<=14 et une direction HOR, VER
    Pour créer une coordonnée à partir d'une référence alphanumérique, procéder en 2 temps :
        c = coord()
        c.fromstr("O16")

    La coordonnée peut être en erreur (cas d'une coordonnée vide ou sur les bords)
    
    Utilisé dans : grille, case, partie
    """

    def __init__(self, x = -1, y = -1, dir=HOR, coo_str = None ) :
        if coo_str is None :
            if 0<=x<=14 and 0<=y<=14 and dir in [HOR, VER] :
                self._x = x
                self._y = y
                self._dir = dir
                self._error = False
            else :
                self.set_error()
        else :
            self.fromstr(coo_str)

    def __str__(self):
        "Sortie alphanumérique de la coordonnée. Ex : 8H"
        if self._error == False :
            if self._dir == HOR:
                return "%c%d" % (65+self._y, self._x+1)
            elif self._dir == VER :
                return "%d%c" % (self._x+1, 65+self._y)
        else :
            return "EE0"
        
    def __eq__(self, other) :
        if self._x==other._x and self._y==other._y :
            return True
        else :
            return False

    def set_error(self) :
            self._x = -1
            self._y = -1
            self._dir = NUL
            self._error = True

    def x(self) :
        return self._x

    def y(self) :
        return self._y

    def dir(self) :
        return self._dir

    def isOK(self) :
        return self._error == False

    def is_bord_droit(self) :
        return (self._dir == HOR and self._x == 14) or (self._dir == VER and self._y == 14)

    def is_centre(self) :
        return self._x == 7 and self._y == 7 

    def change_dir(self) :
        if self._dir == HOR :
            self._dir = VER
        elif self._dir == VER :
            self._dir = HOR
        else :
            self._dir = HOR

    def set_dir(self, dir) :
        self._dir = dir

    def fromstr(self, coo_str) :
        print "fromstr : %s" % coo_str
        "Affecte une coordonnée à partir d'une référence alphanumérique"
        coo_str = coo_str.replace(' ','').upper()
        l = len(coo_str)
        if l == 2 :
            if "A" <= coo_str[0] <= "O" :
                if '1' <= coo_str[1] <= '9' :
                    self._x = int(coo_str[1])-1
                    self._y = ord(coo_str[0])-65
                    self._dir = HOR
                    self._error = False
                else :
                    self.set_error()

            if "1" <= coo_str[0] <= "9" :
                if 'A' <= coo_str[1] <= 'O' :
                    self._x = int(coo_str[0])-1
                    self._y = ord(coo_str[1])-65
                    self._dir = VER
                    self._error = False
                else :
                    self.set_error()
        elif l == 3 :
            if coo_str[0] == '1' and '0' <= coo_str[1] <= '5' and 'A' <= coo_str[2] <= 'O' :
                self._y = ord(coo_str[2])-65
                self._x = int(coo_str[0:2])-1
                self._dir = VER
                self._error = False
            elif 'A' <= coo_str[0] <= 'O' and coo_str[1] == '1' and '0' <= coo_str[2] <= '5' :
                self._y = ord(coo_str[0])-65
                self._x = int(coo_str[1:3])-1
                self._dir = HOR
                self._error = False
            else :
                self.set_error()
        else :
            self.set_error()

    def next(self) :
        "Coordonnée suivante selon direction"
        if self._dir == HOR :
            return coord(self._x + 1, self._y, self._dir)
        else :
            return coord(self._x, self._y + 1, self._dir)

    def prev(self) :
        "Coordonnée précédente selon direction"
        if self._dir == HOR :
            return coord(self._x - 1, self._y, self._dir)
        else :
            return coord(self._x, self._y - 1, self._dir)

    def haut(self) :
        "Coordonnée au-dessus selon direction"
        if self._dir == HOR :
            return coord(self._x , self._y -1, self._dir)
        else :
            return coord(self._x - 1, self._y, self._dir)
    def bas(self) :
        "Coordonnée au-dessous selon direction"
        if self._dir == HOR :
            return coord(self._x, self._y + 1, self._dir)
        else :
            return coord(self._x + 1, self._y, self._dir)

if __name__ == '__main__' :
    e = coord(1,1)
    c = coord(coo_str=" h    8")
    print e,c
    #e.fromstr("8H")
    #print e
    #print c==e
    #c.fromstr("E10")
    #print c
    #c.fromstr("O16")
    #print c
    #c.fromstr("10A")
    #print c
    #c.fromstr("18A")
    #print c
    #c.fromstr("9Z")
    #print c
    #c.fromstr("Z9")
    #print c
    #c.fromstr("A0")
    #print c
    #c.fromstr("A1")
    #print c
    #c.fromstr("A1989")
    #print c
    #c = coord(14,14)
    #print c
    #d = c
    #print d
    #print type(c), type(d)
    #print c,d
    #d = d.next()
    #print c,d
    #c.change_dir()
    #print c
    #c.fromstr("H8")
    #print c,c.next(),c.prev(),c.haut(),c.bas()
    #c.fromstr("H15")
    #print c,c.next(),c.prev(),c.haut(),c.bas()
