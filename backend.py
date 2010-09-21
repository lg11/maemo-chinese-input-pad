#-!- coding=utf-8 -!-

import sqlite3
import threading
import Queue

import time

class QueryCache():
    """
    查询缓存
    """
    FLAG_INVAILD = 0
    FLAG_IN_QUERY = 1
    FLAG_VAILD = 2
    IDX_KEY = 0
    IDX_CODE = 1
    IDX_PINYIN = 2
    IDX_HANZI = 3
    IDX_FREQ = 4
    IDX_LENGTH = 5
    def __init__(self):
        """
        初始化
        @cache 缓存列表
        @flag 标志
        """
        self.list = []
        #self.hanzi_list = []
        self.flag = [] 
        #self.hanzi_list = []
        for i in range(65):
            self.list.append(None)
            #self.hanzi_list.append(None)
            self.flag.append(self.FLAG_INVAILD)
    def reset(self):
        """
        重置整个缓存
        """
        for i in range(65):
            self.flag[i] = self.FLAG_INVAILD

class OperateThread( threading.Thread ):
    OPERATE_REQUEST_INSERT = 1
    OPERATE_REQUEST_DELETE = 2
    OPERATE_REQUEST_UPDATE = 3
    def __init__( self, queue ):
        threading.Thread.__init__(self)
        self.conn = None
        self.cur = None
        self.queue = queue
        self.sql_sentence_update = []
        self.sql_sentence_insert = []
        self.sql_sentence_insert_query = []
        self.sql_sentence_insert_count = []
        self.sql_sentence_delete = []
        for i in range(65):
            self.sql_sentence_update.append([])
            self.sql_sentence_insert.append([])
            self.sql_sentence_insert_query.append([])
            self.sql_sentence_insert_count.append([])
            self.sql_sentence_delete.append([])
            for j in range(10):
                s = "update phrase_" + str(i) + "_" + str(j) + " set freq = ( ( select freq from phrase_" + str(i) + "_" + str(j) + " where key = ? ) + 1 ) where key= ?"
                self.sql_sentence_update[i].append(s)
                s = "insert into phrase_" + str(i) + "_" + str(j) + " values ( NULL, ?, ?, ?, ?, ? )"
                self.sql_sentence_insert[i].append(s)
                s = "select * from phrase_" + str(i) + "_" + str(j) + " where code = ? and hanzi = ?"
                self.sql_sentence_insert_count[i].append(s)
                s = "select * from phrase_" + str(i) + "_" + str(j) + " where code = ? order by freq desc"
                self.sql_sentence_insert_query[i].append(s)
                s = "delete from phrase_" + str(i) + "_" + str(j) + " where key = ?"
                self.sql_sentence_delete[i].append(s)
                #print s
    def run(self):
        """
        线程实际运行时，执行的函数。由于sqlite的连接不能跨线程，所以在这里打开连接。
        """
        self.conn = sqlite3.connect( "data/main.db" )
        self.cur = self.conn.cursor()
        self.cur.execute( "select * from phrase_0_0" )#first query has delay, due it.
        while(True):
            data = self.queue.get()
            time_stamp = time.time()
            request = data[0]
            if request == self.OPERATE_REQUEST_UPDATE :
                i = data[1]
                j = data[2]
                update_key = data[3]
                pos_key = data[4]
                t = ( pos_key, update_key , )
                rs = self.cur.execute( self.sql_sentence_update[i][j], t )
                self.conn.commit()
                print "update cast " + str( time.time() - time_stamp ) + " s"
            elif request == self.OPERATE_REQUEST_INSERT :
                code = data[1]
                pinyin = data[2]
                hanzi = data[3]
                length = data[4]
                freq = 0
                i = len(code)
                j = int(code[0])
                t = ( code, )
                rs = self.cur.execute( self.sql_sentence_insert_query[i][j], t )
                r = rs.fetchone()
                if r == None :
                    #print "no code"
                    t = ( code, pinyin, hanzi, 1, length )
                    self.cur.execute( self.sql_sentence_insert[i][j], t )
                else:
                    t = ( code, hanzi, )
                    rs2 = self.cur.execute( self.sql_sentence_insert_count[i][j], t )
                    r2 = rs.fetchone()
                    if r2 == None :
                        #print "no ci"
                        freq = r[ QueryCache.IDX_FREQ ] - 1
                        r = rs.fetchone()
                        if r != None :
                            freq = r[ QueryCache.IDX_FREQ ] - 1
                            r = rs.fetchone()
                            if r != None :
                                freq = r[ QueryCache.IDX_FREQ ] - 1
                        t = ( code, pinyin, hanzi, freq, length )
                        self.cur.execute( self.sql_sentence_insert[i][j], t )
                        #exist_flag = False
                    else:
                        #print "has"
                        update_key = r2[ QueryCache.IDX_KEY ]
                        pos_key = r[ QueryCache.IDX_KEY ]
                        first_key = pos_key
                        if update_key != pos_key :
                            r = rs.fetchone()
                            pos_key = r[ QueryCache.IDX_KEY ]
                            if update_key != pos_key :
                                r = rs.fetchone()
                                pos_key = r[ QueryCache.IDX_KEY ]
                                if update_key != pos_key :
                                    r = rs.fetchone()
                                    pos_key = r[ QueryCache.IDX_KEY ]
                                    if update_key != pos_key :
                                        t = ( pos_key, update_key , )
                                        self.cur.execute( self.sql_sentence_update[i][j], t )
                                    else:
                                        pass
                                else:
                                    t = ( first_key, update_key , )
                                    self.cur.execute( self.sql_sentence_update[i][j], t )
                            else:
                                t = ( first_key, update_key , )
                                self.cur.execute( self.sql_sentence_update[i][j], t )
                        else:
                            pass
                self.conn.commit()
                print "insert cast " + str( time.time() - time_stamp ) + " s"
            elif request == self.OPERATE_REQUEST_DELETE :
                code = data[1]
                i = len(code)
                j = int(code[0])
                key = data[2]
                t = ( key, )
                self.cur.execute( self.sql_sentence_delete[i][j], t )
                self.conn.commit()
                print "delete cast " + str( time.time() - time_stamp ) + " s"
            #print "operate cast " + str( time.time() - time_stamp ) + " s"

