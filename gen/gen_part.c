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
int use_best = 1;
FILE* out = NULL;

int
cmp_score_best(score_best score_a, score_best score_b)
{
    // tri dans l'ordre retir/pts/nb
    int d_retir = score_a.retir - score_b.retir ;
    int d_pts   = score_a.pts   - score_b.pts ;
    int d_nb    = score_a.nb    - score_b.nb ;
    //fprintf(out,"%d %d %d\n", d_pts,d_nb,d_retir) ;
    if (d_retir > 0)
        return 1 ;
    if (d_retir == 0 && d_pts > 0)
        return 1 ;
    if (d_retir == 0 && d_pts == 0 && d_nb > 0)
        return 1 ;
    if (d_retir == 0 && d_pts == 0 && d_nb == 0)
        return 0 ;
    return -1 ;
}

int
cmp_score(score score_a, score score_b)
{
    // renvoit 1 si score_a > score_b, 0 si =, -1 sinon
    int d_best;
    if (use_best) {
        d_best  = cmp_score_best(score_a.best, score_b.best) ;
    } else {
        d_best = 0;
    }
    int d_cross = score_a.cross - score_b.cross ;
    int d_scrab = score_a.scrab - score_b.scrab ;
    int d_joker = score_a.joker - score_b.joker ;
    int d_pc    = score_a.pc    - score_b.pc ;
    //fprintf(out,"%d %d %d %d %d \n", d_best,d_cross,d_scrab,d_joker,d_pc) ;
    if (d_joker > 0 )
        return 1 ;
    if (d_joker == 0 && d_best > 0)
        return 1 ;
    if (d_joker == 0 && d_best == 0 && d_cross > 0)
        return 1 ;
    if (d_joker == 0 && d_best == 0 && d_cross == 0 && d_scrab > 0)
        return 1 ;
    if (d_joker == 0 && d_best == 0 && d_cross == 0 && d_scrab == 0 && d_pc > 0 )
        return 1 ;
    if (d_joker == 0 && d_best == 0 && d_cross == 0 && d_scrab == 0 && d_pc == 0)
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
    fprintf(out,"<tour num=\"%d\">\n", Game_getnrounds(game));
    Game_getplayedrack(game,num,tirage) ;
    if (change_tirage == 1 && !notiret) {
        fprintf(out,"  <tirage>-%s</tirage>\n",tirage) ;
    } else {
        fprintf(out,"  <tirage>%s</tirage>\n",tirage);
    }
    Game_getplayedword(game,num,word);
    if (!word[0]) {
        return 0;
    }
    fprintf(out,"  <mot>%s</mot>\n",word);
    Game_getplayedfirstcoord(game,num,first);
    Game_getplayedsecondcoord(game,num,second);
#ifdef __OpenBSD__
    strlcat(first,second,2*COOR_SIZE_MAX) ;
#else
    strcat(first,second) ;
#endif
    fprintf(out,"  <coord>%s</coord>\n",first);
    fprintf(out,"  <points>%d</points>\n",Game_getplayedpoints(game,num));
    fprintf(out,"  <scrab>%d</scrab>\n", Game_getplayedbonus(game,num));
    fprintf(out,"  <isotop>%d</isotop>\n", nbisotop);
    fprintf(out,"  <nbsol>%d</nbsol>\n", nbsol);
    fprintf(out,"</tour>\n\n");
    // Bag_print(game->bag);
    return 0;
}

score
traite(Game game, int num, unsigned short int state[3])
{
    if (verbeux >=1) {
        char mot[WORD_SIZE_MAX] ;
        char coord[COOR_SIZE_MAX];
        Game_getsearchedcoord(game,num,coord);
        Game_getsearchedword(game,num,mot) ;
        fprintf(out,"<mot>%s - %s</mot>\n",coord, mot);
    }
    score w_score ;
    w_score.cross = traite_cross(game,num) ;
    if (use_best) {
        w_score.best = traite_best(game,num,state);
    }
    w_score.scrab = traite_scrab(game,num) ;
    w_score.pc    = traite_pc(game,num) ;
    w_score.joker = traite_joker(game,num) ;
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
        fprintf(out,"<score_cross>%d</score_cross>\n", score);
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
        fprintf(out,"<score_scrab>%d</score_scrab>\n", score);
    }
    return score ;
}

