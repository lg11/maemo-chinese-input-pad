#-!- coding=utf-8 -!-

import sys
#用来选出不完全拼音

if __name__ == "__main__":
    file = open( sys.argv[1] )
    buffer = file.readlines()
    lines = []
    for line in buffer:
        lines.append( line[:-1] )
    for i in range( len( lines ) - 1 ):
        len_current = len( lines[i] )
        len_next = len( lines[i+1] )
        if len_next - len_current > 1:
            if lines[i] == lines[i][ : len_current ] :
                #str = lines[i] + " " + lines[i+1]
                str = lines[i+1][:-1]
                print str
