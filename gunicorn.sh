#! /bin/bash

gunicorn -D -b unix:./gun_djpodcaster.sock -w 2 -p ./gun_djpodcaster.pid djpodcaster.wsgi
