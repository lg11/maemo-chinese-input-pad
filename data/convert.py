#-!- coding=utf-8 -!-

import sys

def convert_ch( ch ):
    if ch == "a" or ch == "b" or ch == "c":
        return "2"
    elif ch == "d" or ch == "e" or ch == "f":
        return "3"
    elif ch == "g" or ch == "h" or ch == "i":
        return "4"
    elif ch == "j" or ch == "k" or ch == "l":
        return "5"
    elif ch == "m" or ch == "n" or ch == "o":
        return "6"
    elif ch == "p" or ch == "q" or ch == "r" or ch == "s":
        return "7"
    elif ch == "t" or ch == "u" or ch == "v":
        return "8"
    elif ch == "w" or ch == "x" or ch == "y" or ch == "z":
        return "9"
    elif ch == "'":
        return "'"
    else:
        return ""

def convert_ch2( ch ):
    if ch == "a" or ch == "b" or ch == "c":
        return "2"
    elif ch == "d" or ch == "e" or ch == "f":
        return "3"
    elif ch == "g" or ch == "h" or ch == "i":
        return "4"
    elif ch == "j" or ch == "k" or ch == "l":
        return "5"
    elif ch == "m" or ch == "n" or ch == "o":
        return "6"
    elif ch == "p" or ch == "q" or ch == "r" or ch == "s":
        return "7"
    elif ch == "t" or ch == "u" or ch == "v":
        return "8"
    elif ch == "w" or ch == "x" or ch == "y" or ch == "z":
        return "9"
    else:
        return ""

def convert( str ):
    s = ""
    for ch in str:
        s = s + convert_ch(ch)
    return s

def convert2( str ):
    s = ""
    for ch in str:
        s = s + convert_ch2(ch)
    return s

if __name__ == "__main__":
    #print sys.argv
    file = open( sys.argv[1] )
    for line in file.readlines():
        strings = line.split()
        #str = convert( strings[1] ) + "|" + strings[1] + "|" + strings[0] + "|" + strings[2]
        str = convert2( strings[1] ) + "|" + convert( strings[1] ) + "|" + strings[1] + "|" + strings[0] + "|" + strings[2]
        #str = convert( strings[0] )
        print str

