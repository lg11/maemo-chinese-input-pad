#-!- coding=utf-8 -!-

from codemap import get_data

class QueryCache() :
    """
    phrase code_map data
    to a easy use interface
    """
    def __init__( self, code_map, code ):
        """
        init with a seek
        """
        self.vaild_flag = False
        if not ( code == "" ) :
            flag, result = code_map.power_seek( code )
            if result :
                self.vaild_flag = True
                self.completed_flag = flag
                self.cand_list = []
                self.filter = None
                self.pre_list = []
                self.index_list = []
                for item in result :
                    code = item[0]
                    node = item[1]
                    data = get_data( node )
                    for r in data :
                        self.pre_list.append( [ code, r ] )
                        self.index_list.append( 0 )

    def __len__( self ) :
        """
        get length of all query_result
        """
        length = 0
        if self.vaild_flag :
            for item in self.pre_list :
                length = length + len( item[1][1] )
        return length

    def get_prop( self, cand_index ) :
        index = self.cand_list[cand_index][0]
        phrase_index = self.cand_list[cand_index][1]
        code = self.pre_list[index][0]
        pinyin = self.pre_list[index][1][0]
        hanzi = self.pre_list[index][1][1][phrase_index][0]
        freq = self.pre_list[index][1][1][phrase_index][1]
        return code, pinyin, hanzi, freq

    def __get_highest_freq_phrase( self ) :
        """
        select phrase has highest_freq in pre_list
        pre_list is sorted
        if filter has been set, only select pinyin == filter
        return index for pre_list and index for phrase
        return None if no phrase
        """
        highest_index = -1
        highest_freq = -1
        #print "check start"
        for index in range( len( self.pre_list ) ) :
            result = self.pre_list[index]
            code = result[0]
            pinyin = result[1][0]
            phrase_list = result[1][1]
            phrase_index = self.index_list[index]
            #print "check", index, code, pinyin
            if phrase_index < len( phrase_list ) :
                phrase = phrase_list[phrase_index]
                freq = phrase[1]
                if self.filter :
                    if pinyin == self.filter :
                        highest_freq = freq
                        highest_index = index
                elif freq > highest_freq :
                    highest_freq = freq
                    highest_index = index
                    #print highest_index
        result = None
        if highest_index >= 0 :
            phrase_index = self.index_list[highest_index]
            self.index_list[highest_index] = phrase_index + 1
            result = [ highest_index, phrase_index ]
        return result

    def gen_cand_list( self, request_length ) :
        """
        gen cand_list to request_length
        will do nothing if request_length is too long
        """
        cand_list_length = len( self.cand_list )
        flag = True
        while cand_list_length < request_length and flag :
            result = self.__get_highest_freq_phrase()
            #print result
            if result :
                self.cand_list.append( result )
                cand_list_length = len( self.cand_list )
            else :
                flag = False
        return cand_list_length

    def vaild( self ):
        """
        return is the cache vaild
        """
        return self.vaild_flag

    def completed( self ):
        """
        return is the cache has a completed path
        """
        return self.vaild_flag and self.completed_flag

