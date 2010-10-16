#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import sys

import time

from backendq import Backend

from uiq_base import NumPadKey

class Conn( dbus.service.Object ): 
    def __init__( self, inputpad ):
        dbus.mainloop.glib.DBusGMainLoop( set_as_default=True )
        self.bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName( 'me.maemo.ChineseInputPad', self.bus )
        dbus.service.Object.__init__( self, self.bus_name, '/' )

        self.inputpad = inputpad

    @dbus.service.signal( 'me.maemo.ChineseInputPad', signature = "s" )
    def commit( self, code ):
        pass
    @dbus.service.method( 'me.maemo.ChineseInputPad' )
    def show( self ):
        pass

class CandPad( QtGui.QWidget ) :
    LABEL_WIDTH = 321
    LABEL_HEIGHT = 30
    CAND_LABEL_WIDTH = 105
    CAND_LABEL_HEIGHT = 75
    CAND_LENGTH = 6

    def __init__( self, parent = None, inputpad = None ):
        QtGui.QWidget.__init__( self, parent )
        style_string = ""
        style_string = style_string + "QWidget { border: 1px solid darkgray; border-radius: 8px; background-color: lightgray }"
        style_string = style_string + "QLabel { border: 0px; border-radius: 0px; }"
        self.setStyleSheet( style_string )

        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins( 3, 3, 3, 3 )
        self.setLayout( self.layout )

        self.code_frame = QtGui.QWidget( self )
        self.code_layout = QtGui.QVBoxLayout()
        self.code_layout.setSpacing(0)
        self.code_layout.setContentsMargins( 3, 3, 3, 3 )
        self.code_frame.setLayout( self.code_layout )

        self.pinyin_label = QtGui.QLabel( self.code_frame )
        self.pinyin_label.setFixedHeight( self.LABEL_HEIGHT )
        self.pinyin_label.setAlignment( QtCore.Qt.AlignCenter )
        self.hanzi_label = QtGui.QLabel( self.code_frame )
        self.hanzi_label.setFixedHeight( self.LABEL_HEIGHT )
        self.hanzi_label.setAlignment( QtCore.Qt.AlignCenter )
        self.code_layout.addWidget( self.pinyin_label )
        self.code_layout.addWidget( self.hanzi_label )

        self.cand_frame = QtGui.QWidget( self )
        self.cand_layout = QtGui.QGridLayout()
        self.cand_layout.setSpacing(1)
        self.cand_layout.setContentsMargins( 3, 3, 3, 3 )
        self.cand_frame.setLayout( self.cand_layout )

        self.cand_label = []
        for i in range(2):
            for j in range(3):
                label = QtGui.QLabel( self.cand_frame )
                label.setFixedSize( self.CAND_LABEL_WIDTH, self.CAND_LABEL_HEIGHT )
                label.setAlignment( QtCore.Qt.AlignCenter )
                label.setWordWrap( True )
                self.cand_layout.addWidget( label, i, j )
                self.cand_label.append( label )

        self.layout.addWidget( self.code_frame )
        self.layout.addWidget( self.cand_frame )

        self.inputpad = inputpad

        self.page_index = 0
        self.result_list = []
    def update( self ):
        time_stamp = time.time()
        pinyin_text_list = []
        hanzi_text_list = []

        index = len( self.inputpad.cache )
        if index > 0:
            index = index - 1
            result = self.inputpad.cache[index]
        else:
            result = [ None, None ]
        while not ( result[0] or result[1] ) and index > 0 :
            index = index - 1
            result = self.inputpad.cache[index]
        if not ( result[0] or result[1] ) :
            remained_code = self.inputpad.code
        else:
            remained_code = self.inputpad.code[index + 1:]
        #print result
        #print remained_code

        if result[0] or result[1]:
            index = self.page_index * self.CAND_LENGTH
            if result[0]:
                pinyin = result[0][index][0]
                hanzi = result[0][index][1].decode("utf-8")
            else:
                pinyin = result[1][index][0]
                hanzi = result[1][index][1].decode("utf-8")
            if self.inputpad.mode == self.inputpad.MODE_INPUT :
                pinyin_text_list.append( "<font color=blue>" + pinyin + "</font>" )
                hanzi_text_list.append( "<font color=blue>" + hanzi + "</font>" )
            elif self.inputpad.mode == self.inputpad.MODE_SELECT :
                pinyin_text_list.append( "<font color=white style=\"background-color: blue\">" + pinyin + "</font>" )
                hanzi_text_list.append( "<font color=white style=\"background-color: blue\">" + hanzi + "</font>" )

        if len( remained_code ) > 0 :
            pinyin_text_list.append( "<font color=red>" + remained_code + "</font>" )
            hanzi_text_list.append( "<font color=red>" + remained_code + "</font>" )

        self.pinyin_label.setText( "<font color=green>'</font>".join( pinyin_text_list ) )
        self.hanzi_label.setText( "<font color=green>'</font>".join( hanzi_text_list ) )

        result_list = []
        if result[0] or result[1]:
            zi_count = 0
            ci_count = 0
            if result[0]:
                zi_count = len( result[0] )
            if result[1]:
                ci_count = len( result[1] )
            zi_index = 0
            ci_index = 0
            flag = True
            while flag:
                zi_flag = True
                ci_flag = True
                if zi_index < zi_count:
                    for i in range(3):
                        if zi_index < zi_count:
                            result_list.append( [ 0 ,zi_index ] )
                            zi_index = zi_index + 1
                        else:
                            zi_flag = False
                else:
                    zi_flag = False
                if ci_index < ci_count:
                    for i in range(3):
                        if ci_index < ci_count:
                            result_list.append( [ 1, ci_index ] )
                            ci_index = ci_index + 1
                        else:
                            ci_flag = False
                else:
                    ci_flag = False
                flag = zi_flag or ci_flag
                #if zi_index + ci_index > ( self.page_index + 1 ) * self.CAND_LENGTH :
                    #flag = False

        self.result_list = result_list
        cand_list = []
        for i in range( self.CAND_LENGTH ) :
            index = self.page_index * self.CAND_LENGTH + i
            if index < len( result_list ) :
                cand_list.append( result_list[index] )
        for i in range( self.CAND_LENGTH ) :
            cand_text = ""
            if i < len( cand_list ):
                cand_text = "<font color=black>" + result[ cand_list[i][0] ][ cand_list[i][1] ][1].decode("utf-8") + "</font>"
            self.cand_label[i].setText( cand_text )
        print "candpad update cast", time.time() - time_stamp, "second"
    def prev_page( self ) :
        if self.page_index > 0 :
            self.page_index = self.page_index - 1
            self.update()
    def next_page( self ) :
        self.page_index = self.page_index + 1
        self.update()
            

