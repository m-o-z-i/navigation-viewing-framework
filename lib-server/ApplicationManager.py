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

from   scene_config import scenegraphs

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

  ## @var all_user_reprsentations
  # List of all UserRepresentation instances active in the setup.
  all_user_representations = []

  def __init__(self):
    self.super(ApplicationManager).__init__()

  ## Custom constructor
  # @param WORKSPACE_CONFIG Filepath of the workspace configuration file to be loaded.
  # @param START_CLIENTS Boolean saying if the client processes are to be started automatically.
  def my_constructor(self, WORKSPACE_CONFIG, START_CLIENTS):

    _workspace_config_file_name = WORKSPACE_CONFIG.replace(".py", "")
    _workspace_config_file_name = _workspace_config_file_name.replace("/", ".")
    exec 'from ' + _workspace_config_file_name + ' import workspaces'

    avango.gua.load_shading_models_from("data/materials")
    avango.gua.load_materials_from("data/materials")
    
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

    ## @var workspaces
    # List of all workspace instances loaded from workspace configuration file.
    self.workspaces = workspaces

    ## @var requestable_navigations
    # Navigation instances which are switchable to by a button press on the device.
    self.requestable_navigations = []

    ## @var requestable_navigations_last_button_states
    # Last button states of the request buttons of requestable navigations to detect changes.
    self.requestable_navigations_last_button_states = []

    for _workspace in self.workspaces:

      _w_id = _workspace.id 

      for _user in _workspace.users:

        _u_id = _user.id

        for _display_group in _workspace.display_groups:

          _dg_id = _display_group.id

          # fill list of requestable navigations
          for _navigation in _display_group.navigations:
            if _navigation.is_requestable == True:
              self.requestable_navigations.append( (_workspace, _display_group, _navigation) )
              self.requestable_navigations_last_button_states.append(False)

          # create view transform node only when free slot is availa
          _view_transform_node = avango.gua.nodes.TransformNode(Name = "w" + str(_w_id) + "_dg" + str(_dg_id) + "_u" + str(_u_id))
          self.NET_TRANS_NODE.Children.value.append(_view_transform_node)

          # create user representation in display group
          _user_repr = _user.create_user_representation_for(_display_group, _view_transform_node)
          ApplicationManager.all_user_representations.append(_user_repr)

          # create tool representation in display_group
          for _tool in _workspace.tools:
            _tool_repr = _tool.create_ray_pointer_representation_for(_display_group, _user_repr)

          for _display in _display_group.displays:

            _s_id = _display_group.displays.index(_display)

            # only add screen node for user when free slot is available
            if _u_id < len(_display.displaystrings):
              _user_repr.add_screen_node_for(_display)
              _user_repr.add_screen_visualization_for(_display)

              # add screen visualization for all screens in workspace
              #for _display_group_2 in _workspace.display_groups:
              #  for _display_2 in _display_group_2.displays:
              #    _user_repr.add_screen_visualization_for(_display_group_2, _display_2)

              # add other screen geometries
            else:
              print_warning("Warning: No empty slot left for user " + str(_u_id) + " in workspace " + str(_workspace.name) + " on display " + str(_display.name))
              continue
            
            # start a client on display host if necessary (only once)
            if START_CLIENTS and _u_id == 0:

              if _display.hostname != _hostname:

                # run client process on host
                # command line parameters: server ip, platform id, display name, screen number
                _ssh_run = subprocess.Popen(["ssh", _display.hostname, _directory_name + \
                "/start-client.sh " + _server_ip + " " + str(WORKSPACE_CONFIG) + " " + str(_w_id) + " " + \
                str(_dg_id) + " " + str(_s_id) + " " + _display.name]
                , stderr=subprocess.PIPE)
                time.sleep(1)

    
        for _user_representation in _user.user_representations:
          _user_representation.connect_navigation_of_display_group(0)

    # initialize avatar group names
    for _workspace in self.workspaces:
      for _display_group in _workspace.display_groups:
        for _user in _workspace.users:
          _user.handle_correct_visibility_groups_for(_display_group.id)

    # set avatar groups properly on all user representations
    #self.init_avatar_group_names()

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
    #self.screen.Width.value = 160/1.5 * 0.85
    #self.screen.Height.value = 100/1.5 * 0.85
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

    # set render mask properly
    _render_mask = "(main_scene"

    for _user_repr in ApplicationManager.all_user_representations:
      _render_mask = _render_mask + " | " + _user_repr.view_transform_node.Name.value

    _render_mask = _render_mask + ") && !do_not_display_group"

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

  ## Evaluated every frame.
  def evaluate(self):

    for _requestable_nav in self.requestable_navigations:

      _workspace = _requestable_nav[0]
      _display_group = _requestable_nav[1]
      _navigation = _requestable_nav[2]
      _requestable_nav_index = self.requestable_navigations.index(_requestable_nav)
      _last_button_state = self.requestable_navigations_last_button_states[_requestable_nav_index]

      # if button change from negative to positive, trigger action
      #print _navigation.sf_request_trigger.value

      if _navigation.sf_request_trigger.value == True and \
         _last_button_state == False:

        self.requestable_navigations_last_button_states[_requestable_nav_index] = True

        # trigger coupling
        if _navigation.active_user_representations == []:
          
          _users_in_range = _workspace.get_all_users_in_range(avango.gua.make_inverse_mat(_display_group.offset_to_workspace) * _navigation.device.tracking_reader.sf_abs_vec.value, 0.8)

          for _user in _users_in_range:
            self.switch_navigation_for(_workspace.id, _display_group.id, _user.id, _display_group.navigations.index(_navigation))

        # reset coupling
        else:

          # get user ids to be reset to navigation 0
          _active_user_ids = []

          for _user_repr in _navigation.active_user_representations:
            _active_user_ids.append(_user_repr.USER.id)

          # switch navigation for 
          for _user_id in _active_user_ids:
            self.switch_navigation_for(_workspace.id, _display_group.id, _user_id, 0)

      # if button change from positive to negative, reset flag
      elif _navigation.sf_request_trigger.value == False and \
           _last_button_state == True:

        self.requestable_navigations_last_button_states[_requestable_nav_index] = False




  ## Initializes the GroupNames field of all UserRepresentation's avatars.
  # Users cannot see the avatars in own display group, but the ones in others.
  def init_avatar_group_names(self):

    for _user_repr_1 in ApplicationManager.all_user_representations:

      for _user_repr_2 in ApplicationManager.all_user_representations:

        if _user_repr_2.DISPLAY_GROUP != _user_repr_1.DISPLAY_GROUP:

          _user_repr_1.append_to_avatar_group_names(_user_repr_2.view_transform_node.Name.value)

  ## Switches the navigation for a user at a display group. 
  # @param WORKSPACE_ID The workspace id in which the user is active.
  # @param DISPLAY_GROUP_ID The display group id to change the navigation for.
  # @param USER_ID The user id to change the navigation for.
  # @param NAVIGATION_ID The navigation id to change to.
  def switch_navigation_for(self, WORKSPACE_ID, DISPLAY_GROUP_ID, USER_ID, NAVIGATION_ID):

    _user_instance = self.workspaces[WORKSPACE_ID].users[USER_ID]
    _user_instance.switch_navigation_at_display_group(DISPLAY_GROUP_ID, NAVIGATION_ID, self.workspaces[WORKSPACE_ID].users)

  ## Starts the shell and the viewer.
  # @param LOCALS Local variables.
  # @param GLOBALS Global variables.
  def run(self, LOCALS, GLOBALS):
    self.shell.start(LOCALS, GLOBALS)
    self.viewer.run()

  ## Lists the variables of the shell.
  def list_variables(self):
    self.shell.list_variables()
