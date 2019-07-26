#!/usr/bin/env python3
import dic

class Dico():
    def __init__(self, nom_dico):
        self.d = dic.Dico()
        ret = dic.Dic_init(self.d, nom_dico)
        if ret:
            print("Init dico : erreur", ret)
            raise ValueError

    def isMot(self, mot):
        return dic.isMot(self.d, mot)

    def __del__(self):
        dic.Dic_destroy(self.d)

if __name__ == '__main__':
    d = Dico("/home/philippe/wxscrab/dic/ods7.dico")
    print(d.isMot("pipo"))
    print(d.isMot("pipon"))

