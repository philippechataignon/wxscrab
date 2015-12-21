# -*- coding: utf-8 -*-
import jeton
char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
repart = [9,2,2,3,15,2,2,2,8,1,1,5,3,6,6,2,1,6,6,6,6,2,1,1,1,1,2]

class reliquat :
    def __init__(self) :
        self.__freq = dict(zip(char,repart))
        self.__jetons = []
        for lettre in char :
            for i in xrange(self.__freq[lettre]) :
                self.__jetons.append(jeton.jeton(lettre, jeton.RELIQUAT))

    def __str__(self) :
        return " ".join([l*self.__freq[l] for l in char if self.__freq[l] != 0 ])

    def move_from(self, c_dest, status, lettre) :
        """ Prend un jeton dans le reliquat pour le poser sur la case c_dest 
            avec un status donné et portant la lettre demandée
        """
        cherche = "?" if 'a' <= lettre <= 'z' else lettre
        self.__freq[cherche] -= 1
        ll = [j.get_lettre() for j in self.__jetons]
        pos = ll.index(cherche)
        j = self.__jetons.pop(pos)
        if cherche == "?" :
            j.set_lettre(lettre)
        j.set_status(status)
        c_dest.pose(j)
        return True

    def move_to(self, c_dep) :
        """ Remet un jeton dans le reliquat en provenance de c_dep
        """
        if c_dep.is_vide() :
            return False
        j = c_dep.prend()
        if 'a' <= j.get_lettre() <= 'z' :
            j.set_lettre('?')
        self.__freq[j.get_lettre()] += 1
        j.set_status(jeton.RELIQUAT)
        self.__jetons.append(j)
        return True

if __name__ == '__main__' :
    r = reliquat()
    print r
