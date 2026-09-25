#!/bin/sh
set -e

# Apply database migrations before starting the server. Compose waits for the
# database healthcheck, so no retry loop is needed here.
if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    flask deploy
fi

exec "$@"
