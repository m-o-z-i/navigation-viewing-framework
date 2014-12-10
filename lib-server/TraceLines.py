#!/usr/bin/python

## @file
# Contains class Trace.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
import Utilities
from scene_config import scenegraphs

# import python libraries
import time

## Class which handles the creation and updating of the trace lines.
#
# Is used by Navigation instances to draw the trace of their movement.
class Trace:

  ## Default constructor.
  # @param IDENTIFIER A string that is appended to the scene graph name to separate the line segments of multiple instances of this class.
  # @param NUM_LINES The number of line segments to be used.
  # @param LINE_DISTANCE The overall distance of all line segments together. Determines how long the trace lines are kept before they are overwritten.
  # @param INITIAL_MAT This matrix is used as initial position of all line segments.
  # @param TRACE_MATERIAL The material to be used to display the trace.
  def __init__(self, IDENTIFIER, NUM_LINES, LINE_DISTANCE, INITIAL_MAT, TRACE_MATERIAL):

    ## @var num_lines
    # The number of line segments that are used.
    self.num_lines = NUM_LINES

    ## @var distance_trigger
    # After this distance a new line segment is created. This value is calculated with the given parameters and determines the resolution the trace line.
    self.distance_trigger = LINE_DISTANCE / NUM_LINES
    
    ## @var lines
    # A list of scene graph nodes where each respresents a line segment.
    self.lines  = []

    ## @var line_thickness
    # Thickness of the trace lines in meters.
    self.line_thickness = 0.1

    ## @var transform_node
    # A transform node that is the parent of all line segments. It groups the line segments in the scene graph as the given identifier is added to its name and therefore allows multiple instances of this class.
    self.transform_node = avango.gua.nodes.TransformNode(Name = 'nav_trace_' + str(IDENTIFIER))
    #self.transform_node = avango.gua.nodes.TransformNode(Name = 'nav_trace_' + str(0))
    scenegraphs[0]["/net"].distribute_object(self.transform_node)
    scenegraphs[0]["/net"].Children.value.append(self.transform_node)

    # create each line segment node by loading the geometry and appending it to the parent node
    _loader = avango.gua.nodes.TriMeshLoader()
    for i in range(self.num_lines):
      _line = _loader.create_geometry_from_file('line_geometry_' + str(i), 'data/objects/cube.obj', 'data/materials/' + TRACE_MATERIAL + '.gmd', avango.gua.LoaderFlags.DEFAULTS)
      _line.Transform.value = avango.gua.make_scale_mat(0, 0, 0)
      _line.ShadowMode.value = avango.gua.ShadowMode.OFF
      scenegraphs[0]["/net"].distribute_object(_line)
      self.lines.append(_line)

    # append all line segments to the transform_node that groups the tracing lines of different platforms.
    self.transform_node.Children.value = self.lines

    ## @var crrnt_idx
    # The index of the current point in the list of lines.
    self.crrnt_idx = 0

    ## @var crrnt_point
    # The end point of the last drawn line segment that is used as start point for the next line segment. It is initialized with the translation of the INITIAL_MATRIX parameter.
    self.crrnt_point = INITIAL_MAT.get_translate()

  ## Appends a string to the GroupNames field of all line segments.
  def append_to_group_names(self, STRING):

    for _line in self.lines:
      _line.GroupNames.value.append(STRING)


  ## Calculates the transformation matrix of a line segment node in the scene graph.
  def calc_transform_mat(self, START_VEC, END_VEC):

    # calc the vector in between the two points, the resulting center of the line segment and the scaling needed to connect both points
    _vec = avango.gua.Vec3( END_VEC.x - START_VEC.x, END_VEC.y - START_VEC.y, END_VEC.z - START_VEC.z)
    _center = START_VEC + (_vec * 0.5)
    _scale  = 0.5 * _vec.length()

    # calc the rotation according negative z-axis
    _rotation_mat = Utilities.get_rotation_between_vectors(avango.gua.Vec3(0, 0, -1), _vec)

    # build the complete matrix
    return avango.gua.make_trans_mat(_center) * _rotation_mat * avango.gua.make_scale_mat(self.line_thickness, self.line_thickness, _scale * 2.0)

  ## Clears the traces and starts drawing again from the current position.
  def clear(self, CURRENT_MAT):
    _clear_transform_mat = self.calc_transform_mat(CURRENT_MAT.get_translate(), CURRENT_MAT.get_translate())

    for _line in self.lines:
      _line.Transform.value = _clear_transform_mat

    self.crrnt_point = CURRENT_MAT.get_translate()

  ## Update function that updates the point list whenever the time_offset was reached.
  def update(self, ABS_MAT):

    # only update when time_offset is reached
    if Utilities.euclidean_distance(ABS_MAT.get_translate(), self.crrnt_point) > self.distance_trigger:

      # increase index counter
      self.crrnt_idx = (self.crrnt_idx + 1) % self.num_lines

      # set line segment's transform matrix
      self.lines[self.crrnt_idx].Transform.value = self.calc_transform_mat(self.crrnt_point, ABS_MAT.get_translate())
      
      # set current position as new start point for the next line segment
      self.crrnt_point = ABS_MAT.get_translate()
