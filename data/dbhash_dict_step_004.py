#-!- coding=utf-8 -!-

import string
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

def create_code_map( db ) :
    code_set = set.union( set( db[0].keys() ), set( db[1].keys() ) )
    code_list = list( code_set )
    code_list.sort()
    code_map_entry = [ "0", False, [] ]
    
    count = [ 0, len( code_set ) ]
    for code in code_list :
        count[0] = count[0] + 1
        print "mapping", code, count[0], "/", count[1]

        node = code_map_entry
        code_length = len(code)
        end_flag = False
        for index in range( code_length ) :
            c = code[index]
            if index == code_length - 1 :
                end_flag = True
            map_index = node_find( node, c )
            if map_index < 0 :
                new_node = [ c, end_flag, [] ]
                node[2].append( new_node )
                node = new_node
            else:
                node = node[2][map_index]
                node[1] = end_flag or node[1]
    #while(1) :
        #time.sleep(5)
    #print code_map_entry
    time_stamp = time.time()
    byte_stream = dumps( code_map_entry )
    print "dumps cast", time.time() - time_stamp, "s"
    print "code map len =", len( byte_stream )
    time_stamp = time.time()
    code_map = loads( byte_stream )
    print "loads cast", time.time() - time_stamp, "s"
    db[2]["0"] = byte_stream
    #print code_map
        

def check_long( db ) :
    code_set = set( db[0].keys() )
    long_code_set = set()
    count = [ 0, len( code_set ) ]
    for code in code_set :
        count[0] = count[0] + 1
        print "checked long", code, count[0], "/", count[1]
        node = loads( db[0][code] )
        if len( node[1] ) > 200 :
            print "add", code
            long_code_set.add( code )
    print "long code count", len( long_code_set )
    byte_stream = dumps( long_code_set )
    db[2]["1"] = byte_stream

def phrase_incomplete_code( db ) :
    print "read code set"
    code_set = set.union( set( db[0].keys() ), set( db[1].keys() ) )
    print "read code list"
    code_list = list( code_set )
    print "sort code list"
    #code_list.sort( key = str.lower )
    code_list.sort()

    incomplete_code_dict = {}
    count = [ 0, len( code_list ) ]
    for code in code_list :
        index = 1
        flag = False
        while ( not flag ) and index < len( code ) :
            incomplete_code = code[:-index]
            index = index + 1
            if \
                    ( not incomplete_code_dict.has_key( incomplete_code ) ) \
                    and \
                    ( not ( incomplete_code in code_set ) ) \
                    :
                incomplete_code_dict[incomplete_code] = code
            else :
                if incomplete_code_dict.has_key( incomplete_code ) :
                    old_code = incomplete_code_dict[incomplete_code]
                    if len( code ) < len( old_code ) :
                        incomplete_code_dict[incomplete_code] = code
                        #print "update", old_code, "to", code
                    elif len( code ) == len( old_code ) and code < old_code :
                        incomplete_code_dict[incomplete_code] = code
                        #print "update", old_code, "to", code
                    else :
                        #print "keeped"
                        pass
        count[0] = count[0] + 1
        print "checked", code, count[0], "/", count[1]
    byte_stream = dumps( incomplete_code_dict )
    print "dumps done"
    db[2]["0"] = byte_stream
    print "write done"

def open_db() :
    db = []
    db.append( dbhash.open("dict.0", "r") )
    db.append( dbhash.open("dict.1", "r") )
    db.append( dbhash.open("dict.2", "w") )
    return db

def close_db( db ) :
    db[0].close()
    db[1].close()
    db[2].close()

if __name__ == "__main__" :
    db = open_db()
    #phrase_incomplete_code( db )
    check_long( db )
    create_code_map( db )
    close_db( db )
