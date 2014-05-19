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


class InteractiveObject(avango.script.Script):

  # internal fields
  sf_highlight_flag = avango.SFBool()

  # constructor
  def __init__(self):
    self.super(InteractiveObject).__init__()


  def my_constructor(self, SCENE_MANAGER, NODE, PARENT_OBJECT, SCENEGRAPH, NET_TRANS_NODE):

    # references
    self.SCENE_MANAGER = SCENE_MANAGER

    # variables    
    self.hierarchy_level = 0
    
    self.node = NODE
    self.node.add_and_init_field(avango.script.SFObject(), "InteractiveObject", self)
    self.node.InteractiveObject.dont_distribute(True)

    self.parent_object = PARENT_OBJECT

    self.child_objects = []

    self.home_mat = self.node.Transform.value

    if self.parent_object.get_type() == "Objects::InteractiveObject": # interactive object
      #print "append to IO"
      self.parent_object.append_child_object(self)

    else: # scene root
      #print "append to scene root"
      self.parent_object.Children.value.append(self.node)
    
    #print "new object", self, self.hierarchy_level, self.node, self.node.Name.value, self.node.Transform.value.get_translate(), self.parent_object, self.parent_object.get_type()

    # init sub classes       
    self.bb_vis = BoundingBoxVisualization()
    self.bb_vis.my_constructor(self, SCENEGRAPH, NET_TRANS_NODE, self.get_hierarchy_material())

    self.enable_highlight(False)


  # functions
  def get_node(self):
    
    return self.node

  
  def enable_highlight(self, FLAG):
      
    self.sf_highlight_flag.value = FLAG
    
    for _child_object in self.child_objects:
      _child_object.enable_highlight(FLAG)

         
  def append_child_object(self, OBJECT):

    self.child_objects.append(OBJECT)

    self.node.Children.value.append(OBJECT.get_node())

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
    
    
