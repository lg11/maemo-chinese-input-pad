#-!- coding=utf-8 -!-

import string

file = open("rawdict_utf8_65105_freq.txt", "r")
lines = file.readlines()

chars = "abcdefghijklmnopqrstuvwxyz"
nums  = "22233344455566677778889999"

trans = string.maketrans( chars, nums )

for line in lines:
    line = line[:-1]
    line = line.split()
    strings = [ line[0], line[1], "'".join(line[3:]), "".join(line[3:]).translate( trans ) ]
    print strings[1], strings[3], strings[2], strings[0]
