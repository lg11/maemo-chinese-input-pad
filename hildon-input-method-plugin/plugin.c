#include "utils.h"
#include <hildon-input-method/hildon-im-plugin.h>

static GType plugin_type;
static GtkWidgetClass* parent_class;

typedef struct{
    GtkWindowClass parent;
}plugin_class;

typedef struct{
    HildonIMUI* ui;
    GtkStyle* style;
    PangoLayout *layout;
}plugin_private;

typedef struct{
    GtkWindow parent;
}plugin;

#define PLUGIN( obj ) GTK_CHECK_CAST( object, plugin_type, plugin )
#define PLUGIN_CLASS( klass ) GTK_CHECK_CLASS_CAST( klass, plugin_type, plugin_class )
#define PLUGIN_PRIVATE( obj ) G_TYPE_INSTANCE_GET_PRIVATE( obj, plugin_type, plugin_private );

static void enable( HildonIMPlugin* plugin, gboolean init ){
    g_debug( "enable" );
    plugin_private* priv;
    priv = PLUGIN_PRIVATE( plugin );
    hildon_im_ui_send_communication_message( priv->ui, HILDON_IM_CONTEXT_REQUEST_SURROUNDING );
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

    /*plugin_private* priv;*/
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

    plugin_private* priv;
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
    plugin_private* priv;
    g_debug( "get_property" );

    g_return_if_fail( GTK_CHECK_TYPE( object, plugin_type ) );
    priv = G_TYPE_INSTANCE_GET_PRIVATE( object, plugin_type, plugin_private );

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
    plugin_private* priv;
    g_debug( "set_property" );

    g_return_if_fail( GTK_CHECK_TYPE( object, plugin_type ) );
    priv = G_TYPE_INSTANCE_GET_PRIVATE( object, plugin_type, plugin_private );

    switch ( prop_id ){
        case HILDON_IM_PROP_UI:
            /*plugin_log( "set_property_set_ui" );*/
            priv->ui = g_value_get_object( value );
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID( object, prop_id, pspec );
            break;
    }
}
static void finalize( GObject *object ){
    g_debug( "finalize" );
    if ( G_OBJECT_CLASS( parent_class )->finalize )
        G_OBJECT_CLASS( parent_class )->finalize( object );
}
static void realize ( GtkWidget *widget )
{
    plugin* p;
    plugin_private* priv;

    g_debug( "realize_cb" );

    g_return_if_fail( GTK_CHECK_TYPE( widget, plugin_type ) );
    p = GTK_CHECK_CAST( widget, plugin_type, plugin );
    priv = G_TYPE_INSTANCE_GET_PRIVATE( p, plugin_type, plugin_private );

    GTK_WIDGET_SET_FLAGS( widget, GTK_REALIZED );
}

static gboolean destroy( GtkWidget* widget, GdkEventAny* event ){
    g_debug( "destroy_cb" );
    //release priv resource in this place
    return FALSE;
}
static gboolean expose( GtkWidget* widget, GdkEventExpose* event ){
    //create priv resource in this place
    g_debug( "expose_cb" );
    return TRUE;
}

static void plugin_class_init( plugin_class* klass ){
    g_debug( "plugin_class_init" );
    GObjectClass*  object_class;
    /*GtkObjectClass* gtk_object_class;*/
    GtkWidgetClass* widget_class;

    parent_class = g_type_class_peek_parent( klass );
    g_type_class_add_private( klass, sizeof( plugin_private ) );

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
}

static void plugin_init( plugin* c ){
    g_debug( "plugin_init" );
}
GtkWidget* plugin_widget_new( HildonIMUI* widget ){
    g_debug( "plugin_widget_new" );
    return g_object_new( plugin_type, HILDON_IM_PROP_UI_DESCRIPTION, widget, NULL );
}
static void plugin_interface_init( HildonIMPluginIface* iface ){
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
        sizeof( plugin_class ),
        NULL, /* base_init */
        NULL, /* base_finalize */
        (GClassInitFunc) plugin_class_init,
        NULL, /* class_finalize */
        NULL, /* class_data */
        sizeof( plugin ),
        0, /* n_preallocs */
        (GInstanceInitFunc) plugin_init,
    };
    static const GInterfaceInfo plugin_info = {
        (GInterfaceInitFunc) plugin_interface_init,
        NULL, /* interface_finalize */
        NULL, /* interface_data */
    };
    plugin_type = g_type_module_register_type( module, GTK_TYPE_WIDGET, "plugin", &type_info, 0 );
    g_type_module_add_interface( module, plugin_type, HILDON_IM_TYPE_PLUGIN, &plugin_info );
}

void module_exit( void ){
    g_debug( "module_exit" );
}

HildonIMPlugin* module_create( HildonIMUI* widget ){
    g_debug( "module_create" );
    return HILDON_IM_PLUGIN( plugin_widget_new( widget ) );
}

const HildonIMPluginInfo* hildon_im_plugin_get_info( void ){
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
    g_debug( "hildon_im_plugin_get_info" );
    return &info;
}

gchar** hildon_im_plugin_get_available_languages( gboolean* free ){
    static gchar* list[] = { "zh_CN", "en_GB", "en_US", NULL };
    g_debug( "hildon_im_plugin_get_available_languages" );
    *free = FALSE;
    return list;
}


