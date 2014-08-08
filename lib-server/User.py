#!/usr/bin/python

## @file
# Contains classes User and UserRepresentation.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Intersection import *
from TrackingReader import *
from ConsoleIO import *
import Tools

# import math libraries
import math

class UserRepresentation:

  def __init__(self, NODE, DISPLAY_GROUP):

    self.NODE = NODE

    self.DISPLAY_GROUP = DISPLAY_GROUP

    self.connect_navigation_of_display_group(0)

  def connect_navigation_of_display_group(self, ID):

    if ID < len(self.DISPLAY_GROUP.navigations):
      self.NODE.Transform.disconnect()
      self.NODE.Transform.connect_from(self.DISPLAY_GROUP.navigations[ID].sf_nav_mat)
    else:
      print_error("Error. Navigation ID does not exist.", False)


class User(avango.script.Script):

  ## Default constructor.
  def __init__(self):
    self.super(User).__init__()

  ## Custom constructor.
  # @param WORKSPACE_INSTANCE Workspace instance in which this user is active.
  # @param USER_ID Global user ID to be applied.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param GLASSES_ID ID of the shutter glasses worn by the user.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param PLATFORM_ID Platform ID to which this user should be appended to.
  # @param ENABLE_BORDER_WARNINGS Boolean indicating if the user wants platform borders to be displayed.
  def my_constructor(self
                   , WORKSPACE_INSTANCE
                   , USER_ID
                   , VIP
                   , GLASSES_ID
                   , HEADTRACKING_TARGET_NAME
                   , EYE_DISTANCE
                   , ENABLE_BORDER_WARNINGS
                   ):

    # flags 
    ## @var is_vip
    # Boolean indicating if this user has vip status.
    self.is_vip = VIP

    ## @var is_active
    # Boolean indicating if this user is currently active.
    self.is_active = True

    ## @var eye_distance
    # The eye distance of the user to be applied.
    self.eye_distance = EYE_DISTANCE

    # variables
    ## @var WORKSPACE_INSTANCE
    # Workspace instance in which this user is active.
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ## @var id
    # Identification number of the user, starting from 0.
    self.id = USER_ID

    ##
    #
    self.matrices_per_display_group = [avango.gua.nodes.TransformNode() for i in range(len(self.WORKSPACE_INSTANCE.display_groups))]

    ## 
    # 
    self.user_representations = [UserRepresentation(self.matrices_per_display_group[i], self.WORKSPACE_INSTANCE.display_groups[i]) for i in range(len(self.WORKSPACE_INSTANCE.display_groups))]


    ## @var enable_border_warnings
    # Boolean indicating if the user wants platform borders to be displayed.
    self.enable_border_warnings = ENABLE_BORDER_WARNINGS

    ## @var headtracking_target_name
    # Name of the headtracking station as registered in daemon.
    self.headtracking_target_name = HEADTRACKING_TARGET_NAME

    ## @var glasses_id
    # ID of the shutter glasses worn by the user. Used for frequency updates.
    self.glasses_id = GLASSES_ID

    self.headtracking_reader = TrackingTargetReader()
    self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
    self.headtracking_reader.set_transmitter_offset(self.WORKSPACE_INSTANCE.transmitter_offset)
    self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    # toggles avatar display and activity
    self.toggle_user_activity(self.is_active)

    # set evaluation policy
    self.always_evaluate(True)

  def switch_navigation_at_display_group(self, DISPLAY_GROUP_ID, NAVIGATION_ID):
    
    if DISPLAY_GROUP_ID < len(self.user_representations):
      self.user_representations[DISPLAY_GROUP_ID].connect_navigation_of_display_group(NAVIGATION_ID)
    else:
      print_error("Error. Display Group ID does not exist.", False)


  ## Evaluated every frame.
  def evaluate(self):

    pass
    
  ## Sets the user's active flag.
  # @param ACTIVE Boolean to which the active flag should be set.
  def toggle_user_activity(self, ACTIVE):

    if ACTIVE:
      self.is_active = True
    else:
      self.is_active = False