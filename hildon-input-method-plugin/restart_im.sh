kill -9 `ps aux | grep hildon-input-method | grep -v grep | awk '{print $1}'`
