#!/usr/bin/python

## @file
# Server application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.gua
#import avango.utils

# import framework libraries
from SceneManager import *
from ApplicationManager import *
from RecorderPlayer import *
from Manipulation import *
from TUIO import *

# import python libraries
import sys
import subprocess

# Command line parameters:
# main.py CONFIG_FILE
# @param CONFIG_FILE The filname of the configuration file to parse.
# @param START_CLIENTS Boolean saying if the client processes are to be started automatically.

## Main method for the server application
def start():

  # create scenegraph
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")
  #graph.Root.value.GroupNames.value = ["all"]

  # get server ip 
  server_ip = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE).communicate()[0]
  server_ip = server_ip.strip(" \n")  
  server_ip = server_ip.rsplit(" ")
  server_ip = str(server_ip[-1])

  # initialize pseudo nettrans node as client processes are started in Platform class
  pseudo_nettrans = avango.gua.nodes.TransformNode(Name = "net")
  graph.Root.value.Children.value = [pseudo_nettrans]

  print sys.argv[2]

  if sys.argv[2] == "True":
    start_clients = True 
  else:
    start_clients = False

  # initialize application manager
  application_manager = ApplicationManager(
      NET_TRANS_NODE = pseudo_nettrans
    , SCENEGRAPH = graph
    , CONFIG_FILE = sys.argv[1]
    , START_CLIENTS = start_clients)

  # create distribution node and sync children from pseudo nettrans
  nettrans = avango.gua.nodes.NetTransform(
      Name = "net"
    , Groupname = "AVSERVER|{0}|7432".format(server_ip)
  )
  #nettrans.GroupNames.value = ["all"]

  nettrans.Children.value = pseudo_nettrans.Children.value
  graph.Root.value.Children.value.remove(pseudo_nettrans)
  graph.Root.value.Children.value.append(nettrans)

  # update nettrans node on all platforms
  for _nav in application_manager.navigation_list:
    _nav.platform.update_nettrans_node(nettrans)

  # initialize scene
  scene_manager = SceneManager()
  scene_manager.my_constructor(nettrans, graph, application_manager.navigation_list)

  # initialize touch devices
  multi_touch_devices = []
  for i in application_manager.navigation_list:
    for j in i.platform.displays:
      if "TUIO" in j.get_touch_protocols():
        device = TUIODevice()
        device.my_constructor(graph, j)
        print_message("TUIO touch display '{}' detected.".format(j.name))
        multi_touch_devices.append(device)

  # initialize animation manager
  #animation_manager = AnimationManager()
  #animation_manager.my_constructor([ graph["/net/platform_0"]]
  #                               , [ application_manager.navigation_list[0]])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"], graph["/net/SceneVRHyperspace1/ceiling_light2"], graph["/net/SceneVRHyperspace1/ceiling_light3"], graph["/net/SceneVRHyperspace1/ceiling_light4"], graph["/net/SceneVRHyperspace1/ceiling_light5"], graph["/net/SceneVRHyperspace1/ceiling_light6"]]
  #                               , [None, None, None, None, None, None])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"]]
  #                               , [None])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"], graph["/net/SceneVRHyperspace1/ceiling_light2"]]
  #                               , [None, None])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"], graph["/net/SceneVRHyperspace1/ceiling_light2"], graph["/net/SceneVRHyperspace1/ceiling_light3"], graph["/net/SceneVRHyperspace1/ceiling_light4"]]
  #                               , [None, None, None, None])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/steppo"]]
  #                               , [None])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace3/terrain_group"], graph["/net/SceneVRHyperspace4/terrain_group"]]
  #                               , [None, None])
  #animation_manager.my_constructor([graph["/net/SceneVRHyperspace3/terrain_group"]]
  #                               , [None])

  manipulation_manager = ManipulationManager(nettrans, graph, scene_manager)

  ## distribute all nodes in the scenegraph
  distribute_all_nodes(nettrans, nettrans)


  # run application loop
  application_manager.run(locals(), globals())

## Registers a scenegraph node and all of its children at a NetMatrixTransform node for distribution.
# @param NET_TRANS_NODE The NetMatrixTransform node on which all nodes should be marked distributable.
# @param PARENT_NODE The node that should be registered distributable with all of its children.
def distribute_all_nodes(NET_TRANS_NODE, NODE):

  # do not distribute the nettrans node itself
  if NODE != NET_TRANS_NODE:
    NET_TRANS_NODE.distribute_object(NODE)
    #print "distribute", NODE, NODE.Name.value, NODE.Path.value

  # iterate over children and make them distributable
  for _child in NODE.Children.value:
    distribute_all_nodes(NET_TRANS_NODE, _child)


if __name__ == '__main__':
  start()
