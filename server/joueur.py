#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
sys.path.append('../common')

import msg
import xml.etree.cElementTree as ET

class joueur :
    def __init__(self, nick, proto, channel) :
        self.nick = nick
        self.proto = proto
        self.channel = channel
        self.connect = True
        self.raz()

    def raz(self) :
        self.points_tour = 0
        self.points_tour_def = 0
        self.points_total = 0
        self.points_ber = 0.0
        self.nb_top = 0
        self.nb_solo = 0
        self.rang = 0
        self.rang_total = 0
        self.msg_fin_tour = []

class joueurs :
    cum_top = 0
    def __init__(self) :
        self.liste={}
        self.score_top = 0

    def __len__(self) :
        return len(self.liste_actif())

    def liste_actif(self) :
        return [j for j in self.liste.itervalues() if j.connect]

    def envoi_all(self, mm) :
        for j in self.liste_actif() :
            j.channel.envoi(mm)

    def add_joueur(self, nick, proto, channel) :
        if nick in self.liste :
            j = self.liste[nick] 
            if j.connect == False :
                j.channel = channel
                j.connect = True
                return 2
            else:
                return 0
        else:
            self.liste[nick] = joueur(nick, proto, channel)
            return 1

    def deconnect(self, channel) :
        for nick, j in self.liste.iteritems() :
            if j.channel == channel :
                j.connect = False
                j.channel = None
                return nick
        return None

    def score_tour_zero(self) :
        for j in self.liste.itervalues() :
            j.points_tour = 0
            j.points_tour_def = 0
            j.msg_fin_tour = []

    def score_raz(self) :
        l = self.liste.items()
        for nick,j in l :
            if j.connect == False :
                del self.liste[nick]
            else :
                j.raz()
        joueurs.cum_top = 0

    def set_points_tour(self, nick, score) :
        self.liste[nick].points_tour = score

    def set_msg_fin_tour(self, nick, non_ex) :
        self.liste[nick].msg_fin_tour = non_ex

    def get_infos_joueur(self, nick) :
        if nick in self.liste :
            j = self.liste[nick]
            if joueurs.cum_top == 0 :
                pct = 0
            else :
                pct = float(j.points_total)/joueurs.cum_top*100
            return j.proto, j.points_total, joueurs.cum_top, pct, j.msg_fin_tour

    def score_fin_tour(self, score_top) :
        self.score_top = score_top
        joueurs.cum_top += score_top
        l = self.liste_actif()
        l.sort(key=lambda j: j.points_tour, reverse=True)
        rg = 1
        last_points = -1
        last_rang  = 0
        l_ber = []
        for j in l :
            # tour_def contient les scores affiches dans le tableau des scores
            # évite de repérer son score lors de reconnexion
            j.points_tour_def = j.points_tour
            if j.points_tour != last_points :
                j.rang = rg
                for jb in l_ber :
                    jb.points_ber += float(sum_ber)/len(l_ber)
                l_ber = [j]
                sum_ber = len(l) - rg
            else :
                j.rang = last_rang
                l_ber.append(j)
                sum_ber += (len(l) - rg)
            last_points, last_rang = j.points_tour, j.rang 
            rg += 1
        for jb in l_ber :
            jb.points_ber += float(sum_ber)/len(l_ber)

        liste_top = []
        for j in l :
            j.points_total += j.points_tour
            if j.points_tour == score_top :
                j.nb_top += 1
                liste_top.append(j)
            if j.connect :
                m = msg.msg("info", \
                        "Score : %d (%d) - Rang : %d/%d" \
                        % (j.points_tour, j.points_tour-score_top, j.rang, len(l)), "")
                j.channel.envoi(m)

        if len(l) <= 1 :
            return ""

        txt = ""

        liste_bulle = [j for j in l if j.points_tour == 0]
        liste_best =  [j for j in l if j.rang == 1 and j.points_tour > 0]

        l.sort(key=lambda j: j.points_total, reverse=True)
        rg = 1
        last_points = -1
        last_rang  = 0
        for j in l :
            if j.points_total == last_points :
                j.rang_total = last_rang
            else :
                j.rang_total = rg
            last_points, last_rang = j.points_total, j.rang_total 
            rg += 1

        if len(liste_top) == 0 :
            if len(liste_best) > 0 :
                txt += "Meilleur score (%d points) : " % liste_best[0].points_tour
                for j in liste_best :
                    txt += "%s, " % j.nick
                txt = txt[:-2]+"\n"
        elif len(liste_top) == 1 :
            liste_top[0].nb_solo += 1
            txt += "%s a fait un solo\n" % liste_top[0].nick 
        elif len(liste_top) > 0 :
            txt += "Top réalisé par : "
            for j in liste_top :
                txt += "%s, " % j.nick
            txt = txt[:-2]+"\n"

        if len(liste_bulle) >= 1 :
            txt += "Bulle pour : "
            for j in liste_bulle :
                txt += "%s, " % j.nick
            txt = txt[:-2]+"\n"

        return txt

    def tableau_score(self) :
        tree = ET.Element("score")
        label = ET.SubElement(tree, "label")
        cols = ('Score total', '% total', u'Négatif', 'Top', 'Solo', 'Ber', 'Score tour')
        for c in cols :
            col = ET.SubElement(label,"col")
            col.text = c
        l = self.liste_actif()
        l.sort(reverse=True)
        for j in l :
            if joueurs.cum_top == 0 :
                pct = 0
            else :
                pct = float(j.points_total)/joueurs.cum_top*100
            ligne = ET.SubElement(tree, "ligne")
            nom = ET.SubElement(ligne, "nom", type="s")
            if j.rang_total == 0 :
                nom.text = unicode(j.nick)
            else: 
                nom.text  = "%d. %s" % (j.rang_total, unicode(j.nick))
            e = ET.SubElement(ligne, "val", type="i")
            e.text = "%d" % j.points_total
            e = ET.SubElement(ligne, "val", type="f")
            e.text = "%4.1f" % pct
            e = ET.SubElement(ligne, "val", type="i")
            e.text = "%d" % (j.points_total-joueurs.cum_top)
            e = ET.SubElement(ligne, "val", type="i")
            e.text = "%d" % j.nb_top
            e = ET.SubElement(ligne, "val", type="i")
            e.text = "%d" % j.nb_solo
            e = ET.SubElement(ligne, "val", type="f")
            e.text = "%4.1f" % j.points_ber
            e = ET.SubElement(ligne, "val", type="i")
            e.text = "%d" % j.points_tour_def
        xml = ET.tostring(tree)
        return xml
