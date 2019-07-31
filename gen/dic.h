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

/* $Id: dic.h 16 2004-03-26 20:24:20Z philippe $ */

#ifndef _DIC_H_
#define _DIC_H_

#include "dic_internals.h"


int    Dic_init   (Dictionary, const char*);
int    Dic_destroy(Dictionary);

  /*************************
   * functions to access the elements
   *************************/

char   Dic_chr (Dictionary,uint32_t);
int    Dic_last(Dictionary,uint32_t);
int    Dic_word(Dictionary,uint32_t);

uint32_t Dic_root(Dictionary);
uint32_t Dic_next(Dictionary,uint32_t);
uint32_t Dic_succ(Dictionary,uint32_t);

unsigned int num_noeud_mot_rec(Dictionary dic, const char* mot, int n, unsigned int e);
int num_noeud_mot(Dictionary dic, const char* mot);
int isMot(Dictionary dic, const char* mot);

#endif
