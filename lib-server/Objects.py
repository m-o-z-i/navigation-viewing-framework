#!/usr/bin/python

## @file
# Contains classes SceneObject and InteractiveObject.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Visualization import *

## Abstract base class to represent a scene which is a collection of interactive objects.
# Not to be instantiated.
class SceneObject:

  ## Default constructor.
  # @param NAME Name to be given to the scene to be created.
  # @param SCENE_MANAGER Reference to the SceneManager instance which is used.
  # @param SCENEGRAPH Reference to the scenegraph in which the scene is existing.
  # @param NET_TRANS_NODE Reference to the nettrans node to append the scene to.
  def __init__(self, NAME, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):

    # references
    ## @var SCENE_MANAGER
    # Reference to the SceneManager instance which is used.
    self.SCENE_MANAGER = SCENE_MANAGER

    ## @var SCENEGRAPH
    # Reference to the scenegraph in which the scene is existing.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var NET_TRANS_NODE
    # Reference to the nettrans node to append the scene to.
    self.NET_TRANS_NODE = NET_TRANS_NODE

    # variables
    ## @var objects
    # List of InteractiveObject instances that belong to this scene.
    self.objects = []

    ## @var name
    # Name to be given to the scene.
    self.name = NAME

    self.SCENE_MANAGER.scenes.append(self)

    # nodes
    ## @var scene_root
    # Root node of this scene.
    self.scene_root = avango.gua.nodes.TransformNode(Name = self.name)
    NET_TRANS_NODE.Children.value.append(self.scene_root)

    '''
      Pipeline values
    '''

    ## @var background_texture
    # Mapping of pipeline value BackgroundTexture and FoxTexture.
    self.background_texture = "data/textures/sky.jpg"

    ## @var enable_bloom
    # Mapping of pipeline value EnableBloom.
    self.enable_bloom = False

    ## @var bloom_intensity
    # Mapping of pipeline value BloomIntensity.
    self.bloom_intensity = 0.1

    ## @var bloom_threshold
    # Mapping of pipeline value BloomThreshold.
    self.bloom_threshold = 1.0

    ## @var bloom_radius
    # Mapping of pipeline value BloomRadius.
    self.bloom_radius = 10

    ## @var enable_ssao
    # Mapping of pipeline value EnableSsao.
    self.enable_ssao = False

    ## @var ssao_radius
    # Mapping of pipeline value SsaoRadius.
    self.ssao_radius = 2.0

    ## @var ssao_intensity
    # Mapping of pipeline value SsaoIntensity.
    self.ssao_intensity = 2.0

    ## @var enable_backface_culling
    # Mapping of pipeline value EnableBackfaceCulling.
    self.enable_backface_culling = False

    ## @var enable_frustum_culling
    # Mapping of pipeline value EnableFrustumCulling.
    self.enable_frustum_culling = True

    ## @var enable_fxaa
    # Mapping of pipeline value EnableFXAA.
    self.enable_fxaa = True

    ## @var ambient_color
    # Mapping of pipeline value AmbientColor.
    self.ambient_color = avango.gua.Color(0.4, 0.4, 0.4)

    ## @var enable_fog
    # Mapping of pipeline value EnableFog.
    self.enable_fog = True

    ## @var fog_start
    # Mapping of pipeline value FogStart.
    self.fog_start = 300.0

    ## @var fog_end
    # Mapping of pipeline value FogEnd.
    self.fog_end = 500.0

    ## @var near_clip
    # Mapping of pipeline value NearClip.
    self.near_clip = 0.1

    ## @var far_clip
    # Mapping of pipeline value FarClip.
    self.far_clip = 1000.0

  # functions
  ## Returns the SceneManager instance this scene object is belonging to.
  def get_scene_manager(self):
  
    return self.SCENE_MANAGER
    
  ## Returns the scenegraph to which this scene object is belonging to.
  def get_scenegraph(self):
  
    return self.SCENEGRAPH

  ## Returns the net node of the scenegraph.
  def get_net_trans_node(self):
  
    return self.NET_TRANS_NODE   

  ## Returns a string of all concatenated pipeline values for this SceneObject.
  def get_pipeline_value_string(self):
    return self.background_texture + "#" + \
           str(self.enable_bloom) + "#" + \
           str(self.bloom_intensity) + "#" + \
           str(self.bloom_threshold) + "#" + \
           str(self.bloom_radius) + "#" + \
           str(self.enable_ssao) + "#" + \
           str(self.ssao_radius) + "#" + \
           str(self.ssao_intensity) + "#" + \
           str(self.enable_backface_culling) + "#" + \
           str(self.enable_frustum_culling) + "#" + \
           str(self.enable_fxaa) + "#" + \
           str(round(self.ambient_color.r,3)) + "," + str(round(self.ambient_color.g,3)) + "," + str(round(self.ambient_color.b,3)) + "#" + \
           str(self.enable_fog) + "#" + \
           str(self.fog_start) + "#" + \
           str(self.fog_end) + "#" + \
           str(self.near_clip) + "#" + \
           str(self.far_clip)


  ## Creates and initializes a geometry node in the scene.
  # @param NAME The name of the new node.
  # @param FILENAME Path to the object file to be loaded.
  # @param MATRIX The transformation matrix of the new node.
  # @param MATERIAL Material string to be used for the geometry.
  # @param GROUNDFOLLOWING_PICK_FLAG Boolean indicating if the new geometry should be pickable for GroundFollowing purposes.
  # @param MANIPULATION_PICK_FLAG Boolean indicating if the new geometry should be pickable for manipulation purposes.
  # @param PARENT_NODE Scenegraph node to append the geometry to.
  # @param RENDER_GROUP The render group to be associated with the new geometry.
  def init_geometry(self, NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, RENDER_GROUP):

    _loader = avango.gua.nodes.TriMeshLoader()

    _loader_flags = "avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY" # default loader flags

    if MATERIAL == None: # no material defined --> get materials from file description
      _loader_flags += " | avango.gua.LoaderFlags.LOAD_MATERIALS"
      MATERIAL = "data/materials/White.gmd" # default material

    if GROUNDFOLLOWING_PICK_FLAG == True or MANIPULATION_PICK_FLAG == True:
      _loader_flags += " | avango.gua.LoaderFlags.MAKE_PICKABLE"

    _node = _loader.create_geometry_from_file(NAME, FILENAME, MATERIAL, eval(_loader_flags))
    _node.Transform.value = MATRIX
  
    #print "LOADED", _node, _node.Name.value#, _loader_flags
  
    self.init_interactive_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP, True)

  ## Creates and initializes a light node in the scene.
  # @param TYPE Type of the new light. 0 = sun light, 1 = point light, 2 = spot light
  # @param NAME Name of the new light.
  # @param PARENT_NODE Scenegraph node to append the geometry to.
  # @param RENDER_GROUP The render group to be associated with the new light.
  # @param MANIPULATION_PICK_FLAG Boolean determining if the new light is pickable.
  # @param COLOR Color of the new light.
  # @param ENABLE_SHADOW Boolean indicating if the new light throws shadows.
  # @param SHADOW_MAP_SIZE Size of the shadow map if shadows are enabled.
  # @param LIGHT_DIMENSIONS Scaling of the light in all three directions.
  # @param ENABLE_DIFFUSE_SHADING Boolean saying if diffuse shading is enabled for this light.
  # @param ENABLE_SPECULAR_SHADING Boolean saying if specular shading is enabled for this light.
  # @param ENABLE_GODRAYS Boolean saying if god rays are enabled for this light.
  # @param SOFTNESS Softness factor of the new light.
  # @param FALLOFF Falloff factor of the new light.
  # @param ENABLE_LIGHT_GEOMETRY Boolean saying if a light geometry is to be visualized.
  def init_light(self, 
                TYPE = 0,
                NAME = "light",
                MATRIX = avango.gua.make_identity_mat(),
                PARENT_NODE = None,
                RENDER_GROUP = "main_scene",
                MANIPULATION_PICK_FLAG = False,
                COLOR = avango.gua.Vec3(0.75,0.75,0.75),
                ENABLE_SHADOW = False,
                SHADOW_MAP_SIZE = 1024,
                LIGHT_DIMENSIONS = avango.gua.Vec3(1.0,1.0,1.0),
                ENABLE_DIFFUSE_SHADING = True,
                ENABLE_SPECULAR_SHADING = True,
                ENABLE_GODRAYS = False,
                SOFTNESS = 1.0,
                FALLOFF = 1.0,
                ENABLE_LIGHT_GEOMETRY = True
                ):

    # init and parametrize light source
    if TYPE == 0: # sun light
      _light_node = avango.gua.nodes.SunLightNode()
      _light_node.EnableShadows.value = ENABLE_SHADOW
      _light_node.ShadowMapSize.value = SHADOW_MAP_SIZE
      _light_node.ShadowOffset.value = 0.002
      _light_node.ShadowCascadedSplits.value = [0.2, 3, 10, 50, 150]

      MANIPULATION_PICK_FLAG = False # sun light not pickable (infinite position) 

    elif TYPE == 1: # point light
      _light_node = avango.gua.nodes.PointLightNode()
      _light_node.Falloff.value = FALLOFF # exponent      

    elif TYPE == 2: # spot light
      _light_node = avango.gua.nodes.SpotLightNode()
      _light_node.EnableShadows.value = ENABLE_SHADOW
      _light_node.ShadowMapSize.value = SHADOW_MAP_SIZE
      _light_node.ShadowOffset.value = 0.005
      _light_node.Softness.value = SOFTNESS # exponent
      _light_node.Falloff.value = FALLOFF # exponent

    _light_node.Name.value = NAME
    _light_node.Color.value = COLOR
    _light_node.EnableDiffuseShading.value = ENABLE_DIFFUSE_SHADING
    _light_node.EnableSpecularShading.value = ENABLE_SPECULAR_SHADING
    _light_node.EnableGodrays.value = ENABLE_GODRAYS


    # init light object (incl. light source)
    if TYPE == 0: # sun light
      _light_node.Transform.value = MATRIX
    
      self.init_interactive_objects(_light_node, PARENT_NODE, False, MANIPULATION_PICK_FLAG, RENDER_GROUP, False)

    elif TYPE == 1 or TYPE == 2: # point light or spot light

      if TYPE == 1: # point light
        _filename = "data/objects/sphere.obj"

      elif TYPE == 2: # spot light
        _filename = "data/objects/lamp.obj"

      _loader = avango.gua.nodes.TriMeshLoader()
  
      _light_geometry = _loader.create_geometry_from_file(_light_node.Name.value + "_geometry", _filename, "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
      #_light_geometry.Transform.value = avango.gua.make_scale_mat(0.1)
      _light_geometry.Transform.value = avango.gua.make_scale_mat(3.0)
      _light_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF
      _light_geometry.GroupNames.value.append("man_pick_group") # prepare light geometry for picking
      
      if ENABLE_LIGHT_GEOMETRY == False:
        _light_geometry.GroupNames.value.append("do_not_display_group")
      else:
        _light_geometry.GroupNames.value.append(RENDER_GROUP)


      _node = avango.gua.nodes.TransformNode(Name = _light_node.Name.value)
      _node.Children.value = [_light_node, _light_geometry]
      _node.Transform.value = MATRIX
      
      _light_node.Transform.value = avango.gua.make_scale_mat(LIGHT_DIMENSIONS)

      self.init_interactive_objects(_node, PARENT_NODE, False, MANIPULATION_PICK_FLAG, RENDER_GROUP, False)

      _light_geometry.add_and_init_field(avango.script.SFObject(), "InteractiveObject", _node.InteractiveObject.value) # rework ??
      _light_geometry.InteractiveObject.dont_distribute(True)

  ## Creates and initializes an interactive object responsible for grouping.
  def init_group(self, NAME, MATRIX, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, RENDER_GROUP):
 
    _node = avango.gua.nodes.TransformNode()
    _node.Name.value = NAME    
    _node.Transform.value = MATRIX
 
    self.init_interactive_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP, False)
 
 
  ## Creates and initializes an interactive object responsible for displaying video avatars.
  def init_kinect(self, NAME, FILENAME, MATRIX, PARENT_NODE, RENDER_GROUP):
 
    _loader = avango.gua.nodes.Video3DLoader()
    _node = _loader.load(NAME, FILENAME)
    _node.Transform.value = MATRIX
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF
 
    self.init_interactive_objects(_node, PARENT_NODE, False, False, RENDER_GROUP, False)

  ## Creates and initializes an interactive object responsible for a point-based level-of-detail scene.
  def init_plod(self, NAME, FILENAME, MATRIX, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, RENDER_GROUP):
 
    _loader = avango.gua.nodes.PLODLoader()
    _loader.UploadBudget.value = 32
    _loader.RenderBudget.value = 512
    _loader.OutOfCoreBudget.value = 512

    _loader_flags = "avango.gua.PLODLoaderFlags.DEFAULTS" # default loader flags

    _loader_flags += " | avango.gua.PLODLoaderFlags.NORMALIZE_POSITION | avango.gua.PLODLoaderFlags.NORMALIZE_SCALE"
    
    if GROUNDFOLLOWING_PICK_FLAG == True or MANIPULATION_PICK_FLAG == True:
      _loader_flags += " | avango.gua.PLODLoaderFlags.MAKE_PICKABLE"      

    _node = _loader.create_geometry_from_file(NAME, FILENAME, eval(_loader_flags))
    _node.Transform.value = MATRIX
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF
 
    self.init_interactive_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP, False)


  ## Creates and initializes an interactive object.
  def init_interactive_objects(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP, RECURSIVE_FLAG):

    #print "!!!!!!!", NODE.get_type(), NODE.Name.value, len(NODE.Children.value), NODE.Path.value, RENDER_GROUP

    #_object = InteractiveObject()
    #_object.base_constructor(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

    if RECURSIVE_FLAG == True:

      if NODE.get_type() == 'av::gua::TransformNode' and len(NODE.Children.value) > 0: # group node with children (hierarchy)
        _object = InteractiveObject()
        _object.base_constructor(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

        _childs = []
        for _child in NODE.Children.value:
          _childs.append(_child)

        NODE.Children.value = []

        for _child in _childs:
          self.init_interactive_objects(_child, _object, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP, RECURSIVE_FLAG)

      else: # geometry
        _object = InteractiveObject()
        _object.base_constructor(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
  
    else:
      _object = InteractiveObject()
      _object.base_constructor(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
  

    '''
    if NODE.get_type() == "av::gua::TriMeshNode":
    
      _object = GeometryObject()
      _object.init(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

    elif NODE.get_type() == 'av::gua::SunLightNode' or NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':

      _object = LightObject()
      _object.init(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
    '''

  ## Registers an interactive object with this scene object.
  def register_interactive_object(self, INTERACTIVE_OBJECT):

    self.objects.append(INTERACTIVE_OBJECT)
  
  ## Searches for the interactive object with a given name and returns its instance.
  # @param NAME The name to be searched for.
  def get_interactive_object(self, NAME):
  
    for _object in self.objects:

      if _object.get_node().Name.value == NAME:
        return _object


  ## Gets the interactive object for a given scenegraph path.
  # @param NAME The path in the scenegraph to be searched for.
  def get_object(self, NAME):
  
    _node = self.SCENEGRAPH[self.scene_root.Path.value + "/" + NAME]

    if _node != None:
      
      if _node.has_field("InteractiveObject") == True:

        return _node.InteractiveObject.value

  ## Enables all objects in the scene.
  # @param FLAG Boolean indicating if all objects should be reset first.
  def enable_scene(self, FLAG):
  
    if FLAG == True:
      self.reset()
  
    for _object in self.objects:
      _object.enable_object(FLAG)
    
  ## Resets all objects in the scene.
  def reset(self):
  
    for _object in self.objects:
      _object.reset()


## Class to represent an object in a scene, associated to a scenegraph node.
class InteractiveObject(avango.script.Script):

  # internal fields
  ## @var sf_highlight_flag
  # Boolean field indicating if this object is to be highlighted.
  sf_highlight_flag = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(InteractiveObject).__init__()

    # variables

    ## @var hierarchy_level
    # Level of this interactive object in the local hierarchy. 
    self.hierarchy_level = 0

    ## @var render_group
    # Render group associated to this interactive object.
    self.render_group = ""

    ## @var parent_object
    # Parent InteractiveObject if present.
    self.parent_object = None

    ## @var child_objects
    # List of children InteractiveObjects if present.
    self.child_objects = []
    

  ## Custom constructor.
  # @param SCENE_MANAGER Reference to the SceneManager instance which is used.
  # @param NODE Scenegraph node for which an interactive object is to be created.
  # @param PARENT_OBJECT Parent object of NODE.
  # @param SCENEGRAPH Reference to the scenegraph in which the scene is existing.
  # @param NET_TRANS_NODE Reference to the nettrans node to append the scene to.
  # @param GROUNDFOLLOWING_PICK_FLAG Boolean indicating if the new geometry should be pickable for GroundFollowing purposes.
  # @param MANIPULATION_PICK_FLAG Boolean indicating if the new geometry should be pickable for manipulation purposes.
  def base_constructor(self, SCENE, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP):

    # references
    ## @var SCENE
    # Reference to the SceneObject instance this interactive object is belonging to.
    self.SCENE = SCENE

    self.SCENE.register_interactive_object(self)

    # update variables    
    self.parent_object = PARENT_OBJECT
    self.render_group = RENDER_GROUP

    ## @var node
    # Scenegraph node associated with this interactive object.
    self.node = NODE
        
    self.node.add_and_init_field(avango.script.SFObject(), "InteractiveObject", self)
    self.node.InteractiveObject.dont_distribute(True)

    ## @var home_mat
    # Initial transformation of the handled scenegraph node.
    self.home_mat = self.node.Transform.value

    ## @var gf_pick_flag
    # Boolean indicating if the new geometry should be pickable for GroundFollowing purposes.
    self.gf_pick_flag = GROUNDFOLLOWING_PICK_FLAG

    ## @var man_pick_flag
    # Boolean indicating if the new geometry should be pickable for manipulation purposes.
    self.man_pick_flag = MANIPULATION_PICK_FLAG

    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
      #print "append to IO"
      self.parent_object.append_child_object(self)

    else: # scene root
      #print "append to scene root"
      self.parent_object.Children.value.append(self.node)
    
    #print "new object", self, self.hierarchy_level, self.node, self.node.Name.value, self.node.Transform.value.get_translate(), self.parent_object

    # init sub classes
    ## @var bb_vis
    # Instance of BoundingBoxVisualization to make the bounding box of this object visible.
    self.bb_vis = BoundingBoxVisualization()
    self.bb_vis.my_constructor(self, self.SCENE.get_scenegraph(), self.SCENE.get_net_trans_node(), self.get_hierarchy_material())

    self.enable_object(True)


  ## Returns the node member.
  def get_node(self):
    
    return self.node

  ## Enables or disables this object.
  # @param FLAG Boolean indicating the activation or deactivation process.
  def enable_object(self, FLAG):
  
    if FLAG == True: # enable object
      self.node.GroupNames.value = [self.render_group] # set geometry visible

      if self.gf_pick_flag == True:
        self.node.GroupNames.value.append("gf_pick_group")

      if self.man_pick_flag == True:
        self.node.GroupNames.value.append("man_pick_group")
      
      #for _child in self.node.Children.value:
      #  _child.GroupNames.value = [] # set geometry visible
    
      #self.enable_highlight(True)
    
    else: # disable object
      self.node.GroupNames.value = ["do_not_display_group"] # set geometry invisible
      
      self.enable_highlight(False)
      
      #for _child in self.transform.Children.value:
      #  _child.GroupNames.value = ["invisible_group"] # set geometry invisible

  ## Enables or disables the highlight for this object.
  # @param FLAG Boolean indicating the activation or deactivation process.
  def enable_highlight(self, FLAG):
      
    self.sf_highlight_flag.value = FLAG
        
    # highlight/dehighlight subgraph
    for _child_object in self.child_objects:
      _child_object.enable_highlight(FLAG)

  ## Appends another object as a child of this object.
  # @param OBJECT The object to be appended as a child.
  def append_child_object(self, OBJECT):

    self.child_objects.append(OBJECT)

    self.get_node().Children.value.append(OBJECT.get_node())

    OBJECT.hierarchy_level = self.hierarchy_level + 1

  ## Removes another object as a child of this object.
  # @param OBJECT The object to be removed as a child.
  def remove_child_object(self, OBJECT):

    if self.child_objects.count(OBJECT) > 0:

      self.child_objects.remove(OBJECT)

      self.node.Children.value.remove(OBJECT.get_node())

      OBJECT.hierarchy_level = 0


  ## Gets the transformation of the handled scenegraph node.
  def get_local_transform(self):

    return self.node.Transform.value

  ## Gets the world transformation of the handled scenegraph node.
  def get_world_transform(self):

    return self.node.WorldTransform.value

  ## Sets the transformation of the handled scenegraph node.
  def set_local_transform(self, MATRIX):

    self.node.Transform.value = MATRIX

  ## Sets the world ransformation of the handled scenegraph node.
  def set_world_transform(self, MATRIX):

    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object    
      _parent_world_transform = self.parent_object.get_world_transform()
  
      _mat = avango.gua.make_inverse_mat(_parent_world_transform) * MATRIX # matrix is transformed into world coordinate system of parent object in scenegraph
  
      self.set_local_transform(_mat)
    
    else: # scene root
      
      self.set_local_transform(MATRIX)

  ## Resets the interactive object to the initial matrix.
  def reset(self):
      
    self.set_local_transform(self.home_mat)

    self.bb_vis.calc_bb()

  ## Returns the material string belonging to this object's hierarchy level.
  def get_hierarchy_material(self):
  
    return self.SCENE.get_scene_manager().get_hierarchy_material(self.hierarchy_level)
    
  
  ## Gets the parent object of this interactive object or returns None if there isn't any.
  def get_parent_object(self):
    
    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
      
      return self.parent_object

    else: # scene root
    
      return None

  ## Returns all objects which are located at this or a higher hierarchy level.
  # @param HIERARCHY_LEVEL The hierarchy level to be started from.
  def get_higher_hierarchical_object(self, HIERARCHY_LEVEL):

    if self.hierarchy_level == HIERARCHY_LEVEL:
      return self
    
    else:
    
      if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
        return self.parent_object.get_higher_hierarchical_object(HIERARCHY_LEVEL)

      else: # scene root
        return None


'''
class GeometryObject(InteractiveObject):

  def init(self, SCENE, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP):

    self.base_constructor(SCENE, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)



class LightObject(InteractiveObject):

  def init(self, SCENE, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP):
    
    self.base_constructor(SCENE, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
'''

    
