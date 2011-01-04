#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot


class TextEdit( QtGui.QTextEdit ) :
    longpressed = QtCore.Signal( int )
    clicked = QtCore.Signal( int )
    DEFAULT_LONGPRESS_INTERVAL = 350
    DEFAULT_MOVE_CONTROL_INTERVAL = 350
    DEFAULT_MOVE_INTERVAL = 35
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
        self.start_pos = None
        self.external_flag = False
        self.move_flag = False
        self.move_control_timer = QtCore.QTimer()
        self.move_control_flag = True
        self.move_control_timer.timeout.connect( self.move_control_timeout )
        self.move_timer = QtCore.QTimer()
        self.move_timer.timeout.connect( self.__move )

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
    def mouseDoubleClickEvent( self, event ) :
        self.mousePressEvent( event )
    def mousePressEvent( self, event ) :
        self.auto_repeat_timer.stop()
        self.move_control_flag = True
        self.move_control_timer.stop()
        self.move_timer.stop()
        self.start_pos = event.pos()
        self.move_flag = False
        self.timer.start( self.longpress_interval )
    @QtCore.Slot()
    def __move( self ) :
        self.move_timer.stop
        self.move_timer.start( self.DEFAULT_MOVE_INTERVAL )
        pos = self.mapFromGlobal( QtGui.QCursor.pos() )
        rect = self.cursorRect()
        top, bottom = rect.top(), rect.bottom()
        height = self.height()
        old_cursor = self.textCursor()
        start_cursor = self.textCursor()
        start_cursor.movePosition( QtGui.QTextCursor.StartOfLine )
        end_cursor = self.textCursor()
        end_cursor.movePosition( QtGui.QTextCursor.EndOfLine )
        y = pos.y()
        if y < -0 :
            y = top - 1
        elif y >= -0 and y <= height + 50 :
            y = top
        elif y > height + 30 :
            y = bottom + 1
        pos.setY( y )
        x = pos.x()
        pos.setX( x - 10 )
        new_cursor = self.cursorForPosition( pos )
        self.setTextCursor( new_cursor )
        rect = self.cursorRect()
        if new_cursor < start_cursor or new_cursor >= end_cursor :
            if not self.move_control_flag :
                self.setTextCursor( old_cursor )
            else :
                self.move_control_flag = False
                self.move_control_timer.start( self.DEFAULT_MOVE_CONTROL_INTERVAL )

    def mouseMoveEvent( self, event ) :
        if self.move_flag :
            self.__move()
        else :
            pos = event.pos()
            x = self.start_pos.x() - event.x()
            y = self.start_pos.y() - event.y()
            d = x * x + y * y
            #print d
            if d > 1024 :
                self.move_flag = True
    def mouseReleaseEvent( self, event ) :
        self.auto_repeat_timer.stop()
        self.move_control_flag = True
        self.move_control_timer.stop()
        self.move_timer.stop()
        if self.timer.isActive() :
            self.timer.stop()
            x = event.pos().x()
            if self.move_flag :
                pass
            elif len( self.preedit ) > 0 or self.external_flag :
                self.clicked.emit( self.keycode )
            else :
                width = self.width()
                if x - self.start_pos.x() > width / 10 :
                    self.__move_end()
                elif self.start_pos.x() - x > width / 10 :
                    self.__move_start()
                else :
                    self.__delete()
            self.ensureCursorVisible()
    @QtCore.Slot()
    def auto_repeat( self ) :
        self.auto_repeat_timer.stop()
        self.auto_repeat_timer.start( self.auto_repeat_interval )
        if self.move_flag :
            pass
        elif len( self.preedit ) > 0 or self.external_flag :
            self.clicked.emit( self.keycode )
        else :
            self.__delete()
        self.ensureCursorVisible()
    @QtCore.Slot()
    def move_control_timeout( self ) :
        self.move_control_flag = True
    @QtCore.Slot()
    def timeout( self ) :
        self.timer.stop()
        if self.auto_repeat_flag :
            if self.move_flag :
                pass
            elif len( self.preedit ) > 0 or self.external_flag :
                self.clicked.emit( self.keycode )
            else :
                self.__delete()
            self.ensureCursorVisible()
            self.auto_repeat_timer.start( self.auto_repeat_interval )
        else :
            self.longpressed.emit( self.keycode )


