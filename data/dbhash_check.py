#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash
import sys
import time

def opendb() :
    time_stamp = time.time()
    db = []
    db.append( dbhash.open("dict.0", "w") )
    db.append( dbhash.open("dict.1", "w") )
    db.append( dbhash.open("dict.2", "w") )
    print "opend cast", time.time() - time_stamp, "s"
    return db

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

def check_code_map( code, code_map_entry ) :
    code_length = len( code )
    index = 0
    new_code = ""
    vail_flag = True
    node = code_map_entry
    while index < code_length and vail_flag :
        c = code[index]
        map_index = node_find( node, c )
        if map_index < 0 :
            vail_flag = False
        else :
            new_code = new_code + c
            node = node[2][map_index]
            index = index + 1
    if not vail_flag :
        print "invail"
        return ""
    else :
        # A* ! ... A_Star seek...
        node_stack = [ node ]
        code_stack = [ new_code ]
        deeper_node_stack = []
        deeper_code_stack = []
        flag = False
        while len( node_stack ) > 0 and not flag :
            index = 0
            while index < len( node_stack ) and not flag :
                node = node_stack[index]
                new_code = code_stack[index]
                print new_code, node[0]
                end_flag = node[1]
                if end_flag :
                    print "seeked"
                    flag = True
                else :
                    for sub_node in node[2] :
                        deeper_node_stack.append( sub_node )
                        deeper_code_stack.append( new_code + sub_node[0] )
                    index = index + 1
            node_stack = deeper_node_stack
            code_stack = deeper_code_stack
            deeper_node_stack = []
            deeper_code_stack = []
        return new_code

def check( db ) :
    time_stamp = time.time()
    code_set = []
    code_set.append( db[0].keys() )
    code_set.append( db[1].keys() )
    code_map_entry = loads( db[2]["0"] )
    print "ready"
    while( 1 ) :
        code = sys.stdin.readline()[:-1]
        flag = -1
        if code in code_set[0] :
            flag = 0
        elif code in code_set[1] :
            flag = 1
        else :
            code = check_code_map( code, code_map_entry )
            if len( code ) > 0 :
                if code in code_set[0] :
                    flag = 0
                elif code in code_set[1] :
                    flag = 1
                else :
                    "error"
            else :
                "error"

        if flag < 0 :
            print "invailed code"
        else:
            time_stamp = time.time()
            bs = db[flag][code]
            print "query cast", time.time() - time_stamp, "s"
            time_stamp = time.time()
            s = loads( bs )
            print "loads cast", time.time() - time_stamp, "s"
            print s[1][0][0], s[1][0][1]
            #for node in s[1] :
                #print node[0], node[1]

if __name__ == "__main__" :
    db = opendb()
    check( db )
