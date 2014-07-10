#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate, TimedSwayingUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
import Tools
from Scene import *
from ConsoleIO import *

# import python libraries
import math
import time


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
class SceneManager(avango.script.Script):

  # input fields
  ## @var sf_key1
  # Boolean field representing the key for scene 1.
  sf_key1 = avango.SFBool()

  ## @var sf_key2
  # Boolean field representing the key for scene 2.
  sf_key2 = avango.SFBool()
  
  ## @var sf_key3
  # Boolean field representing the key for scene 3.
  sf_key3 = avango.SFBool()

  ## @var sf_key4
  # Boolean field representing the key for scene 4.
  sf_key4 = avango.SFBool()

  ## @var sf_key5
  # Boolean field representing the key for scene 5.
  sf_key5 = avango.SFBool()

  ## @var sf_key6
  # Boolean field representing the key for scene 6.
  sf_key6 = avango.SFBool()

  ## @var sf_key7
  # Boolean field representing the key for scene 7.
  sf_key7 = avango.SFBool()

  ## @var sf_key8
  # Boolean field representing the key for scene 8.
  sf_key8 = avango.SFBool()

  ## @var sf_key9
  # Boolean field representing the key for scene 9.
  sf_key9 = avango.SFBool()

  ## @var sf_key0
  # Boolean field representing the key for scene 0.
  sf_key0 = avango.SFBool()

  ## @var sf_key_home
  # Boolean field representing the home key.
  sf_key_home = avango.SFBool()


  # Default constructor.
  def __init__(self):
    self.super(SceneManager).__init__()

    # parameters

    ## @var hierarchy_materials
    # List of material strings to be used for representing the bounding box hierarchies.
    self.hierarchy_materials = ["data/materials/AvatarMagentaShadeless.gmd", "data/materials/AvatarGreenShadeless.gmd", "data/materials/AvatarOrangeShadeless.gmd", "data/materials/AvatarYellowShadeless.gmd"]

    # variables
    ## @var scenes
    # A list of scenes that were loaded.
    self.scenes = []

    ## @var active_scene
    # Number of the currently active (displayed) scene.
    self.active_scene = None

    ## @var keyboard_sensor
    # Device sensor representing the keyboard attached to the computer.
    self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.keyboard_sensor.Station.value = "device-keyboard0"

    # init field connections
    self.sf_key1.connect_from(self.keyboard_sensor.Button10) # key 1
    self.sf_key2.connect_from(self.keyboard_sensor.Button11) # key 2
    self.sf_key3.connect_from(self.keyboard_sensor.Button12) # key 3       
    self.sf_key4.connect_from(self.keyboard_sensor.Button13) # key 4
    self.sf_key5.connect_from(self.keyboard_sensor.Button14) # key 5
    self.sf_key6.connect_from(self.keyboard_sensor.Button15) # key 6
    self.sf_key7.connect_from(self.keyboard_sensor.Button16) # key 7
    self.sf_key8.connect_from(self.keyboard_sensor.Button17) # key 8
    self.sf_key9.connect_from(self.keyboard_sensor.Button18) # key 9
    self.sf_key0.connect_from(self.keyboard_sensor.Button9)  # key 0
    self.sf_key_home.connect_from(self.keyboard_sensor.Button31) # key Pos1(Home)


  ## Custom constructor
  # @param NET_TRANS_NODE Scenegraph net matrix transformation node for distribution.
  # @param SCENEGRAPH Reference to the scenegraph to which the nettrans node is appended.
  def my_constructor(self, NET_TRANS_NODE, SCENEGRAPH, NAVIGATION_LIST):

    ## @var navigation_list
    # List of all Navigation instances in the setup.
    self.navigation_list = NAVIGATION_LIST

    # init pipeline value node
    _pipeline_value_node = avango.gua.nodes.TransformNode(Name = "pipeline_values")
    NET_TRANS_NODE.Children.value.append(_pipeline_value_node)

    ## @var pipeline_info_node
    # Scenegraph node storing the actural pipeline values of the current scene.
    self.pipeline_info_node = avango.gua.nodes.TransformNode()
    _pipeline_value_node.Children.value.append(self.pipeline_info_node)

    # init scenes   
    #self.scene_weimar = SceneWeimar(self, SCENEGRAPH, NET_TRANS_NODE)
    #self.scene_monkey = SceneMonkey(self, SCENEGRAPH, NET_TRANS_NODE)
    #self.scene_medieval = SceneMedievalTown(self, SCENEGRAPH, NET_TRANS_NODE)
    #self.scene_pitoti = ScenePitoti(self, SCENEGRAPH, NET_TRANS_NODE)
    #self.scene_vianden = SceneVianden(self, SCENEGRAPH, NET_TRANS_NODE)
    #self.scene_plod = ScenePLOD(self, SCENEGRAPH, NET_TRANS_NODE)      
    
    self.scene_vianden_low = SceneViandenLow(self, SCENEGRAPH, NET_TRANS_NODE)
    #self.scene_vianden_high = SceneViandenHigh(self, SCENEGRAPH, NET_TRANS_NODE)

    self.activate_scene(0) # activate first scene

    #SCENEGRAPH.update_cache()
        

  # callbacks
  ## Called whenever sf_key1 changes.
  @field_has_changed(sf_key1)
  def sf_key1_changed(self):

    if self.sf_key1.value == True: # key pressed
      self.activate_scene(0)

  ## Called whenever sf_key2 changes.
  @field_has_changed(sf_key2)
  def sf_key2_changed(self):

    if self.sf_key2.value == True: # key pressed
      self.activate_scene(1)

  ## Called whenever sf_key3 changes.
  @field_has_changed(sf_key3)
  def sf_key3_changed(self):

    if self.sf_key3.value == True: # key pressed
      self.activate_scene(2)

  ## Called whenever sf_key4 changes.
  @field_has_changed(sf_key4)
  def sf_key4_changed(self):

    if self.sf_key4.value == True: # key pressed
      self.activate_scene(3)

  ## Called whenever sf_key5 changes.
  @field_has_changed(sf_key5)
  def sf_key5_changed(self):

    if self.sf_key5.value == True: # key pressed
      self.activate_scene(4)

  ## Called whenever sf_key6 changes.
  @field_has_changed(sf_key6)
  def sf_key6_changed(self):

    if self.sf_key6.value == True: # key pressed
      self.activate_scene(5)

  ## Called whenever sf_key7 changes.
  @field_has_changed(sf_key7)
  def sf_key7_changed(self):

    if self.sf_key7.value == True: # key pressed
      self.activate_scene(6)

  ## Called whenever sf_key8 changes.
  @field_has_changed(sf_key8)
  def sf_key8_changed(self):

    if self.sf_key8.value == True: # key pressed
      self.activate_scene(7)
      
  ## Called whenever sf_key9 changes.
  @field_has_changed(sf_key9)
  def sf_key9_changed(self):

    if self.sf_key9.value == True: # key pressed
      self.activate_scene(8)
      
  ## Called whenever sf_key0 changes.
  @field_has_changed(sf_key0)
  def sf_key0_changed(self):

    if self.sf_key0.value == True: # key pressed
      self.activate_scene(9)

  ## Called whenever sf_key_home changes.
  @field_has_changed(sf_key_home)
  def sf_key_home_changed(self):

    if self.sf_key_home.value == True: # key pressed
      self.print_active_scene()


  # functions
  ## Sets one of the loaded scene to the active (displayed) one.
  # @param ID The scene id to be activated.
  def activate_scene(self, ID):
    
    # disable all scenes
    for _scene in self.scenes:
      _scene.enable_scene(False)
  
    if ID < len(self.scenes):
      self.active_scene = self.scenes[ID]
      self.active_scene.enable_scene(True)
      self.pipeline_info_node.Name.value = self.active_scene.get_pipeline_value_string()

      # overwrite first Navigation's starting matrix if described in scene.
      if self.active_scene.starting_matrix != None and len(self.navigation_list) > 0:

        print_warning("Overwriting the platforms' starting matrices by the one given in the scene description.")

        for _navigation in self.navigation_list:
          _navigation.start_matrix = self.active_scene.starting_matrix
          _navigation.reset()

      if self.active_scene.starting_scale != None and len(self.navigation_list) > 0:

        print_warning("Overwriting the platforms' starting scale factors by the one given in the scene description.")

        for _navigation in self.navigation_list:
          _navigation.start_scale = self.active_scene.starting_scale
          _navigation.reset()
  
      print "Switching to Scene: " + self.active_scene.name
  
  ## Prints all the nodes of the active scene on the console.
  def print_active_scene(self):
  
    # print navigation nodes
    for _i, _navigation in enumerate(self.navigation_list):
      print "platform_" + str(_i), _navigation.platform.sf_abs_mat.value.get_translate(), _navigation.platform.sf_abs_mat.value.get_rotate(), _navigation.platform.sf_scale.value
  
    # print interactive objects
    if self.active_scene != None:
      
      for _object in self.active_scene.objects:
        _node = _object.node
         
        print "\n"
        print _node.Name.value
        print _node.Path.value
        print _object.hierarchy_level
        print _node.Transform.value
  
  
  ## Returns the hierarchy material string for a given depth.
  # @param INDEX The material index / depth to be returned.
  def get_hierarchy_material(self, INDEX):
  
    return self.hierarchy_materials[INDEX]
    
