#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
sys.path.append('../common')

import case
import jeton

OO = 0
LD = 1
LT = 2
MD = 3
MT = 4

erreur_msg = {
  1:   "Contradiction avec des lettres déjà posées sur la grille", 
  2:   "Mot impossible avec les lettres du tirage" ,
  3:   "Coordonnées mal indiquées" ,
  4:   "Pas de nouvelles lettres posées" ,
  5:   "Impossible à poser : pas de lettres en soutien" ,
  6:   "Le mot doit passer par la case centrale" ,
  7:   "Le mot sort du plateau" ,
  8:   "Il faut au moins deux lettres pour le mot" ,
  10:  "Il y a déjà une lettre avant le mot posé" ,
  11:  "Il y a déjà une lettre après le mot posé" ,
  12:  "Vérifier une interversion horizontal-vertical" ,
  13:  "Le mot proposé n'existe pas" ,
  14:  "Un des mots formés n'existe pas" ,
}

mult =   ((MT,OO,OO,LD,OO,OO,OO,MT,OO,OO,OO,LD,OO,OO,MT),
          (OO,MD,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,MD,OO),
          (OO,OO,MD,OO,OO,OO,LD,OO,LD,OO,OO,OO,MD,OO,OO),
          (LD,OO,OO,MD,OO,OO,OO,LD,OO,OO,OO,MD,OO,OO,LD),
          (OO,OO,OO,OO,MD,OO,OO,OO,OO,OO,MD,OO,OO,OO,OO),
          (OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO),
          (OO,OO,LD,OO,OO,OO,LD,OO,LD,OO,OO,OO,LD,OO,OO),
          (MT,OO,OO,LD,OO,OO,OO,MD,OO,OO,OO,LD,OO,OO,MT),
          (OO,OO,LD,OO,OO,OO,LD,OO,LD,OO,OO,OO,LD,OO,OO),
          (OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,LT,OO),
          (OO,OO,OO,OO,MD,OO,OO,OO,OO,OO,MD,OO,OO,OO,OO),
          (LD,OO,OO,MD,OO,OO,OO,LD,OO,OO,OO,MD,OO,OO,LD),
          (OO,OO,MD,OO,OO,OO,LD,OO,LD,OO,OO,OO,MD,OO,OO),
          (OO,MD,OO,OO,OO,LT,OO,OO,OO,LT,OO,OO,OO,MD,OO),
          (MT,OO,OO,LD,OO,OO,OO,MT,OO,OO,OO,LD,OO,OO,MT))

