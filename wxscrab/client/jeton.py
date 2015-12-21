# -*- coding: utf-8 -*-
NUL = 0
TEMP = 1
PREPOSE = 2
POSE = 3
TIRAGE = 4
RELIQUAT = 5

pts={'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,
     'J':8,'K':10,'L':1,'M':2,'N':1,'O':1,'P':3,'Q':8,'R':1, 
     'S':1,'T':1,'U':1,'V':4,'W':10,'X':10,'Y':10,'Z':10,'?':0}

#Fichier définition class
class jeton :
    def __init__(self, lettre, status) :
        self.__lettre = lettre
        self.__status = status
        if self.is_joker() :
            self.__point = str(pts['?'])
        else :
            self.__point = str(pts[lettre])

    def __str__(self) :
        return self.__lettre

    def is_joker(self) :
        return 'a' <= self.__lettre <='z' or self.__lettre == '?'

    def get_status(self) :
        return self.__status

    def set_status(self, status) :
        self.__status = status

    def get_lettre(self) :
        return self.__lettre

    def set_lettre(self, lettre) :
        assert self.is_joker(), "Change lettre d'un jeton non joker"
        self.__lettre = lettre

    def get_point(self) :
        return self.__point
