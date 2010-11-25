#-!- coding=utf-8 -!-

import sqlite3
from marshal import dumps, loads
import dbhash
import time

def node_find( node, code ) :
    index = 0
    flag = False
    while ( not flag ) and index < len( node[2] ) :
        sub_node = node[2][index]
        if sub_node[0] == code :
            flag = True
        else :
            index = index + 1
    if flag :
        return index
    else :
        return -1

def create_code_map( result ) :
    code_map_entry = [ "0", [], [] ]
    
    count = [ 0, len( result ) ]
    for r in result :
        code = r[0]
        node = code_map_entry
        for c in code :
            index = node_find( node, c )
            if index < 0 :
                new_node = [ c, [], [] ]
                node[2].append( new_node )
                node = new_node
            else:
                node = node[2][index]
        node[1].append( r[1] )
        count[0] = count[0] + 1
        print "mapping", code, count[0], "/", count[1]

    return code_map_entry

def commit( db, code_map_entry ) :
    #print code_map_entry
    time_stamp = time.time()
    byte_stream = dumps( code_map_entry )
    print "dumps cast", time.time() - time_stamp, "s"
    print "code map len =", len( byte_stream )
    time_stamp = time.time()
    code_map = loads( byte_stream )
    print "loads cast", time.time() - time_stamp, "s"
    db["0"] = byte_stream

def phrase( cur ) :
    result = []

    code_set = set( cur.execute( "select code from raw_dict" ) )
    sql_sentence = "select pinyin, hanzi, freq from raw_dict where code = ? order by freq desc"

    count = [ 0, len( code_set ) ]
    for code in code_set :
        rs = cur.execute( sql_sentence, code )
        code = code[0].encode( "utf-8" )
        
        pinyin_list = []
        for r in rs :
            pinyin =  r[0].encode( "utf-8" )
            hanzi = r[1].encode( "utf-8" )
            freq = r[2]
            index = 0
            flag = False
            node = [ hanzi, freq ]
            while ( not flag ) and index < len( pinyin_list ) :
                if pinyin == pinyin_list[index][0] :
                    flag = True
                else :
                    index = index + 1
            if flag :
                pinyin_list[index][1].append( node )
            else :
                pinyin_list.append( [ pinyin, [ node ] ] )
        result.append( [ code, pinyin_list ] )

        count[0] = count[0] + 1
        print "phrase", code, count[0], "/", count[1]

    return result

def create_db() :
    db = dbhash.open( "dict.0", "c" )
    return db

def close_db( db ) :
    time_stamp = time.time()
    db.close()
    print "close cast", time.time() - time_stamp, "s"

def phrase_raw_dict() :
    conn = sqlite3.connect( "temp_buffer_003" )
    cur = conn.cursor()
    result = phrase( cur )
    conn.close()

    code_map_entry = create_code_map( result )

    db = create_db()
    commit( db, code_map_entry )
    close_db( db )

if __name__ == "__main__" :
    phrase_raw_dict()
