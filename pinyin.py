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