class TextView( QtGui.QWidget ) :
    def __init__( self, parent = None, inputpad = None ):
        QtGui.QWidget.__init__( self, parent )
        self.textedit = QtGui.QTextEdit( self )
        #self.textedit.setReadOnly( True )
        self.textedit.resize( 330, 420 )
        self.resize( 330, 420 )

        self.candpad = CandPad( self, inputpad )
        self.move_candpad()

        self.textedit.cursorPositionChanged.connect( self.move_candpad )
    @QtCore.Slot()
    def move_candpad(self):
        rect = self.textedit.cursorRect()
        y = rect.y() + rect.height()
        if y < 35:
            y = 35
        self.candpad.move( 0, y )
    @QtCore.Slot( str )
    def commit( self, text ):
        self.textedit.insertPlainText( text )
        #self.cand.request_cand.emit()

class NumPad( QtGui.QWidget ):
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 96
    BUTTON_HEIGHT_LITE = 68
    CODE_CHECK = 10
    CODE_BACKSPACE = 11
    CODE_MODE = 12

    key_clicked = QtCore.Signal( int )
    
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        
        self.num_button = []
        #check button
        button = NumPadKey( self, self.CODE_CHECK )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( 0, 0 )
        button.key_clicked.connect( self.key_click )
        #backspace button
        button = NumPadKey( self, self.CODE_BACKSPACE )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH, 0 )
        button.key_clicked.connect( self.key_click )
        #mode button
        button = NumPadKey( self, self.CODE_MODE )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        button.key_clicked.connect( self.key_click )
        #button 0
        button = NumPadKey( self, 0 )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( 0, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        button.key_clicked.connect( self.key_click )
        self.num_button.append( button )
        #button 1 - 9
        for i in range(3):
            for j in range(3):
                button = NumPadKey( self, i * 3 + j + 1 )
                button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT )
                button.move( self.BUTTON_WIDTH * j, self.BUTTON_HEIGHT * i + self.BUTTON_HEIGHT_LITE )
                button.key_clicked.connect( self.key_click )
                self.num_button.append( button )

    @QtCore.Slot(int)
    def key_click( self, code ):
        self.key_clicked.emit( code )

