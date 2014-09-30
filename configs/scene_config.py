#!/usr/bin/python

## @file
# Contains the scenegraph instances and scene names to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import python libraries
import subprocess

# get server ip 
server_ip = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
server_ip = server_ip.strip(" \n")  
server_ip = server_ip.rsplit(" ")
server_ip = str(server_ip[-1])

# create raw scenegraph
graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

nettrans = avango.gua.nodes.NetTransform( Name = "net"
                                        , Groupname = "AVSERVER|{0}|7432".format(server_ip))
graph.Root.value.Children.value.append(nettrans)

# create scenegraph list
scenegraphs = [graph]

# create scene list, strings must match a class name in Scene.py
scenes = ["SceneMedievalTown"]
#scenes = ["SceneValcamonicaOptimized"]

# if true, scenes will be switchable using the number buttons
enable_key_bindings = True

## alternative scenes:
# SceneWeimar
# SceneMonkey
# SceneMedievalTown
# ScenePitoti
# SceneVianden
# SceneViandenLow
# SceneViandenHigh
# ScenePLOD