#-!- coding=utf-8 -!-

import gtk
import pango
import pinyin

#class Dis( gtk.Label )

def buffer_append( widget, app, data ):
    app.buffer.append( data )
    app.l_code.set_text( app.buffer.buffer )
    app.buffer.search()
    i = len( app.buffer.buffer )
    rs = app.buffer.query[i]
    while rs == None and i > 0 :
        i = i - 1
        rs = app.buffer.query[i]
    app.pad.current_query_index = i
    if rs:
        r = rs[0]
        py = r[0] + "'" + app.buffer.buffer[i:]
        hz = r[1] + "'" + app.buffer.buffer[i:]
        app.l_pinyin.set_text(py)
        app.l_hanzi.set_text(hz)
        for i in range(5):
            if i < len(rs):
                app.pad.cand_button[i].label.set_text( rs[i][1] )
            else:
                app.pad.cand_button[i].label.set_text( app.pad.cand_button_label[i] )
    else:
        py = app.buffer.buffer
        hz = app.buffer.buffer
        app.l_pinyin.set_text(py)
        app.l_hanzi.set_text(hz)
        for i in range(5):
            app.pad.cand_button[i].label.set_text( app.pad.cand_button_label[i] )
            
def buffer_backspace( widget, app ):
    app.buffer.backspace()
    #print app.buffer.buffer
    app.l_code.set_text( app.buffer.buffer )
    #app.buffer.search()
    i = len( app.buffer.buffer )
    rs = app.buffer.query[i]
    while rs == None and i > 0 :
        i = i - 1
        rs = app.buffer.query[i]
    app.pad.current_query_index = i
    if rs:
        r = rs[0]
        py = r[0] + "'" + app.buffer.buffer[i:]
        hz = r[1] + "'" + app.buffer.buffer[i:]
        app.l_pinyin.set_text(py)
        app.l_hanzi.set_text(hz)
        for i in range(5):
            if i < len(rs):
                app.pad.cand_button[i].label.set_text( rs[i][1] )
            else:
                app.pad.cand_button[i].label.set_text( app.pad.cand_button_label[i] )
    else:
        py = app.buffer.buffer
        hz = app.buffer.buffer
        app.l_pinyin.set_text(py)
        app.l_hanzi.set_text(hz)
        for i in range(5):
            app.pad.cand_button[i].label.set_text( app.pad.cand_button_label[i] )

def cb_backspace( widget, app ):
    if len( app.buffer.buffer ) > 0:
        if app.pad.mode == 1:
            app.pad.mode = 0
        buffer_backspace( widget, app )
        app.pad.cand_page_index = 0
    else:
        text = app.l_text.get_text()
        if len(text) > 0:
            text = text.decode('utf8')
            text = text[:-1]
            app.l_text.set_text(text)

def cb_quit( widget ):
    gtk.main_quit()

def select_cand( app, i ):
    app.l_text.set_text( app.l_text.get_text() + app.pad.cand_button[i].label.get_text() )
    app.pad.mode = 0
    app.pad.cand_page_index = 0
    app.pad.current_query_index = 0
    app.buffer.reset()
    for i in range(5):
        app.pad.cand_button[i].label.set_text( app.pad.cand_button_label[i] )
    app.l_code.set_text("")
    app.l_pinyin.set_text("")
    app.l_hanzi.set_text("")

def next_cand(app):
    i = app.pad.current_query_index
    if i > 0:
        j = app.pad.cand_page_index + 1
        rs = app.buffer.query[i]
        if j*5 >= len( rs ):
            #print "pass"
            #print len(rs)
            pass
        else:
            #print "next"
            app.pad.cand_page_index = j
            for k in range(5):
                l = j * 5 + k
                if l < len(rs):
                    app.pad.cand_button[k].label.set_text( rs[l][1] )
                else:
                    app.pad.cand_button[k].label.set_text( app.pad.cand_button_label[k] )

def prev_cand(app):
    i = app.pad.current_query_index
    if i > 0:
        j = app.pad.cand_page_index - 1
        if j >= 0:
            rs = app.buffer.query[i]
            app.pad.cand_page_index = j
            for k in range(5):
                l = j*5+k
                if l < len(rs):
                    app.pad.cand_button[k].label.set_text( rs[l][1] )
                else:
                    app.pad.cand_button[k].label.set_text( app.pad.cand_button_label[k] )

