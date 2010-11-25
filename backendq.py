#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash

#import sys
#import time

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

def code_map_check( code_map_entry, code ) :
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

class Backend():
    def __init__( self ):
        self.db = []
        self.db.append( dbhash.open( "data/dict.0", "w" ) )
        self.db.append( dbhash.open( "data/dict.1", "w" ) )
        self.db.append( dbhash.open( "data/dict.2", "w" ) )

        self.cache = ( ( {}, set() ), ( {}, set() ) )
        self.code_set = ( set( self.db[0].keys() ), set( self.db[1].keys() ) )
        self.code_map_entry = loads( self.db[2]["0"] )

        preload_code_set = loads( self.db[2]["1"] )
        for code in preload_code_set :
            self.cache[0][0][code] = loads( self.db[0][code] )

    def adjust( self, code, flag, index ):
        #print "code = ", code
        result = self.cache[flag][code]
        item = result[index]
        if flag > 0 and len( item ) > 2 :
            #print item
            item[2] = ( item[2] + 1 ) * 3
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
        def __query( flag, code ):
            item = []
            if code in self.code_set[flag]:
                if self.cache[flag][0].has_key( code ):
                    item = self.cache[flag][0][code]
                else:
                    item = loads( self.db[flag][code] )
                    self.cache[flag][0][code] = item
            return item

        result = [ __query( 0, code ), __query( 1, code ) ]

        if len( result[0] ) <= 0 and len( result[1] ) <= 0 :
            code = code_map_check( self.code_map_entry, code )
            if len( code ) > 0 :
                result = [ __query( 0, code ), __query( 1, code ) ]

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
    print "backend created"
    while True :
        code = sys.stdin.readline()[:-1]
        time_stamp = time.time()
        result = backend.query( code )
        time_stamp = time.time() - time_stamp
        if len( result[0] ) > 0 :
            print "result count", len( result[0][1] )
            for node in result[0][1] :
                print node[0], node[1]
                pass
        if len( result[1] ) > 0 :
            print "result count", len( result[1][1] )
            for node in result[1][1] :
                print node[0], node[1]
                pass
        print "query cast", time_stamp, "second"

