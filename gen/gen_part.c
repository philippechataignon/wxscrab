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

/* $Id: gen_part.c 16 2004-03-26 20:24:20Z philippe $                 */
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <getopt.h>

#include "dic.h"
#include "game.h"
#include "tiles.h"
#include "results.h"
#include "round.h"
#include "rack.h"
#include "bag.h"
#include "game.h"
#include "game_internals.h"
#include "gen_part.h"

int verbeux = 0;

int
cmp_score(score score_a, score score_b)
{
    // renvoit 1 si score_a > score_b
    if (score_a.best > score_b.best)
        return 1 ;
    if ((score_a.best == score_b.best) && (score_a.cross > score_b.cross))
        return 1 ;
    if ((score_a.best == score_b.best) && (score_a.cross == score_b.cross) && (score_a.scrab > score_b.scrab))
        return 1 ;
    if ((score_a.best == score_b.best) && (score_a.cross == score_b.cross) && (score_a.scrab == score_b.scrab) && (score_a.pc > score_b.pc))
        return 1 ;
    if ((score_a.best == score_b.best) && (score_a.cross == score_b.cross) && (score_a.scrab == score_b.scrab) && (score_a.pc == score_b.pc))
        return 0 ;
    return -1 ;
}

int
print_line(Game game, int num, int nbisotop, int change_tirage, int notiret, int nbsol)
{
    char word  [WORD_SIZE_MAX];
    char first [2*COOR_SIZE_MAX];
    char second[COOR_SIZE_MAX];
    char tirage[RACK_SIZE_MAX];
    printf("<tour num=\"%d\">\n", Game_getnrounds(game));
    Game_getplayedrack(game,num,tirage) ;
    if (change_tirage == 1 && !notiret) {
        printf("  <tirage>-%s</tirage>\n",tirage) ;
    } else {
        printf("  <tirage>%s</tirage>\n",tirage);
    }
    Game_getplayedword(game,num,word);
    if (!word[0]) {
        return 0;
    }
    printf("  <mot>%s</mot>\n",word);
    Game_getplayedfirstcoord(game,num,first);
    Game_getplayedsecondcoord(game,num,second);
#ifdef __OpenBSD__
    strlcat(first,second,2*COOR_SIZE_MAX) ;
#else
    strcat(first,second) ;
#endif
    printf("  <coord>%s</coord>\n",first);
    printf("  <points>%d</points>\n",Game_getplayedpoints(game,num));
    printf("  <scrab>%d</scrab>\n", Game_getplayedbonus(game,num));
    printf("  <isotop>%d</isotop>\n", nbisotop);
    printf("  <nbsol>%d</nbsol>\n", nbsol);
    printf("</tour>\n\n");
    return 0;
}

score 
traite(Game game, int num, unsigned short int state[3]) 
{
    score w_score ;
    w_score.cross = traite_cross(game,num) ;
    w_score.best  = traite_best(game,num,state) ; 
    w_score.scrab = traite_scrab(game,num) ;
    w_score.pc    = traite_pc(game,num) ;

    if (verbeux >=1) {
        char mot[WORD_SIZE_MAX] ;
        char coord[COOR_SIZE_MAX];
        Game_getsearchedcoord(game,num,coord);
        Game_getsearchedword(game,num,mot) ;
        //printf("<verbeux>%s - %s (%d)</verbeux>\n",coord, mot,score );
    }
    return w_score ;
}

int 
traite_cross(Game game, int num) 
{
    int score ;
    Game_testplay(game, num) ;
    score = Game_getcalc_cross(game);
    Game_removetestplay(game) ;
    if (verbeux >=2) {
        printf("<score_cross>%d</score_cross>\n", score);
    }
    return score ;
}

int 
traite_scrab(Game game, int num) 
{
    int score ;
    Game_testplay(game, num) ;
    score = Game_getcalc_scrab(game) ;
    Game_removetestplay(game) ;
    if (verbeux >=2) {
        printf("<score_scrab>%d</score_scrab>\n", score);
    }
    return score ;
}

int 
traite_pc(Game game, int num) 
{
    int i;
    int score = 0 ;
    Round round ;

    round=Round_create() ;
    Game_getsearchedround(game,num,round) ;

    for(i=0; i < Round_wordlen(round); i++) {
        if (Round_playedfromrack(round,i)) {
            if (Round_joker(round,i)) {
                score -= 10000000 ;
                score += Tiles_pc[Round_gettile(round,i)] ;
            } else {
                score -= Tiles_pc[Round_gettile(round,i)] ;
            }
        }
    }

    Round_destroy(round) ;
    if (verbeux >=2) {
        printf("<score_pc>%d</score_pc>\n", score);
    }
    return score ;
}

