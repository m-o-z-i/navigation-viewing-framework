#!/usr/bin/python

## @file
# Contains class Workspace.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ConsoleIO import *
from Display import *
from DisplayGroup import *
from User import *

class Workspace:

  number_of_instances = 0

  def __init__(self, NAME, TRANSMITTER_OFFSET):

    self.id = Workspace.number_of_instances
    Workspace.number_of_instances += 1

    self.name = NAME

    self.transmitter_offset = TRANSMITTER_OFFSET

    self.users = []

    self.display_groups = []

    self.size = (3.8, 3.6)

  def create_display_group( self
                          , INPUT_DEVICE_TYPE
                          , INPUT_DEVICE_NAME
                          , STARTING_MATRIX
                          , STARTING_SCALE
                          , MOVEMENT_TRACES
                          , INVERT
                          , NO_TRACKING_MAT
                          , GROUND_FOLLOWING_SETTINGS
                          , TRANSMITTER_OFFSET
                          , DISPLAY_LIST
                          , AVATAR_TYPE
                          , DEVICE_TRACKING_NAME = None):

    _dg = DisplayGroup()
    _dg.my_constructor( self
                       , len(self.display_groups)
                       , STARTING_MATRIX
                       , STARTING_SCALE
                       , INPUT_DEVICE_TYPE
                       , INPUT_DEVICE_NAME
                       , NO_TRACKING_MAT
                       , GROUND_FOLLOWING_SETTINGS
                       , MOVEMENT_TRACES
                       , INVERT
                       , TRANSMITTER_OFFSET
                       , DISPLAY_LIST
                       , AVATAR_TYPE
                       , False
                       , DEVICE_TRACKING_NAME)
    self.display_groups.append(_dg)



  def attach_display(self, DISPLAY_INSTANCE):

    self.display_group.append(DISPLAY_INSTANCE)

  def create_user( self
                 , VIP
                 , GLASSES_ID
                 , HEADTRACKING_TARGET_NAME
                 , EYE_DISTANCE
                 , ENABLE_BORDER_WARNINGS):
    
    _user = User()
    _user.my_constructor( self
                        , len(self.users)
                        , VIP
                        , GLASSES_ID
                        , HEADTRACKING_TARGET_NAME
                        , EYE_DISTANCE
                        , ENABLE_BORDER_WARNINGS)

    self.users.append(_user)