#!/bin/sh
tmux new-session -s scrab -n normal      -d  './go.py  -p1992'
tmux new-window  -a -t normal -n topping -d  './go.py  -p1993 -o'
