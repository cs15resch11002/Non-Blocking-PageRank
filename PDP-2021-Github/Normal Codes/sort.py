import os
import sys
import numpy as np
from operator import itemgetter

file_name = sys.argv[1]

data = open(file_name, 'r').readline().strip().split("\t")

print("started reading data")
if len(data) == 2 :
	data = [list(map(int, x.strip().split("\t"))) for x in open(file_name, 'r').readlines()]
else :
	data = [list(map(int, x.strip().split(" "))) for x in open(file_name, 'r').readlines()]

print("started sorting")
data = sorted(data, key=itemgetter(1))
data = sorted(data, key=itemgetter(0))
data = ["\t".join(list(map(str, x))) for x in data]

print("saving to file")
f = open(file_name, 'w')
for i in data :
    f.write(i + "\n")
f.close()
