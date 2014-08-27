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
from PortalCameraNavigation import *
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
  sf_abs_mat = avango.gua.SFMatrix4()

  ## @var sf_platform_scale
  # Field representing the platform scale of this shot.
  sf_scale = avango.SFFloat()

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

  ## Custom constructor.
  def my_constructor(self
                   , ABS_MAT
                   , SCALE
                   , VIEWING_MODE
                   , CAMERA_MODE
                   , NEGATIVE_PARALLAX):
    
    self.sf_abs_mat.value = ABS_MAT
    self.sf_scale.value = SCALE
    self.sf_viewing_mode.value = VIEWING_MODE
    self.sf_camera_mode.value = CAMERA_MODE
    self.sf_negative_parallax.value = NEGATIVE_PARALLAX


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
    self.camera_frame.Transform.value = avango.gua.make_trans_mat(0.0, self.TOOL_INSTANCE.portal_height/2, 0.0) * \
                                        avango.gua.make_scale_mat(self.TOOL_INSTANCE.portal_width, self.TOOL_INSTANCE.portal_height, 1.0)
    self.camera_frame.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.camera_frame.GroupNames.value.append("portal_invisible_group")
    self.camera_frame.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value)
    self.tool_transform_node.Children.value.append(self.camera_frame)

    ## @var viewing_mode_indicator
    # Tiny geometry in the border of the camera frame to illustrate the current state of self.capture_viewing_mode.
    self.viewing_mode_indicator = _loader.create_geometry_from_file('viewing_mode_indicator',
                                                                    'data/objects/plane.obj',
                                                                    'data/materials/CameraMode3D.gmd',
                                                                    avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.viewing_mode_indicator.Transform.value = avango.gua.make_trans_mat(-self.TOOL_INSTANCE.portal_width/2 * 0.86, self.TOOL_INSTANCE.portal_height * 0.93, 0.0) * \
                                                  avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                                  avango.gua.make_scale_mat(self.TOOL_INSTANCE.portal_height * 0.1, 1.0, self.TOOL_INSTANCE.portal_height * 0.1)
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

    self.portal_nav = PortalCameraNavigation()
    self.portal_nav.my_constructor(PORTAL_CAMERA_INSTANCE = self.TOOL_INSTANCE
                                 , TRACE_VISIBILITY_LIST = {})

    self.portal_dg = DisplayGroup(ID = None
                           , DISPLAY_LIST = [self.portal]
                           , NAVIGATION_LIST = [self.portal_nav]
                           , VISIBILITY_TAG = "portal"
                           , OFFSET_TO_WORKSPACE = avango.gua.make_identity_mat()
                           , WORKSPACE_TRANSMITTER_OFFSET = avango.gua.make_identity_mat()
                           )

    self.assigned_shot = None

    ##
    #
    self.portal_matrix_connected = False

    ##
    #
    self.highlighted = False


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

    # update border color according to highlight enabled
    if self.highlighted:
      if self.portal.border_material != "data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd":
        self.portal.set_border_material("data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd")
    else:
      if self.portal.border_material != "data/materials/White.gmd":
        self.portal.set_border_material("data/materials/White.gmd")

  ##
  #
  def update_size(self):

    self.camera_frame.Transform.value = avango.gua.make_trans_mat(0.0, self.TOOL_INSTANCE.portal_height/2, 0.0) * \
                                        avango.gua.make_scale_mat(self.TOOL_INSTANCE.portal_width, self.TOOL_INSTANCE.portal_height, 1.0)

    self.viewing_mode_indicator.Transform.value = avango.gua.make_trans_mat(-self.TOOL_INSTANCE.portal_width/2 * 0.86, self.TOOL_INSTANCE.portal_height * 0.93, 0.0) * \
                                                  avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                                  avango.gua.make_scale_mat(self.TOOL_INSTANCE.portal_height * 0.1, 1.0, self.TOOL_INSTANCE.portal_height * 0.1)

    self.portal.set_size(self.TOOL_INSTANCE.portal_width, self.TOOL_INSTANCE.portal_height)                                                  

  ##
  #
  def assign_shot(self, SHOT):

    if self.assigned_shot != None:
      self.assigned_shot.sf_abs_mat.disconnect()
      self.assigned_shot.sf_scale.disconnect()


    self.portal_nav.set_navigation_values(SHOT.sf_abs_mat.value, SHOT.sf_scale.value)

    if SHOT.sf_viewing_mode.value != self.portal.viewing_mode:
      self.portal.switch_viewing_mode()

    if SHOT.sf_camera_mode.value != self.portal.camera_mode:
      self.portal.switch_camera_mode()

    if SHOT.sf_negative_parallax.value != self.portal.negative_parallax:
      self.portal.switch_negative_parallax()

    SHOT.sf_abs_mat.disconnect()
    SHOT.sf_abs_mat.connect_from(self.portal_nav.sf_abs_mat)
    SHOT.sf_scale.disconnect()
    SHOT.sf_scale.connect_from(self.portal_nav.sf_scale)

    self.assigned_shot = SHOT

    self.portal.set_visibility(True)

  ##
  #
  def deassign_shot(self):

    self.assigned_shot.sf_abs_mat.disconnect()
    self.assigned_shot.sf_scale.disconnect()
    self.assigned_shot = None

    self.portal.set_visibility(False)

  ##
  #
  def set_viewing_mode(self, MODE):

    if self.portal.viewing_mode != MODE:
      self.portal.switch_viewing_mode()

  ##
  #
  def set_negative_parallax(self, MODE):

    if self.portal.negative_parallax != MODE:
      self.portal.switch_negative_parallax()

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
    
    self.highlighted = True

  ##
  def disable_highlight(self):
    
    self.highlighted = False
    


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

    # apply scale changes
    if self.sf_scale_up_button.value == True and self.current_shot != None:
      self.set_current_shot_scale(self.current_shot.sf_scale.value * 0.985)

    if self.sf_scale_down_button.value == True and self.current_shot != None:
      self.set_current_shot_scale(self.current_shot.sf_scale.value * 1.015)

    # apply size changes
    if self.sf_size_up_button.value == True:
      self.portal_width += 0.005
      self.portal_height += 0.005

      for _tool_repr in self.tool_representations:
        _tool_repr.update_size()

    if self.sf_size_down_button.value == True:
      self.portal_width -= 0.005
      self.portal_height -= 0.005
      
      if self.portal_width < 0.15:
        self.portal_width = 0.15

      if self.portal_height < 0.15:
        self.portal_height = 0.15

      for _tool_repr in self.tool_representations:
        _tool_repr.update_size()


  ## Sets the scale of the currently active shot or returns when no shot is active.
  # @param SCALE The new scale to be set.
  def set_current_shot_scale(self, SCALE):

    if self.current_shot == None:
      return
    else:

      self.current_shot.sf_scale.value = SCALE

      for _tool_repr in self.tool_representations:
        _tool_repr.portal_nav.set_navigation_values(_tool_repr.portal_nav.sf_abs_mat.value, SCALE)

  ##
  #
  def set_current_shot(self, SHOT):

    for _tool_repr in self.tool_representations:
      _tool_repr.assign_shot(SHOT)

    self.current_shot = SHOT

  ##
  #
  def clear_current_shot(self):

    for _tool_repr in self.tool_representations:
      _tool_repr.deassign_shot()

    self.current_shot = None

  ## Called whenever sf_focus_button changes.
  @field_has_changed(sf_focus_button)
  def sf_focus_button_changed(self):

    # show and hide camera frame
    if self.sf_focus_button.value == True and self.current_shot == None:

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

        _active_tool_representation = self.tool_representations[0]
        _active_navigation = _active_tool_representation.DISPLAY_GROUP.navigations[_active_tool_representation.USER_REPRESENTATION.connected_navigation_id]

        _shot_platform_matrix = _active_tool_representation.sf_portal_matrix.value * \
                                avango.gua.make_inverse_mat(avango.gua.make_scale_mat(_active_navigation.sf_scale.value))


        _shot = Shot()
        _shot.my_constructor(_shot_platform_matrix,
                             _active_navigation.sf_scale.value,
                             self.capture_viewing_mode,
                             "PERSPECTIVE",
                             self.capture_parallax_mode)

        self.captured_shots.append(_shot)
        self.set_current_shot(_shot)

  ## Called whenever sf_next_rec_button changes.
  @field_has_changed(sf_next_rec_button)
  def sf_next_rec_button_changed(self):
    if self.sf_next_rec_button.value == True:
      
      # move to next recording in open mode
      if self.current_shot != None:

        _current_index = self.captured_shots.index(self.current_shot)
        _current_index += 1
        _current_index = _current_index % len(self.captured_shots)

        _new_shot = self.captured_shots[_current_index]
        self.set_current_shot(_new_shot)


  ## Called whenever sf_prior_rec_button changes.
  @field_has_changed(sf_prior_rec_button)
  def sf_prior_rec_button_changed(self):
    if self.sf_prior_rec_button.value == True:
      
      # move to prior recording in open mode
      if self.current_shot != None:

        _current_index = self.captured_shots.index(self.current_shot)
        _current_index -= 1
        _current_index = _current_index % len(self.captured_shots)

        _new_shot = self.captured_shots[_current_index]
        self.set_current_shot(_new_shot)


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
        _new_shot = self.captured_shots[self.last_open_shot_index]
        self.set_current_shot(_new_shot)

      # close currently opened portal
      elif self.current_shot != None:
        self.last_open_shot_index = self.captured_shots.index(self.current_shot)
        self.clear_current_shot()


  ## Called whenever sf_delete_button changes.
  @field_has_changed(sf_delete_button)
  def sf_delete_button_changed(self):
    if self.sf_delete_button.value == True:

      # delete current portal
      if self.current_shot != None:
        _shot_to_delete = self.current_shot
        self.gallery_focus_shot_index = max(self.captured_shots.index(_shot_to_delete) - 1, 0)
        self.last_open_shot_index = max(self.captured_shots.index(_shot_to_delete) - 1, 0)
        self.clear_current_shot()

        self.captured_shots.remove(_shot_to_delete)
        del _shot_to_delete


  ## Called whenever sf_2D_mode_button changes.
  @field_has_changed(sf_2D_mode_button)
  def sf_2D_mode_button_changed(self):
    if self.sf_2D_mode_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:

        self.current_shot.sf_viewing_mode.value = "2D"

        for _tool_repr in self.tool_representations:
          _tool_repr.set_viewing_mode("2D")

      # switch capture_viewing_mode
      else:
        self.capture_viewing_mode = "2D"

        for _tool_repr in self.tool_representations:
          _tool_repr.viewing_mode_indicator.Material.value = 'data/materials/CameraMode2D.gmd'

  ## Called whenever sf_3D_mode_button changes.
  @field_has_changed(sf_3D_mode_button)
  def sf_3D_mode_button_changed(self):
    if self.sf_3D_mode_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:
        
        self.current_shot.sf_viewing_mode.value = "3D"

        for _tool_repr in self.tool_representations:
          _tool_repr.set_viewing_mode("3D")
      
      # switch capture_viewing_mode
      else:
        self.capture_viewing_mode = "3D"

        for _tool_repr in self.tool_representations:
          _tool_repr.viewing_mode_indicator.Material.value = 'data/materials/CameraMode3D.gmd'


  ## Called whenever sf_negative_parallax_on_button changes.
  @field_has_changed(sf_negative_parallax_on_button)
  def sf_negative_parallax_on_button_changed(self):
    if self.sf_negative_parallax_on_button.value == True:
      
      # switch mode of currently opened shot
      if self.current_shot != None:

        self.current_shot.sf_negative_parallax.value = "True"

        for _tool_repr in self.tool_representations:
          _tool_repr.set_negative_parallax("True")

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

        for _tool_repr in self.tool_representations:
          _tool_repr.set_negative_parallax("False")

      # switch capture_parallax_mode
      else:
        self.capture_parallax_mode = "False"