#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash

#class Result():
    #def __init__( self, result ):


class Backend():
    def __init__( self ):
        self.cache = ( {}, {} )
        db_zi = dbhash.open( "data/db_zi", "w" )
        db_ci = dbhash.open( "data/db_ci", "w" )
        self.db = ( db_zi, db_ci )
        self.code_set = ( set( db_zi.keys() ), set( db_ci.keys() ) )

    def adjust( self, code, flag, index ):
        #print "code = ", code
        if index > 0:
            result = self.cache[flag][code]
            item = result[index]
            #print item[1]
            if index < 4 :
                new_index = 0
            else:
                new_index = index / 2
            result.pop(index)
            result.insert( new_index, item )
            self.cache[flag][code] = result
            self.db[flag][code] = dumps( result )
            return new_index
        else:
            return 0

    def close( self ):
        self.db[0].close()
        self.db[1].close()

    def query( self, code ):
        result = [ None, None ]

        item = None
        if code in self.code_set[0]:
            if code in self.cache[0].keys():
                item = self.cache[0][code]
            else:
                item = loads( self.db[0][code] )
                self.cache[0][code] = item
        result[0] = item

        item = None
        if code in self.code_set[1]:
            if code in self.cache[1].keys():
                item = self.cache[1][code]
            else:
                item = loads( self.db[1][code] )
                self.cache[1][code] = item
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



