#!/usr/bin/python3
# str = "Holberton School"
# print(f"{str*3}\n{str[:8]}\n")
#5-print

#6-concatinate

# str1 = "Holberton"
# str2 = "School"
# str={str1} + " " +{str2}
# print(f"Welcome to {str}!")

#7-edges

# word = "Holberton"
# word_first_3 = word[:3]
# word_last_2 = word[-2:]
# middle_word = word[1:-1]

# 8-concaat_edges
str = "Python is an interpreted, interactive, object-oriented programming\
         language that combines remarkable power with very clear syntax"
str1=str[39:66] + " "
str2=str[115:119] + " "
str3=str[:6] + " "

print(f"{str1}{str2}{str3}")