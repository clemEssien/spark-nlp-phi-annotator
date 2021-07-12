#!/usr/bin/env bash
set -e

if [ "$1" = 'uwsgi' ] || [ "$1" = 'python' ]; then
    cd ${APP_DIR}
    # Start Apache Spark on port 8080
    bash start-master.sh
    # Start the container command
    exec gosu www-data "$@"
fi

exec "$@"
