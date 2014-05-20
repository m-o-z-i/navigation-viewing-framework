#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
import Tools
from Objects import *
from Scene import *

# import python libraries
import math
import time

'''
## Helper class to update material values with respect to the current time.
class TimedMaterialUniformUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in milliseconds.
  TimeIn = avango.SFFloat()

  ## @var MaterialName
  # Field containing the name of the material to be updated
  MaterialName = avango.SFString()

  ## @var UniformName
  # Field containing the name of the uniform value to be updated
  UniformName = avango.SFString()

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    avango.gua.set_material_uniform(self.MaterialName.value,
                                    self.UniformName.value,
                                    self.TimeIn.value)


## Helper class to get a rotation that alternates with respect to the current time.
class TimedSwayingUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in seconds.
  TimeIn = avango.SFFloat()

  ## @var SFRotMat
  # Field containing the rotation being calculated by this class.
  SFRotMat = avango.gua.SFMatrix4()

  # parameters
  ## @var max_rot_offset
  # Maximum rotation in degrees
  max_rot_offset = 1.0 

  ## @var frequency
  # Frequency to be applied.
  frequency      = 0.1

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    #calculate rotation of the ship
    self.SFRotMat.value = avango.gua.make_rot_mat( self.max_rot_offset * math.sin( (20 * self.frequency * self.TimeIn.value) / math.pi ),
                          0, 0, 1)


## Helper class to create a rotation matrix with resepect to the current time.
class DayAnimationUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containting the current time in seconds.
  TimeIn = avango.SFFloat()

  ## @var sf_sun_mat
  # Field containing the calculated rotation matrix for the sun.
  sf_sun_mat = avango.gua.SFMatrix4()

  ## @var day_time
  # The length of one day in seconds.
  day_time = 5 * 30.0

  ## @var morning_sun_color
  # The color of the sun at sunrise.
  morning_sun_color = avango.gua.Color(0.9, 0.65, 0.65)

  ## @var noon_sun_color
  # The color of the sun at noon.
  noon_sun_color = avango.gua.Color(1.0, 0.8, 0.8)

  ## @var evening_sun_color
  # The color of the sun at sunset.
  evening_sun_color = morning_sun_color

  ## @var sf_sun_color
  # The color of the sun.
  sf_sun_color = avango.gua.SFColor()
  sf_sun_color.value = morning_sun_color

  ## Linearly interpolates between two colors according to a given ratio.
  # @param START_COLOR The starting value for a ratio of 0.
  # @param TARGET_COLOR The final value for a ratio of 1.
  # @param RATIO A value between 0 and 1 that determines the interpolated result.
  def lerp_color(self, START_COLOR, TARGET_COLOR, RATIO):
    _start_vec  = avango.gua.Vec3(START_COLOR.r, START_COLOR.g, START_COLOR.b)
    _end_vec    = avango.gua.Vec3(TARGET_COLOR.r, TARGET_COLOR.g, TARGET_COLOR.b)
    _lerp_vec   = _start_vec.lerp_to(_end_vec, RATIO)
    return avango.gua.Color(_lerp_vec.x, _lerp_vec.y, _lerp_vec.z)

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):

    # set position of the sun
    _sun_angle = ((self.TimeIn.value % self.day_time) / self.day_time) * 360.0

    self.sf_sun_mat.value =  avango.gua.make_rot_mat(-_sun_angle, 1, 0, 0) * \
                             avango.gua.make_rot_mat(-30.0, 0, 1, 0)

    # update the sun color
    # between morning and noon
    if _sun_angle < 45:  
      self.sf_sun_color.value = self.lerp_color(self.morning_sun_color, self.noon_sun_color, _sun_angle / 45.0)
    # between noon and evening
    elif (_sun_angle > 135) and (_sun_angle < 180): 
      self.sf_sun_color.value = self.lerp_color(self.noon_sun_color, self.evening_sun_color, (_sun_angle - 135.0) / 45.0)
'''

