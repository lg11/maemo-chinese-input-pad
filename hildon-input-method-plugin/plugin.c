#include "utils.h"
#include "sender.h"
/*#include "dbus_xml.h"*/
#include <hildon-input-method/hildon-im-plugin.h>
#include <fcntl.h>

static GType Plugin_type;
static GtkWidgetClass* parent_class;

typedef struct{
    GtkWindow parent;
}Plugin;
typedef struct{
    GtkWindowClass parent;
    /*DBusGConnection* conn;*/
}Plugin_class;

typedef struct{
    HildonIMUI* ui;
    /*GtkStyle* style;*/
    /*PangoLayout *layout;*/
    dbus_sender* sender;
    gboolean io_flag;
}Plugin_private;

/*typedef struct{*/
    /*GtkWindow parent;*/
/*}plugin;*/

/*#define PLUGIN_TYPE (get_Plugin_type())*/
#define PLUGIN_TYPE Plugin_type
#define PLUGIN( obj ) GTK_CHECK_CAST( obj, PLUGIN_TYPE, Plugin )
#define PLUGIN_CLASS( klass ) GTK_CHECK_CLASS_CAST( klass, Plugin_type, Plugin_class )
#define PLUGIN_PRIVATE( obj ) G_TYPE_INSTANCE_GET_PRIVATE( obj, Plugin_type, Plugin_private );

/*GType get_Plugin_type(void){ return Plugin_type; }*/

/*static int count_integer;*/

/*gboolean hildon_input_method_plugin_commit( Plugin* p, GString gstr, GError** error ){*/
gboolean io_func( GIOChannel* source, GIOCondition type, gpointer data ){
    Plugin* p = PLUGIN(p);
    Plugin_private* priv;
    GString* gstr = g_string_new(NULL);
    priv = PLUGIN_PRIVATE( p );
    GError* error = NULL;
    g_io_channel_read_line_string( source, gstr, NULL,  &error );
    g_debug( "get text %s", gstr->str );
    hildon_im_ui_send_utf8( priv->ui, gstr->str );

    /*g_string_free( gstr, TRUE );*/
    return TRUE;
}

static void enable( HildonIMPlugin* plugin, gboolean init ){
    g_debug( "enable" );
    Plugin_private* priv;
    priv = PLUGIN_PRIVATE( plugin );
    priv->sender = dbus_sender_new();
    dbus_sender_call( priv->sender );

    /*GError* error;*/
    /*priv->conn = dbus_g_bus_get (DBUS_BUS_SESSION, &error);*/
    /*if (priv->conn == NULL) {*/
        /*g_warning("Unable to connect to dbus: %s", error->message);*/
        /*g_error_free (error);*/
    /*}*/
    /*if ( priv->io_flag == FALSE ) {*/
        /*gint fd;*/
        /*fd = open("/tmp/him_plugin.fifo", O_RDONLY );*/
        /*GIOChannel *io_channel;*/
        /*io_channel = g_io_channel_unix_new( fd );*/
        /*g_io_add_watch( io_channel, G_IO_IN, io_func, plugin );*/
        /*hildon_im_ui_send_communication_message( priv->ui, HILDON_IM_CONTEXT_REQUEST_SURROUNDING );*/
        /*priv->io_flag=TRUE;*/
    /*}*/
}
static void disable( HildonIMPlugin* plugin ){
    g_debug( "disable" );
}
static void settings_changed( HildonIMPlugin* plugin, const gchar* key, const GConfValue* value ){
    g_debug( "setting_changed" );
}
static void language_settings_changed( HildonIMPlugin* plugin, const gint index ){
    g_debug( "language_settings_changed" );
}
static void input_mode_changed( HildonIMPlugin* plugin ){
    g_debug( "input_mode_changed" );
}
static void keyboard_state_changed( HildonIMPlugin* plugin ){
    g_debug( "keyboard_state_changed" );
}
static void client_widget_changed( HildonIMPlugin* plugin ){
    g_debug( "client_widget_changed" );
}
static void character_autocase( HildonIMPlugin* plugin ){
    g_debug( "character_autocase" );
}
static void clear( HildonIMPlugin* plugin ){
    g_debug( "clear" );
}
static void save_data( HildonIMPlugin* plugin ){
    g_debug( "save_data" );
}
static void mode_a( HildonIMPlugin* plugin ){
    g_debug( "mode_a" );
}
static void mode_b( HildonIMPlugin* plugin ){
    g_debug( "mode_b" );
}
static void language( HildonIMPlugin* plugin ){
    g_debug( "language" );
}
static void backspace( HildonIMPlugin* plugin ){
    g_debug( "backspace" );
}
static void enter( HildonIMPlugin* plugin ){
    g_debug( "enter" );
}
static void tab( HildonIMPlugin* plugin ){
    g_debug( "tab" );
}
static void fullscreen( HildonIMPlugin* plugin, gboolean fullscreen ){
    g_debug( "fullscreen" );
}
static void select_region( HildonIMPlugin *plugin, gint start, gint end ){
    g_debug( "select_region" );
}

