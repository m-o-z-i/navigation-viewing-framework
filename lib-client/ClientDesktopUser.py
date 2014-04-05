#!/usr/bin/python

## @file
# Contains class ClientDesktopUser. 

# import guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
import ClientPipelineValues
from ClientUser import *

## Internal representation of a desktop user on client side.
#
# Creates viewing setup and initializes a default tracking sensor in order to avoid latency 
# due to distribution in the network.

class ClientDesktopUser(ClientUser):

  ## Default constructor.
  def __init__(self):
    self.super(ClientDesktopUser).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param USER_ATTRIBUTES List created by file parser containing all the important user attributes.
  def my_constructor(self, SCENEGRAPH, VIEWER, USER_ATTRIBUTES):

    # get user, platform id and display string
    user_id = USER_ATTRIBUTES[7]
    platform_id = USER_ATTRIBUTES[2]
    display = USER_ATTRIBUTES[8]

    self.construct_user(SCENEGRAPH, platform_id, user_id, "desktop")

    # create camera
    camera = avango.gua.nodes.Camera()
    camera.SceneGraph.value = SCENEGRAPH.Name.value
    camera.LeftScreen.value = "/net/platform_" + str(platform_id) + "/screen_" + str(user_id)
    camera.RightScreen.value = camera.LeftScreen.value
    camera.LeftEye.value = "/net/platform_" + str(platform_id) + "/head_" + str(user_id) + "/eye"
    camera.RightEye.value = camera.LeftEye.value

    render_mask = "!do_not_display_group && !avatar_group_" + str(platform_id) + " && !couple_group_" + str(platform_id)

    for i in range(0, 10):
        if i != platform_id:
            render_mask = render_mask + " && !platform_group_" + str(i)

    camera.RenderMask.value = render_mask

    # create window
    window_size = avango.gua.Vec2ui(USER_ATTRIBUTES[3], USER_ATTRIBUTES[4])
    window = avango.gua.nodes.Window()
    window.Title.value = "User_" + str(user_id)
    window.Size.value = window_size
    window.LeftResolution.value = window_size
    window.Display.value = display

    # create pipeline
    pipeline = avango.gua.nodes.Pipeline()
    pipeline.Window.value = window
    pipeline.LeftResolution.value = window.LeftResolution.value
    pipeline.EnableStereo.value = False
    pipeline.Camera.value = camera
    pipeline.Enabled.value = True

    ClientPipelineValues.set_pipeline_values(pipeline)

    # add tracking reader to avoid latency
    self.add_tracking_reader(USER_ATTRIBUTES[1], USER_ATTRIBUTES[9], USER_ATTRIBUTES[10])

    VIEWER.Pipelines.value.append(pipeline)