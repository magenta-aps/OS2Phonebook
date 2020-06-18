#!/bin/bash

set -e

python /app/cli.py pingdb

chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /app
chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /data-cache
chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /log
chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /entrypoint

su - sys_magenta_os2phonebook -c exec "$@"
