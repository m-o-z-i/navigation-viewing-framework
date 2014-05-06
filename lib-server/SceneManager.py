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

# import python libraries
import math
import time
import random

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


## Class for building a scene and appending the necessary nodes to the scenegraph.
#
# The actual member variables vary from scene to scene and can be chosen at will.
class SceneManager:

  ## Custom constructor
  # @param LOADER The geometry loader to be used.
  # @param NET_TRANS_NODE Scenegraph net matrix transformation node for distribution.
  def __init__(self, LOADER, NET_TRANS_NODE):

    self.timer = avango.nodes.TimeSensor()

    # create town
    self.town = LOADER.create_geometry_from_file( 'town',
                                                  'data/objects/medieval_harbour/town.obj',
                                                  'data/materials/Stones.gmd',
                                                  avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    self.town.Transform.value = avango.gua.make_scale_mat(7.5, 7.5, 7.5)
    NET_TRANS_NODE.Children.value.append(self.town)

    # create water
    
    self.water = LOADER.create_geometry_from_file('water_geometry',
                                                  'data/objects/plane.obj',
                                                  'data/materials/Water.gmd',
                                                  avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    self.water.Transform.value =  avango.gua.make_trans_mat(0, -3.15, 0) *\
                                  avango.gua.make_scale_mat(1500.0, 1.0, 1500.0)
    NET_TRANS_NODE.Children.value.append(self.water)
    self.water_updater = TimedMaterialUniformUpdate()
    self.water_updater.MaterialName.value = "data/materials/Water.gmd"
    self.water_updater.UniformName.value = "time"
    self.water_updater.TimeIn.connect_from(self.timer.Time)
    

    '''
    # create ship
    self.ship_transform = avango.gua.nodes.TransformNode(Name = 'ship_transform')
    self.ship_transform.Transform.value = avango.gua.make_trans_mat(0, 2.2, 33) * avango.gua.make_scale_mat(7, 7, 7)
    self.ship = LOADER.create_geometry_from_file( 'ship_geometry', 
                                                  'data/objects/suzannes_revenge/ship.dae', 
                                                  'data/materials/SimplePhongWhite.gmd', 
                                                  avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    self.ship_transform.Children.value.append(self.ship)
    NET_TRANS_NODE.Children.value.append(self.ship_transform)
    self.swaying_updater = TimedSwayingUpdate()
    self.swaying_updater.TimeIn.connect_from(self.timer.Time)
    self.ship.Transform.connect_from(self.swaying_updater.SFRotMat)


    #create plank
    self.plank_transform = avango.gua.nodes.TransformNode(Name = 'plank_transform')
    self.plank = LOADER.create_geometry_from_file( 'plank_geometry',
                                                   'data/objects/cube.obj',
                                                   'data/materials/Wood.gmd',
                                                   avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    self.plank.Transform.value = avango.gua.make_trans_mat(0.45, 0.76, 26) *\
                                  avango.gua.make_rot_mat(-18, 1, 0, 0) *\
                                  avango.gua.make_scale_mat(0.4, 0.05, 2.4)
    self.plank_transform.Transform.connect_from(self.swaying_updater.SFRotMat)
    self.plank_transform.Children.value.append(self.plank)
    NET_TRANS_NODE.Children.value.append(self.plank_transform)
    '''
    
    # commented out because SunLightNode is not distributable yet, so we use the SpotLightNode above instead
    self.sun = avango.gua.nodes.SunLightNode( Name = "sun",
                                              Color = avango.gua.Color(1.0, 0.7, 0.5),
                                              EnableShadows = True,
                                              EnableGodrays = True,
                                              EnableDiffuseShading = True,
                                              EnableSpecularShading = True,
                                              ShadowMapSize = 2048,
                                              ShadowOffset = 0.0008
                                        )

    self.day_updater = DayAnimationUpdate()
    #self.day_updater.TimeIn.connect_from(self.timer.Time)
    test = avango.SFFloat()
    test.value = 30.0
    self.day_updater.TimeIn.connect_from(test)
    self.sun.Transform.connect_from(self.day_updater.sf_sun_mat)
    self.sun.Color.connect_from(self.day_updater.sf_sun_color)
    
    NET_TRANS_NODE.Children.value.append(self.sun)
