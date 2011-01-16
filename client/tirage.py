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
        self.nbpos = self.app.settings["view_tirage_nbpos"]
        size = self.app.settings["size_jeton"]
        fill = self.app.settings["size_fill"]
        sizer = wx.GridSizer(rows = 1, cols = self.nbpos, hgap=fill, vgap=fill)
        for pos in xrange(self.nbpos)  :
            case = case_tirage.case_tirage(self, pos)
            self.cases.append(case)
            sizer.Add(case, flag=wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.Fit()

## Fonctions basiques

    def cases_non_vides(self) :
        return [case for case in self.cases if not case.is_vide()]

    def cree_tirage(self, mot) :
        """Cree les jetons quand on reçoit un mot"""
        self.vide_tirage()
        pos = 0
        for c in mot :
            lettre = c.upper()
            if  'A'<= lettre <= 'Z' or lettre == '?' :
                j = self.app.reliquat.retire(lettre, jeton.TIRAGE)
                self.cases[pos].pose(j)
                pos += 1
            elif lettre in ("+",'-') :
                pos += 1

    def vide_tirage(self) :
        """Vide toutes les cases et remet les jetons dans le reliquat
        """
        for c in self.cases_non_vides() :
            self.app.reliquat.remet(c.jeton)
            c.vide()

    def allowdrags(self, allow) :
        for c in self.cases :
            c.allowdrag = allow

## Principales fonctions publiques 
    def retire_jeton(self, lettre) :
        cherche = "?" if 'a' <= lettre <= 'z' else lettre
        ok = False
        for c in self.cases_non_vides() :
            if c.jeton.lettre == cherche :
                case = c
                ok = True
                break
            if c.jeton.lettre == "?" : # joker au coup où
                case = c
                ok = True 

        if ok :
            j = case.jeton 
            j.set_status(jeton.TEMP)
            if j.lettre == "?" : #cas du joker
                j.lettre = lettre.lower()
            case.vide()
            return j
        else :
            return None

    def remet(self, j) :
        """Remet le jeton j dans le tirage
        On remet le jeton dans la première case libre trouvée
        """
        for c in self.cases :
            if c.is_vide() :
                if j.is_joker() :
                    j.lettre = '?'
                j.set_status(jeton.TIRAGE)
                c.pose(j)
                break

## Fonctions de manipulation : tri, swap...

    def alpha(self): 
        # implémente un magnifique tri à bulles...
        for n in xrange(self.nbpos -1 ) :
            for i in xrange(self.nbpos-1) :
                if self.cases[i+1].is_vide() :
                    continue
                if self.cases[i].is_vide() or self.cases[i].jeton.lettre > self.cases[i+1].jeton.lettre :
                    self.swap(i, i+1)

    def shuffle(self) :
        for i in xrange(self.nbpos) :
            alea = random.randint(0, self.nbpos-1)
            self.swap(i, alea)

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

