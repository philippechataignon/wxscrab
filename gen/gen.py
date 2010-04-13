#! /usr/bin/python
import subprocess
import sys
import re

r = re.compile(r"<total>(\d+)</total>", re.S|re.M)
sum = 0
for i in range(int(sys.argv[1])) :
    print i
    output = subprocess.Popen(["/home/philippe/wxscrab2/gen/gen_part -d /home/philippe/wxscrab2/dic/ods5.dawg -s 6 -q -n %d " % i], stdout=subprocess.PIPE, shell=True).communicate()[0]
    m = r.search(output)
    sum += int(m.group(1))
print sum
