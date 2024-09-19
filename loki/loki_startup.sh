#!/bin/sh

# Ensure correct permissions on the /data directory
chown -R 10001:10001 /data

# Execute the main Loki process with the passed arguments
exec "$@"