int
traite_joker(Game game, int num)
{
    int i;
    int score = 2 ;
    Round round ;
    round=Round_create() ;
    Game_getsearchedround(game,num,round) ;

    for(i=0; i < Round_wordlen(round); i++) {
        if (Round_playedfromrack(round,i)) {
            if (Round_joker(round,i)) {
                score -= 1 ;
            }
        }
    }
    Round_destroy(round) ;
    if (verbeux >=2) {
        fprintf(out,"<score_joker>%d</score_joker>\n", score);
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
                score += Tiles_pc[Round_gettile(round,i)] ;
            } else {
                score -= Tiles_pc[Round_gettile(round,i)] ;
            }
        }
    }
    Round_destroy(round) ;
    if (verbeux >=2) {
        fprintf(out,"<score_pc>%d</score_pc>\n", score);
    }
    return score ;
}

score_best
traite_best(Game game, int num, unsigned short int state[3])
{
    int i;
    score_best sscore ;
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
    tir = Game_setrack_random(g, state, 0) ;
    if (tir >= 2) {
        sscore.pts = 0 ;
        sscore.nb  = 0 ;
        goto fin ;
    }
    // renvoit 1 si pas de retirage, 0 sinon
    sscore.retir = tir == 1 ? 0 : 1;
    Game_search(g);
    if (Game_getnresults(g) == 0) {
        sscore.pts = 0 ;
        sscore.nb  = 0 ;
    } else {
        sscore.pts = Game_getsearchedpoints(g, 0) ;
        sscore.nb  = Game_getntotal(g) ;
    }

    if (verbeux >=2) {
        fprintf(out,"<best_tirage>%d</best_tirage>\n", sscore.retir);
        fprintf(out,"<best_pts>%d</best_pts>\n", sscore.pts);
        fprintf(out,"<best_nb>%d</best_nb>\n", sscore.nb);
    }

    if (verbeux >= 3) {
        char mot[WORD_SIZE_MAX] ;
        char coord[COOR_SIZE_MAX];
        for (i=0 ; i<Game_getnresults(g); i++) {
            Game_getsearchedcoord(g,i,coord);
            Game_getsearchedword(g,i,mot) ;
            fprintf(out,"<mot>%s - %s</mot>\n",coord, mot );
        }
    }

fin:
    Game_destroy(g) ;
    /* restaure le contexte random */
    for (i=0 ; i<3 ; i++) {
        state[i]=contexte[i] ;
    }
    return sscore ;
}

