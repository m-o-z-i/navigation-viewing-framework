#!/usr/bin/python

## @file
# Contains class View.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ClientTrackingReader import *
import ClientPipelineValues


## Internal representation of a standard view on client side.
#
# Creates viewing setup and initializes a tracking sensor in order to avoid latency 
# due to distribution in the network. Refers to a StandardUser on server side.
class View(avango.script.Script):

  ### Fields ###
  sf_head_mat = avango.gua.SFMatrix4()
  sf_head_mat.value = avango.gua.make_identity_mat()


  ## Default constructor.
  def __init__(self):
  	self.super(View).__init__()


  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param VIEWER Reference to the viewer to which the created pipeline will be appended to.
  # @param USER_ATTRIBUTES List created by file parser containing all the important user attributes.
  # @param PLATFORM_ID The platform id on which this user is standing on.
  # @param DISPLAY_INSTANCE An instance of Display to represent the values.
  # @param SCREEN_NUM The number of the screen node on the platform.
  # @param STEREO Boolean indicating if the view to be constructed is stereo or mono.
  def my_constructor(self, SCENEGRAPH, VIEWER, USER_ATTRIBUTES, PLATFORM_ID, DISPLAY_INSTANCE, SCREEN_NUM, STEREO):

    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    # structure of USER_ATTRIBUTES:
    # [stereo, headtrackingstation, startplatform, user_id, transmitteroffset, notrackingmat]

    ## @var view_id
    # User ID of this user within his or her user group.
    self.view_id = USER_ATTRIBUTES[3]
    
   	## @var platform_id
    # The platform id for which this client process is responsible for.
    self.platform_id = USER_ATTRIBUTES[2]

    ## @var ONLY_TRANSLATION_UPDATE
    # In case this boolean is true, only the translation values will be locally updated from the tracking system.
    self.ONLY_TRANSLATION_UPDATE = False


    # retrieve the needed values from display
    self.display_values = DISPLAY_INSTANCE.register_user()

    # check if no more users allowed at this screen
    if not self.display_values:
      # TODO better handling of this case?
      print 'Error: no more users allowed at display "' + DISPLAY_INSTANCE.name + '"!'
      return


    self.window_size = avango.gua.Vec2ui(DISPLAY_INSTANCE.resolution[0], DISPLAY_INSTANCE.resolution[1]) 

    # create window
    self.window = avango.gua.nodes.Window()
    self.window.Display.value = self.display_values[0] # GPU-ID

    # create camera
    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = SCENEGRAPH.Name.value

    # set render mask for camera
    _render_mask = "!do_not_display_group && !avatar_group_" + str(self.platform_id) + " && !couple_group_" + str(self.platform_id)

    for _i in range(0, 10):
      if _i != self.platform_id:
        _render_mask = _render_mask + " && !platform_group_" + str(_i)

    self.camera.RenderMask.value = _render_mask

    # create pipeline
    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.Enabled.value = True

    if STEREO:

      '''
        Stereo View
      '''

      self.camera.LeftScreen.value = "/net/platform_" + str(self.platform_id) + "/scale/screen_" + str(SCREEN_NUM)
      self.camera.RightScreen.value = "/net/platform_" + str(self.platform_id) + "/scale/screen_" + str(SCREEN_NUM)
      self.camera.LeftEye.value = "/net/platform_" + str(self.platform_id) + "/scale/head_" + str(self.view_id) + "/eyeL"
      self.camera.RightEye.value = "/net/platform_" + str(self.platform_id) + "/scale/head_" + str(self.view_id) + "/eyeR"

      self.window.Title.value = "User_" + str(self.view_id)
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
          #self.window.StereoMode.value = avango.gua.StereoMode.ANAGLYPH_RED_GREEN
          self.window.StereoMode.value = avango.gua.StereoMode.ANAGLYPH_RED_CYAN

        elif DISPLAY_INSTANCE.stereomode == "CHECKERBOARD":
          self.window.StereoMode.value = avango.gua.StereoMode.CHECKERBOARD

      self.pipeline.EnableStereo.value = True
      self.pipeline.LeftResolution.value = self.window.LeftResolution.value
      self.pipeline.RightResolution.value = self.window.RightResolution.value

    else:

      '''
        Mono View
      '''

      self.camera.LeftScreen.value = "/net/platform_" + str(self.platform_id) + "/scale/screen_" + str(SCREEN_NUM)
      self.camera.LeftEye.value = "/net/platform_" + str(self.platform_id) + "/scale/head_" + str(self.view_id) + "/eye"

      self.window.Title.value = "User_" + str(self.view_id)
      self.window.Size.value = self.window_size
      self.window.LeftResolution.value = self.window_size

      self.pipeline.EnableStereo.value = False
      self.pipeline.LeftResolution.value = self.window.LeftResolution.value


    self.pipeline.Window.value = self.window
    self.pipeline.Camera.value = self.camera


    '''
      General user settings
    '''

    # set nice pipeline values
    ClientPipelineValues.set_pipeline_values(self.pipeline)

    # add tracking reader to avoid latency
    self.init_local_tracking_override(USER_ATTRIBUTES[1], USER_ATTRIBUTES[4])

    # set display string and warpmatrices as given by the display
    if len(self.display_values) > 1:
      self.set_warpmatrices(self.window, self.display_values[1])
    
    # append pipeline to the viewer
    VIEWER.Pipelines.value.append(self.pipeline)


  ### Functions ###
  
  ## Adds a tracking reader to the view instance.
  # @param TRACKING_TARGET_NAME The target name of the tracked object as chosen in daemon.
  # @param TRANSMITTER_OFFSET The transmitter offset to be applied.
  def init_local_tracking_override(self, TRACKING_TARGET_NAME, TRANSMITTER_OFFSET):

  	## @var headtracking_reader
    # Instance of a child class of ClientTrackingReader to supply translation input.
    if TRACKING_TARGET_NAME != None:
      self.headtracking_reader = ClientTrackingTargetReader()
      self.headtracking_reader.my_constructor(TRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(TRANSMITTER_OFFSET)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

      self.sf_head_mat.connect_from(self.headtracking_reader.sf_tracking_mat)


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

  
  ### Callbacks ###

  ## Called whenever sf_head_mat changes.
  @field_has_changed(sf_head_mat)
  def sf_head_mat_changed(self):

    _head_node = self.SCENEGRAPH["/net/platform_" + str(self.platform_id) + "/scale/head_" + str(self.view_id)]

    if _head_node != None:
      if self.ONLY_TRANSLATION_UPDATE:
        _mat = _head_node.Transform.value
        _mat.set_translate(self.sf_head_mat.value.get_translate())
        _head_node.Transform.value = _mat
      else:
        _head_node.Transform.value = self.sf_head_mat.value

