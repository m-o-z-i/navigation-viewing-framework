#!/bin/bash

# kill running python on this machine
killall python

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

# assuming a local guacmole version is located properly
LOCAL_GUACAMOLE="$DIR/../../../guacamole"
LOCAL_AVANGO="$DIR/../../../avango"

# if not, this path will be used
GUACAMOLE=/opt/guacamole/testing/guacamole
AVANGO=/opt/guacamole/testing/avango

# third party libs
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/latest/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib

# schism
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/schism/current/lib/linux_x86

# avango
export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH
export PYTHONPATH="$LOCAL_AVANGO/lib/python2.7":"$LOCAL_AVANGO/examples":$AVANGO/lib/python2.7:$AVANGO/examples:"./configs":$PYTHONPATH

# guacamole
export LD_LIBRARY_PATH="$LOCAL_GUACAMOLE/lib":$GUACAMOLE/lib:$LD_LIBRARY_PATH:./lib-server

# run daemon
python ./lib-server/Daemon.py > /dev/null &

# run program
cd "$DIR" && python ./lib-server/main.py $1

# kill daemon
kill %1