class QueryThread( threading.Thread ):
    """
    sqlite查询线程。用来脱离主线程执行词库查询。
    """
    def __init__( self, queue ):
        """
        @queue Queue队列，用来和主线程交换数据。
        数据格式为:
        data = [ code, self.cache, self.frontend ]
        @code 需要查询的code字符串。
        @cache 保存查询结果的缓存列表。
        @frontend 输入面板前端，调用该前端的request_update方法进行刷新。
        """
        threading.Thread.__init__(self)
        self.conn = None
        self.cur = None
        self.queue = queue
        self.sql_sentence = []
        for i in range(65):
            self.sql_sentence.append([])
            for j in range(10):
                s = "select * from phrase_" + str(i) + "_" + str(j) + " where code=? order by freq desc"
                self.sql_sentence[i].append(s)
    def run(self):
        """
        线程实际运行时，执行的函数。由于sqlite的连接不能跨线程，所以在这里打开连接。
        """
        self.conn = sqlite3.connect( "data/main.db" )
        self.cur = self.conn.cursor()
        self.cur.execute( "select * from phrase_0_0" )#first query has delay, due it.
        while(True):
            data = self.queue.get()
            time_stamp = time.time()
            code = data[0]
            cache = data[1]
            frontend = data[2]
            i = len(code)
            cache.flag[i] = QueryCache.FLAG_IN_QUERY
            t = ( code, )
            j = int(code[0])
            #print "start code = " + code
            rs = self.cur.execute( self.sql_sentence[i][j], t )
            rl = rs.fetchall()
            #print type(rl)

            #hz_rl = []
            #if i > 6 :
                #pass
            #else:
                #for r in rl:
                    #if r[cache.IDX_LENGTH] == 1 :
                        #hz_rl.append(r) 

            if len(rl) > 0:
                cache.list[i] = rl
            else:
                cache.list[i] = None
            #if len(hz_rl) > 0:
                #cache.hanzi_list[i] = hz_rl
            #else:
                #cache.hanzi_list[i] = None
            cache.flag[i] = QueryCache.FLAG_VAILD
            #print "end"

            print "query cast " + str( time.time() - time_stamp ) + " s"
            frontend.request_update()

