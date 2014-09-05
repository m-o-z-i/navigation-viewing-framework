#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Objects import *

# import python libraries
# ...


class TimedObjectRotation(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in milliseconds.
  TimeIn = avango.SFFloat()

  MatrixIn = avango.gua.SFMatrix4()
  MatrixOut = avango.gua.SFMatrix4()

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    self.MatrixOut.value = self.MatrixIn.value * avango.gua.make_rot_mat(self.TimeIn.value * 6.0, 0.0, 1.0, 0.0)



class SceneVRHyperspace0(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace0", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.0,5.5,-5.7) * avango.gua.make_rot_mat(135.0,0,-1,0)
    self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner_barless.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_geometry("bwb_inner_windows", "data/objects/demo_models/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0) * avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    #self.enable_ssao = True
    self.enable_ffxa = True
    #self.background_texture = "/opt/guacamole/resources/skymaps/bright_sky.jpg"
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)



class SceneVRHyperspace1(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace1", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.0,5.5,-5.7) * avango.gua.make_rot_mat(135.0,0,-1,0)
    self.starting_scale = 1.0

    # navigation texture
    self.tex_quad = avango.gua.nodes.TexturedQuadNode(
          Name = "navigation_map"
        , Texture = "data/textures/bwb/place-ticket-here-1.png"
        , Width = 0.85
        , Height = 1.7
    )
    self.tex_quad.Transform.value = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-63.8, 6.6, 1.3) * avango.gua.make_rot_mat(180, 0, 1, 0)
    self.scene_root.Children.value.append(self.tex_quad)

    # navigation light
    _mat = avango.gua.make_trans_mat(-70.95, 7.48, 0.55)
    self.init_group("nav_light_group", _mat, False, False, self.scene_root, "main_scene")

    _parent_object = self.get_object("nav_light_group")

    _mat = avango.gua.make_trans_mat(64.53, -6.705, -0.48)
    self.init_geometry("light_geometry", "data/objects/nav/01.obj", _mat, None, False, False, _parent_object, "main_scene")
    _mat = avango.gua.make_rot_mat(-90, 1, 0, 0)
    self.init_light(TYPE = 2, NAME = "light", COLOR = avango.gua.Color(1.0, 1.0, 3.0), MATRIX = _mat, PARENT_NODE = _parent_object, LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False)

    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner_barless.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_geometry("bwb_inner_windows", "data/objects/demo_models/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0) * avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-65.355, 6.95, -6.310)
    self.init_light(TYPE = 1, NAME = "map_light", COLOR = avango.gua.Color(1.5, 1.5, 1.5), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(1.0,1.0,1.0), ENABLE_SPECULAR_SHADING = False, MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    #self.enable_ssao = True
    self.enable_ffxa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)



class SceneVRHyperspace2(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace2", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.406, 5.424, 8.033) * avango.gua.make_rot_mat(90.0,0,1,0)
    self.starting_scale = 1.0


    # seat emergeny exit map texture
    self.tex_quad = avango.gua.nodes.TexturedQuadNode(
          Name = "emergency_exit_map"
        , Texture = "data/textures/tiles_diffuse.jpg"
        , Width = 0.42
        , Height = 0.21
    )
    self.tex_quad.Transform.value = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-50.668, 6.456, 6.74) * avango.gua.make_rot_mat(90, 0, 1, 0) * avango.gua.make_rot_mat(12, 1, 0, 0)
    self.scene_root.Children.value.append(self.tex_quad)


    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_geometry("bwb_inner_windows", "data/objects/demo_models/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0) * avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    '''
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.156, 5.499, 0.215) * avango.gua.make_rot_mat(90.0,0,-1,0)
    self.init_geometry("barman", "data/objects/demo_models/avatars_obj/shot_steppo_animation_010000000001.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-52.5, 5.35, 7.4) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("flight_instruction2", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-52.5, 5.35, 4.75) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("flight_instruction2", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 5.35, 8.5) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("flight_instruction3", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 5.35, 5.85) * avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_geometry("flight_instruction4", "/opt/3d_models/Avatars/smooth/VR_Hyperspace_pose_steward_010000000000.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    '''


    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_ffxa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)


class SceneVRHyperspace3(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace3", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.406, 5.424, 8.033) * avango.gua.make_rot_mat(90.0,0,1,0)
    self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/demo_models/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0) * avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_rot_mat(90.0, 1, 0, 0) * avango.gua.make_scale_mat(7.0)
    _parent_node = SCENEGRAPH["/net/platform_0/scale/screen_0"]
    self.init_geometry("clouds", "data/objects/plane.obj", _mat, "data/materials/bwb/Fog.gmd", False, False, _parent_node, "pre_scene1")


    _mat = avango.gua.make_identity_mat()
    self.init_group("terrain_group", _mat, False, False, self.scene_root, "pre_scene2")

    _parent_object = self.get_object("terrain_group")

    _tile_scale = 2.0
    _tile_height = -150.0

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile4", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile5", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile6", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile7", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile8", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile9", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile10", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile11", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile12", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile13", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile14", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile15", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile16", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0),  MANIPULATION_PICK_FLAG = True, ENABLE_LIGHT_GEOMETRY = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-148, 0, 1, 0) * avango.gua.make_rot_mat(-15.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "mountain_sun", COLOR = avango.gua.Color(1.1, 1.1, 1.1), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "pre_scene2", ENABLE_SHADOW = True) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    #self.enable_ssao = True
    self.enable_fxaa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)
    #self.background_texture = "pre_scene1_texture"


class SceneVRHyperspace4(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace4", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    self.timer = avango.nodes.TimeSensor()

    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-57.937, 5.563, 7.599) * avango.gua.make_rot_mat(135.0,0,1,0)
    self.starting_scale = 1.0

    # advertisement geometry
    _mat = avango.gua.make_trans_mat(0.0, 0.0, -102.0)
    self.init_geometry("ad_object_1", "data/objects/ads/tours-object.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.ad1_updater = TimedObjectRotation()
    self.ad1_updater.TimeIn.connect_from(self.timer.Time)
    self.ad1_updater.MatrixIn.value = avango.gua.make_trans_mat(0.0, -0.65, -100.3) * avango.gua.make_scale_mat(1.2)
    SCENEGRAPH["/net/SceneVRHyperspace4/ad_object_1"].Transform.connect_from(self.ad1_updater.MatrixOut)
    _mat = avango.gua.make_trans_mat(0.0, -0.55, -100.1) * avango.gua.make_rot_mat(180, 0, 1, 0)
    self.init_geometry("ad_text_1", "data/objects/ads/tours-text.obj", _mat, None, False, False, self.scene_root, "main_scene")


    _mat = avango.gua.make_trans_mat(10.0, -0.4, -102.0)
    self.init_geometry("ad_object_2", "data/objects/ads/shop-object.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.ad2_updater = TimedObjectRotation()
    self.ad2_updater.TimeIn.connect_from(self.timer.Time)
    self.ad2_updater.MatrixIn.value = avango.gua.make_trans_mat(10.0, -0.65, -100.3)  * avango.gua.make_scale_mat(1.2)
    SCENEGRAPH["/net/SceneVRHyperspace4/ad_object_2"].Transform.connect_from(self.ad2_updater.MatrixOut)
    _mat = avango.gua.make_trans_mat(10.0, -0.55, -100.1) * avango.gua.make_rot_mat(180, 0, 1, 0)
    self.init_geometry("ad_text_2", "data/objects/ads/shop-text.obj", _mat, None, False, False, self.scene_root, "main_scene")

    _tex_quad1 = avango.gua.nodes.TexturedQuadNode(
          Name = "tex_ad_1"
        , Texture = "data/textures/bwb/advert-1.png"
        , Width = 0.85
        , Height = 1.7
    )
    _tex_quad1.Transform.value = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-63.79, 6.62, -0.95)
    self.scene_root.Children.value.append(_tex_quad1)

    _tex_quad2 = avango.gua.nodes.TexturedQuadNode(
          Name = "tex_ad_2"
        , Texture = "data/textures/bwb/advert-2.png"
        , Width = 0.85
        , Height = 1.7
    )
    _tex_quad2.Transform.value = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-58.34, 6.62, -0.95)
    self.scene_root.Children.value.append(_tex_quad2)

    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner_windows", "data/objects/demo_models/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/Glass2.gmd", False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0) * avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_rot_mat(90.0, 1, 0, 0) * avango.gua.make_scale_mat(5.0)
    _parent_node = SCENEGRAPH["/net/platform_0/scale/screen_0"]
    self.init_geometry("clouds", "data/objects/plane.obj", _mat, "data/materials/bwb/Fog.gmd", False, False, _parent_node, "pre_scene1")


    _mat = avango.gua.make_identity_mat()
    self.init_group("terrain_group", _mat, False, False, self.scene_root, "pre_scene2")

    _parent_object = self.get_object("terrain_group")

    _tile_scale = 2.0
    _tile_height = -150.0

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile1", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile2", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile3", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 0) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile4", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile5", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile6", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile7", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile8", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile9", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile10", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile11", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * 2) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile12", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * 0, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile13", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -1, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile14", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -2, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile15", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(204.7 * _tile_scale * -3, _tile_height, 204.7 * _tile_scale * -1) * avango.gua.make_scale_mat(_tile_scale)
    self.init_geometry("terrain_tile16", "data/objects/demo_models/vr_hyperspace/terrain/lod0.obj", _mat, None, False, False, _parent_object, "pre_scene2") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-148, 0, 1, 0) * avango.gua.make_rot_mat(-15.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "mountain_sun", COLOR = avango.gua.Color(1.1, 1.1, 1.1), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "pre_scene2", ENABLE_SHADOW = True) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    #self.enable_ssao = True
    self.enable_fxaa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)
    self.background_texture = "pre_scene1_texture"


class SceneVRHyperspace5(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace5", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-57.937, 5.563, 7.599) * avango.gua.make_rot_mat(135.0,0,1,0)
    self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_identity_mat()
    self.init_geometry("office", "data/objects/demo_models/vr_hyperspace/bwb/office3.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-60.8, 5.5, 9.5)# * avango.gua.make_scale_mat(0.95)
    self.init_kinect("office_call", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")

    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.239, 7.322, 20.381)
    self.init_light(TYPE = 1, NAME = "office_light1", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 31.481)
    self.init_light(TYPE = 1, NAME = "office_light2", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 14.103)
    self.init_light(TYPE = 1, NAME = "office_light3", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-58.700, 7.469, 18.703)
    self.init_light(TYPE = 1, NAME = "office_light4", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.239, 7.322, 10.381)
    self.init_light(TYPE = 1, NAME = "office_light5", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 5.481)
    self.init_light(TYPE = 1, NAME = "office_light6", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 35.103)
    self.init_light(TYPE = 1, NAME = "office_light7", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-58.700, 7.469, 40.703)
    self.init_light(TYPE = 1, NAME = "office_light8", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = False
    self.enable_ssao = False
    self.enable_fxaa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)
    self.background_texture = "/opt/guacamole/resources/skymaps/DH211SN.png"



class SceneVRHyperspace6(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace6", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-57.937, 5.563, 7.599) * avango.gua.make_rot_mat(135.0,0,1,0)
    self.starting_scale = 1.0

    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("office", "data/objects/demo_models/vr_hyperspace/bwb/office3.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.8, 0.25, 0.0)
    self.init_geometry("office_barchart", "data/objects/demo_models/vr_hyperspace/props/chart.obj", _mat, None, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-60.8, 5.5, 9.5)# * avango.gua.make_scale_mat(0.95)
    self.init_kinect("office_call", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")


    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.239, 7.322, 20.381)
    self.init_light(TYPE = 1, NAME = "office_light1", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 31.481)
    self.init_light(TYPE = 1, NAME = "office_light2", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 14.103)
    self.init_light(TYPE = 1, NAME = "office_light3", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-58.700, 7.469, 18.703)
    self.init_light(TYPE = 1, NAME = "office_light4", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.239, 7.322, 10.381)
    self.init_light(TYPE = 1, NAME = "office_light5", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 5.481)
    self.init_light(TYPE = 1, NAME = "office_light6", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-67.000, 7.369, 35.103)
    self.init_light(TYPE = 1, NAME = "office_light7", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-58.700, 7.469, 40.703)
    self.init_light(TYPE = 1, NAME = "office_light8", COLOR = avango.gua.Color(0.8, 0.8, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = False
    self.enable_ssao = False
    self.enable_fxaa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)
    self.background_texture = "/opt/guacamole/resources/skymaps/DH211SN.png"



class SceneVRHyperspace7(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVRHyperspace7", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor


    # navigation parameters
    self.starting_matrix = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-51.588, 5.805, 5.198) * avango.gua.make_rot_mat(90.0,0,1,0)
    self.starting_scale = 1.0

    #'''
    # geometry
    _mat = avango.gua.make_scale_mat(1.1)
    self.init_geometry("bwb_inner", "data/objects/demo_models/vr_hyperspace/bwb/inner.obj", _mat, None, True, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_windows", "data/objects/demo_models/vr_hyperspace/bwb/inner_windows.obj", _mat, "data/materials/bwb/White.gmd", False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_roof", "data/objects/demo_models/vr_hyperspace/bwb/roof.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0)
    self.init_geometry("bwb_inner_left_seats_base_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3sitze-einzeln.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_backrest_extra", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/3-aussenschalen.obj", _mat, None, False, False, self.scene_root, "main_scene")
    self.init_geometry("bwb_inner_left_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_left_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(0.0, 0.15, 0.0) * avango.gua.make_scale_mat(1.0,1.0,-1.0)
    self.init_geometry("bwb_inner_right_seats_base", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/Komplett-sitze-singled_plus_16.obj", _mat, None, False, False, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("bwb_inner_right_seats_backrest", "data/objects/demo_models/vr_hyperspace/komplett_links_1er_2er_3er/aussenschale.obj", _mat, None, False, False, self.scene_root, "main_scene")

    _mat = avango.gua.make_trans_mat(-54.8, 5.419, 5.0) * avango.gua.make_rot_mat(90.0,0,-1,0)
    self.init_kinect("home_call", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")
    #self.init_kinect("home_call", "/opt/kinect-resources/shot_steppo_animation_01.ks", _mat, self.scene_root, "main_scene")

    '''
    _mat = avango.gua.make_trans_mat(-54.8, 5.419, 3.0) * avango.gua.make_rot_mat(90.0,0,-1,0)
    self.init_kinect("home_call2", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")

    _mat = avango.gua.make_trans_mat(-54.8, 5.419, 7.0) * avango.gua.make_rot_mat(90.0,0,-1,0)
    self.init_kinect("home_call3", "/opt/kinect-resources/kinect_surfaceLCD.ks", _mat, self.scene_root, "main_scene")
    '''

    # lights
    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, 5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light1", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, 6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light2", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-59.0, 7.74, -5.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light3", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-49.0, 7.74, -6.5)
    self.init_light(TYPE = 1, NAME = "ceiling_light4", COLOR = avango.gua.Color(0.6, 0.6, 0.7), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(7.0,7.0,7.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, 3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light5", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-64.412, 7.819, -3.626)
    self.init_light(TYPE = 1, NAME = "ceiling_light6", COLOR = avango.gua.Color(0.6, 0.8, 0.6), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(5.0,5.0,5.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_trans_mat(-47.647, 6.413, 0.121)
    self.init_light(TYPE = 1, NAME = "toilet_light", COLOR = avango.gua.Color(0.3, 0.3, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(3.0,3.0,3.0)) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light1", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-225.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light2", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light

    _mat = avango.gua.make_scale_mat(1.1) * avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 0, NAME = "directional_light3", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, RENDER_GROUP = "main_scene", ENABLE_SPECULAR_SHADING = False) # TYPE: 0 = sun light; 1 = point light; 2 = spot light


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_fxaa = True
    #self.ambient_color = avango.gua.Vec3(0.25,0.25,0.25)
    #self.background_texture = "/opt/guacamole/resources/skymaps/DH211SN.png"


