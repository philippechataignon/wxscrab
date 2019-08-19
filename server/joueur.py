#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import msg
import xml.etree.cElementTree as ET
from functools import total_ordering

@total_ordering
class joueur:
    def __init__(self, nick, proto, channel) :
        self.nick = nick
        self.proto = proto
        self.channel = channel
        self.raz()

    def raz(self) :
        self.points_tour = 0
        self.points_tour_affiche = 0
        self.points_total = 0
        self.points_ber = 0.0
        self.nb_top = 0
        self.nb_solo = 0
        self.rang = 0
        self.rang_total = 0
        self.msg_fin_tour = []
        self.tick = True

    def __eq__(self, other):
        return ((self.points_total, self.points_tour) == (other.points_total, other.points_tour))

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return ((self.points_total, self.points_tour) < (other.points_total, other.points_tour))

class joueurs :
    cum_top = 0
    def __init__(self) :
        self.nick2joueur={}
        self.score_top = 0

    def __len__(self) :
        return len(self.nick2joueur)

    def liste_actif(self) :
        # les joueurs actifs sont les joueurs connectés
        # ou ayant fait un score dans le tour
        return [j for j in self.nick2joueur.values() if (j.channel is not None or j.tick)]

    def liste_envoi(self) :
        return [j for j in self.nick2joueur.values() if j.channel is not None]

    def add_joueur(self, nick, proto, channel) :
        if nick in self.nick2joueur :
            j = self.nick2joueur[nick]
            if j.channel is None :
                j.channel = channel
                return 2
            else:
                return 0
        else:
            self.nick2joueur[nick] = joueur(nick, proto, channel)
            return 1

    def deconnect(self, channel) :
        for nick, j in self.nick2joueur.items() :
            if j.channel == channel :
                j.channel = None
                return nick
        return None

    def score_tour_zero(self) :
        for j in self.nick2joueur.values() :
            j.points_tour = 0
            j.points_tour_affiche = 0
            j.msg_fin_tour = []
            j.tick = False

    def score_raz(self) :
        # appelé par debut_game
        for nick, j in list(self.nick2joueur.items()) :
            # supprime les joueurs déconnectés
            if j.channel is None :
                del self.nick2joueur[nick]
            else :
                j.raz()
        joueurs.cum_top = 0

    def set_points_tour(self, nick, score) :
        # appelé suite à proposition
        # score correspond au vrai score (0 si non ex)
        self.nick2joueur[nick].points_tour = score

    def set_msg_fin_tour(self, nick, non_ex) :
        # appelé suite à proposition
        # message éventuel de fin de tour
        # en général mot non existant
        self.nick2joueur[nick].msg_fin_tour = non_ex

    def set_tick(self, nick, channel) :
        self.nick2joueur[nick].tick = True
        if self.nick2joueur[nick].channel is None :
            self.nick2joueur[nick].channel = channel
            print("%s à nouveau actif" % nick)

    def check_tick(self) :
        # appelé en fin de tour
        # kick les joueurs sans tick
        for j in self.nick2joueur.values() :
            if not j.tick :
                j.channel = None
                print("%s inactif" % j.nick)

    def get_infos_joueur(self, nick) :
        if nick in self.nick2joueur :
            j = self.nick2joueur[nick]
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
            # points_tour_affiche contient les scores affiches dans le tableau des scores
            # évite de repérer son score lors de reconnexion
            j.points_tour_affiche = j.points_tour
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
            if j.channel is not None :
                m = msg.msg("info", "Score : %d - Ecart : %d - Rang : %d/%d" %
                    (j.points_tour, j.points_tour-score_top, j.rang, len(l)))
                j.channel.envoi(m)

        # pas d'envoi de stats si un seul joueur
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

        l_msg = []
        if len(liste_top) == 0 :
            if len(liste_best) > 0 :
                txt = "Meilleur score (%d points) : %s" % (liste_best[0].points_tour,
                        self.l_comma(liste_best))
                l_msg.append(txt)
        elif len(liste_top) == 1 :
            liste_top[0].nb_solo += 1
            txt = "%s a fait un solo" % liste_top[0].nick
            l_msg.append(txt)
        elif len(liste_top) > 0 :
            txt = "Top réalisé par : %s " % self.l_comma(liste_top)
            l_msg.append(txt)
        if len(liste_bulle) >= 1 :
            txt = "Bulle pour : %s" % self.l_comma(liste_bulle)
            l_msg.append(txt)
        return "\n".join(l_msg)

    def l_comma(self, liste) :
        return ", ".join(sorted([j.nick for j in liste]))

    def tableau_score(self) :
        tree = ET.Element("score")
        label = ET.SubElement(tree, "label")
        cols = ('Score total', '% total', 'Négatif', 'Top', 'Solo', 'Ber', 'Score tour')
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
                nom.text = str(j.nick)
            else:
                nom.text  = "%d. %s" % (j.rang_total, str(j.nick))
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
            e.text = "%d" % j.points_tour_affiche
        xml = ET.tostring(tree, encoding="unicode")
        return xml
