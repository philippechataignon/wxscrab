/* Eliot                                                       */
/* Copyright (C) 1999  Antoine Fraboulet                             */
/* antoine.fraboulet@free.fr                                       */
/*                                                            */
/* This program is free software; you can redistribute it and/or modify    */
/* it under the terms of the GNU General Public License as published by    */
/* the Free Software Foundation; either version 2 of the License, or       */
/* (at your option) any later version.                               */
/*                                                            */
/* This program is distributed in the hope that it will be useful,        */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of         */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          */
/* GNU General Public License for more details.                        */
/*                                                            */
/* You should have received a copy of the GNU General Public License       */
/* along with this program; if not, write to the Free Software            */
/* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA */

/* $Id: board_search.c 13 2004-03-17 15:57:42Z philippe $  */

#include <stdio.h>
#include <string.h>
#include "dic.h"
#include "tiles.h"
#include "bag.h"
#include "rack.h"
#include "round.h"
#include "results.h"
#include "board.h"
#include "board_internals.h"

/*
 * computes the score of a word, coordinates may be changed to reflect
 * the real direction of the word 
 */
static void
Boardsearch_evalmove(
    Dictionary dic,
    tile_t tiles[BOARD_REALDIM][BOARD_REALDIM],
    int points[BOARD_REALDIM][BOARD_REALDIM],
    char joker[BOARD_REALDIM][BOARD_REALDIM],
    Results results, Round word)
{
    int i,pts,ptscross;
    int l,t,fromrack;
    int len,row,col,wordmul;

    fromrack = 0;
    pts      = 0;
    ptscross = 0;
    wordmul  = 1;

    len = Round_wordlen(word);
    row = Round_row(word);
    col = Round_column(word);

    for (i=0; i < len; i++) {
        //si la case n'est pas vide
        if (tiles[row][col+i]) {
            // et que ce n'est pas un joker
            if (! joker[row][col+i]) {
                // on ajoute les points de la lettre
                pts += Tiles_points[Round_gettile(word,i)];
            }
        // sinon, si la case est vide
        } else {
            // et que ce n'est pas un joker
            if (! Round_joker(word,i)) {
                // on ajoute les points * multilettre eventuel
                l = Tiles_points[Round_gettile(word,i)] *
                    Board_tile_multipliers[row][col+i];
            } else {
                // si joker, 0
                l = 0;
            }
            // on ajoute � pts
            pts += l;
            // on met � jour le wordmul utilis� � la fin du mot
            wordmul *= Board_word_multipliers[row][col+i];

            // points d�ja stock�s du mot constitu� en vertical
            t = points[row][col+i];
            if (t >= 0) {
                // t+l = points du mot complet
                // application du multiplieur de mots
                ptscross += (t + l) * Board_word_multipliers[row][col+i];
            }
            // et un jeton de plus provenant du rack
            fromrack++;
        }
        // lettre suivante
    }
    // on cumule tout �a et on g�re les scrabbles
    pts = ptscross + pts * wordmul + 50 * (fromrack == 7);
    Round_setbonus(word,fromrack == 7);
    Round_setpoints(word,pts);

    // inversion ligne/col si vertical pour r�sults
    if (Round_dir(word) == VERTICAL) {
        Round_setrow(word,col);
        Round_setcolumn(word,row);
    }
    Results_addsorted(results,word);
    // remise ligne/col �tat initial
    if (Round_dir(word) == VERTICAL) {
        Round_setrow(word,row);
        Round_setcolumn(word,col);
    }
}

