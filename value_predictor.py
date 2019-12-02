# calculate median? I may have misunderstood the question!

import sys

list1 = eval(sys.argv[1])
length = len(list1)
#print(length)
half = length // 2
median = (list1[half - 1] + list1[half]) / 2
sys.stdout.write(repr(median))