static void key_event( HildonIMPlugin *plugin, GdkEventType type, guint state, guint keyval, guint hardware_keycode ){
    if ( type == GDK_KEY_PRESS )
        g_debug( "key_event, type = press, state = %d, keyval = %d, hardware_keycode = %d", state, keyval, hardware_keycode );
    else if ( type == GDK_KEY_RELEASE )
        g_debug( "key_event, type = release, state = %d, keyval = %d, hardware_keycode = %d", state, keyval, hardware_keycode );
    else
        g_debug( "key_event, type = unknown, state = %d, keyval = %d, hardware_keycode = %d", state, keyval, hardware_keycode );

    /*Plugin_private* priv;*/
    /*priv = PLUGIN_PRIVATE( plugin );*/
    /*hildon_im_ui_send_utf8( priv->ui, "test commit" );*/
    /*hildon_im_ui_send_communication_message( priv->ui, HILDON_IM_CONTEXT_REQUEST_SURROUNDING );*/
    /*g_debug( "surrounding = %s", hildon_im_ui_get_surrounding( priv->ui )  );*/
}

static void transition( HildonIMPlugin *plugin, gboolean from ){
    g_debug( "transition" );
}
static void surrounding_received( HildonIMPlugin *plugin, const gchar *surrounding, gint offset ){
    g_debug( "surrounding_received" );

    Plugin_private* priv;
    priv = PLUGIN_PRIVATE( plugin );
    /*hildon_im_ui_send_communication_message( priv->ui, HILDON_IM_CONTEXT_REQUEST_SURROUNDING );*/
    g_debug( "surrounding = %s", surrounding  );
}
static void button_activated( HildonIMPlugin *plugin, HildonIMButton button, gboolean long_press ){
    g_debug( "button_activated" );
}
static void preedit_committed( HildonIMPlugin *plugin, const gchar *committed_preedit ){
    g_debug( "preedit_committed" );
}

//ui interface function
static void get_property( GObject* object, guint prop_id, GValue* value, GParamSpec* pspec ){
    Plugin_private* priv;
    g_debug( "get_property" );

    g_return_if_fail( GTK_CHECK_TYPE( object, Plugin_type ) );
    priv = G_TYPE_INSTANCE_GET_PRIVATE( object, Plugin_type, Plugin_private );

    switch ( prop_id ){
        case HILDON_IM_PROP_UI:
            g_value_set_object( value, priv->ui );
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID( object, prop_id, pspec );
            break;
    }
}