## Class for building a scene and appending the necessary nodes to the scenegraph.
#
# The actual member variables vary from scene to scene and can be chosen at will.
class SceneManager:

  hierarchy_materials = ["data/materials/AvatarMagentaShadeless.gmd", "data/materials/AvatarGreenShadeless.gmd", "data/materials/AvatarGreenShadeless.gmd.gmd", "data/materials/AvatarGreenShadeless.gmd.gmd"]

  ## Custom constructor
  # @param NET_TRANS_NODE Scenegraph net matrix transformation node for distribution.
  def __init__(self, NET_TRANS_NODE, SCENEGRAPH):

    # create loader class for geometry loading
    _loader = avango.gua.nodes.GeometryLoader()

    # references
    self.SCENEGRAPH = SCENEGRAPH
    self.NET_TRANS_NODE = NET_TRANS_NODE

    # variables
    self.objects = [] # interactive objects    


    # init scene
    #self.scene1 = SceneVRHyperspace(self, NET_TRANS_NODE)

    self.scene2 = MedievalTown(self, NET_TRANS_NODE)    

    #self.scene3 = Test(self, NET_TRANS_NODE)

    self.reset() # enforce BoundingBox update


  # functions
  def init_geometry(self, NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE):

    _loader = avango.gua.nodes.GeometryLoader()

    _loader_flags = "avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY"

    if MATERIAL == None: # no material defined --> get materials from file description
      _loader_flags += " | avango.gua.LoaderFlags.LOAD_MATERIALS"
      MATERIAL = "data/materials/White.gmd" # default material

    if GROUNDFOLLOWING_PICK_FLAG == True or MANIPULATION_PICK_FLAG == True:
      _loader_flags += " | avango.gua.LoaderFlags.MAKE_PICKABLE"

    _node = _loader.create_geometry_from_file(NAME, FILENAME, MATERIAL, eval(_loader_flags))
    _node.Transform.value = MATRIX
  
    self.init_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
 

  def init_light(self, TYPE, NAME, COLOR, MATRIX, PARENT_NODE):

    if TYPE == 0: # sun light
      _node = avango.gua.nodes.SunLightNode()
      _node.EnableShadows.value = True
      _node.ShadowMapSize.value = 2048
      _node.ShadowOffset.value = 0.001

    elif TYPE == 1: # point light
      _node = avango.gua.nodes.PointLightNode()
      _node.Falloff.value = 1.0 # exponent

    elif TYPE == 2: # spot light
      _node = avango.gua.nodes.SpotLightNode()
      _node.EnableShadows.value = True
      _node.ShadowMapSize.value = 2048
      _node.ShadowOffset.value = 0.001
      _node.Softness.value = 1.0 # exponent
      _node.Falloff.value = 1.0 # exponent

      
    _node.Name.value = NAME
    _node.Color.value = COLOR
    _node.Transform.value = MATRIX
    _node.EnableDiffuseShading.value = True
    _node.EnableSpecularShading.value = True
    _node.EnableGodrays.value = True

    self.init_objects(_node, PARENT_NODE, False, False)


  def init_objects(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG):

    if NODE.get_type() == 'av::gua::TransformNode' and len(NODE.Children.value) > 0: # group node 

      _object = InteractiveObject()
      _object.my_constructor(self, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)

      self.objects.append(_object)

      for _child in NODE.Children.value:
        self.init_objects(_child, _object, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
        
    elif NODE.get_type() == 'av::gua::GeometryNode' or NODE.get_type() == 'av::gua::SunLightNode' or NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':

      _object = InteractiveObject()
      _object.my_constructor(self, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)

      self.objects.append(_object)

    
  def reset(self):
  
    for _object in self.objects:
      _object.reset()


  def get_hierarchy_material(self, INDEX):
  
    return self.hierarchy_materials[INDEX]
    
