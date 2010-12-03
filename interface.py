#-!- coding=utf-8 -!-

from backend import Backend

class Interface() :
    CAND_LENGTH = 6
    def __init__( self ) :
        self.backend = Backend()
        self.invailed_code = ""
        self.page_index = 0
        self.cand_list = []
    def set_code( self, code ) :
        vaild_code = self.backend.set_code( code )
        self.invailed_code = code[ len( vaild_code ) : ]
        self.page_index = 0
    def append( self, code ) :
        if len( self.invailed_code ) > 0 :
            self.invailed_code = self.invailed_code + code
        else :
            flag = self.backend.append( code )
            if not flag :
                self.invailed_code = self.invailed_code + code
            self.page_index = 0
    def pop( self ) :
        if len( self.invailed_code ) > 0 :
            code = self.invailed_code[-1]
            self.invailed_code = self.invailed_code[:-1]
        else :
            code = self.backend.pop()
            self.page_index = 0
        return code
    def gen_cand( self ) :
        start_index = self.page_index * self.CAND_LENGTH
        pre_list = self.backend.get_cand( start_index, self.CAND_LENGTH )
        #print pre_list
        self.cand_list = []
        for index in pre_list :
            code, pinyin, hanzi, freq = self.backend.get_prop( index )
            self.cand_list.append( [ code, pinyin, hanzi.decode( "utf-8" ) ] )
    def commit( self ) :
        self.invailed_code = ""
        self.backend.commit()

        #self.gen_cand()
    def code( self ) :
        return self.backend.code + self.invailed_code
    def selected( self ) :
        return self.backend.get_selected().decode( "utf-8" )
    def deselect( self ) :
        code = self.backend.deselect()
        if len( code ) > 0 :
            print code, self.invailed_code
            code = code + self.invailed_code
            print code, self.invailed_code
            self.set_code( code )
            self.gen_cand()
        return code
    def select( self, index ) :
        index = self.CAND_LENGTH * self.page_index + index
        remained_code = self.backend.select( index )
        remained_code = remained_code + self.invailed_code
        self.set_code( remained_code )
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