static void set_property( GObject* object, guint prop_id, const GValue* value, GParamSpec* pspec ){
    Plugin_private* priv;
    g_debug( "set_property" );

    g_return_if_fail( GTK_CHECK_TYPE( object, Plugin_type ) );
    priv = G_TYPE_INSTANCE_GET_PRIVATE( object, Plugin_type, Plugin_private );

    switch ( prop_id ){
        case HILDON_IM_PROP_UI:
            /*Plugin_log( "set_property_set_ui" );*/
            priv->ui = g_value_get_object( value );
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID( object, prop_id, pspec );
            break;
    }
    /*priv->io_flag = FALSE;*/

}
static void finalize( GObject *object ){
    g_debug( "finalize" );
    if ( G_OBJECT_CLASS( parent_class )->finalize )
        G_OBJECT_CLASS( parent_class )->finalize( object );
}
static void realize ( GtkWidget *widget )
{
    Plugin* p;
    Plugin_private* priv;

    g_debug( "realize" );

    g_return_if_fail( GTK_CHECK_TYPE( widget, Plugin_type ) );
    p = PLUGIN( widget );
    priv = G_TYPE_INSTANCE_GET_PRIVATE( p, Plugin_type, Plugin_private );

    GTK_WIDGET_SET_FLAGS( widget, GTK_REALIZED );
}

static gboolean destroy( GtkWidget* widget, GdkEventAny* event ){
    g_debug( "destroy_cb" );
    //release priv resource in this place
    return FALSE;
}
static gboolean expose( GtkWidget* widget, GdkEventExpose* event ){
    //create priv resource in this place
    g_debug( "expose" );
    
    /*Plugin* p;*/
    /*Plugin_private* priv;*/

    /*g_return_if_fail( GTK_CHECK_TYPE( widget, Plugin_type ) );*/
    /*p = GTK_CHECK_CAST( widget, Plugin_type, plugin );*/
    /*priv = G_TYPE_INSTANCE_GET_PRIVATE( p, Plugin_type, Plugin_private );*/
    
    
    return TRUE;
}

static void Plugin_class_init( Plugin_class* klass ){
    g_debug( "Plugin_class_init" );
    GObjectClass*  object_class;
    /*GtkObjectClass* gtk_object_class;*/
    GtkWidgetClass* widget_class;

    parent_class = g_type_class_peek_parent( klass );
    g_type_class_add_private( klass, sizeof( Plugin_private ) );

    object_class = G_OBJECT_CLASS( klass );
    /*gtk_object_class = GTK_OBJECT_CLASS( class );*/
    widget_class = GTK_WIDGET_CLASS( klass );

    object_class->set_property = set_property;
    object_class->get_property = get_property;
    object_class->finalize = finalize;

    widget_class->realize = realize;
    widget_class->destroy_event = destroy;
    widget_class->expose_event = expose;

    g_object_class_install_property(object_class, HILDON_IM_PROP_UI,
            g_param_spec_object(HILDON_IM_PROP_UI_DESCRIPTION, 
                HILDON_IM_PROP_UI_DESCRIPTION,
                "maemo-chinese-input-pad-plugin",
                HILDON_IM_TYPE_UI,
                G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY
                )
            );

    /*GError* error = NULL;*/
    /*klass->conn = dbus_g_bus_get (DBUS_BUS_SESSION, &error);*/
    /*if (klass->conn == NULL) {*/
        /*g_warning("Unable to connect to dbus: %s", error->message);*/
        /*g_error_free (error);*/
    /*}*/

    /*g_debug( "Plugin_init 4" );*/
    /*dbus_g_object_type_install_info ( Plugin_type, &dbus_glib_plugin_object_info );*/

}

static void Plugin_init( Plugin* p ){
    g_debug( "Plugin_init" );

    /*GError* error = NULL;*/
    /*DBusGProxy *driver_proxy;*/
    /*DBusGConnection* conn;*/
    /*int request_ret;*/

    /*conn = dbus_g_bus_get (DBUS_BUS_SESSION, &error);*/
    /*if (conn == NULL) {*/
        /*g_warning("Unable to connect to dbus: %s", error->message);*/
        /*g_error_free (error);*/
    /*}*/


    /*Register DBUS path*/
    /*dbus_g_connection_register_g_object (conn, "/me/hildon_input_method_plugin", G_OBJECT (p));*/

    /* Register the service name, the constant here are defined in dbus-glib-bindings.h */
    /*driver_proxy = dbus_g_proxy_new_for_name (klass->connection, DBUS_SERVICE_DBUS, DBUS_PATH_DBUS, DBUS_INTERFACE_DBUS);*/
    /*driver_proxy = dbus_g_proxy_new_for_name( conn, "me.hildon_input_method_plugin", "/", "me.hildon_input_method_plugin" );*/
    /*if (!dbus_g_proxy_call( driver_proxy, "RequestName", &error, G_TYPE_STRING, "me.hildon_input_method_plugin", G_TYPE_UINT, 0, G_TYPE_INVALID, G_TYPE_UINT, &request_ret, G_TYPE_INVALID)) {*/
        /*g_warning("Unable to register service: %s", error->message);*/
        /*g_error_free (error);*/
    /*}*/
    /*g_object_unref (driver_proxy);*/
}

