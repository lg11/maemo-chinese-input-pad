#include "utils.h"

/*int dbus_call_pad_show( DBusGConnection* conn ){*/
int dbus_call_pad_show( const gchar* str, const gchar* anti_eat_cache ){
    GError* error = NULL;
    static DBusGConnection* conn = NULL;
    static DBusGProxy* proxy = NULL;

    if (!conn)
        conn = dbus_g_bus_get (DBUS_BUS_SESSION, &error);

    if (!proxy )
        proxy = dbus_g_proxy_new_for_name( conn, "me.maemo_chinese_input_pad", "/", "me.maemo_chinese_input_pad" );

    if ( !dbus_g_proxy_call( proxy, "show", &error, G_TYPE_STRING, str, G_TYPE_STRING, anti_eat_cache, G_TYPE_INVALID, G_TYPE_INVALID ) ) {
        g_debug( "failed to call: %s", error->message );
        g_error_free(error);
        return 1;
    }
    return 0;
}
