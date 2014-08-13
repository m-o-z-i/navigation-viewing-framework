#!/usr/bin/python

## @file
# Contains class GroundFollowing.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from   avango.script import field_has_changed

# import framework libraries
from Intersection import *
from scene_config import scenegraphs

# import python libraries
import math

## Class to realize a simple ground following method.
# 
# This class takes a matrix as an input and corrects it with
# respect to gravity using the scenegraph. Therefore, a ray
# is shot from a specific start height downwards and the intersection
# point is compared to the position of the device belonging to the platform.

class GroundFollowing(avango.script.Script):

  # input field
  ## @var sf_abs_input_mat
  # The input matrix to be corrected by the ground following algorithm.
  sf_abs_input_mat = avango.gua.SFMatrix4()
  sf_abs_input_mat.value = avango.gua.make_identity_mat()

  # output field
  ## @var sf_abs_output_mat
  # The corrected matrix after the ground following algorithm was applied.
  sf_abs_output_mat = avango.gua.SFMatrix4()
  sf_abs_output_mat.value = avango.gua.make_identity_mat()

  # internal fields
  ## @var sf_gf_start_mat
  # The matrix representing the position where the sent ray to the ground starts. 
  sf_gf_start_mat = avango.gua.SFMatrix4()
  sf_gf_start_mat.value = avango.gua.make_identity_mat()

  ## @var sf_station_mat
  # The matrix representing the position of the device belonging to the platform.
  sf_station_mat = avango.gua.SFMatrix4()
  sf_station_mat.value = avango.gua.make_identity_mat()

  ## @var sf_scale
  # The current scaling factor of the Navigation.
  sf_scale = avango.SFFloat()
  sf_scale.value = 1.0

  ## @var mf_ground_pick_result
  # Intersections of the ground following ray with the objects in the scene.
  mf_ground_pick_result = avango.gua.MFPickResult()

  ## Default constructor.
  def __init__(self):
    self.super(GroundFollowing).__init__()

  ## Custom constructor.
  # @param SF_STATION_MAT The field containing the current position of the device belonging to the platform.
  # @param RAY_START_HEIGHT A height from which the ground following ray will originate.
  def my_constructor(self, SF_STATION_MAT, RAY_START_HEIGHT):
    
    # attributes
    ## @var activated
    # Indicates if the ground following algorithm is activated or deactivated. In the last case,
    # the input matrix is simply passed through.
    self.activated = False

    ## @var falling
    # A boolean indicating if the user is currently falling. Used for fall speed computations.
    self.falling = False

    ## @var initial_fall_velocity
    # The starting velocity when the user is falling in meters per frame. Is increased the longer the falling process goes on.
    self.initial_fall_velocity = 0.05

    ## @var height_modification_factor
    # Scaling factor used for the modification of up and down vectors.
    self.height_modification_factor = 0.15

    # fall velocity in meter per frame
    ## @var fall_velocity
    # Speed when the user is falling in meters per frame.
    self.fall_velocity = self.initial_fall_velocity

    # pick length in meter
    ## @var ground_pick_length
    # Length of the ground following ray.
    self.ground_pick_length = 100.0

    ## @var ground_pick_direction_mat
    # Direction of the ground following ray.
    self.ground_pick_direction_mat = avango.gua.make_identity_mat()

    ## @var SCENEGRAPH
    # Reference to the scenegraph to intersect the ground following ray with.
    self.SCENEGRAPH = scenegraphs[0]

    ## @var ray_start_height
    # Starting height of the ground following ray.
    self.ray_start_height = RAY_START_HEIGHT

    # initialize shoot and output matrices
    self.sf_abs_output_mat.value = self.sf_abs_input_mat.value

    self.set_pick_direction(avango.gua.Vec3(0.0, -1.0, 0.0))

    # init field connections
    self.sf_station_mat.connect_from(SF_STATION_MAT)

    # init internal class
    ## @var ground_intersection
    # Intersection class to determine the intersections of the ground following ray with the objects in the scenegraph.
    self.ground_intersection = Intersection()
    self.ground_intersection.my_constructor(self.SCENEGRAPH, self.sf_gf_start_mat, self.ground_pick_length, "gf_pick_group")
    self.mf_ground_pick_result.connect_from(self.ground_intersection.mf_pick_result)


  ## Evaluated every frame.
  def evaluate(self):
    if self.activated == True:
      # platform translation in the world
      _platform_trans_vec = self.sf_abs_input_mat.value.get_translate()

      # tracked device translation on the platform
      _device_trans_vec = self.sf_station_mat.value.get_translate()

      # prepare ground following matrix
      _gf_start_pos = self.sf_station_mat.value.get_translate()
      _gf_start_pos.y = self.ray_start_height
      _gf_start_pos *= self.sf_scale.value
      _gf_start_pos = self.sf_abs_input_mat.value * _gf_start_pos
      _gf_start_pos = avango.gua.Vec3(_gf_start_pos.x, _gf_start_pos.y, _gf_start_pos.z)
      self.sf_gf_start_mat.value = avango.gua.make_trans_mat(_gf_start_pos) * self.ground_pick_direction_mat

      if len(self.mf_ground_pick_result.value) > 0: # an intersection with the ground was found

        # get first intersection target
        _pick_result = self.mf_ground_pick_result.value[0]             
        #print _pick_result.Object.value, _pick_result.Object.value.Name.value

        # compare distance to ground and ray_start_height
        _distance_to_ground = _pick_result.Distance.value * self.ground_pick_length
        _difference = _distance_to_ground - (self.ray_start_height * self.sf_scale.value)
        _difference = round(_difference, 3)

        if _difference < 0: # climb up

          # end falling when necessary
          if self.falling:
            self.falling = False
            self.fall_velocity = self.initial_fall_velocity 

          # move player up
          _up_vec = avango.gua.Vec3(0.0, _difference * -1.0 * self.height_modification_factor, 0.0)
          self.sf_abs_output_mat.value = avango.gua.make_trans_mat(_up_vec) * self.sf_abs_input_mat.value

        elif _difference > 0:
          
          if _difference > (self.ray_start_height * self.sf_scale.value): # falling

            # make player fall down faster every time
            self.falling = True
            _fall_vec = avango.gua.Vec3(0.0, -self.fall_velocity, 0.0)
            self.sf_abs_output_mat.value = avango.gua.make_trans_mat(_fall_vec) * self.sf_abs_input_mat.value
            self.fall_velocity += 0.005

          else: # climb down
            
            # end falling when necessary
            if self.falling:
              self.falling = False
              self.fall_velocity = self.initial_fall_velocity 

            # move player down
            _down_vec = avango.gua.Vec3(0.0, _difference * -1.0 * self.height_modification_factor, 0.0)
            self.sf_abs_output_mat.value = avango.gua.make_trans_mat(_down_vec) * self.sf_abs_input_mat.value

        else:
          self.sf_abs_output_mat.value = self.sf_abs_input_mat.value        # player remains on ground

      else:
        #print "None"
        self.sf_abs_output_mat.value = self.sf_abs_input_mat.value          # no intersection with ground was found
  
    else:
      self.sf_abs_output_mat.value = self.sf_abs_input_mat.value            # ground following is deactivated


  ## Sets the pick_direction attribute.
  # @param PICK_DIRECTION New pick direction.
  def set_pick_direction(self, PICK_DIRECTION):

    PICK_DIRECTION.normalize()
    
    _ref = avango.gua.Vec3(0.0,0.0,-1.0)
    _angle = math.degrees(math.acos(_ref.dot(PICK_DIRECTION)))
    _axis = _ref.cross(PICK_DIRECTION)

    self.ground_pick_direction_mat = avango.gua.make_rot_mat(_angle, _axis)


  ## Activates the ground following algorithm.
  def activate(self):
    self.activated = True
    self.ground_intersection.activate(True)

  ## Deactivates the ground following algorithm. The input matrix is just passed through after calling this method.
  def deactivate(self):
    self.activated = False
    self.ground_intersection.activate(False)
