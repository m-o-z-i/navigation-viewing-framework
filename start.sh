#!/bin/bash

# Usage: start.sh WORKSPACE_CONFIG_FILE [OPTION]
# OPTION = server: just starts server
# OPTION = daemon: just starts daemon

# kill running python on this machine
if [ "$2" != false ] ; then
    killall python3
    killall python
fi

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

# assuming a local guacmole version is located properly
LOCAL_GUACAMOLE="$DIR/../../../guacamole"
LOCAL_AVANGO="$DIR/../../../avango"

GUACAMOLE=/opt/guacamole/feature_test
AVANGO=/opt/avango/feature_python3

# third party libs
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/latest/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib

# schism
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/schism/current/lib/linux_x86

# avango
export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH
export PYTHONPATH="$LOCAL_AVANGO/lib/python3.4":"$LOCAL_AVANGO/examples":$AVANGO/lib/python3.4:$AVANGO/examples:"./configs":$PYTHONPATH

# guacamole
export LD_LIBRARY_PATH="$LOCAL_GUACAMOLE/lib":$GUACAMOLE/lib:$LD_LIBRARY_PATH:./lib-server

# run daemon

if [ "$2" != "daemon" ] ; then
		python3 ./lib-server/Daemon.py > /dev/null &
else
		python3 ./lib-server/Daemon.py
		exit
fi

# run program
if [ "$2" != "server" ] ; then
    cd "$DIR" && python3 ./lib-server/main.py $1 True
else 
	  cd "$DIR" && python3 ./lib-server/main.py $1 False
fi

# kill daemon
kill %1