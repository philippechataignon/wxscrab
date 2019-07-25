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

/* $Id: game.c 13 2004-03-17 15:57:42Z philippe $ */

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

#include "dic.h"
#include "tiles.h"
#include "bag.h"
#include "rack.h"
#include "round.h"
#include "pldrack.h"
#include "results.h"
#include "board.h"
#include "game.h"
#include "game_internals.h"
#include "board_internals.h"

Game
Game_create(Dictionary dic)
{
    int i;
    Game g;

    g = (Game)malloc(sizeof(struct tgame));
    if (g == NULL) {
        return NULL;
    }

    g->dic         = dic;
    g->bag         = Bag_create();
    g->board       = Board_create();
    g->searchresults = Results_create();

    for(i=0; i<PLAYEDRACK_MAX; i++) {
        g->playedrounds[i] = Round_create();
        g->playedracks[i]  = Playedrack_create();
    }
    Game_init(g);
    return g;
}

void
Game_destroy(Game g)
{
    int i;
    if (g) {
        Bag_destroy(g->bag);
        Board_destroy(g->board);
        Results_destroy(g->searchresults);
        for (i=0; i < PLAYEDRACK_MAX; i++) {
            Round_destroy(g->playedrounds[i]);
            Playedrack_destroy(g->playedracks[i]);
        }
        free(g);
    }
}

void
Game_init(Game g)
{
    int i;
    Bag_init(g->bag);
    Board_init(g->board);
    Results_init(g->searchresults);
    for(i=0; i<PLAYEDRACK_MAX; i++) {
        Round_init(g->playedrounds[i]);
        Playedrack_init(g->playedracks[i]);
    }
    g->points  = 0;
    g->nrounds = 0;
}

void
Game_copy(Game dest, Game src)
{
    int i;
    Bag_copy(dest->bag,src->bag);
    Board_copy(dest->board,src->board);
    Results_init(dest->searchresults);
    for(i=0; i<PLAYEDRACK_MAX; i++) {
        Round_copy(dest->playedrounds[i],src->playedrounds[i]);
        Playedrack_copy(dest->playedracks[i],src->playedracks[i]);
    }
    dest->points  = src->points ;
    dest->nrounds = src->nrounds ;
}

void
Game_copy_n(Game dest, Game src)
{
    Bag_copy(dest->bag,src->bag);
    Board_copy(dest->board,src->board);
    Results_init(dest->searchresults);
    Round_copy(dest->playedrounds[src->nrounds],src->playedrounds[src->nrounds]);
    Playedrack_copy(dest->playedracks[src->nrounds],src->playedracks[src->nrounds]);
    dest->points  = src->points ;
    dest->nrounds = src->nrounds ;
}

Dictionary
Game_getdic(Game g)
{
    return g->dic;
}

void
Game_setdic(Game g, Dictionary d)
{
    g->dic = d;
}

int
Game_search(Game game)
{
    Rack rack;
    if (game->dic == NULL) {
        return 1;
    }
    Game_removetestplay(game);
    Results_init(game->searchresults);
    rack = Rack_create();
    Playedrack_getrack(game->playedracks[game->nrounds],rack);
    // si on n'est pas au premier coup
    if (game->nrounds) {
        Board_search(game->dic,game->board, rack, game->searchresults);
    } else {
        Board_search_first(game->dic,game->board, rack, game->searchresults);
    }
    Rack_destroy(rack);
    return 0;
}

/*
   This function returns a rack "dest" with the unplayed tiles from
   the current round.
   03 sept 2000 : We have to sort the tiles according to the new rules
*/
static void
Game_restfromround(Playedrack dest, Playedrack source, Round round)
{
    tile_t i;
    Rack r;

    r = Rack_create();
    Playedrack_getrack(source,r);

    /* we remove the played tiles from rack r */
    for (i=0; i < Round_wordlen(round); i++) {
        if (Round_playedfromrack(round,i)) {
            if (Round_joker(round,i)) {
                Rack_remove(r,(tile_t)JOKER_TILE);
            } else {
                Rack_remove(r,Round_gettile(round,i));
            }
        }
    }
    Playedrack_init(dest);
    Playedrack_setold(dest,r);
    Rack_destroy(r);
}

int
Game_play(Game game, int n)
{
    return Game_play_round(game,Results_get(game->searchresults,n)) ;
}

int
Game_play_round(Game game, Round round)
{
    /*
     * We remove tiles from the bag only when they are played
     * on the board. When going back in the game, we must only
     * replace played tiles.
     * We test a rack when it is set but tiles are left in
     * the bag.
     */
    int i;

    if (game->dic == NULL) {
        return 1;
    }

    if (round == NULL) {
        return 2;
    }

    Round_copy(game->playedrounds[game->nrounds],round);
    Board_addround(game->dic,game->board,round);
    game->points += Round_points(round);
    Game_restfromround(game->playedracks[game->nrounds + 1],
            game->playedracks[game->nrounds],
            round);
    for (i=0; i < Round_wordlen(round); i++) {
        if (Round_playedfromrack(round,i)) {
            if (Round_joker(round,i)) {
                Bag_taketile(game->bag,(tile_t)JOKER_TILE);
            } else {
                Bag_taketile(game->bag,Round_gettile(round,i));
            }
        }
    }
    game->nrounds++;
    Results_init(game->searchresults);
    return 0;
}

