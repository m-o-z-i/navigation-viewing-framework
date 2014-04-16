#!/usr/bin/python

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
                    , translation = (0.0, 1.57, 0.0)
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
                    , translation = (0.0, 1.42, 0.0)
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
class TouchTable(Display):
##################################################
  def __init__(self):
    Display.__init__( self
                    , hostname = "perseus"
                    , name = "touch_table"
                    , resolution = (3840, 2160)
                    , displaystrings = [":0.0"]
                    , size = (1.25, 0.70)
                    , translation = (0.0, 0.65, 0.0)
                    , rotation = (-90.0, 0.0, 0.0)
                    )


##################################################
# STORE ALL DISPLAYS TO BE USED IN THIS LIST
##################################################
displays = [
    LargePowerwall()
  , SmallPowerwall()
  , TouchTable()
  , Display(hostname = "atalante", translation = (0.0, 1.0, 0.0))
  , Display(hostname = "nestor", translation = (0.0, 1.0, 0.0))
  #, Display(hostname = "nestor", translation = (-0.645, 1.0, 0.0))
]
