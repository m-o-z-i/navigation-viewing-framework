#!/usr/bin/python

## @file
# Contains class View.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
import avango.oculus
from avango.script import field_has_changed

# import framework libraries
from ClientTrackingReader import *
from ClientPortal import *
from ConsoleIO import *

# import python libraries
import time


## Internal representation of a standard view on client side.
# Creates the viewing setup needed for one individual workspace-displaygroup-screen-user view.
class View(avango.script.Script):

  ## @var sf_pipeline_string
  # String field containing the concatenated pipeline values.
  sf_pipeline_string = avango.SFString()

  ## Default constructor.
  def __init__(self):
    self.super(View).__init__()

    ## @var portal_pre_views
    # A list of all PortalPreView instances for this view.
    self.portal_pre_views = []

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param DISPLAY_INSTANCE An instance of Display to represent the values.
  # @param WORKSPACE_ID ID of the workspace to deal with.
  # @param DISPLAY_GROUP_ID ID of the display group to deal with.
  # @param SCREEN_ID ID of the screen to deal with.
  # @param USER_ID ID of the user to deal with.
  def my_constructor(self, SCENEGRAPH, VIEWER, DISPLAY_INSTANCE, WORKSPACE_ID, DISPLAY_GROUP_ID, SCREEN_ID, USER_ID):

    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var is_stereo
    # Boolean indicating if the view to be constructed is stereo or mono.
    self.is_stereo = DISPLAY_INSTANCE.stereo

    ## @var workspace_id
    # ID of the workspace to deal with.
    self.workspace_id = WORKSPACE_ID

    ## @var display_group_id
    # ID of the display group to deal with.
    self.display_group_id = DISPLAY_GROUP_ID

    ## @var screen_id
    # ID of the screen to deal with.
    self.screen_id = SCREEN_ID

    ## @var user_id
    # ID of the user to deal with.
    self.user_id = USER_ID

    # retrieve the needed values from display
    ## @var display_values
    # Values that are retrieved from the display. Vary for each view on this display.
    self.display_values = DISPLAY_INSTANCE.register_view()

    ## @var display_render_mask
    # Additional render mask contraints given by the display.
    self.display_render_mask = DISPLAY_INSTANCE.render_mask

    # check if no more users allowed at this screen
    if not self.display_values:
      # TODO better handling of this case?
      print_error('Error: no more users allowed at display "' + DISPLAY_INSTANCE.name + '"!', False)
      return

    ## @var window_size
    # Size of the window in which this View will be rendered.
    self.window_size = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1]) 

    # create camera
    ## @var camera
    # The camera from which this View will be rendered.
    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = SCENEGRAPH.Name.value
    self.camera.Mode.value = DISPLAY_INSTANCE.cameramode

    # set render mask for camera
    _render_mask = "(main_scene | w" + str(WORKSPACE_ID) + "_dg" + str(DISPLAY_GROUP_ID) + "_u" + str(USER_ID) + ") && !do_not_display_group && !portal_invisible_group"
    self.camera.RenderMask.value = _render_mask
    #print repr(self.camera.RenderMask.value)

    # create pipeline
    ## @var pipeline
    # The pipeline used to render this View.
    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.Enabled.value = True

    '''
      Standard View
    '''

    self.camera.LeftScreen.value = "/net/w" + str(self.workspace_id) + "_dg" + str(self.display_group_id) + "_u" + str(self.user_id) + "/screen_" + str(self.screen_id)
    self.camera.RightScreen.value = "/net/w" + str(self.workspace_id) + "_dg" + str(self.display_group_id) + "_u" + str(self.user_id) + "/screen_" + str(self.screen_id)
    self.camera.LeftEye.value = "/net/w" + str(self.workspace_id) + "_dg" + str(self.display_group_id) + "_u" + str(self.user_id) + "/head/eyeL"
    self.camera.RightEye.value = "/net/w" + str(self.workspace_id) + "_dg" + str(self.display_group_id) + "_u" + str(self.user_id) + "/head/eyeR"

    # create window
    ## @var window
    # The window in which this View will be rendered to.
    self.window = avango.gua.nodes.Window()
    self.window.Display.value = self.display_values[0] # GPU-ID
    self.window.Title.value = "Display: " + str(DISPLAY_INSTANCE.name) + "; User: " + str(self.user_id)
    self.window.LeftResolution.value = self.window_size
    self.window.RightResolution.value = self.window_size

    if DISPLAY_INSTANCE.stereomode == "SIDE_BY_SIDE":
      self.window.Size.value = avango.gua.Vec2ui(self.window_size.x * 2, self.window_size.y)
      self.window.LeftPosition.value = avango.gua.Vec2ui(0, 0)
      self.window.RightPosition.value = avango.gua.Vec2ui(self.window_size.x, 0)
      self.window.StereoMode.value = avango.gua.StereoMode.SIDE_BY_SIDE
    
    elif DISPLAY_INSTANCE.stereomode == "ANAGLYPH_RED_CYAN" or DISPLAY_INSTANCE.stereomode == "CHECKERBOARD":
      self.window.Size.value = self.window_size
      self.window.LeftPosition.value = avango.gua.Vec2ui(0, 0)
      self.window.RightPosition.value = avango.gua.Vec2ui(0, 0)
      
      if DISPLAY_INSTANCE.stereomode == "ANAGLYPH_RED_CYAN":
        self.window.StereoMode.value = avango.gua.StereoMode.ANAGLYPH_RED_CYAN

      elif DISPLAY_INSTANCE.stereomode == "CHECKERBOARD":
        self.window.StereoMode.value = avango.gua.StereoMode.CHECKERBOARD

    self.pipeline.LeftResolution.value = self.window.LeftResolution.value
    self.pipeline.RightResolution.value = self.window.RightResolution.value

    if self.is_stereo:
      self.pipeline.EnableStereo.value = True
    else:
      self.pipeline.EnableStereo.value = False

    self.pipeline.Window.value = self.window
    self.pipeline.Camera.value = self.camera
    self.pipeline.EnableFPSDisplay.value = True

    '''
      General user settings
    '''

    # set display string and warpmatrices as given by the display
    if len(self.display_values) > 1:
      self.set_warpmatrices(self.window, self.display_values[1])

    # append pipeline to the viewer
    VIEWER.Pipelines.value.append(self.pipeline)

    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method.
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)
  

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

  ## Creates a PortalPreView instance for the portal copied at LOCAL_PORTAL_NODE.
  # @param SERVER_PORTAL_NODE Server portal grouping node.
  def create_portal_preview(self, SERVER_PORTAL_NODE):
    _pre_view = PortalPreView()
    _pre_view.my_constructor(SERVER_PORTAL_NODE, self)
    self.portal_pre_views.append(_pre_view)

  ## Removes the PortalPreView instance of LOCAL_PORTAL_NODE.
  # @param LOCAL_PORTAL_NODE The client portal node to remove the PreView for.
  def remove_portal_preview(self, LOCAL_PORTAL_NODE):

    _pre_views_to_remove = []

    for _pre_view in self.portal_pre_views:
      if _pre_view.compare_portal_node(LOCAL_PORTAL_NODE) == True:
        _pre_views_to_remove.append(_pre_view)
        
    for _pre_view in _pre_views_to_remove:
      print("Remove a pre view")
      _pre_view.deactivate()
      self.portal_pre_views.remove(_pre_view)
      del _pre_view
      print("New list of pre views", self.portal_pre_views)

  ## Called whenever sf_pipeline_string changes.
  @field_has_changed(sf_pipeline_string)
  def sf_pipeline_string_changed(self):
      
    _splitted_string = self.sf_pipeline_string.value.split("#")

    print_message("w" + str(self.workspace_id) + "_dg" + str(self.display_group_id) + "_u" + str(self.user_id) + ": Set pipeline values to " + str(_splitted_string))

    # Note: Calling avango.gua.create_texture during runtime causes the application
    # to crash. All textures have to be preloaded, for example in ClientPipelineValues.py
    # avango.gua.create_texture(_splitted_string[0])
    
    if self.display_render_mask == "!main_scene":
      self.pipeline.BackgroundMode.value = avango.gua.BackgroundMode.COLOR
      self.pipeline.BackgroundColor.value = avango.gua.Color(0.2, 0.45, 0.6)
    else:
      self.pipeline.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
      self.pipeline.BackgroundTexture.value = _splitted_string[0]
      self.pipeline.FogTexture.value = _splitted_string[0]

    if _splitted_string[1] == "True":
      self.pipeline.EnableBloom.value = True
    else:
      self.pipeline.EnableBloom.value = False

    self.pipeline.BloomIntensity.value = float(_splitted_string[2])
    self.pipeline.BloomThreshold.value = float(_splitted_string[3])
    self.pipeline.BloomRadius.value = float(_splitted_string[4])

    if _splitted_string[5] == "True":
      self.pipeline.EnableSsao.value = True
    else:
      self.pipeline.EnableSsao.value = False

    self.pipeline.SsaoRadius.value = float(_splitted_string[6])
    self.pipeline.SsaoIntensity.value = float(_splitted_string[7])

    if _splitted_string[8] == "True":
      self.pipeline.EnableBackfaceCulling.value = True
    else:
      self.pipeline.EnableBackfaceCulling.value = False

    if _splitted_string[9] == "True":
      self.pipeline.EnableFrustumCulling.value = True
    else:
      self.pipeline.EnableFrustumCulling.value = False

    if _splitted_string[10] == "True":
      self.pipeline.EnableFXAA.value = True
    else:
      self.pipeline.EnableFXAA.value = False

    _ambient_color_values = _splitted_string[11].split(",")
    _ambient_color = avango.gua.Color(float(_ambient_color_values[0]), float(_ambient_color_values[1]), float(_ambient_color_values[2]))
    self.pipeline.AmbientColor.value = _ambient_color

    if _splitted_string[12] == "True":
      self.pipeline.EnableFog.value = True
    else:
      self.pipeline.EnableFog.value = False

    self.pipeline.FogStart.value = float(_splitted_string[13])
    self.pipeline.FogEnd.value = float(_splitted_string[14])
    self.pipeline.NearClip.value = float(_splitted_string[15])
    self.pipeline.FarClip.value = float(_splitted_string[16])
  
    #avango.gua.reload_materials()
  
  ## Evaluated every frame until connection is setup.
  def frame_callback(self):

    try:
      _pipeline_info_node = self.SCENEGRAPH["/net/pipeline_values"].Children.value[0]
    except:
      return

    # connect sf_pipeline_string with Name field of info node once
    if _pipeline_info_node != None and self.sf_pipeline_string.value == "":
      self.sf_pipeline_string.connect_from(_pipeline_info_node.Name)
      self.frame_trigger.Active.value = False