class Conn():
    """
    sqlite连接类
    """
    def __init__(self):
        """
        初始化
        @queue 和查询线程交换数据用的队列
        @qthread 查询线程
        """
        self.query_queue = Queue.Queue()
        self.operate_queue = Queue.Queue()
        self.query_thread = QueryThread( self.query_queue )
        self.operate_thread = OperateThread( self.operate_queue )
        self.query_thread.setDaemon(True) #让子线程在主线程退出后随之退出。
        self.operate_thread.setDaemon(True)
        self.query_thread.start()
        self.operate_thread.start()
    def query( self, data ):
        """
        查询，调用queue的put方法，向查询线程提交数据。
        数据格式为:
        @data = [ code, self.query, self.frontend ]
        @code 需要查询的code字符串。
        @query_cache 保存查询结果的缓存列表。
        @query_cache_flag 保存查询结果的缓存列表flag。
        @frontend 输入面板前端，调用该前端的request_update方法进行刷新。
        """
        self.query_queue.put(data)
    def operate( self, data ):
        self.operate_queue.put(data)

class Cand():
    """
    候选词列表类
    """
    def __init__( self, backend ):
        """
        @backend 输入法后端
        内部变量：
        @list 候选词列表
        @page_index 页码
        @query_index 查询缓存的索引
        @backend 输入法后端
        """
        self.list = []
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.list.append(None)
        self.page_index = 0
        self.query_index = 0
        self.backend = backend
    def update(self):
        rs = self.backend.cache.list[self.query_index]
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
                        #print rs[idx][1]
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
    def shorter(self):
        #print "shorter"
        if self.query_index > 0 :
            i = self.query_index - 1
            rs = self.backend.cache.list[i]
            flag = True
            while flag and rs == None:
                #print i
                if i == 0:
                    flag = False
                else:
                    i = i - 1
                    rs = self.backend.cache.list[i]
            self.query_index = i
    def longest(self):
        i = len( self.backend.code )
        rs = self.backend.cache.list[i]
        while rs == None and i > 0 :
            i = i - 1
            rs = self.backend.cache.list[i]
        self.query_index = i
    def next_page(self):
        rs = self.backend.cache.list[self.query_index]
        if rs :
            idx = self.page_index + 1
            if idx * 6 >= len( rs ):
                pass
            else:
                self.page_index = idx
    def prev_page(self):
        if self.page_index > 0:
            self.page_index = self.page_index - 1
        else:
            pass
            #if self.query_index > 6 :
                #pass
            #else:
                #rs = self.backend.cache.hanzi_list[self.query_index]
                #idx = self.page_index - 1
                #hz_idx = -1 - idx
                #for r in rs :
                    #print r
                #idx = self.page_index + 1
    def reset_page(self):
        self.page_index = 0
    def reset(self):
        self.page_index = 0
        self.selected = []
        self.selected_half = []
        self.list[0] = None
        self.list[1] = None
        self.list[2] = None
        self.list[3] = None
        self.list[4] = None
        self.list[5] = None
    def cancel_select(self):
        i = len( self.backend.selected )
        if i > 0:
            self.backend.code = self.backend.selected[i-1][self.backend.cache.IDX_CODE] + self.backend.code
            self.backend.selected = self.backend.selected[:-1]
            self.backend.selected_half = self.backend.selected_half[:-1]
            return True
        else:
            return False
    def select( self, index ):
        if self.list[index] != None and self.list[index][ QueryCache.IDX_LENGTH ] > 0:
            self.backend.selected.append( self.list[index] )
            idx = self.page_index * 6 + index
            if idx < 3:
                idx = 0
            else:
                idx = idx / 2
            self.backend.selected_half.append( self.backend.cache.list[self.query_index][idx] )
            self.backend.code = self.backend.code[self.query_index:]
            self.backend.cache.reset()
            self.backend.search()
    def delete( self, index ):
        item = self.list[index]
        if item[ QueryCache.IDX_LENGTH ] > 1 :
            #print item[3]
            request = OperateThread.OPERATE_REQUEST_DELETE
            data = [ request, item[ QueryCache.IDX_CODE ] , item[ QueryCache.IDX_KEY ] ]
            self.backend.conn.operate(data)
            idx = self.page_index * 6 + index
            item = ( 0, "", "", "", 0, 0 )
            self.backend.cache.list[ self.query_index ][idx] = item
            self.list[index] = item
            #print item[2]
    def commit(self):
        text = ""
        select_count = len( self.backend.selected )
        for i in range( select_count ) :
            #biaoji
            #print item
            item = self.backend.selected[i]
            text = text + item[self.backend.cache.IDX_HANZI]
            
            request = OperateThread.OPERATE_REQUEST_UPDATE
            code = item[self.backend.cache.IDX_CODE]
            length = len(code)
            j = int(code[0])
            update_key = item[ self.backend.cache.IDX_KEY ]
            item = self.backend.selected_half[i]
            pos_key = item[ self.backend.cache.IDX_KEY ]
            if update_key != pos_key:
                data = [ request, length, j, update_key, pos_key ]
                self.backend.conn.operate(data)

        if select_count > 1: #insert
            code = ""
            pinyin = ""
            for i in range( select_count ) :
                item = self.backend.selected[i]
                code = code + item[self.backend.cache.IDX_CODE]
                pinyin = pinyin + "'" + item[self.backend.cache.IDX_PINYIN]
            pinyin = pinyin[1:]
            length = pinyin.count("'") + 1
            hanzi = text
            request = OperateThread.OPERATE_REQUEST_INSERT
            data = [ request, code, pinyin, hanzi, length ]
            self.backend.conn.operate(data)
        self.backend.reset()
        return text

