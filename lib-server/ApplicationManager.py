#!/usr/bin/python

## @file
# Contains class ApplicationManager.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.daemon
from   examples_common.GuaVE import GuaVE

# import framework libraries
from   ConsoleIO        import *
import Tools

from   scenegraph_config import scenegraphs
from   workspace_config import workspaces

# import python libraries
import subprocess

## Class to manage all navigations and users in the viewing setup.
#
# Creates Navigation, OVRUser, PowerWallUser and BorderObserver instances according to the preferences read in from a XML configuration file.
# Therefore, an instance of ConfigFileParser is created and used.

class ApplicationManager():
  
  ## @var viewer
  # The guacamole viewer to be used for rendering.
  viewer = avango.gua.nodes.Viewer()

  ## @var shell
  # The GuaVE shell to be used when the application is running.
  shell = GuaVE()

  ## Custom constructor
  # @param NET_TRANS_NODE Reference to the net transformation node.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param CONFIG_FILE Path to the XML configuration file.
  # @param START_CLIENTS Boolean saying if the client processes are to be started automatically.
  def __init__(
      self
    , START_CLIENTS
    ):
    
    # parameters
    ## @var background_texture
    # The skymap to be used for all pipelines.
    self.background_texture = "data/textures/sky.jpg"
    avango.gua.create_texture(self.background_texture)

    # references
    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = scenegraphs[0]

    ## @var NET_TRANS_NODE
    # Reference to the net transformation node.
    self.NET_TRANS_NODE = self.SCENEGRAPH["/net"]

    ## @var start_clients
    # Boolean saying if the client processes are to be started automatically.
    self.start_clients = START_CLIENTS

    # kill all running python processes on display hosts
    if self.start_clients:
      _own_hostname = open('/etc/hostname', 'r').readline().strip(" \n")

      for _workspace in workspaces:
        for _display_group in _workspace.display_groups:
          for _display in _display_group.display_list:

            if _display.hostname != _own_hostname:
              _ssh_kill = subprocess.Popen(["ssh", _display.hostname, "killall python"])

    # server control monitor setup #

    ## @var server_transform
    # Transform node representing the position and orientation of the server control monitor.
    self.server_transform = avango.gua.nodes.TransformNode(Name = "server_transform")
    self.server_transform.Transform.value = avango.gua.make_trans_mat(0, 20, 0) * \
                                            avango.gua.make_rot_mat(-90, 1, 0, 0)
    self.NET_TRANS_NODE.Children.value.append(self.server_transform)

    ## @var eye
    # Transform node representing the server's eye
    self.eye = avango.gua.nodes.TransformNode(Name = "server_eye")
    self.eye.Transform.value = avango.gua.make_trans_mat(0, 0, 0)
    self.server_transform.Children.value.append(self.eye)

    ## @var screen
    # Screen node representing the server's screen.
    self.screen = avango.gua.nodes.ScreenNode(Name = "server_screen")
    self.screen.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.5)
    #self.screen.Width.value = 160/1.5 * 0.1
    #self.screen.Height.value = 100/1.5 * 0.1
    self.screen.Width.value = 160/1.5 * 0.85
    self.screen.Height.value = 100/1.5 * 0.85    
    self.server_transform.Children.value.append(self.screen)

    ## @var camera
    # Camera used for the server control monitor.
    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = self.SCENEGRAPH.Name.value
    self.camera.LeftScreen.value = self.screen.Path.value
    self.camera.RightScreen.value = self.screen.Path.value
    self.camera.LeftEye.value = self.eye.Path.value
    self.camera.RightEye.value = self.eye.Path.value
    self.camera.Mode.value = 1

    _render_mask = "!do_not_display_group && !server_do_not_display_group"

    for i in range(0, 10):
      _render_mask = _render_mask + " && !platform_group_" + str(i)

    self.camera.RenderMask.value = _render_mask

    ## @var window
    # Window displaying the server control view.
    self.window = avango.gua.nodes.Window()
    self.window.Title.value = "Server Control Monitor"
    self.window.Size.value = avango.gua.Vec2ui(1280, 1024)
    self.window.LeftResolution.value = avango.gua.Vec2ui(1280, 1024)

    ## @var pipeline
    # Pipeline repsonsible for rendering the server control monitor.
    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.BackgroundMode.value = avango.gua.BackgroundMode.COLOR
    self.pipeline.Window.value = self.window
    self.pipeline.LeftResolution.value = self.window.LeftResolution.value
    self.pipeline.EnableStereo.value = False
    self.pipeline.Camera.value = self.camera
    self.pipeline.EnableFrustumCulling.value = True
    self.pipeline.EnableSsao.value = False
    self.pipeline.EnableFPSDisplay.value = True
    #self.pipeline.Enabled.value = False
    
    # add pipeline and scenegraph to viewer
    self.viewer.Pipelines.value = [self.pipeline]
    self.viewer.SceneGraphs.value = [self.SCENEGRAPH]


  ## Starts the shell and the viewer.
  # @param LOCALS Local variables.
  # @param GLOBALS Global variables.
  def run(self, LOCALS, GLOBALS):
    self.shell.start(LOCALS, GLOBALS)
    self.viewer.run()

  ## Lists the variables of the shell.
  def list_variables(self):
    self.shell.list_variables()
