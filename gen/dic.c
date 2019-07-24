/* Eliot                                                       */
/* Copyright (C) 1999  antoine.fraboulet                             */
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
/*
 * $Id: dic.c 9 2004-03-17 09:47:34Z philippe $
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <ctype.h>
#include "dic_internals.h"
#include "dic.h"

static int
check_header(FILE* file, Dict_header *header)
{
    if (fread(header,sizeof(Dict_header),1,file) != 1)
        return 1;
    return strcmp(header->ident,_COMPIL_KEYWORD_);
}

int
Dic_init(Dictionary dic, const char* path)
{
    FILE* file;
    Dict_header header;

    if ((file = fopen(path,"rb")) == NULL)
        return 1;
    if (check_header(file,&header))
        return 2;
    if ((dic->dawg = (Dawg_edge*)malloc((header.edgesused + 1)*
                    sizeof(Dawg_edge))) == NULL) {
        return 4;
    }
    if (fread(dic->dawg,sizeof(Dawg_edge),header.edgesused + 1,file) !=
            (header.edgesused + 1)) {
        free(dic->dawg);
        return 5;
    }
    dic->root = header.root;
    dic->nwords = header.nwords;
    dic->nnodes = header.nodesused;
    dic->nedges = header.edgesused;

    fclose(file);
    return 0;
}

int
Dic_destroy(Dictionary dic)
{
    free(dic->dawg);
    return 0;
}

char
Dic_chr(Dictionary d, uint32_t e)
{
    return (d->dawg[e]).chr;
}

int
Dic_last(Dictionary d, uint32_t e)
{
    return (d->dawg[e]).last;
}

int
Dic_word(Dictionary d, uint32_t e)
{
    return (d->dawg[e]).term;
}

uint32_t
Dic_next(Dictionary d, uint32_t e)
{
    if (! Dic_last(d,e))
        return e+1;
    return 0;
}

uint32_t
Dic_succ(Dictionary d, uint32_t e)
{
    return (d->dawg[e]).ptr;
}

uint32_t
Dic_root(Dictionary d)
{
    return d->root;
}

unsigned int
num_noeud_mot_rec(Dictionary dic, const char* mot, int n, unsigned int e)
{
    unsigned int p;

    if (mot[n]) {
        char c = (mot[n] & 0x1f) ;
        for(p = Dic_succ(dic,e); p && Dic_chr(dic,p)<=c ; p = Dic_next(dic,p)) {
            if ( c == Dic_chr(dic,p) ) {
                return num_noeud_mot_rec(dic, mot, n+1, p) ;
            }
        }
        return 0 ;
    } else {
        return e ;
    }
}

int
num_noeud_mot(Dictionary dic, const char* mot) {
    return num_noeud_mot_rec(dic,mot,0,Dic_root(dic)) ;
}

int
isMot(Dictionary dic, const char* mot) {
    return Dic_word(dic,num_noeud_mot(dic,mot)) ;
}
