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
    self.eye.Transform.value = avango.gua.make_trans_mat(0, 0, 0)

    # viewing setup
    self.append_to_platform(VIEWING_MANAGER.SCENEGRAPH, self.head_transform)
    self.append_to_platform(VIEWING_MANAGER.SCENEGRAPH, self.screen)
    self.head_transform.Children.value.append(self.eye)

    # create the camera
    ## @var camera
    # Camera to represent the user's viewport to be rendered.
    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = VIEWING_MANAGER.SCENEGRAPH.Name.value
    self.camera.LeftScreen.value = self.screen.Path.value
    self.camera.RightScreen.value = self.screen.Path.value
    self.camera.LeftEye.value = self.eye.Path.value
    self.camera.RightEye.value = self.eye.Path.value

    _render_mask = "!do_not_display_group && !desktop_avatar_group_" + str(self.platform_id) + " && !couple_group_" + str(self.platform_id)

    for i in range(0, 10):
        if i != self.platform_id:
            _render_mask = _render_mask + " && !platform_group_" + str(i)

    self.camera.RenderMask.value = _render_mask

    # create window node
    ## @var window
    # Window to display the rendered image to.
    self.window = avango.gua.nodes.Window()
    self.window.Title.value = "DesktopUser_" + str(self.id)
    self.window.Size.value = self.window_size
    self.window.LeftResolution.value = avango.gua.Vec2ui(self.window_size.x, self.window_size.y)

    # create default headtracking value supplier
    ## @var headtracking_reader
    # TrackingReader instance to supply constant basic tracking values.
    self.headtracking_reader = TrackingDefaultReader()
    self.headtracking_reader.set_no_tracking_matrix(avango.gua.make_trans_mat(0, 1.2, 1.5))
    self.head_transform.Transform.connect_from(self.headtracking_reader.sf_abs_mat)

    # create pipeline
    ## @var pipeline
    # Pipeline for rendering purposes.
    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.BackgroundTexture.value = VIEWING_MANAGER.background_texture
    self.pipeline.Window.value = self.window
    self.pipeline.LeftResolution.value = self.window.LeftResolution.value
    self.pipeline.EnableStereo.value = False
    self.pipeline.Camera.value = self.camera
    self.set_pipeline_values()

    # create avatar representation
    self.create_avatar_representation(VIEWING_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat)

    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()

    # add newly created pipeline to the list of all pipelines in the viewer
    VIEWING_MANAGER.viewer.Pipelines.value.append(self.pipeline)