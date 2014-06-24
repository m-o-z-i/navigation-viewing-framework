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
import Tools

# import python libraries
# ...

## A PortalCamera is a physical device to interactively caputure, view
# and manipulate Portal instances in the scene.
class PortalCamera(avango.script.Script):
 
  ## @var sf_tracking_mat
  # Tracking matrix of the PortalCamera within the platform coordinate system.
  sf_tracking_mat = avango.gua.SFMatrix4()

  ## @var sf_border_mat
  # Matrix with which binded portals must be connected.
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

  ## @var sf_open_close_button
  # Boolean field to check if the open and close button was pressed.
  sf_open_close_button = avango.SFBool()

  ## @var sf_delete_button
  # Boolean field to check if the delete button was pressed.
  sf_delete_button = avango.SFBool()

  ## @var sf_gallery_button
  # Boolean field to check if the gallery button was pressed.
  sf_gallery_button = avango.SFBool()

  ## @var sf_scene_copy_button
  # Boolean field to check if the scene copy button was pressed.
  sf_scene_copy_button = avango.SFBool()

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

    ## @var free_portals
    # List of Portal instances that were placed in the scene by this PortalCamera.
    self.free_portals = []

    ## @var current_portal
    # Portal instance which is currently displayed above the PortalCamera.
    self.current_portal = None

    ## @var portal_width
    # Width of the portals displayed in this PortalCamera.
    self.portal_width = 0.3

    ## @var portal_height
    # Height of the portals displayed in this PortalCamera.
    self.portal_height = 0.3

    ## @var capture_viewing_mode
    # Viewing mode with which new portals will be created.
    self.capture_viewing_mode = "3D"

    ## @var capture_parallax_mode
    # Negative parallax mode with which new portals will be created.
    self.capture_parallax_mode = "True"

    ## @var gallery_activated
    # Boolean indicating if the gallery is currently visible for this PortalCamera.
    self.gallery_activated = False

    ## @var gallery_focus_portal_index
    # Index within self.captured_portals saying which of the Portals is currently in the gallery's focus.
    self.gallery_focus_portal_index = 0

    ## @var next_focus_portal_index
    # Index within self.captured_portals to indicate which Portal is the next one to be set in focus.
    # Used for animation purposed.
    self.next_focus_portal_index = 0

    ## @var gallery_magification_factor
    # Factor with which the size of the portals will be multiplied when in gallery mode.
    self.gallery_magnification_factor = 1.5

    ##
    #
    self.interaction_spaces = []

    ## @var min_scale
    # The minimum scaling factor that can be applied.
    self.min_scale = 0.001

    ## @var max_scale
    # The maximum scaling factor that can be applied.
    self.max_scale = 1000.0

    ## @var scale_stop_time
    # Time at which a scaling process stopped at a fixed step.
    self.scale_stop_time = None

    ## @var scale_stop_duration
    # Time how long a scaling process is stopped at a fixed step in seconds.
    self.scale_stop_duration = 1.0


  ## Custom constructor.
  # @param PORTAL_MANAGER Reference to the PortalManager used for Portal creation and management.
  # @param NAVIGATION Navigation instance to which this PortalCamera belongs to.
  # @param CAMERA_INPUT_NAME Name of the PortalCamera's input sensor as registered in daemon.
  # @param CAMERA_TRACKING_NAME Name of the PortalCamera's tracking target as registered in daemon.
  def my_constructor(self, PORTAL_MANAGER, NAVIGATION, CAMERA_INPUT_NAME, CAMERA_TRACKING_NAME):
    
    ## @var PORTAL_MANAGER
    # Reference to the PortalManager used for Portal creation and management.
    self.PORTAL_MANAGER = PORTAL_MANAGER

    ## @var NAVIGATION
    # Navigation instance to which this PortalCamera belongs to.
    self.NAVIGATION = NAVIGATION

    ## @var PLATFORM_NODE
    # Platform scenegraph node to which this PortalCamera should be appended to.
    self.PLATFORM_NODE = self.NAVIGATION.platform.platform_scale_transform_node

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
    self.sf_open_close_button.connect_from(self.device_sensor.Button2)
    self.sf_delete_button.connect_from(self.device_sensor.Button15)
    self.sf_gallery_button.connect_from(self.device_sensor.Button6)
    self.sf_scene_copy_button.connect_from(self.device_sensor.Button3)
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
    self.PLATFORM_NODE.Children.value.append(self.camera_frame)

    self.camera_frame.Transform.connect_from(self.sf_border_mat)

    ## @var viewing_mode_indicator
    # Tiny geometry in the border of the camera frame to illustrate the current state of self.capture_viewing_mode.
    self.viewing_mode_indicator = _loader.create_geometry_from_file('viewing_mode_indicator',
                                                                    'data/objects/plane.obj',
                                                                    'data/materials/CameraMode' + self.capture_viewing_mode + '.gmd',
                                                                    avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.viewing_mode_indicator.Transform.value = avango.gua.make_trans_mat(-self.portal_width * 1.5, self.portal_height * 1.5, 0.0) * \
                                                  avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                                  avango.gua.make_scale_mat(self.portal_height * 0.3, 1.0, self.portal_height * 0.3)
    self.viewing_mode_indicator.ShadowMode.value = avango.gua.ShadowMode.OFF

    self.camera_frame.Children.value.append(self.viewing_mode_indicator)

    ## @var last_open_portal_index
    # Index within self.captured_portals saying which of the Portals was lastly opened by the PortalCamera.
    self.last_open_portal_index = None

    ## @var start_drag_portal_mat
    # Portal matrix at the beginning of a dragging process. None if no dragging is in progress.
    self.start_drag_portal_mat = None

    ## @var start_drag_scene_mat
    # Scene matrix at the beginning of a dragging process. None if no dragging is in progress.
    self.start_drag_scene_mat = None

    # set evaluation policy
    self.always_evaluate(True)

    ######## Debugging setup
    self.debug_portal = self.PORTAL_MANAGER.add_portal(avango.gua.make_trans_mat(0.0, 1.2, 0.0), 
                                             avango.gua.make_trans_mat(0.0, 1.2, 0.0),
                                             1.0,
                                             1.0,
                                             "2D",
                                             "PERSPECTIVE",
                                             self.capture_parallax_mode,
                                             "data/materials/ShadelessBlue.gmd")
    self.captured_portals.append(self.debug_portal)
    self.debug_portal.portal_matrix_node.Transform.connect_from(self.camera_frame.WorldTransform)
    self.current_portal = self.debug_portal


  ## Evaluated every frame.
  def evaluate(self):

    # update portal and camera frame matrix
    self.sf_border_mat.value  = self.tracking_reader.sf_abs_mat.value * \
                                avango.gua.make_trans_mat(0.0, self.portal_height/2, 0.0) * \
                                avango.gua.make_scale_mat(self.portal_width, self.portal_height, 1.0)

    # always hide red camera frame when a portal is displayed
    if self.current_portal != None:
      self.camera_frame.GroupNames.value = ["do_not_display_group"]

    # apply scale changes 
    if self.sf_scale_up_button.value == True:
      
      self.set_current_portal_scale(self.current_portal.scale * 0.985)
      
    if self.sf_scale_down_button.value == True:

      self.set_current_portal_scale(self.current_portal.scale * 1.015)


    # update matrices in drag mode
    if self.start_drag_portal_mat != None and self.start_drag_scene_mat != None:

      _current_portal_mat = self.tracking_reader.sf_abs_mat.value
      _diff_mat = _current_portal_mat * avango.gua.make_inverse_mat(self.start_drag_portal_mat)
      #_mapped_translation = avango.gua.make_rot_mat(self.start_drag_portal_mat.get_rotate()) * _diff_mat.get_translate()
      #_mapped_translation = avango.gua.Vec3(_mapped_translation.x, _mapped_translation.y, _mapped_translation.z)
      _diff_mat = avango.gua.make_trans_mat(_diff_mat.get_translate() * self.current_portal.scale)
      self.current_portal.scene_matrix_node.Transform.value = _diff_mat * self.start_drag_scene_mat


    # check for camera hitting free portals
    _camera_vec = self.camera_frame.WorldTransform.value.get_translate()

    if self.current_portal == None:

      for _free_portal in self.free_portals:

        _portal_vec = _free_portal.portal_matrix_node.WorldTransform.value.get_translate()

        if _camera_vec.x > _portal_vec.x - (self.portal_width/2) and \
           _camera_vec.x < _portal_vec.x + (self.portal_width/2) and \
           _camera_vec.y > _portal_vec.y - 0.1 and \
           _camera_vec.y < _portal_vec.y + 0.1 and \
           _camera_vec.z > _portal_vec.z - 0.05 and \
           _camera_vec.z < _portal_vec.z + 0.05:

          _free_portal.portal_matrix_node.Transform.connect_from(self.camera_frame.WorldTransform)
          self.free_portals.remove(_free_portal)
          self.captured_portals.append(_free_portal)
          self.current_portal = _free_portal
          return

    # check for interaction spaces and corresponding scene matrix updates
    for _interaction_space in self.interaction_spaces:

      if _interaction_space.is_inside(self.tracking_reader.sf_abs_mat.value.get_translate()) and \
         self.current_portal != None and \
         self.gallery_activated == False:
        
        _device_values = _interaction_space.get_values()
        _x = _device_values[0]
        _y = _device_values[1]
        _z = _device_values[2]
        _rx = _device_values[3]
        _ry = _device_values[4]
        _rz = _device_values[5]
        _w = _device_values[6]

        if _w == -1:
          self.set_current_portal_scale(self.current_portal.scale * 0.985)
        elif _w == 1:
          self.set_current_portal_scale(self.current_portal.scale * 1.015)

        _trans_vec = avango.gua.Vec3(_x, _y, _z)
        _rot_vec = avango.gua.Vec3(_rx, _ry, _rz)

        if _trans_vec.length() != 0.0 or _rot_vec.length() != 0.0:

          _scene_transform = self.current_portal.scene_matrix_node.Transform.value
          _scene_translate = _scene_transform.get_translate()
          _scene_rotate    = _scene_transform.get_rotate()

          _device_forward_yaw = Tools.get_yaw(_interaction_space.DEVICE.sf_station_mat.value)
          _device_rot_mat = avango.gua.make_rot_mat(math.degrees(_device_forward_yaw), 0, 1, 0)
          _combined_rot_mat = avango.gua.make_rot_mat(_scene_rotate) * _device_rot_mat
          _transformed_trans_vec = _combined_rot_mat * avango.gua.Vec3(_x, _y, _z)
          _transformed_trans_vec = avango.gua.Vec3(_transformed_trans_vec.x, _transformed_trans_vec.y, _transformed_trans_vec.z)

          _scene_transform = avango.gua.make_trans_mat(_transformed_trans_vec) * \
                             _scene_transform * \
                             avango.gua.make_rot_mat( _rot_vec.z, 0, 0, 1) * \
                             avango.gua.make_rot_mat( _rot_vec.x, 1, 0, 0) * \
                             avango.gua.make_rot_mat( _rot_vec.y, 0, 1, 0)

          self.current_portal.scene_matrix_node.Transform.value = _scene_transform



    # update matrices in gallery mode
    if self.gallery_activated:

      # disable gallery when no captured portals are present (anymore)
      if len(self.captured_portals) == 0:
        self.gallery_activated = False
        return

      # if current index equals next index, no animation is needed
      if self.gallery_focus_portal_index == self.next_focus_portal_index:
        _i = -self.gallery_focus_portal_index
        self.current_portal = self.captured_portals[self.gallery_focus_portal_index]

      # animation is needed
      else:
        
        # snap to next integer value if close enough
        if (self.gallery_focus_portal_index < self.next_focus_portal_index and self.gallery_focus_portal_index > self.next_focus_portal_index - 0.01) or \
           (self.gallery_focus_portal_index > self.next_focus_portal_index and self.gallery_focus_portal_index < self.next_focus_portal_index + 0.01):
          _i = -self.next_focus_portal_index

        # determine animation coefficient
        else:
          _i = -(self.gallery_focus_portal_index + (self.next_focus_portal_index-self.gallery_focus_portal_index) * 0.1)

        self.gallery_focus_portal_index = -_i

      # place gallery correctly over device
      for _portal in self.captured_portals:
        _station_mat = self.NAVIGATION.device.sf_station_mat.value
        _station_vec = _station_mat.get_translate()

        _modified_station_mat = avango.gua.make_trans_mat(_station_vec.x + self.gallery_magnification_factor * (self.portal_width + 0.05) * _i, _station_vec.y + self.gallery_magnification_factor * self.portal_height, _station_vec.z)

        _matrix = self.NAVIGATION.platform.platform_scale_transform_node.WorldTransform.value * \
                  avango.gua.make_trans_mat(_station_vec) * \
                  avango.gua.make_rot_mat(_station_mat.get_rotate()) * \
                  avango.gua.make_trans_mat(_station_vec * -1) * \
                  _modified_station_mat * \
                  avango.gua.make_scale_mat(self.gallery_magnification_factor * self.portal_width, self.gallery_magnification_factor * self.portal_height, 1.0)

        _portal.portal_matrix_node.Transform.disconnect()
        _portal.portal_matrix_node.Transform.value = _matrix
        _portal.set_visibility(True)
        _i += 1


      # check for camera hitting portal in gallery mode
      for _portal in self.captured_portals:

        _portal_vec = _portal.portal_matrix_node.WorldTransform.value.get_translate()

        if _camera_vec.x > _portal_vec.x - (self.portal_width/2) and \
           _camera_vec.x < _portal_vec.x + (self.portal_width/2) and \
           _camera_vec.y > _portal_vec.y - 0.1 and \
           _camera_vec.y < _portal_vec.y + 0.1 and \
           _camera_vec.z > _portal_vec.z - 0.05 and \
           _camera_vec.z < _portal_vec.z + 0.05:

          for _portal_2 in self.captured_portals:
            
            if _portal_2 != _portal:
              _portal_2.set_visibility(False)
            
            _portal_2.portal_matrix_node.Transform.connect_from(self.camera_frame.WorldTransform)

          _grabbed_portal_index = self.captured_portals.index(_portal)
          self.last_open_portal_index = _grabbed_portal_index
          self.gallery_activated = False
          self.current_portal = _portal
          return

  ##
  def add_interaction_space(self, INTERACTION_SPACE):

    self.interaction_spaces.append(INTERACTION_SPACE)
    #self.debug_portal.Transform.disconnect()
    #self.debug_portal.portal_matrix_node.Transform.value = self.interaction_spaces[0].get_min_y_plane_transform()

  ##
  #
  def set_current_portal_scale(self, SCALE):

    if self.current_portal == None:
      return
 
    if self.scale_stop_time == None:
  
      _old_scale = self.current_portal.scale
      _old_scale = round(_old_scale,6)
      
      _new_scale = max(min(SCALE, self.max_scale), self.min_scale)
      _new_scale = round(_new_scale,6)
            
      # stop at certain scale levels
      if (_old_scale < 100.0 and _new_scale > 100.0) or (_new_scale < 100.0 and _old_scale > 100.0):
        #print "snap 100:1"
        _new_scale = 100.0
        self.scale_stop_time = time.time()
              
      elif (_old_scale < 10.0 and _new_scale > 10.0) or (_new_scale < 10.0 and _old_scale > 10.0):
        #print "snap 10:1"
        _new_scale = 10.0
        self.scale_stop_time = time.time()
      
      elif (_old_scale < 1.0 and _new_scale > 1.0) or (_new_scale < 1.0 and _old_scale > 1.0):
        #print "snap 1:1"
        _new_scale = 1.0
        self.scale_stop_time = time.time()

      elif (_old_scale < 0.1 and _new_scale > 0.1) or (_new_scale < 0.1 and _old_scale > 0.1):
        #print "snap 1:10"
        _new_scale = 0.1
        self.scale_stop_time = time.time()


      elif (_old_scale < 0.01 and _new_scale > 0.01) or (_new_scale < 0.01 and _old_scale > 0.01):
        #print "snap 1:100"
        _new_scale = 0.01
        self.scale_stop_time = time.time()

      self.current_portal.set_scale(_new_scale)

    else:

      if (time.time() - self.scale_stop_time) > self.scale_stop_duration:
        self.scale_stop_time = None


  ## Called whenever sf_focus_button changes.
  @field_has_changed(sf_focus_button)
  def sf_focus_button_changed(self):

    # show and hide camera frame
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

      # capture a new portal
      if self.current_portal == None:
        _portal = self.PORTAL_MANAGER.add_portal(self.camera_frame.WorldTransform.value, 
                                                 self.camera_frame.WorldTransform.value,
                                                 1.0,
                                                 1.0,
                                                 self.capture_viewing_mode,
                                                 "PERSPECTIVE",
                                                 self.capture_parallax_mode,
                                                 "data/materials/ShadelessBlue.gmd")
        self.captured_portals.append(_portal)
        _portal.portal_matrix_node.Transform.connect_from(self.camera_frame.WorldTransform)
        self.current_portal = _portal

      # initiate dragging
      else:

        self.start_drag_portal_mat = self.tracking_reader.sf_abs_mat.value
        self.start_drag_scene_mat = self.current_portal.scene_matrix_node.Transform.value

    # capture button released
    else:

      self.start_drag_portal_mat = None
      self.start_drag_scene_mat = None

  ## Called whenever sf_next_rec_button changes.
  @field_has_changed(sf_next_rec_button)
  def sf_next_rec_button_changed(self):
    if self.sf_next_rec_button.value == True:

      # update focus in gallery mode
      if self.gallery_activated:
        if (self.gallery_focus_portal_index == self.next_focus_portal_index):
          self.next_focus_portal_index = min(self.gallery_focus_portal_index + 1, len(self.captured_portals) - 1)
          return
      
      # move to next recording in open mode
      if self.current_portal != None:
        self.current_portal.set_visibility(False)

        _current_index = self.captured_portals.index(self.current_portal)
        _current_index += 1
        _current_index = _current_index % len(self.captured_portals)

        self.current_portal = self.captured_portals[_current_index]
        self.current_portal.set_visibility(True)


  ## Called whenever sf_prior_rec_button changes.
  @field_has_changed(sf_prior_rec_button)
  def sf_prior_rec_button_changed(self):
    if self.sf_prior_rec_button.value == True:

      # update focus in gallery mode
      if self.gallery_activated:
        if (self.gallery_focus_portal_index == self.next_focus_portal_index):
          self.next_focus_portal_index = max(self.gallery_focus_portal_index - 1, 0)
          return
      
      # move to prior recording in open mode
      if self.current_portal != None:
        self.current_portal.set_visibility(False)

        _current_index = self.captured_portals.index(self.current_portal)
        _current_index -= 1
        _current_index = _current_index % len(self.captured_portals)

        self.current_portal = self.captured_portals[_current_index]
        self.current_portal.set_visibility(True)


  ## Called whenever sf_open_button changes.
  @field_has_changed(sf_open_close_button)
  def sf_open_button_changed(self):
    if self.sf_open_close_button.value == True:

      # open lastly opened portal when no portal is opened
      if self.current_portal == None and len(self.captured_portals) > 0:
        self.current_portal = self.captured_portals[self.last_open_portal_index]
        self.current_portal.set_visibility(True)

      # close currently opened portal
      elif self.current_portal != None:
        self.current_portal.set_visibility(False)
        self.last_open_portal_index = self.captured_portals.index(self.current_portal)
        self.current_portal = None


  ## Called whenever sf_delete_button changes.
  @field_has_changed(sf_delete_button)
  def sf_delete_button_changed(self):
    if self.sf_delete_button.value == True:

      # delete current portal
      if self.current_portal != None and self.gallery_focus_portal_index == self.next_focus_portal_index:
        _portal_to_delete = self.current_portal
        self.gallery_focus_portal_index = max(self.captured_portals.index(_portal_to_delete) - 1, 0)
        self.next_focus_portal_index = max(self.captured_portals.index(_portal_to_delete) - 1, 0)
        self.last_open_portal_index = max(self.captured_portals.index(_portal_to_delete) - 1, 0)

        self.captured_portals.remove(_portal_to_delete)
        self.PORTAL_MANAGER.remove_portal(_portal_to_delete.id)
        self.current_portal = None

  ## Called whenever sf_gallery_button changes.
  @field_has_changed(sf_gallery_button)
  def sf_gallery_button_changed(self):
    if self.sf_gallery_button.value == True:

      # open gallery when not opened
      if self.gallery_activated == False:
        self.gallery_activated = True
      
      # close gallery when opened, trigger correct portal visibilities
      else:
        
        if self.gallery_focus_portal_index != self.next_focus_portal_index:
          self.gallery_focus_portal_index = self.next_focus_portal_index

        self.gallery_activated = False
        self.last_open_portal_index = self.gallery_focus_portal_index
        self.current_portal = None

        for _portal in self.captured_portals:
          _portal.set_visibility(False)
          _portal.portal_matrix_node.Transform.connect_from(self.camera_frame.WorldTransform)

  ## Called whenever sf_scene_copy_button_changes.
  @field_has_changed(sf_scene_copy_button)
  def sf_scene_copy_button_changed(self):
    if self.sf_scene_copy_button.value == True:
      
      # create a free copy of the opened portal in the scene
      if self.current_portal != None and self.gallery_activated == False:

        _portal = self.PORTAL_MANAGER.add_portal(self.current_portal.scene_matrix_node.Transform.value, 
                                                 self.current_portal.portal_matrix_node.Transform.value,
                                                 1.0,
                                                 1.0,
                                                 self.current_portal.viewing_mode,
                                                 self.current_portal.camera_mode,
                                                 self.current_portal.negative_parallax,
                                                 self.current_portal.border_material)
        self.free_portals.append(_portal)

      
  ## Called whenever sf_2D_mode_button changes.
  @field_has_changed(sf_2D_mode_button)
  def sf_2D_mode_button_changed(self):
    if self.sf_2D_mode_button.value == True:
      
      # switch mode of currently opened portal
      if self.current_portal != None:
        if self.current_portal.viewing_mode == "3D":
          self.current_portal.switch_viewing_mode()

      # switch capture_viewing_mode
      else:
        self.capture_viewing_mode = "2D"
        self.viewing_mode_indicator.Material.value = 'data/materials/CameraMode2D.gmd'

  ## Called whenever sf_3D_mode_button changes.
  @field_has_changed(sf_3D_mode_button)
  def sf_3D_mode_button_changed(self):
    if self.sf_3D_mode_button.value == True:
      
      # switch mode of currently opened portal
      if self.current_portal != None:
        if self.current_portal.viewing_mode == "2D":
          self.current_portal.switch_viewing_mode()
      
      # switch capture_viewing_mode
      else:
        self.capture_viewing_mode = "3D"
        self.viewing_mode_indicator.Material.value = 'data/materials/CameraMode3D.gmd'


  ## Called whenever sf_negative_parallax_on_button changes.
  @field_has_changed(sf_negative_parallax_on_button)
  def sf_negative_parallax_on_button_changed(self):
    if self.sf_negative_parallax_on_button.value == True:
      
      # switch mode of currently opened portal
      if self.current_portal != None:
        if self.current_portal.negative_parallax == "False":
          self.current_portal.switch_negative_parallax()

      # switch capture_parallax_mode
      else:
        self.capture_parallax_mode = "True"


  ## Called whenever sf_negative_parallax_off_button changes.
  @field_has_changed(sf_negative_parallax_off_button)
  def sf_negative_parallax_off_button_changed(self):
    if self.sf_negative_parallax_off_button.value == True:
      
      # switch mode of currently opened portal portal
      if self.current_portal != None:
        if self.current_portal.negative_parallax == "True":
          self.current_portal.switch_negative_parallax()

      # switch capture_parallax_mode
      else:
        self.capture_parallax_mode = "False"