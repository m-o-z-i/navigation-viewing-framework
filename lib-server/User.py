#!/usr/bin/python

## @file
# Contains classes UserRepresentation and User.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Avatar import *
from Intersection import *
from TrackingReader import *
from VisibilityHandler import *
from ConsoleIO import *
import Utilities

# import math libraries
import math
import time

## A User instances has UserRepresentations for each display group of his workspace.
# It handles the selection of the display group's navigations.
class UserRepresentation:

  ## Default constructor.
  def __init__(self):
    pass

  ## Custom constructor.
  # @param USER Reference to the user to be represented.
  # @param DISPLAY_GROUP Reference to the display group this user representation is responsible for.
  # @param VIEW_TRANSFORM_NODE Transform node to be filled by one navigation of the display group.
  # @param VIRTUAL_USER_REPR_DISPLAY_INDEX If this is a portal user representation, ID giving the display index within the display group. -1 otherwise.
  # @param HEAD_NODE_NAME Name of the UserRepresentation's head node in the scenegraph.
  # @param COMPLEX_SETUP If activated, the transformation policy is evaluated every frame to update head. If deactivated,
  #                      a standard mono viewing setup is assumed.
  def my_constructor(self, USER, DISPLAY_GROUP, VIEW_TRANSFORM_NODE, VIRTUAL_USER_REPR_DISPLAY_INDEX = -1, HEAD_NODE_NAME = 'head', COMPLEX_SETUP = True):

    ## @var USER
    # Reference to the user to be represented.
    self.USER = USER

    ## @var DISPLAY_GROUP
    # Reference to the display group this user representation is responsible for.
    self.DISPLAY_GROUP = DISPLAY_GROUP

    ## @var view_transform_node
    # Transform node to be filled by one navigation of the display group.
    self.view_transform_node = VIEW_TRANSFORM_NODE

    ## @var screens
    # List of screen nodes for each display of the display group.
    self.screens = []

    ## @var dependent_nodes
    # Placeholder for scenegraph nodes which are relevant for the transformation policy.
    self.dependent_nodes = []

    ## @var execute_transformation_policy
    # Boolean indicating if the transformation policy is evaluated every frame.
    self.execute_transformation_policy = True

    ## create user representation nodes ##

    ## @var stereo_display_group
    # Boolean saying if this DisplayGroup contains of only stereo displays.
    self.stereo_display_group = True

    for _display in DISPLAY_GROUP.displays:

      if _display.stereo == False:
        self.stereo_display_group = False
        break


    ## @var head
    # Head node of the user.
    self.head = avango.gua.nodes.TransformNode(Name = HEAD_NODE_NAME)
    self.view_transform_node.Children.value.append(self.head)

    ## @var left_eye
    # Left eye node of the user.
    self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
    self.head.Children.value.append(self.left_eye)

    ## @var right_eye
    # Right eye node of the user.
    self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
    self.head.Children.value.append(self.right_eye)

    # assign correct transformations to nodes
    if COMPLEX_SETUP:
      self.make_complex_viewing_setup()
    else:
      self.make_default_viewing_setup()

    ## @var connected_navigation_id
    # Navigation ID within the display group that is currently used.
    self.connected_navigation_id = -1

    ## @var avatar
    # Avatar instance belonging to this UserRepresentation.
    self.avatar = Avatar()
    self.avatar.my_constructor(self)

    ## @var virtual_user_repr_display_index
    # If this is a portal user representation, ID giving the display index within the display group. -1 otherwise.
    self.virtual_user_repr_display_index = VIRTUAL_USER_REPR_DISPLAY_INDEX

    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method.
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

    ## @var thumbnail_mode
    # Boolean indicating if the portal if a default viewing setup is activated although the portal might suggest it differently.
    self.thumbnail_mode = False


  ## Evaluated every frame.
  def frame_callback(self):
  
    if self.execute_transformation_policy:
      
      if self.virtual_user_repr_display_index == -1:
        self.perform_physical_user_head_transformation()

      else:
        self.perform_virtual_user_head_transformation(self.virtual_user_repr_display_index)

        # activate thumbnail mode when scale is too small
        # make sure not to switch off own PortalCameraRepresentations
        _physical_nav_node = self.dependent_nodes[0].Parent.value
        _physical_nav_scale = _physical_nav_node.Transform.value.get_scale()

        _physical_user_w_id = _physical_nav_node.Name.value.split("_")[0].replace("w", "")
        _physical_user_dg_id = _physical_nav_node.Name.value.split("_")[1].replace("dg", "")
        _portal_w_id = self.view_transform_node.Parent.value.Name.value.split("_")[2].replace("w", "")
        _portal_dg_id = self.view_transform_node.Parent.value.Name.value.split("_")[3].replace("dg", "")

        if _physical_nav_scale.x > 30.0 and (_physical_user_w_id != _portal_w_id or _physical_user_dg_id != _portal_dg_id):
          self.thumbnail_mode = True
          self.make_default_viewing_setup()

    # handle reactivation in thumbnail mode
    elif self.thumbnail_mode:

      self.perform_virtual_user_head_transformation(self.virtual_user_repr_display_index)

      # same check as performed above
      _physical_nav_node = self.dependent_nodes[0].Parent.value
      _physical_nav_scale = _physical_nav_node.Transform.value.get_scale()

      _physical_user_w_id = _physical_nav_node.Name.value.split("_")[0].replace("w", "")
      _physical_user_dg_id = _physical_nav_node.Name.value.split("_")[1].replace("dg", "")
      _portal_w_id = self.view_transform_node.Parent.value.Name.value.split("_")[2].replace("w", "")
      _portal_dg_id = self.view_transform_node.Parent.value.Name.value.split("_")[3].replace("dg", "")

      # remain in thumbnail mode
      if _physical_nav_scale.x > 30.0 and (_physical_user_w_id != _portal_w_id or _physical_user_dg_id != _portal_dg_id):
        self.make_default_viewing_setup()
      
      # deactive thumbnail mode
      else:
        if self.DISPLAY_GROUP.displays[self.virtual_user_repr_display_index].viewing_mode == "3D":
          self.make_complex_viewing_setup()
        else:
          self.make_default_viewing_setup()

        self.thumbnail_mode = False

  ## Transforms the head node according to the display group offset and the tracking matrix.
  def perform_physical_user_head_transformation(self):
    self.head.Transform.value = self.DISPLAY_GROUP.offset_to_workspace * self.USER.headtracking_reader.sf_abs_mat.value

  ## Transforms the head according to the head - portal entry relation.
  def perform_virtual_user_head_transformation(self, DISPLAY_INDEX):
    self.head.Transform.value = self.DISPLAY_GROUP.displays[DISPLAY_INDEX].portal_screen_node.Transform.value * \
                                avango.gua.make_inverse_mat(self.DISPLAY_GROUP.displays[DISPLAY_INDEX].portal_matrix_node.Transform.value) * \
                                self.dependent_nodes[0].WorldTransform.value



  ## Deactivates the evaluation of the transformation policy and assigns fixed matrices
  # for the eye and head nodes.
  def make_default_viewing_setup(self):

    self.execute_transformation_policy = False
    self.head.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 1.5)
    self.left_eye.Transform.value = avango.gua.make_identity_mat()
    self.right_eye.Transform.value = avango.gua.make_identity_mat()

  ## Activates the evaluation of the transformation policy and sets the eye
  # distance properly.
  def make_complex_viewing_setup(self):

    if self.stereo_display_group:
      _eye_distance = self.USER.eye_distance
    else:
      _eye_distance = 0.0

    self.execute_transformation_policy = True
    self.left_eye.Transform.value = avango.gua.make_trans_mat(-_eye_distance / 2, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(_eye_distance / 2, 0.0, 0.0)


  ## Sets the GroupNames field on all avatar parts to a list of strings.
  # @param LIST_OF_STRINGS A list of group names to be set for the avatar parts.
  def set_avatar_group_names(self, LIST_OF_STRINGS):

    self.avatar.set_group_names(LIST_OF_STRINGS)

  ## Appends a string to the GroupNames field of all avatar parts.
  # @param STRING The string to be appended to the GroupNames field.
  def append_to_avatar_group_names(self, STRING):
    
    self.avatar.append_to_group_names(STRING)

  ## Adds a screen visualization for a display instance to the avatar.
  # @param DISPLAY_INSTANCE The Display instance to retrieve the screen visualization from.
  def add_screen_visualization_for(self, DISPLAY_INSTANCE):

    self.avatar.add_screen_visualization_for(DISPLAY_INSTANCE)


  ## Appends a screen node for a display instance to the view transformation node.
  # @param DISPLAY_INSTANCE The Display instance to retrieve the screen node from.
  def add_screen_node_for(self, DISPLAY_INSTANCE):

    ## @var workspace_id
    # Identification number of the workspace the associated user is belonging to.
    self.workspace_id = int(self.view_transform_node.Name.value.split("_")[0].replace("w", ""))

    _screen = DISPLAY_INSTANCE.create_screen_node("screen_" + str(len(self.screens)))
    self.view_transform_node.Children.value.append(_screen)
    self.screens.append(_screen)

    _loader = avango.gua.nodes.TriMeshLoader()

    _navigation_color_geometry = _loader.create_geometry_from_file('nav_color_plane',
                                                                   'data/objects/plane.obj',
                                                                   'data/materials/' + self.DISPLAY_GROUP.navigations[0].trace_material + 'Shadeless.gmd',
                                                                    avango.gua.LoaderFlags.LOAD_MATERIALS)

    _trans = avango.gua.Vec3(-0.45 * _screen.Width.value, 0.4 * _screen.Height.value, 0.0)
    _scale = 0.05 * _screen.Height.value
    _navigation_color_geometry.Transform.value =  avango.gua.make_trans_mat(_trans) * \
                                                  avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                                  avango.gua.make_scale_mat(_scale, _scale, _scale)
    _navigation_color_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF
    _navigation_color_geometry.GroupNames.value = ["w" + str(self.workspace_id) + "_dg" + str(self.DISPLAY_GROUP.id) + "_u" + str(self.USER.id)]
    _screen.Children.value.append(_navigation_color_geometry)


  ## Adds an already existing screen node to this UserRepresentation.
  # @param SCREEN_NODE The screen node to be added.
  def add_existing_screen_node(self, SCREEN_NODE):

    self.screens.append(SCREEN_NODE)

  ## Adds a scenegraph node to the list of dependent nodes.
  # @param NODE The node to be added.
  def add_dependent_node(self, NODE):

    self.dependent_nodes.append(NODE)


  ## Connects a specific navigation of the display group to the user.
  # @param ID The ID of the navigation to connect with.
  def connect_navigation_of_display_group(self, ID):

    # change is not necessary
    if ID == self.connected_navigation_id:
      print_message("User " + str(self.USER.id) + " at display group " + str(self.DISPLAY_GROUP.id) + \
                    ": Already on Navigaton " + str(ID)) 

    # change is necessary
    elif ID < len(self.DISPLAY_GROUP.navigations):

      _old_navigation = self.DISPLAY_GROUP.navigations[self.connected_navigation_id]
      _new_navigation = self.DISPLAY_GROUP.navigations[ID]

      self.view_transform_node.Transform.disconnect()

      if len(_new_navigation.active_user_representations) == 0 and self.connected_navigation_id != -1:

        try:
          _new_navigation.inputmapping.set_abs_mat(_old_navigation.sf_abs_mat.value)
          _new_navigation.inputmapping.set_scale(_old_navigation.sf_scale.value)
          
          # avoid field connection frame latency by setting value directly
          self.view_transform_node.Transform.value = _old_navigation.sf_abs_mat.value * avango.gua.make_scale_mat(_old_navigation.sf_scale.value)

        except:
          pass

      _old_navigation.remove_user_representation(self)
      _new_navigation.add_user_representation(self)

      # connect view transform node to new navigation
      self.view_transform_node.Transform.connect_from(_new_navigation.sf_nav_mat)

      self.connected_navigation_id = ID

      try:
        print_message("User " + str(self.USER.id) + " at display group " + str(self.DISPLAY_GROUP.id) + \
         ": Switch navigation to " + str(ID) + " (" + _new_navigation.input_device_name + ")")
      except:
        print_message("User " + str(self.USER.id) + " at display group " + str(self.DISPLAY_GROUP.id) + \
         ": Switch navigation to " + str(ID) + " (no input device)")

      # trigger avatar and screen geometry visibilities
      self.avatar.set_material('data/materials/' + _new_navigation.trace_material + ".gmd"
                             , 'data/materials/' + _new_navigation.trace_material + "Shadeless.gmd")


    else:
      print_error("Error. Navigation ID does not exist.", False)

###############################################################################################

## Logical representation of a user within a Workspace. Stores the relevant parameters
# and cares for receiving the headtracking input.
class User(VisibilityHandler2D):

  ## @var mf_screen_pick_result
  # Intersections of the viewing ray with the screens in the setup.
  mf_screen_pick_result = avango.gua.MFPickResult()

  ## Default constructor.
  def __init__(self):
    self.super(User).__init__()

  ## Custom constructor.
  # @param WORKSPACE_INSTANCE Workspace instance in which this user is active.
  # @param USER_ID Global user ID to be applied.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param AVATAR_VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied when HEADTRACKING_TARGET_NAME is None.
  def my_constructor(self
                   , WORKSPACE_INSTANCE
                   , USER_ID
                   , VIP
                   , AVATAR_VISIBILITY_TABLE
                   , HEADTRACKING_TARGET_NAME
                   , EYE_DISTANCE
                   , NO_TRACKING_MAT
                   ):

    self.table_constructor(AVATAR_VISIBILITY_TABLE)

    # flags 
    ## @var is_vip
    # Boolean indicating if this user has vip status.
    self.is_vip = VIP

    ## @var is_active
    # Boolean indicating if this user is currently active.
    self.is_active = True

    ## @var eye_distance
    # The eye distance of the user to be applied.
    self.eye_distance = EYE_DISTANCE

    # variables
    ## @var WORKSPACE_INSTANCE
    # Workspace instance at which this user is registered.
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ## @var id
    # Identification number of the user within the workspace, starting from 0.
    self.id = USER_ID

    ## @var headtracking_target_name
    # Name of the headtracking station as registered in daemon.
    self.headtracking_target_name = HEADTRACKING_TARGET_NAME

    ## @var headtracking_reader
    # TrackingTargetReader for the user's glasses.
    if self.headtracking_target_name == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(NO_TRACKING_MAT)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.WORKSPACE_INSTANCE.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    ## @var user_representations
    # List of UserRepresentation instances for all display groups in the user's workspace.
    self.user_representations = []

    # toggles activity
    self.toggle_user_activity(self.is_active)

    ## @var intersection_tester
    # Instance of Intersection to determine intersection points of user with screens.
    self.intersection_tester = Intersection()
    self.intersection_tester.my_constructor(scenegraphs[0]
                                          , self.headtracking_reader.sf_abs_mat
                                          , 5.0
                                          , "screen_proxy_group"
                                          , False)
    self.mf_screen_pick_result.connect_from(self.intersection_tester.mf_pick_result)

    ## @var last_seen_display_group
    # DisplayGroup instance for which the user's viewing ray lastly hit a screen proxy geometry.
    self.last_seen_display_group = None

    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):

    # evaluate viewing ray intersections with screen proxy geometries
    for _i in range(len(self.mf_screen_pick_result.value)):

      _pick_object = self.mf_screen_pick_result.value[_i].Object.value

      # only consider own workspace geometries
      if _pick_object.Name.value.startswith("proxy_w" + str(self.WORKSPACE_INSTANCE.id)):
        _display_group_id = int(_pick_object.Name.value.split("_")[2].replace("dg", ""))
        self.last_seen_display_group = self.WORKSPACE_INSTANCE.display_groups[_display_group_id]
        break

    _track_vec = self.headtracking_reader.sf_abs_vec.value

    if _track_vec.x < -1.5 and _track_vec.x > -2.4 and \
       _track_vec.y < 1.05 and _track_vec.y > 0.95 and \
       _track_vec.z < 1.35 and _track_vec.z > 0.16:

      self.toggle_user_activity(False)

    else:

      self.toggle_user_activity(True)

  ## Changes the visibility table during runtime.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def change_visiblity_table(self, VISIBILITY_TABLE):

    self.visibility_table = VISIBILITY_TABLE

    for _display_group in self.WORKSPACE_INSTANCE.display_groups:
      self.handle_correct_visibility_groups_for(_display_group)

  ## Creates a UserRepresentation instance for a given display group.
  # @param DISPLAY_GROUP Reference to the DisplayGroup instance to create the user representation for.
  # @param VIEW_TRANSFORM_NODE Transform node to be filled by one navigation of the display group.
  # @param VIRTUAL_USER_REPR_DISPLAY_INDEX If this is a portal user representation, ID giving the display index within the display group. -1 otherwise.
  # @param HEAD_NODE_NAME Name of the UserRepresentation's head node in the scenegraph.
  # @param COMPLEX_SETUP If activated, the transformation policy is evaluated every frame to update head. If deactivated,
  #                      a standard mono viewing setup is assumed.
  def create_user_representation_for(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE, VIRTUAL_USER_REPR_DISPLAY_INDEX = -1, HEAD_NODE_NAME = "head", COMPLEX_SETUP = True):

    _user_repr = UserRepresentation()
    _user_repr.my_constructor(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE, VIRTUAL_USER_REPR_DISPLAY_INDEX, HEAD_NODE_NAME, COMPLEX_SETUP)
    self.user_representations.append(_user_repr)
    return _user_repr

  ## Returns the UserRepresentation instance at a diven DISPLAY_GROUP_ID.
  # @param DISPLAY_GROUP_ID The id of the DisplayGroup to retrieve the UserRepresentation for.
  def get_user_representation_at(self, DISPLAY_GROUP_ID):
    return self.user_representations[DISPLAY_GROUP_ID]

  ## Switches the navigation for a display group.
  # @param DISPLAY_GROUP_ID Identification number of the display group to switch the navigation for.
  # @param NAVIGATION_ID Identification number of the navigation to be used within the display group.
  # @param WORKSPACE_USERS A list of all Users active in the workspace.
  def switch_navigation_at_display_group(self, DISPLAY_GROUP_ID, NAVIGATION_ID, WORKSPACE_USERS):
    
    if DISPLAY_GROUP_ID < len(self.user_representations):
      
      # switch navigation to desired one for DISPLAY_GROUP_ID
      _old_nav_id = self.user_representations[DISPLAY_GROUP_ID].connected_navigation_id

      self.user_representations[DISPLAY_GROUP_ID].connect_navigation_of_display_group(NAVIGATION_ID)
      _display_group_instance = self.user_representations[DISPLAY_GROUP_ID].DISPLAY_GROUP

      # trigger correct tool visibilities at display group
      for _tool in self.WORKSPACE_INSTANCE.tools:
        _tool.handle_correct_visibility_groups_for(_display_group_instance)

      # trigger correct avatar and screen visibilities
      #for _user in WORKSPACE_USERS:
      #  _user.handle_correct_visibility_groups_for(_display_group_instance)

      # trigger correct video visibilites at both navigations
      if self.WORKSPACE_INSTANCE.video_3D != None and ApplicationManager.current_avatar_mode == "VIDEO":
        _old_nav = self.WORKSPACE_INSTANCE.display_groups[DISPLAY_GROUP_ID].navigations[_old_nav_id]
        _new_nav = self.WORKSPACE_INSTANCE.display_groups[DISPLAY_GROUP_ID].navigations[NAVIGATION_ID]
        self.WORKSPACE_INSTANCE.video_3D.handle_correct_visibility_groups_for(_old_nav)
        self.WORKSPACE_INSTANCE.video_3D.handle_correct_visibility_groups_for(_new_nav)
      else:
        for _user in WORKSPACE_USERS:
          _user.handle_correct_visibility_groups_for(_display_group_instance)

    else:
      print_error("Error. Display Group ID does not exist.", False)

    
  ## Sets the user's active flag.
  # @param ACTIVE Boolean to which the active flag should be set.
  def toggle_user_activity(self, ACTIVE):

    if ACTIVE:
      self.is_active = True
    else:
      self.is_active = False

  ## Handles the correct GroupNames of all UserRepresentations at a display group.
  # @param DISPLAY_GROUP The DisplayGroup to be handled.
  def handle_correct_visibility_groups_for(self, DISPLAY_GROUP):

    # All UserRepresentation instances at DISPLAY_GROUP
    # normally, this list should just contain one user representation
    # in case of portals, however, a display group may have more than one user representation
    _user_representations_at_display_group = []

    for _user_repr in self.user_representations:
      
      if _user_repr.DISPLAY_GROUP == DISPLAY_GROUP:
        _user_representations_at_display_group.append(_user_repr)
        
    # for all found user representations in the given display group
    for _user_repr_at_display_group in _user_representations_at_display_group:

      # display group instance belonging to DISPLAY_GROUP
      _handled_display_group_instance = _user_repr_at_display_group.DISPLAY_GROUP

      _all_user_reprs_at_display_group = []

      for _user_repr in ApplicationManager.all_user_representations:
        if _user_repr.DISPLAY_GROUP == _handled_display_group_instance:
          _all_user_reprs_at_display_group.append(_user_repr)

      ## determine which group names have to be added to the user representations ##
      _user_visible_for = []

      # when video avatars are enabled, do not make josephs visible
      if ApplicationManager.current_avatar_mode == "JOSEPH":
        
        # append all names of user representations which are not on same navigation
        for _user_repr in _all_user_reprs_at_display_group:

          if _user_repr.connected_navigation_id != _user_repr_at_display_group.connected_navigation_id:
            _user_visible_for.append(_user_repr.view_transform_node.Name.value)

        # check for all user representations outside the handled display group
        for _user_repr in ApplicationManager.all_user_representations:
          if _user_repr.DISPLAY_GROUP != _handled_display_group_instance:

            # consider visibility table
            _handled_display_group_tag = _handled_display_group_instance.visibility_tag
            _user_repr_display_group_tag = _user_repr.DISPLAY_GROUP.visibility_tag
            
            try:
              _visible = self.visibility_table[_user_repr_display_group_tag][_handled_display_group_tag]
            except:
              _visible = False
            
            if _visible:
              if _user_repr.view_transform_node.Name.value == "scene_matrix":
                _user_visible_for.append(_user_repr.view_transform_node.Parent.value.Name.value + "_" + _user_repr.head.Name.value)
              else:
                _user_visible_for.append(_user_repr.view_transform_node.Name.value)

      # apply the obtained group names to the user representation
      if len(_user_visible_for) == 0:

        # prevent wildcard from rendering the avatar
        _user_repr_at_display_group.set_avatar_group_names(["do_not_display_group"])

      else:

        for _string in _user_visible_for:
          _user_repr_at_display_group.set_avatar_group_names(_user_visible_for)