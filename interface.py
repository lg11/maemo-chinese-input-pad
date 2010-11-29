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
        self.query_cache = [ [], [], [] ]
    def append( self, code ) :
        self.code = self.code + code
        if len( self.invailed_code ) > 0 :
            self.invailed_code = self.invailed_code + code
        else :
            query_cache = self.backend.query( self.code )
            if len( query_cache[1] ) > 0 : 
                self.query_cache = query_cache
            else :
                self.invailed_code = self.invailed_code + code
    def backspace( self ) :
            if len( self.code ) > 0 :
                self.code = self.code[:-1]
                if len( self.invailed_code ) > 0 :
                    self.invailed_code = self.invailed_code[:-1]
            elif len( self.selected[0] ) > 0 :
                index = self.selected[1].rfind( "'" )
                #print self.selected[0], self.selected[1], self.selected[2]
                if index < 0 :
                    self.selected = [ "", "", "" ]
                else :
                    code_length = len( self.selected[1] ) - index - 1
                    self.selected[0] = self.selected[0][:-code_length]
                    self.selected[1] = self.selected[1][:index]
                    self.selected[2] = self.selected[2][:-1]
                #print self.selected[0], self.selected[1], self.selected[2]
            self.query_cache = self.backend.query( self.code )
    def gen_cand( self ) :
        start_index = self.page_index * self.CAND_LENGTH
        self.cand_list = self.backend.get_cand( self.query_cache, start_index, self.CAND_LENGTH )
    def select( self, index ) :
        self.selected[0] = self.selected[0] + self.cand_list[index][0]
        self.selected[1] = self.selected[1] + self.cand_list[index][1]
        self.selected[2] = self.selected[2] + self.cand_list[index][2]
        #print self.code, self.invailed_code
        remained_code = self.invailed_code
        self.code = ""
        self.invailed_code = ""
        if len( remained_code ) > 0 :
            for code in remained_code :
                self.append( code )
        else :
            self.query_cache = self.backend.query( self.code )
        self.gen_cand()

