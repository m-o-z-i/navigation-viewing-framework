#!/usr/bin/python

## @file
# Contains class ClientPowerWallUser.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
import ClientPipelineValues
from View import *

## Internal representation of a standard view on client side.
#
# Creates viewing setup and initializes a tracking sensor in order to avoid latency 
# due to distribution in the network. Refers to a StandardUser on server side.

class StandardView(View):

  ## Default constructor.
  def __init__(self):
    self.super(View).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param USER_ATTRIBUTES List created by file parser containing all the important user attributes.
  #
  #
  #
  def my_constructor(self, SCENEGRAPH, VIEWER, USER_ATTRIBUTES, PLATFORM_ID, DISPLAY_INSTANCE, SCREEN_NUM, STEREO):

    # [type, headtrackingstation, startplatform, user_id, transmitteroffset, notrackingmat]

    # get user, platform id and display string
    user_id = USER_ATTRIBUTES[3]
    platform_id = USER_ATTRIBUTES[2]

    self.construct_view(SCENEGRAPH, platform_id, user_id, False)

    display_values = DISPLAY_INSTANCE.register_user()

    # no more users allowed at this screen
    if not display_values:
      print 'Error: no more users allowed at display "' + DISPLAY_INSTANCE.name + '"!'
      return

    if STEREO:
      left_eye_resolution  = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1])
      right_eye_resolution = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1])

      # create camera
      camera = avango.gua.nodes.Camera()
      camera.SceneGraph.value = SCENEGRAPH.Name.value
      camera.LeftScreen.value = "/net/platform_" + str(platform_id) + "/screen_" + str(SCREEN_NUM)
      camera.RightScreen.value = camera.LeftScreen.value
      camera.LeftEye.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/eyeL"
      camera.RightEye.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/eyeR"

      render_mask = "!do_not_display_group && !avatar_group_" + str(platform_id) + " && !couple_group_" + str(platform_id)

      for i in range(0, 10):
        if i != platform_id:
          render_mask = render_mask + " && !platform_group_" + str(i)

      camera.RenderMask.value = render_mask

      # create window
      window_size = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0] * 2, DISPLAY_INSTANCE.resolution[1]) 
      window = avango.gua.nodes.Window()
      window.Title.value = "User_" + str(user_id)
      window.Size.value = window_size
      window.LeftResolution.value = avango.gua.Vec2ui(window_size.x / 2, window_size.y)
      window.LeftPosition.value = avango.gua.Vec2ui(0, 0)
      window.RightResolution.value = avango.gua.Vec2ui(window_size.x / 2, window_size.y)
      window.RightPosition.value = avango.gua.Vec2ui(int(window_size.x * 0.5), 0)
      window.StereoMode.value            = avango.gua.StereoMode.SIDE_BY_SIDE

      # create pipeline
      pipeline = avango.gua.nodes.Pipeline(Window = window, 
                                           LeftResolution = window_size,
                                           RightResolution = window_size)

      pipeline.Camera.value =  camera
      pipeline.EnableStereo.value = True
      pipeline.Enabled.value = True

      ClientPipelineValues.set_pipeline_values(pipeline)

      # add tracking reader to avoid latency
      self.add_tracking_reader(USER_ATTRIBUTES[1], USER_ATTRIBUTES[4], USER_ATTRIBUTES[5])

      VIEWER.Pipelines.value.append(pipeline)
    
    else:
      eye_resolution  = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1])

      camera = avango.gua.nodes.Camera()
      camera.SceneGraph.value = SCENEGRAPH.Name.value
      camera.LeftScreen.value = "/net/platform_" + str(platform_id) + "/screen_" + str(SCREEN_NUM)
      camera.RightScreen.value = camera.LeftScreen.value
      camera.LeftEye.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/eye"
      camera.RightEye.value = camera.LeftEye.value

      render_mask = "!do_not_display_group && !avatar_group_" + str(platform_id) + " && !couple_group_" + str(platform_id)

      for i in range(0, 10):
        if i != platform_id:
          render_mask = render_mask + " && !platform_group_" + str(i)

      camera.RenderMask.value = render_mask

      window_size = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1]) 
      window = avango.gua.nodes.Window()
      window.Title.value = "User_" + str(user_id)
      window.Size.value = window_size
      window.LeftResolution.value = window_size

      # create pipeline
      pipeline = avango.gua.nodes.Pipeline()
      pipeline.Window.value = window
      pipeline.LeftResolution.value = window.LeftResolution.value
      pipeline.EnableStereo.value = False
      pipeline.Camera.value = camera
      pipeline.Enabled.value = True

      ClientPipelineValues.set_pipeline_values(pipeline)

      # add tracking reader to avoid latency
      self.add_tracking_reader(USER_ATTRIBUTES[1], USER_ATTRIBUTES[4], USER_ATTRIBUTES[5])

      VIEWER.Pipelines.value.append(pipeline)

    # set display string and warpmatrices as given by the display
    if len(display_values) > 1:
      self.set_warpmatrices(window, display_values[1])
      window.Display.value = display_values[0]

  def set_warpmatrices(self, WINDOW, WARPMATRICES):
    if len(WARPMATRICES) == 6:
      WINDOW.WarpMatrixRedRight.value    = WARPMATRICES[0]
      WINDOW.WarpMatrixGreenRight.value  = WARPMATRICES[1]
      WINDOW.WarpMatrixBlueRight.value   = WARPMATRICES[2]
      
      WINDOW.WarpMatrixRedLeft.value     = WARPMATRICES[3]
      WINDOW.WarpMatrixGreenLeft.value   = WARPMATRICES[4]
      WINDOW.WarpMatrixBlueLeft.value    = WARPMATRICES[5]
