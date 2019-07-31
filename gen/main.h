extern int verbeux;
extern int use_best;
extern FILE* out;

int cmp_score_best(score_best score_a, score_best score_b);
int cmp_score(score score_a, score score_b);
int print_line(Game game, int num, int nbisotop, int change_tirage, int notiret, int nbsol);
score traite(Game game, int num, unsigned short int state[3]);
int traite_cross(Game game, int num);
int traite_scrab(Game game, int num);
int traite_joker(Game game, int num);
int traite_pc(Game game, int num);
score_best traite_best(Game game, int num, unsigned short int state[3]);
int fin_partie (Game game, int noprint, int nbscrab, int maxisotop);
int main_loop(Game game,int noprint, int notiret, int nbessai, unsigned short int state[3]);
void help();
