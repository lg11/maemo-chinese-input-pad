#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash

#class Result():
    #def __init__( self, result ):


class Backend():
    def __init__( self ):
        self.cache_zi = {}
        self.cache_ci = {}
        self.db_zi = dbhash.open( "data/db_zi", "w" )
        self.db_ci = dbhash.open( "data/db_ci", "w" )
        self.code_set_zi = set( self.db_zi.keys() )
        self.code_set_ci = set( self.db_ci.keys() )

    def query( self, code ):
        result = [ None, None ]

        item = None
        if code in self.code_set_zi:
            if code in self.cache_zi.keys():
                item = self.cache_zi[code]
            else:
                item = loads( self.db_zi[code] )
                self.cache_zi[code] = item
        result[0] = item

        item = None
        if code in self.code_set_ci:
            if code in self.cache_ci.keys():
                item = self.cache_ci[code]
            else:
                item = loads( self.db_ci[code] )
                self.cache_ci[code] = item
        result[1] = item

        return result


if __name__ == "__main__" :
    import sys
    import time
    backend = Backend()
    #print "backend created"
    while True :
        code = sys.stdin.readline()[:-1]
        time_stamp = time.time()
        result = backend.query( code )
        print "query cast", time.time() - time_stamp, "second"
        print result



