#!/bin/bash


# stop server app
./stop.sh # kill running python apps


# stop client apps on remote hosts
DIR="$( cd "$( dirname "$0" )" && pwd )" # get directory of script

HOSTS=$(grep '<hostname' "$1" | cut -f2 -d">"|cut -f1 -d"<")

for host in $HOSTS; do
  ssh $host "$DIR"/stop.sh& # kill running python apps
  sleep 0.2
done


