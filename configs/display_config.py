#!/usr/bin/python

## @file
# Contains display configuration classes and a list of Display instances to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from Display import Display

## Display configuration for the large powerwall in the VR lab.
class LargePowerwall(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "kerberos"
                    , name = "large_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1", ":0.2", ":0.3"]
                    #, displaystrings = [":0.0", ":0.1", ":0.2", ":0.3", ":0.4", "0.5"]
                    #, shutter_timings = [ [(0,100), (2400,2500)], 
                    #                      [(3000,3100),(4600,4700)],
                    #                      [(5700,5800), (8175,8275)],
                    #                      [(8200,8300), (10700,10800)],
                    #                      [(11400,11500), (12900,13000)],
                    #                      [(14000,14100), (15800,15900)]
                    #                    ]
                    , shutter_timings = [ [(0,100), (8175,8275)],
                                          [(8200,8300), (10700,10800)],
                                          [(11400,11500), (12900,13000)],
                                          [(14000,14100), (15800,15900)]
                                        ]
                    #, shutter_values = [  [(22,88), (44,11)],
                    #                      [(22,88), (44,11)],
                    #                      [(22,88), (44,11)],
                    #                      [(22,88), (44,11)],
                    #                      [(22,88), (44,11)],
                    #                      [(22,88), (44,11)]
                    #                   ]
                    , shutter_values = [  [(22,88), (44,11)],
                                          [(22,88), (44,11)],
                                          [(22,88), (44,11)],
                                          [(22,88), (44,11)]
                                       ]
                    , size = (4.16, 2.6)
                    , transformation = avango.gua.make_trans_mat(0, 1.57, 0)
                    , stereomode = "SIDE_BY_SIDE"                    
                    )

  ## Registers a new view at this display and returns the display string 
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 4:
      warpmatrices = [
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None

## Display configuration for the small powerwall in the VR lab.
class SmallPowerwall(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "medusa"
                    , name = "small_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1"]
                    , size = (3.0, 1.98)
                    , transformation = avango.gua.make_trans_mat(0, 1.42, 0)
                    , stereomode = "SIDE_BY_SIDE"
                    )

  ## Registers a new view at this display and returns the display string 
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 2:
      warpmatrices = [
          "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)

        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None



class SamsungStereoTV(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "apollo"
                    , name = "samsung_tv"
                    , resolution = (1920, 1080)
                    , displaystrings = [":0.0"]
                    , size = (1.235, 0.695)
                    , transformation = avango.gua.make_trans_mat(0.0,1.6,0.0) * avango.gua.make_rot_mat(-40.0,1,0,0)
                    , stereomode = "CHECKERBOARD"
                    )


class MitsubishiStereoTV(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "demeter"
                    , name = "mitsubishi_tv"
                    , resolution = (1920, 1080)
                    , displaystrings = [":0.0"]
                    , size = (1.44, 0.81)
                    , transformation = avango.gua.make_trans_mat(0.0,1.3,0.0)
                    , stereomode = "CHECKERBOARD"
                    )


##################################################
# STORE ALL DISPLAYS TO BE USED IN THIS LIST
##################################################
## @var displays A list of Display instances to be used in the framework.

displays = [
    LargePowerwall()
  , Display(hostname = "atalante"
      , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0)
      #, transformation = avango.gua.make_trans_mat(0.645, 1.2, 0.0)
  )
  , Display(hostname = "daedalos"
      , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0)
      #, transformation = avango.gua.make_trans_mat(0.645, 1.2, 0.0)
  )
  , Display(hostname = "nestor"
      , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0)
  )
]
