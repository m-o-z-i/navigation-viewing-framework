#!/usr/bin/python

## @file
# Contains class DisplayGroup.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
from Device           import *
from GroundFollowing  import *
from InputMapping     import InputMapping
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

class DisplayGroup(avango.script.Script):

  # output fields
  ## @var sf_abs_mat
  # Matrix representing the current translation and rotation of the platform in the scene.
  sf_abs_mat = avango.gua.SFMatrix4()
  sf_abs_mat.value = avango.gua.make_identity_mat()

  ## @var sf_scale
  # The current scaling factor of this platform.
  sf_scale = avango.SFFloat()
  sf_scale.value = 1.0

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
    self.super(DisplayGroup).__init__()

    # if every material has already been used, reset the pool
    _reset_pool = True

    for _boolean in DisplayGroup.material_used:
      if _boolean == False:
        _reset_pool = False
        break

    if _reset_pool:
      DisplayGroup.material_used = [False, False, False, False, False, False, False, False, False, False]

    # get a random material from the pool of materials
    _random_material_number = random.randint(0, len(DisplayGroup.trace_materials) - 1)
 
    # if the material is already used, go further until the first unused one is found
    while DisplayGroup.material_used[_random_material_number] == True:
      _random_material_number = (_random_material_number + 1) % len(DisplayGroup.material_used)

    # get the selected material 
    ## @var trace_material
    # The material to be used for the movement traces.
    self.trace_material = DisplayGroup.trace_materials[_random_material_number]
    DisplayGroup.material_used[_random_material_number] = True

  ## Custom constructor.
  # @param WORKSPACE_INSTANCE Workspace instance in which this user is active.
  # @param STARTING_MATRIX Initial position matrix of the platform to be created.
  # @param STARTING_SCALE Start scaling of the platform.
  # @param INPUT_DEVICE_TYPE String indicating the type of input device to be created, e.g. "XBoxController" or "OldSpheron"
  # @param INPUT_DEVICE_NAME Name of the input device sensor as chosen in daemon.
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  # @param GF_SETTINGS Setting list for the GroundFollowing instance: [activated, ray_start_height]
  # @param ANIMATE_COUPLING Boolean indicating if an animation should be done when a coupling of navigations is initiated.
  # @param MOVEMENT_TRACES Boolean indicating if the device should leave traces behind.
  # @param INVERT Boolean indicating if the input values should be inverted.
  # @param SLOT_MANAGER Reference to the one and only SlotManager instance in the setup.
  # @param TRANSMITTER_OFFSET The matrix offset that is applied to the values delivered by the tracking system.
  # @param DISPLAY_LIST A list of Display instances that belong to this Navigation.
  # @param AVATAR_TYPE A string that determines what kind of avatar representation is to be used ["joseph", "joseph_table", "kinect"].
  # @param CONFIG_FILE The path to the config file that is used.
  # @param START_CLIENTS Boolean saying if the client processes are to be started automatically.
  # @param TRACKING_TARGET_NAME Name of the device's tracking target name as chosen in daemon.
  def my_constructor(
      self
    , WORKSPACE_INSTANCE
    , ID
    , STARTING_MATRIX
    , STARTING_SCALE
    , INPUT_DEVICE_TYPE
    , INPUT_DEVICE_NAME
    , NO_TRACKING_MAT
    , GF_SETTINGS
    , MOVEMENT_TRACES
    , INVERT
    , TRANSMITTER_OFFSET
    , DISPLAY_LIST
    , AVATAR_TYPE
    , START_CLIENTS
    , DEVICE_TRACKING_NAME = None
    ):
    
    ##
    #
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ##
    #
    self.id = ID

    ## @var input_device_type
    # String indicating the type of input device to be created, e.g. "XBoxController" or "OldSpheron"
    self.input_device_type = INPUT_DEVICE_TYPE

    ## @var input_device_name
    # Name of the input device sensor as chosen in daemon.
    self.input_device_name = INPUT_DEVICE_NAME

    if self.input_device_name == None:
      self.input_device_name = "keyboard"

    ## @var start_matrix
    # Initial position matrix of the platform.
    self.start_matrix = STARTING_MATRIX

    ## @var start_scale
    # Initial scaling factor of the platform.
    self.start_scale = STARTING_SCALE
    
    # create device
    ## @var device
    # Device instance handling relative inputs of physical device.
    if self.input_device_type == "OldSpheron":
      self.device = OldSpheronDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "NewSpheron":
      self.device = NewSpheronDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "XBoxController":
      self.device = XBoxDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "KeyboardMouse":
      self.device = KeyboardMouseDevice()
      self.device.my_constructor(NO_TRACKING_MAT)
    elif self.input_device_type == "Spacemouse":
      self.device = SpacemouseDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "Globefish":
      self.device = GlobefishDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, NO_TRACKING_MAT)


    # init field connections
    self.sf_reset_trigger.connect_from(self.device.sf_reset_trigger)
    self.sf_coupling_trigger.connect_from(self.device.sf_coupling_trigger)
    self.sf_dof_trigger.connect_from(self.device.sf_dof_trigger)
    
    # create ground following
    ## @var groundfollowing
    # GroundFollowing instance to correct the absolute matrices with respect to gravity.
    self.groundfollowing = GroundFollowing()
    self.groundfollowing.my_constructor(self.device.sf_station_mat, float(GF_SETTINGS[1]))

    # create input mapping
    ## @var inputmapping
    # InputMapping instance to process and map relative device inputs to an absolute matrix.
    self.inputmapping = InputMapping()
    self.inputmapping.my_constructor(self, self.device, self.groundfollowing, STARTING_MATRIX, INVERT)
    self.inputmapping.set_input_factors(self.device.translation_factor, self.device.rotation_factor)
    self.inputmapping.sf_scale.value = STARTING_SCALE

    # activate correct input mapping mode according to configuration file
    if GF_SETTINGS[0]:
      self.inputmapping.activate_realistic_mode()
    else:
      self.inputmapping.deactivate_realistic_mode()

    # create device avatar
    #if AVATAR_TYPE != "None" and AVATAR_TYPE.endswith(".ks") == False:
    #  self.device.create_device_avatar(self.platform)

    ##
    #
    self.display_list = DISPLAY_LIST

    # attributes
    ## @var in_dofchange_animation
    # Boolean variable to indicate if a movement animation for a DOF change (realistic/unrealistic) is in progress.
    self.in_dofchange_animation = False

    ## @var timer
    # Instance of TimeSensor to handle the duration of animations.
    self.timer = avango.nodes.TimeSensor()

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
      self.trace = TraceLines.Trace(self.platform.platform_id, 500, 50.0, STARTING_MATRIX, self.trace_material + 'Shadeless')    

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


  ## Switches from realistic to unrealistic or from unrealistic to realistic mode on this
  # and all other coupled instances.
  def trigger_dofchange(self):

    # if in realistic mode, switch to unrealistic mode
    if self.inputmapping.realistic == True:
      #print "GF off"
      self.deactivate_realistic_mode()
    
    # if in unrealistic mode, switch to realistic mode
    else:
      #print "GF on"
      self.activate_realistic_mode()

  ## Computes the current world position of the rotation center on the platform ground (y = 0).
  def get_current_world_pos(self):
    _station_trans = self.device.sf_station_mat.value.get_translate()
    _mat = self.platform.sf_abs_mat.value * avango.gua.make_trans_mat(avango.gua.Vec3(_station_trans.x, 0, _station_trans.z) * self.platform.sf_scale.value)
    return _mat
  
  ## Evaluated every frame.
  def evaluate(self):

    # handle dofchange animation
    if self.in_dofchange_animation:
      self.animate_dofchange()

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
          

  ## Evaluated when value changes.
  @field_has_changed(sf_dof_trigger)
  def sf_dof_trigger_changed(self):
  
    if self.sf_dof_trigger.value == True: # button pressed

      if self.in_dofchange_animation == False:
         self.trigger_dofchange()
    
         

