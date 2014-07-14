#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango

# import framework libraries
from Objects import *

# import python libraries
# ...


class Passat(SceneObject):

  # dummy testing scene with just the passat object

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Passat", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    _mat = avango.gua.make_trans_mat(-1.99, 0.0, -3) * \
           avango.gua.make_rot_mat(-90.0,1,0,0) * \
           avango.gua.make_rot_mat(90.0,0,0,1) * \
           avango.gua.make_scale_mat(0.04)
    self.init_geometry("passat", "data/objects/passat/passat.obj", _mat, None, True, True, self.scene_root) 

    self.background_texture = "data/textures/skymap.png"


class SceneMedievalTown(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "MedievalTown", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 3.0, 22.0)
    self.starting_scale = 1.0


    # geometry
    _mat = avango.gua.make_scale_mat(7.5)
    self.init_geometry("town", "data/objects/demo_models/medieval_harbour/town.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(0, -3.15, 0) * avango.gua.make_scale_mat(1500.0, 1.0, 1500.0)
    self.init_geometry("water", "data/objects/plane.obj", _mat, 'data/materials/Water.gmd', True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG,
  
    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 20.0)
    #self.init_kinect("kinect1", "/opt/kinect-resources/shot_steppo_animation_distributed_daedalos.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE    
    #self.init_kinect("kinect1", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE
      
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_fxaa = True


class ScenePitoti(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "ScenePitotiTest", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    #self.starting_matrix = avango.gua.make_trans_mat(0.092, 4.922, 22.049)
    #self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_point_cloud("spacemonkey", "/mnt/pitoti/KDN_LOD/PITOTI_KDN_LOD/Spacemonkey_new.kdn", _mat, self.scene_root, "main_scene")
          
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE


class SceneViandenHigh(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneViandenHigh", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(72.730, -5.571, -51.930)
    self.starting_scale = 1.0    

    # geometry
    _mat = avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("vianden_out", "data/objects/demo_models/Arctron/Vianden/Aussen_gesamt/VIANDEN.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("vianden_in", "data/objects/demo_models/Arctron/Vianden/Innen_gesamt/Innenraeume_Gesamt.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
          
    # lights
    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.75, 0.75, 0.75), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False, SHADOW_MAP_SIZE = 256, ENABLE_GODRAYS = False) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(50.0, 100.0, -50.0) * \
           avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 2, 
                    NAME = "spot_light", 
                    COLOR = avango.gua.Color(1.0, 1.0, 1.0), 
                    MATRIX = _mat, 
                    PARENT_NODE = self.scene_root, 
                    MANIPULATION_PICK_FLAG = True, 
                    ENABLE_SHADOW = True, 
                    LIGHT_DIMENSIONS = avango.gua.Vec3(600.0,600.0,200.0), 
                    FALLOFF = 0.009, 
                    SOFTNESS = 0.003, 
                    SHADOW_MAP_SIZE = 2048)

    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = True
    self.enable_fxaa = True
    self.enable_fog = False
    self.ambient_color = avango.gua.Color(0.5, 0.5, 0.5)
    #self.background_texture = "/opt/guacamole/resources/skymaps/DH221SN.png"
    self.background_texture = "/opt/guacamole/resources/skymaps/cycles_island2.jpg"

class SceneViandenLow(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneViandenLow", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(72.730, -5.571, -51.930)
    self.starting_scale = 1.0    

    # geometry
    _mat = avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("vianden_out", "data/objects/demo_models/Arctron/Vianden/Aussen_gesamt/VIANDEN.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
          
    # lights
    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.75, 0.75, 0.75), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False, SHADOW_MAP_SIZE = 256, ENABLE_GODRAYS = False) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(50.0, 100.0, -50.0) * \
           avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 2, 
                    NAME = "spot_light", 
                    COLOR = avango.gua.Color(1.0, 1.0, 1.0), 
                    MATRIX = _mat, 
                    PARENT_NODE = self.scene_root, 
                    MANIPULATION_PICK_FLAG = True, 
                    ENABLE_SHADOW = False, 
                    LIGHT_DIMENSIONS = avango.gua.Vec3(600.0,600.0,200.0), 
                    FALLOFF = 0.009, 
                    SOFTNESS = 0.003, 
                    SHADOW_MAP_SIZE = 1024)

    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_fxaa = True
    self.enable_fog = False
    self.ambient_color = avango.gua.Color(0.5, 0.5, 0.5)
    #self.background_texture = "/opt/guacamole/resources/skymaps/DH221SN.png"
    self.background_texture = "/opt/guacamole/resources/skymaps/cycles_island2.jpg"

 
