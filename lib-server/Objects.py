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


  ## Creates and initializes a geometry node in the scene.
  # @param NAME The name of the new node.
  # @param FILENAME Path to the object file to be loaded.
  # @param MATRIX The transformation matrix of the new node.
  # @param MATERIAL Material string to be used for the geometry.
  # @param GROUNDFOLLOWING_PICK_FLAG Boolean indicating if the new geometry should be pickable for GroundFollowing purposes.
  # @param MANIPULATION_PICK_FLAG Boolean indicating if the new geometry should be pickable for manipulation purposes.
  # @param PARENT_NODE Scenegraph node to append the geometry to.
  def init_geometry(self, NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE):

    _loader = avango.gua.nodes.GeometryLoader()

    _loader_flags = "avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY"

    if MATERIAL == None: # no material defined --> get materials from file description
      _loader_flags += " | avango.gua.LoaderFlags.LOAD_MATERIALS"
      MATERIAL = "data/materials/White.gmd" # default material

    if GROUNDFOLLOWING_PICK_FLAG == True or MANIPULATION_PICK_FLAG == True:
      _loader_flags += " | avango.gua.LoaderFlags.MAKE_PICKABLE"

    _node = _loader.create_geometry_from_file(NAME, FILENAME, MATERIAL, eval(_loader_flags))
    _node.Transform.value = MATRIX
  
    self.init_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
 
  ## Creates and initializes a light node in the scene.
  # @param TYPE Type of the new light. 0 sun light, 1 point light, 2 spot light
  # @param NAME The name of the new node.
  # @param COLOR The color to be assigned to the light.
  # @param MATRIX The transformation matrix of the new node.
  # @param PARENT_NODE Scenegraph node to append the geometry to.
  def init_light(self, TYPE, NAME, COLOR, MATRIX, PARENT_NODE):

    # sun light node
    if TYPE == 0:
      _node = avango.gua.nodes.SunLightNode()
      _node.EnableShadows.value = True
      _node.ShadowMapSize.value = 2048
      _node.ShadowOffset.value = 0.001

    # point light node
    elif TYPE == 1:
      _node = avango.gua.nodes.PointLightNode()
      _node.Falloff.value = 1.0 # exponent

    # spot light node
    elif TYPE == 2:
      _node = avango.gua.nodes.SpotLightNode()
      _node.EnableShadows.value = True
      _node.ShadowMapSize.value = 2048
      _node.ShadowOffset.value = 0.001
      _node.Softness.value = 1.0 # exponent
      _node.Falloff.value = 1.0 # exponent

      
    _node.Name.value = NAME
    _node.Color.value = COLOR
    _node.Transform.value = MATRIX
    _node.EnableDiffuseShading.value = True
    _node.EnableSpecularShading.value = True
    _node.EnableGodrays.value = True

    self.init_objects(_node, PARENT_NODE, False, True)

  ## Initializes InteractiveObject instances assigned to scenegraph nodes.
  # @param NODE Scenegraph node for which an interactive object is to be created.
  # @param PARENT_OBJECT Parent object of NODE.
  # @param GROUNDFOLLOWING_PICK_FLAG Boolean indicating if the new geometry should be pickable for GroundFollowing purposes.
  # @param MANIPULATION_PICK_FLAG Boolean indicating if the new geometry should be pickable for manipulation purposes.
  def init_objects(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG):

    if NODE.get_type() == 'av::gua::TransformNode' and len(NODE.Children.value) > 0: # group node 

      _object = InteractiveObject()
      _object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)

      self.objects.append(_object)

      for _child in NODE.Children.value:
        self.init_objects(_child, _object, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
        
    elif NODE.get_type() == 'av::gua::GeometryNode' or NODE.get_type() == 'av::gua::SunLightNode' or NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':

      _object = InteractiveObject()
      _object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)

      self.objects.append(_object)

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

  # Default constructor.
  def __init__(self):
    self.super(InteractiveObject).__init__()

  ## Custom constructor.
  # @param SCENE_MANAGER Reference to the SceneManager instance which is used.
  # @param NODE Scenegraph node for which an interactive object is to be created.
  # @param PARENT_OBJECT Parent object of NODE.
  # @param SCENEGRAPH Reference to the scenegraph in which the scene is existing.
  # @param NET_TRANS_NODE Reference to the nettrans node to append the scene to.
  # @param GROUNDFOLLOWING_PICK_FLAG Boolean indicating if the new geometry should be pickable for GroundFollowing purposes.
  # @param MANIPULATION_PICK_FLAG Boolean indicating if the new geometry should be pickable for manipulation purposes.
  def my_constructor(self, SCENE_MANAGER, NODE, PARENT_OBJECT, SCENEGRAPH, NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG):

    # references
    ## @var SCENE_MANAGER
    # Reference to the SceneManager instance which is used.
    self.SCENE_MANAGER = SCENE_MANAGER

    # variables
    ## @var hierarchy_level
    # Level of this object in the hierarchy. 
    self.hierarchy_level = 0

    ## @var parent_object
    # Parent object of this interactive object.
    self.parent_object = PARENT_OBJECT

    ## @var child_objects
    # List of child objects that belong to this interactive object.
    self.child_objects = []

    if NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':
      _loader = avango.gua.nodes.GeometryLoader()

      ## @var node
      # Geometry placed around lights to make them grabbable.
      self.node = _loader.create_geometry_from_file(NODE.Name.value, "data/objects/sphere.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
      self.node.Children.value = [NODE]
      self.node.Transform.value = NODE.Transform.value * avango.gua.make_scale_mat(0.2)

      if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object

        self.parent_object.get_node().Children.value.append(self.node)

      else: # scene root
        self.parent_object.Children.value.append(self.node)

      NODE.Transform.value = avango.gua.make_scale_mat(15.0)
      NODE.Name.value += "_lightsource"

    else:
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
    
    #print "new object", self, self.hierarchy_level, self.node, self.node.Name.value, self.node.Transform.value.get_translate(), self.parent_object#, self.parent_object.get_type()

    # init sub classes
    ## @var bb_vis
    # Instance of BoundingBoxVisualization to make the bounding box of this object visible.
    self.bb_vis = BoundingBoxVisualization()
    self.bb_vis.my_constructor(self, SCENEGRAPH, NET_TRANS_NODE, self.get_hierarchy_material())

    self.enable_object(True)


  ## Returns the node member.
  def get_node(self):
    
    return self.node

  ## Enables or disables this object.
  # @param FLAG Boolean indicating the activation or deactivation process.
  def enable_object(self, FLAG):
  
    if FLAG == True: # enable object
      self.node.GroupNames.value = [] # set geometry visible

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
    
    for _child_object in self.child_objects:
      _child_object.enable_highlight(FLAG)

  ## Appends another object as a child of this object.
  # @param OBJECT The object to be appended as a child.
  def append_child_object(self, OBJECT):

    self.child_objects.append(OBJECT)

    #self.get_node().Children.value.append(OBJECT.get_node())

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
  
    return self.SCENE_MANAGER.get_hierarchy_material(self.hierarchy_level)
    
  
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
    
    
