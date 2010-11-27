#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash
import sys
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

def code_map_find( code_map_entry, code ) :
    code_length = len( code )
    code_index = 0
    vailed_flag = True
    node = code_map_entry
    while code_index < code_length and vailed_flag :
        c = code[code_index]
        index = node_find( node, c )
        if index < 0 :
            vailed_flag = False
        else :
            node = node[2][index]
            code_index = code_index + 1
    if not vailed_flag :
        return [ code, [] ]
    elif len( node[1] ) > 0 :
        return [ code, node[1] ]
    else :
        # A* ! ... this is A_Star seek ...
        node_stack = [ node ]
        code_stack = [ code ]
        deeper_node_stack = []
        deeper_code_stack = []
        seeked_flag = False
        while len( node_stack ) > 0 and ( not seeked_flag ) :
            index = 0
            while index < len( node_stack ) and not seeked_flag :
                node = node_stack[index]
                new_code = code_stack[index]
                print new_code, node[0]
                if len( node[1] ) > 0 :
                    print "seeked"
                    seeked_flag = True
                else :
                    for sub_node in node[2] :
                        deeper_node_stack.append( sub_node )
                        deeper_code_stack.append( new_code + sub_node[0] )
                    index = index + 1
            node_stack = deeper_node_stack
            code_stack = deeper_code_stack
            deeper_node_stack = []
            deeper_code_stack = []
        if seeked_flag :
            return [ code, node[1] ]
        else :
            print "unknown error"

def check( code_map_entry ) :
    while( 1 ) :
        code = sys.stdin.readline()[:-1]
        flag = -1
        time_stamp = time.time()
        result = code_map_find( code_map_entry, code )
        print "query cast", time.time() - time_stamp, "s"
        print result[1][0][0][0], result[1][0][0][1][0][0]

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

if __name__ == "__main__" :
    code_map_entry = open_dict_file()
    check( code_map_entry )