static void
ExtendRight(Dictionary dic, 
      tile_t tiles[BOARD_REALDIM][BOARD_REALDIM],
      unsigned int  cross[BOARD_REALDIM][BOARD_REALDIM],
      int points[BOARD_REALDIM][BOARD_REALDIM],
      char joker[BOARD_REALDIM][BOARD_REALDIM],
      Rack rack, Round partialword,
      Results results, unsigned int n, int row, int column, int anchor)
{
    // n : numero du noeud dans arbre dawg
    // anchor reste constant dans les appels r�cursifs de ExtendRight
    // column s'incr�mente � chaque appel
    // column=anchor quand l'appel provient de la r�cursivit� de leftpart
    tile_t l;
    unsigned int succ;

    // si case vide
    if (! tiles[row][column]) {
        // si un mot est r�alis� et qu'on a avanc� strictement 
        // min 2 lettres pour un mot 
        if (Dic_word(dic,n) && column > anchor) {
            // on �value
            Boardsearch_evalmove(dic,tiles,points,joker,results,partialword);
        }

        // boucle parcourant l'ensemble des "sous-noeuds" d'un niveau de l'arbre
        for(succ = Dic_succ(dic,n); succ ; succ = Dic_next(dic,succ)) {
            l = Dic_chr(dic,succ);
            // si la lettre est autori�se par le cross_mask de la case
            if (cross[row][column] & (1 << l)) {
                // et si elle est dans le rack
                if (Rack_in(rack,l)) {
                    //on la retire du rack
                    Rack_remove(rack,l);
                    // on l'ajoute � droite du motpartiel
                    Round_addrightfromrack(partialword,l,0);
                    // on fait la r�cursivit� avec succ/col+1
                    ExtendRight(dic,tiles,cross,points,joker,
                            rack,partialword,results,
                            succ,row,column + 1,anchor);
                    // retour � l'�tat initial
                    // on enl�ve l'ajout � droite du motpartiel
                    Round_removerighttorack(partialword,l,0);
                    // et on remet dans le rack
                    Rack_add(rack,l);
                }
                // si il y a un joker dans le rack
                if (Rack_in(rack,(tile_t)JOKER_TILE)) {
                    //on le retire du rack
                    Rack_remove(rack,(tile_t)JOKER_TILE);
                    // on ajoute la lettre correspondante � droite du motpartiel
                    Round_addrightfromrack(partialword,l,1);
                    // on fait la r�cursivit� avec succ/col+1
                    ExtendRight(dic,tiles,cross,points,joker,
                            rack,partialword,results,
                            succ,row,column + 1,anchor);
                    // on enl�ve l'ajout � droite du motpartiel
                    Round_removerighttorack(partialword,l,1);
                    // et on remet le joker dans le rack
                    Rack_add(rack,JOKER_TILE);
                }
            }
        }
    // sinon, si la case est d�j� occup�e
    } else {
        // on r�cup�re la lettre correspondante
        l = tiles[row][column];
        // boucle parcourant l'ensemble des "sous-noeuds" d'un niveau de l'arbre
        for(succ = Dic_succ(dic,n); succ ; succ = Dic_next(dic,succ)) {
            // avec la contrainte d'�galit� 
            if (Dic_chr(dic,succ) == l) {
                // on ajoute la lettre correspondante � droite du motpartiel
                Round_addrightfromboard(partialword,l);
                // on fait la r�cursivit� avec succ/col+1
                ExtendRight(dic,tiles,cross,points,joker,
                        rack,partialword,
                        results,succ,row,column + 1,anchor);
                // on enl�ve l'ajout � droite du motpartiel
                Round_removerighttoboard(partialword,l);
            }
        }
    }
}

static void
LeftPart(Dictionary dic, 
    tile_t tiles[BOARD_REALDIM][BOARD_REALDIM],
    unsigned int cross[BOARD_REALDIM][BOARD_REALDIM],
    int points[BOARD_REALDIM][BOARD_REALDIM],
    char joker[BOARD_REALDIM][BOARD_REALDIM],
    Rack rack, Round partialword,
    Results results, int n, int row, int anchor, int limit)
{
    // la r�cursivit� se fait sur limit qui se decr�mente � chaque appel
    tile_t l;
    int succ;

    // on �tend � droite � partir de anchor
    // c'est ici que se fait la vraie g�n�ration des mots
    // les appels successifs de leftpart sont de plus en plus "� gauche"
    ExtendRight(dic,tiles,cross,points,joker,rack,
        partialword,results,n,row,anchor,anchor);

    // gestion de la r�cursivit� de la fonction
    // tant qu'on n'a pas atteint le bord gauche
    if (limit > 0) {
        // boucle parcourant l'ensemble des "sous-noeuds" d'un niveau de l'arbre
        for(succ = Dic_succ(dic,n); succ ; succ = Dic_next(dic,succ)) {
            l = Dic_chr(dic,succ);
            // si la lettre est dans le rack
            if (Rack_in(rack,l)) {
                //on la retire du rack
                Rack_remove(rack,l);
                // on l'ajoute � droite du motpartiel
                Round_addrightfromrack(partialword,l,0);
                // on d�cr�mente la colonne du mot partiel
                Round_setcolumn(partialword,Round_column(partialword) - 1);
                // on fait la r�cursivit� avec succ/limit-1
                LeftPart(dic,tiles,cross,points,joker,
                    rack,partialword,results,
                    succ,row,anchor,limit - 1);
                // on remet tout en place : colonne mot partiel, mot partiel et rack
                Round_setcolumn(partialword,Round_column(partialword) + 1);
                Round_removerighttorack(partialword,l,0);
                Rack_add(rack,l);
            }
            // si il y a un joker dans le rack
            if (Rack_in(rack,JOKER_TILE)) {
                // m�me principe que pr�c�demment avec dualit� joker/lettre correspondante
                Rack_remove(rack,JOKER_TILE);
                Round_addrightfromrack(partialword,l,1);
                Round_setcolumn(partialword,Round_column(partialword) - 1);
                // on fait la r�cursivit� avec succ/limit-1
                LeftPart(dic,tiles,cross,points,joker,
                    rack,partialword,results,
                    succ,row,anchor,limit - 1);
                Round_setcolumn(partialword,Round_column(partialword) + 1);
                Round_removerighttorack(partialword,l,1);
                Rack_add(rack,JOKER_TILE);
            }
        }
    } 
}

