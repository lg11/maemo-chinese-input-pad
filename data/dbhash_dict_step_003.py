#-!- coding=utf-8 -!-

import sqlite3
from marshal import dumps, loads
import dbhash

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
        byte_stream = dumps( list( rs ) )
        result.append( ( code[0], byte_stream,  ) )

    return result

def insert( db, flag, result ) :
    db = db[flag]

    count = [ 0, len( result ) ]
    for node in result :
        count[0] = count[0] + 1
        print "insert", node[0], count[0], "/", count[1]
        
        code = node[0]
        byte_stream = node[1]
        
        db[ str( code ) ] = byte_stream


def create_db() :
    db = []
    db.append( dbhash.open("dict.zi", "c") )
    db.append( dbhash.open("dict.ci", "c") )
    db.append( dbhash.open("dict.misc", "c") )
    return db

def close_db( db ) :
    db[0].close()
    db[1].close()
    db[2].close()

def phrase_raw_dict() :
    conn = sqlite3.connect( "dict.db" )
    cur = conn.cursor()
    zi = phrase( cur, 0 )
    ci = phrase( cur, 1 )
    conn.close()

    db = create_db()
    insert( db, 0, zi )
    insert( db, 1, ci )
    close_db( db )

if __name__ == "__main__" :
    phrase_raw_dict()
