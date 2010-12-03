#-!- coding=utf-8 -!-

from backend import Backend

class Interface() :
    CAND_LENGTH = 6
    def __init__( self ) :
        self.backend = Backend()
        self.code = ""
        self.invailed_code = ""
        self.selected = [ "", "", "" ]
        self.page_index = 0
        self.cand_list = []
    def append( self, code ) :
        self.code = self.code + code
        if len( self.invailed_code ) > 0 :
            self.invailed_code = self.invailed_code + code
        else :
            flag = self.backend.append( code )
            if not flag :
                self.invailed_code = self.invailed_code + code
            self.page_index = 0
    def pop( self ) :
        if len( self.code ) > 0 :
            self.code = self.code[:-1]
            if len( self.invailed_code ) > 0 :
                self.invailed_code = self.invailed_code[:-1]
            else :
                self.backend.pop()
                self.page_index = 0
        elif len( self.selected[0] ) > 0 :
            index = self.selected[1].rfind( "'" )
            if index < 0 :
                self.selected = [ "", "", "" ]
            else :
                code_length = len( self.selected[1] ) - index - 1
                self.selected[0] = self.selected[0][:-code_length]
                self.selected[1] = self.selected[1][:index]
                self.selected[2] = self.selected[2][:-1]
        
    def gen_cand( self ) :
        start_index = self.page_index * self.CAND_LENGTH
        pre_list = self.backend.get_cand( start_index, self.CAND_LENGTH )
        #print pre_list
        self.cand_list = []
        for index in pre_list :
            code, pinyin, hanzi, freq = self.backend.get_prop( index )
            self.cand_list.append( [ code, pinyin, hanzi.decode( "utf-8" ) ] )
    def commit( self ) :
        self.code = ""
        self.invailed_code = ""
        self.backend.reset()
        self.selected = [ "", "", "" ]
        self.gen_cand()
    def select( self, index ) :
        self.selected[0] = self.selected[0] + self.cand_list[index][0]
        self.selected[1] = self.selected[1] + self.cand_list[index][1]
        self.selected[2] = self.selected[2] + self.cand_list[index][2]
        
        index = self.CAND_LENGTH * self.page_index + index
        if index > 0 :
            self.backend.select( index )
        remained_code = self.invailed_code
        self.code = ""
        self.invailed_code = ""
        self.backend.reset()
        if len( remained_code ) > 0 :
            for code in remained_code :
                self.append( code )
        else :
            pass
            #self.query_cache = self.backend.query( self.code )
        self.gen_cand()
    def page_next( self ) :
        page_index = self.page_index + 1
        start_index = page_index * self.CAND_LENGTH
        cand_list = self.backend.get_cand( start_index, self.CAND_LENGTH )
        if len( cand_list ) > 0 :
            self.page_index = page_index
            self.gen_cand()
    def page_prev( self ) :
        if self.page_index > 0 :
            self.page_index = self.page_index - 1
            self.gen_cand()

