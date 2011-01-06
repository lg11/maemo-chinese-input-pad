#-!- coding=utf-8 -!-

#from PySide import QtCore, QtGui
from PyQt4 import QtCore, QtGui
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

#from widget import Key

class Post( QtGui.QPushButton ) :
    HEIGHT = 55
    longpressed = QtCore.Signal( int )
    clicked = QtCore.Signal( int )
    sticked = QtCore.Signal( int )
    unsticked = QtCore.Signal( int )
    DEFAULT_LONGPRESS_INTERVAL = 350
    def __init__( self, id, parent = None ) :
        QtGui.QPushButton.__init__( self, parent )

        self.PALETTE = self.palette()
        color = self.PALETTE.text().color()
        color.setAlpha( 125 )
        self.PALETTE.setColor( QtGui.QPalette.ButtonText, color )
        
        self.label = QtGui.QLabel( self )
        self.stick = QtGui.QLabel( self )

        self.focus = None

        layout = QtGui.QHBoxLayout()
        layout.setSpacing( 3 )
        layout.setContentsMargins( 8, 0, 15, 0 )
        layout.addWidget( self.stick )
        layout.addWidget( self.label )
        layout.addStretch()
        self.setLayout( layout )

        self.stick.setText( u"◇" )
        self.stick.setPalette( self.PALETTE )

        self.text = self.label.text
        self.start_pos = QtCore.QPoint( 0, 0 )
        self.flag = False
        self.id = id
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.timeout )
        self.longpress_interval = self.DEFAULT_LONGPRESS_INTERVAL
    def setText( self, text ) :
        self.label.setText( text )
    def mousePressEvent( self, event ) :
        self.setDown( True )
        self.timer.start( self.longpress_interval )
        self.start_pos = event.pos()
    def set( self, flag ) :
        if flag :
            self.sticked.emit( self.id )
            self.stick.setText( u"◆" )
            self.flag = True
        else :
            self.stick.setText( u"◇" )
            self.unsticked.emit( self.id )
            self.flag = False
    def mouseReleaseEvent( self, event ) :
        if self.timer.isActive() :
            self.setDown( False )
            self.timer.stop()
            pos = event.pos()
            if pos.x() < self.HEIGHT * 1.5 or self.start_pos.x() < self.HEIGHT * 1.5 :
                self.set( not self.flag )
            else :
                self.clicked.emit( self.id )
    @QtCore.Slot()
    def timeout( self ) :
        self.timer.stop()
        self.setDown( False )
        self.longpressed.emit( self.id )
    def set_id( self, id ) :
        self.id = id
    @QtCore.Slot()
    def stop( self ) :
        self.timer.stop()
        self.setDown( False )

class PostPad( QtGui.QWidget ) :
    set = QtCore.Signal( str )
    commit = QtCore.Signal( str )
    def __init__( self, parent = None ) :
        QtGui.QWidget.__init__( self, parent )
        self.post_list = []
        #self.
        self.sticked_count = 0
        #self.lay
    @QtCore.Slot( str )
    def add( self, text ) :
        if len( text ) > 0 :
            if not self.check( text ) :
                index = len( self.post_list )
                post = Post( index, self )
                post.setText( text )
                post.clicked.connect( self.__commit )
                post.longpressed.connect( self.__set )
                post.setFocusProxy( self.focus )
                self.post_list.append( post )
                self.__remap()
    def setFocusProxy( self, proxy ) :
        for post in self.post_list :
            post.setFocusProxy( proxy )
        self.focus = proxy
        QtGui.QWidget.setFocusProxy( self, proxy )
    def __remap( self ) :
        width = self.width()
        height = self.height ()
        y = 0
        index = len( self.post_list ) - 1
        while index >= 0 :
            post = self.post_list[index]
            post.show()
            post.resize( width, post.HEIGHT )
            post.move( 0, y )
            y = y + post.HEIGHT
            index = index - 1
    def resizeEvent( self, event ) :
        self.__remap()
    def check( self, text ) :
        flag = False
        for post in self.post_list :
            if post.text() == text :
                flag = True
                break
        return flag
    @QtCore.Slot()
    def stop( self ) :
        for post in self.post_list :
            post.stop()
    @QtCore.Slot( int )
    def __commit( self, id ) :
        text = self.post_list[id].text()
        self.commit.emit( text )
    @QtCore.Slot( int )
    def __set( self, id ) :
        text = self.post_list[id].text()
        self.set.emit( text )


if __name__ == "__main__" :
    import sys
    app = QtGui.QApplication( sys.argv )

    pad = PostPad()
    cb = app.clipboard()
    text = cb.text( cb.Clipboard )
    if len( text ) > 0 :
        pad.add( text )
    text = cb.text( cb.Selection )
    if len( text ) > 0 :
        pad.add( text )
    pad.add( "tststtttydhdydhgdhndhyudhyudhyudhudhydbhyhbhyhghybghyhghyhhyhhyhhyuhyuhujnhju" )
    pad.add( "tstst" )
    pad.show()
    sys.exit( app.exec_() )
