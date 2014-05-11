#!/usr/bin/python

## @file
# Contains class User.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from TrackingReader import *
from ConsoleIO import *

# import math libraries
import math

## Internal representation of a user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates eyes
# and initializes the headtracking.

class User:

  ## Custom constructor.
  # @param APPLICATION_MANAGER Reference to the ApplicationManager instance from which this user is created.
  # @param USER_ID Global user ID to be applied.
  # @param STEREO Boolean indicating if this user is a stereo or mono one.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param PLATFORM_ID Platform ID to which this user should be appended to.
  # @param AVATAR_MATERIAL The material string for the user avatar to be created.
  def __init__(self, APPLICATION_MANAGER, USER_ID, STEREO, HEADTRACKING_TARGET_NAME, PLATFORM_ID, AVATAR_MATERIAL):

    # variables
    ## @var APPLICATION_MANAGER
    # Reference to the ApplicationManager instance from which the user is created.
    self.APPLICATION_MANAGER = APPLICATION_MANAGER

    ## @var id
    # Identification number of the PowerWallUser, starting from 0.
    self.id = USER_ID

    ## @var platform_id
    # ID of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID

    ## @var platform
    # Instance of the platform the user is belonging to.
    self.platform = self.APPLICATION_MANAGER.navigation_list[self.platform_id].platform

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset   = self.platform.transmitter_offset

    ## @var no_tracking_mat
    # The matrix to be applied when no tracking is available.
    self.no_tracking_mat      = self.platform.no_tracking_mat
    
    ## @var avatar_material
    # Material of the user's avatar.
    self.avatar_material = AVATAR_MATERIAL

    self.eye_distance = 0.0

    # init viewing setup 
    ## @var head_transform
    # Scenegraph node representing the head position of the user with respect to platform.
    self.head_transform = avango.gua.nodes.TransformNode(Name = "head_" + str(self.id))
    #self.platform.platform_transform_node.Children.value.append(self.head_transform)
    self.platform.platform_scale_transform_node.Children.value.append(self.head_transform)

    ## @var headtracking_reader
    # Instance of a child class of TrackingReader to supply translation input.
    if HEADTRACKING_TARGET_NAME == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(self.no_tracking_mat)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())
   
    # connect the tracking input to the scenegraph node
    self.head_transform.Transform.connect_from(self.headtracking_reader.sf_abs_mat)

    if STEREO:
      # create the eyes
      ## @var left_eye
      # Scenegraph node representing the user's left eye.
      self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.left_eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.left_eye)

      ## @var right_eye
      # Scenegraph node representing the user's right eye.
      self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
      self.right_eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.right_eye)

      self.set_eye_distance(0.065)
      
    else:
      # create the eye
      ## @var eye
      # Scenegraph node representing the user's eye.
      self.eye = avango.gua.nodes.TransformNode(Name = "eye")
      self.eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.eye)

    # create avatar representation
    if self.platform.avatar_type == "joseph":
      self.create_avatar_representation(self.APPLICATION_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat)
    else:
      print_error("Error: Unknown avatar type " + self.platform.avatar_type, True)
  
  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    self.eye_distance = VALUE
  
    self.left_eye.Transform.value  = avango.gua.make_trans_mat(self.eye_distance * -0.5, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(self.eye_distance * 0.5, 0.0, 0.0)

  ## Appends a node to the children of a platform in the scenegraph.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param NODE The node to be appended to the platform node.
  def append_to_platform(self, SCENEGRAPH, NODE):
    
    # find corresponding platform node
    _platform_path = "/net/platform_" + str(self.platform_id) + "/scale"
    _node = SCENEGRAPH.get_node(_platform_path)
    _node.Children.value.append(NODE)

  ## Creates a basic "joseph" avatar for this user.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param SF_AVATAR_BODY_MATRIX Field containing the transformation matrix for the avatar's body on the platform.
  def create_avatar_representation(self, SCENEGRAPH, SF_AVATAR_BODY_MATRIX):

    _loader = avango.gua.nodes.GeometryLoader()
    
    # create avatar head
    ## @var head_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_avatar = _loader.create_geometry_from_file( 'head_avatar_' + str(self.id),
                                                          'data/objects/Joseph/JosephHead.obj',
                                                          'data/materials/' + self.avatar_material + '.gmd',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.head_avatar.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
    self.head_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    self.head_transform.Children.value.append(self.head_avatar)

    # create avatar body
    ## @var body_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_avatar = _loader.create_geometry_from_file( 'head_avatar_' + str(self.id),
                                                          'data/objects/Joseph/JosephBody.obj',
                                                          'data/materials/' + self.avatar_material + '.gmd',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.body_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    
    self.append_to_platform(SCENEGRAPH, self.body_avatar)

    self.body_avatar.Transform.connect_from(SF_AVATAR_BODY_MATRIX)