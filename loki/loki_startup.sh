#!/bin/sh

# Ensure that root is used to modify permissions on the /data directory
if [ "$(id -u)" = "0" ]; then
    chown -R 10001:10001 /data
    # Now drop to user 10001 after setting permissions
    exec su-exec 10001 /usr/bin/loki "$@"
else
    exec /usr/bin/loki "$@"
fi
