#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

#import time

#import rotate
from textedit import TextEdit
from numpad import NumPad
from keyboard import KeyPad, KEYPAD_MAP, KEYPAD_MAP_NAME
from backend import Backend

class Rotater( QtGui.QWidget ) :
    def __init__( self, parent = None ) :
        QtGui.QWidget.__init__( self, parent, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
        self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, False )
        self.setFixedHeight( 1 )
    def resizeEvent( self, event ) :
        if event.size().width() >= 800 :
            self.hide()
    def closeEvent( self, event ) :
        self.hide()
        event.ignore()

class CharRoller( QtCore.QObject ) :
    ROLLER = [ " @", ".,", "abcABC", "defDEF", "ghiGHI", "jklJKL", "mnoMNO", "pqrsPQRS" ,"tuvTUV", "wxyzWXYZ" ]
    timeout_interval = 1000
    commit = QtCore.Signal( str )
    #timeout = QtCore.Signal()
    def __init__( self ) :
        QtCore.QObject.__init__( self )
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.slot_timeout )
        self.roller = -1
        self.code = -1
    @QtCore.Slot()
    def slot_timeout( self ) :
        self.timer.stop()
        c = self.ROLLER[self.code][self.roller]
        self.code = -1
        self.roller = -1
        self.commit.emit( c )
        #self.timeout.emit()
    def cancel( self ) :
        self.timer.stop()
        self.code = -1
        self.roller = -1
    def stop( self ) :
        if self.code >= 0 :
            c = self.ROLLER[self.code][self.roller]
            self.code = -1
            self.roller = -1
            self.commit.emit( c )
        self.cancel()
    def roll( self, code ) :
        self.timer.stop()
        if code == self.code :
            if self.roller < len( self.ROLLER[code] ) - 1 :
                self.roller = self.roller + 1
            else :
                self.roller = 0
            self.timer.start( self.timeout_interval )
        else :
            if self.code >= 0 :
                self.commit.emit( self.ROLLER[self.code][self.roller] )
            self.code = code
            self.roller = 0
            self.timer.start( self.timeout_interval )
    def get( self ) :
        c = ""
        if self.code >= 0 :
            c = self.ROLLER[self.code][self.roller]
        return c

class InputPad( QtGui.QWidget ) :
    request_commit = QtCore.Signal( str )
    NUMPAD_HEIGHT = 440
    PAD_HEIGHT = 690
    TEXTEDIT_HEIGHT = 140
    LAYOUT_SPACING = 0
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
        self.text_palette.setColor( QtGui.QPalette.Base, self.sub_palette.window().color() )
        self.text_palette.setColor( QtGui.QPalette.Base, QtGui.QColor( 0, 0, 0, 0 ) )
        self.text_palette.setColor( QtGui.QPalette.Background, QtGui.QColor( 0, 0, 0, 0 ) )

        self.rotater = Rotater()

        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing( 0 )
        self.layout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( self.layout )

        self.textedit = TextEdit( NumPad.KEYCODE_BACKSPACE, self )
        #self.textedit.setStyleSheet( "QTextEdit { border-width : 0px ; padding : 0px }" )
        #self.textedit.setPalette( self.text_palette )
        self.textedit.setFixedHeight( self.TEXTEDIT_HEIGHT )
        #self.textedit.longpressed.connect( self.slot_key_longpress )
        self.textedit.setAttribute( QtCore.Qt.WA_TranslucentBackground, True )
        self.layout.addWidget( self.textedit )
        
        self.stack = QtGui.QStackedLayout()
        self.layout.addLayout( self.stack )
        self.keypad_list = []
        
        keypad = NumPad( self )
        keypad.setFixedHeight( self.NUMPAD_HEIGHT )
        self.keypad_list.append( keypad )
        keypad.commit.connect( self.textedit.commit )
        keypad.commit_preedit.connect( self.textedit.commit_preedit )
        self.textedit.clicked.connect( keypad.slot_key_click )
        keypad.external_request.connect( self.textedit.accept_request )
        for key in keypad.key_list :
            key.setFocusProxy( self.textedit )

        self.stack.addWidget( keypad )

        #self.layout.addStretch()
        self.tab = QtGui.QTabBar( self )
        self.tab.addTab( "中".decode( "utf-8" ) )
        self.layout.addWidget( self.tab )

        for i in range( len( KEYPAD_MAP ) ) :
            keypad = KeyPad( KEYPAD_MAP[i] )
            keypad.commit.connect( self.textedit.commit )
            for row in keypad.key_list :
                for key in row :
                    if key :
                        key.setFocusProxy( self.textedit )
            self.keypad_list.append( keypad )
            self.stack.addWidget( keypad )
            self.tab.addTab( KEYPAD_MAP_NAME[i] )

        self.tab.currentChanged.connect( self.stack.setCurrentIndex )

        self.daemon_flag = daemon_flag
        if self.daemon_flag :
            self.desktop = QtGui.QApplication.desktop()
            rect = self.desktop.screenGeometry()
            if rect.height() < rect.width() :
                self.portrait = False
            else :
                self.portrait = True
    def callback_show( self, string ) :
        self.textedit.setText( string )
        self.textedit.moveCursor( QtGui.QTextCursor.End )
        self.textedit.ensureCursorVisible()
        rect = self.desktop.screenGeometry()
        if rect.height() < rect.width() :
            self.portrait = False
        else :
            self.portrait = True
        self.show()
    def resizeEvent( self, event ) :
        #print self.width(), self.height(), self.isVisible()
        if self.height() < self.PAD_HEIGHT :
            self.resize( 480, self.PAD_HEIGHT )
    def closeEvent( self, event ) :
        if self.daemon_flag :
            #self.setAttribute( QtCore.Qt.WA_Maemo5PortraitOrientation, True )
            self.hide()
            event.ignore()
            if not self.portrait :
                self.rotater.resize( 1, 1 )
                self.rotater.show()
            self.textedit.commit_preedit( "" )
            self.keypad_list[0].set_mode( self.keypad_list[0].MODE_NORMAL )
            self.keypad_list[0].backend.set_code( "" )
            text = self.textedit.toPlainText()
            self.request_commit.emit( text )
        else :
            event.accept()
        #self.backend.backend.save()


if __name__ == "__main__" :
    import sys
    app = QtGui.QApplication( sys.argv )

    pad = InputPad()
    pad.show()
    sys.exit( app.exec_() )


