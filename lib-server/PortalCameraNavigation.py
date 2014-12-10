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

## Special type of Navigation associated to a PortalCamera.
# Allows moving and rotating by moving the device when a button is pressed and
# changes scalings by button presses.
class PortalCameraNavigation(Navigation):

  ## @var sf_clutch_button
  # Boolean field to check if the clutch trigger button was pressed.
  sf_clutch_button = avango.SFBool()

  ## @var sf_scale_up_button
  # Boolean field to check if the scale up button was pressed.
  sf_scale_up_button = avango.SFBool()

  ## @var sf_scale_down_button
  # Boolean field to check if the scale down button was pressed.
  sf_scale_down_button = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(PortalCameraNavigation).__init__()

  ## Custom constructor.
  # @param PORTAL_CAMERA_INSTANCE Instance of PortalCamera which is the input device of this Navigation.
  def my_constructor(self, PORTAL_CAMERA_INSTANCE):

    ## @var portal_cam
    # Instance of PortalCamera which is the input device of this Navigation.
    self.portal_cam = PORTAL_CAMERA_INSTANCE

    ## @var drag_last_frame_camera_mat
    # Matrix containing the value of the tracking target of the last frame when in drag mode.
    self.drag_last_frame_camera_mat = None

    # init field connections
    self.sf_clutch_button.connect_from(self.portal_cam.sf_focus_button)
    self.sf_scale_up_button.connect_from(self.portal_cam.sf_scale_up_button)
    self.sf_scale_down_button.connect_from(self.portal_cam.sf_scale_down_button)

    # set evaluation policy
    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):

    # update matrices in dragging    
    if self.drag_last_frame_camera_mat != None:
  
      _current_camera_mat = self.portal_cam.tracking_reader.sf_abs_mat.value * avango.gua.make_trans_mat(0.0, self.portal_cam.portal_height/2, 0.0)
      _drag_input_mat = avango.gua.make_inverse_mat(self.drag_last_frame_camera_mat) * _current_camera_mat
      _drag_input_mat.set_translate(_drag_input_mat.get_translate() * self.sf_scale.value)
      _new_scene_mat = self.sf_abs_mat.value * _drag_input_mat
    
      self.sf_abs_mat.value = _new_scene_mat
      self.drag_last_frame_camera_mat = _current_camera_mat

    # update scaling
    if self.sf_scale_up_button.value == True and self.portal_cam.current_shot != None:
      self.portal_cam.set_current_shot_scale(self.portal_cam.current_shot.sf_scale.value * 0.995)

    if self.sf_scale_down_button.value == True and self.portal_cam.current_shot != None:
      self.portal_cam.set_current_shot_scale(self.portal_cam.current_shot.sf_scale.value * 1.005)

    # update nav mat
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)


  ## Sets sf_abs_mat and sf_scale.
  # @param STATIC_ABS_MAT The new sf_abs_mat to be set.
  # @param STATIC_SCALE The new sf_scale to be set.
  def set_navigation_values(self, STATIC_ABS_MAT, STATIC_SCALE):
    self.sf_abs_mat.value = STATIC_ABS_MAT
    self.sf_scale.value = STATIC_SCALE
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)

  ## Called whenever sf_clutch_button changes
  @field_has_changed(sf_clutch_button)
  def sf_capture_button_changed(self):
    
    # initiate dragging
    if self.sf_clutch_button.value == True and self.portal_cam.current_shot != None:

      self.drag_last_frame_camera_mat = self.portal_cam.tracking_reader.sf_abs_mat.value * \
                                        avango.gua.make_trans_mat(0.0, self.portal_cam.portal_height/2, 0.0)


    # stop dragging
    else:

      self.drag_last_frame_camera_mat = None