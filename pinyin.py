#-!- coding=utf-8 -!-

import sqlite3
code = []
code.append("")
code.append("")
code.append("abc")
code.append("def")
code.append("ghi")
code.append("jkl")
code.append("mno")
code.append("pqrs")
code.append("tuv")
code.append("wxyz")

def get_code_set():
    """获取编码集合"""
    file = open( "data/code" )
    buffer = file.readlines()
    lines = []
    for line in buffer:
        lines.append( line[:-1] )
    code_set = set( lines )
    return code_set

def get_ucode_set():
    """获取不完整编码集合"""
    file = open( "data/code_un" )
    buffer = file.readlines()
    lines = []
    for line in buffer:
        lines.append( line[:-1] )
    ucode_set = set( lines )
    return ucode_set

class Cand():
    def __init__( self, buffer ):
        self.list = []
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.page_index = 0
        self.query_index = 0
        self.buffer = buffer
    def update(self):
        i = len( self.buffer.buffer )
        rs = self.buffer.query[i]
        while rs == None and i > 0 :
            i = i - 1
            rs = self.buffer.query[i]
        self.query_index = i
        if rs:
            if self.page_index * 6 >= len( rs ):
                self.list[0] = None
                self.list[1] = None
                self.list[2] = None
                self.list[3] = None
                self.list[4] = None
                self.list[5] = None
            else:
                for i in range(6):
                    idx = self.page_index * 6 + i
                    if idx < len(rs):
                        self.list[i] = rs[ idx ]
                    else:
                        self.list[i] = None
        else:
            self.list[0] = None
            self.list[1] = None
            self.list[2] = None
            self.list[3] = None
            self.list[4] = None
            self.list[5] = None
    def next_page(self):
        rs = self.buffer.query[self.query_index]
        idx = self.page_index + 1
        if idx * 6 >= len( rs ):
            pass
        else:
            self.page_index = idx
            self.update()
    def prev_page(self):
        idx = self.page_index - 1
        if idx >= 0:
            self.page_index = idx
            self.update()
    def reset(self):
        #self.list[0] = None
        #self.list[1] = None
        #self.list[2] = None
        #self.list[3] = None
        #self.list[4] = None
        #self.list[5] = None
        self.page_index = 0
        #self.query_index = 0

class Buffer():
    code_set = get_code_set()
    ucode_set = get_ucode_set()

    codes = set( ["2","3","4","5","6","7","8","9"] )

    def __init__(self):
        self.buffer = ""
        self.conn = sqlite3.connect( "data/main.db" )
        self.cur = self.conn.cursor()
        self.sql_qb = []
        self.query = []
        self.cand = Cand(self)
        for i in range(65):
            self.query.append(None)
            s = "select pinyin,hanzi,freq from pc_" + str(i) + " where code=? order by freq desc"
            self.sql_qb.append( s )

    def append( self, code ):
        if code in self.codes:
            self.buffer = self.buffer + code

    def backspace(self):
        if len(self.buffer) > 0:
            self.buffer = self.buffer[:-1]

    def reset(self):
        self.buffer = ""
        self.cand.reset()
    def search(self):
        t = ( self.buffer, )
        i = len( self.buffer )
        rs = self.cur.execute( self.sql_qb[i], t )
        rl = []
        for r in rs :
            rl.append(r)
        if len(rl) > 0:
            self.query[i] = rl
        else:
            self.query[i] = None
        #self.cand.update()
        #for r in self.cand.list:
            #print r

