#-!- coding=utf-8 -!-

import gtk
import gobject
import pango
import backend

class LabelButton( gtk.Button ):
    def __init__( self, label ):
        gtk.Button.__init__(self)
        self.label = gtk.Label()
        self.label.get_layout().set_wrap(pango.WRAP_CHAR)
        #print self.label.get_layout().get_wrap()
        self.label.set_line_wrap(True)
        self.label.set_width_chars(10)
        self.label.set_text(label)
        self.label.show()
        self.add(self.label)
