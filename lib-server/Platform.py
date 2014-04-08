#!/usr/bin/python

## @file
# Contains class Platform.

# import guacamole libraries
import avango
import avango.gua
import avango.script
import avango.daemon
from   avango.script import field_has_changed

# import python libraries
import subprocess
import os


## Internal representation of a platform which is controlled by an input device.
#
# Users can stick themselves to a platform and explore the scene on it.

class Platform(avango.script.Script):

  # input and output field
  ## @var sf_abs_mat
  # Matrix representing the current translation and rotation of the platform in the scene.
  sf_abs_mat = avango.gua.SFMatrix4()
  sf_abs_mat.value = avango.gua.make_identity_mat()

  ##
  #
  hosts_visited = []
  
  ## Default constructor.
  def __init__(self):
    self.super(Platform).__init__()

  ## Custom constructor.
  # @param NET_TRANS_NODE Reference to the net matrix node in the scenegraph for distribution.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param PLATFORM_SIZE Physical size of the platform in meters. Passed in an two-element list: [width, depth]
  # @param INPUT_MAPPING_INSTANCE An instance of InputMapping which accumulates the device inputs for this platform.
  # @param PLATFORM_ID The id number assigned to this platform, starting from 0.
  #
  #
  #
  #
  def my_constructor(self, NET_TRANS_NODE, SCENEGRAPH, PLATFORM_SIZE, INPUT_MAPPING_INSTANCE, PLATFORM_ID, TRANSMITTER_OFFSET, NO_TRACKING_MAT, DISPLAYS, AVATAR_TYPE, CONFIG_FILE):

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

    ##
    #
    self.transmitter_offset = TRANSMITTER_OFFSET

    ##
    #
    self.no_tracking_mat = NO_TRACKING_MAT

    ##
    #
    self.displays = DISPLAYS

    ##
    #
    self.avatar_type = AVATAR_TYPE

    # get own ip adress
    _server_ip = subprocess.Popen(["hostname", "-I"], stdout=subprocess.PIPE).communicate()[0]
    _server_ip = _server_ip.strip(" \n")

    # open ssh connection for all hosts associated to display
    for _display in self.displays:
      # TODO: append screen nodes to platform

      _directory_name = os.path.dirname(os.path.dirname(__file__))

      # run ClientDaemon on host if necessary
      if _display.name not in Platform.hosts_visited:
        #_ssh_run = subprocess.Popen(["ssh", _display.hostname, _directory_name + "/start-client-daemon.sh"])
        Platform.hosts_visited.append(_display.name)

      # run client process on host
      # command line parameters: server ip, platform id, config file
      _ssh_run = subprocess.Popen(["ssh", _display.hostname, _directory_name + "/start-client.sh " + _server_ip + " " + str(self.platform_id) + " " + _display.name + " " + CONFIG_FILE], stderr=subprocess.PIPE)

    # connect to input mapping instance
    self.sf_abs_mat.connect_from(INPUT_MAPPING_INSTANCE.sf_abs_mat)

    # extend scenegraph with platform node
    ## @var platform_transform_node
    # Scenegraph node representing this platform's transformation.
    self.platform_transform_node = avango.gua.nodes.TransformNode(Name = "platform_" + str(PLATFORM_ID))
    self.platform_transform_node.Transform.connect_from(self.sf_abs_mat)
    NET_TRANS_NODE.Children.value.append(self.platform_transform_node)

    # create four boundary planes
    _loader = avango.gua.nodes.GeometryLoader()

    ## @var left_border
    # Geometry scenegraph node of the platform's left border
    self.left_border = _loader.create_geometry_from_file('left_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)

    self.left_border.Transform.value = avango.gua.make_trans_mat(-self.width/2, 1.0, self.depth/2) * \
                                       avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                       avango.gua.make_rot_mat(270, 0, 0, 1) * \
                                       avango.gua.make_scale_mat(self.depth, 1, 2)
    self.left_border.GroupNames.value = ["do_not_display_group", "platform_group_" + str(PLATFORM_ID)]
    self.platform_transform_node.Children.value.append(self.left_border)
    
    ## @var right_border
    # Geometry scenegraph node of the platform's left border
    self.right_border = _loader.create_geometry_from_file('right_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.right_border.Transform.value = avango.gua.make_trans_mat(self.width/2, 1.0, self.depth/2) * \
                                        avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                        avango.gua.make_rot_mat(90, 0, 0, 1) * \
                                        avango.gua.make_scale_mat(self.depth, 1, 2)
    self.right_border.GroupNames.value = ["do_not_display_group", "platform_group_" + str(PLATFORM_ID)]
    self.platform_transform_node.Children.value.append(self.right_border)

    ## @var front_border
    # Geometry scenegraph node of the platform's front border
    self.front_border = _loader.create_geometry_from_file('front_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.front_border.Transform.value = avango.gua.make_trans_mat(0, 1, 0) * \
                                        avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                        avango.gua.make_scale_mat(self.width, 1, 2)
    self.front_border.GroupNames.value = ["do_not_display_group", "platform_group_" + str(PLATFORM_ID)]
    self.platform_transform_node.Children.value.append(self.front_border)

    ## @var back_border
    # Geometry scenegraph node of the platform's back border
    self.back_border = _loader.create_geometry_from_file('back_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.back_border.Transform.value = avango.gua.make_trans_mat(0.0, 1.0, self.depth) * \
                                        avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                        avango.gua.make_rot_mat(180, 0, 0, 1) * \
                                        avango.gua.make_scale_mat(self.width, 1, 2)
    self.back_border.GroupNames.value = ["do_not_display_group", "platform_group_" + str(PLATFORM_ID)]
    self.platform_transform_node.Children.value.append(self.back_border)   

  ## Toggles visibility of left platform border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_left_border(self, VISIBLE):
    if VISIBLE:
      self.left_border.GroupNames.value[0] = "display_group"
    else:
      self.left_border.GroupNames.value[0] = "do_not_display_group"

  ## Toggles visibility of right platform border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_right_border(self, VISIBLE):
    if VISIBLE:
      self.right_border.GroupNames.value[0] = "display_group"
    else:
      self.right_border.GroupNames.value[0] = "do_not_display_group"

  ## Toggles visibility of front platform border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_front_border(self, VISIBLE):
    if VISIBLE:
      self.front_border.GroupNames.value[0] = "display_group"
    else:
      self.front_border.GroupNames.value[0] = "do_not_display_group"

  ## Toggles visibility of back platform border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_back_border(self, VISIBLE):
    if VISIBLE:
      self.back_border.GroupNames.value[0] = "display_group"
    else:
      self.back_border.GroupNames.value[0] = "do_not_display_group"
