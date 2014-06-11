#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango

# import framework libraries
from Objects import *

# import python libraries
# ...


class SceneVRHyperspace0(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace0", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner_barless.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    '''
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    '''

    # lights   
    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE
        

    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
   

class SceneVRHyperspace1(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace1", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner_barless.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.0,-0.15,0.0)
    self.init_geometry("bwb_map", "data/objects/vr_hyperspace/props/map.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    # lights   
    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(-65.355, 6.95, -6.310) * avango.gua.make_scale_mat(1.0)
    self.init_light(5, "map", avango.gua.Color(1.5, 1.5, 1.5), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
   
    _mat = avango.gua.make_trans_mat(-64.300, 7.673, 0.87) * avango.gua.make_scale_mat(2.5)
    self.init_light(1, "guiding_light1", avango.gua.Color(0.9, 0.9, 0.1), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.104, 7.673, 0.87) * avango.gua.make_scale_mat(2.5)
    self.init_light(1, "guiding_light2", avango.gua.Color(0.9, 0.9, 0.1), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-55.683, 7.673, 0.87) * avango.gua.make_scale_mat(2.5)
    self.init_light(1, "guiding_light3", avango.gua.Color(0.9, 0.9, 0.1), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE


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


class SceneVRHyperspace2(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace2", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    
    _mat = avango.gua.make_trans_mat(-67.156, 5.499, 0.215) * avango.gua.make_rot_mat(90.0,0,-1,0)
    #self.init_kinect("barman", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")
    self.init_geometry("steppo", "data/objects/avatars_obj/shot_steppo_animation_010000000001.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    '''
    _mat = avango.gua.make_trans_mat(-52.5, 5.35, 7.4) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0) * avango.gua.make_scale_mat(0.9)
    self.init_geometry("flight_instruction2", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-52.5, 5.35, 4.75) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0) * avango.gua.make_scale_mat(0.9)
    self.init_geometry("flight_instruction2", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 5.35, 8.5) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0) * avango.gua.make_scale_mat(0.9)
    self.init_geometry("flight_instruction3", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 5.35, 5.85) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0) * avango.gua.make_scale_mat(0.9)
    self.init_geometry("flight_instruction4", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    '''

    # lights
    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE        
    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE



class SceneVRHyperspace3(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace3", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_rot_mat(90.0, 1, 0, 0) * avango.gua.make_scale_mat(5.0)
    _parent_node = SCENEGRAPH["/net/platform_0/scale/screen_0"]
    self.init_geometry("clouds", "data/objects/plane.obj", _mat, "data/materials/bwb/Fog.gmd", False, False, _parent_node, "pre_scene1")

    
    _mat = avango.gua.make_identity_mat()
    self.init_group("terrain_group", _mat, False, False, self.scene_root, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _tile_scale = 2.0
    _tile_height = -150.0
    _parent_node = SCENEGRAPH["/net/SceneVRHyperspace3/terrain_group"]
    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile4", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile5", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile6", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile7", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile8", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile9", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile10", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile11", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile12", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile13", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile14", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile15", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile16", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    # lights
    _mat = avango.gua.make_rot_mat(-148, 0, 1, 0) * avango.gua.make_rot_mat(-15.0, 1.0, 0.0, 0.0)
    self.init_light(4, "mountain_sun", avango.gua.Color(1.1, 1.1, 1.1), _mat, self.scene_root, "pre_scene2") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE        
    
    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE


class SceneVRHyperspace4(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace4", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

 
    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    #self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(90.0, 1, 0, 0) * avango.gua.make_scale_mat(5.0)
    _parent_node = SCENEGRAPH["/net/platform_0/scale/screen_0"]
    self.init_geometry("clouds", "data/objects/plane.obj", _mat, "data/materials/bwb/Fog.gmd", False, False, _parent_node, "pre_scene1")

    _mat = avango.gua.make_identity_mat()
    self.init_group("terrain_group", _mat, False, False, self.scene_root, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _tile_scale = 2.0
    _tile_height = -150.0
    _parent_node = SCENEGRAPH["/net/SceneVRHyperspace4/terrain_group"]
    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile4", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile5", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile6", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile7", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile8", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile9", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile10", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile11", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile12", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile13", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile14", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile15", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile16", "data/objects/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_node, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    # lights
    _mat = avango.gua.make_rot_mat(-148, 0, 1, 0) * avango.gua.make_rot_mat(-15.0, 1.0, 0.0, 0.0)
    self.init_light(4, "mountain_sun", avango.gua.Color(1.1, 1.1, 1.1), _mat, self.scene_root, "pre_scene2") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE        

    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE


class SceneVRHyperspace5(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace5", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    
    self.init_geometry("office", "data/objects/vr_hyperspace/bwb/office3.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(-60.8, 5.5, 9.4) * avango.gua.make_scale_mat(0.95)
    self.init_kinect("office_call", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")
    

    # lights
    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE        

    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_trans_mat(-64.239, 7.322, 20.381) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light1", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 31.481) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light2", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 14.103) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light3", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-58.700, 7.469, 18.703) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light4", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.239, 7.322, 10.381) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light5", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 5.481) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light6", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 35.103) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light7", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-58.700, 7.469, 40.703) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light8", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE



class SceneVRHyperspace6(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace6", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    
    self.init_geometry("office", "data/objects/vr_hyperspace/bwb/office3.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(0.8, 0.25, 0.0)
    self.init_geometry("office_barchart", "data/objects/vr_hyperspace/props/chart.obj", _mat, None, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(-60.8, 5.5, 9.4) * avango.gua.make_scale_mat(0.95)
    self.init_kinect("office_call", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")


    # lights
    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE        

    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_trans_mat(-64.239, 7.322, 20.381) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light1", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 31.481) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light2", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 14.103) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light3", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-58.700, 7.469, 18.703) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light4", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.239, 7.322, 10.381) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light5", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 5.481) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light6", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-67.000, 7.369, 35.103) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light7", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-58.700, 7.469, 40.703) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "office_light8", avango.gua.Color(0.8, 0.8, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE



class SceneVRHyperspace7(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace7", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_identity_mat()
    self.init_geometry("bwb_inner", "data/objects/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

        
    _mat = avango.gua.make_trans_mat(-54.8, 5.419, 5.0) * avango.gua.make_rot_mat(90.0,0,-1,0)
    self.init_kinect("kinect_lcd_wall", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")
    

    # lights
    _mat = avango.gua.make_trans_mat(-59.0, 7.74, 5.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light1", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, 6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-59.0, 7.74, -5.5  ) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-49.0, 7.74, -6.5) * avango.gua.make_scale_mat(7.0)
    self.init_light(1, "ceiling_light4", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, 3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light5", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-64.412, 7.819, -3.626) * avango.gua.make_scale_mat(5.0)
    self.init_light(1, "ceiling_light6", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE        

    
    _mat = avango.gua.make_trans_mat(-47.647, 6.413, 0.121) * avango.gua.make_scale_mat(3.0)
    self.init_light(1, "toilet", avango.gua.Color(0.3, 0.3, 1.0), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light, 1 = point light, 2 = spot light), NAME, COLOR, MATRIX, PARENT_NODE


    _mat = avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light2", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE
    
    _mat = avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(3, "directional_light3", avango.gua.Color(0.6, 0.6, 0.7), _mat, self.scene_root, "main_scene") # parameters TYPE (3 = directional), NAME, COLOR, MATRIX, PARENT_NODE




class SceneMedievalTown(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "MedievalTown", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # geometry
    _mat = avango.gua.make_scale_mat(7.5)
    self.init_geometry("town", "data/objects/demo_models/medieval_harbour/town.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    #self.init_geometry("town", "data/objects/medieval_harbour/town.obj", _mat, "data/materials/SimplePhongWhite.gmd", True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    #_mat = avango.gua.make_scale_mat(7.5)
    #self.init_geometry("town", "data/objects/demo_models/medieval_harbour/town.obj", _mat, 'data/materials/SimplePhongWhite.gmd', False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    #self.init_geometry("town", "data/objects/demo_models/medieval_harbour/town.obj", _mat, None, False, True, self.scene_root, "") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(0, -3.15, 0) * avango.gua.make_scale_mat(1500.0, 1.0, 1500.0)
    self.init_geometry("water", "data/objects/plane.obj", _mat, 'data/materials/Water.gmd', True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG,
  
    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 20.0)
    #self.init_kinect("kinect1", "/opt/kinect-resources/shot_steppo_animation_01.ks", _mat, self.scene_root) # parameters: NAME, FILENAME, MATRIX, PARENT_NODE
    #self.init_kinect("kinect1", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE
  
    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    #self.init_geometry("steppo", "data/objects/avatars_obj/shot_steppo_animation_010000000001.obj", _mat, None, False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE


 
class SceneVianden(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Vianden", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # geometry
    _mat = avango.gua.make_trans_mat(-47.0,-28.0,-24.0) * avango.gua.make_rot_mat(90.0,-1,0,0)									
    self.init_geometry("Vianden", "/home/kunert/Desktop/guacamole/tabletop/data/objects/Arctron/Vianden/Aussen_gesamt/VIANDEN.obj", _mat, "data/materials/SimplePhongWhite.gmd", True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    #self.init_geometry("steppo", "data/objects/avatars_obj/shot_steppo_animation_010000000001.obj", _mat, None, False, True, self.scene_root) # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
   
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(0, "sun_light", avango.gua.Color(1.0, 0.7, 0.5), _mat, self.scene_root, "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE



class SceneMonkey(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Monkey", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    self.starting_matrix = avango.gua.make_trans_mat(0, 0, 10)

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
    self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 0.25, 0.25), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = True, SHADOW_DIMENSIONS = avango.gua.Vec3(2.0,2.0,1.0)) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
      
