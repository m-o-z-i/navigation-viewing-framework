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

  ##
  #
  sf_border_mat = avango.gua.SFMatrix4()

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

  ## @var sf_close_button
  # Boolean field to check if the close button was pressed.
  sf_close_button = avango.SFBool()

  ## @var sf_open_button
  # Boolean field to check if the open button was pressed.
  sf_open_button = avango.SFBool() 

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

    ## @var portal_width
    # Width of the portals displayed in this PortalCamera.
    self.portal_width = 0.2

    ## @var portal_height
    # Height of the portals displayed in this PortalCamera.
    self.portal_height = 0.2


  ## Custom constructor.
  # @param PORTAL_MANAGER Reference to the PortalManager used for Portal creation and management.
  # @param PLATFORM_NODE Platform scenegraph node to which this PortalCamera should be appended to.
  # @param CAMERA_INPUT_NAME Name of the PortalCamera's input sensor as registered in daemon.
  # @param CAMERA_TRACKING_NAME Name of the PortalCamera's tracking target as registered in daemon.
  def my_constructor(self, PORTAL_MANAGER, PLATFORM_NODE, CAMERA_INPUT_NAME, CAMERA_TRACKING_NAME):
    
    ## @var PORTAL_MANAGER
    # Reference to the PortalManager used for Portal creation and management.
    self.PORTAL_MANAGER = PORTAL_MANAGER

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
    self.sf_scale_down_button.connect_from(self.device_sensor.Button10)
    self.sf_close_button.connect_from(self.device_sensor.Button2)
    self.sf_open_button.connect_from(self.device_sensor.Button3)
    self.sf_2D_mode_button.connect_from(self.device_sensor.Button7)
    self.sf_3D_mode_button.connect_from(self.device_sensor.Button8)
    self.sf_negative_parallax_on_button.connect_from(self.device_sensor.Button12)
    self.sf_negative_parallax_off_button.connect_from(self.device_sensor.Button13)

    ## @var tracking_reader
    # TrackingTargetReader to process the tracking input of the PortalCamera.
    self.tracking_reader = TrackingTargetReader()
    self.tracking_reader.my_constructor(CAMERA_TRACKING_NAME)
    self.sf_tracking_mat.connect_from(self.tracking_reader.sf_abs_mat)

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var camera_frame
    # Geometry node containing the PortalCamera's portal frame.
    self.camera_frame = _loader.create_geometry_from_file("portal_camera", "data/objects/screen.obj", "data/materials/ShadelessRed.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.camera_frame.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.camera_frame.GroupNames.value = ["do_not_display_group"]
    PLATFORM_NODE.Children.value.append(self.camera_frame)

    self.camera_frame.Transform.connect_from(self.sf_border_mat)

    ##
    #
    self.last_open_portal_index = None

    # set evaluation policy
    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):

    self.sf_border_mat.value  = avango.gua.make_trans_mat(0.0, self.portal_height/2, 0.0) * \
                                self.tracking_reader.sf_abs_mat.value * \
                                avango.gua.make_scale_mat(self.portal_width, self.portal_height, 1.0)

    if self.current_portal != None:
      self.camera_frame.GroupNames.value = ["do_not_display_group"]
    

  ## Called whenever sf_focus_button changes.
  @field_has_changed(sf_focus_button)
  def sf_focus_button_changed(self):

    if self.sf_focus_button.value == True:

      try:
        self.camera_frame.GroupNames.value = []
      except:
        pass

    else:

      try:
        self.camera_frame.GroupNames.value = ["do_not_display_group"]
      except:
        pass

  ## Called whenever sf_capture_button changes.
  @field_has_changed(sf_capture_button)
  def sf_capture_button_changed(self):
    if self.sf_capture_button.value == True:

      if self.current_portal == None:
        _portal = self.PORTAL_MANAGER.add_portal(self.camera_frame.WorldTransform.value, 
                                                 self.camera_frame.WorldTransform.value,
                                                 1.0,
                                                 1.0,
                                                 "3D",
                                                 "PERSPECTIVE",
                                                 "True",
                                                 "data/materials/ShadelessBlue.gmd")
        self.captured_portals.append(_portal)
        _portal.portal_matrix_node.Transform.connect_from(self.camera_frame.WorldTransform)
        self.current_portal = _portal

  ## Called whenever sf_next_rec_button changes.
  @field_has_changed(sf_next_rec_button)
  def sf_next_rec_button_changed(self):
    if self.sf_next_rec_button.value == True:
      
      self.current_portal.set_visibility(False)

      _current_index = self.captured_portals.index(self.current_portal)
      #print "_current_index", _current_index
      _current_index += 1
      #print "_current_index+1", _current_index
      _current_index = _current_index % len(self.captured_portals)
      #print "modulo", 

      self.current_portal = self.captured_portals[_current_index]
      self.current_portal.set_visibility(True)


  ## Called whenever sf_prior_rec_button changes.
  @field_has_changed(sf_prior_rec_button)
  def sf_prior_rec_button_changed(self):
    if self.sf_prior_rec_button.value == True:
      
      self.current_portal.set_visibility(False)

      _current_index = self.captured_portals.index(self.current_portal)
      _current_index -= 1
      _current_index = _current_index % len(self.captured_portals)

      self.current_portal = self.captured_portals[_current_index]
      self.current_portal.set_visibility(True)

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

  ## Called whenever sf_close_button changes.
  @field_has_changed(sf_close_button)
  def sf_close_button_changed(self):
    if self.sf_close_button.value == True:

      if self.current_portal != None:
        self.current_portal.set_visibility(False)
        self.last_open_portal_index = self.captured_portals.index(self.current_portal)
        self.current_portal = None

  ## Called whenever sf_open_button changes.
  @field_has_changed(sf_open_button)
  def sf_open_button_changed(self):
    if self.sf_open_button.value == True:

      if self.current_portal == None and len(self.captured_portals) > 0:
       self.current_portal = self.captured_portals[self.last_open_portal_index]
       self.current_portal.set_visibility(True)
      

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