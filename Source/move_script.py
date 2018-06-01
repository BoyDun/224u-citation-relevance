import sys
import os
import random
from shutil import copyfile

probability = 0.01
counter = 0
IN = 'nd'
OUT = 'nd_100'

for f in os.listdir(IN):
    if random.uniform(0,1) >= probability:
        continue
    print f
    path = os.path.join(IN, f)
    out = os.path.join(OUT, f)
    copyfile(path, out)
    counter += 1
    print counter
    if counter >= 99:
        break
