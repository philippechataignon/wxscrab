#!/bin/zsh
export VIRTUAL_ENV="/home/philippe/ve_wxscrab"
cd $VIRTUAL_ENV
tmux new-session -s scrab -n normal -d 
tmux send-keys 'cd wxscrab/server' 'C-m'
tmux send-keys '$VIRTUAL_ENV/bin/python go.py -d ../dic/ods7.dawg -g ../gen/gen_part -p1989 -l' 'C-m'
tmux new-window  -a -t normal -n topping -d 
tmux select-window -n
tmux send-keys 'cd wxscrab/server' 'C-m'
tmux send-keys '$VIRTUAL_ENV/bin/python go.py -d ../dic/ods7.dawg -g ../gen/gen_part -p1991 -o -c90 -i10 -l' 'C-m'
