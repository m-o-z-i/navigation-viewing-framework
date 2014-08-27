#!/usr/bin/python

## @file
# Contains classes Shot and PortalCamera.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from DisplayGroup import *
from Portal import *
from StaticNavigation import *
from TrackingReader import *
from Tool import *
import Utilities

# import python libraries
import time
import math

## Class representing the parameters of a captured photo by a PortalCamera.
class Shot(avango.script.Script):

  ## @var sf_platform_mat
  # Field representing the platform matrix of this shot.
  sf_platform_mat = avango.gua.SFMatrix4()

  ## @var sf_platform_scale
  # Field representing the platform scale of this shot.
  sf_platform_scale = avango.SFFloat()

  ## @var sf_viewing_mode
  # Field representing the viewing mode of this shot.
  sf_viewing_mode = avango.SFString()

  ## @var sf_camera_mode
  # Field representing the camera mode of this shot.
  sf_camera_mode = avango.SFString()

  ## @var sf_negative_parallax
  # Field representing the negative parallax state of this shot.
  sf_negative_parallax = avango.SFString()

  ## Default constructor.
  def __init__(self):
    self.super(Shot).__init__()
    self.associated_portal_instance = None

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
  def my_constructor(self
                   , PLATFORM_MATRIX
                   , PLATFORM_SCALE
                   , VIEWING_MODE
                   , CAMERA_MODE
                   , NEGATIVE_PARALLAX):
    
    self.sf_platform_mat.value = PLATFORM_MATRIX
    self.sf_platform_scale.value = PLATFORM_SCALE
    self.sf_viewing_mode.value = VIEWING_MODE
    self.sf_camera_mode.value = CAMERA_MODE
    self.sf_negative_parallax.value = NEGATIVE_PARALLAX

  ## Tells this Shot that it was loaded into a Portal instance and is now being displayed.
  # @param PORTAL_INSTANCE The Portal instance in which this Shot was loaded.
  def assign_portal(self, PORTAL_INSTANCE):

    self.associated_portal_instance = PORTAL_INSTANCE
    self.associated_portal_instance.set_platform_matrix(self.sf_platform_mat.value)
    self.associated_portal_instance.set_platform_scale(self.sf_platform_scale.value)

    if self.associated_portal_instance.viewing_mode != self.sf_viewing_mode.value:
      self.associated_portal_instance.switch_viewing_mode()

    if self.associated_portal_instance.camera_mode != self.sf_camera_mode.value:
      self.associated_portal_instance.switch_camera_mode()

    if self.associated_portal_instance.negative_parallax != self.sf_negative_parallax.value:
      self.associated_portal_instance.switch_negative_parallax()

    PORTAL_INSTANCE.set_visibility(True)

  ## Tells this Shot that no portal instance is associated anymore.
  def deassign_portal(self):

    if self.associated_portal_instance != None:
      self.associated_portal_instance.set_visibility(False)
      self.associated_portal_instance = None

  ## Modifies the scene matrix (platform matrix and platform scale) by the input values given from a device.
  # @param DEVICE_INPUT_VALUES List of input values from a device.
  # @param OFFSET_MAT Offset matrix to be applied to the translation and rotation.
  def modify_scene_matrix(self, DEVICE_INPUT_VALUES = [0,0,0,0,0,0,0], OFFSET_MAT = avango.gua.make_identity_mat):

    _x = DEVICE_INPUT_VALUES[0]
    _y = DEVICE_INPUT_VALUES[1]
    _z = DEVICE_INPUT_VALUES[2]
    _rx = DEVICE_INPUT_VALUES[3]
    _ry = DEVICE_INPUT_VALUES[4]
    _rz = DEVICE_INPUT_VALUES[5]
    _w = DEVICE_INPUT_VALUES[6]

    if _w == -1:
      self.set_scale(self.sf_platform_scale.value * 0.985)
    elif _w == 1:
      self.set_scale(self.sf_platform_scale.value * 1.015)

    _trans_vec = avango.gua.Vec3(_x, _y, _z)
    _rot_vec = avango.gua.Vec3(_rx, _ry, _rz)

    if _trans_vec.length() != 0.0 or _rot_vec.length() != 0.0:

      # object metaphor
      _transformed_trans_vec = avango.gua.make_rot_mat(self.sf_platform_mat.value.get_rotate_scale_corrected()) * avango.gua.Vec3(_x*-1.0, _z, _y*-1.0)
      _transformed_trans_vec = OFFSET_MAT * _transformed_trans_vec
      _transformed_trans_vec = avango.gua.Vec3(_transformed_trans_vec.x, _transformed_trans_vec.y, _transformed_trans_vec.z)
      _transformed_trans_vec *= self.sf_platform_scale.value

      _rot_vec = OFFSET_MAT * _rot_vec

      _new_platform_matrix = avango.gua.make_trans_mat(_transformed_trans_vec) * \
                             self.sf_platform_mat.value * \
                             avango.gua.make_rot_mat( _rot_vec.y, 0, 0, -1) * \
                             avango.gua.make_rot_mat( _rot_vec.x, -1, 0, 0) * \
                             avango.gua.make_rot_mat( _rot_vec.z, 0, 1, 0)

      self.sf_platform_mat.value = _new_platform_matrix

  ## Sets the scale of this shot and snaps at specific scalings.
  # @param SCALE The new scale value to be set.
  def set_scale(self, SCALE):
 
    if self.scale_stop_time == None:
  
      _old_scale = self.sf_platform_scale.value
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

      self.sf_platform_scale.value = _new_scale

    else:

      if (time.time() - self.scale_stop_time) > self.scale_stop_duration:
        self.scale_stop_time = None

  ## Called whenever sf_platform_mat changes.
  @field_has_changed(sf_platform_mat)
  def sf_platform_mat_changed(self):
    if self.associated_portal_instance != None:
      self.associated_portal_instance.set_platform_matrix(self.sf_platform_mat.value)

  ## Called whenever sf_platform_scale changes.
  @field_has_changed(sf_platform_scale)
  def sf_platform_scale_changed(self):
    if self.associated_portal_instance != None:
      self.associated_portal_instance.set_platform_scale(self.sf_platform_scale.value)

  ## Called whenever sf_viewing_mode changes.
  @field_has_changed(sf_viewing_mode)
  def sf_viewing_mode_changed(self):
    if self.associated_portal_instance != None and \
       self.associated_portal_instance.viewing_mode != self.sf_viewing_mode.value:

      self.associated_portal_instance.switch_viewing_mode()

  ## Called whenever sf_camera_mode changes.
  @field_has_changed(sf_camera_mode)
  def sf_camera_mode_changed(self):
    if self.associated_portal_instance != None and \
       self.associated_portal_instance.camera_mode != self.sf_camera_mode.value:

      self.associated_portal_instance.switch_camera_mode()

  ## Called whenever sf_negative_parallax changes.
  @field_has_changed(sf_negative_parallax)
  def sf_negative_parallax_changed(self):
    if self.associated_portal_instance != None and \
       self.associated_portal_instance.negative_parallax != self.sf_negative_parallax.value:

      self.associated_portal_instance.switch_negative_parallax()

