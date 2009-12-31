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
                self.cases[pos].met(jeton.jeton(lettre, self.app.skin, status=jeton.TIRAGE))
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
                self.cases[pos].enleve()
                self.app.reliquat.remet(l)

    def allowdrags(self, allow) :
        for c in self.cases :
            c.allowdrag = allow

## Principales fonctions publiques 

    def retire_jeton(self, lettre, status) :
        """Retire et renvoie le jeton du tirage
        Renvoit le jeton qui correspond à la lettre transmise.
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
                    case.enleve()
                    j.status = status
                    return j

        for case in lc :
            j = case.jeton
            if j.lettre == "?" :
                j.lettre = lettre.lower()
                case.enleve()
                j.status = status
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
                j.status = jeton.TIRAGE 
                self.cases[pos].met(j)
                break

## Fonctions de manipulation : tri, swap...

    def alpha(self) :
        self.permute('A')

    def shuffle(self) :
        self.permute('R')

    def permute(self, code) :
        lj = [case.jeton for case in self.cases if not case.is_vide()]
        if code == 'A' :
            lj.sort(key=lambda x: x.lettre.lower())
        elif code == 'R' :
            random.shuffle(lj)
        for pos in xrange(self.nbpos) :
            if pos < len(lj) :
                self.cases[pos].met(lj[pos])
            else :
                self.cases[pos].enleve()

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
            self.cases[pos].enleve()
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
                self.cases[pos].enleve()

    def swap(self, pos_old, pos_new) :
        self.cases[pos_old].jeton, self.cases[pos_new].jeton = self.cases[pos_new].jeton, self.cases[pos_old].jeton  
        self.cases[pos_old].redraw()
        self.cases[pos_new].redraw()

