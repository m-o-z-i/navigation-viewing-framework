#!/usr/bin/python

## @file
# Contains class Navigation.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
from Device           import *
from GroundFollowing  import GroundFollowing
from InputMapping     import InputMapping
from Platform         import Platform
import Tools
import TraceLines

# import python libraries
import math
import random

## Wrapper class to create an input Device, a GroundFollowing instance, an InputMapping and a Platform.
#
# Furthermore, this class reacts on the device's button inputs and toggles the 3-DOF (realistic) / 6-DOF (unrealistic) 
# navigation mode. When switching from unrealistic to realistic mode, an animation is triggered in which the platform
# is rotated back in an upright position (removal of pitch and roll angle). It also handles couplings and their animations
# with other Navigation instances. Apart from that, it uses the class Trace to draw lines representing its past movements.

class Navigation(avango.script.Script):

  # input fields
  ## @var sf_reset_trigger
  # Boolean field to indicate if the platform is to be reset.
  sf_reset_trigger = avango.SFBool()

  ## @var sf_coupling_trigger
  # Boolean field to indicate if the coupling mechanism is to be triggered.
  sf_coupling_trigger = avango.SFBool()

  ## @var sf_dof_trigger
  # Boolean field to indicate if the change of the dof mode is to be triggered.
  sf_dof_trigger = avango.SFBool()  

  # static class variables
  ## @var trace_materials
  # List of material pretexts to choose from when a trace is created. All avatars on this
  # platform will have this material.
  trace_materials = ['AvatarBlue', 'AvatarCyan', 'AvatarGreen', 'AvatarMagenta', 'AvatarDarkGreen',
                     'AvatarOrange', 'AvatarRed', 'AvatarWhite', 'AvatarYellow', 'AvatarGrey']

  ## @var material_used
  # List of booleans to indicate if a material in trace_materials was already used.
  material_used = [False, False, False, False, False,
                   False, False, False, False, False]

  ## Default constructor.
  def __init__(self):
    self.super(Navigation).__init__()

    # if every material has already been used, reset the pool
    _reset_pool = True

    for _boolean in Navigation.material_used:
      if _boolean == False:
        _reset_pool = False
        break

    if _reset_pool:
      Navigation.material_used = [False, False, False, False, False, False, False, False, False, False]

    # get a random material from the pool of materials
    _random_material_number = random.randint(0, len(Navigation.trace_materials) - 1)
 
    # if the material is already used, go further until the first unused one is found
    while Navigation.material_used[_random_material_number] == True:
      _random_material_number = (_random_material_number + 1) % len(Navigation.material_used)

    # get the selected material 
    ## @var trace_material
    # The material to be used for the movement traces.
    self.trace_material = Navigation.trace_materials[_random_material_number]
    Navigation.material_used[_random_material_number] = True

  ## Custom constructor.
  # @param NET_TRANS_NODE Reference to the net matrix node in the scenegraph for distribution.
  # @param SCENEGRAPH Reference to the scenegraph in which the navigation should take place.
  # @param PLATFORM_SIZE Physical size of the platform in meters. Passed in an two-element list: [width, depth]
  # @param SCALE Start scaling of the platform.
  # @param STARTING_MATRIX Initial position matrix of the platform to be created.
  # @param NAVIGATION_LIST List of all navigations in the setup.
  # @param INPUT_SENSOR_TYPE String indicating the type of input device to be created, e.g. "XBoxController" or "OldSpheron"
  # @param INPUT_SENSOR_NAME Name of the input device sensor as chosen in daemon.
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  # @param GF_SETTINGS Setting list for the GroundFollowing instance: [activated, ray_start_height]
  # @param ANIMATE_COUPLING Boolean indicating if an animation should be done when a coupling of navigations is initiated.
  # @param MOVEMENT_TRACES Boolean indicating if the device should leave traces behind.
  # @param INVERT Boolean indicating if the input values should be inverted.
  # @param SLOT_MANAGER Reference to the one and only SlotManager instance in the setup.
  # @param TRANSMITTER_OFFSET The matrix offset that is applied to the values delivered by the tracking system.
  # @param DISPLAYS The names of the displays that belong to this navigation.
  # @param AVATAR_TYPE A string that determines what kind of avatar representation is to be used ["joseph", "joseph_table", "kinect"].
  # @param CONFIG_FILE The path to the config file that is used.
  # @param START_CLIENTS Boolean saying if the client processes are to be started automatically.
  # @param TRACKING_TARGET_NAME Name of the device's tracking target name as chosen in daemon.
  def my_constructor(
      self
    , NET_TRANS_NODE
    , SCENEGRAPH
    , PLATFORM_SIZE
    , SCALE
    , STARTING_MATRIX
    , NAVIGATION_LIST
    , INPUT_SENSOR_TYPE
    , INPUT_SENSOR_NAME
    , NO_TRACKING_MAT
    , GF_SETTINGS
    , ANIMATE_COUPLING
    , MOVEMENT_TRACES
    , INVERT
    , SLOT_MANAGER
    , TRANSMITTER_OFFSET
    , DISPLAYS
    , AVATAR_TYPE
    , CONFIG_FILE
    , START_CLIENTS
    , TRACKING_TARGET_NAME = None
    ):
    
    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var NET_TRANS_NODE
    # Reference to the net matrix node in the scenegraph for distribution.
    self.NET_TRANS_NODE = NET_TRANS_NODE

    ## @var coupled_navigations
    # List of coupled Navigation instances to which this Navigation's changes are forwarded to.
    self.coupled_navigations = []

    ## @var input_sensor_type
    # String indicating the type of input device to be created, e.g. "XBoxController" or "OldSpheron"
    self.input_sensor_type = INPUT_SENSOR_TYPE

    ## @var input_sensor_name
    # Name of the input device sensor as chosen in daemon.
    self.input_sensor_name = INPUT_SENSOR_NAME

    if self.input_sensor_name == None:
      self.input_sensor_name = "keyboard"

    ## @var start_matrix
    # Initial position matrix of the platform.
    self.start_matrix = STARTING_MATRIX

    ## @var start_scale
    # Initial scaling factor of the platform.
    self.start_scale = SCALE
    
    # create device
    ## @var device
    # Device instance handling relative inputs of physical device.
    if self.input_sensor_type == "OldSpheron":
      self.device = OldSpheronDevice()
      self.device.my_constructor(INPUT_SENSOR_NAME, TRACKING_TARGET_NAME, NO_TRACKING_MAT)
    elif self.input_sensor_type == "NewSpheron":
      self.device = NewSpheronDevice()
      self.device.my_constructor(INPUT_SENSOR_NAME, TRACKING_TARGET_NAME, NO_TRACKING_MAT)
    elif self.input_sensor_type == "XBoxController":
      self.device = XBoxDevice()
      self.device.my_constructor(INPUT_SENSOR_NAME, TRACKING_TARGET_NAME, NO_TRACKING_MAT)
    elif self.input_sensor_type == "KeyboardMouse":
      self.device = KeyboardMouseDevice()
      self.device.my_constructor(NO_TRACKING_MAT)
    elif self.input_sensor_type == "Spacemouse":
      self.device = SpacemouseDevice()
      self.device.my_constructor(INPUT_SENSOR_NAME, NO_TRACKING_MAT)
    elif self.input_sensor_type == "Globefish":
      self.device = GlobefishDevice()
      self.device.my_constructor(INPUT_SENSOR_NAME, NO_TRACKING_MAT)


    # init field connections
    self.sf_reset_trigger.connect_from(self.device.sf_reset_trigger)
    self.sf_coupling_trigger.connect_from(self.device.sf_coupling_trigger)
    self.sf_dof_trigger.connect_from(self.device.sf_dof_trigger)
    
    # create ground following
    ## @var groundfollowing
    # GroundFollowing instance to correct the absolute matrices with respect to gravity.
    self.groundfollowing = GroundFollowing()
    self.groundfollowing.my_constructor(self.SCENEGRAPH, self.device.sf_station_mat, float(GF_SETTINGS[1]))

    # create input mapping
    ## @var inputmapping
    # InputMapping instance to process and map relative device inputs to an absolute matrix.
    self.inputmapping = InputMapping()
    self.inputmapping.my_constructor(self, self.device, self.groundfollowing, STARTING_MATRIX, INVERT)
    self.inputmapping.set_input_factors(self.device.translation_factor, self.device.rotation_factor)
    self.inputmapping.sf_scale.value = SCALE

    # activate correct input mapping mode according to configuration file
    if GF_SETTINGS[0]:
      self.inputmapping.activate_realistic_mode()
    else:
      self.inputmapping.deactivate_realistic_mode()

    # create platform
    ## @var platform
    # Platform instance that is controlled by the Device.
    self.platform = Platform()
    self.platform.my_constructor(
        NET_TRANS_NODE = self.NET_TRANS_NODE
      , SCENEGRAPH = self.SCENEGRAPH
      , PLATFORM_SIZE = PLATFORM_SIZE
      , INPUT_MAPPING_INSTANCE = self.inputmapping
      , PLATFORM_ID = len(NAVIGATION_LIST)
      , TRANSMITTER_OFFSET = TRANSMITTER_OFFSET
      , NO_TRACKING_MAT = NO_TRACKING_MAT
      , DISPLAYS = DISPLAYS
      , AVATAR_TYPE = AVATAR_TYPE
      , SLOT_MANAGER = SLOT_MANAGER
      , CONFIG_FILE = CONFIG_FILE
      , AVATAR_MATERIAL = self.trace_material
      , START_CLIENTS = START_CLIENTS
      )

    # create device avatar
    #if AVATAR_TYPE != "None" and AVATAR_TYPE.endswith(".ks") == False:
    #  self.device.create_device_avatar(self.platform.platform_scale_transform_node
    #                                 , self.platform.platform_id)

    ## @var NAVIGATION_LIST
    # Reference to a list containing all Navigation instances in the setup.
    self.NAVIGATION_LIST = NAVIGATION_LIST

    # attributes
    ## @var in_dofchange_animation
    # Boolean variable to indicate if a movement animation for a DOF change (realistic/unrealistic) is in progress.
    self.in_dofchange_animation = False

    ## @var in_coupling_animation
    # Boolean variable to indicate if a movement animation for coupling is in progress.
    self.in_coupling_animation = False

    ## @var timer
    # Instance of TimeSensor to handle the duration of animations.
    self.timer = avango.nodes.TimeSensor()

    ## @var ANIMATE_COUPLING
    # Boolean indicating if an animation should be done when a coupling of navigations is initiated.
    self.ANIMATE_COUPLING = ANIMATE_COUPLING

    ## @var movement_traces
    # Boolean indicating if the movement traces are currently visualized by line segments.
    self.movement_traces = MOVEMENT_TRACES

    ## @var movement_traces_activated
    # Boolean indicating if the movement traces are generally activated.
    self.movement_traces_activated = self.movement_traces

    ## @var trace
    # The trace class that handles the line segment updating.
    self.trace = None

    if self.movement_traces:
      # create trace and add 'Shadeless' to material string to have a nicer line apperance
      ## @var trace
      # Instance of Trace class to handle trace drawing of this navigation's movements.
      self.trace = TraceLines.Trace(self.NET_TRANS_NODE, self.platform.platform_id, 500, 50.0, STARTING_MATRIX, self.trace_material + 'Shadeless')    

    # evaluate every frame
    self.always_evaluate(True)

  ## Resets the platform's matrix to the initial value.
  def reset(self):
    self.inputmapping.set_abs_mat(self.start_matrix)
    self.inputmapping.set_scale(self.start_scale)

    if self.movement_traces_activated:
      self.trace.clear(self.start_matrix)

  ## Activates 3-DOF (realistic) navigation mode.
  def activate_realistic_mode(self):

    # remove pitch and roll from current orientation
    _current_mat = self.platform.sf_abs_mat.value
    _current_trans = _current_mat.get_translate()
    _current_yaw = Tools.get_yaw(_current_mat)

    ## @var start_rot
    # Quaternion representing the start rotation of the animation
    self.start_rot = self.platform.sf_abs_mat.value.get_rotate()

    ## @var target_rot
    # Quaternion representing the target rotation of the animation
    self.target_rot = avango.gua.make_rot_mat(math.degrees(_current_yaw), 0, 1, 0).get_rotate()

    ## @var animation_time
    # Time of the rotation animation in relation to the rotation distance.
    self.animation_time = 2 * math.sqrt(math.pow(self.start_rot.x - self.target_rot.x, 2) \
      + math.pow(self.start_rot.y - self.target_rot.y, 2) \
      + math.pow(self.start_rot.z - self.target_rot.z, 2) \
      + math.pow(self.start_rot.w - self.target_rot.w, 2))
   
    # if no animation is needed, set animation time to a minimum value to avoid division by zero
    if self.animation_time == 0.0:
      self.animation_time = 0.01

    ## @var start_trans
    # Starting translation vector of the animation.
    self.start_trans = _current_trans

    ## @var animation_start_time
    # Point in time where the animation started.
    self.animation_start_time = self.timer.Time.value
 
    self.in_dofchange_animation = True                       
  
  ## Animates the removal of pitch and roll angles when switching from 6-DOF (unrealistic) to 3-DOF (realistic) navigation mode.
  def animate_dofchange(self):

    _current_time = self.timer.Time.value
    _slerp_ratio = (_current_time - self.animation_start_time) / self.animation_time

    # when end of animation is reached
    if _slerp_ratio > 1:
      _slerp_ratio = 1
      self.in_dofchange_animation = False
      self.inputmapping.activate_realistic_mode()

    # compute slerp position and set it on the player's inputmapping
    _transformed_quat = self.start_rot.slerp_to(self.target_rot, _slerp_ratio)

    _position_yaw_mat = avango.gua.make_trans_mat(self.start_trans.x, self.start_trans.y, self.start_trans.z) * \
                        avango.gua.make_rot_mat(_transformed_quat)

    self.inputmapping.set_abs_mat(_position_yaw_mat)

  ## Activates 6-DOF (unrealistic) navigation mode.
  def deactivate_realistic_mode(self):
    self.inputmapping.deactivate_realistic_mode()

  ## Bidirectional coupling of this and another navigation.
  # @param NAVIGATION The Navigation to be coupled.
  def couple_navigation(self, NAVIGATION):

    # write navigation to be coupled in the list of coupled navigations on all coupled navigations
    if not ((NAVIGATION in self.coupled_navigations) or (self in NAVIGATION.coupled_navigations)):
      for _nav in self.coupled_navigations:
        if not (NAVIGATION in _nav.coupled_navigations):
          _nav.coupled_navigations.append(NAVIGATION)
        if not (_nav in NAVIGATION.coupled_navigations):
          NAVIGATION.coupled_navigations.append(_nav)
      for _nav in NAVIGATION.coupled_navigations:
        if not (self in _nav.coupled_navigations):
          _nav.coupled_navigations.append(self)
        if not (_nav in self.coupled_navigations):
          self.coupled_navigations.append(_nav)
      self.coupled_navigations.append(NAVIGATION)
      NAVIGATION.coupled_navigations.append(self)

      # if one of the navigations is in unrealistic (6 dof) mode, switch the other one to unrealistic as well
      if self.inputmapping.realistic == False and NAVIGATION.inputmapping.realistic == True:
        NAVIGATION.deactivate_realistic_mode()
      elif self.inputmapping.realistic == True and NAVIGATION.inputmapping.realistic == False:
        self.deactivate_realistic_mode()


  ## Bidirectional decoupling of this and another navigation.
  # @param NAVIGATION The Navigation to be decoupled.
  def decouple_navigation(self, NAVIGATION):
    if NAVIGATION in self.coupled_navigations:
      self.coupled_navigations.remove(NAVIGATION)
      NAVIGATION.coupled_navigations.remove(self)

  ## Triggers the coupling mechanism.
  # When other platforms are close enough, they are coupled to each other.
  def trigger_coupling(self):
    
    # list containing the navigataions close enough to couple
    _close_navs = []

    # threshold when two navigations should be considered for coupling (distance in meter)
    _threshold = 7.0
    
    # compute center position of own platform
    _position_self = (self.platform.sf_abs_mat.value * self.device.sf_station_mat.value).get_translate()

    # check for all navigations in the setup
    for _nav in self.NAVIGATION_LIST:
      
      # compute center position of currently iterated platform
      _position_nav = (_nav.platform.sf_abs_mat.value * _nav.device.sf_station_mat.value).get_translate()

      # append navigation to the list of close ones if distance is smaller than a threshold
      if _nav != self and \
         Tools.euclidean_distance(_position_self, _position_nav) < _threshold and \
         _nav.platform.sf_scale.value == self.platform.sf_scale.value:
        _close_navs.append(_nav)

    # sort list of close navs, highest distance first
    _close_navs.sort(key = lambda _nav: Tools.euclidean_distance(_position_self,
      (_nav.platform.sf_abs_mat.value * _nav.device.sf_station_mat.value).get_translate()),
      reverse = True)

    if len(_close_navs) > 0:
      if self.movement_traces_activated:
        _mat = self.get_current_world_pos()
        self.trace.clear(_mat)

      # couple the close navigations
      for _nav in _close_navs:
        self.couple_navigation(_nav)
        
        # clear movement traces
        if _nav.movement_traces_activated:
          _mat = _nav.get_current_world_pos()
          _nav.trace.clear(_mat)
          _nav.movement_traces = False

      if self.ANIMATE_COUPLING:
        # do an animation to closest navigation if this functionality is switched on
        _nav_animation_target = _close_navs[-1]
        
        self.set_coupling_animation_settings(_nav_animation_target)
        self.inputmapping.blocked = True
        self.platform.show_coupling_plane()
   
        for i in range(len(_close_navs)):
          _close_navs[i].set_coupling_animation_settings(_nav_animation_target)
          _close_navs[i].inputmapping.blocked = True
          _close_navs[i].platform.show_coupling_plane()

      # notify users
      _all_coupled_navs = list(self.coupled_navigations)
      _all_coupled_navs.append(self)

      for _nav in _all_coupled_navs:
        _nav.platform.display_coupling(_all_coupled_navs)

    else:
      print "No platform in range for coupling."

  
  ## Sets all the necessary attributes to perform a lerp and slerp animation to another navigation.
  # @param TARGET_NAVIGATION The Navigation instance to animate to.
  def set_coupling_animation_settings(self, TARGET_NAVIGATION):

    # determine start and target rotation and translation
    self.start_rot = self.platform.sf_abs_mat.value.get_rotate()
    self.start_trans = self.platform.sf_abs_mat.value.get_translate()

    _start_rot_center_mat = self.platform.sf_abs_mat.value * self.device.sf_station_mat.value
    _target_rot_center_mat = TARGET_NAVIGATION.platform.sf_abs_mat.value * TARGET_NAVIGATION.device.sf_station_mat.value

    _difference_vector = _target_rot_center_mat.get_translate() - _start_rot_center_mat.get_translate()
    _difference_vector.y = 0.0

    # it turned out that slerping rotation does not look that nice
    # can be changed by switching comments in the two lines below
    self.target_rot = self.start_rot
    #self.target_rot = avango.gua.make_rot_mat(math.degrees(Tools.get_yaw(_target_rot_center_mat)), 0, 1, 0).get_rotate()

    ## @var target_trans
    # The current animation's target translation.
    self.target_trans = self.start_trans + _difference_vector

    ## @var target_navigation
    # Reference to the target Navigation instance used in coupling animations. Used for updating target_trans when the rotation center moves.
    self.target_navigation = TARGET_NAVIGATION

    ## @var start_rot_center_mat
    # Matrix representing the transformation of the start navigation's rotation center (used for coupling animation purposes).
    self.start_rot_center_mat = _start_rot_center_mat

    self.animation_time = 0.5 * math.sqrt(math.pow(self.start_trans.x - self.target_trans.x, 2) \
      + math.pow(self.start_trans.y - self.target_trans.y, 2) + math.pow(self.start_trans.z - self.target_trans.z, 2)) \
      + math.sqrt(math.pow(self.start_rot.x - self.target_rot.x, 2) + math.pow(self.start_rot.y - self.target_rot.y, 2) \
      + math.pow(self.start_rot.z - self.target_rot.z, 2) + math.pow(self.start_rot.w - self.target_rot.w, 2))

    # if no animation is needed, set animation time to a minimum value to avoid division by zero
    if self.animation_time == 0.0:
      self.animation_time = 0.01

    self.animation_start_time = self.timer.Time.value
    self.in_coupling_animation = True

  ## Animates the movement to another platform during the coupling process.
  def animate_coupling(self):
    
    _current_time = self.timer.Time.value
    _animation_ratio = (_current_time - self.animation_start_time) / self.animation_time

    # recompute target_trans in case the rotation center moves
    _target_rot_center_mat = self.target_navigation.platform.sf_abs_mat.value * self.target_navigation.device.sf_station_mat.value
    _difference_vector = _target_rot_center_mat.get_translate() - self.start_rot_center_mat.get_translate()
    _difference_vector.y = 0.0
    self.target_trans = self.start_trans + _difference_vector
    
    # when end of animation is reached
    if _animation_ratio > 1:
      _animation_ratio = 1
      self.in_coupling_animation = False

      # clear blockings when all coupling animations are done
      _clear_blockings = True
      for _nav in self.coupled_navigations:
        if _nav.in_coupling_animation == True:
          _clear_blockings = False
          break

      if _clear_blockings:
        self.inputmapping.blocked = False
        self.platform.hide_coupling_plane()
        for _nav in self.coupled_navigations:
          _nav.inputmapping.blocked = False
          _nav.platform.hide_coupling_plane()

    # compute slerp and lerp position and set it on the player's inputmapping
    _transformed_quat = self.start_rot.slerp_to(self.target_rot, _animation_ratio)
    _transformed_vec = self.start_trans.lerp_to(self.target_trans, _animation_ratio)

    _animation_mat = avango.gua.make_trans_mat(_transformed_vec.x, _transformed_vec.y, _transformed_vec.z) * \
                     avango.gua.make_rot_mat(_transformed_quat)

    self.inputmapping.set_abs_mat(_animation_mat)
  
  ## Decouples this Navigation from all coupled Navigations.
  def clear_couplings(self):

    if len(self.coupled_navigations) > 0:
      # create hard copy of coupled navigations
      _couplings = list(self.coupled_navigations)

      if self.movement_traces_activated:
        self.movement_traces = True
        _mat = self.get_current_world_pos()
        self.trace.clear(_mat)

        if len(_couplings) == 1:
          _couplings[0].movement_traces = True
          _mat = _couplings[0].get_current_world_pos()
          _couplings[0].trace.clear(_mat)

      # iterate over all navigations and clear the coupling
      for _nav in _couplings:
        _nav.decouple_navigation(self)
        _nav.platform.remove_from_coupling_display(self, True)
        self.platform.remove_from_coupling_display(_nav, False)

      self.coupled_navigations = []

  ## Switches from realistic to unrealistic or from unrealistic to realistic mode on this
  # and all other coupled instances.
  def trigger_dofchange(self):

    # if in realistic mode, switch to unrealistic mode
    if self.inputmapping.realistic == True:
      #print "GF off"
      self.deactivate_realistic_mode()
      for _navigation in self.coupled_navigations:
        _navigation.deactivate_realistic_mode()
    
    # if in unrealistic mode, switch to realistic mode
    else:
      #print "GF on"
      self.activate_realistic_mode()
      for _navigation in self.coupled_navigations:
        _navigation.activate_realistic_mode()

  ## Computes the current world position of the rotation center on the platform ground (y = 0).
  def get_current_world_pos(self):
    _station_trans = self.device.sf_station_mat.value.get_translate()
    _mat = self.platform.sf_abs_mat.value * avango.gua.make_trans_mat(avango.gua.Vec3(_station_trans.x, 0, _station_trans.z) * self.platform.sf_scale.value)
    return _mat
  
  ## Evaluated every frame.
  def evaluate(self):

    # handle visibilities
    if self.ANIMATE_COUPLING:
      self.platform.platform_transform_node.GroupNames.value = []
      for _nav in self.coupled_navigations:
        self.platform.platform_transform_node.GroupNames.value.append("couple_group_" + str(_nav.platform.platform_id))

    # handle dofchange animation
    if self.in_dofchange_animation:
      self.animate_dofchange()

    # handle coupling animation
    elif self.in_coupling_animation:
      self.animate_coupling()

    # draw the traces if enabled
    if self.movement_traces:
      _mat = self.get_current_world_pos()
      self.trace.update(_mat)


  ## Evaluated when value changes.
  @field_has_changed(sf_reset_trigger)
  def sf_reset_trigger_changed(self):
  
    if self.sf_reset_trigger.value == True: # button pressed
      #print "RESET"
      self.reset()
      for _navigation in self.coupled_navigations:
          _navigation.reset()


  ## Evaluated when value changes.
  @field_has_changed(sf_coupling_trigger)
  def sf_coupling_trigger_changed(self):
  
    if self.sf_coupling_trigger.value == True: # button pressed

      if self.in_coupling_animation == False: 
        if len(self.coupled_navigations) == 0:
          self.trigger_coupling()
        else:
          self.clear_couplings()           
          

  ## Evaluated when value changes.
  @field_has_changed(sf_dof_trigger)
  def sf_dof_trigger_changed(self):
  
    if self.sf_dof_trigger.value == True: # button pressed

      if self.in_dofchange_animation == False:
         self.trigger_dofchange()
    
         