int
fin_partie (Game game, int noprint, int nbscrab, int maxisotop)
{
    fprintf(out,"<resume>\n<total>%d</total>\n",Game_getpoints (game)) ;
    fprintf(out,"<nbtour>%d</nbtour>\n",Game_getnrounds(game)) ;
    fprintf(out,"<nbscrab>%d</nbscrab>\n",nbscrab) ;
    fprintf(out,"<maxisotop>%d</maxisotop>\n</resume>\n",maxisotop) ;
    fprintf(out,"</partie>\n");
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
        score t_score ;
        int change_tirage = 0 ;
        res = Game_setrack_random(game, state, 0) ;
        // -1 = problème définitif lié au sac
        if (res == -1) {
            fin_partie(game,noprint,nbscrab,maxisotop) ;
            return 0 ;
        }

        // 1 = OK après retirage
        if (res == 1) {
            change_tirage = 1;
        }

        Game_search(game);

        while (Game_getnresults(game) == 0 && nbessai-- > 0) {
            change_tirage = 2 ;
            if (verbeux) {
                char tirage[RACK_SIZE_MAX];
                Game_getplayedrack(game,Game_getnrounds(game),tirage) ;
                fprintf(out,"<essai_tirage>%s</essai_tirage>\n",tirage) ;
            }
            Game_setrack_random(game, state, 1) ;
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
    puts ("Génération de parties Scrabble - Philippe CHATAIGNON") ;
    puts ("d'après Eliot - Antoine FRABOULET - sous license GPL") ;
    puts ("");
    puts ("Utilisation : gen_part [-d dictionnaire] [-n numéro] [-s seed] [-v] [-q] [-h]") ;
    puts ("        -d : fichier dawg contenant le dictionnaire (par défaut : ../dic/ods7.dawg)");
    puts ("        -n : numéro de la partie à générer ; par défaut, utilise time(0)");
    puts ("        -s : seed, valeur de la variante  ; par défaut, 47482");
    puts ("        -q : n'imprime que les statistiques de la partie");
    puts ("        -t : n'imprime pas un - devant les tirages rejetés");
    puts ("        -e : nombre d'essais de tirages si absence de solution (par défaut : 1000) ; -e0 pour supprimer la fonctionnalité");
    puts ("        -b : pas de best score (couteux en temps)");
    puts ("        -h : affiche cette aide");
    puts ("");
}

int
main(int argc, char *argv[])
{
    Game game ;
    Dico dic ;
    unsigned short int state[3] ;
    static char* nomdic = "../../wxscrab/dic/ods7.dico" ;
    unsigned long int seed = time(0) ;
    int noprint = 0;
    int notiret = 0;
    int nbessai = 1000;
    int c;
    verbeux = 0;
    out = stdout;

    srand48(0);
    state[2] = 0xB97A ;

    opterr = 0;
    while ((c = getopt (argc, argv, "o:bqd:n:s:e:vht")) != -1) {
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
            case 'b':
                use_best = 0;
                break;
            case 'q':
                noprint = 1;
                break;
            case 'd':
                nomdic = optarg;
                break;
            case 'n':
                seed = strtoul(optarg, NULL, 10);
                break;
            case 'o':
                out = fopen(optarg, "w");
                break;
            case 'h' :
                help() ;
                exit(10) ;
                break ;
            case '?':
                if (isprint (optopt)) {
                    help() ;
                    fprintf(stderr, "Option inconnue `-%c'.\n", optopt);
                } else {
                    help() ;
                    fprintf(stderr, "Caractère non reconnu dans les options `\\x%x'.\n",optopt);
                }
                return 1;
            default:
                abort ();
        }
    }

    if (!nomdic) {
        help() ;
        puts("Spécifier un dictionnaire avec l'option -d (ex : -d ods7.dawg)") ;
        exit(11);
    }

    switch (Dic_init(&dic, nomdic)) {
        case 0:
            /* cas normal */
            break;
        case 1:
            help();
            fprintf(out,"chargement: problème d'ouverture de %s\n",nomdic) ;
            exit(1);
            break;
        case 2:
            help();
            fprintf(out,"chargement: mauvais en-tete de dictionnaire\n");
            exit(2);
            break;
        case 3:
            help();
            fprintf(out,"chargement: problème 3 d'allocation mémoire\n");
            exit(3);
            break;
        case 4:
            help();
            fprintf(out,"chargement: problème 4 d'allocation mémoire\n");
            exit(4);
            break;
        case 5:
            help();
            fprintf(out,"chargement: problème de lecture des arcs du dictionnaire\n");
            exit(5);
            break;
        default:
            help();
            fprintf(out,"chargement: problème non-repertorié\n");
            exit(6);
            break;
    }

    state[0] = seed>>16 ;
    state[1] = seed&0x0000FFFF ;

    fprintf(out,"<?xml version=\"1.0\"?>\n");
    fprintf(out,"<partie ");
    fprintf(out,"num=\"%lu\" ",seed);
    fprintf(out,"seed=\"%u\" ",state[2]);
    fprintf(out,"dic=\"%s\" >\n",nomdic) ;

    game = Game_create(&dic);
    main_loop(game,noprint,notiret,nbessai,state);
    fclose(out);
    Game_destroy(game);
    Dic_destroy(&dic);
    return 0;
}
