#-!- coding=utf-8 -!-

from codemap import get_data

class Query() :
    """
    phrase code_map data
    to a easy use interface
    """
    def __init__( self, code_map, code ) :
        """
        init with a seek
        """
        self.vaild_flag = False
        #self.completed_flag = False
        if not ( code == "" ) :
            flag, result = code_map.power_seek( code )
            if result :
                self.vaild_flag = True
                self.completed_flag = flag
                self.cand = []
                self.filter = None
                self.cache = []
                self.index_list = []
                for item in result :
                    code = item[0]
                    node = item[1]
                    data = get_data( node )
                    for r in data :
                        self.cache.append( [ code, r ] )
                        self.index_list.append( 0 )
    def get_prop( self, cand_index ) :
        index = self.cand[cand_index][0]
        phrase_index = self.cand[cand_index][1]
        code = self.cache[index][0]
        pinyin = self.cache[index][1][0]
        hanzi = self.cache[index][1][1][phrase_index][0]
        freq = self.cache[index][1][1][phrase_index][1]
        return code, pinyin, hanzi, freq
    def __get_highest_freq_phrase( self ) :
        """
        select phrase has highest_freq in cache
        cache is sorted
        if filter has been set, only select pinyin == filter
        return index for cache and index for phrase
        return None if no phrase
        """
        highest_index = -1
        highest_freq = -1
        #print "check start"
        for cache_index in range( len( self.cache ) ) :
            cache = self.cache[cache_index]
            code = cache[0]
            pinyin = cache[1][0]
            phrase_list = cache[1][1]
            phrase_index = self.index_list[cache_index]
            #print "check", index, code, pinyin
            if phrase_index < len( phrase_list ) :
                phrase = phrase_list[phrase_index]
                freq = phrase[1]
                if self.filter :
                    if pinyin == self.filter :
                        highest_freq = freq
                        highest_index = cache_index
                elif freq > highest_freq :
                    highest_freq = freq
                    highest_index = cache_index
                    #print highest_index
        result = None
        if highest_index >= 0 :
            phrase_index = self.index_list[highest_index]
            self.index_list[highest_index] = phrase_index + 1
            result = [ highest_index, phrase_index ]
        return result
    def gen_cand( self, request_length ) :
        """
        gen cand_list to request_length
        will do nothing if request_length is too long
        """
        cand_length = len( self.cand )
        flag = True
        while cand_length < request_length and flag :
            result = self.__get_highest_freq_phrase()
            #print result
            if result :
                self.cand.append( result )
                cand_length = len( self.cand )
            else :
                flag = False
        return cand_length
    def vaild( self ) :
        """
        return is the cache vaild
        """
        return self.vaild_flag
    def completed( self ) :
        """
        return is the cache has a completed path
        """
        return self.vaild_flag and self.completed_flag

class QueryCache() :
    def __init__( self, code_map ) :
        """
        phrase mutli query_cache
        """
        self.code_map = code_map
        self.code = ""
        self.cache = []
        self.cache_index = -1
        self.cache_cand_index = 0
        self.cand = []
        self.filter = ""
    def append( self, code ) :
        """
        append a code
        will gen cache and put in to cache_stack if the code is vaild
        """
        code = self.code + code
        cache = Query( self.code_map, code )
        flag = cache.vaild()
        if flag :
            self.code = code
            self.cache.append( cache )
            self.cache_index = len( self.cache ) - 1
            self.cache_cand_index = 0
            self.cand = []
            self.filter = ""
        return flag
    def pop( self ) :
        """
        pop a code
        will pop cache from cache_stack
        """
        code = ""
        if len( self.code ) > 0 :
            code = self.code[-1]
            self.code = self.code[:-1]
            self.cache.pop()
            self.cache_index = len( self.cache ) - 1
            self.cache_cand_index = 0
            self.cand = []
            self.filter = ""
        return code
    def __clear( self ) :
        self.code = ""
        self.cache = []
        self.cache_index = -1
        self.cache_cand_index = 0
        self.cand = []
        self.filter = ""
    def set( self, code ) :
        """
        set code
        """
        self.__clear()
        for c in code :
            if not self.append( c ) :
                break
        #return code[ len( self.code ) : ]
        return self.code
    def get_prop( self, cand_index ) :
        """
        get node prot by self cand_list index
        return code, pinyin, hanzi, freq
        """
        cache_index = self.cand[cand_index][0]
        cache_cand_index = self.cand[cand_index][1]
        cache = self.cache[cache_index]
        return cache.get_prop( cache_cand_index )
    def gen_cand( self, request_length ) :
        """
        gen cand_list, include current query_cache
        and shooter but completed path cache
        will do nothing if request_length too long or too small
        """
        cand_length = 0
        if len( self.cache ) > 0 :
            cand_length = len( self.cand )
            if cand_length < request_length :
                if self.filter == "" :
                    #gen cand list without filter
                    cache_index = self.cache_index
                    flag = False
                    while cache_index >= 0 and ( not flag ) :
                        cache_cand_index = self.cache_cand_index
                        cache = self.cache[cache_index]
                        cache_request_length = cache_cand_index + request_length - cand_length #compute how many cand need gen
                        #print cache_request_length
                        new_cache_cand_index = cache.gen_cand( cache_request_length )
                        #print new_cache_cand_index, cache_request_length, cache_cand_index
                        if new_cache_cand_index > cache_request_length :
                            new_cache_cand_index = cache_request_length #maybe the cache has gen too long cand, cut it
                        for i in range( cache_cand_index, new_cache_cand_index ) :
                            #print i, cache_index
                            self.cand.append( [ cache_index, i ] )
                        self.cache_cand_index = new_cache_cand_index
                        cand_length = len( self.cand )
                        if cand_length < request_length :
                            #need more cand
                            while cache_index >= 0 :
                                cache_index = cache_index - 1
                                cache = self.cache[cache_index]
                                if cache.completed() :
                                    self.cache_index = cache_index
                                    self.cache_cand_index = 0
                                    break
                        else :
                            flag = True
                else :
                    #gen cand list with filter
                    pass
        return cand_length
    def select( self, cand_index ) :
        remained_code = ""
        cache_index = self.cand[cand_index][0]
        cache_cand_index = self.cand[cand_index][1]
        cache = self.cache[cache_index]
        code, hanzi, pinyin, freq = cache.get_prop( cache_cand_index )
        if len( self.code ) < len( code ) :
            code = self.code
        else :
            remained_code = self.code[ len( code ) : ]
        self.__clear()
        return remained_code, code, cache, cache_cand_index
