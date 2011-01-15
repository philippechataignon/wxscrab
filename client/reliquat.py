#! /usr/bin/env python
# -*- coding: utf-8 -*-
class reliquat :
    def __init__(self) :
        self.char="ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
        repart = [9,2,2,3,15,2,2,2,8,1,1,5,3,6,6,2,1,6,6,6,6,2,1,1,1,1,2]
        self.bag=dict(zip(self.char,repart))

    def __str__(self) :
        return " ".join([l*self.bag[l] for l in self.char if self.bag[l] != 0 ])

    def retire(self, mot) :
        for l in mot :
            if 'a' <= l <= 'z' :
                l = '?'
            self.bag[l] -= 1

    def remet(self, mot) :
        for l in mot :
            if 'a' <= l <= 'z' :
                l = '?'
            self.bag[l] += 1

if __name__ == '__main__' :
    r = reliquat()
    print r
    r.retire("AvEZ")
    print r
