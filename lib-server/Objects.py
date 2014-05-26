#!/usr/bin/python

## @file
# 

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ConsoleIO   import *
from Visualization import *

# import python libraries
# ...

import psycopg2


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
  def load_objects_from_database(self, USER, PASSWORD, DBNAME, TABLENAME, HOST = "localhost", SELECT = "*"):
    # connect to database
    try:
      _dbconn = psycopg2.connect("dbname='" + DBNAME + "' user='" + USER + "' host='" + HOST + "' password = '" + PASSWORD + "'")
    except:
      print_error("Unable to access database '{0}' as user '{1}' on '{2}'".format(DBNAME, USER, HOST), False)
      return False

    # select rows from table according to given select-string
    _cursor = _dbconn.cursor()
    _cursor.execute("SELECT {0} FROM {1}".format(SELECT, TABLENAME))

    # load geometry for each row
    for _id, _name, _filename, _color, _trans, _rot, _scale in _cursor.fetchall():
      _trans_mat = avango.gua.make_trans_mat(_trans[0], _trans[1], _trans[2])
      _rot_mat = avango.gua.make_rot_mat(_rot[0], _rot[1], _rot[2], _rot[3])
      _scale_mat = avango.gua.make_scale_mat(_scale[0], _scale[1], _scale[2])
      _mat = _trans_mat * _scale_mat * _rot_mat

      self.init_geometry(_name, _filename, _mat, None, True, True, self.scene_root, _id)


  def init_geometry(self, NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, DB_ID = -1):

    _loader = avango.gua.nodes.GeometryLoader()

    _loader_flags = "avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.OPTIMIZE_GEOMETRY"

    if MATERIAL == None: # no material defined --> get materials from file description
      _loader_flags += " | avango.gua.LoaderFlags.LOAD_MATERIALS"
      MATERIAL = "data/materials/White.gmd" # default material

    if GROUNDFOLLOWING_PICK_FLAG == True or MANIPULATION_PICK_FLAG == True:
      _loader_flags += " | avango.gua.LoaderFlags.MAKE_PICKABLE"

    _node = _loader.create_geometry_from_file(NAME, FILENAME, MATERIAL, eval(_loader_flags))
    _node.Transform.value = MATRIX
  
    self.init_objects(_node, PARENT_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, DB_ID)
 

  def init_light(self, TYPE, NAME, COLOR, MATRIX, PARENT_NODE):

    if TYPE == 0: # sun light
      _node = avango.gua.nodes.SunLightNode()
      _node.EnableShadows.value = True
      _node.ShadowMapSize.value = 2048
      _node.ShadowOffset.value = 0.001

    elif TYPE == 1: # point light
      _node = avango.gua.nodes.PointLightNode()
      _node.Falloff.value = 1.0 # exponent

    elif TYPE == 2: # spot light
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


  def init_objects(self, NODE, PARENT_OBJECT, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, DB_ID = -1):

    if NODE.get_type() == 'av::gua::TransformNode' and len(NODE.Children.value) > 0: # group node 

      #_node = avango.gua.nodes.TransformNode()
      #_node.Name.value = NODE.Name.value
      #_node.Transform.value = NODE.Transform.value
      #_node.BoundingBox.value = NODE.BoundingBox.value

      _object = InteractiveObject()
      _object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
      #_object.my_constructor(self.SCENE_MANAGER, _node, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)

      self.objects.append(_object)

      for _child in NODE.Children.value:
        self.init_objects(_child, _object, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG)
        
    elif NODE.get_type() == 'av::gua::GeometryNode' or NODE.get_type() == 'av::gua::SunLightNode' or NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':

      _object = InteractiveObject()
      _object.my_constructor(self.SCENE_MANAGER, NODE, PARENT_OBJECT, self.SCENEGRAPH, self.NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, DB_ID)

      self.objects.append(_object)


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


  def my_constructor(self, SCENE_MANAGER, NODE, PARENT_OBJECT, SCENEGRAPH, NET_TRANS_NODE, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, DB_ID = -1):

    # references
    self.SCENE_MANAGER = SCENE_MANAGER

    # variables    
    self.hierarchy_level = 0

    self.parent_object = PARENT_OBJECT

    self.child_objects = []


    if NODE.get_type() == 'av::gua::PointLightNode' or NODE.get_type() == 'av::gua::SpotLightNode':
      _loader = avango.gua.nodes.GeometryLoader()

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

    self.home_mat = self.node.Transform.value

    self.gf_pick_flag = GROUNDFOLLOWING_PICK_FLAG
    self.man_pick_flag = MANIPULATION_PICK_FLAG
    self.db_id = DB_ID


    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
      #print "append to IO"
      self.parent_object.append_child_object(self)

    else: # scene root
      #print "append to scene root"
      self.parent_object.Children.value.append(self.node)
    
    #print "new object", self, self.hierarchy_level, self.node, self.node.Name.value, self.node.Transform.value.get_translate(), self.parent_object#, self.parent_object.get_type()

    # init sub classes       
    self.bb_vis = BoundingBoxVisualization()
    self.bb_vis.my_constructor(self, SCENEGRAPH, NET_TRANS_NODE, self.get_hierarchy_material())

    self.enable_object(True)


  # functions
  def get_node(self):
    
    return self.node


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

  
  def enable_highlight(self, FLAG):
      
    self.sf_highlight_flag.value = FLAG
    
    for _child_object in self.child_objects:
      _child_object.enable_highlight(FLAG)

         
  def append_child_object(self, OBJECT):

    self.child_objects.append(OBJECT)

    #self.get_node().Children.value.append(OBJECT.get_node())

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
  
    return self.SCENE_MANAGER.get_hierarchy_material(self.hierarchy_level)
    
    
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
  

  def print_db_data(self):

    if self.db_id >= 0:

      DBNAME = "pitoti"
      USER = "pitoti"
      HOST = "localhost"
      PASSWORD = "seradina"
      TABLENAME = "testscene"
      
      # connect to database
      try:
        _dbconn = psycopg2.connect("dbname='" + DBNAME + "' user='" + USER + "' host='" + HOST + "' password = '" + PASSWORD + "'")
      except:
        print_error("Unable to access database '{0}' as user '{1}' on '{2}'".format(DBNAME, USER, HOST), False)
        return False

      # select rows from table according to given select-string
      _cursor = _dbconn.cursor()
      _cursor.execute("SELECT * FROM {0} WHERE id = {1}".format(TABLENAME, self.db_id))

      # load geometry for each row
      for _id, _name, _filename, _color, _trans, _rot, _scale in _cursor.fetchall():
        print "PICKED '{0}', loaded from '{1}'".format(_name, _filename)
