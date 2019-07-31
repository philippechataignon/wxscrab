%module dic
%{
#define SWIG_FILE_WITH_INIT
#include "dic_internals.h"
#include "dic.h"
%}

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