class Backend():
    """
    输入法后端，脏活累活全归它还见不得光的无名狗熊
    """
    codes = set( ["2","3","4","5","6","7","8","9"] )

    def __init__( self, frontend ):
        """
        初始化。
        @conn sqlite连接
        @frontend 输入法前端
        @code 输入的数字code
        @selected 已经选择好的词列表
        @cache 查询结果缓冲
        @cand 候选字列表
        """
        self.conn = Conn()
        self.frontend = frontend
        self.code = ""
        self.selected = []
        self.selected_half = []
        self.cache = QueryCache()
        self.cand = Cand(self)

    def append_code( self, code ):
        if code in self.codes:
            self.code = self.code + code
        #self.cand.reset()
        self.search()

    def backspace_code(self):
        i = len(self.code)
        if i > 0:
            self.cache.flag[i] = 0
            self.code = self.code[:-1]
        #self.cand.longest()

    def reset(self):
        self.code = ""
        self.selected = []
        self.selected_half = []
        self.cand.reset()
        self.cache.reset()

    def search(self):
        code_len = len( self.code )
        #print "serch enter"
        if code_len > 0:
            for i in range(1,code_len+1):
                #print i
                if self.cache.flag[i] != 1 and  self.cache.flag[i] != 2:
                    data = [ self.code[:i], self.cache, self.frontend ]
                    #print "enter"
                    self.conn.query(data)
                    #print "return"

