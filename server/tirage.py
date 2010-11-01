#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import jeton

class tirage :
    def __init__(self, mot) :
        self.mot = mot
        self.jetons=[]
        for c in self.mot :
            lettre = c.upper()
            if  'A'<= lettre <= 'Z' or lettre == '?': 
                j = jeton.jeton(lettre)
                self.jetons.append(j)

    def __str__(self) :
        return "".join([j.lettre for j in self.jetons])

    def __len__(self) :
        return len(self.jetons)

    def get_mot(self) :
        return self.mot

    def copy(self) :
        return tirage(self.mot)

    def isPlein(self) :
        return len(self) == 7

    def isVide(self) :
        return len(self) == 0

    def retire(self, lettre) :
        if  'a' <= lettre <= 'z' :
            lettre = '?'
        lettre = lettre.upper()
        if 'A' <= lettre <= 'Z' or lettre == '?' :
            for i,j in enumerate(self.jetons) :
                if j.lettre == lettre :
                    del self.jetons[i]
                    return True
        return False

if __name__ == '__main__' :
    t = tirage("AZERTYU")
    print t
    print len(t)
    print t.isPlein()
    print t.isVide()
    u = t.copy()
    u.retire('R')
    print t,u
    print len(u)
    print u.isPlein()
    print u.isVide()
