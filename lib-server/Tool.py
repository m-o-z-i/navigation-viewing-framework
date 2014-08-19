#!/usr/bin/python

## @file
# Contains class RayPointer.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
from TrackingReader import TrackingTargetReader

##
class ToolRepresentation(avango.script.Script):

  ##
  def __init__(self):
    self.super(ToolRepresentation).__init__()

  ##
  def base_constructor(self
                   , TOOL_INSTANCE
                   , DISPLAY_GROUP
                   , USER_REPRESENTATION
                   , TOOL_TRANSFORM_NODE_NAME
                   , TRANSFORMATION_POLICY):
    
    ##
    #
    self.TOOL_INSTANCE = TOOL_INSTANCE

    ##
    #
    self.DISPLAY_GROUP = DISPLAY_GROUP

    ##
    #
    self.USER_REPRESENTATION = USER_REPRESENTATION

    ##
    #
    self.user_id = self.USER_REPRESENTATION.USER.id

    ##
    #
    self.workspace_id = int(self.USER_REPRESENTATION.view_transform_node.Name.value.split("_")[0].replace("w", ""))

    ##
    #
    self.transformation_policy = TRANSFORMATION_POLICY

    ##
    #
    self.tool_transform_node = avango.gua.nodes.TransformNode(Name = TOOL_TRANSFORM_NODE_NAME)
    self.USER_REPRESENTATION.view_transform_node.Children.value.append(self.tool_transform_node)



    self.always_evaluate(True)

  ##
  def get_world_transform(self):

    return self.tool_transform_node.WorldTransform.value

  ##
  #
  def reset_visualization_group_names(self):
    pass

  ##
  #
  def append_to_visualization_group_names(self, STRING):
    pass

  ##
  #
  def remove_from_visualization_group_names(self, STRING):
    pass

  ##
  def evaluate(self):

    exec self.transformation_policy


class Tool(avango.script.Script):

  def __init__(self):
    self.super(Tool).__init__()


  def base_constructor(self
                     , WORKSPACE_INSTANCE
                     , TOOL_ID
                     , TRACKING_STATION):

    # references
    ## @var WORKSPACE_INSTANCE
    # Workspace instance at which this tool is registered.
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ## @var id
    # Identification number of the Tool within the workspace.
    self.id = TOOL_ID

    ##
    #
    self.assigned_user = None

    ##
    #
    self.tool_representations = []

    # init sensors
    self.tracking_reader = TrackingTargetReader()
    self.tracking_reader.my_constructor(TRACKING_STATION)
    self.tracking_reader.set_transmitter_offset(self.WORKSPACE_INSTANCE.transmitter_offset)
    self.tracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    self.always_evaluate(True)

  ##
  #
  def create_candidate_list(self):
    pass

  ##
  #
  def choose_from_candidate_list(self, CANDIDATE_LIST):
    pass

  ##
  def check_for_user_assignment(self):

    _closest_user = None
    _closest_distance = 1000

    for _user in self.WORKSPACE_INSTANCE.users:

      if _user.is_active:

        _dist = self.compute_line_distance( self.tracking_reader.sf_abs_vec.value
                                          , _user.headtracking_reader.sf_abs_vec.value
                                          , avango.gua.Vec3(0, -1, 0) )
        if _dist < _closest_distance:
          _closest_distance = _dist
          _closest_user = _user

    if _closest_user != self.assigned_user:
      self.assign_user(_closest_user)


  ##
  def assign_user(self, USER_INSTANCE):

    self.assigned_user = USER_INSTANCE

    for _display_group in self.WORKSPACE_INSTANCE.display_groups:
      self.WORKSPACE_INSTANCE.trigger_tool_visibilities_at(_display_group.id)

  ##
  #
  def compute_line_distance(self, POINT_TO_CHECK, LINE_POINT_1, LINE_VEC):

    _point_line_vec = avango.gua.Vec3(LINE_POINT_1.x - POINT_TO_CHECK.x, LINE_POINT_1.y - POINT_TO_CHECK.y, LINE_POINT_1.z - POINT_TO_CHECK.z)

    _dist = (_point_line_vec.cross(LINE_VEC)).length() / LINE_VEC.length()

    return _dist