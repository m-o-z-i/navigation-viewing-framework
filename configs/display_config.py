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
                    , size = (4.16, 2.6)
                    , transformation = avango.gua.make_trans_mat(0, 1.57, 0)
                    , stereomode = "SIDE_BY_SIDE"                    
                    )

  ## Registers a new user at this display and return the display string and the 
  # warp matrices assigned to the new user.
  def register_user(self):
    user_num = self.num_users
    if user_num < 4:
      warpmatrices = [
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      ]
      self.num_users += 1
      return (self.displaystrings[user_num], warpmatrices)
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

  ## Registers a new user at this display and return the display string and the 
  # warp matrices assigned to the new user.
  def register_user(self):
    user_num = self.num_users
    if user_num < 2:
      warpmatrices = [
          "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)

        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
      ]
      self.num_users += 1
      return (self.displaystrings[user_num], warpmatrices)
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
  Display(hostname = "atalante"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
      #, transformation = avango.gua.make_trans_mat(0.645, 1.0, 0.0)
  )
  , Display(hostname = "nestor"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
  )
]



'''
displays = [
    SamsungStereoTV()
  , MitsubishiStereoTV()
  , Display(hostname = "atalante"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
      #, transformation = avango.gua.make_trans_mat(0.645, 1.0, 0.0)
      , stereomode = "CHECKERBOARD"
  )
  , Display(hostname = "nestor"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
  )
]
'''

'''
displays = [
    LargePowerwall()
  , SmallPowerwall()
  , Display(hostname = "perseus"
      , name = "touch_table"
      , resolution = (3840, 2160)
      , size = (1.25, 0.7)
      , transformation = avango.gua.make_trans_mat(0, 0.65, 0) * avango.gua.make_rot_mat(-90, 1, 0, 0)
  )
  , Display(hostname = "atalante"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
      #, transformation = avango.gua.make_trans_mat(0.645, 1.0, 0.0)      
  )
  , Display(hostname = "nestor"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
  )
]
'''