class InputPad( QtGui.QWidget ): 
    MODE_INPUT = 1
    MODE_SELECT = 2
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )

        self.numpad = NumPad( self )
        self.numpad.move( 340, 0 )
     
        self.textview = TextView( self, self )
        self.textview.move( 5, 3 )

        self.candpad = self.textview.candpad

        self.backend = Backend()
        self.code = ""

        self.mode = 0
        self.set_mode( self.MODE_INPUT )

        self.numpad.key_clicked.connect( self.numpad_key_click )

        self.cache = []

    def set_mode( self, mode ):
        self.mode = mode
    @QtCore.Slot( int )
    def numpad_key_click( self, code ):
        #time_stamp = time.time()
        if self.mode == self.MODE_INPUT :
            if code >= 2 and code <= 9 :
                self.code = self.code + str(code)
                time_stamp = time.time()
                result = self.backend.query( self.code )
                print "query cast", time.time() - time_stamp, "second"
                self.cache.append( result )
                self.candpad.update()
            elif code == 1 :
                self.set_mode( self.MODE_SELECT )
                self.candpad.update()
            elif code == self.numpad.CODE_BACKSPACE :
                if len( self.code ) > 0:
                    self.code = self.code[:-1]
                    self.cache.pop()
                    self.candpad.update()
        if self.mode == self.MODE_SELECT :
            if code >= 1 and code <= 6 :
                pass
            elif code == 7 :
                self.candpad.prev_page()
            elif code == 9 :
                self.candpad.next_page()
            elif code == self.numpad.CODE_BACKSPACE :
                self.set_mode( self.MODE_INPUT )
                self.candpad.update()
        #print "key_click cast", time.time() - time_stamp, "second"
                


if __name__ == "__main__" :
    app = QtGui.QApplication( sys.argv )

    #style_string = ""
    #style_string = style_string + "QWidget { background-color: gray }"
    #style_string = style_string + "QLayout { border: 1px }"
    #style_string = style_string + "QLabel { border: 1px solid darkgray; background-color: white }"
    #style_string = style_string + "QLabel { background-color: lightgray }"
    #style_string = style_string + "QTextEdit { background-color: white; border: 0px; border-radius: 0px }"
    #style_string = style_string + "QPushButton { border: 5px solid gray; border-radius: 0px; background-color: qlineargradient(x1: 0, y1: 0.15, x2: 0, y2: 0.18, stop: 0 #f6f7fa, stop: 1 #dadbde); min-width: 80px; }"
    #style_string = style_string + "QPushButton:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.7, stop: 0 #5566ee, stop: 1 #f6f7fa); }"

    style_string = ""
    style_string = style_string + "QWidget { background-color: white }"
    style_string = style_string + "QTextEdit { background-color: white; border: 1px solid darkgray; border-radius: 8px }"
    style_string = style_string + "QPushButton { margin: 3px; border: 1px solid darkgray; border-radius: 8px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.05, stop: 0 white, stop: 1 lightgray); }"
    style_string = style_string + "QPushButton:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.7, lightblue: 0 blue, stop: 1 white); }"
    app.setStyleSheet( style_string )

    #win = QtGui.QWidget( None, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
    pad = InputPad()
    pad.resize( 800, 480 )
    pad.show()

    sys.exit( app.exec_() )

