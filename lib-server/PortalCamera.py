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

  ## @var sf_abs_mat
  # Field representing the translation and rotation matrix of this shot.
  sf_abs_mat = avango.gua.SFMatrix4()

  ## @var sf_scale
  # Field representing the scaling of this shot.
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

  ## @var sf_portal_matrix
  # Field to which the portal entry matrices are connected to in order to appear above the PortalCamera.
  sf_portal_matrix = avango.gua.SFMatrix4()
  sf_portal_matrix.value = avango.gua.make_identity_mat()

  ## Default constructor.
  def __init__(self):
    self.super(PortalCameraRepresentation).__init__()

  ## Custom constructor.
  # @param PORTAL_CAMERA_INSTANCE An instance of PortalCamera to which this PortalCameraRepresentation is associated.
  # @param DISPLAY_GROUP DisplayGroup instance for which this PortalCameraRepresentation is responsible for. 
  # @param USER_REPRESENTATION Corresponding UserRepresentation instance under which's view_transform_node the PortalCameraRepresentation is appended.
  def my_constructor(self, PORTAL_CAMERA_INSTANCE, DISPLAY_GROUP, USER_REPRESENTATION):
    
    # call base class constructor
    self.base_constructor(PORTAL_CAMERA_INSTANCE
                        , DISPLAY_GROUP
                        , USER_REPRESENTATION
                        , "portal_cam_" + str(PORTAL_CAMERA_INSTANCE.id))

    ## @var portal
    # Portal display instance belonging to this representation.
    self.portal = Portal(PORTAL_MATRIX = avango.gua.make_identity_mat()
                       , WIDTH = PORTAL_CAMERA_INSTANCE.portal_width
                       , HEIGHT = PORTAL_CAMERA_INSTANCE.portal_height
                       , VIEWING_MODE = PORTAL_CAMERA_INSTANCE.capture_viewing_mode
                       , CAMERA_MODE = "PERSPECTIVE"
                       , NEGATIVE_PARALLAX = PORTAL_CAMERA_INSTANCE.capture_parallax_mode
                       , BORDER_MATERIAL = "data/materials/White.gmd"
                       , TRANSITABLE = False
                       , PORTAL_NODE_NAME_ATTACHMENT = "w" + str(PORTAL_CAMERA_INSTANCE.WORKSPACE_INSTANCE.id) + "_dg" + str(self.DISPLAY_GROUP.id))

    ## @var portal_nav
    # Instance of PortalCameraNavigation in which the captured shots are to be loaded.
    self.portal_nav = PortalCameraNavigation()
    self.portal_nav.my_constructor(PORTAL_CAMERA_INSTANCE = self.TOOL_INSTANCE)

    ## @var portal_dg
    # DisplayGroup opened up by the portal of this representation.
    self.portal_dg = DisplayGroup(ID = None
                           , DISPLAY_LIST = [self.portal]
                           , NAVIGATION_LIST = [self.portal_nav]
                           , VISIBILITY_TAG = "portal"
                           , OFFSET_TO_WORKSPACE = avango.gua.make_identity_mat()
                           , WORKSPACE_TRANSMITTER_OFFSET = avango.gua.make_identity_mat()
                           )

    ## @var assigned_shot
    # Shot instance which is currently displayed in the portal of this representation.
    self.assigned_shot = None

    ## @var highlighted
    # Boolean indicating if this representation is highlighted. Usually used to color the assigned user's representation.
    self.highlighted = False

    ## @var portal_matrix_connected
    # Boolean saying if the portal's portal matrix node was connected. Is done once it is present by evaluate().
    self.portal_matrix_connected = False

  ## Computes the WorldTransform of a scenegraph node manually without using the pre-defined field.
  # @param NODE The scenegraph node to compute the world transformation for.
  def compute_world_transform(self, NODE):

    if NODE == None:
      return avango.gua.make_identity_mat()
    else:   
      return self.compute_world_transform(NODE.Parent.value) * NODE.Transform.value

  ## Evaluated every frame.
  def evaluate(self):

    # base class evaluate
    self.perform_tool_node_transformation()

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
  

    # update sf_portal_matrix
    self.sf_portal_matrix.value = self.compute_world_transform(self.tool_transform_node) * \
                                  avango.gua.make_trans_mat(0.0, self.TOOL_INSTANCE.portal_height/2, 0.0)

    # update border color according to highlight enabled
    if self.highlighted:
      if self.portal.border_material != "data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd":
        self.portal.set_border_material("data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd")
    else:
      if self.portal.border_material != "data/materials/White.gmd":
        self.portal.set_border_material("data/materials/White.gmd")

  ## Retrieves portal_width and portal_height from the PortalCamera instance and updates the sizes of the representation's parts.
  def update_size(self):

    self.portal.set_size(self.TOOL_INSTANCE.portal_width, self.TOOL_INSTANCE.portal_height)                                                  

  ## Loads a shot to this representation's portal and sets it visible.
  # @param SHOT The Shot instance to be loaded.
  def assign_shot(self, SHOT):

    # disconnect fields when a shot is already assigned
    if self.assigned_shot != None:
      self.assigned_shot.sf_abs_mat.disconnect()
      self.assigned_shot.sf_scale.disconnect()

    # copy shot values to navigation
    self.portal_nav.set_navigation_values(SHOT.sf_abs_mat.value, SHOT.sf_scale.value)

    # copy shot values to portal
    if SHOT.sf_viewing_mode.value != self.portal.viewing_mode:
      self.portal.switch_viewing_mode()

    if SHOT.sf_camera_mode.value != self.portal.camera_mode:
      self.portal.switch_camera_mode()

    if SHOT.sf_negative_parallax.value != self.portal.negative_parallax:
      self.portal.switch_negative_parallax()

    # establish field connections to copy updates done by the PortalCameraNavigation.
    SHOT.sf_abs_mat.disconnect()
    SHOT.sf_abs_mat.connect_from(self.portal_nav.sf_abs_mat)
    SHOT.sf_scale.disconnect()
    SHOT.sf_scale.connect_from(self.portal_nav.sf_scale)

    self.assigned_shot = SHOT
    self.portal.set_visibility(True)

  ## Removes the assigned shot of this representation and makes the portal invisible.
  def deassign_shot(self):

    self.assigned_shot.sf_abs_mat.disconnect()
    self.assigned_shot.sf_scale.disconnect()
    self.assigned_shot = None

    self.portal.set_visibility(False)

  ## Sets the viewing mode on the portal.
  # @param MODE The mode string to be set.
  def set_viewing_mode(self, MODE):

    if self.portal.viewing_mode != MODE:
      self.portal.switch_viewing_mode()

  ## Sets the negative parallax mode on the portal.
  # @param MODE The mode string to be set.
  def set_negative_parallax(self, MODE):

    if self.portal.negative_parallax != MODE:
      self.portal.switch_negative_parallax()


  ## Appends a string to the GroupNames field of this PortalCameraRepresentation's visualization.
  # @param STRING The string to be appended.
  def append_to_visualization_group_names(self, STRING):
    
    # do not add portal head group nodes for visibility of this portal
    if not STRING.startswith("portal"):
      self.portal.portal_matrix_node.GroupNames.value.append(STRING)


  ## Removes a string from the GroupNames field of this PortalCameraRepresentation's visualization.
  # @param STRING The string to be removed.
  def remove_from_visualization_group_names(self, STRING):
    
    self.portal.portal_matrix_node.GroupNames.value.remove(STRING)

  ## Resets the GroupNames field of this PortalCameraRepresentation's visualization to the user representation's view_transform_node.
  def reset_visualization_group_names(self):

    self.portal.portal_matrix_node.GroupNames.value = [self.USER_REPRESENTATION.view_transform_node.Name.value]

  ## Enables the highlight for this PortalCameraRepresentation.
  def enable_highlight(self):
    
    self.highlighted = True

  ## Disables the highlight for this PortalCameraRepresentation.
  def disable_highlight(self):
    
    self.highlighted = False
    


