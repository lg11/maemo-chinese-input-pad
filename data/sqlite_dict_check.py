#-!- coding=utf-8 -!-

import sqlite3
from marshal import dumps, loads

if __name__ == "__main__" :
    import sys
    import time
    conn = sqlite3.connect( "dict.db" )
    cur = conn.cursor()

    code_set = []

    rs = cur.execute( "select code from marshal_dict_zi" )
    s = set()
    for node in rs :
        s.add( node[0] )
    code_set.append( s )

    rs = cur.execute( "select code from marshal_dict_ci" )
    s = set()
    for node in rs :
        s.add( node[0] )
    code_set.append( s )

    #print code_set

    sql_sentence = []
    sql_sentence.append( "select byte_stream from marshal_dict_zi where code = ?" )
    sql_sentence.append( "select byte_stream from marshal_dict_ci where code = ?" )

    while( 1 ):
        print "input code :"
        code = int( sys.stdin.readline()[:-1] )
        time_stamp = time.time()
        if code in code_set[0] :
            rs = list( cur.execute( sql_sentence[0], ( code, ) ) )
        elif code in code_set[1] :
            rs = list( cur.execute( sql_sentence[1], ( code, ) ) )
        else :
            rs = []
        if len( rs ) > 0 :
            result = loads( str( rs[0][0] ) ) 
            for node in result :
                pinyin = node[0]
                hanzi = node[1]
                #print pinyin, hanzi
        elif len( rs ) > 1 :
            print "unknown error"
        else :
            print "invail code"

        print "query cast", time.time() - time_stamp, "s"
