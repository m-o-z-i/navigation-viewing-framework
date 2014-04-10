#!/usr/bin/python

## @file
# Server application for the distributed viewing setup.

# import guacamole libraries
import avango
import avango.gua

# import framwork libraries
from SceneManager import *
from ViewingManager import *

# import python libraries
import sys

# Command line parameters:
# main.py CONFIG_FILE SERVER_IP
# @param CONFIG_FILE The filname of the configuration file to parse.
# @param SERVER_IP The own IP address.

## Main method for the server application
def start():

  # initialize materials
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")

  # create loader class for geometry loading
  loader = avango.gua.nodes.GeometryLoader()

  # create scenegraph
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  # get server ip 
  server_ip = str(sys.argv[2])

  # initialize pseudo nettrans node as client processes are started in Platform.py
  pseudo_nettrans = avango.gua.nodes.TransformNode(Name = "net")
  graph.Root.value.Children.value = [pseudo_nettrans]

  # initialize viewing setup
  viewing_manager = ViewingManager(
      NET_TRANS_NODE = pseudo_nettrans
    , SCENEGRAPH = graph
    , CONFIG_FILE = sys.argv[1])

  # create distribution node and sync children from pseudo nettrans
  nettrans = avango.gua.nodes.NetTransform(
      Name = "net"
    , Groupname = "AVSERVER|{0}|7432".format(server_ip)
  )

  nettrans.Children.value = pseudo_nettrans.Children.value
  graph.Root.value.Children.value = [nettrans]

  # initialize scene
  scene_manager = SceneManager(loader, nettrans, viewing_manager)

  # distribute all nodes in the scenegraph
  distribute_all_nodes(nettrans, nettrans)

  # run application loop
  viewing_manager.run(locals(), globals())

## Registers a scenegraph node and all of its children at a NetMatrixTransform node for distribution.
# @param NET_TRANS_NODE The NetMatrixTransform node on which all nodes should be marked distributable.
# @param PARENT_NODE The node that should be registered distributable with all of its children.
def distribute_all_nodes(NET_TRANS_NODE, PARENT_NODE):

  # do not distribute the nettrans node itself
  if PARENT_NODE != NET_TRANS_NODE:
    NET_TRANS_NODE.distribute_object(PARENT_NODE)

  # iterate over children and make them distributable
  for _child in PARENT_NODE.Children.value:
    distribute_all_nodes(NET_TRANS_NODE, _child)


if __name__ == '__main__':
  start()
