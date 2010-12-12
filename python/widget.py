#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

class Key( QtGui.QPushButton ) :
    longpressed = QtCore.Signal( int )
    clicked = QtCore.Signal( int )
    DEFAULT_LONGPRESS_INTERVAL = 350
    def __init__( self, keycode, parent = None ) :
        QtGui.QPushButton.__init__( self, parent )
        self.keycode = keycode
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.longpress_interval = self.DEFAULT_LONGPRESS_INTERVAL
    def mousePressEvent( self, event ) :
        self.setDown( True )
        self.timer.start( self.longpress_interval )
    def mouseReleaseEvent( self, event ) :
        self.setDown( False )
        if self.timer.isActive() :
            self.timer.stop()
            self.clicked.emit( self.keycode )
    @QtCore.Slot()
    def timeout( self ) :
        self.timer.stop()
        self.longpressed.emit( self.keycode )

class TextEditKey( QtGui.QTextEdit ) :
    longpressed = QtCore.Signal( int )
    clicked = QtCore.Signal( int )
    DEFAULT_LONGPRESS_INTERVAL = 350
    DEFAULT_AUTO_REPEAT_INTERVAL = 65
    def __init__( self, keycode, parent = None ) :
        QtGui.QTextEdit.__init__( self, parent )
        self.keycode = keycode
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.longpress_interval = self.DEFAULT_LONGPRESS_INTERVAL
        self.preedit_start_pos = -1
        self.preedit_end_pos = -1

        self.auto_repeat_timer = QtCore.QTimer()
        self.auto_repeat_flag = True
        self.auto_repeat_interval = self.DEFAULT_AUTO_REPEAT_INTERVAL
        self.auto_repeat_timer.timeout.connect( self.auto_repeat )
    def __clear_preedit( self ) :
        if not ( self.preedit_start_pos < 0 ) :
            cursor = self.textCursor()
            cursor.setPosition( self.preedit_end_pos )
            while cursor.position() > self.preedit_start_pos :
                cursor.deletePreviousChar()
        self.preedit_start_pos = -1
        self.preedit_end_pos = -1
        self.normal_format = QtGui.QTextCharFormat()
        self.preedit_format = QtGui.QTextCharFormat()
        self.preedit_format.setFontUnderline( True )
    def __insert_preedit( self, text ) :
        cursor = self.textCursor()
        self.preedit_start_pos = cursor.position()
        cursor.insertText( text, self.preedit_format )
        self.preedit_end_pos = cursor.position()
    def set_preedit( self, text ) :
        self.__clear_preedit()
        if len( text ) > 0 :
            self.__insert_preedit( text )
    def mouseDoubleClickEvent( self, event ) :
        self.mousePressEvent( event )
    def mousePressEvent( self, event ) :
        self.timer.start( self.longpress_interval )
    def mouseReleaseEvent( self, event ) :
        self.auto_repeat_timer.stop()
        if self.timer.isActive() :
            self.timer.stop()
            self.clicked.emit( self.keycode )
    @QtCore.Slot()
    def auto_repeat( self ) :
        self.auto_repeat_timer.stop()
        self.auto_repeat_timer.start( self.auto_repeat_interval )
        self.clicked.emit( self.keycode )
    @QtCore.Slot()
    def timeout( self ) :
        self.timer.stop()
        if self.auto_repeat_flag :
            self.auto_repeat_timer.start( self.auto_repeat_interval )
            self.clicked.emit( self.keycode )
        else :
            self.longpressed.emit( self.keycode )


class m_key( QtGui.QPushButton ) :
    m_longpressed = QtCore.Signal()
    m_clicked = QtCore.Signal()
    DEFAULT_LONGPRESS_INTERVAL = 350
    DEFAULT_AUTO_REPEAT_INTERVAL = 60
    DEFAULT_DISABLE_INTERVAL = 5000
    def __init__( self, parent = None ) :
        QtGui.QPushButton.__init__( self, parent )
        self.timer = QtCore.QTimer()
        self.disable_timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.disable_timer.timeout.connect( self.disable_timeout )
        self.longpress_interval = self.DEFAULT_LONGPRESS_INTERVAL
        self.auto_repeat_interval = self.DEFAULT_AUTO_REPEAT_INTERVAL
        self.pressed.connect( self.m_slot_press )
        self.released.connect( self.m_slot_release )
        self.clicked.connect( self.m_slot_click )
        self.auto_repeat = False
        self.auto_repeat_flag = False
        self.pause_auto_repeat_flag = False
        self.need_cancel_pause_auto_repeat_flag = False
        self.disable_flag = False
        self.longpress_flag = False
    def enableAutoRepeat( self ) :
        self.auto_repeat = True
    def disableAutoRepeat( self ) :
        self.auto_repeat = False
    def disable( self, disable_interval = DEFAULT_DISABLE_INTERVAL ) :
        self.disable_flag = True
        self.disable_timer.start( disable_interval )
    def pause_auto_repeat( self, disable_interval = DEFAULT_DISABLE_INTERVAL ) :
        if self.auto_repeat_flag :
            self.pause_auto_repeat_flag = True
            self.disable( disable_interval )
    @QtCore.Slot()
    def disable_timeout( self ) :
        self.disable_timer.stop()
        self.disable_flag = False
    @QtCore.Slot()
    def timeout( self ) :
        #self.timer.stop()
        if not self.disable_flag :
            if self.auto_repeat == True :
                if not self.auto_repeat_flag :
                    self.auto_repeat_flag = True
                self.m_clicked.emit()
                self.timer.start( self.auto_repeat_interval )
            else :
                self.longpress_flag = True
                self.m_longpressed.emit()
    @QtCore.Slot()
    def m_slot_press( self ) :
        if not self.disable_flag :
            self.longpress_flag = False
            self.timer.stop()
            self.timer.start( self.longpress_interval )
    @QtCore.Slot()
    def m_slot_release( self ) :
        self.timer.stop()
        self.auto_repeat_flag = False
        if self.pause_auto_repeat_flag :
            self.pause_auto_repeat_flag = False
            self.need_cancel_pause_auto_repeat_flag = True
    @QtCore.Slot()
    def m_slot_click( self ) :
        if not self.longpress_flag and not self.disable_flag :
            self.m_clicked.emit()
        if self.need_cancel_pause_auto_repeat_flag :
            self.need_cancel_pause_auto_repeat_flag = False
            self.disable_timeout()

class NumPadKey( Key ) :
    def __init__( self, keycode, parent ) :
        Key.__init__( self, keycode, parent )
    
