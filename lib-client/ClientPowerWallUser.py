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
from ClientUser import *

## Internal representation of a powerwall user on client side.
#
# Creates viewing setup and initializes a tracking sensor in order to avoid latency 
# due to distribution in the network.

class ClientPowerWallUser(ClientUser):

  ## Default constructor.
  def __init__(self):
    self.super(ClientPowerWallUser).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param USER_ATTRIBUTES List created by file parser containing all the important user attributes.
  # @param IDENTIFIER Identifies which powerwall is used ('small' or 'large').
  def my_constructor(self, SCENEGRAPH, VIEWER, USER_ATTRIBUTES, IDENTIFIER):

    # get user, platform id and display string
    user_id = USER_ATTRIBUTES[7]
    platform_id = USER_ATTRIBUTES[2]
    display = USER_ATTRIBUTES[8]

    self.construct_user(SCENEGRAPH, platform_id, user_id, "wall")

    # powerwall settings
    left_eye_resolution  = avango.gua.Vec2ui(1920, 1200)
    right_eye_resolution = avango.gua.Vec2ui(1920, 1200)
    if IDENTIFIER == "large":
      screen_transform    = avango.gua.make_trans_mat(0.0, 1.57, 0.0)
    else:
      screen_transform     = avango.gua.make_trans_mat(0.0, 1.42, 0.0)
    if IDENTIFIER == "large":
      warp_matrices_path = "/opt/dlp-warpmatrices/"
    else:
      warp_matrices_path   = "/opt/lcd-warpmatrices/"

    # create camera
    camera = avango.gua.nodes.Camera()
    camera.SceneGraph.value = SCENEGRAPH.Name.value
    camera.LeftScreen.value = "/net/platform_" + str(platform_id) + "/wall_screen_" + str(user_id)
    camera.RightScreen.value = camera.LeftScreen.value
    camera.LeftEye.value = "/net/platform_" + str(platform_id) + "/wall_head_" + str(user_id) + "/eyeL"
    camera.RightEye.value = "/net/platform_" + str(platform_id) + "/wall_head_" + str(user_id) + "/eyeR"

    render_mask = "!do_not_display_group && !wall_avatar_group_" + str(platform_id) + " && !couple_group_" + str(platform_id)

    for i in range(0, 10):
      if i != platform_id:
        render_mask = render_mask + " && !platform_group_" + str(i)

    camera.RenderMask.value = render_mask

    # create window
    window_size          = avango.gua.Vec2ui(1920*2, 1200) 
    window = avango.gua.nodes.Window()
    window.Title.value = "PowerWallUser_" + str(user_id)
    window.Size.value = window_size
    window.LeftResolution.value = avango.gua.Vec2ui(window_size.x / 2, window_size.y)
    window.LeftPosition.value = avango.gua.Vec2ui(0, 0)
    window.RightResolution.value = avango.gua.Vec2ui(window_size.x / 2, window_size.y)
    window.RightPosition.value = avango.gua.Vec2ui(int(window_size.x * 0.5), 0)

    window.StereoMode.value            = avango.gua.StereoMode.SIDE_BY_SIDE
    if IDENTIFIER == "large":
      window.WarpMatrixRedRight.value    = "{0}dlp_6_warp_P4.warp".format(warp_matrices_path)
      window.WarpMatrixGreenRight.value  = "{0}dlp_6_warp_P5.warp".format(warp_matrices_path)
      window.WarpMatrixBlueRight.value   = "{0}dlp_6_warp_P6.warp".format(warp_matrices_path)

      window.WarpMatrixRedLeft.value     = "{0}dlp_6_warp_P1.warp".format(warp_matrices_path)
      window.WarpMatrixGreenLeft.value   = "{0}dlp_6_warp_P2.warp".format(warp_matrices_path)
      window.WarpMatrixBlueLeft.value    = "{0}dlp_6_warp_P3.warp".format(warp_matrices_path)
    else:
      window.WarpMatrixRedRight.value    = "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, (user_id)*2 + 2)
      window.WarpMatrixGreenRight.value  = "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, (user_id)*2 + 2)
      window.WarpMatrixBlueRight.value   = "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, (user_id)*2 + 2)
      
      window.WarpMatrixRedLeft.value     = "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, (user_id)*2 + 1)
      window.WarpMatrixGreenLeft.value   = "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, (user_id)*2 + 1)
      window.WarpMatrixBlueLeft.value    = "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, (user_id)*2 + 1)

    window.Display.value = display

    # create pipeline
    pipeline = avango.gua.nodes.Pipeline(Window = window, 
                                         LeftResolution = window_size,
                                         RightResolution = window_size)
    pipeline.Camera.value =  camera
    pipeline.EnableStereo.value = True
    pipeline.Enabled.value = True

    ClientPipelineValues.set_pipeline_values(pipeline)

    # add tracking reader to avoid latency
    self.add_tracking_reader(USER_ATTRIBUTES[1], USER_ATTRIBUTES[9], USER_ATTRIBUTES[10])

    VIEWER.Pipelines.value.append(pipeline)