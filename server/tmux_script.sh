#!/bin/sh
#
# cd /home/scrabble/wxscrab2/server
# su -c "./tmux_script.sh" scrabble
#
tmux new-session -s scrab -n normal      -d  './go.py  -p1989 -l'
tmux new-window  -a -t normal -n topping -d  './go.py  -p1991 -o -c90 -i10 -l'