GtkWidget* Plugin_widget_new( HildonIMUI* widget ){
    g_debug( "Plugin_widget_new" );
    return g_object_new( Plugin_type, HILDON_IM_PROP_UI_DESCRIPTION, widget, NULL );
}
static void Plugin_interface_init( HildonIMPluginIface* iface ){
    g_debug( "interface_init" );
    iface->enable = enable;
    iface->disable = disable;
    iface->settings_changed = settings_changed;
    iface->language_settings_changed = language_settings_changed;
    iface->input_mode_changed = input_mode_changed;
    iface->keyboard_state_changed = keyboard_state_changed;
    iface->client_widget_changed = client_widget_changed;
    iface->character_autocase = character_autocase;
    iface->clear = clear;
    iface->save_data = save_data;
    iface->mode_a = mode_a;
    iface->mode_b = mode_b;
    iface->language = language;
    iface->backspace = backspace;
    iface->enter = enter;
    iface->tab = tab;
    iface->fullscreen = fullscreen;
    iface->select_region = select_region;
    iface->key_event = key_event;
    iface->transition = transition;
    iface->surrounding_received = surrounding_received;
    iface->button_activated = button_activated;
    iface->preedit_committed = preedit_committed;
}
void module_init( GTypeModule* module ){
    g_debug( "module_init" );
    static const GTypeInfo type_info = {
        sizeof( Plugin_class ),
        NULL, /* base_init */
        NULL, /* base_finalize */
        (GClassInitFunc) Plugin_class_init,
        NULL, /* class_finalize */
        NULL, /* class_data */
        sizeof( Plugin ),
        0, /* n_preallocs */
        (GInstanceInitFunc) Plugin_init,
    };
    static const GInterfaceInfo Plugin_info = {
        (GInterfaceInitFunc) Plugin_interface_init,
        NULL, /* interface_finalize */
        NULL, /* interface_data */
    };
    Plugin_type = g_type_module_register_type( module, GTK_TYPE_WIDGET, "Plugin", &type_info, 0 );
    g_type_module_add_interface( module, Plugin_type, HILDON_IM_TYPE_PLUGIN, &Plugin_info );
}

void module_exit( void ){
    g_debug( "module_exit" );
}

HildonIMPlugin* module_create( HildonIMUI* widget ){
    g_debug( "module_create" );
    /*count_integer = 0;*/
    return HILDON_IM_PLUGIN( Plugin_widget_new( widget ) );
}

const HildonIMPluginInfo* hildon_im_Plugin_get_info( void ){
    static const HildonIMPluginInfo info = 
    {
        "MAEMO-CHINESE-INPUT-PAD-PLUGIN",
        "maemo-chinese-input-pad-plugin",
        NULL,
        NULL,
        FALSE,
        FALSE,
        HILDON_IM_TYPE_OTHERS,
        HILDON_IM_GROUP_CJK,
        HILDON_IM_DEFAULT_PLUGIN_PRIORITY,
        NULL,
        NULL,
        FALSE,
        HILDON_IM_DEFAULT_HEIGHT,
        HILDON_IM_TRIGGER_NONE
    };
    g_debug( "hildon_im_Plugin_get_info" );
    return &info;
}

gchar** hildon_im_Plugin_get_available_languages( gboolean* free ){
    static gchar* list[] = { "zh_CN", "en_GB", "en_US", NULL };
    g_debug( "hildon_im_Plugin_get_available_languages" );
    *free = FALSE;
    return list;
}


