#-!- coding=utf-8 -!-

import gtk
import gobject
import pango

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from backend import Backend, QueryCache
from ui_base import LabelButton
from ui_base import LongPressButton

def cb_button_0( widget, ipad ):
    if widget.enable_flag :
        #print widget.enable_flag
        if ipad.mode == ipad.MODE_INPUT:
            if len( ipad.backend.code ) > 0:
                if len( ipad.backend.code ) == 1:
                    widget.set_disable()
                    #print "disbale"
                ipad.backend.backspace_code()
                ipad.backend.cand.longest()
                ipad.backend.cand.reset_page()
                ipad.backend.cand.update()
            else:
                #text = ipad.text_buffer.backspace( ipad.text_buffer.get_end_iter(), False, False )
                iter_here = ipad.text_buffer.get_iter_at_mark(ipad.text_buffer.get_insert())
                text = ipad.text_buffer.backspace( iter_here, True, True )
                #if len(text) > 0:
                    #text = text.decode('utf8')
                    #text = text[:-1]
                    #ipad.text_view.get_buffer().set_text(text)
        elif ipad.mode == ipad.MODE_SELECT:
            #print "shorter"
            ipad.backend.cand.shorter()
            ipad.backend.cand.reset_page()
            #print ipad.backend.cand.query_index
            if ipad.backend.cand.query_index < 1:
                if ipad.backend.cand.cancel_select():
                    ipad.backend.cache.reset()
                    ipad.backend.search()
                else:
                    widget.set_disable()
                    ipad.mode = ipad.MODE_INPUT
                ipad.backend.cand.longest()
            ipad.backend.cand.update()
        elif ipad.mode == ipad.MODE_PUNC:
            ipad.reset()
        ipad.update()

def cb_npad_longpress( widget, ipad ):
    if ipad.mode == ipad.MODE_SELECT:
        if widget.index >= 0 and widget.index <= 6:
            ipad.backend.cand.delete(widget.index)
            ipad.update()
    #print "longpressed"

def cb_npad_click( widget, ipad ):
    index = widget.index
    if widget.longpressed_flag != True :
        if ipad.mode == ipad.MODE_INPUT:
            if index == 0:
                if len(ipad.backend.code) == 0:
                    ipad.mode = ipad.MODE_PUNC
                    ipad.update()
                else:
                    ipad.mode = ipad.MODE_SELECT
                    ipad.update()
            else:
                ipad.backend.append_code( str(index+1) )
                ipad.update()
        elif ipad.mode == ipad.MODE_SELECT:
            if index in range(6):
                ipad.select( index )
            elif index == 8:
                ipad.backend.cand.next_page()
                ipad.backend.cand.update()
                ipad.update()
            elif index == 6:
                ipad.backend.cand.prev_page()
                ipad.backend.cand.update()
                ipad.update()
            elif index == 7:
                ipad.commit()
            else:
                pass
        elif ipad.mode == ipad.MODE_PUNC:
            if index in range(6):
                ipad.commit_punc( index )
            elif index == 8:
                ipad.next_punc()
                ipad.update()
            elif index == 6:
                ipad.prev_punc()
                ipad.update()
            elif index == 7:
                pass
            else:
                pass
        else:
            pass

class NumPad( gtk.Frame ):
    button_label = [ \
            ["1","2","3","4","5","6","7","8","9","0"]\
            ,\
            ["1","2","3","4","5","6","7","8","9","0"]\
            ]
    button_width = 145
    button_height = 110
    button_width_0 = button_width * 2
    button_height_0 = 90
    def __init__( self, ipad ):
        gtk.Frame.__init__(self)
        self.ipad = ipad
        self.button = []
        self.layout = gtk.Fixed()
        self.add(self.layout)
        for i in range(3):
            for j in range(3):
                b = LabelButton(self.button_label[0][i*3+j])
                b.index = i*3+j
                b.set_size_request( self.button_width, self.button_height )
                b.connect( "clicked", cb_npad_click, ipad  )
                b.connect( "longpressed", cb_npad_longpress, ipad )
                self.layout.put( b, self.button_width * j, self.button_height * i )
                b.show()
                self.button.append(b)
        b = LabelButton(self.button_label[0][9])
        b.index = 9
        b.set_size_request( self.button_width_0, self.button_height_0 )
        b.connect( "clicked", cb_button_0, ipad )
        b.show()
        self.layout.put( b, 0, self.button_height * 3 )
        self.button.append(b)

        self.layout.show()
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
            ["；","：","！","（","）","～"]\
            ,\
            ["、","；","！","《","》","～"]\
            ]
    punc_page_count = 3
    MODE_INPUT = 0
    MODE_SELECT = 1
    MODE_PUNC = 2
    height_hint = 5
    width_hint = 35
    label_width = 800 - NumPad.button_width * 3 - width_hint
    label_height = 40
    def __init__( self, text_view ):
        gtk.Frame.__init__(self)
        self.backend = Backend(self)
        self.layout = gtk.Fixed()
        self.npad = NumPad( self )
        self.add(self.layout)
        #self.layout.put(self.npad,0,90)
        self.layout.put( self.npad, self.label_width, self.height_hint )
        self.npad.show()
        self.layout.show()

        self.l_hanzi = gtk.Label()
        self.l_pinyin = gtk.Label()
        self.l_hanzi.set_size_request( self.label_width, self.label_height )
        self.l_pinyin.set_size_request( self.label_width, self.label_height )
        self.layout.put( self.l_pinyin, 0, self.height_hint )
        self.layout.put( self.l_hanzi, 0, self.label_height + self.height_hint )
        self.l_hanzi.set_selectable(True)
        self.l_pinyin.set_selectable(True)
        self.l_pinyin.show()
        self.l_hanzi.show()

        self.mode = self.MODE_INPUT
        self.punc_index = 0

        self.text_view = text_view
        self.text_buffer = self.text_view.get_buffer()
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
            if cand.list[0]:
                self.l_hanzi.select_region(len(selected_text),len(selected_text)+len(cand_hz)-1)
            else:
                self.l_hanzi.select_region(len(selected_text),len(hz))
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
        #self.text_buffer.set_text( self.text_buffer.get_text( self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter() ) + text )
        self.text_buffer.insert_at_cursor( text )
        self.reset()
    def commit_punc( self, i ):
        #self.text_buffer.set_text( self.text_buffer.get_text( self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter() ) + self.punc_list[self.punc_index][i] )
        self.text_buffer.insert_at_cursor( self.punc_list[self.punc_index][i] )
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

