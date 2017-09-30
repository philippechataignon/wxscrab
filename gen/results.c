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

/* $Id: results.c 10 2004-03-17 10:29:54Z philippe $ */

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "tiles.h"
#include "round.h"
#include "results.h"

struct tresults {
    Round list [RESULTS_INTERNAL_MAX];
    int nresults; /* nb de tops */
    int ntotal;   /* nb de coups possibles */
};

Results
Results_create()
{
    Results r;
    r = (Results)malloc(sizeof(struct tresults));
    memset(r->list,0,sizeof(Round)*RESULTS_INTERNAL_MAX) ;
    Results_init(r);
    return r;
}

void
Results_init(Results r)
{
    Results_init_p(r);
    r->ntotal   = 0 ;
}

void
Results_init_p(Results r)
{
    int i;
    for(i=0; i < RESULTS_INTERNAL_MAX; i++) {
        if (r->list[i]) {
            Round_destroy(r->list[i]);
            r->list[i] = 0;
        }
    }
    r->nresults = 0;
}

void
Results_destroy(Results r)
{
    if (r) {
        Results_init_p(r);
        free(r);
    }
}

void
Results_addsorted(Results re, Round ro)
{
    re->ntotal++ ;
    /* Si liste vide ou points>max , on réinitialise la liste avec ce round */
    if (re->nresults == 0 || Round_points(ro)>Round_points(re->list[0])) {
        Results_init_p(re) ;
        re->list[0]=Round_create() ;
        Round_copy(re->list[0],ro);
        re->nresults = 1 ;
    } else if (Round_points(ro) == Round_points(re->list[0])) {
        /* Sinon points=max et on ajoute un isotop à la liste */
        re->list[re->nresults]=Round_create() ;
        Round_copy(re->list[re->nresults],ro);
        re->nresults++ ;
    }
}

int
Results_in(Results r)
{
    return r->nresults;
}

int
Results_total(Results r)
{
    return r->ntotal;
}

Round
Results_get(Results r, int i)
{
    if (i >= 0 && i < r->nresults) {
        return r->list[i];
    }
    return NULL;
}
