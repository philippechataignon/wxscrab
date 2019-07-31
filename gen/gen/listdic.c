/* Eliot                                                                     */
/* Copyright (C) 1999  antoine.fraboulet                                     */
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

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "dic_internals.h"
#include "dic.h"

static void
print_dic_rec(FILE* out, Dico dic, char *buf, char *s, Dawg_edge i)
{
	if (i.term) {		/* edge points at a complete word */
		*s = '\0';
		fprintf(out, "%s\n", buf);
	}
	if (i.ptr) {		/* Compute index: is it non-zero ? */
		Dawg_edge *p = dic.dawg + i.ptr;
		do {		/* for each edge out of this node */
			*s = p->chr + 'a' - 1;
			print_dic_rec(out, dic, buf, s + 1, *p);
		}
		while (!(*p++).last);
	}
}

void dic_load(Dico *dic, char *filename)
{
	int res;
	if ((res = Dic_init(dic, filename)) != 0) {
		switch (res) {
		case 1:
			printf("chargement: problème d'ouverture de %s\n",
			       filename);
			break;
		case 2:
			printf("chargement: mauvais en-tete de dictionnaire\n");
			break;
		case 3:
			printf
			    ("chargement: problème 3 d'allocation mémoire\n");
			break;
		case 4:
			printf
			    ("chargement: problème 4 d'alocation mémoire\n");
			break;
		case 5:
			printf
			    ("chargement: problème de lecture des arcs du dictionnaire\n");
			break;
		default:
			printf("chargement: problème non-repertorié\n");
			break;
		}
		exit(res);
	}
}

void print_dic_list(char *filename)
{
	Dico dic;
	static char buf[80];
	dic_load(&dic, filename);
	print_dic_rec(stdout, dic, buf, buf, dic.dawg[dic.root]);
    Dic_destroy(&dic);
}

void print_header(char *filename)
{
	FILE *file;
	Dict_header header;

	if ((file = fopen(filename, "rb")) == NULL)
		return;
	if (fread(&header, sizeof(Dict_header), 1, file) != 1)
		return;
	fclose(file);

	printf("Dico * header information\n");
	printf("ident       : %s\n", header.ident);
	printf("root        : %8d\n", header.root);
	printf("words       : %8d\n", header.nwords);
	printf("edges used  : %8d\n", header.edgesused);
	printf("nodes used  : %8d\n", header.nodesused);
	printf("nodes saved : %8d\n", header.nodessaved);
	printf("edges saved : %8d\n", header.edgessaved);
	printf("size header : %8zd\n", sizeof(header));
}

void print_node_hex(int i, Dico * dic)
{
	Dawg_edge e = dic->dawg[i];
	printf("%2d ptr=%2d t=%d l=%d f=%d chr=%d (%c)\n",
	       i, e.ptr, e.term, e.last, e.fill, e.chr, e.chr + 'a' - 1);
}

void print_dic_hex(char *filename)
{
	int i;
	Dico * dic;
	dic_load(dic, filename);
	for (i = 0; i < (dic->nedges + 1); i++) {
		print_node_hex(i, dic);
	}
	//Dic_destroy(dic);
}

void usage(char *name)
{
	printf("usage: %s [-a|-d|-h|-l] dictionnaire\n", name);
	printf("  -a : print all\n");
	printf("  -h : print header\n");
	printf("  -d : print dic in hex\n");
	printf("  -l : print dic word list\n");
}

int main(int argc, char *argv[])
{
	int arg_count;
	int option_print_all = 0;
	int option_print_header = 0;
	int option_print_dic_hex = 0;
	int option_print_dic_list = 0;

	if (argc < 2) {
		usage(argv[0]);
		exit(1);
	}

	arg_count = 1;
	while (argv[arg_count][0] == '-') {
		switch (argv[arg_count][1]) {
		case 'a':
			option_print_all = 1;
			break;
		case 'h':
			option_print_header = 1;
			break;
		case 'd':
			option_print_dic_hex = 1;
			break;
		case 'l':
			option_print_dic_list = 1;
			break;
		default:
			usage(argv[0]);
			exit(2);
			break;
		}
		arg_count++;
	}

	if (option_print_header || option_print_all) {
		print_header(argv[arg_count]);
	}
	if (option_print_dic_hex || option_print_all) {
		print_dic_hex(argv[arg_count]);
	}
	if (option_print_dic_list || option_print_all) {
		print_dic_list(argv[arg_count]);
	}
	return 0;
}
