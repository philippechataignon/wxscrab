#! /usr/bin/env python
# -*- coding: utf-8 -*-
import jeton

class reliquat :
    def __init__(self, settings) :
        self.settings = settings
        self.char="ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
        repart = [9,2,2,3,15,2,2,2,8,1,1,5,3,6,6,2,1,6,6,6,6,2,1,1,1,1,2]
        self.freq = dict(zip(self.char,repart))
        self.jetons = []
        for lettre in self.char :
            for i in xrange(self.freq[lettre]) :
                self.jetons.append(jeton.jeton(lettre, jeton.RELIQUAT, self.settings))

    def __str__(self) :
        return " ".join([l*self.freq[l] for l in self.char if self.freq[l] != 0 ])

    def retire(self, lettre, status) :
        cherche = "?" if 'a' <= lettre <= 'z' else lettre
        self.freq[cherche] -= 1
        ll = [j.lettre for j in self.jetons]
        pos = ll.index(cherche)
        j = self.jetons.pop(pos)
        j.set_status(status)
        if cherche == "?" :
            j.lettre = lettre
        return j

    def remet(self, j) :
        if 'a' <= j.lettre <= 'z' :
            j.lettre = '?'
        self.freq[j.lettre] += 1
        j.set_status(jeton.RELIQUAT)
        self.jetons.append(j)

if __name__ == '__main__' :
    r = reliquat()
    print r
    r.retire("AvEZ")
    print r
