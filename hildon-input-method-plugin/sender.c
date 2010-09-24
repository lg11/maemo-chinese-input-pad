#include <dbus/dbus-glib.h>
#include <glib.h>
#include <stdlib.h>
#include "sender.h"

dbus_sender* dbus_sender_new(){
    dbus_sender* sender = malloc( sizeof(dbus_sender) );
    GError* error;

    error = NULL;
    /*g_debug( "start init" );*/
    sender->conn = dbus_g_bus_get( DBUS_BUS_SESSION, &error );
    if ( !sender->conn ){
        g_debug( "failed to connect to the d-bus daemon: %s", error->message );
        g_error_free(error);
        return NULL;
    }

    /*g_debug( "start proxy" );*/
    sender->proxy = dbus_g_proxy_new_for_name( sender->conn, "me.maemo_chinese_input_pad", "/", "me.maemo_chinese_input_pad" );
    /*g_debug( "start proxy end" );*/

    return sender;
}

int dbus_sender_call( dbus_sender* sender ){
    GError* error;
    /*g_debug( "try send" );*/
    if ( !dbus_g_proxy_call( sender->proxy, "show", &error, G_TYPE_INVALID, G_TYPE_INVALID ) ) {
        g_debug( "failed to call: %s", error->message );
        g_error_free(error);
        return 1;
    }
    return 0;
}
