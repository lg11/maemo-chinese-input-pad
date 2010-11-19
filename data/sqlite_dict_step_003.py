#-!- coding=utf-8 -!-

import sqlite3
from marshal import dumps, loads

def create_table( cur ) :
    cur.execute( "create table marshal_dict_zi ( code int, byte_stream blob )" )
    cur.execute( "create table marshal_dict_ci ( code int, byte_stream blob )" )

def create_index( cur ) :
    cur.execute( "create index index_marshal_dict_zi on marshal_dict_zi ( code )" )
    cur.execute( "create index index_marshal_dict_ci on marshal_dict_ci ( code )" )


def phrase( cur, flag ) :
    result = []

    if flag > 0 :
        code_set = set( cur.execute( "select code from raw_dict_ci" ) )
        sql_sentence = "select pinyin, hanzi from raw_dict_ci where code = ? order by freq desc"
    else :
        code_set = set( cur.execute( "select code from raw_dict_zi" ) )
        sql_sentence = "select pinyin, hanzi from raw_dict_zi where code = ? order by freq desc"

    count = [ 0, len( code_set ) ]
    for code in code_set :
        count[0] = count[0] + 1
        rs = cur.execute( sql_sentence, code )
        print "dump", code[0], count[0], "/", count[1]
        byte_stream = sqlite3.Binary( dumps( list( rs ) ) )
        result.append( ( code[0], byte_stream,  ) )

    return result

def insert( cur, flag, result ) :
    if flag > 0 :
        sql_sentence = "insert into marshal_dict_ci values ( ?, ? )"
    else :
        sql_sentence = "insert into marshal_dict_zi values ( ?, ? )"

    count = [ 0, len( result ) ]
    for node in result :
        count[0] = count[0] + 1
        print "insert", node[0], count[0], "/", count[1]
        #print node[1]
        rs = cur.execute( sql_sentence, node )

def phrase_raw_dict() :
    conn = sqlite3.connect( "dict.db" )
    cur = conn.cursor()
    zi = phrase( cur, 0 )
    ci = phrase( cur, 1 )
    create_table( cur )
    insert( cur, 0, zi )
    insert( cur, 1, ci )
    create_index( cur )
    conn.commit()
    conn.close()

if __name__ == "__main__" :
    phrase_raw_dict()
