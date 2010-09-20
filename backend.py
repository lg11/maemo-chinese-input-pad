#-!- coding=utf-8 -!-

import sqlite3
import threading
import Queue

class QueryCache():
    """
    查询缓存
    """
    FLAG_INVAILD = 0
    FLAG_IN_QUERY = 1
    FLAG_VAILD = 2
    IDX_ROWID = 0
    IDX_CODE = 1
    IDX_PINYIN = 2
    IDX_HANZI = 3
    def __init__(self):
        """
        初始化
        @cache 缓存列表
        @flag 标志
        """
        self.list = []
        self.flag = [] 
        for i in range(65):
            self.list.append(None)
            self.flag.append(self.FLAG_INVAILD)
    def reset(self):
        """
        重置整个缓存
        """
        for i in range(65):
            self.flag[i] = self.FLAG_INVAILD

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
        self.sql_ci = []
        self.sql_zi = []
        for i in range(65):
            self.sql_ci.append([])
            if i < 7 :
                self.sql_zi.append([])
            for j in range(10):
                s = "select ROWID,* from ci_" + str(i) + "_" + str(j) + " where code=? order by update_count desc, priority asc"
                self.sql_ci[i].append( s )
                if i < 7 :
                    s = "select ROWID,* from zi_" + str(i) + "_" + str(j) + " where code=? order by update_count desc, priority"
                    self.sql_zi[i].append( s )
    def run(self):
        """
        线程实际运行时，执行的函数。由于sqlite的连接不能跨线程，所以在这里打开连接。
        """
        self.conn = sqlite3.connect( "data/main.db" )
        self.cur = self.conn.cursor()
        while(True):
            data = self.queue.get()
            code = data[0]
            cache = data[1]
            frontend = data[2]
            i = len(code)
            t = ( code, )
            j = int(code[0])
            cache.flag[i] = QueryCache.FLAG_IN_QUERY
            #print "start code = " + code
            rs = self.cur.execute( self.sql_ci[i][j], t )
            rl = rs.fetchall()
            for r in rl:
                print r[3] + str(r[4])
            if len(rl) > 0:
                cache.list[i] = rl
            else:
                cache.list[i] = None
            cache.flag[i] = QueryCache.FLAG_VAILD
            #print "end"
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
        self.queue = Queue.Queue()
        self.qthread = QueryThread( self.queue )
        self.qthread.setDaemon(True) #让子线程在主线程退出后随之退出。
        self.qthread.start()
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
        self.queue.put(data)

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
        idx = self.page_index + 1
        if idx * 6 >= len( rs ):
            pass
        else:
            self.page_index = idx
    def prev_page(self):
        if self.page_index > 0:
            self.page_index = self.page_index - 1
    def reset_page(self):
        self.page_index = 0
    def reset(self):
        self.page_index = 0
        self.selected = []
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
            return True
        else:
            return False
    def select( self, index ):
        if self.list[index] != None:
            self.backend.selected.append( self.list[index] )
            self.backend.code = self.backend.code[self.query_index:]
            self.backend.cache.reset()
            self.backend.search()
    def commit(self):
        text = ""
        for item in self.backend.selected:
            #print item
            text = text + item[3]
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
        @selected_phrase 已经选择好的词列表
        @cache 查询结果缓冲
        @cand 候选字列表
        """
        self.conn = Conn()
        self.frontend = frontend
        self.code = ""
        self.selected = []
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