int 
traite_best(Game game, int num, unsigned short int state[3]) 
{
    int i;
    int score = 0 ;
    unsigned short int contexte[3] ;
    Game g ;
    int tir ;
    
    /* sauve le contexte rand */
    for (i=0 ; i<3 ; i++) {
        contexte[i] = state[i] ;
    }

    /* Fait une copie de game dans g pour faire ce qu'on veut */
    g = Game_create(game->dic) ;
    Game_copy_n(g,game) ;
    /* joue le round num dans la copie de game */
    Game_play_round(g,Results_get(game->searchresults,num)) ;
    // tir vaut 1 si retirage ; -1 si vide et 0 sinon
    if ( (tir=Game_setrack_random(g,state)) == -1) {
        score = 0 ;
        goto fin ;
    }
    Game_search(g);
    if (Game_getnresults(g) == 0) {
        score = 0 ;
    } else {
        score = Game_getsearchedpoints(g, 0) ;
    }
    if (tir == 1) {
        score -= 10 ;
    }
    if (verbeux >=2) {
        printf("<score_best_pts>%d</score_best_pts>\n", score);
        printf("<best_sol>%d</best_sol>\n", Game_getntotal(g));
        printf("<tirage>%d</tirage>\n", tir);
    }
    score *= 10000 ;
    score += Game_getntotal(g)*10 ;

    if (verbeux >= 3) {
        char mot[WORD_SIZE_MAX] ;
        char coord[COOR_SIZE_MAX];
        for (i=0 ; i<Game_getnresults(g); i++) {
            Game_getsearchedcoord(g,i,coord);
            Game_getsearchedword(g,i,mot) ;
            printf("<mot>%s - %s - %d</mot>\n",coord, mot,score );
        }
    }

fin:
    Game_destroy(g) ;
    /* restaure le contexte random */
    for (i=0 ; i<3 ; i++) {
        state[i]=contexte[i] ;
    }
    if (verbeux >=2) {
        printf("<score_best>%d</score_best>\n", score);
    }
    return score ;
}

int 
fin_partie (Game game, int noprint, int nbscrab, int maxisotop) 
{
    printf("<resume>\n<total>%d</total>\n",Game_getpoints (game)) ;
    printf("<nbtour>%d</nbtour>\n",Game_getnrounds(game)) ;
    printf("<nbscrab>%d</nbscrab>\n",nbscrab) ;
    printf("<maxisotop>%d</maxisotop>\n</resume>\n",maxisotop) ;
    puts("</partie>");
    return 0 ;
}

int
main_loop(Game game,int noprint, int notiret, int nbessai, unsigned short int state[3])
{
    int nbscrab = 0;
    int nbisotop = 0 ;
    int maxisotop = 0 ;
    int nbsol = 0 ;

    while(1) {
        int i,res;
        int joue;
        score w_score ;
        memset(&w_score, 0, sizeof(score));
        score t_score ;
        int change_tirage = 0 ;
        res = Game_setrack_random(game,state) ;
        if (res == -1) {
            // puts ("# Plus de consonnes ou de voyelles") ;
            fin_partie(game,noprint,nbscrab,maxisotop) ;
            return 0 ;
        }

        if (res == 1) {
            change_tirage = 1;
        }

        Game_search(game);

        while (Game_getnresults(game) == 0 && nbessai-- > 0) {
            change_tirage = 2 ;
            if (verbeux) {
                char tirage[RACK_SIZE_MAX];
                Game_getplayedrack(game,Game_getnrounds(game),tirage) ;
                printf ("<essai_tirage>%s</essai_tirage>\n",tirage) ;
            }
            Game_setrack_random(game,state) ;
            Game_search(game);
        }
        
        if (nbessai < 0) {
            fin_partie(game,noprint,nbscrab,maxisotop) ;
            return 0 ;
        }
        
        nbisotop = Game_getnresults(game) ;
        nbsol    = Game_getntotal(game) ;
        
        if (nbisotop > maxisotop) {
            maxisotop = nbisotop ;
        }
    
        if (nbisotop == 1) {
            Game_play(game, 0) ;
        } else {
            joue = 0 ;
            w_score = traite(game,0,state);
            for (i = 1; i<nbisotop; i++) {
                if ( cmp_score(t_score=traite(game,i,state), w_score) > 0 ) {
                    w_score = t_score ;
                    joue = i;
                }
            }
            Game_play(game, joue) ;
        }
        if (Game_getplayedbonus(game,Game_getnrounds(game)-1)) {
            nbscrab ++ ;
        }
        if (Game_getnrounds(game)==1 || (Game_getplayedbonus(game,Game_getnrounds(game)-2))) {
            change_tirage = 0 ;
        }
        if (! noprint) {
            print_line(game,Game_getnrounds(game)-1,nbisotop,change_tirage,notiret,nbsol);
        }
    }
}

