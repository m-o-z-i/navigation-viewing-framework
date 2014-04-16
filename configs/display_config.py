#!/usr/bin/python

import avango
import avango.gua
from Display import Display

##################################################
class LargePowerwall(Display):
##################################################
  def __init__(self):
    Display.__init__( self
                    , hostname = "kerberos"
                    , name = "large_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1", ":0.2", ":0.3"]
                    , size = (4.16, 2.6)
                    , transformation = (0.0, 1.57, 0.0)
                    )

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

##################################################
class SmallPowerwall(Display):
##################################################
  def __init__(self):
    Display.__init__( self
                    , hostname = "medusa"
                    , name = "small_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1"]
                    , size = (3.0, 1.98)
                    , transformation = (0.0, 1.42, 0.0)
                    )

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


##################################################
# STORE ALL DISPLAYS TO BE USED IN THIS LIST
##################################################
displays = [
    LargePowerwall()
  , SmallPowerwall()
  , Display(hostname = "perseus"
      , name = "touch_table"
      , resolution = (3840, 2160)
      , size = (1.25, 0.7)
      , transformation = avango.gua.make_rot_mat(-90, 1, 0, 0) * avango.gua.make_trans_mat(0, 0.65, 0)
  )
  , Display(hostname = "atalante"
      , transformation = avango.gua.make_trans_mat(0.0, 1.0, 0.0)
  )
  , Display(hostname = "nestor"
      , transformation = avango.gua.make_trans_mat(-0.645, 1.0, 0.0)
  )
]
