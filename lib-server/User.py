#!/usr/bin/python

## @file
# Contains class User.

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

## Internal representation of a user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates eyes
# and initializes the headtracking.

class User(avango.script.Script):

  ## @var mf_screen_pick_result
  # Intersections of the viewing ray with the screens in the setup.
  mf_screen_pick_result = avango.gua.MFPickResult()

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

    ## @var 
    # 
    # 
    self.use_display_group_navigation = [True for i in range(len(self.WORKSPACE_INSTANCE.display_groups))]

    ## @var matrices_per_platform
    # List of matrices for each platform to be used.
    # Can be either the group matrix or an individual one (switchable in use_group_navigation)
    self.matrices_per_display_group = [avango.gua.make_identity_mat() for i in range(len(self.WORKSPACE_INSTANCE.display_groups))]

    ##
    #
    self.navigation_nodes_per_display_group = []

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
    self.toggle_user_activity(self.is_active, False)

    # set evaluation policy
    self.always_evaluate(True)

  def add_navigation_node(self, NODE):
    self.navigation_nodes.append(NODE)

  ## 
  # 
  # 
  # 
  def individualize_display_group_nav(self, DISPLAY_GROUP_ID, NEW_TRANSFORM, NEW_SCALE):

    self.use_display_group_navigation[DISPLAY_GROUP_ID] = False
    self.matrices_per_platform[DISPLAY_GROUP_ID] = NEW_TRANSFORM
    self.scales_per_platform[DISPLAY_GROUP_ID] = NEW_SCALE

  ## Resets an individualized view back to the group view.
  def reset_view(self, DISPLAY_GROUP_ID):

    self.use_display_group_navigation[DISPLAY_GROUP_ID] = True

  ## Evaluated every frame.
  def evaluate(self):

    # update display group matrix array
    for _display_group_id in range(0, len(self.WORKSPACE_INSTANCE.display_groups)):

      if self.use_display_group_navigation[_display_group_id]:
        self.matrices_per_display_group[_display_group_id] = self.WORKSPACE_INSTANCE.display_groups[_display_group_id].sf_abs_mat.value * \
                                                             avango.gua.make_scale_mat(self.WORKSPACE_INSTANCE.display_groups[_display_group_id].sf_scale.value)
    
  ## Sets the user's active flag.
  # @param ACTIVE Boolean to which the active flag should be set.
  # @param RESEND_CONFIG Boolean indicating if the shutter configuration should be directly resent.
  def toggle_user_activity(self, ACTIVE, RESEND_CONFIG):

    if ACTIVE:
      self.is_active = True
    else:
      self.is_active = False