###############################################################################################

## Geometric representation of a PortalCamera in a DisplayGroup.
class PortalCameraRepresentation(ToolRepresentation):

  ##
  #
  sf_portal_matrix = avango.gua.SFMatrix4()
  sf_portal_matrix.value = avango.gua.make_identity_mat()

  ## Default constructor.
  def __init__(self):
    self.super(PortalCameraRepresentation).__init__()

  ## Custom constructor.
  # @param 
  # @param DISPLAY_GROUP DisplayGroup instance for which this RayPointerRepresentation is responsible for. 
  # @param USER_REPRESENTATION Corresponding UserRepresentation instance under which's view_transform_node the RayPointerRepresentation is appended.
  def my_constructor(self, PORTAL_CAM_INSTANCE, DISPLAY_GROUP, USER_REPRESENTATION):
    
    # call base class constructor
    self.base_constructor(PORTAL_CAM_INSTANCE
                        , DISPLAY_GROUP
                        , USER_REPRESENTATION
                        , "portal_cam_" + str(PORTAL_CAM_INSTANCE.id)
                        , "self.tool_transform_node.Transform.value = self.DISPLAY_GROUP.offset_to_workspace * self.TOOL_INSTANCE.tracking_reader.sf_abs_mat.value")

    _loader = avango.gua.nodes.TriMeshLoader()


    ## @var camera_frame
    # Geometry node containing the PortalCamera's portal frame.
    self.camera_frame = _loader.create_geometry_from_file('camera_frame'
                                                        , 'data/objects/screen.obj'
                                                        , 'data/materials/ShadelessRed.gmd'
                                                        , avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.camera_frame.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.camera_frame.Transform.value = avango.gua.make_trans_mat(0.0, PORTAL_CAM_INSTANCE.portal_height/2, 0.0) * \
                                        avango.gua.make_scale_mat(PORTAL_CAM_INSTANCE.portal_width, PORTAL_CAM_INSTANCE.portal_height, 1.0)
    self.camera_frame.GroupNames.value.append("portal_invisible_group")
    self.camera_frame.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value)
    self.tool_transform_node.Children.value.append(self.camera_frame)

    ## @var viewing_mode_indicator
    # Tiny geometry in the border of the camera frame to illustrate the current state of self.capture_viewing_mode.
    self.viewing_mode_indicator = _loader.create_geometry_from_file('viewing_mode_indicator',
                                                                    'data/objects/plane.obj',
                                                                    'data/materials/CameraMode3D.gmd',
                                                                    avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.viewing_mode_indicator.Transform.value = avango.gua.make_trans_mat(-PORTAL_CAM_INSTANCE.portal_width/2 * 0.86, PORTAL_CAM_INSTANCE.portal_height * 0.93, 0.0) * \
                                                  avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                                  avango.gua.make_scale_mat(PORTAL_CAM_INSTANCE.portal_height * 0.1, 1.0, PORTAL_CAM_INSTANCE.portal_height * 0.1)
    self.viewing_mode_indicator.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.viewing_mode_indicator.GroupNames.value.append("portal_invisible_group")
    self.viewing_mode_indicator.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value)
    self.tool_transform_node.Children.value.append(self.viewing_mode_indicator)

    
    self.portal = Portal(PORTAL_MATRIX = avango.gua.make_identity_mat()
                       , WIDTH = PORTAL_CAM_INSTANCE.portal_width
                       , HEIGHT = PORTAL_CAM_INSTANCE.portal_height
                       , VIEWING_MODE = PORTAL_CAM_INSTANCE.capture_viewing_mode
                       , CAMERA_MODE = "PERSPECTIVE"
                       , NEGATIVE_PARALLAX = PORTAL_CAM_INSTANCE.capture_parallax_mode
                       , BORDER_MATERIAL = "data/materials/White.gmd"
                       , TRANSITABLE = False)

    self.portal_nav = StaticNavigation()
    self.portal_nav.my_constructor(STATIC_ABS_MAT = avango.gua.make_trans_mat(-12.0, 17.3, -7.0)
                            , STATIC_SCALE = 1.0
                            , TRACE_VISIBILITY_LIST = {})

    self.portal_dg = DisplayGroup(ID = None
                           , DISPLAY_LIST = [self.portal]
                           , NAVIGATION_LIST = [self.portal_nav]
                           , VISIBILITY_TAG = "portal"
                           , OFFSET_TO_WORKSPACE = avango.gua.make_identity_mat()
                           , WORKSPACE_TRANSMITTER_OFFSET = avango.gua.make_identity_mat()
                           )

    ##
    #
    self.portal_matrix_connected = False


  def evaluate(self):

    # base class evaluate
    exec self.transformation_policy

    # wait for portal matrix node, then connect it if not already done
    if self.portal_matrix_connected == False:

      try:
        self.portal.portal_matrix_node
      except:
        return

      self.portal.connect_portal_matrix(self.sf_portal_matrix)
      self.portal.portal_matrix_node.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value)
      self.portal_matrix_connected = True
      self.portal.set_visibility(False)
  

    self.sf_portal_matrix.value = self.tool_transform_node.WorldTransform.value * \
                                  avango.gua.make_trans_mat(0.0, self.TOOL_INSTANCE.portal_height/2, 0.0)

  ##
  #
  def show_capture_frame(self):

    self.camera_frame.GroupNames.value.remove("portal_invisible_group")
    self.viewing_mode_indicator.GroupNames.value.remove("portal_invisible_group")

  ##
  #
  def hide_capture_frame(self):
    
    self.camera_frame.GroupNames.value.append("portal_invisible_group")
    self.viewing_mode_indicator.GroupNames.value.append("portal_invisible_group")

  ## Appends a string to the GroupNames field of this ToolRepresentation's visualization.
  # @param STRING The string to be appended.
  def append_to_visualization_group_names(self, STRING):
    
    # do not add portal head group nodes for visibility of this portal
    if not STRING.startswith("portal"):
      self.portal.portal_matrix_node.GroupNames.value.append(STRING)
      self.camera_frame.GroupNames.value.append(STRING)
      self.viewing_mode_indicator.GroupNames.value.append(STRING)


  ## Removes a string from the GroupNames field of this ToolRepresentation's visualization.
  # @param STRING The string to be removed.
  def remove_from_visualization_group_names(self, STRING):
    
    self.portal.portal_matrix_node.GroupNames.value.remove(STRING)
    self.camera_frame.GroupNames.value.remove(STRING)
    self.viewing_mode_indicator.GroupNames.value.remove(STRING)

  ## Resets the GroupNames field of this ToolRepresentation's visualization to the user representation's view_transform_node.
  def reset_visualization_group_names(self):

    self.portal.portal_matrix_node.GroupNames.value = [self.USER_REPRESENTATION.view_transform_node.Name.value]
    self.camera_frame.GroupNames.value = ["portal_invisible_group", self.USER_REPRESENTATION.view_transform_node.Name.value]
    self.viewing_mode_indicator.GroupNames.value = ["portal_invisible_group", self.USER_REPRESENTATION.view_transform_node.Name.value]
    

  ##
  def enable_highlight(self):

    self.portal.set_border_material("data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd")

  ##
  def disable_highlight(self):
    
    self.portal.set_border_material("data/materials/White.gmd")
    


