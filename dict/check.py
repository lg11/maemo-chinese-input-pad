#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash
import sys
import time

import sys
sys.path.append( '../' )

from codemap import CodeMap, get_data, set_data
from querycache import QueryCache

def open_dict_file() :
    time_stamp = time.time()
    dict_file = open( "dict.0", "r" )
    print "opend cast", time.time() - time_stamp, "s"
    
    time_stamp = time.time()
    byte_stream = dict_file.read()
    print "read cast", time.time() - time_stamp, "s"
    
    time_stamp = time.time()
    code_map_entry = loads( byte_stream )
    print "loads cast", time.time() - time_stamp, "s"

    return code_map_entry

def check( code_map_entry ) :
    code_map = CodeMap()
    code_map.entry = code_map_entry
    while( 1 ) :
        code = sys.stdin.readline()[:-1]
        flag = -1
        time_stamp = time.time()
        cache = QueryCache( code_map, code )
        print "query cast", time.time() - time_stamp, "s"
        if cache.vaild() :
            cand = cache.get_cand( 0, 6 )
            for index in range( len( cand ) ) :
                code, pinyin, hanzi, freq = cache.get_prop( index )
                print code, pinyin, hanzi, freq
        #print result[1][0][0][0], result[1][0][0][1][0][0]


if __name__ == "__main__" :
    code_map_entry = open_dict_file()
    check( code_map_entry )
