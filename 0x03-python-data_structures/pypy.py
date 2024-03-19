#!/usr/bin/python3
list2= ['ababa', 23, 'ametu', 'new']
print(list2)
sentence=''
for i in range(len(list2)):
   sentence = sentence + str(list2[i]) + ' '
print('{}'.format(sentence))