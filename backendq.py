#-!- coding=utf-8 -!-

import sqlite3
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from PySide import QtCore
#from PyQt4 import QtCore, QtGui
#QtCore.Signal = QtCore.pyqtSignal
#QtCore.Slot = QtCore.pyqtSlot

import time

class QueryCache():
    """
    查询缓存
    """
    INDEX_KEY = 0
    INDEX_CODE = 1
    INDEX_PINYIN = 2
    INDEX_HANZI = 3
    INDEX_FREQ = 4
    INDEX_LENGTH = 5
    DELETED_PHRASE = ( 0, "", "", "", 0, 0 )
    updated = QtCore.Signal()
    def __init__(self):
        """
        初始化
        @cache 缓存列表
        @flag 标志
        """
        QtCore.QObject.__init__( self )
        self.list = []
        for i in range(65):
            self.list.append([])
    #@QtCore.Slot()
    #def reset(self):
        #pass
        #for i in range(65):
            #self.list[i] = []
    @QtCore.Slot( int, list )
    def update( self, index, result_list ):
        print "cache.update"
        self.list[index] = result_list
        self.updated.emit( index )


class SqliteConn( QtCore.QObject ):
    """
    sqlite连接类
    """
    query_completed = QtCore.Signal( int, list )
    def __init__( self ):
        """
        初始化
        """
        QtCore.QObject.__init__( self )
        self.conn = sqlite3.connect( "/home/user/.config/maemo-chinese-input-pad/data/main.db" )
        self.cur = self.conn.cursor()
        self.cur.execute( "select * from phrase_0_0" )#first query has delay, due it.

        self.sql_sentence_query = []
        self.sql_sentence_update = []
        self.sql_sentence_insert = []
        self.sql_sentence_insert_query = []
        self.sql_sentence_insert_count = []
        self.sql_sentence_delete = []
        for i in range(65):
            self.sql_sentence_query.append([])
            self.sql_sentence_update.append([])
            self.sql_sentence_insert.append([])
            self.sql_sentence_insert_query.append([])
            self.sql_sentence_insert_count.append([])
            self.sql_sentence_delete.append([])
            for j in range(10):
                s = "select * from phrase_" + str(i) + "_" + str(j) + " where code=? order by freq desc"
                self.sql_sentence_query[i].append(s)
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
    @QtCore.Slot( str )
    def query( self, code ):
        time_stamp = time.time()
        i = len(code)
        #cache.flag[i] = QueryCache.FLAG_IN_QUERY
        t = ( code, )
        j = int(code[0])
        print "query start code = " + code
        rs = self.cur.execute( self.sql_sentence_query[i][j], t )
        rl = rs.fetchall()
        self.query_completed.emit( i, rl )
        print "query cast " + str( time.time() - time_stamp ) + " s"
    @QtCore.Slot( str, int, int )
    def adjust( self, code, key, to_key ):
        """
        更新词库词条的词频
        把key上的词的词频调整为to_key上的词的词频+1
        @code 词的code
        @key key
        @to_key
        """
        time_stamp = time.time()
        i = len( code )
        j = int( code[0] )
        t = ( key, to_key , )
        rs = self.cur.execute( self.sql_sentence_update[i][j], t )
        self.conn.commit()
        print "update cast " + str( time.time() - time_stamp ) + " s"
    @QtCore.Slot( str, str, str, int )
    def insert( self, code, pinyin, hanzi, length ):
        time_stamp = time.time()
        freq = 0
        i = len(code)
        j = int(code[0])
        t = ( code, )
        rs = self.cur.execute( self.sql_sentence_insert_query[i][j], t )
        r = rs.fetchone()
        if r == None :
            #print "no code"
            freq = 1
            t = ( code, pinyin, hanzi, freq, length )
            self.cur.execute( self.sql_sentence_insert[i][j], t )
        else:
            t = ( code, hanzi, )
            rs2 = self.cur.execute( self.sql_sentence_insert_count[i][j], t )
            r2 = rs.fetchone()
            if r2 == None :
                #print "no ci"
                freq = r[ QueryCache.INDEX_FREQ ] - 1
                r = rs.fetchone()
                if r != None :
                    freq = r[ QueryCache.INDEX_FREQ ] - 1
                    r = rs.fetchone()
                    if r != None :
                        freq = r[ QueryCache.INDEX_FREQ ] - 1
                t = ( code, pinyin, hanzi, freq, length )
                self.cur.execute( self.sql_sentence_insert[i][j], t )
            else:
                #print "has"
                key = r2[ QueryCache.INDEX_KEY ]
                to_key = r[ QueryCache.INDEX_KEY ]
                first_key = to_key
                if key != to_key :
                    r = rs.fetchone()
                    to_key = r[ QueryCache.INDEX_KEY ]
                    if key != to_key :
                        r = rs.fetchone()
                        to_key = r[ QueryCache.INDEX_KEY ]
                        if key != to_key :
                            r = rs.fetchone()
                            to_key = r[ QueryCache.INDEX_KEY ]
                            if key != to_key :
                                t = ( to_key, key , )
                                self.cur.execute( self.sql_sentence_update[i][j], t )
                            else:
                                to_key = first_key
                                t = ( to_key, key , )
                                self.cur.execute( self.sql_sentence_update[i][j], t )
                        else:
                            to_key = first_key
                            t = ( to_key, key , )
                            self.cur.execute( self.sql_sentence_update[i][j], t )
                    else:
                        to_key = first_key
                        t = ( to_key, update_key , )
                        self.cur.execute( self.sql_sentence_update[i][j], t )
                else:
                    pass
        self.conn.commit()
        print "insert cast " + str( time.time() - time_stamp ) + " s"
    @QtCore.Slot( str, int )
    def delete( self, code, key ):
        time_stamp = time.time()
        i = len(code)
        j = int(code[0])
        t = ( key, )
        self.cur.execute( self.sql_sentence_delete[i][j], t )
        self.conn.commit()
        print "delete cast " + str( time.time() - time_stamp ) + " s"

