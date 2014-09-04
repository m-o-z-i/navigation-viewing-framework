#!/usr/bin/python

## @file
# Contains classes SceneManager.

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
from Scene_Hyperspace import *
import hyperspace_config

# import python libraries
# ...


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

  sf_key_w = avango.SFBool()


  # Default constructor.
  def __init__(self):
    self.super(SceneManager).__init__()

    self.key_w_before = False

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
    self.sf_key_w.connect_from(self.keyboard_sensor.Button0)


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

    # init hyperspace scenes
    for scene in hyperspace_config.active_scenes:
      print "loading hyperspace scene #{0}".format(scene)
      new_scene = eval(hyperspace_config.scenes[scene])

    self.activate_scene(0) # activate first scene

    #SCENEGRAPH.update_cache()

  @field_has_changed(sf_key_w)
  def sf_key_w_changed(self):
    if not (self.sf_key_w.value == self.key_w_before) and not self.key_w_before:
      if (hyperspace_config.active_scenes[0] in hyperspace_config.textures.keys()) and len(self.scenes) > 0:
        hyperspace_config.texture_idx += 1
        if hyperspace_config.texture_idx >= len(hyperspace_config.textures[hyperspace_config.active_scenes[0]]):
          hyperspace_config.texture_idx = 0
        self.scenes[0].tex_quad.Texture.value = hyperspace_config.textures[hyperspace_config.active_scenes[0]][hyperspace_config.texture_idx]
    self.key_w_before = self.sf_key_w.value

  '''
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
  '''

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

