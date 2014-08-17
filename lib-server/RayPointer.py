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
from Tool import *
from TrackingReader import TrackingTargetReader

##
class RayPointerRepresentation(ToolRepresentation):

  ##
  def __init__(self):
    self.super(RayPointerRepresentation).__init__()

  ##
  def my_constructor(self, RAY_POINTER_INSTANCE, DISPLAY_GROUP, VIEW_TRANSFORM_NODE):
    
    self.base_constructor(RAY_POINTER_INSTANCE
                                    , DISPLAY_GROUP
                                    , VIEW_TRANSFORM_NODE
                                    , "pick_ray_" + str(RAY_POINTER_INSTANCE.id)
                                    , "self.tool_transform_node.Transform.value = self.DISPLAY_GROUP.offset_to_workspace * self.TOOL_INSTANCE.tracking_reader.sf_abs_mat.value")

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var ray_geometry
    # Geometry node representing the ray graphically.
    self.ray_geometry = _loader.create_geometry_from_file( "ray_geometry"
                                                         , "data/objects/cylinder.obj"
                                                         , "data/materials/White.gmd"
                                                         , avango.gua.LoaderFlags.DEFAULTS)
    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, self.TOOL_INSTANCE.ray_length * -0.5) * \
                                        avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                        avango.gua.make_scale_mat(0.005, self.TOOL_INSTANCE.ray_length, 0.005)
    self.tool_transform_node.Children.value.append(self.ray_geometry)

    self.always_evaluate(True)


##
class RayPointer(Tool):

  # internal fields
  ## @var sf_pointer_button0
  # Boolean field representing the first button of the pointer.
  sf_pointer_button0 = avango.SFBool()

  ## @var sf_pointer_button1
  # Boolean field representing the second button of the pointer.
  sf_pointer_button1 = avango.SFBool()

  ## @var sf_pointer_button2
  # Boolean field representing the third button of the pointer.
  sf_pointer_button2 = avango.SFBool()  

  ## @var mf_pointer_pick_result
  # Intersections of the picking ray with the objects in the scene.
  mf_pointer_pick_result = avango.gua.MFPickResult()

  ## Default constructor.
  def __init__(self):
    self.super(RayPointer).__init__()

  ## Custom constructor.
  # @param MANIPULATION_MANAGER Reference to the ManipulationManager instance to which this RayPointer is associated.
  def my_constructor(self, WORKSPACE_INSTANCE, TOOL_ID, POINTER_TRACKING_STATION, POINTER_DEVICE_STATION):

    self.base_constructor(WORKSPACE_INSTANCE, TOOL_ID, POINTER_TRACKING_STATION)

    # parameters
    ## @var ray_length
    # Length of the pointer's ray in meters.
    self.ray_length = 10.0

    ## @var ray_thickness
    # Thickness of the pointer's ray in meters.
    self.ray_thickness = 0.0075

    ## @var intersection_sphere_size
    # Radius of the intersection sphere in meters.
    self.intersection_sphere_size = 0.025

    ## @var hierarchy_selection_level
    # Hierarchy level which is selected by this pointer.
    self.hierarchy_selection_level = 0

    # variables

    ## @var highlighted_object
    # Reference to the currently highlighted object.
    self.highlighted_object = None

    ## @var dragged_object
    # Reference to the currently dragged object.
    self.dragged_object = None

    ## @var dragging_offset
    # Offset to be applied during the dragging process.
    self.dragging_offset = None

    ## @var ray_pointer_representations
    # List of RayPointerRepresentation instances belonging to this RayPointer.
    self.ray_pointer_representations = []
    
    ## @var pointer_device_sensor
    # Device sensor capturing the pointer's button input values.
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = POINTER_DEVICE_STATION
    
    # init field connections
    self.sf_pointer_button0.connect_from(self.device_sensor.Button0)
    self.sf_pointer_button1.connect_from(self.device_sensor.Button1)
    self.sf_pointer_button2.connect_from(self.device_sensor.Button2)

  ##
  #
  def create_ray_pointer_representation_for(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE):

    _ray_pointer_repr = RayPointerRepresentation()
    _ray_pointer_repr.my_constructor(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE)
    self.ray_pointer_representations.append(_ray_pointer_repr)
    return _ray_pointer_repr
