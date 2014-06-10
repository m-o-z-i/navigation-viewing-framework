#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango

# import framework libraries
from Objects import *

# import python libraries
# ...


class SceneVRHyperspace1(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace1", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-60.0, 5.5, 4.5)
    self.init_geometry("steppo", "data/objects/avatars_obj/shot_steppo_animation_010000000001.obj", _mat, None, False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    # lights    
    _mat = avango.gua.make_trans_mat(-59.0, 7.75, 5.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(1.0, 0.25, 0.25), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-50.0, 7.75, 5.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(1.0, 1.0, 0.0), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.75, 0.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.0, 1.0, 1.0), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-50.0, 7.75, 0.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(1.0, 1.0, 1.0), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-50.0, 7.75, 0.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(1.0, 0.0, 1.0), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-50.0, 7.75, 0.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.3, 0.7), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE


class Passat(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Passat", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    _mat = avango.gua.make_trans_mat(-1.99, 0.0, -3) * \
           avango.gua.make_rot_mat(-90.0,1,0,0) * \
           avango.gua.make_rot_mat(90.0,0,0,1) * \
           avango.gua.make_scale_mat(0.04)
    self.init_geometry("passat", "data/objects/passat/passat.obj", _mat, None, True, True, self.scene_root) 


class SceneVRHyperspace2(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace2", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _tile_scale = 2.0
    _tile_height = -150.0
    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(0, "sun_light", avango.gua.Color(1.0, 0.7, 0.5), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(-59.0, 7.6, 5.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(1.0, 0.25, 0.25), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-50.0, 7.6, 5.0) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.0, 1.0, 0.0), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE


class SceneVRHyperspace3(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace3", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_outer_rest", "data/objects/vr_hyperspace/bwb/outer_rest.obj", _mat, "data/materials/bwb/Aircraft.gmd", False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_outer_med", "data/objects/vr_hyperspace/bwb/outer_med.obj", _mat, "data/materials/bwb/Aircraft.gmd", False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_outer_dark", "data/objects/vr_hyperspace/bwb/outer_dark.obj", _mat, "data/materials/bwb/AircraftDark.gmd", False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_outer_bright", "data/objects/vr_hyperspace/bwb/outer_bright.obj", _mat, "data/materials/bwb/AircraftBright.gmd", False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _tile_scale = 2.0
    _tile_height = -150.0
    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(0, "sun_light", avango.gua.Color(1.0, 0.7, 0.5), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
    


class MedievalTown(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "MedievalTown", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    self.ssao_radius = 100.0

    # geometry
    _mat = avango.gua.make_scale_mat(7.5)
    self.init_geometry("town", "data/objects/medieval_harbour/town.obj", _mat, None, True, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(0, -3.15, 0) * avango.gua.make_scale_mat(1500.0, 1.0, 1500.0)
    self.init_geometry("water", "data/objects/plane.obj", _mat, 'data/materials/Water.gmd', True, False, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
  
    #self.water_updater = TimedMaterialUniformUpdate()
    #self.water_updater.MaterialName.value = "data/materials/Water.gmd"
    #self.water_updater.UniformName.value = "time"
    #self.water_updater.TimeIn.connect_from(self.timer.Time)

    _mat = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    #self.init_geometry("steppo", "data/objects/avatars_obj/shot_steppo_animation_010000000001.obj", _mat, None, False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(0, "sun_light", avango.gua.Color(1.0, 0.7, 0.5), _mat, self.scene_root) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE


    '''
    # create ship
    self.ship_transform = avango.gua.nodes.TransformNode(Name = 'ship_transform')
    self.ship_transform.Transform.value = avango.gua.make_trans_mat(0, 2.2, 33) * avango.gua.make_scale_mat(7, 7, 7)
    self.ship = _loader.create_geometry_from_file( 'ship_geometry', 
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
    self.plank = _loader.create_geometry_from_file( 'plank_geometry',
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
    '''
    
