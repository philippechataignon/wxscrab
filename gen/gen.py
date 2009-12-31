#! /usr/bin/python
import random 
import os
import sys
os.system('rm stat.txt')
seed = 0
for i in range(int(sys.argv[1])) :
    cmd = './gen_part -q -n'+repr(seed)+' -s 6  >> stat.txt'
    print cmd
    os.system(cmd)
    seed += 1
