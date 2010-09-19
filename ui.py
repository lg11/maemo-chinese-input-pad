#-!- coding=utf-8 -!-

import gtk
import gobject
import pango
from backend import Backend, QueryCache
from ui_base import LabelButton

def cb_backspace( widget, ipad ):
    if len( ipad.backend.code ) > 0:
        if ipad.mode == 1:
            #print "shorter"
            ipad.backend.cand.shorter()
            ipad.backend.cand.reset_page()
            #print ipad.backend.cand.query_index
            if ipad.backend.cand.query_index < 1:
                ipad.mode = 0
                ipad.backend.cand.longest()
            ipad.backend.cand.update()
        elif ipad.mode == 0:
            ipad.backend.backspace_code()
            ipad.backend.cand.longest()
            ipad.backend.cand.reset_page()
            ipad.backend.cand.update()
        ipad.update()
    else:
        text = ipad.text_label.get_text()
        if len(text) > 0:
            text = text.decode('utf8')
            text = text[:-1]
            ipad.text_label.set_text(text)

def cb_pad_click( widget, ipad, data ):
    if ipad.mode == ipad.MODE_INPUT:
        if data == "1":
            if len(ipad.backend.code) == 0:
                ipad.mode = ipad.MODE_PUNC
                ipad.update()
            else:
                ipad.mode = ipad.MODE_SELECT
                ipad.update()
        else:
            ipad.backend.append_code( data )
            ipad.update()
    elif ipad.mode == ipad.MODE_SELECT:
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
            ipad.backend.cand.update()
            ipad.update()
        elif data == "7":
            ipad.backend.cand.prev_page()
            ipad.backend.cand.update()
            ipad.update()
        elif data == "8":
            ipad.commit()
        else:
            pass
    elif ipad.mode == ipad.MODE_PUNC:
        if data == "1":
            ipad.commit_punc( 0 )
        elif data == "2":
            ipad.commit_punc( 1 )
        elif data == "3":
            ipad.commit_punc( 2 )
        elif data == "4":
            ipad.commit_punc( 3 )
        elif data == "5":
            ipad.commit_punc( 4 )
        elif data == "6":
            ipad.commit_punc( 5 )
        elif data == "9":
            ipad.next_punc()
            ipad.update()
        elif data == "7":
            ipad.prev_punc()
            ipad.update()
        elif data == "8":
            pass
        else:
            pass
    else:
        pass

class NumPad( gtk.Frame ):
    button_label = [ \
            ["1","2","3","4","5","6","7","8","9"]\
            ,\
            ["1","2","3","4","5","6","7","8","9"]\
            ]
    def __init__( self, ipad ):
        gtk.Frame.__init__(self)
        self.ipad = ipad
        self.button = []
        t = gtk.Table( 3, 3 )
        t.set_row_spacings(0)
        t.set_col_spacings(0)
        self.add(t)
        for i in range(3):
            for j in range(3):
                b = LabelButton(self.button_label[0][i*3+j])
                b.set_size_request(145,110)
                b.connect( "clicked", cb_pad_click, ipad, self.button_label[0][i*3+j] )
                t.attach( b, j, j+1, i, i+1 )
                b.show()
                self.button.append(b)
        t.show()
    def update(self):
        cand = self.ipad.backend.cand
        if self.ipad.mode == self.ipad.MODE_PUNC:
            for i in range(6):
                self.button[i].label.set_text( self.ipad.punc_list[self.ipad.punc_index][i] )
        else:
            for i in range(6):
                if cand.list[i]:
                    self.button[i].label.set_text( cand.list[i][3] )
                else:
                    self.button[i].label.set_text( self.button_label[0][i] )
        
class ChineseInputPad( gtk.Frame ):
    punc_list = [ \
            ["，","。","？","“","”","……"]\
            ,\
            ["！","（","）","～","《","》"]\
            ]
    MODE_INPUT = 0
    MODE_SELECT = 1
    MODE_PUNC = 2
    def __init__( self, text_label ):
        gtk.Frame.__init__(self)
        self.backend = Backend(self)
        self.layout = gtk.Fixed()
        self.npad = NumPad( self )
        self.add(self.layout)
        #self.layout.put(self.npad,0,90)
        self.layout.put(self.npad,0,90)
        self.npad.show()
        self.layout.show()

        self.l_hanzi = gtk.Label()
        self.l_pinyin = gtk.Label()
        self.l_hanzi.set_size_request(290,50)
        self.l_pinyin.set_size_request(290,50)
        self.layout.put( self.l_pinyin, 0, 5 )
        self.layout.put( self.l_hanzi, 0, 40 )
        self.l_hanzi.set_selectable(True)
        self.l_pinyin.set_selectable(True)
        self.l_pinyin.show()
        self.l_hanzi.show()

        self.bc_b = gtk.Button("退格")
        self.bc_b.set_size_request( 145, 75 )
        self.layout.put( self.bc_b, 290, 10 )
        self.bc_b.show()
        self.bc_b.connect( "clicked", cb_backspace, self )

        self.mode = self.MODE_INPUT
        self.punc_index = 0

        self.text_label = text_label
    def update(self):
        cand = self.backend.cand
        cand_py = ""
        cand_hz = ""
        if cand.list[0]:
            cand_hz = cand.list[0][QueryCache.IDX_HANZI] + "'"
            cand_py = cand.list[0][QueryCache.IDX_PINYIN] + "'"
        if self.mode == self.MODE_INPUT:
            py = cand_py + self.backend.code[cand.query_index:]
            hz = cand_hz + self.backend.code[cand.query_index:]
            self.l_pinyin.set_text(py)
            self.l_hanzi.set_text(hz)
        elif self.mode == self.MODE_SELECT:
            selected_text = ""
            for item in self.backend.selected:
                selected_text = selected_text + item[QueryCache.IDX_HANZI]
            py = selected_text + cand_py + self.backend.code[cand.query_index:]
            hz = selected_text + cand_hz + self.backend.code[cand.query_index:]
            self.l_pinyin.set_text(py)
            self.l_hanzi.set_text(hz)
            self.l_hanzi.select_region(len(selected_text),len(selected_text)+len(cand_hz)-1)
        self.npad.update()
    def cand_update(self):
        #print "cand update"
        cand = self.backend.cand
        cand.longest()
        cand.reset_page()
        cand.update()
        self.update()
    def request_update(self):
        #print "request"
        gobject.idle_add( self.cand_update )
    def select( self, i ):
        self.backend.cand.select(i)
        if len( self.backend.code ) < 1:
            self.commit()
    def reset(self):
        self.mode = self.MODE_INPUT
        self.punc_index = 0
        self.update()
    def commit(self):
        text = self.backend.cand.commit()
        self.text_label.set_text( self.text_label.get_text() + text )
        self.reset()
    def commit_punc( self, i ):
        self.text_label.set_text( self.text_label.get_text() + self.punc_list[self.punc_index][i] )
        self.reset()
    def next_punc(self):
        self.punc_index = self.punc_index + 1
        if self.punc_index > 1:
            self.punc_index = 1
        self.update()
    def prev_punc(self):
        self.punc_index = self.punc_index - 1
        if self.punc_index < 0:
            self.punc_index = 0
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

        l_empty = gtk.Label()
        self.layout.put( l_empty, 0, 0 )
        l_empty.show()
        l_empty.set_selectable(True)

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