def cb_pad_click( widget, app, data ):
    if app.pad.mode == 0:
        if data == "1":
            app.pad.mode = 1
        else:
            buffer_append( widget, app, data )
            app.pad.cand_page_index = 0
    elif app.pad.mode == 1:
        if data == "1":
            app.pad.mode = 0
        else:
            if data == "5":
                select_cand( app, 0 )
            elif data == "4":
                select_cand( app, 1 )
            elif data == "6":
                select_cand( app, 2 )
            elif data == "2":
                select_cand( app, 3 )
            elif data == "8":
                select_cand( app, 4 )
            elif data == "9":
                next_cand( app )
            elif data == "7":
                prev_cand( app )
            else:
                pass
    else:
        pass

def cb_copy( widget, app ):
    app.clipboard.set_text( app.l_text.get_text() )

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

class Pad( gtk.Frame ):
    def __init__( self, app ):
        gtk.Frame.__init__(self)
        self.app = app
        self.set_size_request( 375, 270 )
        self.button_list = []
        t = gtk.Table( 3, 3 )
        self.add(t)
        for i in range(3):
            for j in range(3):
                b = LabelButton( str(i*3+j+1) )
                b.connect( "clicked", cb_pad_click, app, str(i*3+j+1) )
                t.attach( b, j, j+1, i, i+1 )
                b.show()
                self.button_list.append(b)
        t.show()
        self.mode = 0
        self.cand_button = []
        self.cand_button.append( self.button_list[4] )
        self.cand_button.append( self.button_list[3] )
        self.cand_button.append( self.button_list[5] )
        self.cand_button.append( self.button_list[1] )
        self.cand_button.append( self.button_list[7] )
        self.cand_button_label = []
        self.cand_button_label.append( "5" )
        self.cand_button_label.append( "4" )
        self.cand_button_label.append( "6" )
        self.cand_button_label.append( "2" )
        self.cand_button_label.append( "8" )
        self.cand_page_index = 0
        self.current_query_index = 0


class App():
    def __init__( self ):
        self.win = gtk.Window()
        self.layout = gtk.Fixed()
        self.pad = Pad( self )
        self.layout.put(self.pad,340,100)
        self.win.add(self.layout)
        
        self.l_code = gtk.Label()
        self.l_hanzi = gtk.Label()
        self.l_pinyin = gtk.Label()
        self.l_code.set_size_request(320,75)
        self.l_hanzi.set_size_request(320,50)
        self.l_pinyin.set_size_request(320,50)
        self.layout.put( self.l_hanzi, 340, 50 )
        self.layout.put( self.l_pinyin, 340, 0 )
        self.layout.put( self.l_code, 340, 360 )
        self.l_code.show()
        self.l_hanzi.show()
        self.l_pinyin.show()

        self.l_text = gtk.Label()
        self.l_text.set_size_request(320,320)
        self.l_text.get_layout().set_wrap(pango.WRAP_CHAR)
        self.l_text.set_line_wrap(True)
        self.l_text.set_width_chars(30)
        self.l_text.set_text("")
        self.l_text.show()
        self.layout.put( self.l_text, 10, 10 )

        self.bc_b = gtk.Button("退格")
        self.bc_b.set_size_request( 120, 70 )
        self.layout.put( self.bc_b, 650, 15 )
        self.bc_b.show()
        self.bc_b.connect( "clicked", cb_backspace, self )

        self.cp_b = gtk.Button("复制到剪切板")
        self.cp_b.set_size_request( 200, 90 )
        self.layout.put( self.cp_b, 70, 300 )
        self.cp_b.show()
        self.cp_b.connect( "clicked", cb_copy, self )

        self.pad.show()
        self.layout.show()
        self.win.show()
        self.win.connect( "destroy", cb_quit )

        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

        self.buffer = pinyin.Buffer()

    def go(self):
        gtk.main()

if __name__ == "__main__":
    app = App()
    app.go()


