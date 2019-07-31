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

/* $Id: results.h 10 2004-03-17 10:29:54Z philippe $ */

#ifndef _RESULTS_H_
#define _RESULTS_H_

#if defined(__cplusplus)
extern "C"
{
#endif

#define RESULTS_INTERNAL_MAX 5000

#include "round.h"
  /*************************
   * Results is a container. The structure
   * stores the rounds that have been found
   * during a search on the board
   *************************/

typedef struct tresults* Results;

  /*************************
   * Results general routines
   *************************/

Results Results_create     ();
void    Results_init       (Results);
void    Results_init_p       (Results);
void    Results_destroy    (Results);

int     Results_in         (Results);
int     Results_total      (Results);
Round   Results_get        (Results,int);

void    Results_addsorted  (Results,Round);

#if defined(__cplusplus)
}
#endif
#endif
