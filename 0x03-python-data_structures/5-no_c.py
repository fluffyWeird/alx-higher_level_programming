#!/usr/bin/python3
def no_c(my_string):
    mystring = list(my_string)
    for i in range(len(mystring)):
        if mystring[i] == 'c' or mystring[i]== 'C':
            mystring[i] = ''
    return "".join(mystring)
