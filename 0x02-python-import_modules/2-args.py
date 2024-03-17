#!/usr/bin/python3
import sys
if __name__ == '__main__':
    argc = len(sys.argv) - 1
    if argc > 0:
        print('{} arguments:'.format(argc))
        for i in range(argc):
            j = i + 1
            print('{}: {}'.format(j, sys.argv[j]))
    elif argc == 0:
        print('0 arguments.')
