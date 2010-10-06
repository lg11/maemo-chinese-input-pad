#-!- coding=utf-8 -!-

from PySide import QtCore, QtGui
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import sys

from uiq_base import NumPadKey

class Conn( QtCore.QObject ) :
    def __init__( self ):
        QtCore.QObject.__init__( self )
        self.code = ""
        bus = dbus.SessionBus()
        self.backend = bus.get_object( 'me.maemo_chinese_input_pad.backend', '/' )
        self.iface = dbus.Interface( self.backend, "me.maemo_chinese_input_pad.backend" )
        self.iface.connect_to_signal( "new_cand", self.new_cand )
        self.backend.reset()
    @QtCore.Slot(int)
    def slot_append_code( self, code ):
        #print "append_code %d" %( code )
        self.backend.append_code( str(code) )
    def new_cand( self, hanzi_list, pinyin_list, selected_hanzi, selected_pinyin, remained_code ):
        print hanzi_list
        print pinyin_list
        print selected_hanzi
        print selected_pinyin
        print remained_code

        #print "has new cand"
        #cand_list = self.backend.get_cand()
        #print cand_list
        #for i in range( len(cand_list) - 1 ):
            #print cand_list[i]

class CandPad( QtGui.QWidget ) :
    LABEL_WIDTH = 320
    LABEL_HEIGHT = 60
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        self.code = ""
        self.code_label = QtGui.QLabel( self )
        self.code_label.resize( self.LABEL_WIDTH, self.LABEL_HEIGHT )
    @QtCore.Slot(int)
    def slot_append_code( self, code ):
        #print code
        self.code = self.code + str(code)
        self.code_label.setText( self.code )
        #self.repaint()


class NumPad( QtGui.QWidget ):
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 96
    BUTTON_HEIGHT_LITE = 68
    CODE_CHECK = 10
    CODE_BACKSPACE = 11
    CODE_MODE = 12

    append_code = QtCore.Signal(int)
    def __init__( self, parent = None ):
        QtGui.QWidget.__init__( self, parent )
        
        self.num_button = []
        #check button
        button = NumPadKey( self, self.CODE_CHECK )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( 0, 0 )
        button.key_clicked.connect( self.slot_key_clicked )
        #backspace button
        button = NumPadKey( self, self.CODE_BACKSPACE )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH, 0 )
        button.key_clicked.connect( self.slot_key_clicked )
        #mode button
        button = NumPadKey( self, self.CODE_MODE )
        button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT_LITE )
        button.move( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        button.key_clicked.connect( self.slot_key_clicked )
        #button 0
        button = NumPadKey( self, 0 )
        button.resize( self.BUTTON_WIDTH * 2, self.BUTTON_HEIGHT_LITE )
        button.move( 0, self.BUTTON_HEIGHT * 3 + self.BUTTON_HEIGHT_LITE )
        button.key_clicked.connect( self.slot_key_clicked )
        self.num_button.append( button )
        #button 1 - 9
        for i in range(3):
            for j in range(3):
                button = NumPadKey( self, i * 3 + j + 1 )
                button.resize( self.BUTTON_WIDTH, self.BUTTON_HEIGHT )
                button.move( self.BUTTON_WIDTH * j, self.BUTTON_HEIGHT * i + self.BUTTON_HEIGHT_LITE )
                button.key_clicked.connect( self.slot_key_clicked )
                self.num_button.append( button )
    @QtCore.Slot(int)
    def slot_key_clicked( self, code ):
        #print "key_clicked"
        #print code
        if code >= 2 and code <= 9:
            self.append_code.emit(code)


class App( dbus.service.Object ): 
    def __init__( self ):
        dbus.mainloop.glib.DBusGMainLoop( set_as_default=True )
        self.bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName( 'me.maemo_chinese_input_pad.ui', self.bus )
        dbus.service.Object.__init__( self, self.bus_name, '/' )

        self.qapp = QtGui.QApplication( sys.argv )
        style_string = "QWidget { background-color: gray }"
        style_string = style_string + "QPushButton { border: 5px solid gray; border-radius: 0px; background-color: qlineargradient(x1: 0, y1: 0.15, x2: 0, y2: 0.18, stop: 0 #f6f7fa, stop: 1 #dadbde); min-width: 80px; }"
        style_string = style_string + "QPushButton:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.7, stop: 0 #5566ee, stop: 1 #f6f7fa); }"
        self.qapp.setStyleSheet( style_string )

        #win = QtGui.QWidget( None, QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint )
        self.win = QtGui.QWidget()
        self.win.resize( 800, 480 )
        self.pad = NumPad( self.win )
        self.pad.move( 340, 0 )
     
        self.cand = CandPad( self.win )
        self.cand.move( 0, 0 )

        self.conn = Conn()
        self.pad.append_code.connect( self.conn.slot_append_code )

    def run( self ):
        self.win.show()
        sys.exit( self.qapp.exec_() )

if __name__ == "__main__" :
    app = App()
    app.run()




    #pad.grabMouse()

