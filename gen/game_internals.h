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

/* $Id: game_internals.h 13 2004-03-17 15:57:42Z philippe $ */

#ifndef _GAMESTRUCT_H
#define _GAMESTRUCT_H

#if defined(__cplusplus)
extern "C"
{
#endif

#define PLAYEDRACK_MAX 50
#include "dic.h"
#include "tiles.h"
#include "bag.h"
#include "rack.h"
#include "round.h"
#include "pldrack.h"
#include "results.h"
#include "board.h"
#include "game.h"
#include "board_internals.h"

struct tgame {
   Dictionary dic;

   Bag      bag;
   Board    board;
   Results    searchresults;

   Playedrack playedracks [PLAYEDRACK_MAX];
   Round    playedrounds[PLAYEDRACK_MAX];

   int nrounds;
   int points;
};

#if defined(__cplusplus)
}
#endif
#endif
