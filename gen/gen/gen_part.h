/* Eliot                                                                     */

/* Copyright (C) 1999  Antoine Fraboulet                                     */
/* antoine.fraboulet@free.fr                                                 */
/*                                                                           */
/* This program is free software; you can redistribute it and/or modify      */
/* it under the terms of the GNU General Public License as published by      */
/* the Free Software Foundation; either version 2 of the License, or         */
/* (at your option) any later version.                                       */
/*                                                                           */
/* This program is distributed in the hope that it will be useful,           */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of            */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             */
/* GNU General Public License for more details.                              */
/*                                                                           */
/* You should have received a copy of the GNU General Public License         */
/* along with this program; if not, write to the Free Software               */
/* Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA */

/* $Id: gen_part.c 10 2004-03-17 10:29:54Z philippe $                 */
#ifndef _GEN_PART_H_
#define _GEN_PART_H_

#if defined(__cplusplus)
extern "C"
{
#endif

#define WORDSIZE_MAX 16
#define SEARCHRESULTLINE_MAX 50
#define SCORE_INTERNAL_MAX 5000

typedef struct {
    int pts ;
    int nb ;
    int retir ;
} score_best ;

typedef struct {
    score_best best ;
    int cross ;
    int scrab ;
    int pc ;
    int joker ;
} score ;

int cmp_score(score score_a, score score_b) ;
int cmp_score_best(score_best score_a, score_best score_b) ;
int print_line(Game game, int num, int nbisotop, int change_tirage, int notiret, int nbsol) ;
score traite(Game game, int num, unsigned short int state[3]) ;
int traite_cross(Game game, int num) ;
int traite_scrab(Game game, int num) ;
int traite_pc   (Game game, int num) ;
int traite_joker   (Game game, int num) ;
score_best traite_best (Game game, int num, unsigned short int state[3]) ;
int fin_partie  (Game game, int noprint, int nbscrab, int maxisotop) ;
int main_loop   (Game game,int noprint, int notiret, int nbessai, unsigned short int state[3]) ;
void help() ;
int main(int argc, char *argv[]) ;

#if defined(__cplusplus)
}
#endif
#endif

