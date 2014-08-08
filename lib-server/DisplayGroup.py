#!/usr/bin/python

## @file
# Contains class DisplayGroup.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from   Display import *
from   SteeringNavigation import *

class DisplayGroup:

	def __init__(self, ID, DISPLAY_LIST, NAVIGATION_LIST):

		self.id = ID

		self.displays = DISPLAY_LIST

		self.navigations = NAVIGATION_LIST

	def synchronize_navigations(self):

		_transformation = self.navigations[0].sf_abs_mat.value
		_scale = self.navigations[0].sf_scale.value

		for _i in range(1, len(self.navigations)):
			self.navigations[_i].inputmapping.set_abs_mat(_transformation)
			self.navigations[_i].inputmapping.set_scale(_scale)
