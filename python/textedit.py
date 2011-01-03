#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot


class TextEdit( QtGui.QTextEdit ) :
    longpressed = QtCore.Signal( int )
    clicked = QtCore.Signal( int )
    DEFAULT_LONGPRESS_INTERVAL = 350
    DEFAULT_AUTO_REPEAT_INTERVAL = 65
    def __init__( self, keycode, parent = None ) :
        QtGui.QTextEdit.__init__( self, parent )
        self.setAttribute( QtCore.Qt.WA_InputMethodEnabled, False )
        self.keycode = keycode
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.longpress_interval = self.DEFAULT_LONGPRESS_INTERVAL
        self.preedit_start_pos = -1
        self.preedit_end_pos = -1
        self.preedit = ""
        self.start_x = -1
        self.external_flag = False

        self.auto_repeat_timer = QtCore.QTimer()
        self.auto_repeat_flag = True
        self.auto_repeat_interval = self.DEFAULT_AUTO_REPEAT_INTERVAL
        self.auto_repeat_timer.timeout.connect( self.auto_repeat )
        self.normal_format = QtGui.QTextCharFormat()
        self.preedit_format = QtGui.QTextCharFormat()
        self.preedit_format.setFontUnderline( True )
    @QtCore.Slot( bool )
    def accept_request( self, flag ):
        self.external_flag = flag
    def __clear_preedit( self ) :
        if not ( self.preedit_start_pos < 0 ) :
            cursor = self.textCursor()
            cursor.setPosition( self.preedit_end_pos )
            while cursor.position() > self.preedit_start_pos :
                cursor.deletePreviousChar()
        self.preedit = ""
        self.preedit_start_pos = -1
        self.preedit_end_pos = -1
    def __insert_preedit( self, text ) :
        cursor = self.textCursor()
        self.preedit = text
        self.preedit_start_pos = cursor.position()
        cursor.insertText( text, self.preedit_format )
        self.preedit_end_pos = cursor.position()
        self.ensureCursorVisible()
    @QtCore.Slot( str )
    def commit_preedit( self, text ) :
        self.__clear_preedit()
        if len( text ) > 0 :
            self.__insert_preedit( text )
    @QtCore.Slot( str )
    def commit( self, c ) :
        self.textCursor().insertText( c, self.normal_format )
        self.ensureCursorVisible()
        #self.context_update()
    def mouseDoubleClickEvent( self, event ) :
        self.mousePressEvent( event )
    def mousePressEvent( self, event ) :
        self.start_x = self.mapFromGlobal( event.pos() ).x()
        self.timer.start( self.longpress_interval )
    def __move_end( self ) :
        pos = self.textCursor()
        end_pos = self.textCursor()
        end_pos.movePosition( QtGui.QTextCursor.EndOfLine )
        if pos == end_pos :
            self.moveCursor( QtGui.QTextCursor.Right )
        self.moveCursor( QtGui.QTextCursor.EndOfLine )
    def __move_start( self ) :
        pos = self.textCursor()
        start_pos = self.textCursor()
        start_pos.movePosition( QtGui.QTextCursor.StartOfLine )
        if pos == start_pos :
            self.moveCursor( QtGui.QTextCursor.Left )
        self.moveCursor( QtGui.QTextCursor.StartOfLine )
    def __delete( self ) :
        cursor = self.textCursor()
        if cursor.atStart() :
            cursor.deleteChar()
        else :
            cursor.deletePreviousChar()
    def mouseReleaseEvent( self, event ) :
        self.auto_repeat_timer.stop()
        if self.timer.isActive() :
            self.timer.stop()
            x = self.mapFromGlobal( event.pos() ).x()
            if len( self.preedit ) > 0 or self.external_flag :
                self.clicked.emit( self.keycode )
            else :
                width = self.width()
                if x - self.start_x > width / 3 :
                    self.__move_end()
                elif self.start_x - x > width / 3 :
                    self.__move_start()
                elif self.start_x < self.width() / 2 :
                    self.moveCursor( QtGui.QTextCursor.Left )
                else :
                    self.__delete()
            self.ensureCursorVisible()
    @QtCore.Slot()
    def auto_repeat( self ) :
        self.auto_repeat_timer.stop()
        self.auto_repeat_timer.start( self.auto_repeat_interval )
        if len( self.preedit ) > 0 or self.external_flag :
            self.clicked.emit( self.keycode )
        else :
            width = self.width()
            if self.start_x < self.width() / 2 :
                self.moveCursor( QtGui.QTextCursor.Left )
            else :
                self.__delete()
        self.ensureCursorVisible()
    @QtCore.Slot()
    def timeout( self ) :
        self.timer.stop()
        if self.auto_repeat_flag :
            if len( self.preedit ) > 0 or self.external_flag :
                self.clicked.emit( self.keycode )
            else :
                width = self.width()
                if self.start_x < self.width() / 2 :
                    self.moveCursor( QtGui.QTextCursor.Left )
                else :
                    self.__delete()
            self.ensureCursorVisible()
            self.auto_repeat_timer.start( self.auto_repeat_interval )
        else :
            self.longpressed.emit( self.keycode )


