CC=gcc
CFLAGS=-O3 -Wall

exe = gen_part

src = bag.c board.c  board_cross.c board_search.c dic.c game.c \
        gen_part.c getopt.c pldrack.c rack.c results.c round.c tiles.c

obj = bag.o board.o  board_cross.o board_search.o dic.o game.o \
        gen_part.o getopt.o pldrack.o rack.o results.o round.o tiles.o

all : dep $(exe)
$(exe) :  $(obj)
	$(CC) -o $(exe) $(obj)
bag.o: bag.c tiles.h bag.h
board.o: board.c dic.h dic_internals.h tiles.h round.h bag.h rack.h \
  results.h board.h board_internals.h
board_cross.o: board_cross.c dic.h dic_internals.h tiles.h bag.h rack.h \
  round.h results.h board.h board_internals.h
board_search.o: board_search.c dic.h dic_internals.h tiles.h bag.h rack.h \
  round.h results.h board.h board_internals.h
dic.o: dic.c dic_internals.h dic.h
game.o: game.c dic.h dic_internals.h tiles.h bag.h rack.h round.h \
  pldrack.h results.h board.h game.h game_internals.h board_internals.h
gen_part.o: gen_part.c dic.h dic_internals.h game.h round.h tiles.h \
  pldrack.h rack.h results.h bag.h game_internals.h board.h \
  board_internals.h gen_part.h
getopt.o: getopt.c getopt.h
pldrack.o: pldrack.c tiles.h rack.h pldrack.h
rack.o: rack.c tiles.h rack.h
results.o: results.c tiles.h round.h results.h
round.o: round.c tiles.h round.h
tiles.o: tiles.c tiles.h

dep: Makefile.dep
Makefile.dep : $(src)
	gcc -MM $(src) > Makefile.dep

clean :
	-rm -rf  *.o
mrproper :
	-rm -f  $(exe) Makefile.dep *.o

