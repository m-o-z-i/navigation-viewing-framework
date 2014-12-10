#!/usr/bin/python

## @file
# Contains class DisplayGroup.

# import avango-guacamole libraries
import avango
import avango.gua


## Collection of displays that are semantically one navigational unit, although users
# might have individual navigations assigned.
class DisplayGroup:

  ## Custom constructor.
  # @param ID Identification number of this DisplayGroup within the workspace.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assigned to the display group.
  # @param VISIBILITY_TAG Tag used by the Tools' visibility matrices to define if they are visible for this display group.
  # @param OFFSET_TO_WORKSPACE Offset describing the origin of this display group with respect to the origin of the workspace.
  # @param WORKSPACE_TRANSMITTER_OFFSET Transmitter offset applied in the workspace.
  def __init__(self, ID, DISPLAY_LIST, NAVIGATION_LIST, VISIBILITY_TAG, OFFSET_TO_WORKSPACE, WORKSPACE_TRANSMITTER_OFFSET):

    ## @var id
    # Identification number of this DisplayGroup within the workspace.
    self.id = ID

    ## @var displays
    # List of Display instances assigned to this display group.
    self.displays = DISPLAY_LIST

    ## @var navigations
    # List of (Steering-)Navigation instances assigned to the display group.
    self.navigations = NAVIGATION_LIST

    ## @var visibility_tag
    # Tag used by the Tools' visibility matrices to define if they are visible for this display group.
    self.visibility_tag = VISIBILITY_TAG

    ## @var offset_to_workspace
    # Offset describing the origin of this display group with respect to the origin of the workspace.
    self.offset_to_workspace = OFFSET_TO_WORKSPACE

    # update device tracking transmitter offset
    for _navigation in self.navigations:
      
      try:
        _navigation.device.tracking_reader.set_transmitter_offset(self.offset_to_workspace * WORKSPACE_TRANSMITTER_OFFSET)
      except:
        pass

      