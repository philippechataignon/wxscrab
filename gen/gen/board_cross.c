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

/* $Id: board_cross.c 13 2004-03-17 15:57:42Z philippe $ */

#include <stdio.h>
#include "dic.h"
#include "tiles.h"
#include "bag.h"
#include "rack.h"
#include "round.h"
#include "results.h"
#include "board.h"
#include "board_internals.h"

/*
 * crosschecks
 * bitmap over an int, tiles are in reversed order
 * { 0-0 z y x w v u t s r q p o n m l k j i h g f e d c b a 0 }
 * CROSS_MASK is thus set to 0x7FFFFFE when we want to allow
 * every possible letter
 */


static unsigned int
Board_lookup(Dictionary d, unsigned int t, tile_t* s)
{
    unsigned int p;
begin:
    if (!*s) {
        return t;
    }
    if (!(p=Dic_succ(d,t))) {
        return 0;
    }
    while(1) {
        if (Dic_chr(d,p) == *s) {
            t = p;
            s++;
            goto begin;
        } else if (Dic_last(d,p)) {
            return 0;
        }
        p = Dic_next(d,p);
    }
    return 0;
}

static unsigned int
Board_checkout_tile(Dictionary d, tile_t* tiles, char* joker, int *points)
{
    unsigned int node,succ;
    unsigned int mask;
    tile_t* t = tiles; //pointeur de travail sur tiles
    char* j = joker;   //

    mask = 0;
    *points = 0;

    /* points on the left part */
    while (t[-1]) {
        j--;
        t--;
        if (!(*j)) {
            (*points) += Tiles_points[*t];
        }
    }

    /* tiles that can be played */
    node = Board_lookup(d,Dic_root(d),t);
    if (!node) {
        return 0;
    }

    for(succ = Dic_succ(d,node) ; succ ; succ = Dic_next(d,succ)) {
        if (Dic_word(d,Board_lookup(d,succ,tiles + 1))) {
            mask |= (1 << Dic_chr(d,succ));
        }
        if (Dic_last(d,succ)) {
            break;
        }
    }

    /* points on the right part */
    while (tiles[1]) {
        joker++;
        tiles++;
        if (!(*joker)) {
            (*points) += Tiles_points[*tiles];
        }
    }

    return mask;
}

static void
Board_check(Dictionary d,
            tile_t        tiles[BOARD_REALDIM][BOARD_REALDIM],
            char          joker[BOARD_REALDIM][BOARD_REALDIM],
            unsigned int  cross[BOARD_REALDIM][BOARD_REALDIM],
            int           point[BOARD_REALDIM][BOARD_REALDIM])
{
    int i,j;

    // on parcoure toutes les cases
    for(i = 1; i <= BOARD_DIM; i++) {
        for(j = 1; j <= BOARD_DIM; j++) {
            // on initialise point à -1
            point[j][i] = -1;
            // si la case est remplie, on ne peut poser aucune lettre (cross=0)
            if (tiles[i][j]) {
                cross[j][i] = 0;
            // sinon, si il y a une lettre au-dessus ou au-dessous, on teste
            } else if (tiles[i][j - 1] || tiles[i][j + 1]) {
                cross[j][i] = Board_checkout_tile(d, tiles[i] + j, joker[i] + j, point[j] + i);
            // sinon, toutes lettres sont OK (cross par défaut)
            } else {
                cross[j][i] = CROSS_MASK;
            }
        }
    }
}

void
Board_buildcross(Dictionary d, Board b)
{
  Board_check(d,b->tiles_r,b->joker_r,b->cross_c,b->point_c);
  Board_check(d,b->tiles_c,b->joker_c,b->cross_r,b->point_r);
}

/** Fonctions ajoutées / eliot 1.4 */

static unsigned int
Board_checkout_tile_eval(Dictionary d, tile_t* tiles)
{
    unsigned int node,succ;
    unsigned int mask;
    tile_t* t = tiles;

    mask = 0;
    while (t[-1]) {
        t--;
    }
    node = Board_lookup(d,Dic_root(d),t);
    if (!node)
        return 0;

    for( succ = Dic_succ(d,node) ; succ ; succ = Dic_next(d,succ)) {
        if (Dic_word(d,Board_lookup(d,succ,tiles + 1))) {
            mask |= (1 << Dic_chr(d,succ));
        }
        if (Dic_last(d,succ))
            break;
    }
    return mask;
}

static int
Board_check_eval(Dictionary d,
             tile_t tiles[BOARD_REALDIM][BOARD_REALDIM],
             Bag g
             )
{
    int i,j,l;
    unsigned int mask;
    int cumul ;

    cumul = 0 ;

    for(i = 1; i <= BOARD_DIM; i++) {
        for(j = 1; j <= BOARD_DIM; j++) {
            if (!tiles[i][j] &&
                (tiles[i][j-1] || tiles[i][j+1] || tiles[i-1][j] || tiles[i+1][j]) ) {
                mask = Board_checkout_tile_eval(d, tiles[i] + j) ;
                for (l=1 ; l<=26 ; l++) {
                    if ( mask & (1<<l) ) {
                        cumul += 1
                            /**(Bag_in(g,l)>0)*/
                            *Tiles_points[l]
                            /**(1+(Tiles_points[l]>1)+2*(Tiles_points[l]>=8))*/
                            *(Board_tile_multipliers[i][j]+2*Board_word_multipliers[i][j]) ;
                        /* Pond = 1 2 3 3 5 (N l2 l3 w2 w3) */
                                /*printf("Case %d %d %d %d- Lettre %c : %d = %d\n",i,j,
                                Board_tile_multipliers[i][j],Board_word_multipliers[i][j],
                                l+64,Bag_in(g,l),cumul) ;                           */
                    }
                }
            }
        }
    }
    return cumul ;
}

int
Board_calc_cross(Dictionary d, Board b, Bag g)
{
    return Board_check_eval(d,b->tiles_r,g)+Board_check_eval(d,b->tiles_c,g);
}

int
Board_calc_scrab_tiles(tile_t tiles[BOARD_REALDIM][BOARD_REALDIM])
{
    // compte le nombre de cases où il y a la place pour poser un scrabble
    int i,j ;
    int k,s ;
    int scrab = 0;

    for(i = 1; i <= BOARD_DIM; i++) {
        for(j = 1; j <= BOARD_DIM; j++) {
            /* si case vide et case adjacente occupée = anchor */
            if (!tiles[i][j] &&
                (tiles[i][j-1] || tiles[i][j+1] || tiles[i-1][j] || tiles[i+1][j]) ) {
                k = j ;
                s = 0;
                while (k>=1 && !tiles[i][--k]) {
                    s++ ;
                }
                k = j ;
                while (k<=BOARD_DIM && !tiles[i][++k]) {
                    s++ ;
                }
                if (s>=7) {
                    scrab++ ;
                }
            }
        }
    }
    return scrab ;
}

int
Board_calc_scrab(Board b)
{
// printf("nb scrab R : %d\n",Board_calc_scrab_tiles(b->tiles_r)) ;
// printf("nb scrab C : %d\n",Board_calc_scrab_tiles(b->tiles_c)) ;
    return Board_calc_scrab_tiles(b->tiles_r) + Board_calc_scrab_tiles(b->tiles_c) ;
}
