#-!- coding=utf-8 -!-

from PySide import QtCore, QtGui
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import sys

from uiq_base import NumPadKey

class Conn( dbus.service.Object ): 
    def __init__( self, inputpad ):
        dbus.mainloop.glib.DBusGMainLoop( set_as_default=True )
        self.bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName( 'me.maemo_chinese_input_pad.ui', self.bus )
        dbus.service.Object.__init__( self, self.bus_name, '/' )

        self.backend = self.bus.get_object( 'me.maemo_chinese_input_pad.backend', '/' )
        self.backend.setup()
        self.backend.reset()

        self.iface = dbus.Interface( self.backend, "me.maemo_chinese_input_pad.backend" )
        self.iface.connect_to_signal( "cand_updated", self.cand_updated )
        self.iface.connect_to_signal( "commit", self.commit )

        self.inputpad = inputpad

    @dbus.service.signal( 'me.maemo_chinese_input_pad.ui', signature = "s" )
    def append_code( self, code ):
        pass
    @dbus.service.signal( 'me.maemo_chinese_input_pad.ui' )
    def backspace( self ):
        pass
    @dbus.service.signal( 'me.maemo_chinese_input_pad.ui' )
    def request_cand( self ):
        pass
    @dbus.service.signal( 'me.maemo_chinese_input_pad.ui', signature = "i" )
    def select_phrase( self, index ):
        pass
    def backend_reset( self ):
        self.backend.reset()
        #print "append_code %d" %( code )
    def cand_updated( self, hanzi_list, pinyin_list, selected_hanzi, selected_pinyin, remained_code ):
        self.inputpad.cand_updated.emit( hanzi_list, pinyin_list, selected_hanzi, selected_pinyin, remained_code )
    def commit( self, text ):
        self.inputpad.commit( text )



class CandPad( QtGui.QWidget ) :
    LABEL_WIDTH = 321
    LABEL_HEIGHT = 30
    CAND_LABEL_WIDTH = 107
    CAND_LABEL_HEIGHT = 75
    CAND_LENGTH = 6

    MODE_NORMAL = 1
    MODE_SELECT = 2

    request_cand = QtCore.Signal()

    def __init__( self, parent = None ):
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
        self.code_layout.setContentsMargins( 0, 0, 0, 0 )
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
        self.cand_layout.setContentsMargins( 0, 0, 0, 0 )
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

        self.mode = self.MODE_NORMAL

    @QtCore.Slot( list, list, str, str, str )
    def cand_update( self, hanzi_list, pinyin_list, selected_hanzi, selected_pinyin, remained_code ):
        #print pinyin_list
        #print "cand_update"
        #self.show()
        pinyin_text_list = []
        hanzi_text_list = []
        if len( selected_pinyin ) > 0 :
            pinyin_text_list.append( "<font color=black>" + selected_pinyin + "</font>" )
            hanzi_text_list.append( "<font color=black>" + selected_hanzi + "</font>" )
        if len( pinyin_list ) > 0 :
            if self.mode == self.MODE_NORMAL :
                pinyin_text_list.append( "<font color=blue>" + pinyin_list[0] + "</font>" )
                hanzi_text_list.append( "<font color=blue>" + hanzi_list[0] + "</font>" )
            elif self.mode == self.MODE_SELECT :
                pinyin_text_list.append( "<font color=white style=\"background-color: blue\">" + pinyin_list[0] + "</font>" )
                hanzi_text_list.append( "<font color=white style=\"background-color: blue\">" + hanzi_list[0] + "</font>" )
        if len( remained_code ) > 0 :
            pinyin_text_list.append( "<font color=red>" + remained_code + "</font>" )
            hanzi_text_list.append( "<font color=red>" + remained_code + "</font>" )

        self.pinyin_label.setText( "<font color=green>'</font>".join( pinyin_text_list ) )
        self.hanzi_label.setText( "<font color=green>'</font>".join( hanzi_text_list ) )

        for i in range( self.CAND_LENGTH ) :
            cand_text = None
            if i < len( hanzi_list ):
                cand_text = "<font color=black>" + hanzi_list[i] + "</font>"
            self.cand_label[i].setText( cand_text )
        #print selected_hanzi
        #print selected_pinyin
        #print remained_code
    @QtCore.Slot()
    def enter_select_mode(self):
        self.mode = self.MODE_SELECT
        self.request_cand.emit()
    @QtCore.Slot()
    def leave_select_mode(self):
        self.mode = self.MODE_NORMAL

