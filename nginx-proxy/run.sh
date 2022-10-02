#!/bin/bash

mkdir /etc/nginx/htpasswd/
echo -n $HTTP_AUTH_LOGIN:$(openssl passwd -apr1 $HTTP_AUTH_PASSWORD) > /etc/nginx/htpasswd/$PROMETHEUS_HOST
nginx -g "daemon off;"