###############################################################################################

## A PortalCamera is a physical device to interactively caputure, view
# and manipulate Shots in the scene.
class PortalCamera(Tool):
 
  ## @var sf_tracking_mat
  # Tracking matrix of the PortalCamera within the platform coordinate system.
  sf_tracking_mat = avango.gua.SFMatrix4()

  ## @var sf_world_border_mat_no_scale
  # World transformation of the camera frame without scaling. Used for Portal instantiation.
  sf_world_border_mat_no_scale = avango.gua.SFMatrix4()

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

    ## @var in_capture_mode
    # Boolean saying if the portal camera is currently at capturing a photo.
    self.in_capture_mode = False

    ## @var capture_tool_representation
    # PortalCameraRepresentation instance which is used in capture mode. Might change during capturing.
    self.capture_tool_representation = None

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

    ## @var last_open_shot_index
    # Index within self.captured_shots saying which of the Shots was lastly opened by the PortalCamera.
    self.last_open_shot_index = None

    ## @var gallery_magification_factor
    # Factor with which the size of the portals will be multiplied when in gallery mode.
    self.gallery_magnification_factor = 1.5


  ## Custom constructor.
  # @param WORKSPACE_INSTANCE The instance of Workspace to which this Tool belongs to.
  # @param TOOL_ID The identification number of this Tool within the workspace.
  # @param CAMERA_TRACKING_STATION The tracking target name of this PortalCamera.
  # @param CAMERA_DEVICE_STATION The device station name of this PortalCamera.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags.
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
    self.sf_scale_down_button.connect_from(self.device_sensor.Button11)
    self.sf_open_close_button.connect_from(self.device_sensor.Button6)
    self.sf_delete_button.connect_from(self.device_sensor.Button15)
    self.sf_gallery_button.connect_from(self.device_sensor.Button11)
    self.sf_size_up_button.connect_from(self.device_sensor.Button3)
    self.sf_size_down_button.connect_from(self.device_sensor.Button2)
    self.sf_2D_mode_button.connect_from(self.device_sensor.Button7)
    self.sf_3D_mode_button.connect_from(self.device_sensor.Button8)
    self.sf_negative_parallax_on_button.connect_from(self.device_sensor.Button12)
    self.sf_negative_parallax_off_button.connect_from(self.device_sensor.Button13)

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

  ## Selects a list of potentially currently active PortalCameraRepresentations by checking the assigned user of them.
  def create_candidate_list(self):
    
    _candidate_list = []

    # only go on if a user is assigned to the PortalCamera
    if self.assigned_user != None:

      # iterate over all tool representations of assigned user
      for _tool_repr in self.tool_representations:

        if _tool_repr.user_id == self.assigned_user.id:

          _candidate_list.append(_tool_repr)


    return _candidate_list

  ## Chooses one PortalCameraRepresentation among the potentially active ones in a candidate list.
  # @param CANDIDATE_LIST The list of candidates to be checked.
  def choose_from_candidate_list(self, CANDIDATE_LIST):
    
    _dg_hit_by_user = self.assigned_user.last_seen_display_group

    for _tool_repr in CANDIDATE_LIST:

      if _tool_repr.DISPLAY_GROUP == _dg_hit_by_user:
        return _tool_repr

    return None

  ## Create candidate list and select one of the candidates.
  def get_active_tool_representation(self):

    _candidate_representations = self.create_candidate_list()
    _chosen_tool_representation = self.choose_from_candidate_list(_candidate_representations)
    return _chosen_tool_representation


  ## Evaluated every frame.
  def evaluate(self):

    # update user assignment
    self.check_for_user_assignment()

    # handle portal updates in capture mode
    if self.in_capture_mode:

      # get active tool mechanism by decision algorithm
      _active_tool_representation = self.get_active_tool_representation()

      if self.capture_tool_representation != _active_tool_representation:

        self.capture_tool_representation = _active_tool_representation

      # compute shot parameters and assign them
      _active_navigation = _active_tool_representation.DISPLAY_GROUP.navigations[_active_tool_representation.USER_REPRESENTATION.connected_navigation_id]

      # compute matrix
      _shot_platform_matrix = _active_tool_representation.sf_portal_matrix.value * \
                              avango.gua.make_inverse_mat(avango.gua.make_scale_mat(_active_navigation.sf_scale.value))

      for _tool_repr in self.tool_representations:
        _tool_repr.portal_nav.set_navigation_values(_shot_platform_matrix, _active_navigation.sf_scale.value)

    

    # apply size changes
    if self.sf_size_up_button.value == True:
      self.portal_width += 0.005
      self.portal_height += 0.005

      if self.portal_width > 1.0:
        self.portal_width = 1.0

      if self.portal_height > 1.0:
        self.portal_height = 1.0

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

  ## Loads a given Shot instances to all representations.
  # @param SHOT The Shot instance to be loaded.
  def set_current_shot(self, SHOT):

    for _tool_repr in self.tool_representations:
      _tool_repr.assign_shot(SHOT)

    self.current_shot = SHOT

  ## Clears the Shot currently loaded to all representations.
  def clear_current_shot(self):

    for _tool_repr in self.tool_representations:
      _tool_repr.deassign_shot()

    self.current_shot = None


  ## Called whenever sf_focus_button changes.
  @field_has_changed(sf_focus_button)
  def sf_focus_button_changed(self):

    # show and hide camera frame
    if self.sf_focus_button.value == True and self.current_shot == None:

      # get active tool mechanism by decision algorithm
      _active_tool_representation = self.get_active_tool_representation()
      self.capture_tool_representation = _active_tool_representation

      # break when no lastly seen display is available
      if self.assigned_user.last_seen_display_group == None:
        return

      # create shot and assign it
      _active_navigation = _active_tool_representation.DISPLAY_GROUP.navigations[_active_tool_representation.USER_REPRESENTATION.connected_navigation_id]

      # compute matrix
      _shot_platform_matrix = _active_tool_representation.sf_portal_matrix.value * \
                              avango.gua.make_inverse_mat(avango.gua.make_scale_mat(_active_navigation.sf_scale.value))

      _shot = Shot()
      _shot.my_constructor(_shot_platform_matrix,
                           _active_navigation.sf_scale.value,
                           self.capture_viewing_mode,
                           "PERSPECTIVE",
                           self.capture_parallax_mode)

      self.set_current_shot(_shot)              

      self.in_capture_mode = True

    else:

      if self.in_capture_mode == True:
        self.in_capture_mode = False
        self.clear_current_shot()


  ## Called whenever sf_capture_button changes.
  @field_has_changed(sf_capture_button)
  def sf_capture_button_changed(self):
    if self.sf_capture_button.value == True and self.in_capture_mode:

      # store the preview shot currently loaded
      self.captured_shots.append(self.current_shot)
      self.in_capture_mode = False

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