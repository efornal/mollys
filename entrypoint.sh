#!/usr/bin/env bash
set -e

if [ -n "$DB_NAME" ] && [ ${#DB_NAME} -g 1 ]; then 
    python manage.py compilemessages
    python manage.py collectstatic --noinput
    python manage.py migrate --database db_owner
fi
    
exec "$@"