class grille :
    """
    Définit la grille comme un dictionnaire de cases sur clé tuple (x,y)

    Fournit plusieurs fonctions de cases
    Fournit également les deux grandes fonctions : controle et point
    """
    def __init__(self) :
        self.cases = {}
        for x in range(15) :
            for y in range(15) :
                self.cases[(x,y)] = case.case(x, y, mult[x][y])

    def __str__(self) :
        vide = '.'
        saut = '\n'
        m = []
        for y in range(0,15) :
            for x in range(0,15) :
                j = self.cases[(x,y)].jeton
                if j is None :
                    m.append(vide)
                else :
                    m.append(j.lettre)
            m.append(saut)
        return "".join(m)

    def aff_erreur(self, erreur) :
        return erreur_msg.get(erreur, "Erreur inconnue")

    def case_prime(self, coord) :
        if coord.isOK():
            return self.cases[(coord.x(),coord.y())].mult
        else:
            return 0

    def case_coord(self, coord) :
        if coord.isOK():
            return self.cases[(coord.x(),coord.y())]
        else:
            return None

    def case_vide(self, coord) :
        if coord.isOK():
            return self.cases[(coord.x(),coord.y())].isVide()
        else:
            return False

    def case_nonvide(self, coord) :
        if coord.isOK():
            return not self.cases[(coord.x(),coord.y())].isVide()
        else:
            return False

    def case_joker(self, coord) :
        if coord.isOK():
            return self.cases[(coord.x(),coord.y())].isJoker()
        else:
            return False

    def pose(self, c, mot) :
        for l in mot :
            if self.case_vide(c) :
                self.case_coord(c).jeton = jeton.jeton(l)
            c = c.next()
        
    def vide(self) :
        for case in self.cases.itervalues() :
            if not case.isVide() :
                return False
        return True 

    def controle (self, w_coord , w_mot , w_tirage) :
        """ 
        Controle à partir d'une coord, d'un mot et d'un tirage si une erreur
        de placement est rencontré
        Renvoie le code d'erreur ; 0 si pas d'erreur
        Positionne le booléen scrab à TRUE si un scrab a été réalisé (voir point)
        """

        soutien = False                     # vérifie que le mot placé a un soutien (sauf tour 1)
        newlettre = False                   # vérifie qu'au moins une nouvelle lettre a été posée
        passecentrale = False               # vérifie que le mot passe en H8 au tour 1
        scrab = False                       # test si un scrabble est réalisé

        t = w_tirage.copy()                 # copie du tirage pour travailler 

        if not w_coord.isOK() :             # si coordonnée en erreur
            return 3

        if len(w_mot) < 2 :                 # si le mot est trop court
            return 8

        # case précédente occupée
        if self.case_nonvide(w_coord.prev()) :
            return 10

        if w_coord.is_bord_droit() :               # on part d'un bord
            return 12

        i_coord = w_coord            # i_coord : indice de coordonnée courante

        for l in w_mot :
            if not i_coord.isOK() :         # coord en erreur
                return 7

            # positionne passecentrale si on passe en H8
            if i_coord.is_centre() : 
                passecentrale = True

            # cas ou la case est vide
            if self.case_vide(i_coord) :
                # on retire la lettre du tirage si on peut
                # sinon erreur
                if t.retire(l) == True :
                    newlettre = True 
                else:
                    return 2

                # si la case dessus ou dessous est occupée, on a un soutien
                if self.case_nonvide(i_coord.haut()) or self.case_nonvide(i_coord.bas()) :
                    soutien = True 
            else :
                # cas où la case est occupée
                # dans ce cas, on a un soutien pour le mot
                # on vérifie la compatibilité entre la lettre déjà présente
                # et celle qui est dans le mot proposé
                if l.upper() != self.case_coord(i_coord).jeton.lettre.upper() :
                    return 1
                soutien = True 
            # case suivante
            i_coord = i_coord.next()

        if self.case_nonvide(i_coord) :         #lettre sur la case suivante
            return 11

        if not newlettre :                      # pas de nouvelles lettres
            return 4

        if self.vide() :                        # premier tour
            if not passecentrale :              # pas de passage par case centrale au tour 1
                return 6
        else :                                  # tour ordinaire
            if not soutien  :                   # pas de soutien sur une grille non vide
                return 5

        scrab = w_tirage.isPlein() and t.isVide()     # scrabble réalisé
        if scrab :
            return -1                           # pas d'erreur et scrabble
        else :
            return 0                           # pas d'erreur

    def point (self, w_coord , w_mot , scrab , dic) :
        """
        Renvoie le nombre de points de la proposition coord / mot
        Il faut indiquer le booléen scrab issu de controle

        Le nombre de point est renvoyé dans tous les cas, y compris si le mot n'existe pas.
        Une liste (mot_nonex) est constituée des mots non existants

        Test réalisé avec dic
        """
        
        point = 0          # initialise le score
        totv = 0           # initialse le cumul des mots réalisés en posant des lettres
        multmot = 1        # initialise le multiplicateur de score
        mot_nonex = []     # initialise liste mot non existant a vide

        i_coord = w_coord            # i_coord : indice de coordonnée courante

        if dic.isMot(w_mot) == False :      # si le mot proposé n'existe pas
            mot_nonex.append(w_mot)

        for l in w_mot :
            # on parcourt chaque lettre du mot        
            jl = jeton.jeton(l)
            pointl = jl.point               # nombre de points de la lettre courante

            # gestion des primes de lettre

            if self.case_vide(i_coord) :
                if self.case_prime(i_coord) == LT :
                    pointl *= 3
                elif self.case_prime(i_coord) == LD :
                    pointl *= 2
                #si la case est vide, on regarde si un mot est réalisé
                tvois = False               # mot voisin réalisé ?
                pointv = pointl             # initailise le score du mot voisin
                motv = l  # initialise la chaine du mot voisin

                # on remonte vers le haut/gauche tant que les cases sont occupées
                j_coord = i_coord.haut()
                while self.case_nonvide(j_coord) : 
                    j = self.case_coord(j_coord).jeton
                    motv = j.lettre + motv  # on insère les lettres par l'avant
                    pointv += j.point       # on cumule les points sans prime
                    tvois = True
                    j_coord=j_coord.haut()

                # on descend vers le bas/droite tant que les cases sont occupées
                j_coord = i_coord.bas()
                while self.case_nonvide(j_coord) : 
                    j = self.case_coord(j_coord).jeton
                    motv += j.lettre        # on insère les lettres par l'avant
                    pointv += j.point       # on cumule les points sans prime
                    tvois = True
                    j_coord=j_coord.bas()

                # gestion des primes de mot
                if self.case_prime(i_coord) == MT :
                    multmot *= 3            # le multiplicateur du mot posé est mis à jour
                    pointv  *= 3            # le score du mot voisin bénéficie de la prime
                elif self.case_prime(i_coord) == MD :
                    multmot *= 2            # le multiplicateur du mot posé est mis à jour
                    pointv  *= 2            # le score du mot voisin bénéficie de la prime

                # vérification de l'existence des mots voisins
                # renvoie 0 pour le score global si inexistant
                # met à jour totv sinon
                if tvois :
                    if dic.isMot(motv) == False : 
                        mot_nonex.append(motv)
                    totv += pointv 
            else :
                # la case n'est pas vide
                if self.case_joker(i_coord) :
                    # la case contient un joker, donc 0 point
                    # y compris si l'utilisateur n'a pas "shifté" la lettre
                    pointl = 0 

            # fin de l'analyse de la lettre courante
            # on met à jour point et on passe au suivant
            point += pointl
            i_coord = i_coord.next()

        # calcul global du score :
        # on applique le multiplicateur de score et on ajoute
        # le score des mots voisins

        point = point * multmot + totv

        # plus la prime de scrabble éventuele de 50 points
        if scrab :
            point += 50

        return point, mot_nonex

if __name__ == '__main__' :
    import coord
    import dico
    import tirage

    d = dico.dico("../dic/ods5.dawg")
    g = grille()
    t = tirage.tirage("TETESAU")
    c = coord.coord()

    c.fromstr("H8")
    m = "TATES"
    controle = g.controle(c, m, t)
    print controle
    if controle <= 0 :
        print g.point(c, m, controle, d)
    g.pose(c, m)
    print g

    t = tirage.tirage("AEPESTU")
    c.fromstr("7H")
    m = "EPATES"
    controle = g.controle(c, m, t)
    print controle
    if controle <= 0 :
        print g.point(c, m, controle, d)
    g.pose(c, m)
    print g
