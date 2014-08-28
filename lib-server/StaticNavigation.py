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
  def my_constructor(self, STATIC_ABS_MAT, STATIC_SCALE):

    self.set_navigation_values(STATIC_ABS_MAT, STATIC_SCALE)

  ## Sets sf_abs_mat and sf_scale.
  # @param STATIC_ABS_MAT The new sf_abs_mat to be set.
  # @param STATIC_SCALE The new sf_scale to be set.
  def set_navigation_values(self, STATIC_ABS_MAT, STATIC_SCALE):
    self.sf_abs_mat.value = STATIC_ABS_MAT
    self.sf_scale.value = STATIC_SCALE
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)