import ui
#import gtk

def check():
    import os
    if os.path.exists("/home/user/.config/maemo-chinese-input-pad/data/main.db"):
        pass
    else:
        print "copy db"
        os.system("mkdir -p /home/user/.config/maemo-chinese-input-pad/data")
        os.system("cp /usr/share/maemo-chinese-input-pad/data/main.db /home/user/.config/maemo-chinese-input-pad/data")
        print "copy end"

def main():
    #gtk.rc_parse( "/etc/hildon/theme/gtk-2.0/gtkrc" )
    check()
    app = ui.App()
    app.run()

if __name__ == "__main__":
    main()
