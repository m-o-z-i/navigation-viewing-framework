#!/usr/bin/python

## @file
# Client application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.script
import avango.gua
import avango.oculus

# import framework libraries
import ClientMaterialUpdaters
from View import *
from ClientPortal import *
from examples_common.GuaVE import GuaVE

# import python libraries
import sys

# Command line parameters:
# main.py SERVER_IP WORKSPACE_CONFIG_FILE WORKSPACE_ID DISPLAY_GROUP_ID SCREEN_ID DISPLAY_NAME

## Main method for the client application.
def start():

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

  # get the server ip
  server_ip = str(sys.argv[1])

  # get the workspace config file #
  workspace_config_file = str(sys.argv[2])
  exec 'from ' + workspace_config_file.replace("/", ".").replace(".py", "") + ' import displays'

  # get the workspace id
  workspace_id = int(sys.argv[3])

  # get the display group id
  display_group_id = int(sys.argv[4])

  # get the screen id
  screen_id = int(sys.argv[5])

  # get the display name
  display_name = str(sys.argv[6])

  # get own hostname
  hostname = open('/etc/hostname', 'r').readline()
  hostname = hostname.strip(" \n")

  print "This client is running on", hostname, "and listens to server", server_ip
  print "It is responsible for workspace", workspace_id, ", display group", display_group_id, "and screen", screen_id

  # create distribution node
  nettrans = avango.gua.nodes.NetTransform(
                Name = "net",
                # specify role, ip, and port
                Groupname = "AVCLIENT|{0}|7432".format(server_ip)
                )

  # create a dummy scenegraph to be extended by distribution
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  graph.Root.value.Children.value = [nettrans]

  # create material updaters as this cannot be distributed
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")
  
  timer = avango.nodes.TimeSensor()
  
  water_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  water_updater.MaterialName.value = "data/materials/Water.gmd"
  water_updater.UniformName.value = "time"
  water_updater.TimeIn.connect_from(timer.Time)

  # get the display instance
  for _display in displays:
    if _display.name == display_name:
      handled_display_instance = _display

  # create a viewer
  viewer = avango.gua.nodes.Viewer()

  # Create a view for each displaystring (= slot)
  _string_num = 0
  views = []

  for _displaystring in handled_display_instance.displaystrings:

    _view = View()
    _view.my_constructor(graph, 
                         viewer,
                         handled_display_instance, 
                         workspace_id,
                         display_group_id,
                         screen_id,
                         _string_num)
    views.append(_view)
    _string_num += 1

  viewer.SceneGraphs.value = [graph]

  # create client portal manager
  portal_manager = ClientPortalManager()
  portal_manager.my_constructor(graph, views)

  shell = GuaVE()
  shell.start(locals(), globals())

  # start rendering process
  viewer.run()

if __name__ == '__main__':
  start()
