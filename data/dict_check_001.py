#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash
import sys
import time

db_zi = dbhash.open("db_zi", "w")
db_ci = dbhash.open("db_ci", "w")
db = None

ci_code = set( db_ci.keys() )
zi_code = set( db_zi.keys() )

while( 1 ):
    code = sys.stdin.readline()[:-1]
    time_stamp = time.time()
    if code in zi_code:
        db = db_zi
    elif code in ci_code:
        db = db_ci
    else:
        db = None

    if db == None:
        print "invailed code"
    else:
        bs = db[code]
        print "query cast", time.time() - time_stamp, "s"
        time_stamp = time.time()
        s = loads( bs )
        print "loads cast", time.time() - time_stamp, "s"
        print s[0][0], s[0][1]
        print s[-1][0], s[-1][1]
        i = len(s) / 2
        p = i / 2
        r = s[i]
        print "operate"
        print s[i][0], s[i][1]
        print s[p][0], s[p][1]
        time_stamp = time.time()
        s.pop(i)
        print "pop cast", time.time() - time_stamp, "s"
        time_stamp = time.time()
        s.insert(p,r)
        print "insert cast", time.time() - time_stamp, "s"
        print s[i][0], s[i][1]
        print s[p][0], s[p][1]
        time_stamp = time.time()
        bs = dumps( s )
        print "dumps cast", time.time() - time_stamp, "s"
        time_stamp = time.time()
        db[code] = bs
        print "write cast", time.time() - time_stamp, "s"
