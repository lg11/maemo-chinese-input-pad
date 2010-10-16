#-!- coding=utf-8 -!-

import string

file = open("buffer_000", "r")
lines = file.readlines()

chars = "abcdefghijklmnopqrstuvwxyz"
nums  = "22233344455566677778889999"

trans = string.maketrans( chars, nums )

for line in lines:
    line = line[:-1]
    strings = line.split()
    code = strings[1].replace( "'", "" ).translate( trans )
    if len( code ) < 32 and len( strings[0].decode("utf-8") ) < 6 :
        print strings[2], code, strings[1], strings[0]
