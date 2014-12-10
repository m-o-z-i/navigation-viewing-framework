#!/usr/bin/python

## @file
# Contains classes ToolRepresentation and Tool.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
from ApplicationManager import *
from VisibilityHandler import *
from TrackingReader import TrackingTargetReader
import Utilities

## Geometric representation of a Tool in a DisplayGroup. 
# Base class. Not to be instantiated.
class ToolRepresentation(avango.script.Script):

  ## Default constructor.
  def __init__(self):
    self.super(ToolRepresentation).__init__()

  ## Custom constructor. Called by subclasses.
  # @param TOOL_INSTANCE An instance of a subclass of Tool to which this ToolRepresentation is associated.
  # @param DISPLAY_GROUP DisplayGroup instance for which this ToolRepresentation is responsible for.
  # @param USER_REPRESENTATION Corresponding UserRepresentation instance under which's view_transform_node the ToolRepresentation is appended.
  # @param TOOL_TRANSFORM_NODE_NAME String to be used as name for this ToolRepresentation's transform node.
  def base_constructor(self
                   , TOOL_INSTANCE
                   , DISPLAY_GROUP
                   , USER_REPRESENTATION
                   , TOOL_TRANSFORM_NODE_NAME):
    
    ## @var TOOL_INSTANCE
    # An instance of a subclass of Tool to which this ToolRepresentation is associated.
    self.TOOL_INSTANCE = TOOL_INSTANCE

    ## @var DISPLAY_GROUP
    # DisplayGroup instance for which this ToolRepresentation is responsible for.
    self.DISPLAY_GROUP = DISPLAY_GROUP

    ## @var USER_REPRESENTATION
    # Corresponding UserRepresentation instance under which's view_transform_node the ToolRepresentation is appended.
    self.USER_REPRESENTATION = USER_REPRESENTATION

    ## @var user_id
    # Identification number of the USER_REPRESENTATION's user.
    self.user_id = self.USER_REPRESENTATION.USER.id

    ## @var workspace_id
    # Identification number of the workspace in which TOOL_INSTANCE is active.
    self.workspace_id = int(self.USER_REPRESENTATION.view_transform_node.Name.value.split("_")[0].replace("w", ""))


    ## @var tool_transform_node
    # Scenegraph transformation node representing this ToolRepresentation.
    self.tool_transform_node = avango.gua.nodes.TransformNode(Name = TOOL_TRANSFORM_NODE_NAME)
    self.USER_REPRESENTATION.view_transform_node.Children.value.append(self.tool_transform_node)

    # set evaluation policy
    self.always_evaluate(True)

  ## Computes the world transformation of the tool_transform_node.
  def get_world_transform(self):

    return self.tool_transform_node.WorldTransform.value

  ## Performs the necessary tool node transformation in the display group.
  def perform_tool_node_transformation(self):

    self.tool_transform_node.Transform.value = self.DISPLAY_GROUP.offset_to_workspace * self.TOOL_INSTANCE.tracking_reader.sf_abs_mat.value

  ## Appends a string to the GroupNames field of this ToolRepresentation's visualization.
  # @param STRING The string to be appended.
  def append_to_visualization_group_names(self, STRING):
    raise NotImplementedError( "To be implemented by a subclass." )

  ## Removes a string from the GroupNames field of this ToolRepresentation's visualization.
  # @param STRING The string to be removed.
  def remove_from_visualization_group_names(self, STRING):
    raise NotImplementedError( "To be implemented by a subclass." )

  ## Resets the GroupNames field of this ToolRepresentation's visualization to the user representation's view_transform_node.
  def reset_visualization_group_names(self):
    raise NotImplementedError( "To be implemented by a subclass." )

  ## Evaluated every frame.
  def evaluate(self):

    self.perform_tool_node_transformation()


###############################################################################################

