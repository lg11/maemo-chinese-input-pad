#-!- coding=utf-8 -!-

import string
from marshal import dumps, loads
import dbhash
import time

def phrase_incomplete_code( db ) :
    print "read code set"
    code_set = set.union( set( db[0].keys() ), set( db[1].keys() ) )
    print "read code list"
    code_list = list( code_set )
    print "sort code list"
    #code_list.sort( key = str.lower )
    code_list.sort()

    incomplete_code_set = set()
    incomplete_code_dict = {}
    count = [ 0, len( code_list ) ]
    for code in code_list :
        index = 1
        flag = False
        while ( not flag ) and index < len( code ) :
            incomplete_code = code[:-index]
            index = index + 1
            if \
                    ( not ( incomplete_code in incomplete_code_set ) ) \
                    and \
                    ( not ( incomplete_code in code_set ) ) \
                    :
                incomplete_code_set.add( incomplete_code )
                incomplete_code_dict[incomplete_code] = code
            else :
                if incomplete_code in incomplete_code_set :
                    old_code = incomplete_code_dict[incomplete_code]
                    print "check code :", old_code, code
                    if len( code ) < len( old_code ) :
                        incomplete_code_dict[incomplete_code] = code
                        print "update", old_code, "to", code
                    elif len( code ) == len( old_code ) and code < old_code :
                        incomplete_code_dict[incomplete_code] = code
                        print "update", old_code, "to", code
                    else :
                        print "keeped"
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
    phrase_incomplete_code( db )
    close_db( db )
