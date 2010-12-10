#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

class m_key( QtGui.QPushButton ) :
    m_longpressed = QtCore.Signal()
    m_clicked = QtCore.Signal()
    DEFAULT_LONGPRESS_INTERVAL = 350
    DEFAULT_AUTO_REPEAT_INTERVAL = 90
    DEFAULT_DISABLE_INTERVAL = 150
    def __init__( self, parent = None ) :
        QtGui.QPushButton.__init__( self, parent )
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.longpress_interval = self.DEFAULT_LONGPRESS_INTERVAL
        self.auto_repeat_interval = self.DEFAULT_AUTO_REPEAT_INTERVAL
        self.disable_interval = self.DEFAULT_DISABLE_INTERVAL
        self.pressed.connect( self.m_slot_press )
        self.released.connect( self.m_slot_release )
        self.clicked.connect( self.m_slot_click )
        self.auto_repeat = False
        self.disable_flag = False
        self.longpress_flag = False
    def enableAutoRepeat( self ) :
        self.auto_repeat = True
    def disableAutoRepeat( self ) :
        self.auto_repeat = False
    def disable( self ) :
        self.timer.stop()
        self.longpress_flag = False
        self.disable_flag = True
        self.timer.start( self.disable_interval )
    @QtCore.Slot()
    def timeout( self ) :
        self.timer.stop()
        if self.disable_flag :
            self.disable_flag = False
        elif self.auto_repeat == True :
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
        if not self.disable_flag :
            self.timer.stop()
    @QtCore.Slot()
    def m_slot_click( self ) :
        if not self.longpress_flag and not self.disable_flag :
            self.m_clicked.emit()

class NumPadKey( m_key ) :
    key_clicked = QtCore.Signal(int)
    key_longpressed = QtCore.Signal(int)
    def __init__( self, parent, code ) :
        m_key.__init__( self, parent )
        self.code = code
        self.m_clicked.connect( self.slot_click )
        self.m_longpressed.connect( self.slot_longpress )
    @QtCore.Slot()
    def slot_click( self ) :
        self.key_clicked.emit( self.code )
    @QtCore.Slot()
    def slot_longpress( self ) :
        self.key_longpressed.emit( self.code )
    
