#!/usr/bin/python

## @file
# Contains class OVRUser and TrackingRotationCombiner.

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
  # @param OVR_USER_ID Identification number of the OVRUser to be created, starting from 0.
  # @param PLATFORM_ID Platform to append the constructed OVRUser to.
  # @param NO_TRACKING_MAT Matrix to be applied if no headtracking of the Oculus Rift is available.
  # @param AVATAR_MATERIAL Material to be used for the OVR user's avatar
  def __init__(self, VIEWING_MANAGER, HEADTRACKING_TARGET_NAME, OVR_USER_ID, PLATFORM_ID, NO_TRACKING_MAT, AVATAR_MATERIAL):
    User.__init__(self, "ovr", AVATAR_MATERIAL)

    ## @var id
    # Identification number of the OVRUser, starting from 0.
    self.id = OVR_USER_ID

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
    self.append_to_platform(VIEWING_MANAGER.SCENEGRAPH, self.head_transform)
    self.head_transform.Children.value.append(self.left_screen)
    self.head_transform.Children.value.append(self.right_screen)
    self.head_transform.Children.value.append(self.left_eye)
    self.head_transform.Children.value.append(self.right_eye)

    # create the camera
    ## @var camera
    # Camera to represent the user's viewport to be rendered.
    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = VIEWING_MANAGER.SCENEGRAPH.Name.value
    self.camera.LeftScreen.value = self.left_screen.Path.value
    self.camera.RightScreen.value = self.right_screen.Path.value
    self.camera.LeftEye.value = self.left_eye.Path.value
    self.camera.RightEye.value = self.right_eye.Path.value

    _render_mask = "!do_not_display_group && !ovr_avatar_group_" + str(self.platform_id) + " && !couple_group_" + str(self.platform_id)

    for i in range(0, 10):
      if i != self.platform_id:
        _render_mask = _render_mask + " && !platform_group_" + str(i)

    self.camera.RenderMask.value = _render_mask

    # create oculus node
    ## @var oculus_window
    # Window to display the rendered image to.
    self.oculus_window = avango.oculus.nodes.OculusWindow()
    self.oculus_window.Title.value = "OVRUser_" + str(self.id)
    self.oculus_window.Size.value = self.window_size
    self.oculus_window.LeftResolution.value = avango.gua.Vec2ui(self.window_size.x / 2, self.window_size.y)
    self.oculus_window.RightResolution.value = avango.gua.Vec2ui(self.window_size.x / 2, self.window_size.y)

    # Combine tracking and Oculus Input
    ## @var tracking_rotation_combiner
    # Instance of TrackingRotationCombiner to determine the user's position on the platform.
    self.tracking_rotation_combiner = TrackingRotationCombiner()
    self.tracking_rotation_combiner.my_constructor(self.id, HEADTRACKING_TARGET_NAME, NO_TRACKING_MAT)
    self.head_transform.Transform.connect_from(self.tracking_rotation_combiner.sf_combined_mat)

    # create pipeline
    ## @var pipeline
    # Pipeline for rendering purposes.
    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.BackgroundTexture.value = VIEWING_MANAGER.background_texture
    self.pipeline.Window.value = self.oculus_window
    self.pipeline.LeftResolution.value = self.oculus_window.LeftResolution.value
    self.pipeline.RightResolution.value = self.oculus_window.RightResolution.value
    self.pipeline.EnableStereo.value = True
    self.pipeline.Camera.value = self.camera
    self.set_pipeline_values()

    # create avatar representation
    self.create_avatar_representation(VIEWING_MANAGER.SCENEGRAPH, self.tracking_rotation_combiner.get_sf_avatar_body_matrix())

    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()

    # add newly created pipeline to the list of all pipelines in the viewer
    VIEWING_MANAGER.viewer.Pipelines.value.append(self.pipeline)

## Helper class to combine the rotation input from an Oculus Rift with the
# translation input of a tracking system.

class TrackingRotationCombiner(avango.script.Script):

  # output field
  ## @var sf_combined_mat
  # Combination of rotation and translation input.
  sf_combined_mat = avango.gua.SFMatrix4()
  sf_combined_mat.value = avango.gua.make_identity_mat()
  
  ## Default constructor.
  def __init__(self):
    self.super(TrackingRotationCombiner).__init__()

  ## Custom constructor.
  # @param OVR_USER_ID Identification number of the OVRUser.
  # @param HEADTRACKING_TARGET_NAME Name of the Oculus Rift's tracking target to be used as translation input.
  # @param NO_TRACKING_MAT Matrix to be used if no tracking target name was specified.
  def my_constructor(self, OVR_USER_ID, HEADTRACKING_TARGET_NAME, NO_TRACKING_MAT):
    
    ## @var oculus_sensor
    # DeviceSensor communicating with the Oculus Rifts via daemon.
    self.oculus_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.oculus_sensor.Station.value = 'oculus-' + str(OVR_USER_ID)
    
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