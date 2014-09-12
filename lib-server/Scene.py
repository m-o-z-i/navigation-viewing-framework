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
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0


    # geometry
    _mat = avango.gua.make_scale_mat(0.1)
    self.init_geometry("town", "data/objects/demo_models/medieval_harbour/town.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(0, -0.05, 0) * avango.gua.make_scale_mat(1500.0, 1.0, 1500.0)
    self.init_geometry("water", "data/objects/plane.obj", _mat, 'data/materials/Water.gmd', True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG,
  
    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 20.0)
    #self.init_kinect("kinect1", "/opt/kinect-resources/shot_steppo_animation_distributed_daedalos.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE    
    #self.init_kinect("kinect1", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE
      
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_fxaa = True


class SceneChessBoard1(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "ChessBoard1", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("ChessBoard1", "data/objects/demo_models/chess1/chess.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


class SceneChessBoard2(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "ChessBoard2", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("ChessBoard2", "data/objects/demo_models/chess2/chess.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


class SceneChessBoard3(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "ChessBoard3", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("ChessBoard3", "data/objects/demo_models/chess3/chess.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


class SceneChessBoard4(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "ChessBoard4", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("ChessBoard4", "data/objects/demo_models/chess4/chess.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


class SceneCity(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "City", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("City", "data/objects/demo_models/city/city.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


class SpacemonkeyPitoti(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SpacemonkeyPitoti", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    _matrix = avango.gua.make_identity_mat()
    _list = [-2.233, 0.348, -0.051, 0.003, 0.340, 2.217, 0.279, -0.003, 0.093, 0.268, -2.243, 0.012, 0.000, 0.000, 0.000, 1.000 ]
    counter = 0

    for i in range(0, 4):
        for j in range(0, 4):
            _matrix.set_element(i,j,_list[counter])
            counter+=1


    # geometry
    _mat =  _matrix * avango.gua.make_trans_mat(0.0338275, 0.324057, 0.234019)
    self.init_point_cloud("spacemonkey", "/mnt/SSD/PLOD_Models/Spacemonkey/Spacemonkey_new.kdn", _mat, self.scene_root, "main_scene")

    # lights
    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False ) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

class SeradinaRock(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SeradinaRock", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    #trans:  (-0.064  -0.069  0.066)   rot:  (0.018  0.145  0.772  0.619)   scale:  (0.055  0.055  0.055)
    
    _matrix = avango.gua.make_identity_mat()
    _matrix.set_element(0,0,-0.045)
    _matrix.set_element(0,1,0.013)
    _matrix.set_element(0,2,0.004)
    _matrix.set_element(0,3,-0.018)
    _matrix.set_element(1,0,0.005)
    _matrix.set_element(1,1,0.002)
    _matrix.set_element(1,2,0.046)
    _matrix.set_element(1,3,0.036)
    _matrix.set_element(2,0,0.013)
    _matrix.set_element(2,1,0.045)
    _matrix.set_element(2,2,-0.004)
    _matrix.set_element(2,3,0.038)
    _matrix.set_element(3,0,0.0)
    _matrix.set_element(3,1,0.0)
    _matrix.set_element(3,2,0.0)
    _matrix.set_element(3,3,1.0)


    # geometry
    _mat = _matrix * avango.gua.make_trans_mat(23.0957, -391.458, -56.8221)
    self.init_point_cloud("SeradinaRock", "/mnt/SSD/PLOD_Models/Seradina_Rock/TLS_Seradina_Rock-12C.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti1",  "/mnt/SSD/PLOD_Models/Pitoti/Area-9_Deer.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti2",  "/mnt/SSD/PLOD_Models/Pitoti/Area-12_Horn.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti3",  "/mnt/SSD/PLOD_Models/Pitoti/Area-A_Dagger.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti4",  "/mnt/SSD/PLOD_Models/Pitoti/Area-B_Dagger.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti5",  "/mnt/SSD/PLOD_Models/Pitoti/Area-7_Warrior.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti6",  "/mnt/SSD/PLOD_Models/Pitoti/Area-6_house_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti7",  "/mnt/SSD/PLOD_Models/Pitoti/Area-6_house_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti8",  "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti9",  "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti10", "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P03.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti11", "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P04.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti12", "/mnt/SSD/PLOD_Models/Pitoti/Area-3_Archers_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti13", "/mnt/SSD/PLOD_Models/Pitoti/Area-3_Archers_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti14", "/mnt/SSD/PLOD_Models/Pitoti/Area-7_Rosa-Camuna.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti15", "/mnt/SSD/PLOD_Models/Pitoti/Standing-Rider_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti16", "/mnt/SSD/PLOD_Models/Pitoti/Standing-Rider_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti17", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_Alphabet_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti18", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_Alphabet_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti19", "/mnt/SSD/PLOD_Models/Pitoti/TLS_Naquane-Ossimo-8.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti20", "/mnt/SSD/PLOD_Models/Pitoti/Area_4_hunter_with_bow.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti21", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_SFM_Alphabet_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti22", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_SFM_Alphabet_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti23", "/mnt/SSD/PLOD_Models/Pitoti/Area-13_Superimposition.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti23", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti25", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti26", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P03.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti27", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P04.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti28", "/mnt/SSD/PLOD_Models/Pitoti/Area-10_Hunting_Scene_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti29", "/mnt/SSD/PLOD_Models/Pitoti/Area-10_Hunting_Scene_P02.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti30", "/mnt/SSD/PLOD_Models/Pitoti/Area-10_Hunting_Scene_P03.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti31", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-1.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti32", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-2.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti33", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-3.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti34", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-4.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti35", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-1.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti36", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-2.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti37", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-3.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti38", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-4.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti39", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-1.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti40", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-2.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti41", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-3.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti42", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-4.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti43", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-1.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti44", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-2.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti45", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-3.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti46", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-4.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti47", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-1.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti48", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-2.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti49", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-3.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti50", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-4.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti51", "/mnt/SSD/PLOD_Models/Pitoti/TLS_Foppe-di-Nadro_Rock-24.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti52", "/mnt/SSD/PLOD_Models/Pitoti/Area-5_hunter_with_speer_P01.kdn", _mat, self.scene_root, "main_scene")
    self.init_point_cloud("SeradinaRock_pitoti53", "/mnt/SSD/PLOD_Models/Pitoti/Area-5_hunter_with_speer_P02.kdn", _mat, self.scene_root, "main_scene")
    #self.init_point_cloud("SeradinaRock_pitoti53", "/mnt/SSD/PLOD_Models/Pitoti/Area-Area-15_Sun-shape_Superimposition.kdn", _mat, self.scene_root, "main_scene")
   
   
class SeradinaValley(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SeradinaValley", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_trans_mat(0.0338275, 0.324057, 0.234019) * avango.gua.make_scale_mat(2.64027, 2.64027, 2.64027)

    for i in range(1, 15):
        self.init_point_cloud("SeradinaValley"+str(i), "/mnt/SSD/PLOD_Models/Seradina_Valley/CONVERTED_Seradina_Part_"+str(i)+".kdn", _mat, self.scene_root, "main_scene")



class Streets(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Streets", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    _matrix = avango.gua.make_identity_mat()
    _list = [0.021, 0.008, 0.010, 0.801, -0.005, -0.012, 0.021, -1.021, 0.012, -0.020, -0.009, -0.151, 0.000, 0.000, 0.000, 1.000 ]
    counter = 0

    for i in range(0, 4):
        for j in range(0, 4):
            _matrix.set_element(i,j,_list[counter])
            counter+=1
    #print _matrix
    #(0.021 0.008 0.010 0.801
    # -0.005 -0.012 0.021 -1.021
    # 0.012 -0.020 -0.009 -0.151
    # 0.000 0.000 0.000 1.000)

    # geometry
    _mat = _matrix * avango.gua.make_trans_mat(10075.6, -7419.66, 14.7925)

    for i in range(1, 28):
        self.init_point_cloud("Streets"+str(i), "/mnt/SSD/PLOD_Models/Streets/out_"+str(i)+".kdn", _mat, self.scene_root, "main_scene")

class ScenePitoti(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "ScenePitoti", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_trans_mat(0.0338275, 0.324057, 0.234019) * avango.gua.make_scale_mat(2.64027, 2.64027, 2.64027)
    self.init_point_cloud("ScenePitoti", "/mnt/SSD/PLOD_Models/Streets/out_1.kdn/Area_4_hunter_with_bow.kdn", _mat, self.scene_root, "main_scene")

class SceneVianden(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVianden", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_trans_mat(72.730, -5.571, -51.930)
    self.starting_scale = 1.0    

    # geometry
    _mat = avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("vianden", "data/objects/demo_models/Arctron/Vianden/Aussen_gesamt/VIANDEN.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    

          
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.75, 0.75, 0.75), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True, SHADOW_MAP_SIZE = 256, ENABLE_GODRAYS = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # render pipeline parameters
    self.enable_backface_culling = True
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_fxaa = True
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
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-0.3, 1.4, 0.0)
    self.init_light(TYPE = 1, NAME = "point_light", COLOR = avango.gua.Color(0.0, 1.0, 0.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 0.25, 0.25), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = True, LIGHT_DIMENSIONS = avango.gua.Vec3(2.0,2.0,1.0)) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
      
