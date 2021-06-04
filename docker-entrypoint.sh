#! /bin/bash


if [ ! -z $1 ] ; then
    COMMAND=$@
fi

CMD=`echo $COMMAND | awk '{print $1}'`

case "$CMD" in
    loaddata|migrate|runserver)
        exec python3 manage.py $COMMAND
    ;;
esac

if [ -z "$COMMAND" ] ; then
    exec gunicorn -b 0.0.0.0:8000 -w 5 -t 40 -p /var/run/djpodcaster.pid djpodcaster.wsgi:application
elif [ "$COMMAND" = "worker" ] ; then
    exec python3 -m celery -A fmitesla -l info worker --queues=default,celery
fi
