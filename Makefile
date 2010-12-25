DIRS = plugin python dict


ALL :
	set -e ; for d in $(DIRS) ; do $(MAKE) -C $$d ; done

install :
	sh install.sh

uninstall :
	sh uninstall.sh
