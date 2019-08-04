%module dic
%{
#define SWIG_FILE_WITH_INIT
#include "dic_internals.h"
#include "game_internals.h"
#include "tiles.h"
#include "board_internals.h"
#include "pldrack.h"
#include "rack.h"
#include "bag.h"
#include "board.h"
#include "dic.h"
#include "game.h"
#include "getopt.h"
#include "hashtable.h"
#include "results.h"
#include "round.h"
#include "main.h"
%}

typedef struct tresults* Results;

typedef unsigned char tile_t;

typedef struct Dico {
    Dawg_edge *dawg;
    uint32_t root;
    int32_t nwords;
    int32_t nnodes;
    int32_t nedges;
} Dico;

typedef Dico* Dictionary;

int Dic_init   (Dictionary, const char*);
int Dic_destroy(Dictionary);
int isMot(Dictionary dic, const char* mot);
int main_loop(Game game,int noprint, int notiret, int nbessai, unsigned short int state[3]);

