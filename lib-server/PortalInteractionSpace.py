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

##
#

class PortalInteractionSpace(avango.script.Script):

	## Default constructor.
  def __init__(self):
    self.super(PortalInteractionSpace).__init__()

  ## Custom constructor.
  #
  def my_constructor(self, DEVICE, MIN_POINT, MAX_POINT):

  	self.DEVICE = DEVICE

  	self.MIN_POINT = MIN_POINT

  	self.MAX_POINT = MAX_POINT

  ##
  #
  def is_inside(self, POINT):
     
     _x = POINT.x
     _y = POINT.y
     _z = POINT.z

     if _x > self.MIN_POINT.x and _x < self.MAX_POINT.x and \
        _y > self.MIN_POINT.y and _y < self.MAX_POINT.y and \
        _z > self.MIN_POINT.z and _z < self.MAX_POINT.z:

       return True

     return False

  ##
  def get_values(self):

  	_values = self.DEVICE.mf_dof.value

  	_values[0] *= self.DEVICE.translation_factor
  	_values[1] *= self.DEVICE.translation_factor
  	_values[2] *= self.DEVICE.translation_factor
  	_values[3] *= self.DEVICE.rotation_factor
  	_values[4] *= self.DEVICE.rotation_factor
  	_values[5] *= self.DEVICE.rotation_factor

  	return _values