#!/usr/bin/python

## @file
# Contains class PortalInteractionSpace.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Device import *

# import python libraries
import time

## Space on a platform in which an additional device can be used for
# modifying the scene matrices of portals.
class PortalInteractionSpace(avango.script.Script):

  ## @var mf_device_values
  # Multi field containing the device's input values.
  mf_device_values = avango.MFFloat()

  ## @var mf_device_transformed_values
  # Multi field containing the scaled device input values.
  mf_device_transformed_values = avango.MFFloat()

  ## @var sf_min_y_plane_transform
  # Transformation matrix of the min y plane.
  sf_min_y_plane_transform = avango.gua.SFMatrix4()

  ##
  #
  sf_animation_matrix = avango.gua.SFMatrix4()

  ## Default constructor.
  def __init__(self):
    self.super(PortalInteractionSpace).__init__()

  ## Custom constructor.
  # @param DEVICE Instance of Device to be used for portal navigation.
  # @param PLATFORM Platform instance to which this PortalInteractionSpace is belonging to.
  # @param MIN_POINT Minimum coordinates of the point spanning up the space.
  # @param MAX_POINT Maximum coordinates of the point spanning up the space.
  def my_constructor(self, DEVICE, PLATFORM, MIN_POINT, MAX_POINT):

    ## @var DEVICE
    # Instance of Device to be used for portal navigation.
    self.DEVICE = DEVICE

    ## @var PLATFORM
    # Platform instance to which this PortalInteractionSpace is belonging to.
    self.PLATFORM = PLATFORM

    ## @var MIN_POINT
    # Minimum coordinates of the point spanning up the space.
    self.MIN_POINT = MIN_POINT

    ## @var MAX_POINT
    # Maximum coordinates of the point spanning up the space.
    self.MAX_POINT = MAX_POINT

    ## @var maximized_portal
    # Portal instance which is currently maximized in this interaction space.
    self.maximized_portal = None

    ##
    #
    self.animation_start_time = None

    ##
    #
    self.animation_start_matrix = None

    ##
    #
    self.animation_start_size = None

    ##
    #
    self.animation_duration = 1.0

    self.mf_device_values.connect_from(self.DEVICE.mf_dof)

    # set evaluation policy
    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):
    
    _avg_point = (self.MIN_POINT + self.MAX_POINT) / 2
    _plane_transform = avango.gua.make_trans_mat(_avg_point.x, self.MIN_POINT.y, _avg_point.z) * \
                       avango.gua.make_rot_mat(90, 0, 1, 0) * \
                       avango.gua.make_rot_mat(-90, 1, 0, 0)

    self.sf_min_y_plane_transform.value = self.PLATFORM.platform_scale_transform_node.WorldTransform.value * \
                                          _plane_transform

    # handle maximization animation
    if self.animation_start_time != None:

      _time_step = time.time() - self.animation_start_time

      if _time_step > self.animation_duration:
        self.animation_start_time = None
        self.animation_start_matrix = None
        self.animation_start_size = None
        self.maximized_portal.connect_portal_matrix(self.sf_min_y_plane_transform)
        self.maximized_portal.set_size(self.get_width(), self.get_height())
        return
      
      _ratio = _time_step / self.animation_duration
      _start_trans = self.animation_start_matrix.get_translate()
      _end_trans = self.sf_min_y_plane_transform.value.get_translate()
      _animation_trans = _start_trans.lerp_to(_end_trans, _ratio)

      _start_rot = self.animation_start_matrix.get_rotate()
      _end_rot = self.sf_min_y_plane_transform.value.get_rotate()
      _animation_rot = _start_rot.slerp_to(_end_rot, _ratio)

      _start_size = self.animation_start_size
      _end_size = avango.gua.Vec3(self.get_width(), self.get_height(), 1.0)
      _animation_size = _start_size.lerp_to(_end_size, _ratio)

      self.sf_animation_matrix.value = avango.gua.make_trans_mat(_animation_trans) * \
                                       avango.gua.make_rot_mat(_animation_rot)
      self.maximized_portal.set_size(_animation_size.x, _animation_size.y)
      return

    # give input to maximized portal
    if self.maximized_portal != None:
      self.maximized_portal.modify_scene_matrix(self.mf_device_transformed_values.value)

  ## Returns a boolean saying if a point lies within the interaction space.
  # @param POINT The point to be checked for.
  def is_inside(self, POINT):
     
     _x = POINT.x
     _y = POINT.y
     _z = POINT.z

     if _x > self.MIN_POINT.x and _x < self.MAX_POINT.x and \
        _y > self.MIN_POINT.y and _y < self.MAX_POINT.y and \
        _z > self.MIN_POINT.z and _z < self.MAX_POINT.z:

       return True

     return False

  ## Gets the width of the interaction space.
  def get_width(self):
    return self.MAX_POINT.z - self.MIN_POINT.z

  ## Gets the height of the interaction space.
  def get_height(self):
    return self.MAX_POINT.x - self.MIN_POINT.x

  ## Adds a portal instance to this interaction space and maximizes it.
  # @param PORTAL_INSTANCE The Portal instance to be added.
  def add_maximized_portal(self, PORTAL_INSTANCE):

    if self.maximized_portal == None and self.animation_start_time == None:

      self.sf_animation_matrix.value = PORTAL_INSTANCE.portal_matrix_node.WorldTransform.value
      self.animation_start_time = time.time()
      self.animation_start_matrix = self.sf_animation_matrix.value
      self.animation_start_size = avango.gua.Vec3(PORTAL_INSTANCE.width, PORTAL_INSTANCE.height, 1.0)

      PORTAL_INSTANCE.connect_portal_matrix(self.sf_animation_matrix)
      self.maximized_portal = PORTAL_INSTANCE
 
  ## Removes and returns the currently maximized portal.
  def remove_maximized_portal(self):

    if self.maximized_portal != None and self.animation_start_time == None:

      _portal = self.maximized_portal
      self.maximized_portal = None
      return _portal 



  ## Called whenever mf_device_values changes.
  @field_has_changed(mf_device_values)
  def mf_device_values_changed(self):

    self.mf_device_transformed_values.value = self.mf_device_values.value

    self.mf_device_transformed_values.value[0] *= self.DEVICE.translation_factor
    self.mf_device_transformed_values.value[1] *= self.DEVICE.translation_factor
    self.mf_device_transformed_values.value[2] *= self.DEVICE.translation_factor
    self.mf_device_transformed_values.value[3] *= self.DEVICE.rotation_factor
    self.mf_device_transformed_values.value[4] *= self.DEVICE.rotation_factor
    self.mf_device_transformed_values.value[5] *= self.DEVICE.rotation_factor

