#-!- coding=utf-8 -!-

import string

def phrase_raw() :
    chars = "abcdefghijklmnopqrstuvwxyz"
    nums  = "22233344455566677778889999"

    trans = string.maketrans( chars, nums )

    file_raw = open( "cache/utf8raw", "r" )
    file_out = open( "cache/sqlite", "w" )

    lines = file_raw.readlines()
    count = [ 0, len( lines ) ]
    for line in lines :
        count[0] = count[0] + 1

        line = line[:-1]
        line = line.split()

        code = "".join( line[3:] ).translate( trans )
        pinyin = "'".join( line[3:] )
        hanzi = line[0]
        freq = line[1]
        
        length = len( hanzi.decode( "utf-8" ) )
        if length <= 5 :
            print "insert", hanzi, count[0], "/", count[1]
            strings = [ code, pinyin, hanzi, freq ]
            file_out.write( "|".join( strings ) + "\n" )
        else :
            print "drop", hanzi, count[0], "/", count[1]

    file_raw.close()
    file_out.close()

if __name__ == "__main__" :
    phrase_raw()
