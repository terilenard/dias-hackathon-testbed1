#!/bin/bash
COUNTER="00000000"
SERVICES="dbcfeeder.service
          kuksa.val.service
          cloudfeeder.service
          mosquitto.service
          telemetry-deliverer.service
          pycan.service
	  diasfw.service
          dias-logging.service
          mosquitto.service
          log-deliverer.service"

status ()
{
    for service in $SERVICES; do
	systemctl status $service > /dev/null 2>&1
	echo "Service: $service with status: $?"
    done
}

start ()
{
    for service in $SERVICES; do
	systemctl start $service > /dev/null 2>&1
	echo "Service: $service started with code: $?"
    done
}

stop ()
{
    for service in $SERVICES; do
	systemctl stop $service > /dev/null 2>&1
	echo "Service: $service stopped with code: $?"
    done
    echo "Restoring /etc/dbcfeeder/counter.txt with counter $COUNTER"
    echo $COUNTER > /etc/dbcfeeder/counter.txt 

}

restart ()
{
    sudo systemctl stop dbcfeeder diasfw
    echo "Restoring /etc/dbcfeeder/counter.txt with counter $COUNTER"
    echo $COUNTER > /etc/dbcfeeder/counter.txt 

    for service in $SERVICES; do
	systemctl restart $service > /dev/null 2>&1
	echo "Service: $service restarted with code: $?"
    done
}

if [ $# -ne 1 ];
then
    echo "Please enter one of the following arguments: status stop start restart"
    exit
fi

case $1 in

  "status")
    status
    ;;

  "stop")
    stop
    ;;

  "start")
    start
    ;;

 "restart")
    restart
    ;;

esac