## Logical representation of a Tool in a Workspace.
# Base class. Not to be instantiated.
class Tool(VisibilityHandler2D):

  ## Default constructor.
  def __init__(self):
    self.super(Tool).__init__()

  ## Custom constructor. Called by subclasses.
  # @param WORKSPACE_INSTANCE The instance of Workspace to which this Tool belongs to.
  # @param TOOL_ID The identification number of this Tool within the workspace.
  # @param TRACKING_STATION The tracking target name of this Tool.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def base_constructor(self
                     , WORKSPACE_INSTANCE
                     , TOOL_ID
                     , TRACKING_STATION
                     , VISIBILITY_TABLE):

    self.table_constructor(VISIBILITY_TABLE)

    # references
    ## @var WORKSPACE_INSTANCE
    # The instance of Workspace to which this Tool belongs to.
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ## @var id
    # The identification number of this Tool within the workspace.
    self.id = TOOL_ID

    ## @var assigned_user
    # User instance that was identified as the current holder of this Tool.
    self.assigned_user = None

    ## @var tool_representations
    # List of ToolRepresentation instances belonging to this Tool.
    self.tool_representations = []

    # init sensors
    ## @var tracking_reader
    # TrackingTargetReader to capture the tool's tracking information.
    self.tracking_reader = TrackingTargetReader()
    self.tracking_reader.my_constructor(TRACKING_STATION)
    self.tracking_reader.set_transmitter_offset(self.WORKSPACE_INSTANCE.transmitter_offset)
    self.tracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    # set evaluation policy
    self.always_evaluate(True)

  ## Creates a ToolRepresentation for this Tool at a DISPLAY_GROUP. 
  # @param DISPLAY_GROUP The DisplayGroup instance to create the representation for.
  # @param USER_REPRESENTATION The UserRepresentation this representation will belong to.
  def create_tool_representation_for(self, DISPLAY_GROUP, USER_REPRESENTATION):
    raise NotImplementedError( "To be implemented by a subclass." )

  ## Selects a list of potentially currently active ToolRepresentations.
  def create_candidate_list(self):
    raise NotImplementedError( "To be implemented by a subclass." )

  ## Chooses one ToolReprsentation among the potentially active one in a candidate list.
  # @param CANDIDATE_LIST The list of ToolRepresentation candidates to be checked.
  def choose_from_candidate_list(self, CANDIDATE_LIST):
    raise NotImplementedError( "To be implemented by a subclass." )

  ## Checks which user is closest to this Tool in tracking space and makes him the assigned user.
  # Additionally updates the material of the corresponding RayPointerRepresentation.
  def check_for_user_assignment(self):

    _assigned_user_before = self.assigned_user

    _closest_user = None
    _closest_distance = 1000

    for _user in self.WORKSPACE_INSTANCE.users:

      if _user.is_active:


        _dist = Utilities.compute_point_to_line_distance( self.tracking_reader.sf_abs_vec.value
                                                        , _user.headtracking_reader.sf_abs_vec.value
                                                        , avango.gua.Vec3(0, -1, 0) )

        if _dist < _closest_distance:
          _closest_distance = _dist
          _closest_user = _user

    if _closest_user != self.assigned_user:
      self.assign_user(_closest_user)

    _assigned_user_after = self.assigned_user

    # Change material on assigned ray holder
    if _assigned_user_before != _assigned_user_after:

      for _tool_repr in self.tool_representations:

        if self.assigned_user != None and _tool_repr.user_id == self.assigned_user.id:
          _tool_repr.enable_highlight()
        else:
          _tool_repr.disable_highlight()


  ## Assigns a user to this Tool.
  def assign_user(self, USER_INSTANCE):

    self.assigned_user = USER_INSTANCE

    if self.assigned_user != None:
      for _display_group in self.WORKSPACE_INSTANCE.display_groups:
        self.handle_correct_visibility_groups_for(_display_group)


  ## Changes the visibility table during runtime.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def change_visiblity_table(self, VISIBILITY_TABLE):

    self.visibility_table = VISIBILITY_TABLE

    for _display_group in self.WORKSPACE_INSTANCE.display_groups:
      self.handle_correct_visibility_groups_for(_display_group)


  ## Handles the correct GroupNames of all ToolRepresentations at a display group.
  # @param DISPLAY_GROUP The DisplayGroup to be handled.
  def handle_correct_visibility_groups_for(self, DISPLAY_GROUP):

    #print "display group", DISPLAY_GROUP

    # All ToolRepresentation instances at DISPLAY_GROUP
    _tool_reprs_at_display_group = []

    # ToolRepresentation instance belonging to the assigned user at DISPLAY_GROUP
    _tool_repr_of_assigned_user = None

    # display group instance belonging to DISPLAY_GROUP
    _handled_display_group_instance = DISPLAY_GROUP

    ## fill the variables ##
    for _tool_repr in self.tool_representations:

      # get all tool representations in display group
      if _tool_repr.DISPLAY_GROUP == DISPLAY_GROUP:
        _tool_reprs_at_display_group.append(_tool_repr)

        # find tool representation of assigned user
        if _tool_repr.USER_REPRESENTATION.USER == self.assigned_user:
          _tool_repr_of_assigned_user = _tool_repr

    ## determine which group names have to be added to the tool representations ##
    _assigned_user_tool_visible_for = []

    for _tool_repr in _tool_reprs_at_display_group:

      # check for navigation of corresponding user and compare it to assigned user

      # reset initial GroupName state
      _tool_repr.reset_visualization_group_names()

      # if user does not share the assigned user's navigation, hide the tool representation
      if _tool_repr.USER_REPRESENTATION.connected_navigation_id != _tool_repr_of_assigned_user.USER_REPRESENTATION.connected_navigation_id:
        _tool_repr.append_to_visualization_group_names("do_not_display_group")
        _assigned_user_tool_visible_for.append(_tool_repr.USER_REPRESENTATION.view_transform_node.Name.value)

    # check for all user representations outside the handled display group
    for _user_repr in ApplicationManager.all_user_representations:
      if _user_repr.DISPLAY_GROUP != _handled_display_group_instance:

        # consider visibility table
        _handled_display_group_tag = _handled_display_group_instance.visibility_tag
        _user_repr_display_group_tag = _user_repr.DISPLAY_GROUP.visibility_tag
        
        _visible = self.visibility_table[_user_repr_display_group_tag][_handled_display_group_tag]

        #print "Does", _user_repr.view_transform_node.Name.value, "(", _user_repr_display_group_tag, ") see"
        #, _handled_display_group_tag, "?", _visible
        if _visible:
          if _user_repr.view_transform_node.Name.value == "scene_matrix":
            _assigned_user_tool_visible_for.append(_user_repr.view_transform_node.Parent.value.Name.value + "_" + _user_repr.head.Name.value)
          else:
            _assigned_user_tool_visible_for.append(_user_repr.view_transform_node.Name.value)

    # make tool holder tool representation visible for all others on different navigations and display groups
    for _string in _assigned_user_tool_visible_for:
      _tool_repr_of_assigned_user.append_to_visualization_group_names(_string)