%module dic
%{
#define SWIG_FILE_WITH_INIT
#include "dic_internals.h"
#include "dic.h"
%}
int Dic_load(Dictionary *dic, const char* path);
int Dic_destroy(Dictionary dic);
int test_mot(Dictionary dic, const char* mot);
