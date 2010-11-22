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

def check( db ) :
    time_stamp = time.time()
    code_set = []
    code_set.append( db[0].keys() )
    code_set.append( db[1].keys() )
    code_set.append( loads( db[2]["0"] ) )
    print "ready"
    while( 1 ) :
        code = sys.stdin.readline()[:-1]
        flag = -1
        if code in code_set[0] :
            flag = 0
        elif code in code_set[1] :
            flag = 1
        elif code in code_set[2] :
            code = code_set[2][code]
            if code in code_set[0] :
                flag = 0
            elif code in code_set[1] :
                flag = 1
            else :
                "error"
        else :
            pass

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
