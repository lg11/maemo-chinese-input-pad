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
        if not "0" in self.code_set[1] :
            #print "need create temp phrase list"
            self.temp_phrase_list = []
            self.db[1]["0"] = dumps( self.temp_phrase_list )
        else :
            #print "load temp phrase list"
            self.temp_phrase_list = loads( self.db[1]["0"] )

    def adjust( self, code, flag, index ):
        #print "code = ", code
        result = self.cache[flag][code]
        item = result[index]
        if flag > 0 and len( item ) > 2 :
            #print item
            item[2] = item[2] * 3
            #print item
            if item[2] > 100 :
                temp_index = 0
                seek_flag = False
                while ( not seek_flag ) and temp_index < len( self.temp_phrase_list ) :
                    #print temp_index
                    node = self.temp_phrase_list[ temp_index ]
                    if code == node[0] and item[0] == node[1] and item[1] == node[2] :
                        seek_flag = True
                    else :
                        temp_index = temp_index + 1
                #print temp_index
                self.temp_phrase_list.pop( temp_index )
                self.db[1]["0"] = dumps( self.temp_phrase_list )
                item.pop(2)
                #print node
            result[index] = item
            self.cache[flag][code] = result
            self.db[flag][code] = dumps( result )
        if index > 0:
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

    def insert( self, code, pinyin, hanzi ):
        #print code, pinyin, hanzi
        phrase_length = pinyin.count("'")
        if phrase_length > 0 and phrase_length < 5 :
            if code in self.code_set[1]:
                if code in self.cache[1].keys():
                    item = self.cache[1][code]
                else :
                    item = loads( self.db[1][code] )
                    self.cache[1][code] = item
                flag = False
                index = 0
                while ( not flag ) and index < len( item ) :
                    node = item[index]
                    #print node[0], node[1]
                    if node[0] == pinyin and node[1] == hanzi :
                        flag = True
                    else :
                        index = index + 1
                if flag :
                    #print "phrase existed"
                    pass
                else :
                    #print "new phrase"
                    node = [ pinyin, hanzi, 8 ]
                    if len( item ) < 3 :
                        item.append( node )
                    else:
                        item.insert( 2, node )
                    self.cache[1][code] = item
                    self.db[1][code] = dumps( item )
                    node = [ code, pinyin, hanzi ]
                    self.temp_phrase_list.append( node )
            else :
                #new code
                #print "new code"
                self.code_set[1].add( code )
                node = [ pinyin, hanzi, 8 ]
                item = [ node ]
                self.cache[1][code] = item
                self.db[1][code] = dumps( item )
                node = [ code, pinyin, hanzi ]
                self.temp_phrase_list.append( node )
        else:
            #print "not insert"
            pass
    
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

    def close( self ):
        remove_phrase = []
        for temp_index in range( len( self.temp_phrase_list ) ) :
            node = self.temp_phrase_list[temp_index]
            code = node[0]
            pinyin = node[1]
            hanzi = node[2]
            #print code, pinyin, hanzi
            if code in self.cache[1].keys() :
                item = self.cache[1][code]
            else :
                item = loads( self.db[1][code] )
            flag = False
            index = 0
            while ( not flag ) and index < len( item ) :
                node = item[index]
                #print node[0], node[1]
                if node[0] == pinyin and node[1] == hanzi :
                    flag = True
                else :
                    index = index + 1
            node = item[index]
            print node[0], node[1], node[2]
            if node[2] > 0 :
                print "reduce temp phrase prop"
                if node[2] > 50 :
                    node[2] = node[2] - 20
                elif node[2] > 25 :
                    node[2] = node[2] - 10
                elif node[2] > 10 :
                    node[2] = node[2] - 6
                elif node[2] > 5 :
                    node[2] = node[2] - 3
                else :
                    node[2] = node[2] - 1
                item[index] = node
                if code in self.cache[1].keys() :
                    self.cache[1][code] = item
                self.db[1][code] = dumps( item )
            else :
                print "remove temp phrase"
                remove_phrase.append( self.temp_phrase_list[temp_index] )
                item.pop( index )
                if len( item ) > 1 :
                    if code in self.cache[1].keys() :
                        self.cache[1][code] = item
                    self.db[1][code] = dumps( item )
                else :
                    if code in self.cache[1].keys() :
                        self.cache[1].pop( code )
                    self.db[1].pop( code )

        for phrase in remove_phrase :
            self.temp_phrase_list.remove( phrase )
        self.db[1]["0"] = dumps( self.temp_phrase_list )
        self.cache = ( {}, {} )
        self.db[1]["0"] = dumps( self.temp_phrase_list )
        self.db[0].close()
        self.db[1].close()



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