class TextView( QtGui.QWidget ) :
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        self.textedit = QtGui.QTextEdit( self )
        #self.textedit.setReadOnly( True )
        self.textedit.resize( 330, 420 )
        self.resize( 330, 420 )

        self.cand = CandPad( self )
        self.cand.move( 0, 100 )

        self.textedit.cursorPositionChanged.connect( self.move_cand )
        #self.textedit.cursorPositionChanged.emit()
    @QtCore.Slot()
    def move_cand(self):
        rect = self.textedit.cursorRect()
        self.cand.move( 0, rect.y() + rect.height() )
    @QtCore.Slot( str )
    def commit( self, text ):
        self.textedit.insertPlainText( text )
        self.cand.request_cand.emit()

class NumPad( QtGui.QWidget ):
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 96
    BUTTON_HEIGHT_LITE = 68
    CODE_CHECK = 10
    CODE_BACKSPACE = 11
    CODE_MODE = 12

    MODE_INPUT = 1
    MODE_SELECT = 2
    append_code = QtCore.Signal(int)
    backspace = QtCore.Signal()
    mode_changed = QtCore.Signal(int)
    enter_select_mode = QtCore.Signal()
    leave_select_mode = QtCore.Signal()
    select_phrase = QtCore.Signal(int)
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        
        self.num_button = []
        #check button
        button = NumPadKey( self, self.CODE_CHECK )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( 0, 0 )
        button.key_clicked.connect( self.slot_key_clicked )
        #backspace button
        button = NumPadKey( self, self.CODE_BACKSPACE )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH, 0 )
        button.key_clicked.connect( self.slot_key_clicked )
        #mode button
        button = NumPadKey( self, self.CODE_MODE )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        button.key_clicked.connect( self.slot_key_clicked )
        #button 0
        button = NumPadKey( self, 0 )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( 0, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        button.key_clicked.connect( self.slot_key_clicked )
        self.num_button.append( button )
        #button 1 - 9
        for i in range(3):
            for j in range(3):
                button = NumPadKey( self, i * 3 + j + 1 )
                button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT )
                button.move( self.BUTTON_WIDTH * j, self.BUTTON_HEIGHT * i + self.BUTTON_HEIGHT_LITE )
                button.key_clicked.connect( self.slot_key_clicked )
                self.num_button.append( button )

        self.mode = 0
        self.set_mode( self.MODE_INPUT )
    @QtCore.Slot(int)
    def slot_key_clicked( self, code ):
        #print "key_clicked"
        #print code
        if self.mode == self.MODE_INPUT :
            if code >= 2 and code <= 9:
                self.append_code.emit(code)
            elif code == 1 :
                self.set_mode( self.MODE_SELECT )
            elif code == self.CODE_BACKSPACE :
                self.backspace.emit()
        elif self.mode == self.MODE_SELECT :
            if code >= 1 and code <= 6:
                self.select_phrase.emit( code - 1 )
            pass
        else :
            pass
    def set_mode( self, mode ):
        self.mode = mode
        if mode == self.MODE_SELECT :
            self.enter_select_mode.emit()
        self.mode_changed.emit(mode)
    @QtCore.Slot()
    def reset( self ):
        self.set_mode( self.MODE_INPUT )

class InputPad( QtGui.QWidget ): 
    cand_updated = QtCore.Signal( list, list, str, str, str )
    request_commit = QtCore.Signal( str )
    commited = QtCore.Signal()
    def __init__( self, parent = None ):

        QtGui.QWidget.__init__( self, parent )

        self.numpad = NumPad( self )
        self.numpad.move( 340, 0 )
     
        self.textview = TextView( self )
        self.textview.move( 5, 3 )

        self.cand = self.textview.cand

        self.conn = Conn( self )
        self.numpad.append_code.connect( self.append_code )
        self.cand_updated.connect( self.cand.cand_update )
        self.numpad.backspace.connect( self.backspace )

        self.numpad.enter_select_mode.connect( self.cand.enter_select_mode )
        self.numpad.select_phrase.connect( self.conn.select_phrase )
        self.cand.request_cand.connect( self.conn.request_cand )

        self.request_commit.connect( self.textview.commit )
        self.commited.connect( self.conn.backend_reset )
        self.commited.connect( self.numpad.reset )
        self.commited.connect( self.cand.hide )
        self.commited.connect( self.cand.leave_select_mode )
        self.numpad.append_code.connect( self.cand.show )

        self.cand.hide()
        self.code = ""
    @QtCore.Slot( str )
    def append_code( self, code ):
        self.code = self.code + str(code)
        self.conn.append_code( str(code) )
    @QtCore.Slot()
    def backspace( self ):
        if len( self.code ) > 0 :
            self.code = self.code[:-1]
            self.conn.backspace()
    @QtCore.Slot( str )
    def commit( self, text ):
        self.request_commit.emit( text )
        self.commited.emit()
        self.code = ""
        print text

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