int
Game_back(Game game, int n)
{
    int i,j;
    Round lastround;

    if (game->dic == NULL) {
        return 1;
    }

    for(i=0 ; i < n; i++) {
        if (game->nrounds) {
            game->nrounds--;
            lastround = game->playedrounds[game->nrounds];
            game->points -= Round_points(lastround);
            Board_removeround(game->dic,game->board,lastround);
            for(j=0; j < Round_wordlen(lastround); j++) {
                if (Round_playedfromrack(lastround,j)) {
                    if (Round_joker(lastround,j))
                        Bag_replacetile(game->bag,JOKER_TILE);
                    else
                        Bag_replacetile(game->bag,Round_gettile(lastround,j));
                }
            }
            Round_init(lastround);
        }
    }
    return 0;
}

int
Game_testplay(Game game, int n)
{
    Round round;

    if ((round = Results_get(game->searchresults,n))==NULL)
        return 2;
    Board_testround(game->board,round);
    return 0;
}

int
Game_removetestplay(Game game)
{
    Board_removetestround(game->board);
    return 0;
}

int
Game_getpoints(Game g)
{
    return g->points;
}

int
Game_getcalc_cross(Game g)
{
    return Board_calc_cross(g->dic, g->board, g->bag);
}

int
Game_getcalc_scrab(Game g)
{
    return Board_calc_scrab(g->board);
}


int
Game_setrack_random(Game game, unsigned short int etat[3], int force_vide)
{
    // retour :
    // -1 si pb définitif lié au sac
    // 0 si OK
    // 1 si OK après retirage

    Playedrack p = game->playedracks[game->nrounds] ;
    int retour = 0 ;
    int res ;
    if (force_vide)
        res = Game_setrack_random_aux(game, p, RACK_ALL, etat) ;
    else
        res = Game_setrack_random_aux(game, p, RACK_NEW, etat) ;
    if (res == 1) {
        retour = 1 ;
        while ((res = Game_setrack_random_aux(game,p,RACK_ALL,etat)) != 0) ;
    } else if (res >= 2) {
        retour = -1 ;
    }
    return retour ;
}

int
Game_setrack_random_aux(Game game, Playedrack p, set_rack_mode mode, unsigned short int etat[3])
{
    // retour :
    // 0 si OK
    // 1 si mauvais nb voyelles/consonnes
    // 2 si sac vide
    // 3 si plus assez voy/cons dans sac
    //
    int i,min,nold;
    tile_t l;
    Bag b;

    /* create a copy of the bag in which we can do everything we want */
    b = Bag_create();
    Bag_copy(b, game->bag);

    /* si le sac est vide */
    if (Bag_ntiles(b) == 0) {
        Bag_destroy(b);
        return 2;
    }

    min = Game_getnrounds(game)<15 ? 2 : 1 ;

    /* pas assez de consonnes ou de voyelles et plus de joker*/
    if ((Bag_nvowels(b) < min || Bag_nconsonants(b) < min) && (Bag_njoker(b) == 0)) {
        Bag_destroy(b);
        return 3;
    }

    nold = Playedrack_nold(p);

    /* si rack vide ou mode RACK_ALL*/
    if (mode == RACK_ALL || nold == 0) {
        Playedrack_init(p);
        for (i=0; Bag_ntiles(b)!=0 && i<RACK_MAX; i++) {
            l = Bag_select_random(b,etat);
            Bag_taketile(b,l);
            Playedrack_addold(p,l);
        }
    } else {
        /* on complète un rack */
        /* we flush the "new" part of the rack */
        Playedrack_resetnew(p);

        /* retirer les "old" lettres du bag */
        for(i=0; i<nold; i++) {
            Bag_taketile(b,Playedrack_oldtiles(p,i)) ;
        }

        /* take new tiles from the bag */
        for (i=nold; Bag_ntiles(b)!=0 && i<RACK_MAX; i++) {
            l = Bag_select_random(b,etat);
            Bag_taketile(b,l);
            Playedrack_addnew(p,l);
        }
    }
    Bag_destroy(b);
    return Playedrack_check_rack(p, min) ;
}

int
Game_getcharinbag(Game g, char c)
{
    return Bag_in(g->bag,chartocode(c));
}

int
Game_getnrounds(Game g)
{
    return g->nrounds;
}

void
Game_getplayedrack(Game g, int num, char buff[RACK_SIZE_MAX])
{
    int i,l = 0;
    Playedrack p;
    buff[0] = '\0';
    if (num < 0 || num > g->nrounds) {
        return;
    }
    p = g->playedracks[num];
    for (i=0; i<Playedrack_nold(p); i++) {
        buff[l++] = codetochar(Playedrack_oldtiles(p,i));
    }
    if (Playedrack_nold(p) && Playedrack_nnew(p)) {
        buff[l++] = '+';
    }
    for (i=0; i<Playedrack_nnew(p); i++) {
        buff[l++] = codetochar(Playedrack_newtiles(p,i));
    }
    buff[l] = '\0';
}

