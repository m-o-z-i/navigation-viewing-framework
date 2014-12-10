#!/usr/bin/python

## @file
# Server application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from SceneManager import *
from ApplicationManager import *
from Portal import *
from PortalCamera import *
from Device import *

from scene_config import scenegraphs

# import multitouch
from MultiTouch.TUIO import TUIODevice

# import python libraries
import sys
import subprocess

# Command line parameters:
# main.py START_CLIENTS
# @param START_CLIENTS Boolean saying if the client processes are to be started automatically.

## Main method for the server application
def start():

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

  workspace_config = sys.argv[1]

  if sys.argv[2] == "True":
    start_clients = True 
  else:
    start_clients = False

  # preload materials and shading models
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")

  # initialize application manager
  application_manager = ApplicationManager()
  application_manager.my_constructor(WORKSPACE_CONFIG = workspace_config, START_CLIENTS = start_clients)

  # initialize scene
  scene_manager = SceneManager()

  # initialize touch devices
  multi_touch_device = None

  for _workspace in application_manager.workspaces:
    for _display_group in _workspace.display_groups:
      for _display in _display_group.displays:
        if "TUIO" in _display.get_touch_protocols():
          if None == multi_touch_device:
            device = TUIODevice()
            device.my_constructor(scenegraphs[0], _display, scenegraphs[0]["/net"], scene_manager, application_manager)
            multi_touch_device = device


  # initialize animation manager
  #animation_manager = AnimationManager()
  #animation_manager.my_constructor([ graph["/net/platform_0"]]
  #                               , [ application_manager.navigation_list[0]])

  ## distribute all nodes in the scenegraph
  distribute_all_nodes(scenegraphs[0]["/net"], scenegraphs[0]["/net"])

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
