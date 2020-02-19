#!/bin/bash

set -e

python /app/cli.py pingdb

exec "$@"
