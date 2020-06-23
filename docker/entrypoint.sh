#!/bin/bash

set -e

python /app/cli.py pingdb

chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /app
chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /log
chown -R sys_magenta_os2phonebook:sys_magenta_os2phonebook /entrypoint

sudo -u sys_magenta_os2phonebook -E "$@"
