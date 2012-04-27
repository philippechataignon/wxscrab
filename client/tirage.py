# -*- coding: utf-8 -*-
import wx
import random
import jeton
import case_tirage

class tirage(wx.Panel) :
    """
    Représente le tirage
    """
    def __init__(self, parent, app) :
        wx.Panel.__init__(self, parent, -1)
        self.app = app
        nbpos = self.app.settings["view_tirage_nbpos"]
        fill = self.app.settings["size_fill"]
        sizer = wx.GridSizer(rows = 1, cols = nbpos, hgap=fill, vgap=fill)
        self.cases=[]
        for pos in xrange(nbpos)  :
            case = case_tirage.case_tirage(self, pos)
            self.cases.append(case)
            sizer.Add(case, flag=wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.Fit()

## Fonctions basiques
    def nb_pos(self) :
        """ Renvoie nombre de cases du tirage 
        """
        return len(self.cases)

    def cree_tirage(self, mot) :
        """ Crée les jetons quand on reçoit un mot
        """
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
        """ Vide toutes les cases et remet les jetons dans le reliquat
        """
        for c in self.cases :
            self.app.reliquat.move_to(c)

    def cherche_case_lettre(self, lettre) :
        """ Renvoie la première case portant un jeton ayant la lettre indiquée
        """
        cherche = "?" if 'a' <= lettre <= 'z' else lettre
        c_dep = None
        for c in self.cases :
            if c.is_vide() :
                continue
            if c.get_jeton_lettre() == cherche :
                c_dep = c
                break
            if c.get_jeton_lettre() == "?" : # joker au coup où
                c_dep = c
        return c_dep

## Principales fonctions publiques 
    def move_from(self, c_dest, status, lettre) :
        """ Déplace un jeton du tirage vers la case c_dest

        La fonction renvoie true si le transfert s'est fait, false sinon
        Si on trouve un jeton portant la lettre, le jeton est déplacé
        et il prend le status indiqué
        """
        # si destination non vide, pas de transfert
        if not c_dest.is_vide() :
            return False
        # on cherche si un jeton a la lettre (ou un joker éventuellement)
        c_dep = self.cherche_case_lettre(lettre)
        # si on a un jeton dans le tirage :
        # le transfert est possible
        if c_dep is not None :
            j = c_dep.prend()
            j.set_status(status)
            if j.get_lettre() == "?" : #cas du joker
                j.set_lettre(lettre.lower())
            c_dest.pose(j)
            return True
        else :
            return False

    def move_to(self, c_dep) :
        """ Remet le jeton j de la case c_dep 
        dans la première case libre trouvée
        """
        # la case de départ est vide, on sort
        if c_dep.is_vide() :
            return False
        for c in self.cases :
            if c.is_vide() :
                j = c_dep.prend()
                # on remet le ? sur le joker
                if j.is_joker() :
                    j.set_lettre('?')
                j.set_status(jeton.TIRAGE)
                c.pose(j)
                return True
        return False

## Fonctions de manipulation : tri, shuffle
    def alpha(self) :
        """ Trie les jetons par ordre alphabétique
        """
        self.permute('A')

    def shuffle(self) :
        """ Trie les jetons par ordre aléatoire
        """
        self.permute('R')

    def permute(self, code = 'R') :
        """ Fonction interne pour alpha et shuffle
        """
        temp = []
        # vide les cases et
        # met les jetons dans temp
        for c in self.cases :
            j = c.prend()
            if j is not None :
                temp.append(j)
        if code == 'A' :
            # tri temp selon la lettre
            temp.sort(key=lambda x: x.get_lettre())
        elif code == 'R' :
            # mélange temp
            random.shuffle(temp)
        # et repose les jetons de temp
        # dans les cases
        for i, j in enumerate(temp) :
            self.cases[i].pose(j)

    def shift(self, pos) :
        """Décale les jetons (clic droit)
        """
        end = -1
        # cherche index première case vide à droite
        for i in xrange(pos+1, self.nb_pos()) :
            if self.cases[i].is_vide() :
                end = i
                break
        # il y a une case vide : on décale en posant et vidant à chaque pas
        if end >= 0 :
            for i in xrange(end, pos, -1) :
                j = self.cases[i-1].prend()
                self.cases[i].pose(j)
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
                    j = self.cases[i+1].prend()
                    self.cases[i].pose(j)
