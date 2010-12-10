#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

class LongPressButton( QtGui.QPushButton ):
    longpressed = QtCore.Signal()
    DEFAULT_TIMEOUT_VALVE = 350
    def __init__( self, parent = None ):
        QtGui.QPushButton.__init__( self, parent )
        self.timeout_valve = self.DEFAULT_TIMEOUT_VALVE
        self.longpress_flag = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.pressed.connect( self.slot_press )
        self.released.connect( self.slot_release )
        self.auto_repeat = False
        self.auto_repeat_flag = False
        #self.clicked.connect( self.slot_click )
    def enableAutoRepeat( self ) :
        self.auto_repeat = True
    def disableAutoRepeat( self ) :
        self.auto_repeat = False
    @QtCore.Slot()
    def timeout( self ):
        self.longpress_flag = True
        self.timer.stop()
        self.longpressed.emit()
        #print "longpress"
    @QtCore.Slot()
    def slot_press( self ):
        self.longpress_flag = False
        #self.timer.stop()
        self.timer.start( self.timeout_valve )
        #print "press"
    @QtCore.Slot()
    def slot_release( self ):
        self.timer.stop()
        #if self.hitButton( self.mapFromGlobal( self.cursor().pos() ) ) == False and self.longpress_flag == False :
            #self.clicked.emit()
        #print "release"
    #@QtCore.Slot()
    #def slot_click( self ):
        #print "click"

class NumPadKey( LongPressButton ):
    key_clicked = QtCore.Signal(int)
    key_longpressed = QtCore.Signal(int)
    def __init__( self, parent, code ):
        LongPressButton.__init__( self, parent )
        self.code = code
        self.clicked.connect( self.slot_click )
        self.longpressed.connect( self.slot_longpress )
    @QtCore.Slot()
    def slot_click( self ):
        #print "click"
        if self.longpress_flag == False :
            self.key_clicked.emit( self.code )
    @QtCore.Slot()
    def slot_longpress( self ):
        #print "longpress"
        self.key_longpressed.emit( self.code )
    
