#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

class Control( QtGui.QWidget ) :
    take = QtCore.Signal()
    move = QtCore.Signal( int, int )
    command = QtCore.Signal( int, int )
    def __init__( self, parent = None, flags = QtCore.Qt.WindowFlags() ) :
        QtGui.QWidget.__init__( self, parent, flags )
        self.flag = False
        self.check = self.__check
        self.origin = QtCore.QPoint( 0, 0 )
        self.start = QtCore.QPoint( 0, 0 )
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.check_timer = QtCore.QTimer()
        self.check_timer.timeout.connect( self.check_timeout )
        self.command_timer = QtCore.QTimer()
        self.command_timer.timeout.connect( self.command_timeout )
        self.time = QtCore.QTime()
        self.time.start()
        self.stack = []
    def eventFilter( self, target, event ) :
        if event.type() == QtCore.QEvent.MouseButtonPress :
            self.mousePressEvent( event )
        elif event.type() == QtCore.QEvent.MouseButtonDblClick :
            self.mousePressEvent( event )
        elif event.type() == QtCore.QEvent.MouseButtonRelease :
            self.mouseReleaseEvent( event )
        elif event.type() == QtCore.QEvent.MouseMove :
            self.mouseMoveEvent( event )
        return QtGui.QWidget.eventFilter( self, target, event )
    def mousePressEvent( self, event ) :
        #print "press"
        self.flag = False
        self.origin = event.globalPos()
        self.timer.start( 350 )
        self.check_timer.start( 120 )
        self.command_timer.start( 250 )
        self.time.restart()
        self.stack = []
        #self.stack.append( ( event.pos(), self.time.elapsed() ) )
    def mouseReleaseEvent( self, event ) :
        #print "release"
        self.check_timer.stop()
        self.timer.stop()
        if self.command_timer.isActive() :
            self.command_timer.stop()
            if self.check() :
                pos = event.globalPos()
                dx = pos.x() - self.origin.x()
                dy = pos.y() - self.origin.y()
                d = dx * dx + dy * dy
                if d > 1024 * 3.0 :
                    self.take.emit()
                    self.command.emit( dx, dy )
        else :
            if self.check() :
                if len( self.stack ) > 0 :
                    i = len( self.stack ) - 1
                    time = self.time.elapsed()
                    while i > 0 :
                        old_time = self.stack[i][1]
                        #print i, time - old_time, self.stack[i]
                        if time - old_time > 100 :
                            break
                        else :
                            i = i - 1
                    #print i
                    pos = self.stack[i][0]
                    dx = pos.x() - self.start.x()
                    dy = pos.y() - self.start.y()
                    self.move.emit( dx, dy )

    def __check( self ) :
        return True
    def mouseMoveEvent( self, event ) :
        if self.check() :
            pos = event.globalPos()
            if self.flag :
                #print self.time.elapsed()
                dx = pos.x() - self.start.x()
                dy = pos.y() - self.start.y()
                self.move.emit( dx, dy )
                self.stack.append( ( pos, self.time.elapsed() ) )
            else :
                if self.timer.isActive() :
                    dx = pos.x() - self.origin.x()
                    dy = pos.y() - self.origin.y()
                    d = dx * dx + dy * dy
                    if d > 1024 * 1.0 :
                        if not self.check_timer.isActive() :
                            self.start = ( pos + self.origin ) / 2
                            #print "move", dx, dy
                            self.take.emit()
                            self.flag = True
                            self.stack.append( ( pos, self.time.elapsed() ) )
                    elif d > 1024 * 2.5 :
                        self.start = self.origin
                        #print "move", dx, dy
                        self.take.emit()
                        self.flag = True
                        self.stack.append( ( pos, self.time.elapsed() ) )
    def timeout( self ) :
        self.timer.stop()
    def check_timeout( self ) :
        self.check_timer.stop()
    def command_timeout( self ) :
        self.command_timer.stop()
