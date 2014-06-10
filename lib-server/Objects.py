#!/usr/bin/python

## @file
# 

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Visualization import *

# import python libraries
# ...


class SceneObject:

  def __init__(self, NAME, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):

    # references
    self.SCENE_MANAGER = SCENE_MANAGER
    self.SCENEGRAPH = SCENEGRAPH
    self.NET_TRANS_NODE = NET_TRANS_NODE

    # variables
    self.objects = [] # interactive objects
    self.name = NAME

    self.SCENE_MANAGER.scenes.append(self)

    # nodes
    self.scene_root = avango.gua.nodes.TransformNode(Name = self.name)
    NET_TRANS_NODE.Children.value.append(self.scene_root)


  # functions
  def get_scene_manager(self):
  
    return self.SCENE_MANAGER
    

  def get_scenegraph(self):
  
    return self.SCENEGRAPH


  def get_net_trans_node(self):
  
    return self.NET_TRANS_NODE   

  
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
  
    #print "LOADED", _node, _node.Name.value
  
    self.init_interactive_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
 
   
  def init_light(self, 
                TYPE = 0,
                NAME = "light",
                MATRIX = avango.gua.make_identity_mat(),
                PARENT_NODE = None,
                RENDER_GROUP = "",
                MANIPULATION_PICK_FLAG = False,
                COLOR = avango.gua.Vec3(0.75,0.75,0.75),
                ENABLE_SHADOW = False,
                SHADOW_MAP_SIZE = 1024,
                SHADOW_DIMENSIONS = avango.gua.Vec3(1.0,1.0,1.0),
                ENABLE_DIFFUSE_SHADING = True,
                ENABLE_SPECULAR_SHADING = True,
                ENABLE_GODRAYS = False,
                SOFTNESS = 1.0,
                FALLOFF = 1.0
                ):

    # init and parametrize light source
    if TYPE == 0: # sun light
      _light_node = avango.gua.nodes.SunLightNode()
      _light_node.EnableShadows.value = ENABLE_SHADOW
      _light_node.ShadowMapSize.value = SHADOW_MAP_SIZE
      _light_node.ShadowOffset.value = 0.001

      MANIPULATION_PICK_FLAG = False # sun light not pickable (infinite position) 

    elif TYPE == 1: # point light
      _light_node = avango.gua.nodes.PointLightNode()
      _light_node.Falloff.value = FALLOFF # exponent      

    elif TYPE == 2: # spot light
      _light_node = avango.gua.nodes.SpotLightNode()
      _light_node.EnableShadows.value = ENABLE_SHADOW
      _light_node.ShadowMapSize.value = SHADOW_MAP_SIZE
      _light_node.ShadowOffset.value = 0.001
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
    
      self.init_interactive_objects(_light_node, PARENT_NODE, False, MANIPULATION_PICK_FLAG, RENDER_GROUP)

    elif TYPE == 1 or TYPE == 2: # point light or spot light

      if TYPE == 1: # point light
        _filename = "data/objects/sphere.obj"

      elif TYPE == 2: # spot light
        _filename = "data/objects/lamp.obj"

      _loader = avango.gua.nodes.TriMeshLoader()
  
      _light_geometry = _loader.create_geometry_from_file(_light_node.Name.value + "_geometry", _filename, "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
      _light_geometry.Transform.value = avango.gua.make_scale_mat(0.1)
      _light_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF
      _light_geometry.GroupNames.value.append("man_pick_group") # prepare light geometry for picking
  
      _node = avango.gua.nodes.TransformNode(Name = _light_node.Name.value)
      _node.Children.value = [_light_node, _light_geometry]
      _node.Transform.value = MATRIX
      
      _light_node.Transform.value = avango.gua.make_scale_mat(SHADOW_DIMENSIONS)

      self.init_interactive_objects(_node, PARENT_NODE, False, MANIPULATION_PICK_FLAG, RENDER_GROUP)

      _light_geometry.add_and_init_field(avango.script.SFObject(), "InteractiveObject", _node.InteractiveObject.value) # rework
      _light_geometry.InteractiveObject.dont_distribute(True)


  def init_group(self, NAME, MATRIX, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, RENDER_GROUP):
 
    _node = avango.gua.nodes.TransformNode()
    _node.Name.value = NAME    
    _node.Transform.value = MATRIX
 
    self.init_interactive_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
 
 

  def init_kinect(self, NAME, FILENAME, MATRIX, PARENT_NODE, RENDER_GROUP):
 
    _loader = avango.gua.nodes.Video3DLoader()
    _node = _loader.load(NAME, FILENAME)
    _node.Transform.value = MATRIX
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF
 
    self.init_interactive_objects(_node, PARENT_NODE, False, False, RENDER_GROUP)    


  def init_interactive_objects(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP):

    print "!!!!!!!", NODE.get_type(), NODE.Name.value, len(NODE.Children.value), NODE.Path.value, RENDER_GROUP

    _object = InteractiveObject()
    _object.base_constructor(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

    '''
    if NODE.get_type() == 'av::gua::TransformNode' and len(NODE.Children.value) > 0: # group node with children (hierarchy)
      
      _node = avango.gua.nodes.TransformNode()
      _node.Name.value = NODE.Name.value
      _node.Transform.value = NODE.Transform.value
      _node.BoundingBox.value = NODE.BoundingBox.value

      _object = InteractiveObject()
      _object.base_constructor(self, _node, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

      for _child in NODE.Children.value:
        #_child.Parent.value = None
        self.init_interactive_objects(_child, _object, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

    else:
      
      _object = InteractiveObject()
      _object.base_constructor(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
    '''

    '''
    if NODE.get_type() == "av::gua::TriMeshNode":
    
      _object = GeometryObject()
      _object.init(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

    elif NODE.get_type() == 'av::gua::SunLightNode' or NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':

      _object = LightObject()
      _object.init(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
    '''


  '''
  def init_objects(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP):

    print "!!!!!!!", NODE.get_type(), NODE.Name.value, NODE.Path.value, RENDER_GROUP

    if NODE.get_type() == 'av::gua::TransformNode' and len(NODE.Children.value) > 0: # group node 

      #_node = avango.gua.nodes.TransformNode()
      #_node.Name.value = NODE.Name.value
      #_node.Transform.value = NODE.Transform.value
      #_node.BoundingBox.value = NODE.BoundingBox.value

      _object = InteractiveObject()
      #_object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
      _object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

      self.objects.append(_object)

      for _child in NODE.Children.value:
        self.init_objects(_child, _object, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)
        
    elif NODE.get_type() == "av::gua::TriMeshNode" or NODE.get_type() == "av::gua::Video3DNode" or NODE.get_type() == 'av::gua::SunLightNode' or NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':

      _object = InteractiveObject()
      #_object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
      _object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP)

      self.objects.append(_object)
  '''
  

  def register_interactive_object(self, INTERACTIVE_OBJECT):

    self.objects.append(INTERACTIVE_OBJECT)


  def get_object(self, NAME):
  
    _node = self.SCENEGRAPH[self.scene_root.Path.value + "/" + NAME]

    if _node != None:
      
      if _node.has_field("InteractiveObject") == True:

        return _node.InteractiveObject.value


  def enable_scene(self, FLAG):
  
    if FLAG == True:
      self.reset()
  
    for _object in self.objects:
      _object.enable_object(FLAG)
    
    
  def reset(self):
  
    for _object in self.objects:
      _object.reset()



class InteractiveObject(avango.script.Script):

  # internal fields
  sf_highlight_flag = avango.SFBool()

  # constructor
  def __init__(self):
    self.super(InteractiveObject).__init__()

    # variables    
    self.hierarchy_level = 0
    self.render_group = ""
    self.parent_object = None
    self.child_objects = []
    

  def base_constructor(self, SCENE, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, RENDER_GROUP):

    # references
    self.SCENE = SCENE

    self.SCENE.register_interactive_object(self)

    # update variables    
    self.parent_object = PARENT_OBJECT
    self.render_group = RENDER_GROUP
    self.node = NODE
        
    self.node.add_and_init_field(avango.script.SFObject(), "InteractiveObject", self)
    self.node.InteractiveObject.dont_distribute(True)

    self.home_mat = self.node.Transform.value

    self.gf_pick_flag = GROUNDFOLLOWING_PICK_FLAG
    self.man_pick_flag = MANIPULATION_PICK_FLAG


    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
      #print "append to IO"
      self.parent_object.append_child_object(self)

    else: # scene root
      #print "append to scene root"
      self.parent_object.Children.value.append(self.node)
    
    print "new object", self, self.hierarchy_level, self.node, self.node.Name.value, self.node.Transform.value.get_translate(), self.parent_object

    # init sub classes       
    self.bb_vis = BoundingBoxVisualization()
    self.bb_vis.my_constructor(self, self.SCENE.get_scenegraph(), self.SCENE.get_net_trans_node(), self.get_hierarchy_material())

    self.enable_object(True)


  # functions
  def get_node(self):
    
    return self.node


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

  
  def enable_highlight(self, FLAG):
      
    self.sf_highlight_flag.value = FLAG
        
    # highlight/dehighlight subgraph
    for _child_object in self.child_objects:
      _child_object.enable_highlight(FLAG)

         
  def append_child_object(self, OBJECT):

    self.child_objects.append(OBJECT)

    self.get_node().Children.value.append(OBJECT.get_node())

    OBJECT.hierarchy_level = self.hierarchy_level + 1


  def remove_child_object(self, OBJECT):

    if self.child_objects.count(OBJECT) > 0:

      self.child_objects.remove(OBJECT)

      self.node.Children.value.remove(OBJECT.get_node())

      OBJECT.hierarchy_level = 0


  def get_local_transform(self):

    return self.node.Transform.value


  def get_world_transform(self):

    return self.node.WorldTransform.value

  
  def set_local_transform(self, MATRIX):

    self.node.Transform.value = MATRIX


  def set_world_transform(self, MATRIX):

    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object    
      _parent_world_transform = self.parent_object.get_world_transform()
  
      _mat = avango.gua.make_inverse_mat(_parent_world_transform) * MATRIX # matrix is transformed into world coordinate system of parent object in scenegraph
  
      self.set_local_transform(_mat)
    
    else: # scene root
      
      self.set_local_transform(MATRIX)


  def reset(self):
      
    self.set_local_transform(self.home_mat) # set back to intial matrix

    self.bb_vis.calc_bb()


  def get_hierarchy_material(self):
  
    return self.SCENE.get_scene_manager().get_hierarchy_material(self.hierarchy_level)
    
    
  def get_parent_object(self):
    
    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
      
      return self.parent_object

    else: # scene root
    
      return None


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

    
