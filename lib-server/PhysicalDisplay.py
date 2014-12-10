#!/usr/bin/python

## @file
# Contains class PhysicalDisplay.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from Display import *
from ConsoleIO import *

## Class representing a physical display. A physical display is a projection medium
# running on a host and having certain resolution, size and transformation. It
# supports a specific amount of users.
class PhysicalDisplay(Display):
  
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

    # default naming for desktop setups
    if not name:
      _name = hostname + "_display"
    else:
      _name = name

    self.base_constructor(_name, resolution, size, stereo)

    # save values in members
    ## @var hostname
    # The hostname to which this display is connected to.
    self.hostname = hostname
    
    ## @var displaystrings
    # A list of strings on which the windows for each user will pop up.
    self.displaystrings = displaystrings

    ## @var shutter_timings
    # A list of lists of opening and closing times of shutter glasses for each displaystring.
    self.shutter_timings = shutter_timings

    ## @var shutter_values
    # A list of lists of hexadecimal commands for shutter glasses associated with the timings for each displaystring.
    self.shutter_values = shutter_values
    
    ## @var transformation
    # A matrix specifying the display's transformation with respect to the platform coordinate system.
    self.transformation = transformation

    ## @var max_viewing_distance 
    # Specification of the maximum viewing distance for the shutters to sync in.
    self.max_viewing_distance = max_viewing_distance

    ## @var num_views
    # Number of views which are already registered with this display.
    self.num_views = 0
   
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
  def register_view(self):
    view_num = self.num_views
    if view_num < len(self.displaystrings):
      self.num_views += 1
      return [self.displaystrings[view_num]]
    else:
      return None

  ## Creates the screen node of this display to be appended to the Platform transformation node.
  # @param name The name of the screen scenegraph node.
  def create_screen_node(self, Name = "screen_node"):
    _screen = avango.gua.nodes.ScreenNode(Name = Name)
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

  ## Sets the transformation of this physical display to a value when the standard values shall not be used.
  # @param MATRIX The transformation matrix to be set.
  def set_transformation(self, MATRIX):

    self.transformation = MATRIX


  ## Creates a visualization of the display's screen in the scene (white frame). Returns the scenegraph geometry node.
  def create_screen_visualization(self, NODE_NAME):
  
    _loader = avango.gua.nodes.TriMeshLoader()
  
    _node = _loader.create_geometry_from_file(NODE_NAME, "data/objects/screen.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF

    _w, _h = self.size
    _node.Transform.value = self.transformation * avango.gua.make_scale_mat(_w,_h,1.0)
    
    return _node

  ## Creates a proxy geometry for this display to be checked for intesections in the global tracking space.
  # @param WORKSPACE_INSTANCE The Workspace instance to which this Display is belonging to.
  # @param DISPLAY_GROUP_INSTANCE The DisplayGroup instance to which this Display is belonging to.
  # @param DISPLAY_NUM Integer saying which index in the DisplayGroup this Display has, starting from 0.
  def create_transformed_proxy_geometry(self, WORKSPACE_INSTANCE, DISPLAY_GROUP_INSTANCE, DISPLAY_NUM):
  
    _loader = avango.gua.nodes.TriMeshLoader()
  
    _node = _loader.create_geometry_from_file("proxy_w" + str(WORKSPACE_INSTANCE.id) + "_dg" + str(DISPLAY_GROUP_INSTANCE.id) + "_s" + str(DISPLAY_NUM)
                                            , "data/objects/plane.obj"
                                            , "data/materials/White.gmd"
                                            , avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    _node.GroupNames.value = ["screen_proxy_group"]
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF

    _w, _h = self.size

    # make proxy geometry a little larger than the actual screen
    _w += 0.5
    _h += 0.5

    _node.Transform.value = avango.gua.make_inverse_mat(DISPLAY_GROUP_INSTANCE.offset_to_workspace * WORKSPACE_INSTANCE.transmitter_offset) * \
                            self.transformation * avango.gua.make_rot_mat(90, 1, 0 ,0) * avango.gua.make_scale_mat(_w,1.0,_h)
    
    return _node

  def get_touch_protocols(self):
    return [ "NONE" ]



# specialized display setups #

## Display configuration for the large powerwall in the VR lab.
class LargePowerwall(PhysicalDisplay):
  
  ## Default constructor.
  def __init__(self, render_mask = ""):
    PhysicalDisplay.__init__( self
                    , hostname = "kerberos"
                    , name = "large_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1", ":0.2", ":0.3"]
                    #, displaystrings = [":0.0", ":0.1", ":0.2"]
                    , size = (4.16, 2.61)
                    , transformation = avango.gua.make_trans_mat(0, 1.57, 0)
                    #, shutter_timings = [ [(0,2400), (100,2500)],
                    #                      [(3000,4600),(3100,4700)],
                    #                      [(5700,8175), (5800,8275)],
                    #                      [(8200,10700), (8300,10800)],
                    #                      [(11400,12900), (11500,13000)],
                    #                      [(14000,15800), (14100,15900)]
                    #                    ]
                    , shutter_timings = [ [(0,8175), (100,8275)],
                                          [(8200,10700), (8300,10800)],
                                          [(11400,12900), (11500,13000)],
                                          [(14000,15800), (14100,15900)]
                                        ]
                    #, shutter_values = [  [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)]
                    #                   ]
                    , shutter_values = [  [(22,44), (88,11)],
                                          [(22,44), (88,11)],
                                          [(22,44), (88,11)],
                                          [(22,44), (88,11)]
                                       ]
                    , max_viewing_distance = 5.0
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    , render_mask = render_mask
                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < len(self.displaystrings):
      warpmatrices = [
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        #  "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        #, "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        #, "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"        
        #, "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        #, "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        #, "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None

## Display configuration for the small powerwall in the VR lab.
class SmallPowerwall(PhysicalDisplay):

  ## Default constructor.
  def __init__(self, render_mask = ""):
    PhysicalDisplay.__init__( self
                    , hostname = "pandora"
                    , name = "small_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1"]
                    , size = (3.0, 1.98)
                    , transformation = avango.gua.make_trans_mat(0, 1.42, 0)
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    , shutter_timings = [  [(100, 200, 2900, 3000), (8400, 8500, 11400, 11500)],
                                           [(2600, 2700, 5700, 5800), (11000, 11100, 14600, 14700)],
                                           [(6000, 6100, 8200, 8300), (14300, 14400, 15900, 16000)]
                                        ]
                    , shutter_values =  [  [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)]
                                        ]                    
                    , render_mask = render_mask
                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 2:
      warpmatrices = [
          "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)

        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None


## Display configuration for the small powerwall in the VR lab.
class SmallPowerwall2(PhysicalDisplay):

  ## Default constructor.
  def __init__(self, render_mask = ""):
    PhysicalDisplay.__init__( self
                    , hostname = "pandora"
                    , name = "small_powerwall2"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0"]
                    , size = (3.0, 1.98)
                    , transformation = avango.gua.make_trans_mat(0, 1.42, 0)
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    , shutter_timings = [  [(100, 200, 2900, 3000), (8400, 8500, 11400, 11500)],
                                           [(2600, 2700, 5700, 5800), (11000, 11100, 14600, 14700)],
                                           [(6000, 6100, 8200, 8300), (14300, 14400, 15900, 16000)]
                                        ]
                    , shutter_values =  [  [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)]
                                        ]                    
                    , render_mask = render_mask
                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 2:
      warpmatrices = [
          "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)

        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None

## Display configuration for the 3D multiuser touch table in the VR lab.
class TouchTable3D(PhysicalDisplay):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self, render_mask = ""):
    PhysicalDisplay.__init__( self
                    , hostname = "medusa"
                    , name = "touch_table_3D"
                    , resolution = (1400, 1050)
                    , displaystrings = [":0.0", ":0.1", ":0.2"] 
                    , shutter_timings = [  [(100, 200, 2900, 3000), (8400, 8500, 11400, 11500)],
                                           [(2600, 2700, 5700, 5800), (11000, 11100, 14600, 14700)],
                                           [(6000, 6100, 8200, 8300), (14300, 14400, 15900, 16000)]                                          
                                        ]

                    , shutter_values =  [  [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)]
                                        ]
                    , size = (1.15, 0.84)
                    , transformation = avango.gua.make_rot_mat(90, -1, 0, 0)
                    , max_viewing_distance = 1.0
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    , render_mask = render_mask                   
                    )

  ## Registers a new view at this display and returns the display string 
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 3:
      warpmatrices = [
          "/opt/3D43-warpmatrices/3D43_warp_P4.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P5.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P6.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P1.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P2.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P3.warp"
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None

  def get_touch_protocols(self):
    return [ "TUIO" ]

## Display configuration for the Samsung Stereo TV in the VR lab. 
class SamsungStereoTV(PhysicalDisplay):

  ## Default constructor.
  def __init__(self, render_mask = ""):
    PhysicalDisplay.__init__( self
                    , hostname = "apollo"
                    , name = "samsung_tv"
                    , resolution = (1920, 1080)
                    , displaystrings = [":0.0"]
                    , size = (1.235, 0.695)
                    , transformation = avango.gua.make_trans_mat(0.0,1.6,0.0) * avango.gua.make_rot_mat(-40.0,1,0,0)
                    , stereo = True
                    , stereomode = "CHECKERBOARD"
                    , render_mask = render_mask
                    )

## Display configuration for the Mitsubishi Stereo TV in the VR lab. 
class MitsubishiStereoTV(PhysicalDisplay):

  ## Default constructor.
  def __init__(self, render_mask = ""):
    PhysicalDisplay.__init__( self
                    , hostname = "demeter"
                    , name = "mitsubishi_tv"
                    , resolution = (1920, 1080)
                    , displaystrings = [":0.0"]
                    , size = (1.44, 0.81)
                    , transformation = avango.gua.make_trans_mat(0.0,1.3,0.0)
                    , stereo = True
                    , stereomode = "CHECKERBOARD"
                    , render_mask = render_mask
                    )