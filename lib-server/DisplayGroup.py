#!/usr/bin/python

## @file
# Contains class DisplayGroup.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from   Display import *
from   SteeringNavigation import *

## Collection of displays that are semantically one navigational unit, although users
# might have individual navigations assigned.
class DisplayGroup:

  ## Custom constructor.
  # @param ID Identification number of this DisplayGroup within the workspace.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assigned to the display group.
  #
	def __init__(self, ID, DISPLAY_LIST, NAVIGATION_LIST, OFFSET_TO_WORKSPACE, WORKSPACE_TRANSMITTER_OFFSET):

    ## @var id
    # Identification number of this DisplayGroup within the workspace.
		self.id = ID

    ## @var displays
    # List of Display instances assigned to this display group.
		self.displays = DISPLAY_LIST

		## @var navigations
		# List of (Steering-)Navigation instances assigned to the display group.
		self.navigations = NAVIGATION_LIST

		##
		#
		self.offset_to_workspace = OFFSET_TO_WORKSPACE

		for _navigation in self.navigations:
			
			try:
				_navigation.device.tracking_reader.set_transmitter_offset(self.offset_to_workspace * WORKSPACE_TRANSMITTER_OFFSET)
			except:
				pass


  ## Overwrites the navigation matrices of all navigations with the matrix of the first one.
	def synchronize_navigations(self):

		_transformation = self.navigations[0].sf_abs_mat.value
		_scale = self.navigations[0].sf_scale.value

		for _i in range(1, len(self.navigations)):
			self.navigations[_i].inputmapping.set_abs_mat(_transformation)
			self.navigations[_i].inputmapping.set_scale(_scale)
