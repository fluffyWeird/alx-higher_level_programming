#!/usr/bin/python3
def element_at(my_list, idx):
    count = 0
    if idx < 0:
        print("None")
    for num in my_list:
        if idx > num:
            count = count + 1
    if count > len(my_list):
        print("None")
