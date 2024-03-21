#!/usr/bin/python3
import sys
argc = len(sys.argv) - 1
print('{} {}:'.format(argc, sys.argv[argc]))
for i in range(argc):
    j = i + 1
    print('{:d}: {:d}'.format(j, sys.argv[j]))
