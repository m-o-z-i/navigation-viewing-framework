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

from   scenegraph_config import scenegraphs
from   workspace_config import workspaces

# import python libraries
import os
import subprocess
import time

## Class to build the scenegraph from the Workspaces, Display Groups and Users created.
# Builds a server control monitor for debugging purposes.

class ApplicationManager(avango.script.Script):
  
  ## @var viewer
  # The guacamole viewer to be used for rendering.
  viewer = avango.gua.nodes.Viewer()

  ## @var shell
  # The GuaVE shell to be used when the application is running.
  shell = GuaVE()

  def __init__(self):
    self.super(ApplicationManager).__init__()

  ## Custom constructor
  # @param START_CLIENTS Boolean saying if the client processes are to be started automatically.
  def my_constructor(self, START_CLIENTS):
    
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
          for _display in _display_group.displays:

            if _display.hostname != _own_hostname:
              print "kill on", _display.hostname
              _ssh_kill = subprocess.Popen(["ssh", _display.hostname, "killall python -9"])


    # viewing setup and start of client processes #

    if START_CLIENTS:

      # get own ip adress
      _server_ip = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE).communicate()[0]
      _server_ip = _server_ip.strip(" \n")
      _server_ip = _server_ip.rsplit(" ")
      _server_ip = str(_server_ip[-1])

      # get own hostname
      _hostname = open('/etc/hostname', 'r').readline()
      _hostname = _hostname.strip(" \n")

      # get directory name
      _directory_name = os.path.dirname(os.path.dirname(__file__))

    else:
      print_warning("Start of clients disabled for debugging reasons.")


    for _workspace in workspaces:

      _w_id = _workspace.id 

      for _display_group in _workspace.display_groups:

        _dg_id = _display_group.id

        for _display in _display_group.displays:

          _s_id = _display_group.displays.index(_display)

          # start a client on display host if necessary
          if START_CLIENTS:

            if _display.hostname != _hostname:

              # run client process on host
              # command line parameters: server ip, platform id, display name, screen number
              print "/start-client.sh " + _server_ip + " " + str(_w_id) + " " + \
                    str(_dg_id) + " " + str(_s_id) + " " + _display.name

              _ssh_run = subprocess.Popen(["ssh", _display.hostname, _directory_name + \
              "/start-client.sh " + _server_ip + " " + str(_w_id) + " " + \
              str(_dg_id) + " " + str(_s_id) + " " + _display.name]
              , stderr=subprocess.PIPE)
              print "start client on", _display.hostname
              time.sleep(1)

          for _user in _workspace.users:

            _u_id = _user.id

            if _u_id < len(_display.displaystrings):

              _nav_node = avango.gua.nodes.TransformNode(Name = "w" + str(_w_id) + "_dg" + str(_dg_id) + "_s" + str(_s_id) + "_u" + str(_u_id))
              _nav_node.Transform.connect_from(_user.matrices_per_display_group[_dg_id].Transform)
              self.NET_TRANS_NODE.Children.value.append(_nav_node)

              _screen_node = _display.create_screen_node(Name = "screen")
              _nav_node.Children.value.append(_screen_node)

              _head_node = avango.gua.nodes.TransformNode(Name = "head")
              _head_node.Transform.connect_from(_user.headtracking_reader.sf_abs_mat)
              _nav_node.Children.value.append(_head_node)

              _left_eye_node = avango.gua.nodes.TransformNode(Name = "eyeL")
              _left_eye_node.Transform.value = avango.gua.make_trans_mat(-_user.eye_distance / 2, 0.0, 0.0)
              _head_node.Children.value.append(_left_eye_node)

              _right_eye_node = avango.gua.nodes.TransformNode(Name = "eyeR")
              _right_eye_node.Transform.value = avango.gua.make_trans_mat(_user.eye_distance / 2, 0.0, 0.0)
              _head_node.Children.value.append(_right_eye_node)


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

    self.always_evaluate(True)


  ## Starts the shell and the viewer.
  # @param LOCALS Local variables.
  # @param GLOBALS Global variables.
  def run(self, LOCALS, GLOBALS):
    self.shell.start(LOCALS, GLOBALS)
    self.viewer.run()

  ## Lists the variables of the shell.
  def list_variables(self):
    self.shell.list_variables()