###############################################################################################

## A PortalCamera is a physical device to interactively caputure, view
# and manipulate Portal instances in the scene.
class PortalCamera(Tool):
 
  ## @var sf_tracking_mat
  # Tracking matrix of the PortalCamera within the platform coordinate system.
  sf_tracking_mat = avango.gua.SFMatrix4()

  ## @var sf_world_border_mat_no_scale
  # World transformation of the camera frame without scaling. Used for Portal instantiation.
  sf_world_border_mat_no_scale = avango.gua.SFMatrix4()

  ## @var sf_animation_matrix
  # Matrix to which animated objects are connected to.
  sf_animation_matrix = avango.gua.SFMatrix4()

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

  ## @var sf_maximize_button
  # Boolean field to check if the maximize button was pressed.
  sf_maximize_button = avango.SFBool()

  ## @var sf_size_up_button
  # Boolean field to check if the size up button was pressed.
  sf_size_up_button = avango.SFBool()

  ## @var sf_size_down_button
  # Boolean field to check if the size down button was pressed.
  sf_size_down_button = avango.SFBool()

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

    ## @var captured_shots
    # List of Shot instances belonging to this PortalCamera.
    self.captured_shots = []

    ## @var current_shot
    # Shot instance which is currently displayed above the PortalCamera.
    self.current_shot = None

    ## @var portal_width
    # Width of the portals displayed in this PortalCamera.
    self.portal_width = 0.35

    ## @var portal_height
    # Height of the portals displayed in this PortalCamera.
    self.portal_height = 0.35

    ## @var capture_viewing_mode
    # Viewing mode with which new portals will be created.
    self.capture_viewing_mode = "3D"

    ## @var capture_parallax_mode
    # Negative parallax mode with which new portals will be created.
    self.capture_parallax_mode = "False"

    ## @var gallery_activated
    # Boolean indicating if the gallery is currently visible for this PortalCamera.
    self.gallery_activated = False

    ## @var gallery_focus_shot_index
    # Index within self.captured_shots saying which of the Shots is currently in the gallery's focus.
    self.gallery_focus_shot_index = 0

    ## @var gallery_magification_factor
    # Factor with which the size of the portals will be multiplied when in gallery mode.
    self.gallery_magnification_factor = 1.5

    ## @var interaction_spaces
    # List of PortalInteractionSpace instances currently associated with this PortalCamera.
    self.interaction_spaces = []

    ## @var animation_start_time
    # Starting time of an animation handled by this class.
    self.animation_start_time = None

    ## @var animation_start_matrix
    # Starting matrix of an animation handled by this class.
    self.animation_start_matrix = None

    ## @var animation_start_size
    # Starting size of an animation handled by this class.
    self.animation_start_size = None

    ## @var animation_duration
    # Duration of an animation handled by this class.
    self.animation_duration = 1.0


  ## Custom constructor.
  # @param 
  def my_constructor(self, WORKSPACE_INSTANCE, TOOL_ID, CAMERA_TRACKING_STATION, CAMERA_DEVICE_STATION, VISIBILITY_TABLE):

    # call base class constructor
    self.base_constructor(WORKSPACE_INSTANCE, TOOL_ID, CAMERA_TRACKING_STATION, VISIBILITY_TABLE)

    ## @var device_sensor
    # Device sensor for the PortalCamera's button inputs.
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = CAMERA_DEVICE_STATION

    # init field connections
    self.sf_focus_button.connect_from(self.device_sensor.Button0)
    self.sf_capture_button.connect_from(self.device_sensor.Button1)
    self.sf_next_rec_button.connect_from(self.device_sensor.Button5)
    self.sf_prior_rec_button.connect_from(self.device_sensor.Button4)
    self.sf_scale_up_button.connect_from(self.device_sensor.Button9)
    self.sf_scale_down_button.connect_from(self.device_sensor.Button10)
    self.sf_open_close_button.connect_from(self.device_sensor.Button6)
    self.sf_delete_button.connect_from(self.device_sensor.Button15)
    self.sf_gallery_button.connect_from(self.device_sensor.Button11)
    #self.sf_scene_copy_button.connect_from(self.device_sensor.Button14)
    self.sf_maximize_button.connect_from(self.device_sensor.Button14)
    self.sf_size_up_button.connect_from(self.device_sensor.Button3)
    self.sf_size_down_button.connect_from(self.device_sensor.Button2)
    self.sf_2D_mode_button.connect_from(self.device_sensor.Button7)
    self.sf_3D_mode_button.connect_from(self.device_sensor.Button8)
    self.sf_negative_parallax_on_button.connect_from(self.device_sensor.Button12)
    self.sf_negative_parallax_off_button.connect_from(self.device_sensor.Button13)

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var last_open_shot_index
    # Index within self.captured_shots saying which of the Shots was lastly opened by the PortalCamera.
    self.last_open_shot_index = None

    ## @var drag_last_frame_camera_mat
    # Matrix containing the value of the tracking target of the last frame when in drag mode.
    self.drag_last_frame_camera_mat = None

    # set evaluation policy
    self.always_evaluate(True)


  ## Creates a PortalCamearRepresentation for this RayPointer at a DISPLAY_GROUP.
  # @param DISPLAY_GROUP The DisplayGroup instance to create the representation for.
  # @param USER_REPRESENTATION The UserRepresentation this representation will belong to.
  def create_tool_representation_for(self, DISPLAY_GROUP, USER_REPRESENTATION):

    _portal_cam_repr = PortalCameraRepresentation()
    _portal_cam_repr.my_constructor(self, DISPLAY_GROUP, USER_REPRESENTATION)
    self.tool_representations.append(_portal_cam_repr)
    return _portal_cam_repr

  ## Checks which user is closest to this RayPointer in tracking spaces and makes him the assigned user.
  # Additionally updates the material of the corresponding RayPointerRepresentation.
  def check_for_user_assignment(self):

    _assigned_user_before = self.assigned_user
    self.super(PortalCamera).check_for_user_assignment()
    _assigned_user_after = self.assigned_user

    # Change material on assigned ray holder
    if _assigned_user_before != _assigned_user_after:

      for _tool_repr in self.tool_representations:

        if _tool_repr.user_id == self.assigned_user.id:
          _tool_repr.enable_highlight()
        else:
          _tool_repr.disable_highlight()

  ## Evaluated every frame.
  def evaluate(self):

    # update user assignment
    self.check_for_user_assignment()

    #self.viewing_mode_indicator.Transform.value = avango.gua.make_trans_mat(-self.portal_width/2 * 0.86, self.portal_height * 0.93, 0.0) * \
    #                                              avango.gua.make_rot_mat(90, 1, 0, 0) * \
    #                                              avango.gua.make_scale_mat(self.portal_height * 0.1, 1.0, self.portal_height * 0.1)

    '''
    # always hide red camera frame when a shot is displayed
    if self.current_shot != None:
      self.portal_camera_node.GroupNames.value = ["do_not_display_group"]
    
    # apply scale changes 
    if self.sf_scale_up_button.value == True and self.current_shot != None:
      
      self.set_current_shot_scale(self.current_shot.sf_platform_scale.value * 0.985)
      
    if self.sf_scale_down_button.value == True and self.current_shot != None:

      self.set_current_shot_scale(self.current_shot.sf_platform_scale.value * 1.015)
    
    
    # apply size changes
    if self.sf_size_up_button.value == True:
      self.portal_width += 0.005
      self.portal_height += 0.005
      self.display_portal.set_size(self.portal_width, self.portal_height)

    if self.sf_size_down_button.value == True:
      self.portal_width -= 0.005
      self.portal_height -= 0.005
      
      if self.portal_width < 0.15:
        self.portal_width = 0.15

      if self.portal_height < 0.15:
        self.portal_height = 0.15

      self.display_portal.set_size(self.portal_width, self.portal_height)

    # update matrices in drag mode
    if self.drag_last_frame_camera_mat != None:

      _current_camera_mat = self.tracking_reader.sf_abs_mat.value * avango.gua.make_trans_mat(0.0, self.portal_height/2, 0.0)
      _drag_input_mat = avango.gua.make_inverse_mat(self.drag_last_frame_camera_mat) * _current_camera_mat
      _drag_input_mat.set_translate(_drag_input_mat.get_translate() * self.current_shot.sf_platform_scale.value)

      _new_scene_mat = self.current_shot.sf_platform_mat.value * _drag_input_mat

      self.current_shot.sf_platform_mat.value = _new_scene_mat

      self.drag_last_frame_camera_mat = _current_camera_mat

    # check for camera hitting free portals
    _camera_vec = self.camera_frame.WorldTransform.value.get_translate()

    if self.current_shot == None:

      for _free_portal in self.PORTAL_MANAGER.free_portals:

        _portal_vec = _free_portal.portal_matrix_node.WorldTransform.value.get_translate()

        if self.check_for_hit(_camera_vec, _portal_vec):

          _shot = Shot()
          _shot.my_constructor(_free_portal.platform_matrix,
                               _free_portal.platform_scale,
                               _free_portal.viewing_mode,
                               _free_portal.camera_mode,
                               _free_portal.negative_parallax)

          self.captured_shots.append(_shot)
          _shot.assign_portal(self.display_portal)
          self.current_shot = _shot

          self.PORTAL_MANAGER.free_portals.remove(_free_portal)
          self.PORTAL_MANAGER.remove_portal(_free_portal.id)
          return

    # check for animations
    if self.animation_start_time != None:

      _time_step = time.time() - self.animation_start_time

      if _time_step > self.animation_duration:
        self.animation_start_time = None
        self.animation_start_matrix = None
        self.animation_start_size = None
        self.display_portal.connect_portal_matrix(self.sf_world_border_mat_no_scale)
        self.display_portal.set_size(self.portal_width, self.portal_height)
        return

      _ratio = _time_step / self.animation_duration
      _start_trans = self.animation_start_matrix.get_translate()
      _end_trans = self.sf_world_border_mat_no_scale.value.get_translate()
      _animation_trans = _start_trans.lerp_to(_end_trans, _ratio)

      _start_rot = self.animation_start_matrix.get_rotate_scale_corrected()
      _end_rot = self.sf_world_border_mat_no_scale.value.get_rotate_scale_corrected()
      _animation_rot = _start_rot.slerp_to(_end_rot, _ratio)

      _start_scale = self.animation_start_matrix.get_scale()
      _end_scale = self.sf_world_border_mat_no_scale.value.get_scale()
      _animation_scale = _start_scale * (1-_ratio) + _end_scale * _ratio

      _start_size = self.animation_start_size
      _end_size = avango.gua.Vec3(self.portal_width, self.portal_height, 1.0)
      _animation_size = _start_size.lerp_to(_end_size, _ratio)

      self.sf_animation_matrix.value = avango.gua.make_trans_mat(_animation_trans) * \
                                       avango.gua.make_rot_mat(_animation_rot) * \
                                       avango.gua.make_scale_mat(_animation_scale)
      self.display_portal.set_size(_animation_size.x, _animation_size.y)
      return

    # update matrices in gallery mode
    if self.gallery_activated:

      # disable gallery when no captured shots are present (anymore)
      if len(self.captured_shots) == 0:
        self.gallery_activated = False

        for _gallery_portal in self.gallery_portals:
          _gallery_portal.set_visibility(False)

        return

      # place gallery correctly over device
      if len(self.captured_shots) < len(self.gallery_portals):
        _num_displayed_portals = len(self.captured_shots)
      else:
        _num_displayed_portals = len(self.gallery_portals)

      _increment_index = int(math.floor(-_num_displayed_portals / 2) + 1)
      _increment_place = (-_num_displayed_portals / 2.0) + 0.5

      for _gallery_portal in self.gallery_portals:

        if self.gallery_portals.index(_gallery_portal) > _num_displayed_portals - 1:
          _gallery_portal.set_visibility(False)
          break

        _station_mat = self.NAVIGATION.device.sf_station_mat.value
        _station_vec = _station_mat.get_translate()

        _modified_station_mat = avango.gua.make_trans_mat(_station_vec.x + self.gallery_magnification_factor * (0.3 + 0.2 * 0.3) * _increment_place, _station_vec.y + 1.5 * 0.3, _station_vec.z)

        _matrix = self.NAVIGATION.platform.platform_scale_transform_node.WorldTransform.value * \
                  avango.gua.make_trans_mat(_station_vec) * \
                  avango.gua.make_rot_mat(_station_mat.get_rotate()) * \
                  avango.gua.make_trans_mat(_station_vec * -1) * \
                  _modified_station_mat * \
                  avango.gua.make_scale_mat(self.gallery_magnification_factor, self.gallery_magnification_factor, 1.0)

        _gallery_portal.portal_matrix_node.Transform.value = _matrix

        _shot_index = self.gallery_focus_shot_index
        _shot_index += _increment_index
        _shot_index = _shot_index % len(self.captured_shots)

        _shot_instance = self.captured_shots[_shot_index]
        #_shot_instance.deassign_portal()
        _shot_instance.assign_portal(_gallery_portal)

        _increment_index += 1
        _increment_place += 1.0
    '''


  ## Checks if the position of a camera is close to the position of a portal.
  # @param CAMERA_VEC The camera's vector to be used for incidence computation.
  # @param PORTAL_VEC The portal's vector to be used for incidence computation.
  def check_for_hit(self, CAMERA_VEC, PORTAL_VEC):

    _nav_scale = self.NAVIGATION.inputmapping.sf_scale.value

    if CAMERA_VEC.x > PORTAL_VEC.x - (self.portal_width/2) * _nav_scale and \
       CAMERA_VEC.x < PORTAL_VEC.x + (self.portal_width/2) * _nav_scale and \
       CAMERA_VEC.y > PORTAL_VEC.y - 0.1 * _nav_scale and \
       CAMERA_VEC.y < PORTAL_VEC.y + 0.1 * _nav_scale and \
       CAMERA_VEC.z > PORTAL_VEC.z - 0.05 * _nav_scale and \
       CAMERA_VEC.z < PORTAL_VEC.z + 0.05 * _nav_scale:

      return True

    return False


  ## Associates a PortalInteractionSpace with this PortalCamera instance.
  # @param INTERACTION_SPACE The PortalInteractionSpace to be added.
  def add_interaction_space(self, INTERACTION_SPACE):

    self.interaction_spaces.append(INTERACTION_SPACE)

  ## Sets the scale of the currently active shot or returns when no shot is active.
  # @param SCALE The new scale to be set.
  def set_current_shot_scale(self, SCALE):

    if self.current_shot == None:
      return
    else:
      self.current_shot.set_scale(SCALE)

  ## Called whenever sf_focus_button changes.
  @field_has_changed(sf_focus_button)
  def sf_focus_button_changed(self):

    # show and hide camera frame
    if self.sf_focus_button.value == True:

      for _tool_repr in self.tool_representations:
        _tool_repr.show_capture_frame()

    else:

      for _tool_repr in self.tool_representations:
        _tool_repr.hide_capture_frame()

  ## Called whenever sf_capture_button changes.
  @field_has_changed(sf_capture_button)
  def sf_capture_button_changed(self):
    if self.sf_capture_button.value == True:

      # capture a new portal
      if self.current_shot == None:

        _shot_platform_matrix = self.sf_world_border_mat_no_scale.value * \
                                avango.gua.make_inverse_mat(avango.gua.make_scale_mat(self.NAVIGATION.inputmapping.sf_scale.value))

        _shot = Shot()
        _shot.my_constructor(_shot_platform_matrix,
                             self.NAVIGATION.inputmapping.sf_scale.value,
                             self.capture_viewing_mode,
                             "PERSPECTIVE",
                             self.capture_parallax_mode)

        self.captured_shots.append(_shot)
        _shot.assign_portal(self.display_portal)
        self.current_shot = _shot

      # initiate dragging
      else:

        self.drag_last_frame_camera_mat = self.tracking_reader.sf_abs_mat.value * \
                                          avango.gua.make_trans_mat(0.0, self.portal_height/2, 0.0)

    # capture button released, stop dragging
    else:

      self.drag_last_frame_camera_mat = None

  ## Called whenever sf_next_rec_button changes.
  @field_has_changed(sf_next_rec_button)
  def sf_next_rec_button_changed(self):
    if self.sf_next_rec_button.value == True:

      # update focus in gallery mode
      if self.gallery_activated:

          _shot_index = self.gallery_focus_shot_index
          _shot_index += 1
          _shot_index = _shot_index % len(self.captured_shots)
          
          self.gallery_focus_shot_index = _shot_index
          self.current_shot = self.captured_shots[self.gallery_focus_shot_index]
          return
      
      # move to next recording in open mode
      if self.current_shot != None:

        _current_index = self.captured_shots.index(self.current_shot)
        _current_index += 1
        _current_index = _current_index % len(self.captured_shots)

        self.current_shot = self.captured_shots[_current_index]
        self.current_shot.assign_portal(self.display_portal)


  ## Called whenever sf_prior_rec_button changes.
  @field_has_changed(sf_prior_rec_button)
  def sf_prior_rec_button_changed(self):
    if self.sf_prior_rec_button.value == True:

      # update focus in gallery mode
      if self.gallery_activated:
        
        _shot_index = self.gallery_focus_shot_index
        _shot_index -= 1
        _shot_index = _shot_index % len(self.captured_shots)
        
        self.gallery_focus_shot_index = _shot_index
        self.current_shot = self.captured_shots[self.gallery_focus_shot_index]
        return
      
      # move to prior recording in open mode
      if self.current_shot != None:

        _current_index = self.captured_shots.index(self.current_shot)
        _current_index -= 1
        _current_index = _current_index % len(self.captured_shots)

        self.current_shot = self.captured_shots[_current_index]
        self.current_shot.assign_portal(self.display_portal)


  ## Called whenever sf_open_button changes.
  @field_has_changed(sf_open_close_button)
  def sf_open_button_changed(self):
    if self.sf_open_close_button.value == True:

      # grab current gallery portal in gallery mode
      if self.gallery_activated:

        self.gallery_activated = False

        for _gallery_portal in self.gallery_portals:
          _gallery_portal.set_visibility(False)

        self.current_shot = self.captured_shots[self.gallery_focus_shot_index]
        self.current_shot.assign_portal(self.display_portal)

        return

      # open lastly opened portal when no portal is opened
      if self.current_shot == None and len(self.captured_shots) > 0:
        self.current_shot = self.captured_shots[self.last_open_shot_index]
        self.current_shot.assign_portal(self.display_portal)

      # close currently opened portal
      elif self.current_shot != None:
        self.current_shot.deassign_portal()
        self.last_open_shot_index = self.captured_shots.index(self.current_shot)
        self.current_shot = None


  ## Called whenever sf_delete_button changes.
  @field_has_changed(sf_delete_button)
  def sf_delete_button_changed(self):
    if self.sf_delete_button.value == True:

      # delete current portal
      if self.current_shot != None:
        _shot_to_delete = self.current_shot
        self.gallery_focus_shot_index = max(self.captured_shots.index(_shot_to_delete) - 1, 0)
        self.last_open_shot_index = max(self.captured_shots.index(_shot_to_delete) - 1, 0)
        _shot_to_delete.deassign_portal()

        self.captured_shots.remove(_shot_to_delete)
        del _shot_to_delete

        if self.gallery_activated and len(self.captured_shots) > 0:
          self.current_shot = self.captured_shots[self.gallery_focus_shot_index]
        else:
          self.current_shot = None

  ## Called whenever sf_gallery_button changes.
  @field_has_changed(sf_gallery_button)
  def sf_gallery_button_changed(self):
    if self.sf_gallery_button.value == True:

      # open gallery when not opened
      if self.gallery_activated == False:
        
        self.gallery_activated = True

        if self.current_shot != None:
          self.current_shot.deassign_portal()

        if len(self.captured_shots) > 0:
          self.current_shot = self.captured_shots[self.gallery_focus_shot_index]
      
      # close gallery when opened, trigger correct portal visibilities
      else:

        self.gallery_activated = False
        for _gallery_portal in self.gallery_portals:
          _gallery_portal.set_visibility(False)
        self.last_open_shot_index = self.gallery_focus_shot_index
        self.current_shot = None

  ## Called whenever sf_scene_copy_button changes.
  @field_has_changed(sf_scene_copy_button)
  def sf_scene_copy_button_changed(self):
    if self.sf_scene_copy_button.value == True:
      
      # create a free copy of the opened shot in the scene
      if self.current_shot != None and self.gallery_activated == False:

        _portal = self.PORTAL_MANAGER.add_portal(self.current_shot.sf_platform_mat.value,
                                                 self.current_shot.sf_platform_scale.value,
                                                 self.display_portal.portal_matrix_node.Transform.value,
                                                 self.display_portal.width,
                                                 self.display_portal.height,
                                                 self.current_shot.sf_viewing_mode.value,
                                                 self.current_shot.sf_camera_mode.value,
                                                 self.current_shot.sf_negative_parallax.value,
                                                 self.display_portal.border_material)
        self.PORTAL_MANAGER.free_portals.append(_portal)

  ## Called whenever sf_maximize_button changes.
  @field_has_changed(sf_maximize_button)
  def sf_maximize_button_changed(self):
    if self.sf_maximize_button.value == True:

      # check in which interaction space the PortalCamera is
      for _interaction_space in self.interaction_spaces:

        if _interaction_space.is_inside(self.tracking_reader.sf_abs_mat.value.get_translate()) and \
           self.gallery_activated == False:
          
          # push current portal to interaction space and maximize it
          if _interaction_space.maximized_shot == None:

            if self.current_shot == None or self.animation_start_time != None: # no shot to maximize
              return

            _shot = self.current_shot
            _shot.sf_negative_parallax.value = "True"

            # set correct forward angle in interaction space
            _camera_forward = math.degrees(Utilities.get_yaw(self.tracking_reader.sf_abs_mat.value))

            if _camera_forward < 135.0 and _camera_forward > 45.0:
              _interaction_space.maximize_forward_angle = _interaction_space.forward_angle
            elif _camera_forward < 225.0 and _camera_forward > 135.0:
              _interaction_space.maximize_forward_angle = _interaction_space.forward_angle + 90.0
            elif _camera_forward < 315.0 and _camera_forward > 225.0:
              _interaction_space.maximize_forward_angle = _interaction_space.forward_angle + 180.0
            else:
              _interaction_space.maximize_forward_angle = _interaction_space.forward_angle + 270.0

            self.last_open_shot_index = max(self.captured_shots.index(self.current_shot)-1, 0)
            self.gallery_focus_shot_index = max(self.captured_shots.index(self.current_shot)-1, 0)
            
            _shot.deassign_portal()
            self.captured_shots.remove(self.current_shot)
            self.current_shot = None
            _interaction_space.add_maximized_shot(_shot
                                                , self.display_portal.portal_matrix_node.WorldTransform.value
                                                , self.display_portal.width
                                                , self.display_portal.height)

          # grab portal from interaction space and resize it
          else:
            
            if self.current_shot != None:
              self.current_shot.deassign_portal()

            _shot = _interaction_space.remove_maximized_shot()

            if _shot != None:
              self.animation_start_time = time.time()
              self.animation_start_matrix = _interaction_space.sf_min_y_plane_transform.value
              self.sf_animation_matrix.value = self.animation_start_matrix
              self.animation_start_size = avango.gua.Vec3(_interaction_space.get_width()
                                                        , _interaction_space.get_height()
                                                        , 1.0)
              _shot.assign_portal(self.display_portal)
              self.current_shot = _shot
              self.display_portal.portal_matrix_node.Transform.disconnect()
              self.display_portal.connect_portal_matrix(self.sf_animation_matrix)
              self.captured_shots.append(_shot)

          return


  ## Called whenever sf_2D_mode_button changes.
  @field_has_changed(sf_2D_mode_button)
  def sf_2D_mode_button_changed(self):
    if self.sf_2D_mode_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:
        self.current_shot.sf_viewing_mode.value = "2D"

      # switch capture_viewing_mode
      else:
        self.capture_viewing_mode = "2D"
        self.viewing_mode_indicator.Material.value = 'data/materials/CameraMode2D.gmd'

  ## Called whenever sf_3D_mode_button changes.
  @field_has_changed(sf_3D_mode_button)
  def sf_3D_mode_button_changed(self):
    if self.sf_3D_mode_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:
        self.current_shot.sf_viewing_mode.value = "3D"
      
      # switch capture_viewing_mode
      else:
        self.capture_viewing_mode = "3D"
        self.viewing_mode_indicator.Material.value = 'data/materials/CameraMode3D.gmd'


  ## Called whenever sf_negative_parallax_on_button changes.
  @field_has_changed(sf_negative_parallax_on_button)
  def sf_negative_parallax_on_button_changed(self):
    if self.sf_negative_parallax_on_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:
        self.current_shot.sf_negative_parallax.value = "True"

      # switch capture_parallax_mode
      else:
        self.capture_parallax_mode = "True"


  ## Called whenever sf_negative_parallax_off_button changes.
  @field_has_changed(sf_negative_parallax_off_button)
  def sf_negative_parallax_off_button_changed(self):
    if self.sf_negative_parallax_off_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:
        self.current_shot.sf_negative_parallax.value = "False"

      # switch capture_parallax_mode
      else:
        self.capture_parallax_mode = "False"