static void
Board_search_aux(Dictionary dic,
       tile_t tiles[BOARD_REALDIM][BOARD_REALDIM],
       unsigned int cross[BOARD_REALDIM][BOARD_REALDIM],
       int points[BOARD_REALDIM][BOARD_REALDIM],
       char joker[BOARD_REALDIM][BOARD_REALDIM],
       Rack rack,Results results, Direction dir)
{
    int row,column,lastanchor;
    int match, l;
    Round partialword;
    
	// mot partiel vide
    partialword = Round_create();
    // on parcoure les lignes (algo ram�ne � dimension 1)
    for(row = 1; row <= BOARD_DIM; row++) {
        //initialisation du mot partiel
        Round_init(partialword);
        Round_setdir(partialword,dir);
        Round_setrow(partialword,row);
        lastanchor = 0;
        // on parcoure les colonnes
        for(column = 1; column <= BOARD_DIM; column++) {
            // si la case est vide et une case adjacente est occup�e = anchor
            if (! tiles[row][column] &&
                (tiles[row][column - 1] || tiles[row][column + 1] ||
                tiles[row - 1][column] || tiles[row + 1][column])) {
                match = 0;
                // optimisation : ne fait pas la recherche
                // si aucune des lettres du tirage est dans le cross mask
                // (sauf s'il y a un joker dans le tirage)
                if (Rack_in(rack, (tile_t)JOKER_TILE) && cross[row][column]) {
                    match = 1 ;
                } else {
                    for (l=1 ; l<TILES_NUMBER ; l++) {
                        if ( Rack_in(rack, l) && (cross[row][column] & (1 << l)) ) {
                            match = 1;
                            break;
                        }
                    }
                }
                if (match) {
                    // si la case pr�c�dente dans la ligne est occup�e,
                    // on �tend � droite (ExtendRight) � partir de lastanchor+1
                    // et anchor=colonne
                    if (tiles[row][column - 1]) {
                        // si case pr�c�dente non vide
                        Round_setcolumn(partialword,lastanchor + 1);
                        ExtendRight(dic,tiles,cross,points,joker,
                            rack,partialword,results,
                            Dic_root(dic),row,lastanchor + 1,column);
                    } else {
                        // case pr�c�dente dans la ligne est vide
                        // on met le motpartiel
                        Round_setcolumn(partialword,column);
                        // on cherche une partie gauche 
                        LeftPart(dic,tiles,cross,points,joker,
                            rack,partialword,results,
                            Dic_root(dic),row,column,column -
                            lastanchor - 1);
                    }
                }
                // stocke derni�re case vide et adjacente occup�e
                lastanchor = column;
            }
        }
    }
	// on d�truit le round
    Round_destroy(partialword);
}

void
Board_search(Dictionary dic,Board board, Rack rack,Results results)
{
    Board_search_aux(dic,board->tiles_r,board->cross_r,
           board->point_r,board->joker_r,
           rack,results,HORIZONTAL);

    Board_search_aux(dic,board->tiles_c,board->cross_c,
           board->point_c,board->joker_c,
           rack,results,VERTICAL);
}

void
Board_search_first(Dictionary dic, Board board, Rack rack, Results results)
{
    Round partialword;
    int row = 8,column = 8;

    partialword = Round_create();
    Round_setrow(partialword,row);
    Round_setcolumn(partialword,column);
    Round_setdir(partialword,HORIZONTAL);

    LeftPart(dic,board->tiles_r,board->cross_r,board->point_r,board->joker_r,
        rack,partialword,results,Dic_root(dic),row,column,
        Rack_ntiles(rack) - 1);

    Round_destroy(partialword);
}
