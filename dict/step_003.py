#-!- coding=utf-8 -!-

import sqlite3
from marshal import dumps, loads
import dbhash
import time

import sys
sys.path.append( '../' )

from codemap import CodeMap, get_data, set_data

def create_code_map( result ) :

    code_map = CodeMap()
    
    count = [ 0, len( result ) ]
    for r in result :
        code = r[0]
        node = code_map.add_path( code )
        l = get_data( node )
        if l :
            l.extend( r[1] )
        else :
            l = []
            l.extend( r[1] )
            set_data( node, l )
        count[0] = count[0] + 1
        print "mapping", code, count[0], "/", count[1]

    return code_map

def phrase( cur ) :
    result = []

    code_set = set( cur.execute( "select code from raw_dict" ) )
    sql_sentence = "select pinyin, hanzi, freq from raw_dict where code = ? order by freq desc"

    count = [ 0, len( code_set ) ]
    for code in code_set :
    #code_list = list( code_set )
    #for i in range( len( code_list ) / 20 ) :
        #code = code_list[i]
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

def commit( dict_file, code_map_entry ) :
    #print code_map_entry
    time_stamp = time.time()
    byte_stream = dumps( code_map_entry )
    print "dumps cast", time.time() - time_stamp, "s"
    print "code map len =", len( byte_stream )
    time_stamp = time.time()
    code_map = loads( byte_stream )
    print "loads cast", time.time() - time_stamp, "s"
    time_stamp = time.time()
    dict_file.write( byte_stream )
    print "write cast", time.time() - time_stamp, "s"

def open_dict_file() :
    dict_file = open( "dict.0", "w" )
    return dict_file

def close_dict_file( dict_file ) :
    time_stamp = time.time()
    dict_file.close()
    print "close cast", time.time() - time_stamp, "s"

def phrase_raw_dict() :
    conn = sqlite3.connect( "cache/db" )
    cur = conn.cursor()
    result = phrase( cur )
    conn.close()

    code_map = create_code_map( result )
    #print code_map.entry

    dict_file = open_dict_file()
    commit( dict_file, code_map.entry )
    close_dict_file( dict_file )

if __name__ == "__main__" :
    phrase_raw_dict()
