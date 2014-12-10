#!/usr/bin/python

## @file
# Contains class Intersection.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import python libraries
# ...

## Helper class to determine the intersections of a ray with the objects in
# a scene.

class Intersection(avango.script.Script):

  # input fields
  ## @var sf_pick_mat
  # Starting matrix of the ray to be analyzed.
  sf_pick_mat = avango.gua.SFMatrix4()

  # output fields
  ## @var mf_pick_result
  # Intersections of the ray with the objects in the scene.
  mf_pick_result = avango.gua.MFPickResult()

  ## Default constructor.
  def __init__(self):
    self.super(Intersection).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH The scenegraph where to look for intersections of the ray.
  # @param SF_PICK_MAT Starting matrix of the ray.
  # @param PICK_LENGTH Length of the ray in meters.
  # @param PICK_MASK Picking mask of the intersection process.
  # @param PICK_ONLY_FIRST_OBJECT Boolean saying if only the first hit is to be taken.
  def my_constructor(self, SCENEGRAPH, SF_PICK_MAT, PICK_LENGTH, PICK_MASK = "", PICK_ONLY_FIRST_OBJECT = True):
    
    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH
  
    ## @var pick_length
    # Length of the ray in meters.
    self.pick_length = PICK_LENGTH
  
    ## @var activated
    # Indicates if the intersection computation is activated or not. In the last case,
    # nothing will be written in mf_pick_result.
    self.activated = True
  
    ## @var ray
    # The spatial ray to be analyzed.
    self.ray = avango.gua.nodes.RayNode()
  
    ## @var picking_options
    # Picking options for the intersection process.
    if PICK_ONLY_FIRST_OBJECT:
      self.picking_options = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                           | avango.gua.PickingOptions.GET_POSITIONS \
                           | avango.gua.PickingOptions.GET_WORLD_POSITIONS \
                           | avango.gua.PickingOptions.GET_WORLD_NORMALS
    else:
      self.picking_options = avango.gua.PickingOptions.GET_POSITIONS \
                           | avango.gua.PickingOptions.GET_WORLD_POSITIONS \
                           | avango.gua.PickingOptions.GET_WORLD_NORMALS
    
    ## @var picking_mask
    # Picking mask of the intersection process.
    self.picking_mask = PICK_MASK
  
    # init field connections
    self.sf_pick_mat.connect_from(SF_PICK_MAT)
  
    self.always_evaluate(True)
    
  ## Evaluated every frame.
  def evaluate(self):
  
    if self.activated == True:
     
      # set ray properties
      self.ray.Transform.value =  self.sf_pick_mat.value * \
                                  avango.gua.make_scale_mat(1.0, 1.0, self.pick_length)

      #print self.pick_length, self.ray.Transform.value, self.ray.Transform.value.get_rotate()
          
      # compute picking results
      _pick_result = self.SCENEGRAPH.ray_test(self.ray, self.picking_options, self.picking_mask)
      self.mf_pick_result.value = _pick_result.value
  

  ## Activate/Deactivate the intersection procedure.
  def activate(self, FLAG):
    self.activated = FLAG

