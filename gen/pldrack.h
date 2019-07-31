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

/* $Id: pldrack.h 10 2004-03-17 10:29:54Z philippe $ */

#ifndef _PLAYEDRACK_H_
#define _PLAYEDRACK_H_

#if defined(__cplusplus)
extern "C"
{
#endif
#include "rack.h"
typedef struct tplayedrack* Playedrack;

  /*************************
   * general routines
   *************************/

Playedrack Playedrack_create    (void);
void     Playedrack_init       (Playedrack);
void     Playedrack_destroy    (Playedrack);
void     Playedrack_copy       (Playedrack dst, Playedrack src);

void     Playedrack_resetnew    (Playedrack);

void     Playedrack_getold     (Playedrack,Rack);
void     Playedrack_getnew     (Playedrack,Rack);
void     Playedrack_getrack    (Playedrack,Rack);

void     Playedrack_setold     (Playedrack,Rack);
void     Playedrack_setnew     (Playedrack,Rack);

int      Playedrack_empty      (Playedrack);
int      Playedrack_ntiles     (Playedrack);
int      Playedrack_nnew       (Playedrack);
int      Playedrack_nold       (Playedrack);

void     Playedrack_addnew     (Playedrack,tile_t);
void     Playedrack_addold     (Playedrack,tile_t);
tile_t   Playedrack_oldtiles   (Playedrack p, int i);
tile_t   Playedrack_newtiles   (Playedrack p, int i);

int      Playedrack_check_rack  (Playedrack,int);

#if defined(__cplusplus)
}
#endif
#endif
