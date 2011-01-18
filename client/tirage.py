#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import jeton
import dnd
import case_tirage
import random

class tirage(wx.Panel) :
    """
    Représente le tirage
    """

    def __init__(self, parent, app) :
        wx.Panel.__init__(self, parent, -1)
        self.app = app
        self.cases=[]
        self.allowdrag = False
        nbpos = self.app.settings["view_tirage_nbpos"]
        size = self.app.settings["size_jeton"]
        fill = self.app.settings["size_fill"]
        sizer = wx.GridSizer(rows = 1, cols = nbpos, hgap=fill, vgap=fill)
        for pos in xrange(nbpos)  :
            case = case_tirage.case_tirage(self, pos)
            self.cases.append(case)
            sizer.Add(case, flag=wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.Fit()

## Fonctions basiques

    def cases_non_vides(self) :
        return [case for case in self.cases if not case.is_vide()]

    def nb_pos(self) :
        return len(self.cases)

    def nb_jeton(self) :
        return len(self.cases_non_vides())

    def cree_tirage(self, mot) :
        """Cree les jetons quand on reçoit un mot"""
        self.vide_tirage()
        pos = 0
        for c in mot :
            lettre = c.upper()
            if  'A'<= lettre <= 'Z' or lettre == '?' :
                j = self.app.reliquat.move_from(self.cases[pos], jeton.TIRAGE, lettre)
                pos += 1
            elif lettre in ("+",'-') :
                pos += 1

    def vide_tirage(self) :
        """Vide toutes les cases et remet les jetons dans le reliquat
        """
        for c in self.cases :
            self.app.reliquat.move_to(c)

    def allowdrags(self, allow) :
        for c in self.cases :
            c.allowdrag = allow


    def cherche_case_lettre(self, lettre) :
        cherche = "?" if 'a' <= lettre <= 'z' else lettre
        c_dep = None
        for c in self.cases_non_vides() :
            if c.jeton.lettre == cherche :
                c_dep = c
                break
            if c.jeton.lettre == "?" : # joker au coup où
                c_dep = c
        return c_dep

## Principales fonctions publiques 
    def move_from(self, c_dest, status, lettre) :
        # si destination non vide, on dégage
        if not c_dest.is_vide() :
            return False
        c_dep = self.cherche_case_lettre(lettre)
        # on a un jeton dans le tirage :
        # le transfert est possible
        if c_dep is not None :
            j = c_dep.jeton 
            j.set_status(status)
            if j.lettre == "?" : #cas du joker
                j.lettre = lettre.lower()
            c_dest.pose(j)
            c_dep.vide()
            return True
        else :
            return False

    def move_to(self, c_dep) :
        """Remet le jeton j de la case c_dep 
        dans la première case libre trouvée
        """
        if c_dep.is_vide() :
            return False

        j = c_dep.jeton
        for c in self.cases :
            if c.is_vide() :
                if j.is_joker() :
                    j.lettre = '?'
                j.set_status(jeton.TIRAGE)
                c.pose(j)
                c_dep.vide()
                return True
        return False

## Fonctions de manipulation : tri, swap...

    def compacte(self) :
        """ Met tous les jetons à gauche et toutes les cases vides à droite
        """
        p_vide = self.nb_pos() - 1
        while (self.cases[p_vide].is_vide()) :
            p_vide -= 1
        p = 0
        while (p < p_vide) :
            if self.cases[p].is_vide() :
                self.swap(p, p_vide)
                while (self.cases[p_vide].is_vide()) :
                    p_vide -= 1
            p += 1

    def alpha(self): 
        self.compacte()
        lj = [case.jeton for case in self.cases_non_vides()]
        lj.sort(key=lambda x: x.lettre.lower())
        for i in xrange(len(lj)) :
            self.cases[i].vide()
            self.cases[i].pose(lj[i])

    def shuffle(self) :
        self.compacte()
        nbj = self.nb_jeton()
        for i in xrange(nbj) :
            alea = random.randint(0, nbj-1)
            self.swap(i, alea)

    def shift(self, pos) :
        end = -1
        # cherche index première case vide à droite
        for i in xrange(pos+1, self.nb_pos()) :
            if self.cases[i].is_vide() :
                end = i
                break
        # il y a une case vide : on décale en posant et vidant à chaque pas
        if end >= 0 :
            for i in xrange(end, pos, -1) :
                self.cases[i].pose(self.cases[i-1].jeton)
                self.cases[i-1].vide()
            self.cases[pos].vide()
        else :
            # symétrique du traitement précédent
            # mais sur la gauche
            end2 = -1
            for i in xrange(0, pos) :
                if self.cases[i].is_vide() :
                    end2 = i
                    break
            if end2 >= 0 :
                for i in xrange(end2, pos) :
                    self.cases[i].pose(self.cases[i+1].jeton)
                    self.cases[i+1].vide()
                self.cases[pos].vide()

    def swap(self, pos_old, pos_new) :
        self.swap_cases(self.cases[pos_old], self.cases[pos_new])
        
    def swap_cases(self, dep, arr) :
        dep.jeton, arr.jeton  = arr.jeton, dep.jeton
        dep.redraw()
        arr.redraw()
