#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import jeton
import dnd
import case_tirage
import random

class tirage(wx.Window) :
    """
    Représente le tirage
    """

    def __init__(self, parent, app) :
        wx.Window.__init__(self, parent, -1)
        self.app = app
        self.cases=[]
        self.allowdrag = False
        self.nbpos = int(self.app.settings.get("tirage_nbpos"))
        size = self.app.skin.get("size")
        fill = self.app.skin.get("fill")
        for pos in xrange(self.nbpos)  :
            case = case_tirage.case_tirage(pos, self.app, self, -1,  wx.NullBitmap, \
                ((size+fill)*pos, 0))
            self.cases.append(case)

## Fonctions basiques

    def cree_tirage(self, mot) :
        """Cree les jetons quand on reçoit un mot"""
        self.vide_tirage()
        pos = 0
        for c in mot :
            lettre = c.upper()
            if  'A'<= lettre <= 'Z' or lettre == '?' :
                self.cases[pos].pose(jeton.jeton(lettre, self.app.skin, jeton.TEMP))
                self.app.reliquat.retire(lettre)
                pos += 1
            elif lettre in ("+",'-') :
                pos += 1

    def vide_tirage(self) :
        """Vide toutes les cases et remet les jetons dans le reliquat

        Appelé par cree_tirage
        """
        for pos in xrange(self.nbpos)  :
            j = self.cases[pos].jeton
            if j is not None :
                l = j.lettre
                self.cases[pos].vide()
                self.app.reliquat.remet(l)

    def allowdrags(self, allow) :
        for c in self.cases :
            c.allowdrag = allow

## Principales fonctions publiques 
    def pos_retire_jeton(self, lettre) :
        """Retire et renvoie la position dans le tirage
        qui correspond à la lettre transmise.
        On choisit le premier jeton ayant la lettre, sinon le joker s'il y en a un.
        Pour forcer le joker, on passe la lettre en minuscule
        """
        if not( 'A' <= lettre <= 'Z' or 'a' <= lettre <= 'z') :
            return None
        # Liste des cases non vides
        lc = [case for case in self.cases if not case.is_vide()]
        if 'A' <= lettre <= 'Z' :
            for case in lc :
                j = case.jeton
                if j.lettre == lettre :
                    return case.pos
        for case in lc :
            j = case.jeton
            if j.lettre == "?" :
                j.lettre = lettre.lower()
                return case.pos
        return None

    def retire_jeton_case(self, case) :
        if case.is_vide() :
            return None
        else :
            j = case.jeton
            case.vide()
            return j

    def retire_jeton(self, lettre) :
        pos = self.pos_retire_jeton(lettre) 
        if pos is not None :
            j = self.retire_jeton_case(self.cases[pos])
            return j
        return None

    def remet(self, j) :
        """Remet le jeton j dans le tirage
        On remet le jeton dans la première case libre trouvée
        """
        for pos in xrange(self.nbpos) :
            if self.cases[pos].is_vide() :
                if j.is_joker() :
                    j.lettre = '?'
                j.status = jeton.TEMP
                self.cases[pos].pose(j)
                break

## Fonctions de manipulation : tri, swap...

    def alpha(self) :
        lj = [case.jeton for case in self.cases if not case.is_vide()]
        lj.sort(key=lambda x: x.lettre.lower())
        self.permute(lj)

    def shuffle(self) :
        lj = [case.jeton for case in self.cases if not case.is_vide()]
        random.shuffle(lj)
        self.permute(lj)

    def permute(self, lj) :
        for pos in xrange(self.nbpos) :
            if pos < len(lj) :
                self.cases[pos].pose(lj[pos])
            else :
                self.cases[pos].vide()

    def shift(self, pos) :
        end = -1
        for i in xrange(pos+1, self.nbpos) :
            if self.cases[i].is_vide() :
                end = i
                break
        if end >= 0 :
            for i in xrange(end, pos, -1) :
                self.cases[i].jeton = self.cases[i-1].jeton
                self.cases[i].redraw()
            self.cases[pos].vide()
        else :
            end2 = -1
            for i in xrange(0, pos) :
                if self.cases[i].is_vide() :
                    end2 = i
                    break
            if end2 >= 0 :
                for i in xrange(end2, pos) :
                    self.cases[i].jeton = self.cases[i+1].jeton
                    self.cases[i].redraw()
                self.cases[pos].vide()

    def swap(self, pos_old, pos_new) :
        self.cases[pos_old].jeton, self.cases[pos_new].jeton = self.cases[pos_new].jeton, self.cases[pos_old].jeton  
        self.cases[pos_old].redraw()
        self.cases[pos_new].redraw()
