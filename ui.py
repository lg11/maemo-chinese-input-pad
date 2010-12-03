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

from ui_base import NumPadKey
from interface import Interface


class InputPad( QtGui.QWidget ) :
    KEY_MAP = [ \
            [ "0", [ 4, 1, 1, 1 ], 0.9, ] \
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
            [ "undefine", [ 4, 0, 1, 1 ], 0.9, ] \
            , \
            [ "mode", [ 4, 2, 1, 1 ], 0.9, ] \
            , \
            [ "backspace", [ 0, 0, 1, 3 ], 0.75, ] \
            , \
            ]
    UNDEFINE_KEYCODE = 10
    MODE_KEYCODE = 11
    BACKSPACE_KEYCODE = 12
    KEY_HEIGHT = 105
    LAYOUT_SPACING = 0
    MODE_NORMAL = 0
    MODE_SELECT = 1
    MODE_PUNC = 2

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
    FONT_UNDERLINR = QtGui.QFont()
    FONT_UNDERLINR.setUnderline( True )
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        #QtGui.QWidget.__init__( self, parent, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
        self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, True )

        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing( self.LAYOUT_SPACING )
        self.setLayout( self.layout )

        self.textedit = QtGui.QTextEdit( self )
        #self.textedit.setReadOnly( True )
        #self.textedit.grabKeyboard()
        self.layout.addWidget( self.textedit )
        
        self.keypad_layout = QtGui.QGridLayout()
        self.keypad_layout.setSpacing( self.LAYOUT_SPACING )
        self.keypad_layout.setContentsMargins( 0, 0, 0, 0 )
        self.layout.addLayout( self.keypad_layout )

        self.key_list = []
        for keycode in range( len( self.KEY_MAP ) ) :
            key_map = self.KEY_MAP[keycode]
            key = NumPadKey( self, keycode )
            key.setFocusProxy( self.textedit )
            key.setText( key_map[0] )
            key.setFixedHeight( self.KEY_HEIGHT * key_map[2] )
            self.keypad_layout.addWidget( key, key_map[1][0], key_map[1][1] ,key_map[1][2] ,key_map[1][3] )
            self.key_list.append( key )
            key.key_clicked.connect( self.slot_key_click )
            key.key_longpressed.connect( self.slot_key_longpress )

        self.interface = Interface()
        self.mode = self.MODE_NORMAL
        self.punc_index = 0

    def update( self ) :
        if self.mode == self.MODE_NORMAL :
            index = 1
            for item in self.interface.cand_list :
                #print item
                self.key_list[index].setText( item[2] )
                index = index + 1
            text = self.interface.selected[2] + self.interface.code
            self.key_list[self.BACKSPACE_KEYCODE].setText( text )
        elif self.mode == self.MODE_SELECT :
            index = 1
            for item in self.interface.cand_list :
                self.key_list[index].setText( item[2] )
                index = index + 1
            text = self.interface.selected[2] + self.interface.code
            self.key_list[self.BACKSPACE_KEYCODE].setText( text )
        elif self.mode == self.MODE_PUNC :
            index = 2
            punc_list = self.PUNC_MAP[self.punc_index]
            for punc in punc_list :
                self.key_list[index].setText( punc.decode( "utf-8" ) )
                index = index + 1

            
    def set_mode( self, mode ) :
        self.mode = mode

        if mode == self.MODE_NORMAL :
            for i in range( 1, 7 ) :
                self.key_list[i].setFont( self. FONT_NORMAL )
        elif mode == self.MODE_SELECT :
            for i in range( 1, 7 ) :
                self.key_list[i].setFont( self. FONT_UNDERLINR )
        elif mode == self.MODE_PUNC :
            self.punc_index = 0
            for i in range( 1, 7 ) :
                self.key_list[i].setFont( self. FONT_NORMAL )
            
    @QtCore.Slot( int )
    def slot_key_click( self, code ):
        if self.mode == self.MODE_NORMAL :
            if code >= 2 and code <= 9 :
                self.interface.append( str( code ) )
                self.interface.gen_cand()
                self.update()
                #for node in self.interface.cand_list :
                    #print node[0], node[1]
            elif code == self.BACKSPACE_KEYCODE :
                if len( self.interface.code ) > 0 or len( self.interface.selected[0] ) > 0 :
                    self.interface.pop()
                    self.interface.gen_cand()
                    self.update()
                else :
                    cursor = self.textedit.textCursor()
                    cursor.deletePreviousChar()
                    pass
            #elif code == 1 or code == self.UNDEFINE_KEYCODE :
            elif code == 1 :
                if len( self.interface.code ) > 0 :
                    self.set_mode( self.MODE_SELECT )
                    self.update()
                elif len( self.interface.selected[0] ) > 0 :
                    text = self.interface.selected[2]
                    self.interface.commit()
                    self.textedit.insertPlainText( text )
                    self.update()
                else :
                    self.set_mode( self.MODE_PUNC )
                    self.update()
        elif self.mode == self.MODE_SELECT :
            if code >= 1 and code <= 6 :
                self.interface.select( code - 1 )
                if len( self.interface.code ) <= 0 :
                    self.set_mode( self.MODE_NORMAL )
                self.update()
            elif code == self.BACKSPACE_KEYCODE :
                self.set_mode( self.MODE_NORMAL )
                self.update()
            elif code == 7 :
                self.interface.page_prev()
                self.update()
            elif code == 9 :
                self.interface.page_next()
                self.update()
        elif self.mode == self.MODE_PUNC :
            if code >= 2 and code <= 9 :
                index = code - 2
                punc_list = self.PUNC_MAP[self.punc_index]
                self.textedit.insertPlainText( punc_list[index].decode( "utf-8" ) )
                self.set_mode( self.MODE_NORMAL )
                self.update()
            elif code == self.BACKSPACE_KEYCODE :
                self.set_mode( self.MODE_NORMAL )
                self.update()
            #elif code == 1 or code == self.UNDEFINE_KEYCODE :
            elif code == 1 :
                self.punc_index = self.punc_index + 1
                if self.punc_index < len( self.PUNC_MAP ) :
                    pass
                else :
                    self.punc_index = 0
                self.update()
        #self.textedit.setFocus()

    @QtCore.Slot( int )
    def slot_key_longpress( self, code ) :
        #self.textedit.setFocus()
        pass

    def closeEvent( self, event ) :
        self.hide()
        self.interface.backend.save()

if __name__ == "__main__" :
    app = QtGui.QApplication( sys.argv )
    pad = InputPad()
    pad.show()
    sys.exit( app.exec_() )


