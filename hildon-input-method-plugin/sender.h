#ifndef PLUGIN_DBUS_SENDER_H
#define PLUGIN_DBUS_SENDER_H

#include <dbus/dbus-glib.h>
#include <glib.h>
//#include <hildon-input-method/hildon-im-plugin.h>

typedef struct{
    DBusGConnection* conn;
    DBusGProxy* proxy;
}dbus_sender;

dbus_sender* dbus_sender_new();
int dbus_sender_call( dbus_sender* sender );

#endif
