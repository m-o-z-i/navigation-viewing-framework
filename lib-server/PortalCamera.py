#!/usr/bin/python

## @file
# Contains class PortalCamera.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Portal import *
from TrackingReader import *

# import python libraries
# ...

## A PortalCamera is a physical device to interactively caputure, view
# and manipulate Portal instances in the scene.
class PortalCamera(avango.script.Script):
 
  ## @var sf_tracking_mat
  # Tracking matrix of the PortalCamera within the platform coordinate system.
  sf_tracking_mat = avango.gua.SFMatrix4()

  # button fields
  ## @var sf_focus_button
  # Boolean field to check if the focus button was pressed.
  sf_focus_button = avango.SFBool()

  ## @var sf_capture_button
  # Boolean field to check if the capture button was pressed.
  sf_capture_button = avango.SFBool()

  ## @var sf_next_rec_button
  # Boolean field to check if the next recording button was pressed.
  sf_next_rec_button = avango.SFBool()

  ## @var sf_prior_rec_button
  # Boolean field to check if the prior recording button was pressed.
  sf_prior_rec_button = avango.SFBool()

  ## @var sf_scale_up_button
  # Boolean field to check if the scale up button was pressed.
  sf_scale_up_button = avango.SFBool()

  ## @var sf_scale_down_button
  # Boolean field to check if the scale down button was pressed.
  sf_scale_down_button = avango.SFBool()

  ## @var sf_2D_mode_button
  # Boolean field to check if the 2D mode button was pressed.
  sf_2D_mode_button = avango.SFBool()

  ## @var sf_3D_mode_button
  # Boolean field to check if the 3D mode button was pressed.
  sf_3D_mode_button = avango.SFBool()

  ## @var sf_negative_parallax_on_button
  # Boolean field to check if the negative parallax on button was pressed.
  sf_negative_parallax_on_button = avango.SFBool()

  ## @var sf_negative_parallax_off_button
  # Boolean field to check if the negative parallax off button was pressed.
  sf_negative_parallax_off_button = avango.SFBool()


  ## Default constructor.
  def __init__(self):
    self.super(PortalCamera).__init__()

    ## @var captured_portals
    # List of Portal instances belonging to this PortalCamera.
    self.captured_portals = []

    ## @var current_portal
    # Portal instance which is currently displayed above the PortalCamera.
    self.current_portal = None


  ## Custom constructor.
  # @param PLATFORM_NODE Platform scenegraph node to which this PortalCamera should be appended to.
  # @param CAMERA_INPUT_NAME Name of the PortalCamera's input sensor as registered in daemon.
  # @param CAMERA_TRACKING_NAME Name of the PortalCamera's tracking target as registered in daemon.
  def my_constructor(self, PLATFORM_NODE, CAMERA_INPUT_NAME, CAMERA_TRACKING_NAME):
    
    ## @var PLATFORM_NODE
    # Platform scenegraph node to which this PortalCamera should be appended to.
    self.PLATFORM_NODE = PLATFORM_NODE

    ## @var device_sensor
    # Device sensor for the PortalCamera's button inputs.
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = CAMERA_INPUT_NAME

    # init field connections
    self.sf_focus_button.connect_from(self.device_sensor.Button0)
    self.sf_capture_button.connect_from(self.device_sensor.Button1)
    self.sf_next_rec_button.connect_from(self.device_sensor.Button5)
    self.sf_prior_rec_button.connect_from(self.device_sensor.Button4)
    self.sf_scale_up_button.connect_from(self.device_sensor.Button9)
    self.sf_scale_down_button.connect_from(self.device_sensor.Button11)
    self.sf_2D_mode_button.connect_from(self.device_sensor.Button7)
    self.sf_3D_mode_button.connect_from(self.device_sensor.Button8)
    self.sf_negative_parallax_on_button.connect_from(self.device_sensor.Button12)
    self.sf_negative_parallax_off_button.connect_from(self.device_sensor.Button13)

    ## @var tracking_reader
    # TrackingTargetReader to process the tracking input of the PortalCamera.
    self.tracking_reader = TrackingTargetReader()
    self.tracking_reader.my_constructor(CAMERA_TRACKING_NAME)
    self.sf_tracking_mat.connect_from(self.tracking_reader.sf_abs_mat)

    # set evaluation policy
    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):
    pass#print self.device_sensor.Button0.value

  ## Called whenever sf_focus_button changes.
  @field_has_changed(sf_focus_button)
  def sf_focus_button_changed(self):
    if self.sf_focus_button.value == True:
      print "sf_focus_button pressed"

  ## Called whenever sf_capture_button changes.
  @field_has_changed(sf_capture_button)
  def sf_capture_button_changed(self):
    if self.sf_capture_button.value == True:
      print "sf_capture_button pressed"

  ## Called whenever sf_next_rec_button changes.
  @field_has_changed(sf_next_rec_button)
  def sf_next_rec_button_changed(self):
    if self.sf_next_rec_button.value == True:
      print "sf_next_rec_button pressed"

  ## Called whenever sf_prior_rec_button changes.
  @field_has_changed(sf_prior_rec_button)
  def sf_prior_rec_button_changed(self):
    if self.sf_prior_rec_button.value == True:
      print "sf_prior_rec_button pressed"

  ## Called whenever sf_scale_up_button changes.
  @field_has_changed(sf_scale_up_button)
  def sf_scale_up_button_changed(self):
    if self.sf_scale_up_button.value == True:
      print "sf_scale_up_button pressed"

  ## Called whenever sf_scale_down_button changes.
  @field_has_changed(sf_scale_down_button)
  def sf_scale_down_button_changed(self):
    if self.sf_scale_down_button.value == True:
      print "sf_scale_down_button pressed"

  ## Called whenever sf_2D_mode_button changes.
  @field_has_changed(sf_2D_mode_button)
  def sf_2D_mode_button_changed(self):
    if self.sf_2D_mode_button.value == True:
      print "sf_2D_mode_button pressed"

  ## Called whenever sf_3D_mode_button changes.
  @field_has_changed(sf_3D_mode_button)
  def sf_3D_mode_button_changed(self):
    if self.sf_3D_mode_button.value == True:
      print "sf_3D_mode_button pressed"

  ## Called whenever sf_negative_parallax_on_button changes.
  @field_has_changed(sf_negative_parallax_on_button)
  def sf_negative_parallax_on_button_changed(self):
    if self.sf_negative_parallax_on_button.value == True:
      print "sf_negative_parallax_on_button pressed"

  ## Called whenever sf_negative_parallax_off_button changes.
  @field_has_changed(sf_negative_parallax_off_button)
  def sf_negative_parallax_off_button_changed(self):
    if self.sf_negative_parallax_off_button.value == True:
      print "sf_negative_parallax_off_button pressed"