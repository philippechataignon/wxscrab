#! /usr/bin/python
import subprocess
import sys
import re
import threading

r = re.compile(r"<total>(\d+)</total>", re.S|re.M)


class Partie(threading.Thread) :
    
    def __init__(self, n) :
        threading.Thread.__init__(self)
        self.n = n

    def run(self) :
        sem.acquire()
        output = subprocess.Popen(["./gen_part -d ../dic/ods5.dawg -s 6 -q -n %d " % self.n], stdout=subprocess.PIPE, shell=True).communicate()[0]
        m = r.search(output)
        self.score = int(m.group(1))
        sem.release()

n_arg = len(sys.argv)
if n_arg <= 1 :
    nb_part = 100
else :
    nb_part = int(sys.argv[1])
if n_arg <= 2 :
    nb_sem = 2
else :
    nb_sem = int(sys.argv[2])
sem = threading.Semaphore(nb_sem)
sum = 0
t = []

for i in xrange(nb_part) :
    s = Partie(i)
    t.append(s)
    s.start()

for thread in t :
    thread.join()
    sum += thread.score
print sum
