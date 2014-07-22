#!/usr/bin/python

## @file
# Contains class BorderObserver.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
from Platform        import *
from User            import *

## Class to check whether the user of a slot is close to platform borders.
#
# If the observed user is close to a platform border, the corresponding
# border plane is made visible.

class BorderObserver(avango.script.Script):

  ## @var warning_tolerance
  # Distance to a border when the warning plane should be displayed
  warning_tolerance = 0.6

  ## Default constructor
  def __init__(self):
    self.super(BorderObserver).__init__()

  ## Custom constructor
  # @param CHECKED_BORDERS A list of four booleans about which borders of the platform should be observed. 
  #                        [display_left_border, display_right_border, display_front_border, display_back_border]
  # @param SLOT_INSTANCE The Slot instance this BorderObserver is looking for.
  # @param PLATFORM_WIDTH Physical width of the platform in meters.
  # @param PLATFORM_DEPTH Physical depth of the platform in meters.
  def my_constructor(self, CHECKED_BORDERS, SLOT_INSTANCE, PLATFORM_WIDTH, PLATFORM_DEPTH):

    ## @var checked_borders
    # A list of four booleans about which borders of the platform should be observed. [left, right, front, back].
    self.checked_borders = CHECKED_BORDERS     

    ## @var SLOT_INSTANCE
    # The Slot instance this BorderObserver is looking for.
    self.SLOT_INSTANCE = SLOT_INSTANCE

    ## @var platform_width
    # Physical width of the platform in meters.
    self.platform_width = PLATFORM_WIDTH

    ## @var platform_depth
    # Physical depth of the platform in meters.
    self.platform_depth = PLATFORM_DEPTH                  

    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):

    if self.SLOT_INSTANCE.assigned_user != None and self.SLOT_INSTANCE.assigned_user.enable_border_warnings:

      _left_plane_visible = False
      _right_plane_visible = False
      _front_plane_visible = False
      _back_plane_visible = False

      _user = self.SLOT_INSTANCE.assigned_user
      _pos = _user.headtracking_reader.sf_abs_vec.value

      if self.checked_borders[0]:
        # toggle left border visibility
        if _pos.x < -self.platform_width/2 + self.warning_tolerance:
          _left_plane_visible = True

      if self.checked_borders[1]:
        # toggle right border visibility
        if _pos.x > self.platform_width/2 - self.warning_tolerance:
          _right_plane_visible = True
   
      if self.checked_borders[2]:
        # toggle front border visibility
        if _pos.z < 0.0 + self.warning_tolerance:
          _front_plane_visible = True

      if self.checked_borders[3]:
        # toggle back border visibility
        if _pos.z > self.platform_depth - self.warning_tolerance:
          _back_plane_visible = True

      # set plane visibilities with respect to toggle variables
      
      if _left_plane_visible == False:
        self.SLOT_INSTANCE.display_left_border(False)
      else:
        self.SLOT_INSTANCE.display_left_border(True)

      if _right_plane_visible == False:
        self.SLOT_INSTANCE.display_right_border(False)
      else:
        self.SLOT_INSTANCE.display_right_border(True)

      if _front_plane_visible == False:
        self.SLOT_INSTANCE.display_front_border(False)
      else:
        self.SLOT_INSTANCE.display_front_border(True)

      if _back_plane_visible == False:
        self.SLOT_INSTANCE.display_back_border(False)
      else:
        self.SLOT_INSTANCE.display_back_border(True)


    else:
      
      self.SLOT_INSTANCE.display_left_border(False)
      self.SLOT_INSTANCE.display_right_border(False)
      self.SLOT_INSTANCE.display_front_border(False)
      self.SLOT_INSTANCE.display_back_border(False)