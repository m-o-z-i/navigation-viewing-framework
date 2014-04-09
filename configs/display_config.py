#!/usr/bin/python

from Display import Display

##################################################
class LargePowerwall(Display):
##################################################
  def __init__(self):
    self.name = "large_powerwall"
    self.hostname = "kerberos"
    self.resolution = (1920, 1200)
    self.displaystrings = [":0.0", ":0.1", ":0.2", ":0.3"]
    self.size = (4.16, 2.6)
    self.transform = (0.0, 1.57, 0.0)

  def register_user(self, user_num):
    if user_num < 4:
      warpmatrices = [
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      ]
      return (self.displaystrings[user_num], warpmatrices)
    else:
      return None

##################################################
class SmallPowerwall(Display):
##################################################
  def __init__(self):
    self.name = "small_powerwall"
    self.hostname = "tba"
    self.resolution = (1920, 1200)
    self.displaystrings = [":0.0", ":0.1"]
    self.size = (3.0, 1.98)
    self.transform = (0.0, 1.42, 0.0)

  def register_user(self, user_num):
    if user_num < 2:
      warpmatrices = [
          "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 2)
      
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
        , "{0}lcd_4_warp_P{1}.warp".format(warp_matrices_path, 2 * user_num + 1)
      ]
      return (self.displaystrings[user_num], warpmatrices)
    else:
      return None

##################################################
# STORE ALL DISPLAYS TO BE USED IN THIS LIST
##################################################
displays = [
    LargePowerwall()
  , SmallPowerwall()
  , Display("atalante")
]
