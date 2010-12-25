#!/bin/bash
su user -c "sh /opt/mcip/plugin/recover.sh"
rm /usr/lib/hildon-input-method/inputpad_plugin.so
rm /usr/share/dbus-1/services/me.maemo.chinese.inputpad.service
rm -rf /opt/mcip

