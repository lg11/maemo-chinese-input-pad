#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

#import time

#import rotate
from widget import NumPadKey
from backend import Backend


class NumPad( QtGui.QWidget ) :
    commit = QtCore.Signal( str )
    commit_preedit = QtCore.Signal( str )
    external_clicked = QtCore.Signal( int )
    external_longpressed = QtCore.Signal( int )
    KEY_TEXT = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
    KEY_SUB = [ "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz" ]
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
    MODE_NORMAL = 0
    MODE_SELECT = 1
    MODE_FILTER = 2
    MODE_PUNC = 3

    FONT_NORMAL = QtGui.QFont()
    FONT_UNDERLINE = QtGui.QFont()
    FONT_UNDERLINE.setUnderline( True )
    FONT_SUB = QtGui.QFont()
    FONT_SUB.setPointSize( FONT_SUB.pointSize() + 2 )
    FONT_LAGER = QtGui.QFont()
    FONT_LAGER.setPointSize( FONT_LAGER.pointSize() + 17 )
    FONT_LAGER.setBold( True )
    KEYCODE_BACKSPACE = 11
    def __init__( self, parent = None ) :
        QtGui.QWidget.__init__( self, parent )

        self.sub_palette = self.palette()
        self.sub_palette.setColor( QtGui.QPalette.ButtonText, self.sub_palette.mid().color() )

        self.key_list = []
        self.key_label_list = []
        for keycode in range( 10 ) :
            key = NumPadKey( keycode, self )
            #key.setText( self.KEY_TEXT[keycode][0] )
            self.key_list.append( key )
            key.clicked.connect( self.slot_key_click )
            key.longpressed.connect( self.slot_key_longpress )

            key_layout = QtGui.QGridLayout()
            key_layout.setSpacing( 0 )
            key_layout.setContentsMargins( 0, 0, 0, 0 )
            key.setLayout( key_layout )

            label = QtGui.QLabel()
            label.setAlignment( QtCore.Qt.AlignCenter )
            label.setMargin( 0 )
            key_layout.addWidget( label, 0, 0, 2, 1 )
            label.setFont( self.FONT_LAGER )
            label.setText( self.KEY_TEXT[keycode] )
            self.key_label_list.append( label )
            
            label = QtGui.QLabel()
            label.setAlignment( QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop )
            label.setMargin( 0 )
            key_layout.addWidget( label, 2, 0, 1, 1 )
            label.setFont( self.FONT_SUB )
            label.setPalette( self.sub_palette )
            label.setText( self.KEY_SUB[keycode] )


        self.backend = Backend()
        self.mode = self.MODE_NORMAL
        self.pinyin_list = []
        self.pinyin_index = 0
        self.punc_index = 0
        self.update_stamp = []
        for i in range( 10 ) :
            self.update_stamp.append( False )
    def resizeEvent( self, event ) :
        key_width = self.width() / 3
        key_height = self.height() / 4

        y = 0
        for i in range( 3 ) :
            x = 0
            for j in range( 3 ) :
                index = i * 3 + j + 1
                key = self.key_list[index]
                key.resize( key_width, key_height )
                key.move( x, y )
                x = x + key_width
            y = y + key_height
        x = key_width
        key = self.key_list[0]
        key.resize( key_width, key_height )
        key.move( x, y )
    def context_update( self ) :
        for i in range( 10 ) :
            self.key_label_list[i].setFont( self.FONT_LAGER )
            self.update_stamp[i] = False
        if self.mode == self.MODE_NORMAL :
            index = 1
            for item in self.backend.cand_list :
                self.key_label_list[index].setFont( self.FONT_NORMAL )
                self.key_label_list[index].setText( item[2] )
                self.update_stamp[index] = True
                index = index + 1
            text = self.backend.get_selected() + self.backend.code()
            self.commit_preedit.emit( text )
        elif self.mode == self.MODE_SELECT :
            index = 1
            for item in self.backend.cand_list :
                self.key_label_list[index].setFont( self.FONT_UNDERLINE )
                self.key_label_list[index].setText( item[2] )
                self.update_stamp[index] = True
                index = index + 1
            text = self.backend.get_selected() + self.backend.code()
            self.commit_preedit.emit( text )
        elif self.mode == self.MODE_FILTER :
            index = 1
            pinyin_index = self.pinyin_index
            while pinyin_index < len( self.pinyin_list ) and index < 7 :
                self.key_label_list[index].setFont( self.FONT_NORMAL )
                self.key_label_list[index].setText( self.pinyin_list[pinyin_index] )
                self.update_stamp[index] = True
                index = index + 1
                pinyin_index = pinyin_index + 1
        elif self.mode == self.MODE_PUNC :
            index = 2
            punc_list = self.PUNC_MAP[self.punc_index]
            for punc in punc_list :
                self.key_label_list[index].setText( punc )
                self.update_stamp[index] = True
                index = index + 1
        for i in range( 10 ) :
            if not self.update_stamp[i] :
                self.key_label_list[i].setText( self.KEY_TEXT[i] )
    def __reset_mode_setting( self ) :
        pass
    def set_mode( self, mode ) :
        self.__reset_mode_setting()
        self.mode = mode

        if mode == self.MODE_NORMAL :
            pass
        elif mode == self.MODE_SELECT :
            pass
        elif mode == self.MODE_FILTER :
            pass
        elif mode == self.MODE_PUNC :
            self.punc_index = 0
    @QtCore.Slot( int )
    def slot_key_click( self, code ) :
        if self.mode == self.MODE_NORMAL :
            if code >= 2 and code <= 9 :
                self.backend.append( str( code ) )
                self.backend.gen_cand_list()
                self.context_update()
            elif code == self.KEYCODE_BACKSPACE :
                if len( self.backend.code() ) > 0 :
                    c = self.backend.pop()
                    self.backend.gen_cand_list()
                    self.context_update()
            elif code == 1 :
                if len( self.backend.code() ) > 0 :
                    self.set_mode( self.MODE_SELECT )
                    self.context_update()
                else :
                    self.set_mode( self.MODE_PUNC )
                    self.context_update()
        elif self.mode == self.MODE_SELECT :
            if code >= 1 and code <= 6 :
                self.backend.select( code - 1 )
                self.backend.gen_cand_list()
                if len( self.backend.code() ) <= 0 :
                    text = self.backend.get_selected()
                    self.backend.commit()
                    self.commit.emit( text )
                    self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == self.KEYCODE_BACKSPACE :
                c = self.backend.deselect()
                self.backend.gen_cand_list()
                if c == "" :
                    self.set_mode( self.MODE_NORMAL )
                self.context_update()
            elif code == 8 :
                self.pinyin_list = self.backend.get_pinyin_list()
                self.pinyin_list.reverse()
                self.pinyin_index = 0
                self.set_mode( self.MODE_FILTER )
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
                self.commit.emit( punc_list[index] )
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
                self.textedit.ensureCursorVisible()
        elif self.mode == self.MODE_ROLLER :
            if code >= 0 and code <= 9 :
                self.roller.roll( code )
                self.context_update()
            #elif code == 1 :
                #self.roller.stop()
            elif code == self.KEYCODE_BACKSPACE :
                if self.roller.code > 0 :
                    self.roller.cancel()
                else :
                    self.textedit.textCursor().deletePreviousChar()
                    self.textedit.ensureCursorVisible()
                self.context_update()
            elif code == self.KEYCODE_MODE :
                if self.roller.code > 0 :
                    self.roller.stop()
                self.set_mode( self.MODE_NORMAL )
                self.context_update()
        elif self.mode == self.MODE_FILTER :
            if code >= 1 and code <= 6 :
                pinyin_index = self.pinyin_index + code - 1
                if pinyin_index < ( self.pinyin_list ) :
                    self.backend.set_filter( self.pinyin_list[pinyin_index] )
                    self.backend.gen_cand_list()
                    self.set_mode( self.MODE_SELECT )
                    self.context_update()
            elif code == 8 :
                self.backend.set_filter( "" )
                self.backend.gen_cand_list()
                self.set_mode( self.MODE_SELECT )
                self.context_update()
            elif code == 7 :
                if self.pinyin_index > 0 :
                    self.pinyin_index = self.pinyin_index - 6
                self.context_update()
            elif code == 9 :
                if ( self.pinyin_index + 6 ) < len( self.pinyin_list ) :
                    self.pinyin_index = self.pinyin_index + 6
                self.context_update()

    @QtCore.Slot( int )
    def slot_key_longpress( self, code ) :
        if self.mode == self.MODE_NORMAL :
            if code >= 0 and code <= 9 :
                self.textedit.textCursor().insertText( str( code ), self.textedit.normal_format )
                self.textedit.ensureCursorVisible()
        elif self.mode == self.MODE_ROLLER :
            if code >= 0 and code <= 9 :
                if self.roller.code > 0 :
                    self.roller.stop()
                self.textedit.textCursor().insertText( str( code ), self.textedit.normal_format )
                self.textedit.ensureCursorVisible()
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

#class Pad( QtGui.QWidget ) :
    #def __init__( self, daemon_flag = False, parent = None ) :


if __name__ == "__main__" :
    import sys
    app = QtGui.QApplication( sys.argv )

    pad = NumPad()
    pad.show()
    sys.exit( app.exec_() )


