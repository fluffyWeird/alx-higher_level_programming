#!/usr/bin/python3
import sys
argc = len(sys.argv) - 1
sum = 0
for i in range(argc):
    j = i + 1
    asrgint = int(sys.argv[j])
    sum += asrgint
print(sum)
