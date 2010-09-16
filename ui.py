#-!- coding=utf-8 -!-

import gtk
import gobject
import pango
import backend

#class Dis( gtk.Label )

def buffer_append( widget, ipad, data ):
    ipad.backend.append( data )
    ipad.backend.search()
    ipad.update()
            
def buffer_backspace( widget, ipad ):
    ipad.backend.backspace()
    ipad.update()

def cb_backspace( widget, ipad ):
    if len( ipad.backend.buffer ) > 0:
        if ipad.mode == 1:
            ipad.mode = 0
        buffer_backspace( widget, ipad )
        #ipad.pad.cand_page_index = 0
    else:
        pass
        #text = ipad.l_text.get_text()
        #if len(text) > 0:
            #text = text.decode('utf8')
            #text = text[:-1]
            #ipad.l_text.set_text(text)

def cb_quit( widget ):
    gtk.main_quit()

def select_cand( ipad, i ):
    #ipad.l_text.set_text( ipad.l_text.get_text() + ipad.pad.cand_button[i].label.get_text() )
    ipad.mode = 0
    ipad.backend.reset()
    for i in range(6):
        ipad.npad.cand_button[i].label.set_text( ipad.npad.cand_button_label[i] )
    ipad.l_pinyin.set_text("")
    ipad.l_hanzi.set_text("")

def next_cand(ipad):
    ipad.backend.cand.next_page()
    ipad.pad.update()

def prev_cand(ipad):
    ipad.backend.cand.prev_page()
    ipad.pad.update()

def cb_pad_click( widget, ipad, data ):
    if ipad.mode == 0:
        if data == "1":
            ipad.mode = 1
        else:
            buffer_append( widget, ipad, data )
            #ipad.pad.cand_page_index = 0
    elif ipad.mode == 1:
        if data == "8":
            ipad.mode = 0
        else:
            if data == "1":
                select_cand( ipad, 0 )
            elif data == "2":
                select_cand( ipad, 1 )
            elif data == "3":
                select_cand( ipad, 2 )
            elif data == "4":
                select_cand( ipad, 3 )
            elif data == "5":
                select_cand( ipad, 4 )
            elif data == "6":
                select_cand( ipad, 5 )
            elif data == "9":
                next_cand( ipad )
            elif data == "7":
                prev_cand( ipad )
            else:
                pass
    else:
        pass

def cb_copy( widget, ipad ):
    ipad.clipboard.set_text( ipad.l_text.get_text() )

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

class NumPad( gtk.Frame ):
    def __init__( self, ipad ):
        gtk.Frame.__init__(self)
        self.ipad = ipad
        #self.set_size_request( 375, 270 )
        self.button_list = []
        t = gtk.Table( 3, 3 )
        t.set_row_spacings(0)
        t.set_col_spacings(0)
        self.add(t)
        for i in range(3):
            for j in range(3):
                b = LabelButton( str(i*3+j+1) )
                b.set_size_request(145,110)
                b.connect( "clicked", cb_pad_click, ipad, str(i*3+j+1) )
                t.attach( b, j, j+1, i, i+1 )
                b.show()
                self.button_list.append(b)
        t.show()
        self.cand_button = []
        self.cand_button.append( self.button_list[0] )
        self.cand_button.append( self.button_list[1] )
        self.cand_button.append( self.button_list[2] )
        self.cand_button.append( self.button_list[3] )
        self.cand_button.append( self.button_list[4] )
        self.cand_button.append( self.button_list[5] )
        self.cand_button_label = []
        self.cand_button_label.append( "1" )
        self.cand_button_label.append( "2" )
        self.cand_button_label.append( "3" )
        self.cand_button_label.append( "4" )
        self.cand_button_label.append( "5" )
        self.cand_button_label.append( "6" )
    def update(self):
        cand = self.ipad.backend.cand
        for i in range(6):
            if cand.list[i]:
                self.cand_button[i].label.set_text( cand.list[i][1] )
            else:
                self.cand_button[i].label.set_text( self.cand_button_label[i] )
        
class ChineseInputPad( gtk.Frame ):
    def __init__(self):
        gtk.Frame.__init__(self)
        self.backend = backend.Backend(self)
        self.layout = gtk.Fixed()
        self.npad = NumPad( self )
        self.add(self.layout)
        self.layout.put(self.npad,0,90)
        self.npad.show()
        self.layout.show()

        self.l_hanzi = gtk.Label()
        self.l_pinyin = gtk.Label()
        self.l_hanzi.set_size_request(320,50)
        self.l_pinyin.set_size_request(320,50)
        self.layout.put( self.l_pinyin, 0, 5 )
        self.layout.put( self.l_hanzi, 0, 40 )
        self.l_pinyin.show()
        self.l_hanzi.show()

        self.bc_b = gtk.Button("退格")
        self.bc_b.set_size_request( 135, 75 )
        self.layout.put( self.bc_b, 320, 10 )
        self.bc_b.show()
        self.bc_b.connect( "clicked", cb_backspace, self )

        self.mode = 0

    def update(self):
        print "update"
        cand = self.backend.cand
        cand.reset()
        cand.update()
        if cand.list[0]:
            py = cand.list[0][0] + "'" + self.backend.buffer[cand.query_index:]
            hz = cand.list[0][1] + "'" + self.backend.buffer[cand.query_index:]
            self.l_pinyin.set_text(py)
            self.l_hanzi.set_text(hz)
        else:
            self.l_pinyin.set_text(self.backend.buffer)
            self.l_hanzi.set_text(self.backend.buffer)
        self.npad.update()

    def request_update(self):
        print "request"
        gobject.idle_add( self.update )

class InputPad( gtk.Frame ):
    def __init__(self):
        gtk.Frame.__init__(self)
        self.layout = gtk.Fixed()
        self.cipad = ChineseInputPad()
        self.layout.put(self.cipad,330,0)
        self.add(self.layout)
        
        #self.l_code = gtk.Label()
        #self.l_code.set_size_request(320,75)
        #self.layout.put( self.l_code, 340, 360 )
        #self.l_code.show()

        self.l_text = gtk.Label()
        self.l_text.set_size_request(320,240)
        self.l_text.get_layout().set_wrap(pango.WRAP_CHAR)
        self.l_text.set_line_wrap(True)
        self.l_text.set_width_chars(30)
        self.l_text.set_text("")
        self.l_text.show()
        self.layout.put( self.l_text, 10, 10 )

        self.cp_b = gtk.Button("复制到剪切板")
        self.cp_b.set_size_request( 200, 90 )
        self.layout.put( self.cp_b, 70, 300 )
        self.cp_b.show()
        self.cp_b.connect( "clicked", cb_copy, self )

        self.cipad.show()
        self.layout.show()
        #self.win.show()
        #self.win.connect( "destroy", cb_quit )

        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

class App():
    def __init__(self):
        gtk.gdk.threads_init()
        self.win = gtk.Window()
        self.ipad = InputPad()
        self.win.add(self.ipad)
        self.ipad.show()
        self.win.show()
        self.win.connect( "destroy", cb_quit )
    def run(self):
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()


if __name__ == "__main__":
    app = App()
    app.run()


