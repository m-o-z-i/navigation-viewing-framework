#!/usr/bin/python

## @file
# Contains class PowerWallUser.

# import guacamole libraries
import avango.daemon

from examples_common.GuaVE import GuaVE

# import framework libraries
from User import *
from TrackingReader import *

# import math libraries
import math

## Internal representation of a Powerwall user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates screens, eyes, camera, pipeline
# and initializes the headtracking.

class PowerWallUser(User):

  ## Custom constructor.
  # @param VIEWING_MANAGER Reference to the ViewingManager instance from which the user is created.
  # @param HEADTRACKING_TARGET_NAME Name of the glasses' tracking target as chosen in daemon.
  # @param WALL_USER_ID Identification number of the PowerWallUser to be created, starting from 0.
  # @param PLATFORM_ID Platform to append the constructed PowerWallUser to.
  # @param NO_TRACKING_MAT Matrix to be applied if no headtracking of the glasses is available.
  # @param TRANSMITTER_OFFSET The transmitter offset to be applied.
  # @param AVATAR_MATERIAL Material to be used for the powerwall user's avatar
  # @param IDENTIFIER String that identifies which powerwall is used ('small' or 'large').
  def __init__(self, VIEWING_MANAGER, HEADTRACKING_TARGET_NAME, WALL_USER_ID, PLATFORM_ID, NO_TRACKING_MAT, TRANSMITTER_OFFSET, AVATAR_MATERIAL, IDENTIFIER):
    User.__init__(self, "wall", AVATAR_MATERIAL)

    # variables
    ## @var VIEWING_MANAGER
    # Reference to the ViewingManager instance from which the user is created.
    self.VIEWING_MANAGER = VIEWING_MANAGER

    ## @var id
    # Identification number of the PowerWallUser, starting from 0.
    self.id = WALL_USER_ID

    ## @var platform_id
    # ID number of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID

    ## @var left_eye_resolution
    # The user's left eye resolution in pixels.
    self.left_eye_resolution  = avango.gua.Vec2ui(1920, 1200)

    ## @var right_eye_resolution
    # The user's right eye resolution in pixels.
    self.right_eye_resolution = avango.gua.Vec2ui(1920, 1200) 

    ## @var window_size
    # The resolution in pixels to be applied on the window.
    self.window_size          = avango.gua.Vec2ui(1920*2, 1200) 

    ## @var warp_matrices_path
    # Path of the warp matrices to be applied on the rendered image.
    if IDENTIFIER == "large":
        self.warp_matrices_path = "/opt/dlp-warpmatrices/"
    else:
        self.warp_matrices_path = "/opt/lcd-warpmatrices/"

    ## @var screen_size
    # Physical screen size of the Powerwall in meters.
    if IDENTIFIER == "large":
        self.screen_size    = avango.gua.Vec2(4.16, 2.6)
    else:
        self.screen_size    = avango.gua.Vec2(3.0, 1.98)

    ## @var screen_transform
    # Physical transformation of the screen in meters.
    if IDENTIFIER == "large":
        self.screen_transform = avango.gua.make_trans_mat(0.0, 1.57, 0.0)
    else:
        self.screen_transform = avango.gua.make_trans_mat(0.0, 1.42, 0.0)

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset   = TRANSMITTER_OFFSET

    # init viewing setup 
    ## @var head_transform
    # Scenegraph node representing the head position of the user with respect to platform.
    self.head_transform = avango.gua.nodes.TransformNode(Name = "wall_head_" + str(self.id))
    self.append_to_platform(self.VIEWING_MANAGER.SCENEGRAPH, self.head_transform)

    ## @var headtracking_reader
    # Instance of a child class of TrackingReader to supply translation input.
    if HEADTRACKING_TARGET_NAME == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(NO_TRACKING_MAT)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())
    
    # connect the tracking input to the scenegraph node
    self.head_transform.Transform.connect_from(self.headtracking_reader.sf_abs_mat)

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

    # create the screen
    ## @var screen
    # Scenegraph node representing the user's screen.
    self.screen = avango.gua.nodes.ScreenNode(Name = "wall_screen_" + str(self.id))
    self.screen.Width.value = self.screen_size.x
    self.screen.Height.value = self.screen_size.y
    self.screen.Transform.value = self.screen_transform
    self.append_to_platform(self.VIEWING_MANAGER.SCENEGRAPH, self.screen)

    # create avatar representation
    self.create_avatar_representation(self.VIEWING_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat)
    
    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()