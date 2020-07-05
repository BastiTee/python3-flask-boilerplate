#!/bin/sh
# Initialize database if not present
if [ ! -f /instance/database.sqlite ]
then
    FLASK_APP=my_module FLASK_DEBUG=1 python3 -m flask init-db
fi
# Start uwsgi daemon
uwsgi uwsgi.ini &
# Start nginx
nginx