void
Game_getplayedword(Game g, int num, char buff[WORD_SIZE_MAX])
{
    Round r;
    char c;
    int i,l = 0;
    buff[0] = 0;
    if (num < 0 || num >= g->nrounds)
        return;
    r = g->playedrounds[num];
    for(i=0; i < Round_wordlen(r); i++) {
        c = codetochar(Round_gettile(r,i));
        if (Round_joker(r,i)) {
            c = tolower(c);
        }
        buff[l++] = c;
    }
    buff[i] = 0;
}

void
Game_getplayedfirstcoord (Game g,int num,char buff[COOR_SIZE_MAX])
{
    Round r;
    buff[0] = 0;
    if (num < 0 || num >= g->nrounds)  {
        return;
    }
    r = g->playedrounds[num];
    if (Round_dir(r) == HORIZONTAL) {
        snprintf(buff,COOR_SIZE_MAX,"%c",Round_row(r)+'A'-1);
    } else {
        snprintf(buff,COOR_SIZE_MAX,"%d",Round_column(r));
    }
}

void
Game_getplayedsecondcoord(Game g,int num,char buff[COOR_SIZE_MAX])
{
    Round r;
    buff[0] = 0;
    if (num < 0 || num >= g->nrounds) {
        return;
    }
    r = g->playedrounds[num];
    if (Round_dir(r) == HORIZONTAL) {
        snprintf(buff,COOR_SIZE_MAX,"%d",Round_column(r));
    } else {
        snprintf(buff,COOR_SIZE_MAX,"%c",Round_row(r)+'A'-1);
    }
}

void
Game_getplayedcoord(Game g, int num, char buff[COOR_SIZE_MAX])
{
    char c1[COOR_SIZE_MAX];
    char c2[COOR_SIZE_MAX];
    Game_getplayedfirstcoord(g,num,c1);
    Game_getplayedsecondcoord(g,num,c2);
    snprintf(buff,COOR_SIZE_MAX,"%2s%2s",c1,c2);
}

int
Game_getplayedpoints(Game g, int num)
{
    if (num < 0 || num >= g->nrounds) {
        return 0;
    }
    return Round_points(g->playedrounds[num]);
}

int
Game_getplayedbonus(Game g, int num)
{
    if (num < 0 || num >= g->nrounds)  {
        return 0;
    }
    return Round_bonus(g->playedrounds[num]);
}

int
Game_getnresults(Game g)
{
    return Results_in(g->searchresults);
}

int
Game_getntotal(Game g)
{
    return Results_total(g->searchresults);
}

void
Game_getsearchedword(Game g, int num ,char buff[WORD_SIZE_MAX])
{
    Round r;
    char c;
    int i,l = 0;
    buff[0] = 0;
    if (num < 0 || num >= Results_in(g->searchresults)) {
        return;
    }
    r = Results_get(g->searchresults,num);
    for (i=0; i < Round_wordlen(r); i++) {
        c = codetochar(Round_gettile(r,i));
        if (Round_joker(r,i)) {
            c = tolower(c);
        }
        buff[l++] = c;
    }
    buff[i] = 0;
}

void
Game_getsearchedfirstcoord(Game g,int num,char buff[COOR_SIZE_MAX])
{
    Round r;
    buff[0] = 0;
    if (num < 0 || num >= Results_in(g->searchresults)) {
        return;
    }
    r = Results_get(g->searchresults,num);
    if (Round_dir(r) == HORIZONTAL) {
        snprintf(buff,COOR_SIZE_MAX,"%c",Round_row(r) + 'A' - 1);
    } else {
        snprintf(buff,COOR_SIZE_MAX,"%d",Round_column(r));
    }
}

void
Game_getsearchedsecondcoord(Game g, int num, char buff[COOR_SIZE_MAX])
{
    Round r;
    buff[0] = 0;
    if (num < 0 || num >= Results_in(g->searchresults))  {
        return;
    }
    r = Results_get(g->searchresults,num);
    if (Round_dir(r) == HORIZONTAL) {
        snprintf(buff,COOR_SIZE_MAX,"%d",Round_column(r));
    } else {
        snprintf(buff,COOR_SIZE_MAX,"%c",Round_row(r) + 'A' - 1);
    }
}

void
Game_getsearchedcoord(Game g, int num, char buff[COOR_SIZE_MAX])
{
    char c1[COOR_SIZE_MAX];
    char c2[COOR_SIZE_MAX];
    Game_getsearchedfirstcoord(g,num,c1);
    Game_getsearchedsecondcoord(g,num,c2);
    snprintf(buff,COOR_SIZE_MAX,"%2s%2s",c1,c2);
}

int
Game_getsearchedpoints(Game g, int num)
{
    if (num < 0 || num >= Results_in(g->searchresults)) {
        return 0;
    }
    return Round_points(Results_get(g->searchresults,num));
}

void
Game_getsearchedround(Game g, int num, Round round) {
    Round_copy(round,Results_get(g->searchresults,num)) ;
}
