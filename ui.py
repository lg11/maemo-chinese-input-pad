#-!- coding=utf-8 -!-

import gtk
import gobject
import pango
from backend import Backend
from ui_base import LabelButton




def cb_backspace( widget, ipad ):
    if len( ipad.backend.code ) > 0:
        if ipad.mode == 1:
            ipad.mode = 0
        ipad.backend.backspace_code()
        ipad.update()
    else:
        #pass
        text = ipad.text_label.get_text()
        if len(text) > 0:
            text = text.decode('utf8')
            text = text[:-1]
            ipad.text_label.set_text(text)

def cb_pad_click( widget, ipad, data ):
    if ipad.mode == 0:
        if data == "1":
            ipad.mode = 1
        else:
            ipad.backend.append_code( data )
            ipad.update()
    elif ipad.mode == 1:
        if data == "1":
            ipad.select( 0 )
        elif data == "2":
            ipad.select( 1 )
        elif data == "3":
            ipad.select( 2 )
        elif data == "4":
            ipad.select( 3 )
        elif data == "5":
            ipad.select( 4 )
        elif data == "6":
            ipad.select( 5 )
        elif data == "9":
            ipad.backend.cand.next_page()
            ipad.update_ui()
        elif data == "7":
            ipad.backend.cand.prev_page()
            ipad.update_ui()
        elif data == "8":
            ipad.commit()
        else:
            pass
    else:
        pass

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
                self.cand_button[i].label.set_text( cand.list[i][3] )
            else:
                self.cand_button[i].label.set_text( self.cand_button_label[i] )
        
class ChineseInputPad( gtk.Frame ):
    def __init__( self, text_label ):
        gtk.Frame.__init__(self)
        self.backend = Backend(self)
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

        self.text_label = text_label
    def update_ui(self):
        cand = self.backend.cand
        if cand.list[0]:
            py = cand.list[0][2] + "'" + self.backend.code[cand.query_index:]
            hz = cand.list[0][3] + "'" + self.backend.code[cand.query_index:]
            self.l_pinyin.set_text(py)
            self.l_hanzi.set_text(hz)
        else:
            self.l_pinyin.set_text(self.backend.code)
            self.l_hanzi.set_text(self.backend.code)
        self.npad.update()
    def update(self):
        print "update"
        cand = self.backend.cand
        cand.reset()
        cand.update()
        self.update_ui()
        self.npad.update()
    def request_update(self):
        print "request"
        gobject.idle_add( self.update )
    def select( self, i ):
        self.backend.cand.select(i)
        if len( self.backend.code ) < 1:
            self.commit()
    def commit(self):
        print "commit"
        text = ""
        print self.text_label.get_text()
        for item in self.backend.selected:
            text = text + item[3]
        self.text_label.set_text( self.text_label.get_text() + text )
        #self.text_label.set_text( "text" )
        self.backend.reset()
        self.mode = 0
        self.update()

def cb_quit( widget ):
    gtk.main_quit()


def cb_copy( widget, ipad ):
    ipad.clipboard.set_text( ipad.l_text.get_text() )

class InputPad( gtk.Frame ):
    def __init__(self):
        gtk.Frame.__init__(self)
        self.layout = gtk.Fixed()
        self.l_text = gtk.Label()
        self.ipad = ChineseInputPad(self.l_text)
        self.layout.put(self.ipad,330,0)
        self.add(self.layout)

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

        self.ipad.show()
        self.layout.show()

        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

class App():
    def __init__(self):
        self.win = gtk.Window()
        self.ipad = InputPad()
        self.win.add(self.ipad)
        self.ipad.show()
        self.win.show()
        self.win.connect( "destroy", cb_quit )
    def run(self):
        gtk.gdk.threads_init()
        #gtk.gdk.threads_enter()
        gtk.main()
        #gtk.gdk.threads_leave()


if __name__ == "__main__":
    app = App()
    app.run()


