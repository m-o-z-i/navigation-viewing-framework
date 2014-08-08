#!/usr/bin/python

## @file
# Server application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from SceneManager import *
from ApplicationManager import *
from RecorderPlayer import *
from Manipulation import *
from Portal import *
from PortalCamera import *
from PortalInteractionSpace import *
from Device import *

# import python libraries
import sys
import subprocess

# Command line parameters:
# main.py CONFIG_FILE
# @param CONFIG_FILE The filname of the configuration file to parse.
# @param START_CLIENTS Boolean saying if the client processes are to be started automatically.

## Main method for the server application
def start():

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

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

  # initialize portal manager
  portal_manager = PortalManager()
  portal_manager.my_constructor(graph, application_manager.navigation_list)

  portal_camera = PortalCamera()
  portal_camera.my_constructor(0, portal_manager, application_manager.navigation_list[0], "device-portal-camera-32", "tracking-portal-camera-32")

  portal_camera_2 = PortalCamera()
  portal_camera_2.my_constructor(1, portal_manager, application_manager.navigation_list[0], "device-portal-camera-31", "tracking-portal-camera-31")

  table_device = SpacemouseDevice()
  table_device.my_constructor("device-spacemouse", avango.gua.make_identity_mat())
  table_device.translation_factor = 0.01

  table_interaction_space = PortalInteractionSpace()
  table_interaction_space.my_constructor(portal_manager
                                       , table_device
                                       , application_manager.navigation_list[0].platform
                                       , avango.gua.Vec3(-2.441, 0.956, 1.635)
                                       , avango.gua.Vec3(-1.450, 1.021, 2.936)
                                       , 90.0)
  portal_camera.add_interaction_space(table_interaction_space)
  portal_camera_2.add_interaction_space(table_interaction_space)

  _table_shot = Shot()
  _table_shot.my_constructor(avango.gua.make_rot_mat(-90, 1, 0, 0),
                             80.0,
                             "3D",
                             "PERSPECTIVE",
                             "True")

  table_interaction_space.add_maximized_shot(_table_shot, avango.gua.make_identity_mat(), 1.0, 1.0)

  # initialize animation manager
  #animation_manager = AnimationManager()
  #animation_manager.my_constructor([ graph["/net/platform_0"]]
  #                               , [ application_manager.navigation_list[0]])

  #manipulation_manager = ManipulationManager(nettrans, graph, scene_manager)

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
