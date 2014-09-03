#!/usr/bin/python

## @file
# Contains class Display.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ConsoleIO import *

## Class representing a display. A display is a physical projection medium
# running on a host and having certain resolution, size and transformation. It
# supports a specific amount of users. In the Platform class, a screen node
# is associated for each display.
class Display:

  ## Custom constructor
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param shutter_timings A list of lists of opening and closing times of shutter glasses for each displaystring.
  # @param shutter_values A list of lists of hexadecimal commands for shutter glasses associated with the timings for each displaystring.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  # @param max_viewing_distance Specification of the maximum viewing distance for the shutters to sync in.
  # @param stereo Boolean indicating if the stereo mode is to be used.
  # @param stereomode A string indicating the stereo mode that is used by this display.
  # @param cameramode An integer indicating the Mode field value to be set on the rendering camera.
  # @param render_mask A string supplying additional render mask constraints.
  def __init__( self
              , hostname
              , name = None
              , resolution = (2560, 1440)
              , displaystrings = [":0.0"]
              , shutter_timings = []
              , shutter_values = []
              , size = (0.595, 0.335)
              , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0)
              , max_viewing_distance = 1.0
              , stereo = False
              , stereomode = "ANAGLYPH_RED_CYAN"
              , cameramode = 0
              , render_mask = ""
              ):

    # save values in members
    ## @var hostname
    # The hostname to which this display is connected to.
    self.hostname = hostname

    # default naming for desktop setups
    ## @var name
    # A name to be associated to that display. Will be used in XML configuration file.
    if not name:
      self.name = hostname + "_display"
    else:
      self.name = name

    ## @var resolution
    # The display's resolution to be used.
    self.resolution = resolution

    ## @var displaystrings
    # A list of strings on which the windows for each user will pop up.
    self.displaystrings = displaystrings

    ## @var shutter_timings
    # A list of lists of opening and closing times of shutter glasses for each displaystring.
    self.shutter_timings = shutter_timings

    ## @var shutter_values
    # A list of lists of hexadecimal commands for shutter glasses associated with the timings for each displaystring.
    self.shutter_values = shutter_values

    ## @var size
    # A list of strings on which the windows for each user will pop up.
    self.size = size

    ## @var transformation
    # A matrix specifying the display's transformation with respect to the platform coordinate system.
    self.transformation = transformation

    ## @var max_viewing_distance
    # Specification of the maximum viewing distance for the shutters to sync in.
    self.max_viewing_distance = max_viewing_distance

    ## @var num_views
    # Number of views which are already registered with this display.
    self.num_views = 0

    ## @var stereo
    # Boolean indicating if the stereo mode is to be used.
    self.stereo = stereo

    ## @var stereomode
    # A string indicating the stereo mode that is used by this display.
    self.stereomode = stereomode

    ## @var cameramode
    # An integer indicating the Mode field value to be set on the rendering camera.
    self.cameramode = cameramode

    ## @var render_mask
    # A string supplying additional render mask constraints.
    self.render_mask = render_mask


  ## Registers a new view at this display and returns the display string assigned to the new view.
  def register_view(self, view_num):
    #view_num = self.num_views
    if view_num < len(self.displaystrings):
      self.num_views += 1
      return [self.displaystrings[view_num]]
    else:
      return None

  ## Creates the screen node of this display to be appended to the Platform transformation node.
  # @param name The name of the screen scenegraph node.
  def create_screen_node(self, name = "screen_node"):
    _screen = avango.gua.nodes.ScreenNode(Name = name)
    _w, _h = self.size
    _screen.Width.value = _w
    _screen.Height.value = _h
    _screen.Transform.value = self.transformation
    return _screen

  ## Returns the shutter mode according to the shutter timings set.
  # Can be ACTIVE_STEREO, PASSIVE_STEREO or NONE.
  def get_shutter_mode(self):

    if self.shutter_timings == []:
      return "NONE"
    elif len(self.shutter_timings[0][0]) == 2:
      return "PASSIVE_STEREO"
    elif len(self.shutter_timings[0][0]) == 4:
      return "ACTIVE_STEREO"

  ## Creates a visualization of the display's screen in the scene (white frame). Returns the scenegraph geometry node.
  def create_screen_visualization(self):

    _loader = avango.gua.nodes.TriMeshLoader()

    _node = _loader.create_geometry_from_file("screen_visualization", "data/objects/screen.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF

    _w, _h = self.size
    _node.Transform.value = self.transformation * avango.gua.make_scale_mat(_w,_h,1.0)

    return _node

  ## Creates a proxy geometry for this display to be checked for intesections in the global tracking space.
  # @param PLATFORM Reference to the Platform instance to which the display is belonging.
  # @param SCREEN_ID Number of the screen this display is representing on the platform.
  def create_transformed_proxy_geometry(self, PLATFORM, SCREEN_ID):

    _loader = avango.gua.nodes.TriMeshLoader()

    _node = _loader.create_geometry_from_file("proxy_" + str(PLATFORM.platform_id) + "_" + str(SCREEN_ID)
                                            , "data/objects/plane.obj", "data/materials/AvatarBlue.gmd"
                                            , avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    _node.GroupNames.value = ["do_not_display_group", "screen_proxy_group"]
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF

    _w, _h = self.size

    # make proxy geometry a little larger than the actual screen
    _w += 0.5
    _h += 0.5

    _node.Transform.value = self.transformation * avango.gua.make_rot_mat(90, 1, 0 ,0) * avango.gua.make_scale_mat(_w,1.0,_h)

    # eliminate transmitter offset to transform screen in tracking space
    _node.Transform.value =  avango.gua.make_inverse_mat(PLATFORM.transmitter_offset) * _node.Transform.value

    return _node