class InputPad( gtk.Frame ):
    def __init__(self):
        gtk.Frame.__init__(self)
        self.layout = gtk.Fixed()
        self.text_view = gtk.TextView()
        self.text_view.set_editable( False )
        self.ipad = ChineseInputPad(self.text_view)
        self.layout.put(self.ipad,0,0)
        self.add(self.layout)

        self.text_view.set_size_request( ChineseInputPad.label_width - 5, 390 - ChineseInputPad.label_height * 2 + ChineseInputPad.height_hint )
        self.text_view.set_wrap_mode(gtk.WRAP_CHAR)
        #self.text_view.set_line_wrap(True)
        #self.text_view.set_width_chars(30)
        self.text_buffer = self.text_view.get_buffer()
        self.text_buffer.set_text("")
        self.text_view.show()
        self.layout.put( self.text_view, 0, ChineseInputPad.label_height * 2 + ChineseInputPad.height_hint )

        l_empty = gtk.Label()
        self.layout.put( l_empty, 0, 0 )
        l_empty.show()
        l_empty.set_selectable(True)

        #self.cp_b = gtk.Button("复制到剪切板")
        #self.cp_b.set_size_request( 200, 90 )
        #self.layout.put( self.cp_b, 70, 300 )
        #self.cp_b.show()
        #self.cp_b.hide()
        #self.cp_b.connect( "clicked", cb_copy, self )

        self.ipad.show()
        self.layout.show()

        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

#def cb_copy( widget, ipad ):
    #ipad.clipboard.set_text( ipad.text_view.get_buffer().get_text() )

class App( dbus.service.Object ):
    def __init__(self):
        self.dbus_loop = DBusGMainLoop()
        self.bus = dbus.SessionBus( mainloop = self.dbus_loop )
        self.bus_name = dbus.service.BusName( 'me.maemo_chinese_input_pad', self.bus )
        dbus.service.Object.__init__( self, self.bus_name, '/' )

        self.pad = gtk.Dialog()
        self.ipad = InputPad()
        self.pad.vbox.pack_start(self.ipad)
        self.pad.set_decorated(False)
        self.ipad.show()
        self.pad.hide()
        self.pad.connect( "destroy", self.cb_quit )
        self.pad.connect( "delete-event", self.cb_delete )
    def run(self):
        gtk.gdk.threads_init()
        gtk.main()
    def cb_delete( self, widget, event ):
        bus = dbus.SessionBus()
        service = bus.get_object('me.him_plugin.dbus_conn', '/')
        method = service.get_dbus_method( 'request_commit', 'me.him_plugin.dbus_conn' )
        method( self.ipad.text_buffer.get_text( self.ipad.text_buffer.get_start_iter(), self.ipad.text_buffer.get_end_iter() ) )
        self.ipad.ipad.backend.reset()
        self.ipad.ipad.reset()
        self.ipad.text_view.get_buffer().set_text("")
        self.pad.hide()
        return True
    def cb_quit( self, widget ):
        #fifo = open( "/tmp/maemo-chinese-input-pad.fifo", "w" )
        #fifo.write( self.ipad.text_view.get_buffer().get_text() )
        #fifo.close()
        gtk.main_quit()
    @dbus.service.method( 'me.maemo_chinese_input_pad' )
    def hide( self ):
        self.pad.hide()
    @dbus.service.method( 'me.maemo_chinese_input_pad' )
    def show( self ):
        self.pad.show()
        #self.set_opacity(0.5)
    @dbus.service.method( 'me.maemo_chinese_input_pad' )
    def quit( self ):
        gtk.main_quit()

if __name__ == "__main__":
    app = App()
    app.run()


