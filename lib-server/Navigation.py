#!/usr/bin/python

## @file
# Contains base class Navigation.

# import avango-guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed

# import framework libraries
from ApplicationManager import *
from VisibilityHandler import *
from TraceLines import *

## Base class. Not to be instantiated.
class Navigation(VisibilityHandler1D):

  # output field
  ## @var sf_nav_mat
  # Combined matrix of sf_abs_mat and sf_scale.
  sf_nav_mat = avango.gua.SFMatrix4()
  sf_nav_mat.value = avango.gua.make_identity_mat()

  # input fields
  ## @var sf_abs_mat
  # Matrix representing the current translation and rotation of the navigation in the scene.
  sf_abs_mat = avango.gua.SFMatrix4()
  sf_abs_mat.value = avango.gua.make_identity_mat()

  ## @var sf_scale
  # The current scaling factor of this navigation.
  sf_scale = avango.SFFloat()
  sf_scale.value = 1.0

  # input fields
  ## @var sf_reset_trigger
  # Boolean field to indicate if the navigation is to be reset.
  sf_reset_trigger = avango.SFBool()

  ## @var sf_coupling_trigger
  # Boolean field to indicate if the coupling mechanism is to be triggered.
  sf_coupling_trigger = avango.SFBool()

  ## @var sf_dof_trigger
  # Boolean field to indicate if the change of the dof mode is to be triggered.
  sf_dof_trigger = avango.SFBool()

  ## @var sf_request_trigger
  # Boolean field to indicate if the request mechanism is to be triggered.
  sf_request_trigger = avango.SFBool()

  # static class variables
  ## @var trace_materials
  # List of material pretexts to choose from when a trace is created. All avatars on this
  # navigation will have this material.
  trace_materials = ['AvatarBlue', 'AvatarGreen', 'AvatarRed', 'AvatarYellow', 'AvatarMagenta', 
                     'AvatarOrange', 'AvatarWhite', 'AvatarGrey', 'AvatarDarkGreen']

  ## @var number_of_instances
  # Number of SteeringNavigation instances already created. Used for trace material assignment.
  number_of_instances = 0

  ## Base constructor.
  def __init__(self):
    self.super(Navigation).__init__()

    ## @var trace
    # The trace class that handles the line segment updating.
    self.trace = None

    ## @var active_user_representations
    # List of UserRepresentation instances which are currently connecting with this navigations matrix.
    self.active_user_representations = []

    ## @var is_requestable
    # Boolean saying if this Navigation is a requestable one. Requestable navigations
    # can be switched to using a special button on the device.
    self.is_requestable = False

    # get the selected material 
    ## @var trace_material
    # The material to be used for the movement traces.
    self.trace_material = Navigation.trace_materials[Navigation.number_of_instances]
    Navigation.number_of_instances += 1
    Navigation.number_of_instances = Navigation.number_of_instances % len(Navigation.trace_materials)


  ## Adds a UserRepresentation to this navigation.
  # @param USER_REPRESENTATION The UserRepresentation instance to be added.
  def add_user_representation(self, USER_REPRESENTATION):

    # set navigation color plane
    for _screen in USER_REPRESENTATION.screens:

      try:
        _screen.Children.value[0].Material.value = 'data/materials/' + self.trace_material + 'Shadeless.gmd'
      except:
        pass

    if len(self.active_user_representations) == 0 and self.trace != None:

      try:
        _device_pos = self.device.sf_station_mat.value.get_translate()
        self.trace.clear(self.sf_abs_mat.value * avango.gua.make_trans_mat(_device_pos.x, 0, _device_pos.z))
      except:
        pass

    self.active_user_representations.append(USER_REPRESENTATION)
  
  ## Removes a UserRepresentation from this navigation.
  # @param USER_REPRESENTATION The UserRepresentation instance to be removed.
  def remove_user_representation(self, USER_REPRESENTATION):

    if USER_REPRESENTATION in self.active_user_representations:
      self.active_user_representations.remove(USER_REPRESENTATION)

      if len(self.active_user_representations) == 0 and self.trace != None:

        try:
          _device_pos = self.device.sf_station_mat.value.get_translate()
        except:
          _device_pos = avango.gua.make_trans_mat(0,0,0)

        self.trace.clear(self.sf_abs_mat.value * avango.gua.make_trans_mat(_device_pos.x, 0, _device_pos.z))

  ## Triggers the correct GroupNames for the different DisplayGroups.
  def handle_correct_visibility_groups(self):

    _trace_visible_for = []

    for _user_repr in ApplicationManager.all_user_representations:

      if self.visibility_list[_user_repr.DISPLAY_GROUP.visibility_tag]:
        _trace_visible_for.append(_user_repr.view_transform_node.Name.value)

    if len(_trace_visible_for) == 0:
      self.trace.append_to_group_names("do_not_display_group")
    
    else:  
      for _string in _trace_visible_for:
        self.trace.append_to_group_names(_string)


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