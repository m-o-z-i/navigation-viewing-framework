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
# ...

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

    if self.maximized_portal == None:

      PORTAL_INSTANCE.connect_portal_matrix(self.sf_min_y_plane_transform)
      PORTAL_INSTANCE.set_size(self.get_width(), self.get_height())
      self.maximized_portal = PORTAL_INSTANCE
 
  ## Removes and returns the currently maximized portal.
  def remove_maximized_portal(self):

    if self.maximized_portal != None:

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