class Cand( QtCore.QObject ):
    """
    候选词列表类
    """
    PAGE_LENGTH = 6
    updated = QtCore.Signal()
    selected = QtCore.Signal( list )
    deleted = QtCore.Signal( str, int )
    def __init__( self, cache ):
        """
        @cache
        内部变量：
        @list 候选词列表
        @page_index 页码
        @cache_index 查询缓存的索引
        @cache
        """
        QtCore.QObject.__init__( self )
        self.list = []
        self.page_index = 0
        self.cache_index = 0
        self.cache = cache
    @QtCore.Slot()
    def update( self ):
        print "cand.update"
        rs = self.cache.list[self.cache_index]
        self.list = []
        if rs:
            if self.page_index * self.PAGE_LENGTH >= len( rs ):
                pass
            else:
                for i in range( self.CAND_LENGTH ):
                    index = self.page_index * self.PAGE_LENGTH + i
                    if index < len(rs):
                        self.list.append( rs[ index ] )
                    else:
                        pass
        else:
            pass
        self.updated.emit()

    @QtCore.Slot()
    def next_page(self):
        index = self.page_index + 1
        if index * self.PAGE_LENGTH >= len( rs ):
            pass
        else:
            self.page_index = index
            self.update()
    @QtCore.Slot()
    def prev_page(self):
        if self.page_index > 0:
            self.page_index = self.page_index - 1
            self.update()
        else:
            pass
    @QtCore.Slot()
    def reset_page(self):
        self.page_index = 0
        self.update()
    @QtCore.Slot()
    def shorter(self):
        #print "shorter"
        if self.cache_index > 0 :
            index = self.cache_index - 1
            rs = self.cache.list[index]
            flag = True
            while flag and len(rs) < 1 :
                if index < 1 :
                    flag = False
                else:
                    index = index - 1
                    rs = self.cache.list[index]
            self.cache_index = index
            self.reset_page()
    @QtCore.Slot( int )
    def longest( self, code_length ):
        rs = self.cache.list[code_length]
        index = code_length
        while len(rs) < 1 and index > 0 :
            index = index - 1
            rs = self.cache.list[index]
        self.cache_index = index
        self.reset_page()
    @QtCore.Slot()
    def reset(self):
        self.page_index = 0
        self.cache_index = 0
        self.list = []
    @QtCore.Slot( int )
    def select( self, index ):
        if index < len( self.list ) :
            if self.list[index][ QueryCache.INDEX_LENGTH ] > 0 :
                r = self.list[index]
                self.selected.emit(r)
    @QtCore.Slot( int )
    def delete( self, index ):
        item = self.list[index]
        if item[ self.cache.INDEX_LENGTH ] > 1 :
            #print item[3]
            self.deleted.emit( item[ QueryCache.INDEX_CODE ] , item[ QueryCache.INDEX_KEY ] )
            item = self.cache.DELETED_PHRASE
            self.list[index] = item
            index = self.page_index * self.CAND_LENGTH + index
            self.cache.list[ self.cache_index ][index] = item


    @QtCore.Slot()
    def commit(self):
        text = ""
        select_count = len( self.selected )
        for i in range( select_count ) :
            item = self.selected[i]
            text = text + item[self.cache.INDEX_HANZI]
            
            code = item[self.cache.INDEX_CODE]
            key = item[ self.cache.INDEX_KEY ]
            item = self.selected_half[i]
            to_key = item[ self.cache.INDEX_KEY ]
            if key != to_key:
                self.commit_phrase.emit( code, key, to_key )
        if select_count > 1: #insert
            code = ""
            pinyin = ""
            for i in range( select_count ) :
                item = self.selected[i]
                code = code + item[self.cache.INDEX_CODE]
                pinyin = pinyin + "'" + item[self.cache.INDEX_PINYIN]
            length = pinyin.count("'")
            pinyin = pinyin[1:]
            hanzi = text
            self.new_phrase.emit( code, pinyin, hanzi, length )
        self.commited.emit(text)

