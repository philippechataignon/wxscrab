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
 * $Id: dic_internals.h 9 2004-03-17 09:47:34Z philippe $
 */
#ifndef _DIC_INTERNALS_H
#define _DIC_INTERNALS_H

#include <stdint.h>
/*

   structure of a compressed dictionary

   ----------------
   header
   ----------------
   specialnode (0)
   +
   + nodes
   +
   firstnode (= root)
   ----------------

*/

#define CHAR    0x1F

#define _COMPIL_KEYWORD_ "__DIC__"

typedef struct Dawg_edge {
    uint32_t ptr  : 24;
    uint32_t term : 1;
    uint32_t last : 1;
    uint32_t fill : 1;
    uint32_t chr  : 5;
} Dawg_edge;

typedef struct Dict_header {
    char ident[8];
    int32_t root;
    int32_t nwords;
    uint32_t edgesused;
    uint32_t nodesused;
    uint32_t nodessaved;
    uint32_t edgessaved;
} Dict_header;

typedef struct Dico {
    Dawg_edge *dawg;
    uint32_t root;
    int32_t nwords;
    int32_t nnodes;
    int32_t nedges;
} Dico;

typedef Dico* Dictionary;

#endif
