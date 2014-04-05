#!/usr/bin/python

## @file
# Contains class OVRUser and TrackingCombiner.

# import guacamole libraries
import avango
import avango.gua
import avango.oculus

# import framework libraries
from User import *
from TrackingReader import *

# import math libraries
import math

## Internal representation of an Oculus Rift user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates screens, eyes, camera, pipeline
# and initializes the headtracking.

class OVRUser(User):

  ## @var window_size
  # The Oculus Rift's resolution in pixels to be applied on the window.
  window_size      = avango.gua.Vec2ui(1280, 800)

  ## @var screen_size
  # Physical screen size of the Oculus Rift in meters.
  screen_size      = avango.gua.Vec2(0.16, 0.1) 

  ## Custom constructor.
  # @param VIEWING_MANAGER Reference to the ViewingManager instance from which the user is created.
  # @param HEADTRACKING_TARGET_NAME Name of the Oculus Rift's tracking target as chosen in daemon.
  # @param USER_ID Identification number of the user to be created, starting from 0.
  # @param PLATFORM_ID Platform to append the constructed OVRUser to.
  # @param NO_TRACKING_MAT Matrix to be applied if no headtracking of the Oculus Rift is available.
  # @param AVATAR_MATERIAL Material to be used for the OVR user's avatar
  def __init__(self, VIEWING_MANAGER, HEADTRACKING_TARGET_NAME, USER_ID, PLATFORM_ID, NO_TRACKING_MAT, AVATAR_MATERIAL):
    User.__init__(self, "ovr", AVATAR_MATERIAL)

    ## @var VIEWING_MANAGER
    # Reference to the ViewingManager instance from which the user is created.
    self.VIEWING_MANAGER = VIEWING_MANAGER

    ## @var id
    # Identification number of the OVRUser, starting from 0.
    self.id = USER_ID

    ## @var platform_id
    # ID number of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID
    
    # create platform transform node
    ## @var head_transform
    # Scenegraph node representing the head position of the user with respect to platform.
    self.head_transform = avango.gua.nodes.TransformNode(Name = "ovr_head_" + str(self.id))

    # create screens
    ## @var left_screen
    # Scenegraph node representing the user's left screen.
    self.left_screen = avango.gua.nodes.ScreenNode(Name = "screenL")
    self.left_screen.Width.value = self.screen_size.x / 2
    self.left_screen.Height.value = self.screen_size.y
    self.left_screen.Transform.value = avango.gua.make_trans_mat(-0.04, 0.0, -0.05)

    ## @var right_screen
    # Scenegraph node representing the user's right screen.
    self.right_screen = avango.gua.nodes.ScreenNode(Name = "screenR")
    self.right_screen.Width.value = self.screen_size.x / 2
    self.right_screen.Height.value = self.screen_size.y
    self.right_screen.Transform.value = avango.gua.make_trans_mat(0.04, 0.0, -0.05)

    ## @var left_eye
    # Scenegraph node representing the user's left eye.
    self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")

    ## @var right_eye
    # Scenegraph node representing the user's right eye.
    self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
    self.set_eye_distance(0.064)

    # viewing setup
    self.append_to_platform(self.VIEWING_MANAGER.SCENEGRAPH, self.head_transform)
    self.head_transform.Children.value.append(self.left_screen)
    self.head_transform.Children.value.append(self.right_screen)
    self.head_transform.Children.value.append(self.left_eye)
    self.head_transform.Children.value.append(self.right_eye)

    # Combine tracking and Oculus Input
    ## @var tracking_rotation_combiner
    # Instance of TrackingCombiner to determine the user's position on the platform.
    self.tracking_combiner = TrackingCombiner()
    self.tracking_combiner.my_constructor(HEADTRACKING_TARGET_NAME, NO_TRACKING_MAT)
    self.head_transform.Transform.connect_from(self.tracking_combiner.sf_combined_mat)

    # create avatar representation
    self.create_avatar_representation(self.VIEWING_MANAGER.SCENEGRAPH, self.tracking_combiner.get_sf_avatar_body_matrix())

    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()


## Helper class to combine the rotation input from an Oculus Rift with the
# translation input of a tracking system.
class TrackingCombiner(avango.script.Script):

  # output field
  ## @var sf_combined_mat
  # Combination of rotation and translation input.
  sf_combined_mat = avango.gua.SFMatrix4()
  sf_combined_mat.value = avango.gua.make_identity_mat()

  ## @var ovr_users_registered
  # Static count of OVR users in order to match them to the input sensors.
  ovr_users_registered = 0
  
  ## Default constructor.
  def __init__(self):
    self.super(TrackingCombiner).__init__()

  ## Custom constructor.
  # @param HEADTRACKING_TARGET_NAME Name of the Oculus Rift's tracking target to be used as translation input.
  # @param NO_TRACKING_MAT Matrix to be used if no tracking target name was specified.
  def my_constructor(self, HEADTRACKING_TARGET_NAME, NO_TRACKING_MAT):
    
    ## @var oculus_sensor
    # DeviceSensor communicating with the Oculus Rifts via daemon.
    self.oculus_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.oculus_sensor.Station.value = 'oculus-' + str(TrackingCombiner.ovr_users_registered)
    TrackingCombiner.ovr_users_registered += 1
    
    ## @var headtracking_reader
    # Instance of a child class of TrackingReader to supply translation input.
    if HEADTRACKING_TARGET_NAME == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(NO_TRACKING_MAT)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)

    self.always_evaluate(True)

  ## Returns the avatar body matrix of the headtracking reader.
  def get_sf_avatar_body_matrix(self):
    return self.headtracking_reader.sf_avatar_body_mat
 
  ## Evaluated every frame.
  def evaluate(self):
    self.sf_combined_mat.value = avango.gua.make_trans_mat(self.headtracking_reader.sf_abs_vec.value) * self.oculus_sensor.Matrix.value