class Backend( dbus.service.Object ): 
    """
    输入法后端，脏活累活全归它还见不得光的无名狗熊
    """
    code_set = set( ["2","3","4","5","6","7","8","9"] )
    #commited = QtCore.Signal( str )
    #code_backspaced = QtCore.Signal()
    def __init__( self ):
        """
        初始化。
        @conn sqlite连接
        @code 输入的数字code
        @selected 已经选择好的词列表
        @cache 查询结果缓冲
        @cand 候选字列表
        """
        self.bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName( 'me.maemo_chinese_input_pad.backend', self.bus )
        dbus.service.Object.__init__( self, self.bus_name, '/' )

        self.code = ""
        self.conn = SqliteConn()
        self.cache = QueryCache()
        self.cand = Cand(self.cache)

        self.selected = []
        self.selected_half = []

    def setup( self ):
        self.ui = self.bus.get_object( 'me.maemo_chinese_input_pad.ui', '/' )
        self.iface = dbus.Interface( self.ui, "me.maemo_chinese_input_pad.ui" )
        self.iface.connect_to_signal( "append_code", self.append_code )
        self.iface.connect_to_signal( "backspace_code", self.backspace_code )
    def append_code( self, code ):
        pass
    def slot_commited( self, text ):
        self.commited.emit( text )
    def slot_request_query( self ):
        self.request_query.emit( self.code )
    def slot_select_phrase( self, r ):
        print "select"
        selected_code_length = len( r[ self.cache.INDEX_CODE ] )
        self.code = self.code[selected_code_length:]
        if len( self.code ) > 0:
            self.request_query.emit( self.code )
        else:
            self.request_commit.emit()
    def slot_cand_updated( self ):
        hanzi_list = []
        pinyin_list = []
        for item in self.cand.list:
            hanzi_list.append( item[ self.cache.INDEX_HANZI ] )
            pinyin_list.append( item[ self.cache.INDEX_PINYIN ] )

        selected_hanzi = ""
        selected_pinyin = ""
        for item in self.cand.selected:
            selected_hanzi = selected_hanzi + item[ self.cache.INDEX_HANZI ]
            selected_pinyin = selected_pinyin + item[ self.cache.INDEX_PINYIN ]

        remained_code = self.code[self.cand.query_index:]
            
        self.cand_updated.emit( hanzi_list, pinyin_list, selected_hanzi, selected_pinyin, remained_code )
    def append_code( self, code ):
        if code in self.code_set and len( self.code ) < 64:
            self.code = self.code + code
            self.request_query.emit( self.code )
    def backspace( self ):
        i = len(self.code)
        if i > 0:
            #self.cache.flag[i] = 0
            self.code = self.code[:-1]
            self.cache.query_completed.emit(i-1)
    def request_cand( self ):
        self.slot_cand_updated()
    def select_phrase( self, index ):
        self.cand.select( index )
    def reset( self ):
        self.code = ""
        #self.selected = []
        #self.selected_half = []
        self.cand.reset()
        self.cache.reset()

