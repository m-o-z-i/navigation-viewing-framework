#!/bin/bash

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

# assuming a local guacmole version is located properly
LOCAL_GUACAMOLE="$DIR/../../../guacamole"
LOCAL_AVANGO="$DIR/../../../avango"

GUACAMOLE=/opt/guacamole/master
AVANGO=/opt/avango/feature_python3

# third party libs
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/latest/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib

# schism
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/schism/current/lib/linux_x86

# avango
export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH
export PYTHONPATH="$LOCAL_AVANGO/lib/python3.4":"$LOCAL_AVANGO/examples":$AVANGO/lib/python3.4:$AVANGO/examples:"./configs":"./lib-server":$PYTHONPATH

# guacamole
export LD_LIBRARY_PATH="$LOCAL_GUACAMOLE/lib":$GUACAMOLE/lib:$LD_LIBRARY_PATH:./lib-server

# run program
cd "$DIR" && python3 ./lib-client/main.py $1 $2 $3 $4 $5 $6

# kill daemon
kill %1
