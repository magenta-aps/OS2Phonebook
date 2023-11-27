#! /usr/bin/env sh
set -e

# Modify gunicorn config for auto-reload
CONF_FILE=/gunicorn_conf.py

LINE="reload = True"
grep -qxF "${LINE}" "${CONF_FILE}" || echo "${LINE}" >> "${CONF_FILE}"

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    # shellcheck source=/dev/null
    . "$PRE_START_PATH"
else 
    echo "There is no script $PRE_START_PATH"
fi

# Start Gunicorn without meinheld
# We explicitly overwrite the timeout to allow the DIPEX export job time to
# upload the whole json file.
exec gunicorn --timeout=60 -c "$GUNICORN_CONF" "$APP_MODULE"
