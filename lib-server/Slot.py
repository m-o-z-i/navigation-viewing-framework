#!/usr/bin/python

## @file
# Contains class Slot.

# import avango-guacamole libraries
import avango
import avango.gua

## 
#
class Slot:

  ## Custom constructor.
  #
  #
  def __init__(self, DISPLAY, SLOT_ID, STEREO, PLATFORM_NODE, HEADTRACKING_STATION):

    ##
    #
    self.slot_id = slot_id

    ##
    #
    self.stereo = STEREO

    ##
    #
    self.PLATFORM_NODE = PLATFORM_NODE

    ##
    #
    self.headtracking_station = HEADTRACKING_STATION

    ##
    #
    if self.stereo:
      self.shutter_timing = DISPLAY.shutter_timings[SLOT_ID]
    else:
      self.shutter_timing = None

    ##
    #
    if self.stereo:
      self.shutter_value = DISPLAY.shutter_values[SLOT_ID]
    else:
      self.shutter_value = None

    # append nodes to platform transform node