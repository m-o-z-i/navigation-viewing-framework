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
import hyperspace_config

# import python libraries
import sys
import subprocess

# Command line parameters:
# main.py CONFIG_FILE
# @param CONFIG_FILE The filname of the configuration file to parse.
# @param START_CLIENTS Boolean saying if the client processes are to be started automatically.


class TimedObjectRotation(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in milliseconds.
  TimeIn = avango.SFFloat()

  MatrixIn = avango.gua.SFMatrix4()
  MatrixOut = avango.gua.SFMatrix4()

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    self.MatrixOut.value = self.MatrixIn.value * avango.gua.make_rot_mat(self.TimeIn.value * 8.0, 0.0, 1.0, 0.0)




def toggle_office(graph):

  if graph["/net/SceneVRHyperspace6/terrain_group"].GroupNames.value[0] == "pre_scene2":

    graph["/net/SceneVRHyperspace6/terrain_group"].GroupNames.value = ["do_not_display_group"]
    graph["/net/SceneVRHyperspace6/office"].GroupNames.value = ["main_scene"]
    graph["/net/SceneVRHyperspace6/office_molecule"].GroupNames.value = ["main_scene"]
    #graph["/net/SceneVRHyperspace6/office_call"].GroupNames.value = ["main_scene"]

  else:

    graph["/net/SceneVRHyperspace6/terrain_group"].GroupNames.value = ["pre_scene2"]
    graph["/net/SceneVRHyperspace6/office"].GroupNames.value = ["do_not_display_group"]
    graph["/net/SceneVRHyperspace6/office_molecule"].GroupNames.value = ["do_not_display_group"]
    #graph["/net/SceneVRHyperspace6/office_call"].GroupNames.value = ["do_not_display_group"]


def toggle_venice(graph):

  if graph["/net/SceneVRHyperspace3/venice"].GroupNames.value[0] == "pre_scene2":

    graph["/net/SceneVRHyperspace3/venice"].GroupNames.value = ["do_not_display_group"]
    graph["/net/SceneVRHyperspace3/terrain_group"].GroupNames.value = ["pre_scene2"]

  else:

    graph["/net/SceneVRHyperspace3/venice"].GroupNames.value = ["pre_scene2"]
    graph["/net/SceneVRHyperspace3/terrain_group"].GroupNames.value = ["do_not_display_group"]


def hide_call_tex(graph):

  hyperspace_config.texture_idx += 1
  if hyperspace_config.texture_idx >= len(hyperspace_config.textures[hyperspace_config.active_scenes[0]]):
    hyperspace_config.texture_idx = 0

  graph["/net/SceneVRHyperspace5/call_textures"].GroupNames.value = ["do_not_display_group"]


def rotate_molecule(graph):

  timer = avango.nodes.TimeSensor()

  molecule_updater = TimedObjectRotation()
  molecule_updater.TimeIn.connect_from(timer.Time)
  molecule_updater.MatrixIn.value = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-60.80, 6.5, 8.8)
  graph["/net/SceneVRHyperspace6/office_molecule"].Transform.connect_from(molecule_updater.MatrixOut)


def scale_molecule(graph, scale = 1.0):

  graph["/net/SceneVRHyperspace6/office_molecule"].Transform.disconnect()
  graph["/net/SceneVRHyperspace6/office_molecule"].Transform.value = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-60.80, 6.5, 8.8) * avango.gua.make_scale_mat(scale)


def toggle_ad_pillar(graph):

  if graph["/net/SceneVRHyperspace4/ad_pillar"].GroupNames.value[0] == "do_not_display_group":

    graph["/net/SceneVRHyperspace4/ad_pillar"].GroupNames.value = ["main_scene"]

  else:

    graph["/net/SceneVRHyperspace4/ad_pillar"].GroupNames.value = ["do_not_display_group"]


def toggle_call_pillar(graph):

  if graph["/net/SceneVRHyperspace5/call_pillar"].GroupNames.value[0] == "do_not_display_group":

    graph["/net/SceneVRHyperspace5/call_pillar"].GroupNames.value = ["main_scene"]

  else:

    graph["/net/SceneVRHyperspace5/call_pillar"].GroupNames.value = ["do_not_display_group"]


