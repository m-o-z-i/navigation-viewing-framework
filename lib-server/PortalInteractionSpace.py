#!/usr/bin/python

## @file
# Contains class PortalInteractionSpace.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Device import *

# import python libraries
# ...

## Space on a platform in which an additional device can be used for
# modifying the scene matrices of portals.
class PortalInteractionSpace(avango.script.Script):

  ## Default constructor.
  def __init__(self):
    self.super(PortalInteractionSpace).__init__()

  ## Custom constructor.
  # @param DEVICE Instance of Device to be used for portal navigation.
  # @param MIN_POINT Minimum coordinates of the point spanning up the space.
  # @param MAX_POINT Maximum coordinates of the point spanning up the space.
  def my_constructor(self, DEVICE, MIN_POINT, MAX_POINT):

    ## @var DEVICE
    # Instance of Device to be used for portal navigation.
    self.DEVICE = DEVICE

    ## @var MIN_POINT
    # Minimum coordinates of the point spanning up the space.
    self.MIN_POINT = MIN_POINT

    ## @var MAX_POINT
    # Maximum coordinates of the point spanning up the space.
    self.MAX_POINT = MAX_POINT

  ## Returns a boolean saying if a point lies within the interaction space.
  # @param POINT The point to be checked for.
  def is_inside(self, POINT):
     
     _x = POINT.x
     _y = POINT.y
     _z = POINT.z

     if _x > self.MIN_POINT.x and _x < self.MAX_POINT.x and \
        _y > self.MIN_POINT.y and _y < self.MAX_POINT.y and \
        _z > self.MIN_POINT.z and _z < self.MAX_POINT.z:

       return True

     return False

  ## Returns the current input values of the associated device.
  def get_values(self):

    _values = self.DEVICE.mf_dof.value

    _values[0] *= self.DEVICE.translation_factor
    _values[1] *= self.DEVICE.translation_factor
    _values[2] *= self.DEVICE.translation_factor
    _values[3] *= self.DEVICE.rotation_factor
    _values[4] *= self.DEVICE.rotation_factor
    _values[5] *= self.DEVICE.rotation_factor

    return _values