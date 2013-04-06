#!/bin/zsh
export VIRTUAL_ENV="/home/scrabble/ve"
cd $VIRTUAL_ENV
tmux new-session -s scrab -n normal -d 
tmux send-keys 'cd wxscrab/server' 'C-m'
tmux send-keys '$VIRTUAL_ENV/bin/python go.py -p1989 -l' 'C-m'
sleep 1
tmux new-window  -a -t normal -n topping -d 
tmux select-window -n
tmux send-keys 'cd wxscrab/server' 'C-m'
tmux send-keys '$VIRTUAL_ENV/bin/python go.py -p1991 -o -c90 -i10 -l' 'C-m'
sleep 1
tmux new-window  -a -t normal -n public -d 
tmux select-window -n
tmux send-keys 'cd wxscrab/server' 'C-m'
tmux send-keys '$VIRTUAL_ENV/bin/python go.py -p12345' 'C-m'
