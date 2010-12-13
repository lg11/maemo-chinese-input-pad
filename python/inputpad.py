#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

import sys
import time

#import rotate
from widget import NumPadKey, TextEditKey
from backend import Backend

class Rotater( QtGui.QWidget ) :
    def __init__( self, parent = None ) :
        QtGui.QWidget.__init__( self, parent, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
        self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, False )
        self.setFixedHeight( 1 )
    def resizeEvent( self, event ) :
        #print "resize"
        #print event.oldSize().width(), event.oldSize().height()
        #print event.size().width(), event.size().height()
        if event.size().width() >= 800 :
            #self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, False )
            self.hide()
    def closeEvent( self, event ) :
        #self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, False )
        self.hide()
        event.ignore()
    #def showEvent( self, event ) :
        #pass

class InputPad( QtGui.QWidget ) :
    request_commit = QtCore.Signal( str )
    KEY_MAP = [ \
            [ "0", [ 4, 1, 1, 1 ], 0.95, ] \
            , \
            [ "1", [ 1, 0, 1, 1 ], 1.0, ] \
            , \
            [ "2", [ 1, 1, 1, 1 ], 1.0, ] \
            , \
            [ "3", [ 1, 2, 1, 1 ], 1.0, ] \
            , \
            [ "4", [ 2, 0, 1, 1 ], 1.0, ] \
            , \
            [ "5", [ 2, 1, 1, 1 ], 1.0, ] \
            , \
            [ "6", [ 2, 2, 1, 1 ], 1.0, ] \
            , \
            [ "7", [ 3, 0, 1, 1 ], 1.0, ] \
            , \
            [ "8", [ 3, 1, 1, 1 ], 1.0, ] \
            , \
            [ "9", [ 3, 2, 1, 1 ], 1.0, ] \
            , \
            [ "navigate", [ 4, 0, 1, 1 ], 0.95, ] \
            , \
            [ "mode", [ 4, 2, 1, 1 ], 0.95, ] \
            , \
            [ "backspace", [ 0, 0, 1, 3 ], 0.85, ] \
            , \
            ]
    KEY_TEXT = [ \
            [ "0", "", "", "", "undefine", ] \
            , \
            [ "1", "", "", "", "sym", ] \
            , \
            [ "2", "", "", "up", "abc", ] \
            , \
            [ "3", "", "", "", "def", ] \
            , \
            [ "4", "", "", "left", "ghi", ] \
            , \
            [ "5", "", "", "", "jkl", ] \
            , \
            [ "6", "", "", "right", "mno", ] \
            , \
            [ "7", "<", "", "", "pqrs", ] \
            , \
            [ "8", "", "", "down", "tuv", ] \
            , \
            [ "9", ">", "", "", "wxyz", ] \
            , \
            [ "", "", "", "", "navigate", ] \
            , \
            [ "", "", "", "", "mode", ] \
            , \
            [ "backspace", "", "", "", "", ] \
            , \
            ]
    KEYCODE_NAVIGATE = 10
    KEYCODE_MODE = 11
    KEYCODE_BACKSPACE = 12
    KEY_HEIGHT = 110
    LAYOUT_SPACING = 0
    MODE_NORMAL = 0
    MODE_SELECT = 1
    MODE_PUNC = 2
    MODE_NAVIGATE = 3

    PUNC_MAP = [ \
            [ " ", "\n", "，", "。", "？", "……", "～", "！", ] \
            , \
            [ "、", "；", "：", "“", "”", "——", "（", "）", ] \
            , \
            [ "@", "&", "_", "《", "》", "%", "‘", "’", ] \
            , \
            [ "*", "#", "\\", "+", "-", "=", "*", "/", ] \
            , \
            ]


    FONT_NORMAL = QtGui.QFont()
    FONT_UNDERLINE = QtGui.QFont()
    FONT_UNDERLINE.setUnderline( True )
    FONT_SUB = QtGui.QFont()
    FONT_SUB.setPointSize( FONT_SUB.pointSize() + 2 )
    FONT_LAGER = QtGui.QFont()
    FONT_LAGER.setPointSize( FONT_LAGER.pointSize() + 17 )
    FONT_LAGER.setBold( True )
    def __init__( self, daemon_flag = False, parent = None ) :
        if daemon_flag :
            QtGui.QWidget.__init__( self, parent, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
        else :
            QtGui.QWidget.__init__( self, parent )

        self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, True )

        self.sub_palette = self.palette()
        self.sub_palette.setColor( QtGui.QPalette.ButtonText, self.sub_palette.mid().color() )
        self.text_palette = self.palette()
        self.text_palette.setColor( QtGui.QPalette.Text, self.sub_palette.windowText().color() )
        self.text_palette.setColor( QtGui.QPalette.Base, self.sub_palette.window().color() )

        self.rotater = Rotater()

        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing( self.LAYOUT_SPACING )
        self.setLayout( self.layout )

        #label = QtGui.QLabel()
        #label.setFixedHeight( 10 )
        #self.layout.addWidget( label )

        self.textedit = TextEditKey( self.KEYCODE_BACKSPACE, self )
        #self.textedit.setPalette( self.text_palette )
        #style = QtGui.QApplication.style()
        #self.textedit.setStyle( style )
        self.textedit.clicked.connect( self.slot_key_click )
        self.textedit.longpressed.connect( self.slot_key_longpress )
        self.layout.addWidget( self.textedit )
        
        self.keypad_layout = QtGui.QGridLayout()
        self.keypad_layout.setSpacing( self.LAYOUT_SPACING )
        self.keypad_layout.setContentsMargins( 0, 0, 0, 65 )
        self.layout.addLayout( self.keypad_layout )

        self.key_list = []
        self.key_label_list = []
        self.key_sub_label_list = []
        for keycode in range( len( self.KEY_MAP ) ) :
            key_map = self.KEY_MAP[keycode]
            key = NumPadKey( keycode, self )
            key.setFocusProxy( self.textedit )
            #key.setText( self.KEY_TEXT[keycode][0] )
            key.setFixedHeight( self.KEY_HEIGHT * key_map[2] )
            self.keypad_layout.addWidget( key, key_map[1][0], key_map[1][1] ,key_map[1][2] ,key_map[1][3] )
            self.key_list.append( key )
            key.clicked.connect( self.slot_key_click )
            key.longpressed.connect( self.slot_key_longpress )

            key_layout = QtGui.QGridLayout()
            key_layout.setSpacing( 0 )
            key_layout.setContentsMargins( 0, 0, 0, 0 )
            key.setLayout( key_layout )

            #label = QtGui.QLabel()
            #key_layout.addWidget( label, 0, 0, 1, 1 )

            label = QtGui.QLabel()
            label.setAlignment( QtCore.Qt.AlignCenter )
            label.setMargin( 0 )
            key_layout.addWidget( label, 0, 0, 2, 1 )
            label.setFont( self.FONT_LAGER )
            label.setText( self.KEY_TEXT[keycode][0] )
            self.key_label_list.append( label )
            
            label = QtGui.QLabel()
            label.setAlignment( QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop )
            label.setMargin( 0 )
            key_layout.addWidget( label, 2, 0, 1, 1 )
            label.setFont( self.FONT_SUB )
            label.setPalette( self.sub_palette )
            label.setText( self.KEY_TEXT[keycode][-1] )
            self.key_sub_label_list.append( label )

        #self.key_list[self.KEYCODE_BACKSPACE].enableAutoRepeat()
        self.key_list[self.KEYCODE_BACKSPACE].hide()

        self.backend = Backend()
        self.mode = self.MODE_NORMAL
        self.punc_index = 0

        self.daemon_flag = daemon_flag
        if self.daemon_flag :
            self.desktop = QtGui.QApplication.desktop()
            rect = self.desktop.screenGeometry()
            if rect.height() < rect.width() :
                self.portrait = False
            else :
                self.portrait = True

    def callback_show( self, string ) :
        #self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, True )
        self.textedit.setText( string )
        self.textedit.moveCursor( QtGui.QTextCursor.End )
        rect = self.desktop.screenGeometry()
        if rect.height() < rect.width() :
            self.portrait = False
        else :
            self.portrait = True
        self.show()
        for key in self.key_label_list[-4:-1] :
            key.repaint()
        #self.update()
    def resizeEvent( self, event ) :
        #print self.width(), self.height(), self.isVisible()
        if self.height() < 655 :
            self.resize( 480, 655 )
            self.update()
    def context_update( self ) :
        update_stamp = []
        for i in range( len( self.KEY_MAP ) ) :
            self.key_label_list[i].setFont( self.FONT_LAGER )
            update_stamp.append( False )
        if self.mode == self.MODE_NORMAL :
            index = 1
            for item in self.backend.cand_list :
                #print item
                self.key_label_list[index].setFont( self.FONT_NORMAL )
                self.key_label_list[index].setText( item[2] )
                update_stamp[index] = True
                index = index + 1
            text = self.backend.get_selected() + self.backend.code()
            self.textedit.set_preedit( text )
        elif self.mode == self.MODE_SELECT :
            index = 1
            for item in self.backend.cand_list :
                self.key_label_list[index].setFont( self.FONT_UNDERLINE )
                self.key_label_list[index].setText( item[2] )
                update_stamp[index] = True
                index = index + 1
            text = self.backend.get_selected() + self.backend.code()
            self.textedit.set_preedit( text )
        elif self.mode == self.MODE_PUNC :
            index = 2
            punc_list = self.PUNC_MAP[self.punc_index]
            for punc in punc_list :
                self.key_label_list[index].setText( punc.decode( "utf-8" ) )
                update_stamp[index] = True
                index = index + 1
        for i in range( len( self.KEY_MAP ) ) :
            if not update_stamp[i] :
                self.key_label_list[i].setText( self.KEY_TEXT[i][self.mode] )

    def __reset_mode_setting( self ) :
        #for i in range( len( self.key_list ) ) :
            #self.key_label_list[i].setFont( self. FONT_NORMAL )
        self.key_list[self.KEYCODE_NAVIGATE].setDown( False )
    def set_mode( self, mode ) :
        self.__reset_mode_setting()
        self.mode = mode

        if mode == self.MODE_NORMAL :
            pass
        elif mode == self.MODE_SELECT :
            pass
        elif mode == self.MODE_PUNC :
            self.punc_index = 0
        elif mode == self.MODE_NAVIGATE :
            self.key_list[self.KEYCODE_NAVIGATE].setDown( True )
            
    @QtCore.Slot( int )
    def slot_key_click( self, code ) :
        if self.mode == self.MODE_NORMAL :
            if code >= 2 and code <= 9 :
                self.backend.append( str( code ) )
                self.backend.gen_cand_list()
                self.context_update()
                #for node in self.backend.cand_list :
                    #print node[0], node[1]
            elif code == self.KEYCODE_BACKSPACE :
                if len( self.backend.code() ) > 0 :
                    c = self.backend.pop()
                    self.backend.gen_cand_list()
                    self.context_update()
                    if len( self.backend.code() ) <= 0 :
                        #self.key_list[code].pause_auto_repeat()
                        #self.key_list[code].disable()
                        pass
                else :
                    cursor = self.textedit.textCursor()
                    cursor.deletePreviousChar()
                    pass
            elif code == 1 :
                if len( self.backend.code() ) > 0 :
                    self.set_mode( self.MODE_SELECT )
                    self.context_update()
                else :
                    self.set_mode( self.MODE_PUNC )
                    self.context_update()
            elif code == self.KEYCODE_NAVIGATE :
                if len( self.backend.code() ) > 0 :
                    pass
                else :
                    self.set_mode( self.MODE_NAVIGATE )
                    self.context_update()
            elif code == self.KEYCODE_MODE :
                #self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, False )
                pass
        elif self.mode == self.MODE_SELECT :
            if code >= 1 and code <= 6 :
                self.backend.select( code - 1 )
                self.backend.gen_cand_list()
                if len( self.backend.code() ) <= 0 :
                    text = self.backend.get_selected()
                    self.backend.commit()
                    self.textedit.textCursor().insertText( text, self.textedit.normal_format )
                    self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == self.KEYCODE_BACKSPACE :
                c = self.backend.deselect()
                self.backend.gen_cand_list()
                if c == "" :
                    self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == 7 :
                self.backend.page_prev()
                self.backend.gen_cand_list()
                self.context_update()
            elif code == 9 :
                self.backend.page_next()
                self.backend.gen_cand_list()
                self.context_update()
        elif self.mode == self.MODE_PUNC :
            if code >= 2 and code <= 9 :
                index = code - 2
                punc_list = self.PUNC_MAP[self.punc_index]
                self.textedit.textCursor().insertText( punc_list[index].decode( "utf-8" ), self.textedit.normal_format )
                self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == self.KEYCODE_BACKSPACE :
                self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == 1 :
                self.punc_index = self.punc_index + 1
                if self.punc_index < len( self.PUNC_MAP ) :
                    pass
                else :
                    self.punc_index = 0
                self.context_update()
        elif self.mode == self.MODE_NAVIGATE :
            if code == self.KEYCODE_NAVIGATE :
                self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == 5 :
                self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == 2 :
                self.textedit.moveCursor( QtGui.QTextCursor.Up )
            elif code == 8 :
                self.textedit.moveCursor( QtGui.QTextCursor.Down )
            elif code == 4 :
                self.textedit.moveCursor( QtGui.QTextCursor.Left )
            elif code == 6 :
                self.textedit.moveCursor( QtGui.QTextCursor.Right )
            elif code == self.KEYCODE_BACKSPACE :
                self.textedit.textCursor().deletePreviousChar()

    @QtCore.Slot( int )
    def slot_key_longpress( self, code ) :
        if self.mode == self.MODE_NORMAL :
            if code >= 0 and code <= 9 :
                self.textedit.textCursor().insertText( str( code ), self.textedit.normal_format )
        pass
    def closeEvent( self, event ) :
        if self.daemon_flag :
            #self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, True )
            self.hide()
            event.ignore()
            if not self.portrait :
                self.rotater.resize( 1, 1 )
                self.rotater.show()
            self.textedit.set_preedit( "" )
            self.set_mode( self.MODE_NORMAL )
            text = self.textedit.toPlainText()
            self.request_commit.emit( text )
        else :
            event.accept()
        #self.backend.backend.save()

if __name__ == "__main__" :
    app = QtGui.QApplication( sys.argv )

    pad = InputPad()
    pad.show()
    sys.exit( app.exec_() )


