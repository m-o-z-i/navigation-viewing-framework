#!/usr/bin/python

## @file
# Contains class StandardView.

# import avango-guacamole libraries
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
# due to distribution in the network. Refers to a Slot on server side.

class StandardView(View):

  ## Default constructor.
  def __init__(self):
    self.super(View).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param PLATFORM_ID The platform id on which the corresponding user is standing on.
  # @param SLOT_ID The identification number of the slot to display.
  # @param DISPLAY_INSTANCE An instance of Display to represent the values.
  # @param SCREEN_NUM The number of the screen node on the platform.
  # @param STEREO Boolean indicating if the view to be constructed is stereo or mono.
  def my_constructor(self, SCENEGRAPH, VIEWER, PLATFORM_ID, SLOT_ID, DISPLAY_INSTANCE, SCREEN_NUM, STEREO):

    # call base class constructor
    self.construct_view(SCENEGRAPH, PLATFORM_ID, SLOT_ID, SCREEN_NUM, False)

    # retrieve the needed values from display
    display_values = DISPLAY_INSTANCE.register_view()

    # check if no more users allowed at this screen
    if not display_values:
      # TODO better handling of this case?
      print 'Error: no more users allowed at display "' + DISPLAY_INSTANCE.name + '"!'
      return

    if STEREO:

      '''
        Stereo user case
      '''

      left_eye_resolution  = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1])
      right_eye_resolution = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1])

      # create camera
      camera = avango.gua.nodes.Camera()
      camera.SceneGraph.value = SCENEGRAPH.Name.value
      camera.LeftScreen.value = "/net/platform_" + str(self.platform_id) + "/screen_" + str(self.screen_num)
      camera.RightScreen.value = camera.LeftScreen.value
      camera.LeftEye.value = "/net/platform_" + str(self.platform_id) + "/s" + str(self.screen_num) + "_slot" + str(self.slot_id) + "/eyeL"
      camera.RightEye.value = "/net/platform_" + str(self.platform_id) + "/s" + str(self.screen_num) + "_slot" + str(self.slot_id) + "/eyeR"

      # set render mask for camera
      render_mask = "!do_not_display_group && !avatar_group_" + str(self.platform_id) + " && !couple_group_" + str(self.platform_id)

      for i in range(0, 10):
        if i != self.platform_id:
          render_mask = render_mask + " && !platform_group_" + str(i)

      camera.RenderMask.value = render_mask

      # create window
      window_size = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0] * 2, DISPLAY_INSTANCE.resolution[1]) 
      window = avango.gua.nodes.Window()
      window.Title.value = "Display: " + str(DISPLAY_INSTANCE.name) + "; Slot: " + str(self.slot_id)
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

    else:

      '''
        Mono user case
      '''

      eye_resolution  = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1])

      camera = avango.gua.nodes.Camera()
      camera.SceneGraph.value = SCENEGRAPH.Name.value
      camera.LeftScreen.value = "/net/platform_" + str(self.platform_id) + "/screen_" + str(self.screen_num)
      camera.RightScreen.value = camera.LeftScreen.value
      camera.LeftEye.value = "/net/platform_" + str(self.platform_id) + "/s" + str(self.screen_num) + "_slot" + str(self.slot_id) + "/eye"
      camera.RightEye.value = camera.LeftEye.value

      # set render mask for camera
      render_mask = "!do_not_display_group && !avatar_group_" + str(self.platform_id) + " && !couple_group_" + str(self.platform_id)

      for i in range(0, 10):
        if i != self.platform_id:
          render_mask = render_mask + " && !platform_group_" + str(i)

      camera.RenderMask.value = render_mask

      window_size = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1]) 
      window = avango.gua.nodes.Window()
      window.Title.value = "Display: " + str(DISPLAY_INSTANCE.name) + "; Slot: " + str(self.slot_id)
      window.Size.value = window_size
      window.LeftResolution.value = window_size

      # create pipeline
      pipeline = avango.gua.nodes.Pipeline(Window = window,
                                           LeftResolution = window.LeftResolution.value)
      pipeline.Camera.value = camera
      pipeline.EnableStereo.value = False
      pipeline.Enabled.value = True


    '''
      General slot settings
    '''

    # set nice pipeline values
    ClientPipelineValues.set_pipeline_values(pipeline)

    # add tracking reader to avoid latency
    #self.add_tracking_reader(USER_ATTRIBUTES[1], USER_ATTRIBUTES[4], USER_ATTRIBUTES[5])

    # set display string and warpmatrices as given by the display
    if len(display_values) > 1:
      self.set_warpmatrices(window, display_values[1])
    
    window.Display.value = display_values[0]

    # append pipeline to the viewer
    VIEWER.Pipelines.value.append(pipeline)


  ## Sets the warp matrices if there is a correct amount of them.
  # @param WINDOW The window instance to apply the warp matrices to.
  # @param WARPMATRICES A list of warp matrices to be applied if there are enough of them.
  def set_warpmatrices(self, WINDOW, WARPMATRICES):
    
    if len(WARPMATRICES) == 6:
      WINDOW.WarpMatrixRedRight.value    = WARPMATRICES[0]
      WINDOW.WarpMatrixGreenRight.value  = WARPMATRICES[1]
      WINDOW.WarpMatrixBlueRight.value   = WARPMATRICES[2]
      
      WINDOW.WarpMatrixRedLeft.value     = WARPMATRICES[3]
      WINDOW.WarpMatrixGreenLeft.value   = WARPMATRICES[4]
      WINDOW.WarpMatrixBlueLeft.value    = WARPMATRICES[5]