class DBusObject( dbus.service.Object ): 
    def __init__( self ):
        """
        初始化。
        @conn sqlite连接
        @code 输入的数字code
        @selected 已经选择好的词列表
        @cache 查询结果缓冲
        @cand 候选字列表
        """
        #QtCore.QObject.__init__( self )
        self.bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName( 'me.maemo_chinese_input_pad.backend', self.bus )
        dbus.service.Object.__init__( self, self.bus_name, '/' )

        self.backend = Backend()
        self.backend.cand_updated.connect( self.cand_updated )
        self.backend.commited.connect( self.commit )

        self.ui = None
        self.iface = None
        #self.backend.reset()

    @dbus.service.method( 'me.maemo_chinese_input_pad.backend' )
    def setup( self ):
        self.ui = self.bus.get_object( 'me.maemo_chinese_input_pad.ui', '/' )
        self.iface = dbus.Interface( self.ui, "me.maemo_chinese_input_pad.ui" )
        self.iface.connect_to_signal( "append_code", self.append_code )
        self.iface.connect_to_signal( "backspace", self.backspace )
        self.iface.connect_to_signal( "request_cand", self.request_cand )
        self.iface.connect_to_signal( "select_phrase", self.select_phrase )
    def select_phrase( self, index ):
        self.backend.select_phrase( index )
    def request_cand( self ):
        self.backend.request_cand()
    def append_code( self, code ):
        #print "append %s" %(code)
        self.backend.append_code( code )
    #@dbus.service.method( 'me.maemo_chinese_input_pad.backend' )
    def backspace(self):
        self.backend.backspace()
    @dbus.service.method( 'me.maemo_chinese_input_pad.backend' )
    def reset(self):
        self.backend.reset()
    @dbus.service.signal( 'me.maemo_chinese_input_pad.backend', signature = "s" )
    def commit( self, text ):
        pass
    @dbus.service.signal( 'me.maemo_chinese_input_pad.backend', signature = "asassss" )
    def cand_updated( self, hanzi_list, pinyin_list, selected_hanzi, selected_pinyin, remained_code ):
        pass
    #@dbus.service.method( 'me.maemo_chinese_input_pad.backend', out_signature='as' )
    #def get_cand( self ):
        #print "gen_cand"
        #cand_list = []
        #for r in self.cand.list:
            #if r != None :
                #cand_list.append( r[QueryCache.INDEX_HANZI] )
        #return cand_list
