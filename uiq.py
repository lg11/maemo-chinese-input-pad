#-!- coding=utf-8 -!-

from PySide import QtCore, QtGui
import sys

from uiq_base import LongPressButton

class CandPad( QtGui.QWidget ):
    LABEL_WIDTH = 320
    LABEL_HEIGHT = 60
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )


class NumPad( QtGui.QWidget ):
    BUTTON_WIDTH = 135
    BUTTON_HEIGHT = 96
    BUTTON_HEIGHT_LITE = 68
    #BUTTON
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        
        self.num_button = []
        #check button
        button = LongPressButton( self )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( 0, 0 )
        #backspace button
        button = LongPressButton( self )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH, 0 )
        #button 0
        button = LongPressButton( self )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( 0, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        self.num_button.append( button )
        #button 1 - 9
        for i in range(3):
            for j in range(3):
                button = LongPressButton( self )
                button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT )
                button.move( self.BUTTON_WIDTH * j, self.BUTTON_HEIGHT * i + self.BUTTON_HEIGHT_LITE )
                self.num_button.append( button )
        #mode button
        button = LongPressButton( self )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
    def key_click( self, code ):
        pass


if __name__ == "__main__" :
    app = QtGui.QApplication( sys.argv )
    style_string = "QWidget { background-color: #f6f7fa }"
    style_string = style_string + "QPushButton { border: 1px solid gray; border-radius: 1px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.1, stop: 0 #f6f7fa, stop: 1 #dadbde); min-width: 80px; }"
    style_string = style_string + "QPushButton:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #5566ee, stop: 1 #f6f7fa); }"
    app.setStyleSheet( style_string )
    #app.setStyleSheet( style_string )


    #win = QtGui.QWidget( None, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
    win = QtGui.QWidget()
    win.resize( 800, 480 )
    pad = NumPad( win )
    pad.move( 340, 0 )

    win.show()

    #pad.grabMouse()

    sys.exit(app.exec_())