def print_camera_pos(graph):
  print "translation:    " + str(graph["/net/platform_0"].Transform.value.get_translate())
  print "rotation angle: " + str(graph["/net/platform_0"].Transform.value.get_rotate().get_angle())
  print "rotation axis:  " + str(graph["/net/platform_0"].Transform.value.get_rotate().get_axis())


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

  '''
  portal_camera = PortalCamera()
  portal_camera.my_constructor(0, portal_manager, application_manager.navigation_list[0], "device-portal-camera-32", "tracking-portal-camera-32")

  portal_camera_2 = PortalCamera()
  portal_camera_2.my_constructor(1, portal_manager, application_manager.navigation_list[0], "device-portal-camera-31", "tracking-portal-camera-31")

  table_device = SpacemouseDevice()
  table_device.my_constructor("device-spacemouse", avango.gua.make_identity_mat())
  table_device.translation_factor = 0.01

  table_interaction_space = PortalInteractionSpace()
  table_interaction_space.my_constructor(table_device
                                       , application_manager.navigation_list[0].platform
                                       , avango.gua.Vec3(-2.441, 0.956, 1.635)
                                       , avango.gua.Vec3(-1.450, 1.021, 2.936)
                                       , 90.0)
  portal_camera.add_interaction_space(table_interaction_space)
  portal_camera_2.add_interaction_space(table_interaction_space)

  _table_portal = portal_manager.add_portal(avango.gua.make_rot_mat(-90, 1, 0, 0),
                                            80.0,
                                            avango.gua.make_identity_mat(),
                                            4.0,
                                            2.0,
                                            "3D",
                                            "PERSPECTIVE",
                                            "True",
                                            "data/materials/ShadelessBlue.gmd")
  table_interaction_space.add_maximized_portal(_table_portal)
  '''

  if [i for i in [1, 3, 5, 6, 7] if i in hyperspace_config.active_scenes]:
    # initialize animation manager
    animation_manager = AnimationManager()

    '''
    animation_manager.my_constructor([ graph["/net/platform_0"]]
                                   , [ application_manager.navigation_list[0]])
    animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"], graph["/net/SceneVRHyperspace1/ceiling_light2"], graph["/net/SceneVRHyperspace1/ceiling_light3"], graph["/net/SceneVRHyperspace1/ceiling_light4"], graph["/net/SceneVRHyperspace1/ceiling_light5"], graph["/net/SceneVRHyperspace1/ceiling_light6"]]
                                   , [None, None, None, None, None, None])
    animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"]]
                                   , [None])
    animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"], graph["/net/SceneVRHyperspace1/ceiling_light2"]]
                                   , [None, None])
    animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/ceiling_light1"], graph["/net/SceneVRHyperspace1/ceiling_light2"], graph["/net/SceneVRHyperspace1/ceiling_light3"], graph["/net/SceneVRHyperspace1/ceiling_light4"]]
                                   , [None, None, None, None])
    animation_manager.my_constructor([graph["/net/SceneVRHyperspace1/steppo"]]
                                   , [None])
    '''

    _nodes = [ graph["/net/platform_0"] ]
    for scene_num in hyperspace_config.active_scenes:
      _scene_nodes = hyperspace_config.animation_nodes[scene_num]
      if _scene_nodes:
        for node_name in _scene_nodes:
          _nodes += [ graph[node_name] ]

    # scenes where the platform node is to be animated
    #_nav_node = []
    #if [i for i in [5] if i in hyperspace_config.active_scenes]:
    #  _nav_node = [ application_manager.navigation_list[0]]
    #  _nodes += [ graph["/net/platform_0/scene{0}".format(hyperspace_config.active_scenes[0])] ]

    animation_manager.my_constructor(_nodes, [ application_manager.navigation_list[0]] + [None] * (len(_nodes) - 1))
    animation_manager.play_recording_by_node_name("/net/SceneVRHyperspace3/terrain_group")
    #animation_manager.play_recording_by_node_name("/net/SceneVRHyperspace4/terrain_group")
    animation_manager.play_recording_by_node_name("/net/SceneVRHyperspace6/terrain_group")
    animation_manager.play_recording_by_node_name("/net/SceneVRHyperspace2b/terrain_group")

    #if hyperspace_config.active_scenes == [3]:
    #  animation_manager.my_constructor([graph["/net/SceneVRHyperspace3/terrain_group"]], [None])

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
