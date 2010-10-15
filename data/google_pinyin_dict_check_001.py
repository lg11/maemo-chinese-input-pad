#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash
import sys
import time

zi_db = dbhash.open("phrase", "w")
ci_db = dbhash.open("phrase", "w")
db = None

ci_code = set( ci_db.keys() )
zi_code = set( zi_db.keys() )

while( 1 ):
    code = sys.stdin.readline()[:-1]
    time_stamp = time.time()
    if code in zi_code:
        db = zi_db
    elif code in ci_code:
        db = ci_db
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
        print s[0][0], s[1][0]
        print s[0][len(s[0])-1], s[1][len(s[1])-1]
        i = len(s[0]) / 2
        p = i / 2
        py = s[0][i]
        hz = s[1][i]
        print "operate"
        print s[0][i], s[1][i]
        print s[0][p], s[1][p]
        time_stamp = time.time()
        s[0].pop(i)
        s[1].pop(i)
        print "pop cast", time.time() - time_stamp, "s"
        time_stamp = time.time()
        s[0].insert(p,py)
        s[1].insert(p,hz)
        print "insert cast", time.time() - time_stamp, "s"
        print s[0][i], s[1][i]
        print s[0][p], s[1][p]
        time_stamp = time.time()
        bs = dumps( s )
        print "dumps cast", time.time() - time_stamp, "s"
        time_stamp = time.time()
        db[code] = bs
        print "write cast", time.time() - time_stamp, "s"
