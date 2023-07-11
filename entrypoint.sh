#!/usr/bin/env bash
set -e

if [ -z "$SKIP_APP_INIT" ]; then
    python manage.py compilemessages
    python manage.py collectstatic --noinput
    python manage.py migrate --database db_owner
fi
    
exec "$@"



