#-!- coding=utf-8 -!-

from marshal import dumps, loads
import dbhash

#import sys
#import time

def __node_find( node, code ) :
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

def node_find( node, code ) :
    code_length = len( code )
    code_index = 0
    vailed_flag = True
    while code_index < code_length and vailed_flag :
        c = code[code_index]
        seek_index = __node_find( node, c )
        if seek_index < 0 :
            vailed_flag = False
        else :
            node = node[2][seek_index]
            code_index = code_index + 1
    if not vailed_flag :
        return None
    else :
        return node

def node_seek( node, code ) :
    # A* ! ... A_Star seek...
    result = []
    node_list = [ node ]
    code_list = [ code ]
    node_stack = []
    code_stack = []
    while len( node_list ) > 0 and len( result ) < 1 :
        for i in range( len( node_list ) ) :
            node = node_list[i]
            code = code_list[i]
            if len( node[1] ) > 0 :
                #print "seeked"
                result.append( [ code, node[1] ] )
            else :
                if len( result ) < 1 :
                    for sub_node in node[2] :
                        node_stack.append( sub_node )
                        code_stack.append( code + sub_node[0] )
        node_list = node_stack
        code_list = code_stack
        node_stack = []
        code_stack = []

    return result
        
def code_map_query( code_map_entry, code ) :
    node = node_find( code_map_entry, code )
    if node == None :
        return []
    else :
        if len( node[1] ) < 1 :
            result = node_seek( node, code )
            return result
        else :
            return [ [ code, node[1] ] ]

def __query_result_get_highest_freq_phrase( query_result, index_list ) :
    highest_index = -1
    highest_freq = -1
    #print "check start"
    for index in range( len( query_result ) ) :
        result = query_result[index]
        code = result[0]
        pinyin = result[1]
        node_list = result[2]
        #print "check", index, code, pinyin
        node_index = index_list[index]
        if node_index < len( node_list ) :
            node = node_list[node_index]
            freq = node[1]
            if freq > highest_freq :
                highest_freq = freq
                highest_index = index
                #print highest_index
    if highest_index >= 0 :
        node_index = index_list[highest_index]
        index_list[highest_index] = node_index + 1
        return [ highest_index, node_index ]
    else :
        return None

def __cand_print_node( cand, index, node_index ) :
    query_result = cand[1]
    result = query_result[index]
    code = result[0]
    pinyin = result[1]
    node_list = result[2]
    node = node_list[node_index]
    hanzi = node[0]
    freq = node[1]
    print code, pinyin, hanzi, freq

def __cand_gen_node( cand, index, node_index ) :
    query_result = cand[1]
    result = query_result[index]
    code = result[0]
    pinyin = result[1]
    node_list = result[2]
    node = node_list[node_index]
    hanzi = node[0]
    freq = node[1]
    return [ pinyin, hanzi ]

def cand_gen( cand, request_length ) :
    cand_list = cand[0]
    query_result = cand[1]
    #for r in query_result :
        #print r[0], r[1]
    index_list = cand[2]
    cand_list_length = len( cand_list )
    if cand_list_length < request_length :
        index = 0
        flag = True
        while index < ( request_length - cand_list_length ) and flag :
            r = __query_result_get_highest_freq_phrase( query_result, index_list )
            if r == None :
                flag = False
            else :
                cand_list.append( r )
                #print "appended"
            index = index + 1
        cand_list_length = len( cand_list )

    return cand_list_length
                
def cand_get( cand, start_index, length ) :
    if length < 1 :
        length = 0
    cand_list_length = cand_gen( cand, start_index + length )
    #for r in cand_list :
        #__cand_print_node( cand, r[0], r[1] )
    r = []
    cand_list = cand[0]
    for i in range( start_index, start_index + length ) :
        if i < cand_list_length :
            node = cand_list[i]
            r.append( __cand_gen_node( cand, node[0], node[1] ) )
    return r

class Backend():
    def __init__( self ):
        dict_file = open( "data/dict.0", "r" )
        byte_stream = dict_file.read()
        dict_file.close()
        self.code_map_entry = loads( byte_stream )
        self.cand = [ [], [], [] ]

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
        result = code_map_query( self.code_map_entry, code )
        self.cand[0] = []
        self.cand[1] = []
        self.cand[2] = []
        for node in result :
            code = node[0]
            for pinyin_node in node[1] :
                pinyin = pinyin_node[0]
                node_list = pinyin_node[1]
                self.cand[1].append( [ code, pinyin, node_list ] )
                self.cand[2].append( 0 )
        #return result


    def get_cand( self, start_index, length ) :
        return cand_get( self.cand, start_index, length )

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
        query_cast = time.time() - time_stamp
        for node in backend.cand[1] :
            code = node[0]
            pinyin = node[1]
            node_list = node[2]
            for node in node_list :
                #print code, pinyin, node[0], node[1]
                pass

        time_stamp = time.time()
        result = backend.get_cand( 0, 6 )
        gen_cand_cast = time.time() - time_stamp
        for r in result :
            print r[0], r[1]
        print "query cast", query_cast, "second"
        print "gen cand cast", gen_cand_cast, "second"
