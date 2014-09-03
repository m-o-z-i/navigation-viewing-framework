#!/bin/bash

# kill running python on this machine
if [ "$2" != false ] ; then
    killall python
fi

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

# assuming a local guacmole version is located properly
LOCAL_GUACAMOLE="$DIR/../../../guacamole"
LOCAL_AVANGO="$DIR/../../../avango"

GUACAMOLE=/opt/guacamole/master
AVANGO=/opt/avango/master

# third party libs
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/latest/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/current/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib

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
if [ "$2" != false ] ; then
    cd "$DIR" && python ./lib-server/main.py $1 True
else
	  cd "$DIR" && python ./lib-server/main.py $1 False
fi

# kill daemon
kill %1
