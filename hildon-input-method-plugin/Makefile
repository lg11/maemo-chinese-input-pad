#gcc main.c -o main `pkg-config --libs --cflags glib-2.0` `pkg-config --libs --cflags gtk+-2.0` `pkg-config --libs --cflags gconf-2.0`

ALL : maemo-chinese-input-pad-plugin.so

utils.o : utils.c utils.h
	gcc -c utils.c -o utils.o
	#gcc -c utils.c -o utils.o `pkg-config --libs --cflags glib-2.0` 

sender.o : sender.c sender.h
	gcc -c sender.c -o sender.o `pkg-config --libs --cflags glib-2.0` `pkg-config --libs --cflags gtk+-2.0` `pkg-config --libs --cflags dbus-glib-1`

plugin.o : plugin.c
	gcc -c plugin.c -o plugin.o `pkg-config --libs --cflags glib-2.0` `pkg-config --libs --cflags gtk+-2.0` `pkg-config --libs --cflags gconf-2.0`

maemo-chinese-input-pad-plugin.so : utils.o plugin.o sender.o
	gcc utils.o plugin.o sender.o -shared -o maemo-chinese-input-pad-plugin.so `pkg-config --libs --cflags glib-2.0` `pkg-config --libs --cflags gtk+-2.0` `pkg-config --libs --cflags gconf-2.0`


