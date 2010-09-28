#-!- coding=utf-8 -!-

import gtk
import gobject
import pango
import backend
#import hildon

class LongPressButton( gtk.Button ):
    __gsignals__ = { 'longpressed': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()), }
    DEFAULT_TIMEOUT_VALVE = 350
    def __init__(self):
        gtk.Button.__init__(self)
        #self.set_name("hildon-accept-button-finger")
        self.timeout_valve = self.DEFAULT_TIMEOUT_VALVE
        self.longpressed_stamp = 0
        self.longpressed_flag = False
        self.connect( "pressed", self.cb_pressed )
        self.connect( "released", self.cb_released )
        #gobject.signal_new( "longpressed", LongPressButton, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () )
    def timeout( self, longpressed_stamp ):
        if self.longpressed_stamp == longpressed_stamp :
            self.longpressed_flag = True
            self.emit( "longpressed" )
    def cb_released( self, widget ):
        self.longpressed_flag = False
        self.longpressed_stamp = self.longpressed_stamp + 1
        if self.longpressed_stamp > 65535:
            self.longpressed_stamp = 0
    def cb_pressed( self, widget ):
        self.longpressed_stamp = self.longpressed_stamp + 1
        if self.longpressed_stamp > 65535:
            self.longpressed_stamp = 0
        gobject.timeout_add( self.timeout_valve, self.timeout, self.longpressed_stamp )
    

class LabelButton( LongPressButton ):
    def __init__( self, label, index = -1 ):
        LongPressButton.__init__(self)
        self.label = gtk.Label()
        self.label.get_layout().set_wrap(pango.WRAP_CHAR)
        #print self.label.get_layout().get_wrap()
        self.label.set_line_wrap(True)
        self.label.set_width_chars(10)
        self.label.set_text(label)
        self.label.show()
        self.add(self.label)

        self.index = index
        self.enable_flag = True
    def recover(self):
        #print "recover"
        self.enable_flag = True
    def set_disable( self, timeout = 350 ):
        self.enable_flag = False
        gobject.timeout_add( timeout, self.recover  )

class CandWin(gtk.Window):
    def __init__( self, text_view ):
        gtk.Window.__init__( self, gtk.WINDOW_POPUP )
        self.text_view = text_view
        width = text_view.get_size_request()[0]
        height = text_view.get_size_request()[1] / 3
        self.set_size_request( width, height )
        self.set_decorated( False )
    def update( self ):
        pass
