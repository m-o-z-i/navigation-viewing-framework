#!/usr/bin/python

## @file
# Contains class Workspace.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ApplicationManager import *
from ConsoleIO import *
from Display import *
from DisplayGroup import *
from RayPointer import *
from User import *
import Tools

## Representation of the physical space holding several users, tools and display groups.
class Workspace:

  ## @var number_of_instances
  # Number of Workspace instances that have already been created. Used for assigning correct IDs.
  number_of_instances = 0

  ## Custom constructor.
  # @param NAME Name of the Workspace to be created.
  # @param TRANSMITTER_OFFSET Transmitter offset to be applied within this workspace.
  def __init__(self, NAME, TRANSMITTER_OFFSET):

    ## @var id
    # Identification number of this workspace.
    self.id = Workspace.number_of_instances
    Workspace.number_of_instances += 1

    # @var name
    # Name of this Workspace.
    self.name = NAME

    ## @var transmitter_offset
    # Transmitter offset to be applied within this workspace.
    self.transmitter_offset = TRANSMITTER_OFFSET

    ## @var users
    # List of users that are active within this workspace.
    self.users = []

    ## @var display_groups
    # List of DisplayGroups present within this workspace.
    self.display_groups = []

    ## @var tools
    # List of RayPointer, ... (tool) instances present within this workspace.
    self.tools = []

    ## @var size
    # Physical size of this workspace in meters.
    self.size = (3.8, 3.6)

  ## Triggers the correct GroupNames of all ToolRepresentations at a display group.
  # @param DISPLAY_GROUP_ID The identification number of the DisplayGroup.
  def trigger_tool_visibilities_at(self, DISPLAY_GROUP_ID):

    #print "display group", DISPLAY_GROUP_ID

    # handle every tool in workspace
    for _tool in self.tools:

      # All ToolRepresentation instances at DISPLAY_GROUP_ID
      _tool_reprs_at_display_group = []

      # ToolRepresentation instance belonging to the assigned user at DISPLAY_GROUP_ID
      _tool_repr_of_assigned_user = None

      # display group instance belonging to DISPLAY_GROUP_ID
      _handled_display_group_instance = None

      ## fill the variables ##
      for _tool_repr in _tool.tool_representations:

        # get all tool representations in display group
        if _tool_repr.DISPLAY_GROUP.id == DISPLAY_GROUP_ID:

          _handled_display_group_instance = _tool_repr.DISPLAY_GROUP
          _tool_reprs_at_display_group.append(_tool_repr)

          # find tool representation of assigned user
          if _tool_repr.USER_REPRESENTATION.USER == _tool.assigned_user:
            _tool_repr_of_assigned_user = _tool_repr

      ## determine which group names have to be added to the tool representations ##
      _assigned_user_ray_visible_for = []

      for _tool_repr in _tool_reprs_at_display_group:

        # check for navigation of corresponding user and compare it to assigned user

        # reset initial GroupName state
        _tool_repr.reset_visualization_group_names()

        # if user does not share the assigned user's navigation, hide the tool representation
        if _tool_repr.USER_REPRESENTATION.connected_navigation_id != _tool_repr_of_assigned_user.USER_REPRESENTATION.connected_navigation_id:
          _tool_repr.append_to_visualization_group_names("do_not_display_group")
          _assigned_user_ray_visible_for.append(_tool_repr.USER_REPRESENTATION.view_transform_node.Name.value)

      # check for all user representations outside the handled display group
      for _user_repr in ApplicationManager.all_user_representations:
        if _user_repr.DISPLAY_GROUP != _handled_display_group_instance:

          # consider visibility table
          _handled_display_group_tag = _handled_display_group_instance.visibility_tag
          _user_repr_display_group_tag = _user_repr.DISPLAY_GROUP.visibility_tag
          
          _visible = _tool.visibility_table[_user_repr_display_group_tag][_handled_display_group_tag]

          #print "Does", _user_repr.view_transform_node.Name.value, "(", _user_repr_display_group_tag, ") see"
          #, _handled_display_group_tag, "?", _visible
          if _visible:
            _assigned_user_ray_visible_for.append(_user_repr.view_transform_node.Name.value)

      # make ray holder tool representation visible for all others on different navigations and display groups
      for _string in _assigned_user_ray_visible_for:
        _tool_repr_of_assigned_user.append_to_visualization_group_names(_string)

      #print "assigned user is seen by", _assigned_user_ray_visible_for
      #print

  ## Computes a list of users whose tracking targets are not farer away than DISTANCE from a POINT.
  # @param POINT The point to compute the proximity to.
  # @param DISTANCE The tolerance distance to be applied.
  def get_all_users_in_range(self, POINT, DISTANCE):

    _users_in_range = []

    for _user in self.users:

      if Tools.euclidean_distance(_user.headtracking_reader.sf_abs_vec.value, POINT) < DISTANCE:
        _users_in_range.append(_user)
        print "In range", _user.id, Tools.euclidean_distance(_user.headtracking_reader.sf_abs_vec.value, POINT)

      else:
        print "not in range", _user.id, Tools.euclidean_distance(_user.headtracking_reader.sf_abs_vec.value, POINT)

    return _users_in_range


  ## Creates a DisplayGroup instance and adds it to this workspace.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assiged to the display group.
  # @param VISIBILITY_TAG Tag used by the Tools' visibility matrices to define if they are visible for this display group.
  # @param OFFSET_TO_WORKSPACE Offset describing the origin of this display group with respect to the origin of the workspace.
  def create_display_group( self
                          , DISPLAY_LIST
                          , NAVIGATION_LIST
                          , VISIBILITY_TAG
                          , OFFSET_TO_WORKSPACE):

    _dg = DisplayGroup(len(self.display_groups), DISPLAY_LIST, NAVIGATION_LIST, VISIBILITY_TAG, OFFSET_TO_WORKSPACE, self.transmitter_offset)
    self.display_groups.append(_dg)

  ## Creates a User instance and adds it to this workspace.
  # To be called after all display groups have been created.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param GLASSES_ID ID of the shutter glasses worn by the user.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied when HEADTRACKING_TARGET_NAME is None.
  def create_user( self
                 , VIP
                 , GLASSES_ID
                 , HEADTRACKING_TARGET_NAME
                 , EYE_DISTANCE
                 , NO_TRACKING_MAT = avango.gua.make_trans_mat(0,0,0)):
    
    _user = User()
    _user.my_constructor( self
                        , len(self.users)
                        , VIP
                        , GLASSES_ID
                        , HEADTRACKING_TARGET_NAME
                        , EYE_DISTANCE
                        , NO_TRACKING_MAT)

    self.users.append(_user)

  ## Creates a RayPointer instance and adds it to the tools of this workspace.
  # @param POINTER_TRACKING_STATION The tracking target name of this RayPointer.
  # @param POINTER_DEVICE_STATION The device station name of this RayPointer.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def create_ray_pointer( self
                        , POINTER_TRACKING_STATION
                        , POINTER_DEVICE_STATION
                        , VISIBILITY_TABLE):

    _ray_pointer = RayPointer()
    _ray_pointer.my_constructor( self
                               , len(self.tools)
                               , POINTER_TRACKING_STATION
                               , POINTER_DEVICE_STATION
                               , VISIBILITY_TABLE)
    self.tools.append(_ray_pointer)