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

/* $Id: tiles.c 10 2004-03-17 10:29:54Z philippe $ */

#include <ctype.h>

#include "tiles.h"


/* The jokers and the 'Y' can be considered both as vowels or consonants */
const int Tiles_vowels[TILES_NUMBER] =
{
/* x A B C D  E F G H I J  K L M N O P Q R S T U V  W  X  Y  Z ? */
   0,1,0,0,0, 1,0,0,0,1,0, 0,0,0,0,1,0,0,0,0,0,1,0, 0, 0, 0, 0,0
};

const int Tiles_consonants[TILES_NUMBER] =
{
/* x A B C D  E F G H I J  K L M N O P Q R S T U V  W  X  Y  Z ? */
   0,0,1,1,1, 0,1,1,1,0,1, 1,1,1,1,0,1,1,1,1,1,0,1, 1, 1, 0, 1,0
};

const int Tiles_numbers[TILES_NUMBER] =
{
/* x A B C D  E F G H I J  K L M N O P Q R S T U V  W  X  Y  Z ? */
   0,9,2,2,3,15,2,2,2,8,1, 1,5,3,6,6,2,1,6,6,6,6,2, 1, 1, 1, 1,2
};

const int Tiles_points[TILES_NUMBER] =
{
/* x A B C D  E F G H I J  K L M N O P Q R S T U V  W  X  Y  Z ? */
   0,1,3,3,2, 1,4,2,4,1,8,10,1,2,1,1,3,8,1,1,1,1,4,10,10,10,10,0
};

//const int Tiles_pc[TILES_NUMBER] =
//    {
////     a   b   c   d   e   f   g   h   i  j  k
//    0,35, 15, 37, 16, 53, 18, 11, 17, 34, 5, 3,
////   l   m   n   o   p   q   r   s   t   u   v
//    14, 18, 26, 21, 25, 15, 17, 36, 24, 13, 13,
////  w  x  y   z   ?
//    1, 9, 14, 15, 100000
//    };

const int Tiles_pc[TILES_NUMBER] =
    {
//     a   b   c   d   e   f   g   h   i  j  k
    0,30, 10, 30, 10, 50, 30, 10, 20, 30, 5, 3,
//   l   m   n   o   p   q   r   s   t   u   v
    20, 20, 30, 20, 20, 10, 30, 50, 20, 10, 20,
//  w  x  y   z   ?
    1, 10, 10, 10, 100000
    };

tile_t
chartocode(char c)
{
    if (c == '?') {
        return (tile_t)JOKER_TILE;
    }
    if (isalpha(c)) {
        return (tile_t)(toupper(c) - 'A' + 1);
    }
    return 0;
}

char
codetochar(tile_t t)
{
    if (t == (tile_t)JOKER_TILE) {
        return '?';
    }
    return (char)t - 1 + 'A';
}
