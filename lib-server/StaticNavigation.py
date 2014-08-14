#!/usr/bin/python

## @file
# Contains class StaticNavigation.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from Navigation import *

## Representation of a static navigation. Fills sf_abs_mat and sf_scale with constant values and
# computes sf_nav_mat only once.
class StaticNavigation(Navigation):

  ## Default constructor.
  def __init__(self):
    self.super(StaticNavigation).__init__()

  ## Custom constructor.
  # @param STATIC_ABS_MAT Static value to be set for sf_abs_mat.
  # @param STATIC_SCALE Static value to be set for sf_scale.
  # @param AVATAR_TYPE Avatar type of this navigation instance.
  def my_constructor(self, STATIC_ABS_MAT, STATIC_SCALE, AVATAR_TYPE):

    ## @var avatar_type
    # A string that determines what kind of avatar representation is to be used, e.g. "joseph".
    self.avatar_type = AVATAR_TYPE

    self.sf_abs_mat.value = STATIC_ABS_MAT
    self.sf_scale.value = STATIC_SCALE
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)