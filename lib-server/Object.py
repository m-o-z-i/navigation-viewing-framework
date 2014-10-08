#!/usr/bin/python

## @file
# Contains class Object 

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Visualization import *
from Manipulators import *

class Object(avango.script.Script):
  
  sf_number_of_contacts = avango.SFInt()
  def __init__(self):
    self.super(Object).__init__()

  # Manipulator als Liste uebergeben !!  

  def my_constructor(self, SCENE, NODE, MATRIX, MATERIAL, PARENT_OBJECT, MANIPULATORS, CHILD_OBJECTS):
    self.scene = SCENE
    self.node = NODE
    self.parent_object = PARENT_OBJECT
    self.manipulators = []
    self.active_manipulator = None
    self.child_objects = CHILD_OBJECTS
    self.contacts = []
    self.number_of_contacts = 0
    
    
    for _child in self.node.Children.value:
      _child.add_and_init_field(avango.script.SFObject(), "InteractiveObject", self)
      _child.InteractiveObject.dont_distribute(True)
    #self.node.add_and_init_field(avango.script.SFObject(), "InteractiveObject", self)
    #self.node.InteractiveObject.dont_distribute(True)

    self.node.WorldTransform.value = MATRIX

    for _manipulator in MANIPULATORS:
      if _manipulator == "MatrixManipulator":
        self.manipulators.append(MatrixManipulator(_manipulator, self))

    if self.parent_object.get_type() == "Object::Object": # interactive object
      #print "append to IO"
      self.parent_object.add_child(self)

    else: # scene root
      #print "append to scene root"
      print self.parent_object
      self.parent_object.Children.value.append(self.node)
      self.parent_object = None
    

  def get_parent(self):
    return self.parent_object

  def get_node(self):
    return self.node

  def add_contact(self, CONTACT):
    
    for _manipulator in self.manipulators:  
      print "!!!"
      print _manipulator.name
      if _manipulator.name == CONTACT.manipulator and _manipulator.is_available:
        print "!"
        self.contacts.append(CONTACT)
        _manipulator.add_input(CONTACT)
        self.active_manipulator = _manipulator

    #self.number_of_contacts += 1

  def remove_contact(self, CONTACT):
    for _contact in self.contacts:
      if _contact == CONTACT:
        self.contacts.remove(CONTACT)
        self.active_manipulator.remove_input(CONTACT)
        if len(self.contacts) == 0:
          self.active_manipulator = None
    #self.number_of_contacts -= 1

  def add_child(self, OBJECT):
    
    _mat = OBJECT.get_world_transform()
    self.child_objects.append(OBJECT)
    OBJECT.parent_object = self
    OBJECT.set_world_transform(_mat)
    self.get_node().Children.value.append(OBJECT.get_node())
    
    
  def remove_child(self,OBJECT):
    self.child_objects.remove(OBJECT)
    self.get_node().Children.value.remove(OBJECT.get_node())

  def get_manipulator(self,MANIPULATOR):
    for _manipulator in self.manipulators:
      if _manipulator.get_name() == MANIPULATOR:
        return _manipulator
      else: 
        return None

  def has_parent(self):
    if self.parent_object == None:
      return False
    else:
      return True


  def get_transform(self):
     return self.node.Transform.value    
    
    
  def set_transform(self, MATRIX):
     self.node.Transform.value = MATRIX

  def get_world_transform(self):

    return self.node.WorldTransform.value

  def set_world_transform(self, MATRIX):

    if self.parent_object != None and self.parent_object.get_type() == "Object::Object": # interactive object    
      _parent_world_transform = self.parent_object.get_world_transform()
  
      _mat = avango.gua.make_inverse_mat(_parent_world_transform) * MATRIX # matrix is transformed into world coordinate system of parent object in scenegraph
  
      self.set_transform(_mat)
    
    else: # scene root
      
      self.set_transform(MATRIX)

  #callbacks
  