void
help()
{
    puts ("G�n�ration de parties Scrabble - Philippe CHATAIGNON") ;
    puts ("d'apr�s Eliot - Antoine FRABOULET - sous license GPL") ;
    puts ("");
    puts ("Utilisation : gen_part [-d dictionnaire] [-n num�ro] [-s seed] [-v] [-q] [-h]") ; 
    puts ("        -d : fichier dawg contenant le dictionnaire (par d�faut : ../dic/ods5.dawg)");
    puts ("        -n : num�ro de la partie � g�n�rer ; par d�faut, utilise time(0)");
    puts ("        -s : seed, valeur de la variante  ; par d�faut, 47482");
    puts ("        -q : n'imprime que les statistiques de la partie");
    puts ("        -t : n'imprime pas un - devant les tirages rejet�s");
    puts ("        -e : nombre d'essais de tirages si absence de solution (par d�faut : 1000) ; -e0 pour supprimer la fonctionnalit�");    
    puts ("        -h : affiche cette aide");
    puts ("");
}

int
main(int argc, char *argv[])
{
    Game game ;
    Dictionary dic ;
    unsigned short int state[3] ;
    static char* nomdic = "../dic/ods5.dawg" ;
    long int seed = time(0) ;
    int noprint = 0;
    int notiret = 0;
    int nbessai = 1000;
    int c;
    verbeux = 0;

    srand48(0);
    state[2] = 0xB97A ;

    opterr = 0;
    while ((c = getopt (argc, argv, "qd:n:s:e:vht")) != -1) {
        switch (c) {
            case 'v':
                verbeux++;
                break;
            case 's':
                state[2]= atoi(optarg);
                break;
            case 'e':
                nbessai = atoi(optarg);
                break;
            case 't':
                notiret = 1;
                break;
            case 'q':
                noprint = 1;
                break;
            case 'd':
                nomdic = optarg;
                break;
            case 'n':
                seed = atoi(optarg);
                break;
            case 'h' :
                help() ;
                exit(10) ;
                break ;
            case '?':
                if (isprint (optopt)) {
                    help() ;
                    fprintf (stderr, "Option inconnue `-%c'.\n", optopt);
                } else {
                    help() ;
                    fprintf (stderr, "Caract�re non reconnu dans les options `\\x%x'.\n",optopt);
                }
                return 1;
            default:
                abort ();
        }
    }    

    if (! nomdic) {
        help() ;
        puts("Sp�cifier un dictionnaire avec l'option -d (ex : -d ods4.dawg)") ;
        exit(11);
    }

    switch (Dic_load(&dic, nomdic)) {
        case 0:
            /* cas normal */
            break;
        case 1:
            help();
            printf("chargement: probl�me d'ouverture de %s\n",nomdic) ;
            exit(1);
            break;
        case 2:
            help();
            printf("chargement: mauvais en-tete de dictionnaire\n");
            exit(2);
            break;
        case 3:
            help();
            printf("chargement: probl�me 3 d'allocation m�moire\n");
            exit(3);
            break;
        case 4:
            help();
            printf("chargement: probl�me 4 d'allocation m�moire\n");
            exit(4);
            break;
        case 5:
            help();
            printf("chargement: probl�me de lecture des arcs du dictionnaire\n");
            exit(5);
            break;
        default:
            help();
            printf("chargement: probl�me non-repertori�\n");
            exit(6);
            break;
    }

    state[0] = seed>>16 ;
    state[1] = seed&0x0000FFFF ;

    printf("<?xml version=\"1.0\"?>\n");
    printf("<partie ");
    printf("num=\"%ld\" ",seed);
    printf("seed=\"%d\" ",state[2]);
    printf("dic=\"%s\" >\n",nomdic) ;
    
    game = Game_create(dic);
    main_loop(game,noprint,notiret,nbessai,state);
    Game_destroy(game);
    Dic_destroy(dic);
    return 0;
}
