#-!- coding=utf-8 -!-

from querycache import QueryCache
from codemap import CodeMap

class SelectedStack() :
    def __init__( self ) :
        self.code_stack = []
        self.cache_stack = []
        self.cand_index_stack = []
    def push( self, code, cache, cand_index ) :
        self.code_stack.append( code )
        self.cache_stack.append( cache )
        self.cand_index_stack.append( cand_index )
    def pop( self ) :
        code = ""
        if len( self.code_stack ) > 0 :
            code = self.code_stack.pop()
            self.cache_stack.pop()
            self.cand_index_stack.pop()
        return code
    def get( self ) :
        code = ""
        pinyin = ""
        hanzi = ""
        for index in range( len( self.cache_stack ) ) :
            cache = self.cache_stack[index]
            cand_index = self.cand_index_stack[index]
            c, py, hz, freq = cache.get_prop( cand_index )
            code = code + c
            pinyin = pinyin + py
            hanzi = hanzi + hz
        return code, pinyin, hanzi
    def clear( self ) :
        self.code_stack = []
        self.cache_stack = []
        self.cand_index_stack = []

def __load_code_map( file_path ) :
    """
    load code map from a file
    """
    from marshal import loads
    file = open( file_path, "r" )
    byte_stream = file.read()
    file.close()
    entry = loads( byte_stream )
    code_map = CodeMap()
    code_map.entry = entry
    return code_map

load_code_map = __load_code_map

class Backend() :
    CAND_LENGTH = 6
    CODE_MAP_FILE_PATH = "/opt/mcip/dict/dict.0"
    CODE_MAP_FILE_PATH = "../dict/dict.0"
    def __init__( self ) :
        code_map = load_code_map( self.CODE_MAP_FILE_PATH )
        self.cache = QueryCache( code_map )
        self.invailed_code = ""
        self.page_index = 0
        self.cand_list = []
        self.selected = SelectedStack()
        self.get_pinyin_list = self.cache.get_pinyin_list
    def set_filter( self, pinyin ) :
        self.page_index = 0
        self.cache.set_filter( pinyin )
    def set_code( self, code ) :
        vaild_code = self.cache.set( code )
        self.invailed_code = code[ len( vaild_code ) : ]
        self.page_index = 0
    def append( self, code ) :
        if len( self.invailed_code ) > 0 :
            self.invailed_code = self.invailed_code + code
        else :
            flag = self.cache.append( code )
            if not flag :
                self.invailed_code = self.invailed_code + code
            self.page_index = 0
    def pop( self ) :
        if len( self.invailed_code ) > 0 :
            code = self.invailed_code[-1]
            self.invailed_code = self.invailed_code[:-1]
        else :
            code = self.cache.pop()
            self.page_index = 0
        return code
    def gen_cand_list( self ) :
        start_index = self.page_index * self.CAND_LENGTH
        request_length = start_index + self.CAND_LENGTH
        cand_length = self.cache.gen_cand( request_length )
        #print self.code(), "cand_length", cand_length
        self.cand_list = []
        if request_length < cand_length :
            cand_length = request_length
        if start_index < cand_length :
            for index in range( start_index, cand_length ) :
                #print self.code(), "index", index
                code, pinyin, hanzi, freq = self.cache.get_prop( index )
                self.cand_list.append( [ code, pinyin, hanzi.decode( "utf-8" ) ] )
    def commit( self ) :
        self.invailed_code = ""
        self.cache.set("")
        self.selected.clear()
    def code( self ) :
        return self.cache.code + self.invailed_code
    def get_selected( self ) :
        code, pinyin, hanzi = self.selected.get()
        return hanzi.decode( "utf-8" )
    def deselect( self ) :
        code = self.selected.pop()
        if len( code ) > 0 :
            #print code, self.code()
            code = code + self.code()
            self.set_code( code )
        return code
    def select( self, index ) :
        index = self.CAND_LENGTH * self.page_index + index
        remained_code, code, cache, cand_index = self.cache.select( index )
        self.selected.push( code, cache, cand_index )
        remained_code = remained_code + self.invailed_code
        self.set_code( remained_code )
    def page_next( self ) :
        page_index = self.page_index + 1
        start_index = page_index * self.CAND_LENGTH
        cand_length = self.cache.gen_cand( start_index + self.CAND_LENGTH )
        if cand_length > start_index :
            self.page_index = page_index
    def page_prev( self ) :
        if self.page_index > 0 :
            self.page_index = self.page_index - 1

