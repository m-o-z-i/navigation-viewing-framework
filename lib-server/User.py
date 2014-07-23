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
from display_config import INTELLIGENT_SHUTTER_SWITCHING
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
  # @param APPLICATION_MANAGER Reference to the ApplicationManager instance from which this user is created.
  # @param USER_ID Global user ID to be applied.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param GLASSES_ID ID of the shutter glasses worn by the user.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param HMD_SENSOR_NAME Name of the HMD sensor belonging to the user, if applicable.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param PLATFORM_ID Platform ID to which this user should be appended to.
  # @param ENABLE_BORDER_WARNINGS Boolean indicating if the user wants platform borders to be displayed.
  def my_constructor(self
                   , APPLICATION_MANAGER
                   , USER_ID
                   , VIP
                   , GLASSES_ID
                   , HEADTRACKING_TARGET_NAME
                   , HMD_SENSOR_NAME
                   , EYE_DISTANCE
                   , PLATFORM_ID
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
    ## @var APPLICATION_MANAGER
    # Reference to the ApplicationManager instance from which the user is created.
    self.APPLICATION_MANAGER = APPLICATION_MANAGER

    ## @var id
    # Identification number of the user, starting from 0.
    self.id = USER_ID

    ## @var platform_id
    # ID of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID

    ## @var platform
    # Instance of the platform the user is belonging to.
    self.platform = self.APPLICATION_MANAGER.navigation_list[self.platform_id].platform

    ## @var use_group_navigation
    # List of booleans saying if this user uses the navigation of the associated platform.
    # When False, an own matrix and own scaling can be provided.
    self.use_group_navigation = [True for i in range(len(self.APPLICATION_MANAGER.navigation_list))]

    ## @var matrices_per_platform
    # List of matrices for each platform to be used.
    # Can be either the group matrix or an individual one (switchable in use_group_navigation)
    self.matrices_per_platform = [avango.gua.make_identity_mat() for i in range(len(self.APPLICATION_MANAGER.navigation_list))]

    ## @var scales_per_platform
    # List of scalings for each platform to be used.
    # Can be either the group scaling or an individual one (switchable in use_group_navigation)
    self.scales_per_platform = [1.0 for i in range(len(self.APPLICATION_MANAGER.navigation_list))]

    ## @var current_display
    # Display instance on which the user physically is currently looking at.
    self.current_display = self.platform.displays[0]

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset   = self.platform.transmitter_offset

    ## @var no_tracking_mat
    # The matrix to be applied when no tracking is available.
    self.no_tracking_mat      = self.platform.no_tracking_mat

    ## @var enable_border_warnings
    # Boolean indicating if the user wants platform borders to be displayed.
    self.enable_border_warnings = ENABLE_BORDER_WARNINGS

    ## @var headtracking_target_name
    # Name of the headtracking station as registered in daemon.
    self.headtracking_target_name = HEADTRACKING_TARGET_NAME

    ## @var glasses_id
    # ID of the shutter glasses worn by the user. Used for frequency updates.
    self.glasses_id = GLASSES_ID

    ## @var headtracking_reader
    # Instance of a child class of TrackingReader to supply translation input.
    if self.current_display.stereomode == "HMD":

      # it is assumed that headtracking is present when using a HMD
      if HEADTRACKING_TARGET_NAME == None:
        print_error("Error: User " + str(self.id) + " is using a platform with HMD display, but has no headtracking target specified.", True)
      if HMD_SENSOR_NAME == None:
        print_error("Error: User " + str(self.id) + " is using a platform with HMD display, but has no HMD sensor name specified.", True)  

      self.headtracking_reader = TrackingHMDReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME, HMD_SENSOR_NAME)
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    elif HEADTRACKING_TARGET_NAME == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(self.no_tracking_mat)
    
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    # toggles avatar display and activity
    self.toggle_user_activity(self.is_active, False)

    # init intersection class for proxy geometry hit test

    ## @var pick_length
    # Length of the picking ray in meters to check for screen intersections.
    self.pick_length = 5.0

    ## @var intersection_tester
    # Instance of Intersection to determine intersection points of user with screens.
    self.intersection_tester = Intersection()
    self.intersection_tester.my_constructor(self.APPLICATION_MANAGER.SCENEGRAPH
                                          , self.headtracking_reader.sf_global_mat
                                          , self.pick_length
                                          , "screen_proxy_group")
    self.mf_screen_pick_result.connect_from(self.intersection_tester.mf_pick_result)

    ## @var looking_outside_start
    # If the user is not facing a screen, the start time of this behaviour is saved to open glasses after a certain amount of time.
    self.looking_outside_start = None

    ## @var open_threshold
    # Time in seconds after which shutter glasses should open when no screen is hit by the viewing ray.
    self.open_threshold = 2.0

    ## @var timer
    # Time sensor to handle time events.
    self.timer = avango.nodes.TimeSensor()

    # set evaluation policy
    self.always_evaluate(True)

  ## Sets an own (!= platform) transformation for this User instance.
  # @param PLATFORM_ID The platform id to individualize the view.
  # @param NEW_TRANSFORM The new transformation matrix of the user without scaling.
  # @param NEW_SCALE The new scaling factor to be applied.
  def individualize_view(self, PLATFORM_ID, NEW_TRANSFORM, NEW_SCALE):

    self.use_group_navigation[PLATFORM_ID] = False
    self.matrices_per_platform[PLATFORM_ID] = NEW_TRANSFORM
    self.scales_per_platform[PLATFORM_ID] = NEW_SCALE

  ## Resets an individualized view back to the group view.
  def reset_view(self, PLATFORM_ID):

    self.use_group_navigation[PLATFORM_ID] = True

  ## Evaluated every frame.
  def evaluate(self):

    # update platform matrix array
    for _platform_id in range(0, len(self.APPLICATION_MANAGER.navigation_list)):

      if self.use_group_navigation[_platform_id]:
        self.matrices_per_platform[_platform_id] = self.APPLICATION_MANAGER.navigation_list[_platform_id].platform.sf_abs_mat.value
        self.scales_per_platform[_platform_id] = self.APPLICATION_MANAGER.navigation_list[_platform_id].platform.sf_scale.value

    
    if INTELLIGENT_SHUTTER_SWITCHING:

      if len(self.mf_screen_pick_result.value) > 0:

        _hit = self.mf_screen_pick_result.value[0].Object.value.Name.value
        _hit = _hit.replace("proxy_", "")
        _hit = _hit.split("_")

        _hit_platform = int(_hit[0])
        _intended_platform = self.APPLICATION_MANAGER.navigation_list[_hit_platform].platform
        _hit_screen = int(_hit[1])
        _intended_display = _intended_platform.displays[_hit_screen]

        if _intended_display != self.current_display and \
           _hit_platform == self.platform_id:

          self.set_user_location(_hit_platform, _hit_screen, True)

      else:
        pass
      
      '''
      if len(self.mf_screen_pick_result.value) > 0:

        _hit = self.mf_screen_pick_result.value[0]
        _hit_name = _hit.Object.value.Name.value.replace("proxy_", "")
        _hit_name = _hit_name.split("_")

        _hit_platform = int(_hit_name[0])
        _hit_screen   = int(_hit_name[1])

        _intended_platform = self.APPLICATION_MANAGER.navigation_list[_hit_platform].platform
        _max_viewing_distance = _intended_platform.displays[_hit_screen].max_viewing_distance
        _distance_to_center = Tools.euclidean_distance(_hit.Object.value.Transform.value.get_translate()
                                                     , self.headtracking_reader.sf_global_mat.value.get_translate())
        _hit_distance = _hit.Distance.value * self.pick_length


        if _hit_platform != self.platform_id and \
           _hit_distance < _max_viewing_distance and \
           _distance_to_center < 1.0:

          if self.is_active == False:
            self.toggle_user_activity(True, True)

          # new intersection with other platform found in range

          self.set_user_location(_hit_platform, True)
          self.looking_outside_start = None

        elif _hit_distance > _max_viewing_distance:

          # intersection found but too far away

          if self.looking_outside_start == None:
            self.looking_outside_start = self.timer.Time.value

          if self.timer.Time.value - self.looking_outside_start > self.open_threshold:
            if self.is_active == True:
              self.toggle_user_activity(False, True)

      else:

        # no intersection found

        if self.looking_outside_start == None:
          self.looking_outside_start = self.timer.Time.value

        if self.timer.Time.value - self.looking_outside_start > self.open_threshold:
          if self.is_active == True:
            #print_message("Opening user")
            self.toggle_user_activity(False, True)
      '''
      

  ## Sets the user's active flag.
  # @param ACTIVE Boolean to which the active flag should be set.
  # @param RESEND_CONFIG Boolean indicating if the shutter configuration should be directly resent.
  def toggle_user_activity(self, ACTIVE, RESEND_CONFIG):

    if ACTIVE:
      self.is_active = True
    else:
      self.is_active = False
      self.platform_id = -1

    if RESEND_CONFIG:
      self.APPLICATION_MANAGER.slot_manager.update_slot_configuration()

  ## Changes the user's current platform.
  # @param PLATFORM_ID The new platform id to be set.
  # @param SCREEN_ID The new screen id to be set.
  # @param RESEND_CONFIG Boolean indicating if the shutter configuration should be directly resent.
  def set_user_location(self, PLATFORM_ID, SCREEN_ID, RESEND_CONFIG):

    _intended_platform = self.APPLICATION_MANAGER.navigation_list[PLATFORM_ID].platform
    _intended_display = _intended_platform.displays[SCREEN_ID]

    if self.APPLICATION_MANAGER.slot_manager.display_has_free_slot(_intended_display):

      self.platform_id = PLATFORM_ID
      self.platform = _intended_platform
      self.current_display = _intended_display

      self.transmitter_offset = self.platform.transmitter_offset
      self.no_tracking_mat = self.platform.no_tracking_mat
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)

      if RESEND_CONFIG:
        self.APPLICATION_MANAGER.slot_manager.update_slot_configuration()

    else:
      print_warning("Blocked")