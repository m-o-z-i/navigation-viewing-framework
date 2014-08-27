#!/usr/bin/python

## @file
# Contains class PortalCameraNavigation.

# import avango-guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed

# import framework libraries
from Navigation import *
from PortalCamera import *

## 
#
class PortalCameraNavigation(Navigation):

  sf_capture_button = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(PortalCameraNavigation).__init__()

  ## Custom constructor.
  #
  def my_constructor(self, PORTAL_CAMERA_INSTANCE, TRACE_VISIBILITY_LIST):

    self.list_constructor(TRACE_VISIBILITY_LIST)

    ##
    #
    self.portal_cam = PORTAL_CAMERA_INSTANCE

    ##
    #
    self.drag_last_frame_camera_mat = None

    # init field connections
    self.sf_capture_button.connect_from(self.portal_cam.sf_capture_button)

    #
    self.always_evaluate(True)

  ##
  def evaluate(self):

     # update matrices in dragging    
     if self.drag_last_frame_camera_mat != None:

      _current_camera_mat = self.portal_cam.tracking_reader.sf_abs_mat.value * avango.gua.make_trans_mat(0.0, self.portal_cam.portal_height/2, 0.0)
      _drag_input_mat = avango.gua.make_inverse_mat(self.drag_last_frame_camera_mat) * _current_camera_mat
      _drag_input_mat.set_translate(_drag_input_mat.get_translate() * self.sf_scale.value)
      _new_scene_mat = self.sf_abs_mat.value * _drag_input_mat
      
      self.sf_abs_mat.value = _new_scene_mat
      self.drag_last_frame_camera_mat = _current_camera_mat

      # update nav mat
      self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)

  ##
  #
  def set_navigation_values(self, STATIC_ABS_MAT, STATIC_SCALE):
    self.sf_abs_mat.value = STATIC_ABS_MAT
    self.sf_scale.value = STATIC_SCALE
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)

  @field_has_changed(sf_capture_button)
  def sf_capture_button_changed(self):
    
    if self.sf_capture_button.value == True and self.portal_cam.current_shot != None:

      self.drag_last_frame_camera_mat = self.portal_cam.tracking_reader.sf_abs_mat.value * \
                                        avango.gua.make_trans_mat(0.0, self.portal_cam.portal_height/2, 0.0)


    # stop dragging
    else:

      self.drag_last_frame_camera_mat = None