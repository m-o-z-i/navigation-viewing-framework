#!/usr/bin/python

## @file
# Contains class ApplicationManager.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.daemon
from   examples_common.GuaVE import GuaVE

# import framework libraries
from   Navigation       import *
from   Platform         import *
from   User             import *
from   BorderObserver   import *
from   ConfigFileParser import *
from   SlotManager      import *
from   ConsoleIO        import *
from   display_config   import displays
import Tools


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
    , NET_TRANS_NODE
    , SCENEGRAPH
    , CONFIG_FILE
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
    self.SCENEGRAPH = SCENEGRAPH

    ## @var NET_TRANS_NODE
    # Reference to the net transformation node.
    self.NET_TRANS_NODE = NET_TRANS_NODE

    # variables
    ## @var user_list
    # List of all created user instances.
    self.user_list  = []

    ## @var navigation_list
    # List of all created Navigation instances.
    self.navigation_list      = []

    ## @var border_observer_list
    # List of all created BorderObserver instances.
    self.border_observer_list = []

    ## @var start_clients
    # Boolean saying if the client processes are to be started automatically.
    self.start_clients = START_CLIENTS

    # kill all running python processes on display hosts
    if self.start_clients:
      _own_hostname = open('/etc/hostname', 'r').readline().strip(" \n")

      for _display in displays:
        if _display.hostname != _own_hostname:
          _ssh_kill = subprocess.Popen(["ssh", _display.hostname, "killall python"])

    ## @var slot_manager
    # A SlotManager instance in order to handle the shutter timings of users.
    self.slot_manager = SlotManager()
    self.slot_manager.my_constructor(self.user_list)

    # create file parser and load file
    ## @var config_file_parser
    # Instance of ConfigFileParser in order to load and parse an XML configuration file.
    self.config_file_parser = ConfigFileParser(self)
    self.config_file_parser.parse(CONFIG_FILE)    

    # care for correct slot assignment
    self.slot_manager.update_slot_configuration()

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
    self.pipeline.Enabled.value = False
    
    # add pipeline and scenegraph to viewer
    self.viewer.Pipelines.value = [self.pipeline]
    self.viewer.SceneGraphs.value = [self.SCENEGRAPH]

  ## Creates a Navigation instance and adds it to the list of navigations.
  # @param INPUT_DEVICE_TYPE Type of the input device to be associated (e.g. XBoxController" or "OldSpheron")
  # @param INPUT_DEVICE_NAME Name of the input device values as chosen in daemon.
  # @param STARTING_MATRIX Initial platform matrix for the new device.
  # @param PLATFORM_SIZE Physical size of the platform in meters. [width, depth]
  # @param SCALE Start scaling of the platform.
  # @param ANIMATE_COUPLING Boolean indicating if an animation should be done when a coupling of Navigations is initiated.
  # @param MOVEMENT_TRACES Boolean indicating if the platform should leave traces behind.
  # @param INVERT Boolean indicating if the input values should be inverted.
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  # @param GROUND_FOLLOWING_SETTINGS Setting list for the GroundFollowing instance: [activated, ray_start_height]
  # @param TRANSMITTER_OFFSET The matrix offset that is applied to the values delivered by the tracking system.
  # @param DISPLAYS The names of the displays that belong to this navigation.
  # @param AVATAR_TYPE A string that determines what kind of avatar representation is to be used ["joseph", "joseph_table", "kinect"].
  # @param CONFIG_FILE The path to the config file that is used.
  # @param DEVICE_TRACKING_NAME Name of the device's tracking sensor as chosen in daemon if available.
  def create_navigation(
      self
    , INPUT_DEVICE_TYPE
    , INPUT_DEVICE_NAME
    , STARTING_MATRIX
    , PLATFORM_SIZE
    , SCALE
    , ANIMATE_COUPLING
    , MOVEMENT_TRACES
    , INVERT
    , NO_TRACKING_MAT
    , GROUND_FOLLOWING_SETTINGS
    , TRANSMITTER_OFFSET
    , DISPLAYS
    , AVATAR_TYPE
    , CONFIG_FILE
    , DEVICE_TRACKING_NAME = None
    ):
    
    # convert list of parsed display strings to the corresponding instances
    _display_instances = []
    _displays_found = list(DISPLAYS)

    # create bool list if displays were found
    for _i in range(len(_displays_found)):
      _displays_found[_i] = False

    # search for display instances
    for _i in range(len(DISPLAYS)):
      for _display_instance in displays:
        if _display_instance.name == DISPLAYS[_i]:
          _display_instances.append(_display_instance)
          _displays_found[_i] = True
    
    # check if all display instances were found
    for _i in range(len(_displays_found)):
      if _displays_found[_i] == False:
        print_error("No matching display instance found for " + DISPLAYS[_i], True)

    # create the navigation instance
    _navigation = Navigation()
    _navigation.my_constructor(
        NET_TRANS_NODE = self.NET_TRANS_NODE
      , SCENEGRAPH = self.SCENEGRAPH
      , PLATFORM_SIZE = PLATFORM_SIZE
      , SCALE = SCALE
      , STARTING_MATRIX = STARTING_MATRIX
      , NAVIGATION_LIST = self.navigation_list
      , INPUT_SENSOR_TYPE = INPUT_DEVICE_TYPE
      , INPUT_SENSOR_NAME = INPUT_DEVICE_NAME
      , NO_TRACKING_MAT = NO_TRACKING_MAT
      , GF_SETTINGS = GROUND_FOLLOWING_SETTINGS
      , ANIMATE_COUPLING = ANIMATE_COUPLING
      , MOVEMENT_TRACES = MOVEMENT_TRACES
      , INVERT = INVERT
      , SLOT_MANAGER = self.slot_manager
      , TRANSMITTER_OFFSET = TRANSMITTER_OFFSET
      , DISPLAYS = _display_instances
      , AVATAR_TYPE = AVATAR_TYPE
      , CONFIG_FILE = CONFIG_FILE
      , START_CLIENTS = self.start_clients
      , TRACKING_TARGET_NAME = DEVICE_TRACKING_NAME
    )
    self.navigation_list.append(_navigation)
    self.border_observer_list.append(None)

  ## Creates a user.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param GLASSES_ID ID of the shutter glasses worn by the user.
  # @param PLATFORM_ID The ID of the platform this user belongs to.
  # @param HEADTRACKING_TARGET_NAME The headtracking target identifier attached to this user.
  # @param HMD_SENSOR_NAME Name of the HMD sensor belonging to the user, if applicable.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param WARNINGS Boolean indicating whether to display warning planes when the user gets close to the platform borders.
  def create_user(
      self
    , VIP
    , GLASSES_ID
    , PLATFORM_ID
    , HEADTRACKING_TARGET_NAME
    , HMD_SENSOR_NAME
    , EYE_DISTANCE
    , WARNINGS
    ):
    _user = User()
    _user.my_constructor(self
                       , len(self.user_list)
                       , VIP
                       , GLASSES_ID
                       , HEADTRACKING_TARGET_NAME
                       , HMD_SENSOR_NAME
                       , EYE_DISTANCE
                       , PLATFORM_ID
                       , self.navigation_list[PLATFORM_ID].trace_material
                       )
    self.user_list.append(_user)

    # init border checker to warn user on platform
    if WARNINGS:
      if self.border_observer_list[PLATFORM_ID] == None:
        _checked_borders = [True, True, True, True]
        self.create_border_observer(_checked_borders, _user, self.navigation_list[PLATFORM_ID].platform)
      else:
        self.border_observer_list[PLATFORM_ID].add_user(_user)
   

  ## Creates a BorderObserver instance for a Platform and adds a User to it.
  # @param CHECKED_BORDERS A list of four booleans to indicate which borders of the platform should be checked: 
  #                        [display_left_border, display_right_border, display_front_border, display_back_border]
  # @param USER_INSTANCE A first User to be appended to the new BorderObserver.
  # @param PLATFORM_INSTANCE The platform to which the BorderObserver should belong to.
  def create_border_observer(self, CHECKED_BORDERS, USER_INSTANCE, PLATFORM_INSTANCE):
    _border_observer = BorderObserver()
    _border_observer.my_constructor(CHECKED_BORDERS, USER_INSTANCE, PLATFORM_INSTANCE)
    self.border_observer_list[PLATFORM_INSTANCE.platform_id] = _border_observer

  ## Starts the shell and the viewer.
  # @param LOCALS Local variables.
  # @param GLOBALS Global variables.
  def run(self, LOCALS, GLOBALS):
    self.shell.start(LOCALS, GLOBALS)
    self.viewer.run()

  ## Lists the variables of the shell.
  def list_variables(self):
    self.shell.list_variables()
