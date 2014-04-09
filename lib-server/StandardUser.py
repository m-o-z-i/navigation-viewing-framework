#!/usr/bin/python

## @file
# Contains class StandardUser.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from User import *
from TrackingReader import *

# import math libraries
import math

## Internal representation of a standard user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates eyes
# and initializes the headtracking.

class StandardUser(User):

  ##
  #
  def __init__(self, VIEWING_MANAGER, USER_ID, STEREO, HEADTRACKING_TARGET_NAME, PLATFORM_ID, AVATAR_MATERIAL):

    User.__init__(self, AVATAR_MATERIAL)

    # variables
    ## @var VIEWING_MANAGER
    # Reference to the ViewingManager instance from which the user is created.
    self.VIEWING_MANAGER = VIEWING_MANAGER

    ## @var id
    # Identification number of the PowerWallUser, starting from 0.
    self.id = USER_ID

    ## @var platform_id
    # ID of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID

    ## @var platform
    # Instance of the platform the user is belonging to.
    self.platform = self.VIEWING_MANAGER.navigation_list[self.platform_id].platform

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset   = self.platform.transmitter_offset

    ## @var no_tracking_mat
    # The matrix to be applied when no tracking is available.
    self.no_tracking_mat      = self.platform.no_tracking_mat

    # init viewing setup 
    ## @var head_transform
    # Scenegraph node representing the head position of the user with respect to platform.
    self.head_transform = avango.gua.nodes.TransformNode(Name = "head_" + str(self.id))
    self.platform.platform_transform_node.Children.value.append(self.head_transform)

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

      self.set_eye_distance(0.06)
      
    else:
      # create the eye
      ## @var eye
      # Scenegraph node representing the user's eye.
      self.eye = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.eye)

    # create avatar representation
    if self.platform.avatar_type == "joseph":
      self.create_avatar_representation(self.VIEWING_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat, False)
    elif self.platform.avatar_type == "joseph_table":
      self.create_avatar_representation(self.VIEWING_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat, True)
    
    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()


  ## Correctly places and appends the message plane node in and to the scenegraph.
  def handle_message_plane_node(self):
    self.message_plane_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.18) * \
                                              avango.gua.make_rot_mat(90, 1, 0, 0)

    for _screen in self.platform.screens:
      _screen.Children.value.append(self.message_plane_node)

  ## Handles all the specialized settings for the coupling status overview.
  def handle_coupling_status_attributes(self):
    self.coupling_status_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.screen.Children.value.append(self.coupling_status_node)

    ## @var start_trans
    # Translation of the first coupling status notifier (own color).
    self.start_trans = avango.gua.Vec3(-0.433 * self.screen.Width.value, 0.454 * self.screen.Height.value, 0.0)
      
    ## @var start_scale
    # Scaling of the first coupling status notifier (own color).
    self.start_scale = 0.1
      
    ## @var y_increment
    # Y offset for all coupling status notifiers after the own color.
    self.y_increment = -0.14