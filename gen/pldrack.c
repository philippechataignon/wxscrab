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

/* $Id: pldrack.c 10 2004-03-17 10:29:54Z philippe $ */

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "tiles.h"
#include "rack.h"
#include "pldrack.h"

#define PLDRCK_INTERNAL_MAX 20

struct tplayedrack {
  tile_t oldtiles[PLDRCK_INTERNAL_MAX];
  tile_t newtiles[PLDRCK_INTERNAL_MAX];
  int nnew;
  int nold;
};


Playedrack
Playedrack_create(void)
{
    Playedrack p;
    p = (Playedrack)malloc(sizeof(struct tplayedrack));
    if (p) {
        Playedrack_init(p);
    }
    return p;
}

void 
Playedrack_init(Playedrack p)
{
    p->oldtiles[0] = '\0';
    p->newtiles[0] = '\0';
    p->nnew = 0;
    p->nold = 0;
}

void 
Playedrack_destroy(Playedrack p)
{
    if (p) {
        free(p);
    }
}

void
Playedrack_copy(Playedrack dest, Playedrack source)
{
    int i;
    for (i=0; i < source->nold; i++) {
        dest->oldtiles[i] = source->oldtiles[i];
    }
    dest->nold = source->nold;
    for (i=0; i < source->nnew; i++) {
        dest->newtiles[i] = source->newtiles[i];
    }
    dest->nnew = source->nnew;
}

int
Playedrack_nnew(Playedrack p)
{
    return p->nnew;
}

int
Playedrack_nold(Playedrack p)
{
    return p->nold;
}

int  
Playedrack_ntiles(Playedrack p)
{
    return Playedrack_nold(p) + Playedrack_nnew(p);
}

int  
Playedrack_empty(Playedrack p)
{
    return Playedrack_ntiles(p) == 0;
}

void
Playedrack_addold(Playedrack p, tile_t l)
{
    if (p->nold < PLDRCK_INTERNAL_MAX) {
        p->oldtiles[p->nold++] = l;
    }
}

void
Playedrack_addnew(Playedrack p, tile_t l)
{
    if (p->nnew < PLDRCK_INTERNAL_MAX) {
        p->newtiles[p->nnew++] = l;
    }
}

void
Playedrack_resetnew(Playedrack p)
{
    p->nnew = 0;
}

tile_t
Playedrack_oldtiles(Playedrack p, int i) {
    if ( 0<=i && i<p->nold) {
        return p->oldtiles[i] ;
    } else {
        return 0;
    }
}
 
tile_t
Playedrack_newtiles(Playedrack p, int i) {
    if ( 0<=i && i<p->nnew) {
        return p->newtiles[i] ;
    } else {
        return 0;
    }
}
 
void
Playedrack_getold(Playedrack p, Rack r)
{
    int i;
    Rack_init(r);
    for(i=0; i < p->nold; i++) {
        Rack_add(r,p->oldtiles[i]);
    }
}

void
Playedrack_getnew(Playedrack p, Rack r)
{
    int i;
    Rack_init(r);
    for(i=0; i < p->nnew; i++) {
        Rack_add(r,p->newtiles[i]);
    }
}


void 
Playedrack_getrack(Playedrack p, Rack r)
{
    int i;
    Rack_init(r);
    for(i=0; i < p->nold; i++)
        Rack_add(r,p->oldtiles[i]);
    for(i=0; i < p->nnew; i++)
        Rack_add(r,p->newtiles[i]);
}


void
Playedrack_setold(Playedrack p, Rack r)
{
    int n;
    tile_t i;
    p->nold = 0;
    for(i=0; i<TILES_NUMBER; i++) {
        for(n=0; n < Rack_in(r,i); n++) {
            Playedrack_addold(p,i);
        }
    }
}

void
Playedrack_setnew(Playedrack p, Rack r)
{
    int n;
    tile_t i;
    p->nnew = 0;
    for(i=0; i<TILES_NUMBER; i++) {
        for(n=0; n < Rack_in(r,i); n++) {
            Playedrack_addnew(p,i);
        }
    }
}

int
Playedrack_check_rack(Playedrack p, int min)
{
    tile_t i;
    int v = 0;
    int c = 0;
    int j = 0;

    for(i=0; i < p->nold; i++) {
        v += Tiles_vowels[p->oldtiles[i]];
        c += Tiles_consonants[p->oldtiles[i]];
        j += ( p->oldtiles[i] == JOKER_TILE );
    }
    for(i=0; i < p->nnew; i++) {
        v += Tiles_vowels[p->newtiles[i]];
        c += Tiles_consonants[p->newtiles[i]];
        j += ( p->newtiles[i] == JOKER_TILE );
    }
    if (min > 0) {
        return (v >= min) && (c >= min);
    } else {
        return (j >= 1) ;
    }
}
