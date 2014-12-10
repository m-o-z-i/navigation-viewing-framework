#!/usr/bin/python

## @file
# Contains helper methods for various tasks.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import python libraries
import math

## Converts a rotation matrix to the Euler angles yaw, pitch and roll.
# @param MATRIX The rotation matrix to be converted.
def get_euler_angles(MATRIX):

  quat = MATRIX.get_rotate()
  qx = quat.x
  qy = quat.y
  qz = quat.z
  qw = quat.w

  sqx = qx * qx
  sqy = qy * qy
  sqz = qz * qz
  sqw = qw * qw
  
  unit = sqx + sqy + sqz + sqw # if normalised is one, otherwise is correction factor
  test = (qx * qy) + (qz * qw)

  if test > 1:
    yaw = 0.0
    roll = 0.0
    pitch = 0.0

  if test > (0.49999 * unit): # singularity at north pole
    yaw = 2.0 * math.atan2(qx,qw)
    roll = math.pi/2.0
    pitch = 0.0
  elif test < (-0.49999 * unit): # singularity at south pole
    yaw = -2.0 * math.atan2(qx,qw)
    roll = math.pi/-2.0
    pitch = 0.0
  else:
    yaw = math.atan2(2.0 * qy * qw - 2.0 * qx * qz, 1.0 - 2.0 * sqy - 2.0 * sqz)
    roll = math.asin(2.0 * test)
    pitch = math.atan2(2.0 * qx * qw - 2.0 * qy * qz, 1.0 - 2.0 * sqx - 2.0 * sqz)

  if yaw < 0.0:
    yaw += 2.0 * math.pi

  if pitch < 0:
    pitch += 2 * math.pi
  
  if roll < 0:
    roll += 2 * math.pi

  return yaw, pitch, roll


## Extracts the yaw (head) rotation from a rotation matrix.
# @param MATRIX The rotation matrix to extract the angle from.
def get_yaw(MATRIX):

  try:
    _yaw, _, _ = get_euler_angles(MATRIX)
    return _yaw
  except:
    return 0


## Returns the rotation matrix of the rotation between two input vectors.
# @param VEC1 First vector.
# @param VEC2 Second vector.
def get_rotation_between_vectors(VEC1, VEC2):

  VEC1.normalize()
  VEC2.normalize()    

  _angle = math.degrees(math.acos(VEC1.dot(VEC2)))
  _axis = VEC1.cross(VEC2)

  return avango.gua.make_rot_mat(_angle, _axis)

## Returns the Euclidean distance between two points.
# @param POINT1 Starting point.
# @param POINT2 End point.
def euclidean_distance(POINT1, POINT2):
  _diff_x = POINT2.x - POINT1.x
  _diff_y = POINT2.y - POINT1.y
  _diff_z = POINT2.z - POINT1.z

  return math.sqrt(math.pow(_diff_x, 2) + math.pow(_diff_y, 2) + math.pow(_diff_z, 2))

## Computes the distance between a Point and a 3D-line.
# @param POINT_TO_CHECK The point to compute the distance for.
# @param LINE_POINT_1 One point lying on the line.
# @param LINE_VEC Direction vector of the line.
def compute_point_to_line_distance(POINT_TO_CHECK, LINE_POINT_1, LINE_VEC):

  _point_line_vec = avango.gua.Vec3(LINE_POINT_1.x - POINT_TO_CHECK.x, LINE_POINT_1.y - POINT_TO_CHECK.y, LINE_POINT_1.z - POINT_TO_CHECK.z)

  _dist = (_point_line_vec.cross(LINE_VEC)).length() / LINE_VEC.length()

  return _dist