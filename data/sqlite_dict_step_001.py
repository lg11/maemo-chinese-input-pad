#-!- coding=utf-8 -!-

import string

def phrase_raw() :
    chars = "abcdefghijklmnopqrstuvwxyz"
    nums  = "22233344455566677778889999"

    trans = string.maketrans( chars, nums )

    file_raw = open( "temp_buffer_001", "r" )
    file_zi = open( "temp_buffer_002", "w" )
    file_ci = open( "temp_buffer_003", "w" )

    for line in file_raw.readlines() :
        line = line[:-1]
        line = line.split()

        code = "".join( line[3:] ).translate( trans )
        pinyin = "'".join( line[3:] )
        hanzi = line[0]
        freq = line[1]
        
        length = len( hanzi.decode( "utf-8" ) )
        if length <= 5 :
            print "insert", hanzi
            strings = [ code, pinyin, hanzi, freq ]
            if length > 1 :
                file_ci.write( "|".join( strings ) + "\n" )
            else :
                file_zi.write( "|".join( strings ) + "\n" )
        else :
            print "drop", hanzi

    file_raw.close()
    file_zi.close()
    file_ci.close()

if __name__ == "__main__" :
    phrase_raw()
