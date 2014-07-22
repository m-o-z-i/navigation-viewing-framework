#!/usr/bin/python

## @file
# Contains class Platform.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
import avango.daemon
from   avango.script import field_has_changed

# import framework libraries
from SlotManager import *
from Slot        import *
from ConsoleIO   import *

# import python libraries
import subprocess
import os
import time


## Internal representation of a platform which is controlled by an input device.
#
# Users can stick themselves to a platform and explore the scene on it.

class Platform(avango.script.Script):

  # input and output field
  ## @var sf_abs_mat
  # Matrix representing the current translation and rotation of the platform in the scene.
  sf_abs_mat = avango.gua.SFMatrix4()
  sf_abs_mat.value = avango.gua.make_identity_mat()

  ## @var sf_scale
  # The current scaling factor of this platform.
  sf_scale = avango.SFFloat()
  sf_scale.value = 1.0

  ## @var sf_scale_mat
  # The current scaling matrix of this platform.
  sf_scale_mat = avango.gua.SFMatrix4()
  sf_scale_mat.value = avango.gua.make_scale_mat(sf_scale.value)

  ## @var hosts_visited
  # List of hostnames on which a client daemon was already launched. Used to avoid double launching.
  hosts_visited = []
  
  ## Default constructor.
  def __init__(self):
    self.super(Platform).__init__()

    ## @var start_clients
    # Debug flag saying if client processes should be started.
    self.start_clients = True

    ## @var screens
    # List of ScreenNode instances which are appended to this platform.
    self.screens = []

  ## Custom constructor.
  # @param NET_TRANS_NODE Reference to the net matrix node in the scenegraph for distribution.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param PLATFORM_SIZE Physical size of the platform in meters. Passed in an two-element list: [width, depth]
  # @param INPUT_MAPPING_INSTANCE An instance of InputMapping which accumulates the device inputs for this platform.
  # @param PLATFORM_ID The id number assigned to this platform, starting from 0.
  # @param TRANSMITTER_OFFSET The matrix offset that is applied to the values delivered by the tracking system.
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  # @param DISPLAYS The names of the displays that belong to this navigation.
  # @param AVATAR_TYPE A string that determines what kind of avatar representation is to be used ["joseph", "joseph_table", "kinect"].
  # @param SLOT_MANAGER Reference to the one and only SlotManager instance in the setup.
  # @param CONFIG_FILE The path to the config file that is used.
  # @param AVATAR_MATERIAL String containing the material to be used for avatars of this platform.
  # @param START_CLIENTS Boolean saying if the client processes are to be started automatically.
  def my_constructor(
      self
    , NET_TRANS_NODE
    , SCENEGRAPH
    , PLATFORM_SIZE
    , INPUT_MAPPING_INSTANCE
    , PLATFORM_ID
    , TRANSMITTER_OFFSET
    , NO_TRACKING_MAT
    , DISPLAYS
    , AVATAR_TYPE
    , SLOT_MANAGER
    , CONFIG_FILE
    , AVATAR_MATERIAL
    , START_CLIENTS):

    ## @var NET_TRANS_NODE
    # Reference to the net matrix node in the scenegraph for distribution.
    self.NET_TRANS_NODE = NET_TRANS_NODE

    ## @var platform_id
    # The id number of this platform, starting from 0.
    self.platform_id = PLATFORM_ID   

    ## @var INPUT_MAPPING_INSTANCE
    # Reference to an InputMapping which accumulates the device inputs for this platform.
    self.INPUT_MAPPING_INSTANCE = INPUT_MAPPING_INSTANCE

    ## @var width
    # Physical width of the platform in meters.
    self.width = PLATFORM_SIZE[0]

    ## @var depth
    # Physical depth of the platform in meters.
    self.depth = PLATFORM_SIZE[1]

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset = TRANSMITTER_OFFSET

    ## @var no_tracking_mat
    # The matrix to be applied when no tracking information is available for users.
    self.no_tracking_mat = NO_TRACKING_MAT

    ## @var displays 
    # List of names of the displays that belong to this navigation.
    self.displays = DISPLAYS

    ## @var avatar_type
    # A string that determines what kind of avatar representation is to be used.
    self.avatar_type = AVATAR_TYPE

    ## @var slot_list
    # A list of Slot instances that are associated to this platform.
    self.slot_list = []

    ## @var avatar_material
    # String containing the material to be used for avatars of this platform.
    self.avatar_material = AVATAR_MATERIAL

    # extend scenegraph with platform node
    ## @var platform__node
    # Semantic scenegraph node representing this platform.
    self.platform_transform_node = avango.gua.nodes.TransformNode(Name = "platform_" + str(PLATFORM_ID))
    NET_TRANS_NODE.Children.value.append(self.platform_transform_node)

    ## @var platform_scale_transform_node
    # Scenegraph node representing this platform's scale. Is below platform_transform_node.
    #self.platform_scale_transform_node = avango.gua.nodes.TransformNode(Name = "scale")
    #self.platform_transform_node.Children.value = [self.platform_scale_transform_node]

    self.start_clients = START_CLIENTS

    # get own ip adress
    _server_ip = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE).communicate()[0]
    _server_ip = _server_ip.strip(" \n")
    _server_ip = _server_ip.rsplit(" ")
    _server_ip = str(_server_ip[-1])

    # get own hostname
    _hostname = open('/etc/hostname', 'r').readline()
    _hostname = _hostname.strip(" \n")

    # open ssh connection for all hosts associated to display
    for _display in self.displays:
      # append a screen node to platform

      # create screen proxy geometry for view ray hit tests
      _proxy_geometry = _display.create_transformed_proxy_geometry(self, self.displays.index(_display))
      SCENEGRAPH.Root.value.Children.value.append(_proxy_geometry)

      _string_num = 0
      # create a slot for each displaystring
      for _displaystring in _display.displaystrings:
        
        if _display.stereomode == "HMD":
          # create hmd slot
          _slot = SlotHMD()
          _slot.my_constructor(_display,
                               _string_num,
                               self.displays.index(_display),
                               True,
                               self)
          self.slot_list.append(_slot)
          SLOT_MANAGER.register_slot(_slot, _display)
          #self.screens.append(_slot.left_screen)
          #self.screens.append(_slot.right_screen)

        if _display.stereo == True:
          # create stereo slot
          _slot = Slot()
          _slot.my_constructor(_display,
                               _string_num,
                               self.displays.index(_display),
                               True,
                               self)
          self.slot_list.append(_slot)
          SLOT_MANAGER.register_slot(_slot, _display) 

        else:
          # create mono slot
          _slot = Slot()
          _slot.my_constructor(_display,
                               _string_num,
                               self.displays.index(_display),
                               True,
                               self)
          self.slot_list.append(_slot)
          SLOT_MANAGER.register_slot(_slot, _display)


        _string_num += 1


      _directory_name = os.path.dirname(os.path.dirname(__file__))

      if self.start_clients:
        # run ClientDaemon on host if necessary
        if _display.hostname not in Platform.hosts_visited and \
           _display.hostname != _hostname:
          _ssh_run = subprocess.Popen(["ssh", _display.hostname, _directory_name + "/start-client-daemon.sh"])
          Platform.hosts_visited.append(_display.name)

        # run client process on host
        # command line parameters: server ip, platform id, display name, screen number
        _ssh_run = subprocess.Popen(["ssh", _display.hostname, _directory_name + \
            "/start-client.sh " + _server_ip + " " + str(self.platform_id) + " " + \
            _display.name + " " + str(self.displays.index(_display))]
          , stderr=subprocess.PIPE)
        
        time.sleep(1)
      else:
        print_warning("Start of client on " + _display.hostname + " disabled for debugging reasons.")

    # connect to input mapping instance
    self.sf_abs_mat.connect_from(INPUT_MAPPING_INSTANCE.sf_abs_mat)
    self.sf_scale.connect_from(INPUT_MAPPING_INSTANCE.sf_scale)

    _loader = avango.gua.nodes.TriMeshLoader()

    # create kinect avatars if desired
    if AVATAR_TYPE.endswith(".ks"):

      _video_loader = avango.gua.nodes.Video3DLoader()

      ## @var video_geode
      # Video3D node containing the caputred video geometry.
      self.video_geode = _video_loader.load("kincet", AVATAR_TYPE)

      self.video_geode.Transform.value = self.transmitter_offset
      self.platform_scale_transform_node.Children.value.append(self.video_geode)
      self.video_geode.GroupNames.value = ['avatar_group_' + str(self.platform_id), 'video'] # own group avatars not visible (only for WALL setups)

      ## @var video_abstraction_transform
      # Transform node for the placement of the video abstraction.
      self.video_abstraction_transform = avango.gua.nodes.TransformNode(Name = "video_abstraction_transform")
      self.video_abstraction_transform.Transform.connect_from(self.INPUT_MAPPING_INSTANCE.DEVICE_INSTANCE.sf_station_mat)
      self.platform_scale_transform_node.Children.value.append(self.video_abstraction_transform)

      ## @var video_abstraction
      # Abstract geometry displayed when too far away from the video geode.
      self.video_abstraction = _loader.create_geometry_from_file('video_abstraction',
                                                                 'data/objects/sphere.obj',
                                                                 'data/materials/' + self.avatar_material + 'Shadeless.gmd',
                                                                 avango.gua.LoaderFlags.DEFAULTS)
      self.video_abstraction.Transform.value = avango.gua.make_scale_mat(2.0)
      self.video_abstraction.GroupNames.value = ["video_abstraction", "server_do_not_display_group"]
      self.video_abstraction_transform.Children.value.append(self.video_abstraction)

         
  ## Scales the platform scale transform node when the scaling changes in the inputmapping.
  @field_has_changed(sf_scale)
  def sf_scale_values_changed(self):

    self.sf_scale_mat.value = avango.gua.make_scale_mat(self.sf_scale.value)

  ## Updates the nettrans node. Used to replace pseudo nettrans.
  # @param NET_TRANS_NODE The new nettrans node to be set.
  def update_nettrans_node(self, NET_TRANS_NODE):
    self.NET_TRANS_NODE = NET_TRANS_NODE

  ## Displays the coupling plane with the "Coupling" texture.
  def show_coupling_plane(self):
    for _slot in self.slot_list:
      _slot.show_coupling_plane()

  ## Hides the coupling plane.
  def hide_coupling_plane(self):
    for _slot in self.slot_list:
      _slot.hide_coupling_plane()

  ## Displays coupling status notifiers for all navigations in COUPLED_NAVIGATION_LIST
  # @param COUPLED_NAVIGATION_LIST List of Navigation instances that are now coupled.
  def display_coupling(self, COUPLED_NAVIGATION_LIST):
    for _slot in self.slot_list:
      _slot.display_coupling(COUPLED_NAVIGATION_LIST)

  ## Removes a platform indicator from the coupling display and shows a message to all other platforms.
  # @param NAVIGATION The Navigation instance to be removed from all couplings.
  # @param SHOW_NOTIFICATION Boolean saying if a notification should be displayed to all other platforms involved.
  def remove_from_coupling_display(self, NAVIGATION, SHOW_NOTIFICATION):
    for _slot in self.slot_list:
      _slot.remove_from_coupling_display(NAVIGATION, SHOW_NOTIFICATION)