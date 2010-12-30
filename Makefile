DIRS = plugin python dict

ALL :
	set -e ; for d in $(DIRS) ; do $(MAKE) -C $$d ; done

clean :
	set -e ; for d in $(DIRS) ; do $(MAKE) -C $$d clean ; done

install :
	mkdir -p /opt/mcip
	mkdir -p /opt/mcip/python
	mkdir -p /opt/mcip/plugin
	mkdir -p /opt/mcip/dict
	cp plugin/inputpad_plugin.so /opt/mcip/plugin
	cp plugin/gconf.sh /opt/mcip/plugin 
	cp plugin/recover.sh /opt/mcip/plugin 
	cp plugin/me.maemo.chinese.inputpad.service /opt/mcip/plugin
	ln -s /opt/mcip/plugin/inputpad_plugin.so /usr/lib/hildon-input-method/
	ln -s /opt/mcip/plugin/me.maemo.chinese.inputpad.service /usr/share/dbus-1/services/
	cp dict/dict.0 /opt/mcip/dict
	cp python/*.py /opt/mcip/python
	cp python/*.pyo /opt/mcip/python
	cp python/run.sh /opt/mcip/python
	hildon-im-recache
	su user -c "sh /opt/mcip/plugin/gconf.sh"

uninstall :
	su user -c "sh /opt/mcip/plugin/recover.sh"
	rm /usr/lib/hildon-input-method/inputpad_plugin.so
	rm /usr/share/dbus-1/services/me.maemo.chinese.inputpad.service
	rm -rf /opt/mcip
