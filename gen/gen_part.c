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
#include "main.h"

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
