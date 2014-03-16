#!/usr/bin/python

## @file
# Contains class ViewingManager.

# import guacamole libraries
import avango
import avango.gua
import avango.daemon
from   examples_common.GuaVE import GuaVE

# import framework libraries
from   Navigation       import *
from   Platform         import *
from   User             import *
from   OVRUser          import *
from   PowerWallUser    import *
from   DesktopUser      import *
from   BorderObserver   import *
from   ConfigFileParser import *
from   StatusManager    import *
import Tools

## Class to manage all navigations and users in the viewing setup.
#
# Creates Navigation, OVRUser, PowerWallUser and BorderObserver instances according to the preferences read in from a XML configuration file.
# Therefore, an instance of ConfigFileParser is created and used.

class ViewingManager():
  
  ## @var viewer
  # The guacamole viewer to be used for rendering.
  viewer = avango.gua.nodes.Viewer()

  ## @var shell
  # The GuaVE shell to be used when the application is running.
  shell = GuaVE()

  ## Custom constructor
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param CONFIG_FILE Path to the XML configuration file.
  def __init__(self, SCENEGRAPH, CONFIG_FILE):
    
    # parameters
    ## @var background_texture
    # The skymap to be used for all pipelines.
    self.background_texture = "data/textures/sky.jpg"
    avango.gua.create_texture(self.background_texture)

    # references
    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    # variables
    ## @var powerwall_user_list
    # List of all created PowerWallUser instances.
    self.powerwall_user_list  = []

    ## @var ovr_user_list
    # List of all created OVRUser instances.
    self.ovr_user_list        = []

    ## @var desktop_user_list
    # List of all created DesktopUser instances.
    self.desktop_user_list        = []

    ## @var navigation_list
    # List of all created Navigation instances.
    self.navigation_list      = []

    ## @var border_observer_list
    # List of all created BorderObserver instances.
    self.border_observer_list = []

    ## @var status_manager
    # A StatusManager instance in order to arrange the user display for the different stati.
    self.status_manager = StatusManager()
    self.status_manager.my_constructor(self.ovr_user_list, self.desktop_user_list, self.powerwall_user_list)

    # create file parser and load file
    ## @var config_file_parser
    # Instance of ConfigFileParser in order to load and parse an XML configuration file.
    self.config_file_parser = ConfigFileParser(self)
    self.config_file_parser.parse(CONFIG_FILE)

    self.viewer.SceneGraphs.value = [self.SCENEGRAPH]

  ## Creates a Navigation instance and adds it to the list of navigations.
  # @param INPUT_DEVICE_TYPE Type of the input device to be associated (e.g. XBoxController" or "OldSpheron")
  # @param INPUT_DEVICE_NAME Name of the input device values as chosen in daemon.
  # @param STARTING_MATRIX Initial platform matrix for the new device.
  # @param PLATFORM_SIZE Physical size of the platform in meters. [width, depth]
  # @param ANIMATE_COUPLING Boolean indicating if an animation should be done when a coupling of Navigations is initiated.
  # @param MOVEMENT_TRACES Boolean indicating if the platform should leave traces behind.
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  # @param GROUND_FOLLOWING_SETTINGS Setting list for the GroundFollowing instance: [activated, ray_start_height]
  # @param DEVICE_TRACKING_NAME Name of the device's tracking sensor as chosen in daemon if available.
  def create_navigation(self, INPUT_DEVICE_TYPE, INPUT_DEVICE_NAME, STARTING_MATRIX, PLATFORM_SIZE, ANIMATE_COUPLING, MOVEMENT_TRACES, NO_TRACKING_MAT, GROUND_FOLLOWING_SETTINGS, DEVICE_TRACKING_NAME = None):
    _navigation = Navigation()
    _navigation.my_constructor(self.SCENEGRAPH, PLATFORM_SIZE, STARTING_MATRIX, self.navigation_list, INPUT_DEVICE_TYPE, INPUT_DEVICE_NAME, NO_TRACKING_MAT, GROUND_FOLLOWING_SETTINGS, ANIMATE_COUPLING, MOVEMENT_TRACES, self.status_manager, DEVICE_TRACKING_NAME)
    self.navigation_list.append(_navigation)
    self.border_observer_list.append(None)

  ## Creates a PowerWallUser instance and adds it to the list of PowerWallUsers.
  # @param TRACKING_TARGET_NAME Name of the glasses' tracking target as chosen in daemon.py
  # @param PLATFORM_ID Platform to which the user should be appended to.
  # @param TRANSMITTER_OFFSET The transmitter offset to be applied.
  # @param WARNINGS Boolean value to determine if the user should be appended to a BorderObserver (i.e. the user is shown warning planes when close to the platform borders)
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  def create_powerwall_user(self, TRACKING_TARGET_NAME, PLATFORM_ID, TRANSMITTER_OFFSET, WARNINGS, NO_TRACKING_MAT):
    _user = PowerWallUser(self, TRACKING_TARGET_NAME, len(self.powerwall_user_list), PLATFORM_ID, NO_TRACKING_MAT, TRANSMITTER_OFFSET, self.navigation_list[PLATFORM_ID].trace_material)
    self.powerwall_user_list.append(_user)

    # init border checker to warn user on platform
    if WARNINGS:
      if self.border_observer_list[PLATFORM_ID] == None:
        _checked_borders = [False, False, True, False]
        self.create_border_observer(_checked_borders, _user, self.navigation_list[PLATFORM_ID].platform)
      else:
        self.border_observer_list[PLATFORM_ID].add_user(_user)

  ## Creates a OVRUser instance and adds it to the list of OVRUsers.
  # @param TRACKING_TARGET_NAME Name of the Oculus Rift's tracking target as chosen in daemon.py
  # @param PLATFORM_ID Platform to which the user should be appended to.
  # @param WARNINGS Boolean value to determine if the user should be appended to a BorderObserver (i.e. the user is shown warning planes when close to the platform borders)
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  def create_ovr_user(self, TRACKING_TARGET_NAME, PLATFORM_ID, WARNINGS, NO_TRACKING_MAT):
    _user = OVRUser(self, TRACKING_TARGET_NAME, len(self.ovr_user_list), PLATFORM_ID, NO_TRACKING_MAT, self.navigation_list[PLATFORM_ID].trace_material)
    self.ovr_user_list.append(_user)
   
    # init border checker to warn user on platform
    if WARNINGS:
      if self.border_observer_list[PLATFORM_ID] == None:
        _checked_borders = [True, True, True, True]
        self.create_border_observer(_checked_borders, _user, self.navigation_list[PLATFORM_ID].platform)
      else:
        self.border_observer_list[PLATFORM_ID].add_user(_user)

  ## Creates a DesktopUser instance and adds it to the list of DesktopUsers.
  # @param PLATFORM_ID Platform to which the user should be appended to.
  # @param WINDOW_SIZE Resolution of the window to be created on the display. [width, height]
  # @param SCREEN_SIZE Physical width of the screen space to be rendered on in meters. [width, height]
  def create_desktop_user(self, PLATFORM_ID, WINDOW_SIZE, SCREEN_SIZE):
    _user = DesktopUser(self, len(self.desktop_user_list), PLATFORM_ID, WINDOW_SIZE, SCREEN_SIZE, self.navigation_list[PLATFORM_ID].trace_material)
    self.desktop_user_list.append(_user)
   

  ## Creates a BorderObserver instance for a Platform and adds a User to it.
  # @param CHECKED_BORDERS A list of four booleans to indicate which borders of the platform should be checked: 
  # [display_left_border, display_right_border, display_front_border, display_back_border]
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


