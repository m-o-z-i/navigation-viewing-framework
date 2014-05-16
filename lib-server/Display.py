#!/usr/bin/python

## @file
# Contains class Display.

# import avango-guacamole libraries
import avango
import avango.gua

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
  # @param stereomode A string indicating the stereo mode that is used by this display.
  def __init__( self
              , hostname
              , name = None
              , resolution = (2560, 1440)
              , displaystrings = [":0.0"]
              , shutter_timings = []
              , shutter_values = []
              , size = (0.595, 0.335)
              , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0)
              , stereomode = "ANAGLYPH_RED_CYAN"
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

    ## @var num_views
    # Number of views which are already registered with this display.
    self.num_views = 0
   
    ## @var stereomode
    # A string indicating the stereo mode that is used by this display.
    self.stereomode = stereomode

  ## Registers a new view at this display and returns the display string assigned to the new view.
  def register_view(self):
    view_num = self.num_views
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
  
    _loader = avango.gua.nodes.GeometryLoader()
  
    _node = _loader.create_geometry_from_file("screen_visualization", "data/objects/screen.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF

    _w, _h = self.size
    _node.Transform.value = self.transformation * avango.gua.make_scale_mat(_w,_h,1.0)
    
    return _node