class SceneMonkey(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Monkey", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 1.0)

    _mat = avango.gua.make_identity_mat()
    self.init_group("group", _mat, False, True, self.scene_root, "main_scene")

    _parent_object = self.get_object("group")

    _mat = avango.gua.make_trans_mat(0.0,1.2,0.0) * avango.gua.make_scale_mat(0.1)
    self.init_geometry("monkey1", "data/objects/monkey.obj", _mat, "data/materials/SimplePhongWhite.gmd", False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, RENDER_GROUP

    _mat = avango.gua.make_trans_mat(-0.25,1.2,0.0) * avango.gua.make_scale_mat(0.05)
    self.init_geometry("monkey2", "data/objects/monkey.obj", _mat, "data/materials/AvatarBlue.gmd", False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.25,1.2,0.0) * avango.gua.make_scale_mat(0.05)
    self.init_geometry("monkey3", "data/objects/monkey.obj", _mat, "data/materials/AvatarBlue.gmd", False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.0, 1.0, 0.0) * avango.gua.make_scale_mat(2.0)
    self.init_geometry("plane", "data/objects/plane.obj", _mat, 'data/materials/ComplexPhongTiles.gmd', False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
  
    
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True, RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-0.3, 1.4, 0.0)
    self.init_light(TYPE = 1, NAME = "point_light", COLOR = avango.gua.Color(0.0, 1.0, 0.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 0.25, 0.25), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = True, LIGHT_DIMENSIONS = avango.gua.Vec3(2.0,2.0,1.0)) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE



class ScenePLOD(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "PLOD", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 1.0)

    _mat = avango.gua.make_trans_mat(0.0,1.2,0.0) * avango.gua.make_scale_mat(0.25)
    self.init_plod("pig", "/opt/3d_models/point_based/plod/pig.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    #_mat = avango.gua.make_trans_mat(1.0,2.5,0.0) * avango.gua.make_scale_mat(3.0)
    #self.init_plod("pitoti", "/mnt/pitoti/KDN_LOD/PITOTI_KDN_LOD/Spacemonkey_new.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    

    #_mat = avango.gua.make_trans_mat(1.0,2.5,0.0) * avango.gua.make_scale_mat(3.0)
    #self.init_plod("pitoti", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area_4_hunter_with_bow.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    

    #_mat = avango.gua.make_identity_mat()
    #self.init_plod("pitoti", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/TLS_Seradina_Rock-12C.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    

    _mat = avango.gua.make_trans_mat(0.0, 1.0, 0.0) * avango.gua.make_scale_mat(3.0)
    self.init_geometry("plane", "data/objects/plane.obj", _mat, 'data/materials/ComplexPhongTiles.gmd', False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
  
    _mat = avango.gua.make_trans_mat(-1.1,1.3,0.0) * avango.gua.make_scale_mat(0.25)
    self.init_geometry("monkey2", "data/objects/monkey.obj", _mat, "data/materials/AvatarBlue.gmd", False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    # lights
    _mat = avango.gua.make_trans_mat(0.0, 1.55, 0.0)
    self.init_light(TYPE = 1, NAME = "point_light", COLOR = avango.gua.Color(0.0, 1.0, 0.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0)) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    #_mat = avango.gua.make_trans_mat(0.0, 1.55, 0.0)
    #self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 0.25, 0.25), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = True, LIGHT_DIMENSIONS = avango.gua.Vec3(2.0,2.0,1.0), RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
      

class SceneWeimar(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Weimar", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    self.starting_matrix = avango.gua.make_trans_mat(42.0, 0.1, -5.8)
    self.enable_ssao = True
    self.ssao_radius = 2.0
    self.ssao_intensity = 2.0
    self.enable_fog = False
    self.ambient_color.value = avango.gua.Color(0.0, 0.0, 0.0)
    #self.ambient_color.value = avango.gua.Color(1.0, 0.0, 0.0)
    self.far_clip = 2000.0

    self.background_texture = "data/textures/bright_sky.jpg"

    _mat = avango.gua.make_scale_mat(0.5)
    #self.init_geometry("weimar", "data/objects/demo_models/weimar_stadtmodell_29.08.12/weimar_stadtmodell_final.obj", _mat, "data/materials/SimplePhongWhite.gmd", True, False, self.scene_root, "main_scene")
    self.init_geometry("weimar", "data/objects/demo_models/weimar_stadtmodell_29.08.12/weimar_stadtmodell_final.obj", _mat, None, True, False, self.scene_root, "main_scene")

    _mat = avango.gua.make_trans_mat(0.0, 200.0, 60.0) * \
           avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 1.0, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = False, LIGHT_DIMENSIONS = avango.gua.Vec3(1000.0,1000.0,300.0), FALLOFF = 0.009, SOFTNESS = 0.003, SHADOW_MAP_SIZE = 2048, ENABLE_SPECULAR_SHADING = True)

    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True, SHADOW_MAP_SIZE = 2048) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
    
    
