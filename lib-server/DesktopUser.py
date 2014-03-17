#!/usr/bin/python

## @file
# Contains class DesktopUser.

# import guacamole libraries
import avango
import avango.gua
import avango.oculus

# import framework libraries
from User import *
from TrackingReader import *

# import math libraries
import math

## Internal representation of a desktop user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates screens, eyes, camera, pipeline
# and initializes the headtracking.

class DesktopUser(User):

  ## Custom constructor.
  # @param VIEWING_MANAGER Reference to the ViewingManager instance from which the user is created.
  # @param DESKTOP_USER_ID Identification number of the OVRUser to be created, starting from 0.
  # @param PLATFORM_ID Platform to append the constructed OVRUser to.
  # @param WINDOW_SIZE Resolution of the window to be created on the display. [width, height]
  # @param SCREEN_SIZE Physical width of the screen space to be rendered on in meters. [width, height]
  # @param AVATAR_MATERIAL Material to be used for the desktop user's avatar
  def __init__(self, VIEWING_MANAGER, DESKTOP_USER_ID, PLATFORM_ID, WINDOW_SIZE, SCREEN_SIZE, AVATAR_MATERIAL):
    User.__init__(self, "desktop", AVATAR_MATERIAL)

    ## @var VIEWING_MANAGER
    # Reference to the ViewingManager instance from which the user is created.
    self.VIEWING_MANAGER = VIEWING_MANAGER

    ## @var window_size
    # The window's resolution in pixels to be applied.
    self.window_size = avango.gua.Vec2ui(WINDOW_SIZE[0], WINDOW_SIZE[1])

    ## @var id
    # Identification number of the DesktopUser, starting from 0.
    self.id = DESKTOP_USER_ID

    ## @var platform_id
    # ID number of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID
    
    # create platform transform node
    ## @var head_transform
    # Scenegraph node representing the head position of the user with respect to platform. In desktop case,
    # the head is at the platform's position.
    self.head_transform = avango.gua.nodes.TransformNode(Name = "desktop_head_" + str(self.id))

    # create screen
    ## @var screen
    # Scenegraph node representing the user's screen.
    self.screen = avango.gua.nodes.ScreenNode(Name = "desktop_screen_" + str(self.id))

    # take the physical size from config file; alternatively one could use:
    # self.screen.Width.value = self.window_size.x * (1.6/1920)
    # self.screen.Height.value = self.window_size.y * (1.0/1080)
    self.screen.Width.value = SCREEN_SIZE[0]
    self.screen.Height.value = SCREEN_SIZE[1]
    self.screen.Transform.value = avango.gua.make_trans_mat(0.0, 1.2, 0.0)

    ## @var eye
    # Scenegraph node representing the user's eye.
    self.eye = avango.gua.nodes.TransformNode(Name = "eye")
    self.eye.Transform.value = avango.gua.make_identity_mat()

    # viewing setup
    self.append_to_platform(self.VIEWING_MANAGER.SCENEGRAPH, self.head_transform)
    self.append_to_platform(self.VIEWING_MANAGER.SCENEGRAPH, self.screen)
    self.head_transform.Children.value.append(self.eye)

    # create default headtracking value supplier
    ## @var headtracking_reader
    # TrackingReader instance to supply constant basic tracking values.
    self.headtracking_reader = TrackingDefaultReader()
    self.headtracking_reader.set_no_tracking_matrix(avango.gua.make_trans_mat(0, 1.2, 1.5))
    self.head_transform.Transform.connect_from(self.headtracking_reader.sf_abs_mat)

    # create avatar representation
    self.create_avatar_representation(self.VIEWING_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat)

    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()