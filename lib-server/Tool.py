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
                   , VIEW_TRANSFORM_NODE
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
    self.view_transform_node = VIEW_TRANSFORM_NODE

    ##
    #
    self.workspace_id = int(VIEW_TRANSFORM_NODE.Name.value.split("_")[0].replace("w", ""))

    ##
    #
    self.transformation_policy = TRANSFORMATION_POLICY

    ##
    #
    self.tool_transform_node = avango.gua.nodes.TransformNode(Name = TOOL_TRANSFORM_NODE_NAME)
    VIEW_TRANSFORM_NODE.Children.value.append(self.tool_transform_node)



    self.always_evaluate(True)

  ##
  def get_world_transformation(self):

    return self.tool_transform_node.WorldTransform.value

  ##
  def evaluate(self):

    exec self.transformation_policy


class Tool(avango.script.Script):

  def __init__(self):
    self.super(Tool).__init__()


  def base_constructor(self, WORKSPACE_INSTANCE, TOOL_ID):

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
  def assign_user(self, USER_INSTANCE):

    self.assigned_user = USER_INSTANCE