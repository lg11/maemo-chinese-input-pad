#!/bin/bash
mkdir -p /opt/mcip
mkdir -p /opt/mcip/python
mkdir -p /opt/mcip/dict
mkdir -p /opt/mcip/plugin
cp plugin/inputpad_plugin.so /opt/mcip/plugin
cp plugin/gconf.sh /opt/mcip/plugin 
cp plugin/recover.sh /opt/mcip/plugin 
ln -s /opt/mcip/plugin/inputpad_plugin.so /usr/lib/hildon-input-method/
cp plugin/me.maemo.chinese.inputpad.service /usr/share/dbus-1/services/
cp dict/dict.0 /opt/mcip/dict
cp python/*.py /opt/mcip/python
cp python/*.pyo /opt/mcip/python
cp python/run.sh /opt/mcip/python
su user -c "sh /opt/mcip/plugin/gconf.sh"
