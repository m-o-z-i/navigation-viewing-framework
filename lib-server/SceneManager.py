#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from   avango.script import field_has_changed
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
class SceneManager(avango.script.Script):

  ## @var treasure_position
  # List of matrices indicating all possible positions of treasures.
  treasure_positions = [avango.gua.make_trans_mat(8.235, 1.203, 13.185),
                        avango.gua.make_trans_mat(7.818, 1.204, -1.089),
                        avango.gua.make_trans_mat(-7.201, 1.237, -7.024),
                        avango.gua.make_trans_mat(15.391, 4.091, -15.492),
                        avango.gua.make_trans_mat(12.379, 4.091, -1.012),
                        avango.gua.make_trans_mat(-12.178, 1.204, 11.465),
                        avango.gua.make_trans_mat(-10.426, 3.760, 7.580),
                        avango.gua.make_trans_mat(8.239, 4.091, -8.893),
                        avango.gua.make_trans_mat(14.381, 4.091, 19.217),
                        avango.gua.make_trans_mat(-11.357, 1.204, -7.378),
                        avango.gua.make_trans_mat(2.280, 0.341, 34.095),
                        avango.gua.make_trans_mat(-21.622, 8.175, 32.795),
                        avango.gua.make_trans_mat(12.265, 4.683, 32.921),
                        avango.gua.make_trans_mat(0.588, 1.204, 5.045),
                        avango.gua.make_trans_mat(18.998, 1.204, 0.020),
                        avango.gua.make_trans_mat(-21.615, 1.204, -12.392)
                       ]


  ## Default constructor.
  def __init__(self):
    self.super(SceneManager).__init__()

  ## Custom constructor
  # @param LOADER The geometry loader to be used.
  # @param NET_TRANS_NODE Scenegraph net matrix transformation node for distribution.
  # @param VIEWING_MANAGER Reference to the viewing manager for user list.
  def my_constructor(self, LOADER, NET_TRANS_NODE, VIEWING_MANAGER):

    self.timer = avango.nodes.TimeSensor()

    # create town
    self.town = LOADER.create_geometry_from_file( 'town',
                                                  'data/objects/medieval_harbour/town.obj',
                                                  'data/materials/Stones.gmd',
                                                  avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    self.town.Transform.value = avango.gua.make_scale_mat(7.5, 7.5, 7.5)
    NET_TRANS_NODE.Children.value.append(self.town)

    # create marketbooth
    self.marketbooth_trans = avango.gua.nodes.TransformNode(Name = 'marketbooth_trans')
    self.marketbooth = LOADER.create_geometry_from_file( 'marketbooth',
                                                         'data/objects/marketbooth/market_booth.obj',
                                                         'data/materials/Stones.gmd',
                                                         avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.marketbooth_trans.Children.value.append(self.marketbooth)

    self.apple = LOADER.create_geometry_from_file( 'apple',
                                                   'data/objects/apfel/apfel.obj',
                                                   'data/materials/Stones.gmd',
                                                   avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.apple.Transform.value = avango.gua.make_trans_mat(-0.9, 1.4, 0.4)
    self.marketbooth_trans.Children.value.append(self.apple)

    self.marketbooth_trans.Transform.value = avango.gua.make_trans_mat(2.6, 0.0, -5.0) * avango.gua.make_rot_mat(-30, 0, 1, 0) * avango.gua.make_scale_mat(0.5, 0.6, 0.6)
   
    self.banana =  LOADER.create_geometry_from_file( 'banana',
                                                     'data/objects/bananas/Bananas.obj',
                                                     'data/materials/Stones.gmd',
                                                     avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.banana.Transform.value = avango.gua.make_trans_mat(0, 1.65, 0.5) * avango.gua.make_rot_mat(-75, 0, 1, 0) * avango.gua.make_scale_mat(0.15, 0.15, 0.15)

    self.banana2 =  LOADER.create_geometry_from_file( 'banana2',
                                                     'data/objects/bananas/Bananas.obj',
                                                     'data/materials/Stones.gmd',
                                                     avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.banana2.Transform.value = avango.gua.make_trans_mat(0, 1.65, 0.1) * avango.gua.make_rot_mat(-75, 0, 1, 0) * avango.gua.make_scale_mat(0.15, 0.15, 0.15)

    self.marketbooth_trans.Children.value.append(self.banana)
    self.marketbooth_trans.Children.value.append(self.banana2) 

    NET_TRANS_NODE.Children.value.append(self.marketbooth_trans)

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
    
    

    # create sun
    self.sun = avango.gua.nodes.SpotLightNode( Name = "sun",
                                              Color = avango.gua.Color(1.0, 0.7, 0.5),
                                              EnableShadows = True,
                                              EnableGodrays = False,
                                              EnableDiffuseShading = True,
                                              EnableSpecularShading = True,
                                              ShadowMapSize = 2048,
                                              ShadowOffset = 0.008
                                        )
    self.sun.Transform.value =  avango.gua.make_trans_mat(-2, 70, 20) *\
                                avango.gua.make_rot_mat(-80, 1, 0, 0) *\
                                avango.gua.make_scale_mat(500, 700, 500)

    '''
    # commented out because SunLightNode is not distributable yet, so we use the SpotLightNode above instead
    self.sun = avango.gua.nodes.SunLightNode( Name = "sun",
                                              Color = avango.gua.Color(1.0, 0.7, 0.5),
                                              EnableShadows = False,
                                              EnableGodrays = True,
                                              EnableDiffuseShading = True,
                                              EnableSpecularShading = True,
                                              ShadowMapSize = 2048,
                                              ShadowOffset = 0.0008
                                        )

    self.day_updater = DayAnimationUpdate()
    self.day_updater.TimeIn.connect_from(self.timer.Time)
    self.sun.Transform.connect_from(self.day_updater.sf_sun_mat)
    self.sun.Color.connect_from(self.day_updater.sf_sun_color)
    '''
    NET_TRANS_NODE.Children.value.append(self.sun)

    # save users to be checked for treasures
    self.users_to_check = []

    for _powerwall_user in VIEWING_MANAGER.powerwall_user_list:
      self.users_to_check.append(_powerwall_user)

    for _ovr_user in VIEWING_MANAGER.ovr_user_list:
      self.users_to_check.append(_ovr_user)

    for _desktop_user in VIEWING_MANAGER.desktop_user_list:
      self.users_to_check.append(_desktop_user)

    ## @var scoreboard
    # A dict containing the platform ids and their current scores.
    self.scoreboard = dict()

    ## @var platform_names
    # Names associated to platform ids to be displayed in the scoreboard.
    self.platform_names = dict()

    ## @var platform_materials
    # Trace and avatar materials associated to platform ids.
    self.platform_materials = dict()

    for _nav in VIEWING_MANAGER.navigation_list:
      self.scoreboard[_nav.platform.platform_id] = 0
      self.platform_materials[_nav.platform.platform_id] = _nav.trace_material
      self.platform_names[_nav.platform.platform_id] = "Platform " + str(_nav.platform.platform_id) + " (" + _nav.input_sensor_type + " - " + _nav.trace_material.replace('Avatar', '') + ")"

    ## @var frames_since_last_score
    # Past frames since the last team scored a point.
    self.frames_since_last_score = 0

    ## @var VIEWING_MANAGER
    # Reference to the viewing manager in the setup.
    self.VIEWING_MANAGER = VIEWING_MANAGER

    ## @var NET_TRANS_NODE
    # Scenegraph net matrix transformation node for distribution.
    self.NET_TRANS_NODE = NET_TRANS_NODE

    self.display_treasures(LOADER, NET_TRANS_NODE)
    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):
    
    # increase frame counter
    self.frames_since_last_score += 1

    # check for every user and every treasure if user is close enough
    for _user in self.users_to_check:
      for _treasure in self.treasure_list:
        _treasure_pos = _treasure.WorldTransform.value.get_translate()
        _user_pos = _user.head_transform.WorldTransform.value.get_translate()
        _user_pos.y = _user_pos.y - _user.head_transform.Transform.value.get_translate().y

        if Tools.euclidean_distance(_treasure_pos, _user_pos) < 0.5 and \
           _treasure.GroupNames.value[0] == 'display_group' and \
           self.frames_since_last_score > 100:
          self.update_treasure_display(_treasure)
          self.scoreboard[_user.platform_id] += 1
          self.print_scoreboard()
          return

  ## Resets the point counter for each platform to zero and replaces the platforms
  # to their starting positions.
  def reset_game(self):
    for key in self.scoreboard:
      self.scoreboard[key] = 0

    for _nav in self.VIEWING_MANAGER.navigation_list:
      _nav.reset()

    print "Game reset"
    self.print_scoreboard()


  ## Prints the current treasure hunt's scoreboard.
  def print_scoreboard(self):
  
    _scoreboard_string = '''                                        __                                 __      
                                       /\ \                               /\ \     
        ____    ___    ___   _ __    __\ \ \____    ___      __     _ __  \_\ \     
       /',__\  /'___\ / __`\/\`'__\/'__`\ \ '__`\  / __`\  /'__`\  /\`'__\/'_` \    
      /\__, `\/\ \__//\ \L\ \ \ \//\  __/\ \ \L\ \/\ \L\ \/\ \L\.\_\ \ \//\ \L\ \  
      \/\____/\ \____\ \____/\ \_\\\\ \____\\\\ \_,__/\ \____/\ \__/.\_\\\\ \_\\\\ \___,_\ 
       \/___/  \/____/\/___/  \/_/ \/____/ \/___/  \/___/  \/__/\/_/ \/_/ \/__,_ / 
    '''

    print ""
    print _scoreboard_string
    print ""
    print ""

    for key in self.scoreboard:
      print "               ", self.platform_names[key], ":", self.scoreboard[key]

    self.visualize_scoreboard()

  ## Visualizes the scoreboard in the scene in form of stacked boxes.
  def visualize_scoreboard(self):
    self.scoreboard_visualization_node.Children.value = []

    _loader = avango.gua.nodes.GeometryLoader()

    _keyID = 0

    for key in self.scoreboard:
      for i in range(0, self.scoreboard[key]):
        _point_box = _loader.create_geometry_from_file( 'score_geometry', 
                                                        'data/objects/cube.obj', 
                                                        'data/materials/' + self.platform_materials[key] + '.gmd', 
                                                        avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY)
        _point_box.Transform.value = avango.gua.make_trans_mat(_keyID * 1.0, i * 0.2 + 0.2, 0.0) * \
                                     avango.gua.make_scale_mat(0.2, 0.2, 0.2)
        self.NET_TRANS_NODE.distribute_object(_point_box)
        self.scoreboard_visualization_node.Children.value.append(_point_box)
      _keyID += 1

  ## Displays the first treasures for the TreasureHunt game.
  # @param LOADER The geometry loader to be used.
  # @param PARENT_NODE Scenegraph node to which the scene should be appended.
  def display_treasures(self, LOADER, PARENT_NODE):
    
    ## @var treasure_node
    # Scenegraph node collecting all the treasure geometry nodes.
    self.treasure_node = avango.gua.nodes.TransformNode(Name = 'treasure_node')
    PARENT_NODE.Children.value.append(self.treasure_node)

    ## @var scoreboard_visualization
    # Scenegraph node on which all "point boxes" will be appended to.
    self.scoreboard_visualization_node = avango.gua.nodes.TransformNode(Name = 'scoreboard_visualization_node')
    self.scoreboard_visualization_node.Transform.value = avango.gua.make_trans_mat(-13.0, 0.0, 23.0)
    PARENT_NODE.Children.value.append(self.scoreboard_visualization_node)

    ## @var treasure_list
    # List collecting all possible treasures in the scene.
    self.treasure_list = []

    ## @var treasure_light_list
    # List collecting all lights coming with the treasures in the scene.
    self.treasure_light_list = []

    ## @var visible_treasures
    # Number of treasures visible to the hunters.
    self.visible_treasures = 6

    # choose visible_treasures treasures from the list to display
    _chosen_treasure_ids = random.sample(range(0, len(self.treasure_positions)),  self.visible_treasures)

    # create treasure nodes and toggle their visibilities
    for i in range(0, len(self.treasure_positions)):
      _treasure = LOADER.create_geometry_from_file( 'treasure_geometry_' + str(i), 
                                                    'data/objects/chest.obj', 
                                                    'data/materials/AvatarGreen.gmd',
                                                    avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY | avango.gua.LoaderFlags.LOAD_MATERIALS)
      _treasure.Transform.value = self.treasure_positions[i] * \
                                  avango.gua.make_trans_mat(0, -1.3, 0) * \
                                  avango.gua.make_scale_mat(0.3, 0.3, 0.3)
      _light = avango.gua.nodes.SpotLightNode( Name = "treasure_light_" + str(i),
                                              Color = avango.gua.Color(1.0, 0.8, 0.2),
                                              EnableShadows = False,
                                              EnableGodrays = True)
      _light.Transform.value = self.treasure_positions[i] * \
                               avango.gua.make_trans_mat(0, -1.0, 0) * \
                               avango.gua.make_rot_mat(110, 1, 0, 0) * \
                               avango.gua.make_scale_mat(1, 1, 1)

      self.treasure_node.Children.value.append(_light)
      self.treasure_node.Children.value.append(_treasure)
      self.treasure_list.append(_treasure)
      self.treasure_light_list.append(_light)

      if i in _chosen_treasure_ids:
        _treasure.GroupNames.value = ['display_group']
        _light.GroupNames.value = ['display_group', 'server_do_not_display_group']
      else:
        _treasure.GroupNames.value = ['do_not_display_group']
        _light.GroupNames.value = ['do_not_display_group', 'server_do_not_display_group']


  ## Removes a given treasure and displays another one, randomly chosen, instead.
  # @param TREASURE_TO_REMOVE The treasure node to be removed.
  def update_treasure_display(self, TREASURE_TO_REMOVE):

    if TREASURE_TO_REMOVE.GroupNames.value[0] == "display_group":

      _visible_treasures = self.determine_visible_treasures()
       
      while _visible_treasures < self.visible_treasures:
        # get a new treasure id to display
        _new_treasure_id = random.randint(0, len(self.treasure_list) - 1)

        # get another number if the treasure is already visible or if it is the old one to be removed
        while self.treasure_list[_new_treasure_id].GroupNames.value[0] == ['display_group'] and self.treasure_list[_new_treasure_id] != TREASURE_TO_REMOVE:
          _new_treasure_id = random.randint(0, len(self.treasure_list) - 1)

        self.treasure_list[_new_treasure_id].GroupNames.value = ['display_group']
        self.treasure_light_list[_new_treasure_id].GroupNames.value[0] = 'display_group'

        _visible_treasures = self.determine_visible_treasures()

      self.frames_since_last_score = 0
      TREASURE_TO_REMOVE.GroupNames.value = ["do_not_display_group"]
      _corresponding_light = self.treasure_light_list[self.treasure_list.index(TREASURE_TO_REMOVE)]
      _corresponding_light.GroupNames.value[0] = "do_not_display_group"

  ## Computes the number of currently visible treasures. To be kept at self.visible_treasures
  def determine_visible_treasures(self):
    _visible_treasures = 0

    for i in range(0, len(self.treasure_list)):
       if self.treasure_list[i].GroupNames.value[0] == 'display_group':
        _visible_treasures += 1

    return _visible_treasures
