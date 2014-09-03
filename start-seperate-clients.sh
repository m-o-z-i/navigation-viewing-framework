#!/bin/bash

# param 1: server-ip
# param 2: platform-id
# param 3: display-name
# param 4: screen-number
# param 5: number of client applications

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

GUACAMOLE=/opt/guacamole/master
AVANGO=/opt/avango/master

# third party libs
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/latest/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib

# schism
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/schism/current/lib/linux_x86

# avango
export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH
export PYTHONPATH="$LOCAL_AVANGO/lib/python2.7":"$LOCAL_AVANGO/examples":$AVANGO/lib/python2.7:$AVANGO/examples:"./configs":"./lib-server":$PYTHONPATH

# guacamole
export LD_LIBRARY_PATH="$LOCAL_GUACAMOLE/lib":$GUACAMOLE/lib:$LD_LIBRARY_PATH:./lib-server

# loop to start all the desired client applications
num=$(($5 - 1))

for i in `seq 0 $num`;
  do
    # run program
    cd "$DIR" && python ./lib-client/main.py $1 $2 $3 $4 $i
  done
