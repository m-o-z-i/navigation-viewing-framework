#!/usr/bin/python

## @file
# Contains class ClientOVRUser.

# import guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
import ClientPipelineValues
from ClientUser import *

## Internal representation of an Oculus Rift user on client side.
#
# Creates viewing setup and initializes a tracking sensor in order to avoid latency 
# due to distribution in the network.

class ClientOVRUser(ClientUser):

  ## Default constructor.
  def __init__(self):
    self.super(ClientOVRUser).__init__()

  ## Custom constructor
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param USER_ATTRIBUTES List created by file parser containing all the important user attributes.
  def my_constructor(self, SCENEGRAPH, VIEWER, USER_ATTRIBUTES):

    # get user, platform id and display string
    user_id = USER_ATTRIBUTES[7]
    platform_id = USER_ATTRIBUTES[2]
    display = USER_ATTRIBUTES[8]

    self.construct_user(SCENEGRAPH, platform_id, user_id, True)

    # create camera
    camera = avango.gua.nodes.Camera()
    camera.SceneGraph.value = SCENEGRAPH.Name.value
    camera.LeftScreen.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/screenL"
    camera.RightScreen.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/screenR"
    camera.LeftEye.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/eyeL"
    camera.RightEye.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/eyeR"

    render_mask = "!do_not_display_group && !avatar_group_" + str(platform_id) + " && !couple_group_" + str(platform_id)

    for i in range(0, 10):
        if i != platform_id:
            render_mask = render_mask + " && !platform_group_" + str(i)

    camera.RenderMask.value = render_mask

    # create window
    window_size = avango.gua.Vec2ui(1280, 800)
    window = avango.oculus.nodes.OculusWindow()
    window.Title.value = "User_" + str(user_id)
    window.Size.value = window_size
    window.LeftResolution.value = avango.gua.Vec2ui(window_size.x / 2, window_size.y)
    window.RightResolution.value = avango.gua.Vec2ui(window_size.x / 2, window_size.y)
    window.Display.value = display

    # create pipeline
    pipeline = avango.gua.nodes.Pipeline()
    pipeline.Window.value = window
    pipeline.LeftResolution.value = window.LeftResolution.value
    pipeline.RightResolution.value = window.RightResolution.value
    pipeline.EnableStereo.value = True
    pipeline.Camera.value = camera
    pipeline.Enabled.value = True

    ClientPipelineValues.set_pipeline_values(pipeline)

    # add tracking reader to avoid latency
    self.add_tracking_reader(USER_ATTRIBUTES[1], USER_ATTRIBUTES[9], USER_ATTRIBUTES[10])

    VIEWER.Pipelines.value.append(pipeline)