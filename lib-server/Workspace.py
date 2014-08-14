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

## Representation of the physical space holding several users, tools and display groups.
class Workspace:

  ## @var number_of_instances
  # Number of Workspace instances that have already been created. Used for assigning correct IDs.
  number_of_instances = 0

  ## Custom constructor.
  # @param NAME Name of the Workspace to be created.
  # @param TRANSMITTER_OFFSET Transmitter offset to be applied within this workspace.
  def __init__(self, NAME, TRANSMITTER_OFFSET):

    ## @var id
    # Identification number of this workspace.
    self.id = Workspace.number_of_instances
    Workspace.number_of_instances += 1

    # @var name
    # Name of this Workspace.
    self.name = NAME

    ## @var transmitter_offset
    # Transmitter offset to be applied within this workspace.
    self.transmitter_offset = TRANSMITTER_OFFSET

    ## @var users
    # List of users that are active within this workspace.
    self.users = []

    ## @var display_groups
    # List of DisplayGroups present within this workspace.
    self.display_groups = []

    ## @var size
    # Physical size of this workspace in meters.
    self.size = (3.8, 3.6)

  ## Creates a DisplayGroup instance and adds it to this workspace.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assiged to the display group.
  # @param OFFSET_TO_WORKSPACE Offset describing the origin of this display group with respect to the origin of the workspace.
  def create_display_group( self
                          , DISPLAY_LIST
                          , NAVIGATION_LIST
                          , OFFSET_TO_WORKSPACE):

    _dg = DisplayGroup(len(self.display_groups), DISPLAY_LIST, NAVIGATION_LIST, OFFSET_TO_WORKSPACE, self.transmitter_offset)
    self.display_groups.append(_dg)

  ## Creates a User instance and adds it to this workspace.
  # To be called after all display groups have been created.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param GLASSES_ID ID of the shutter glasses worn by the user.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied when HEADTRACKING_TARGET_NAME is None.
  def create_user( self
                 , VIP
                 , GLASSES_ID
                 , HEADTRACKING_TARGET_NAME
                 , EYE_DISTANCE
                 , NO_TRACKING_MAT = avango.gua.make_trans_mat(0,0,0)):
    
    _user = User()
    _user.my_constructor( self
                        , len(self.users)
                        , VIP
                        , GLASSES_ID
                        , HEADTRACKING_TARGET_NAME
                        , EYE_DISTANCE
                        , NO_TRACKING_MAT)

    self.users.append(_user)