#!/usr/bin/python

## @file
# Contains class StaticNavigation.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from Navigation import *

class StaticNavigation(Navigation):

  def __init__(self):
    self.super(StaticNavigation).__init__()

  def my_constructor(self, STATIC_ABS_MAT, STATIC_SCALE, AVATAR_TYPE):

    ## @var avatar_type
    # A string that determines what kind of avatar representation is to be used, e.g. "joseph".
    self.avatar_type = AVATAR_TYPE

    self.sf_abs_mat.value = STATIC_ABS_MAT
    self.sf_scale.value = STATIC_SCALE
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)