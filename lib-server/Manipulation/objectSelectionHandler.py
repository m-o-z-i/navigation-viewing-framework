#!/usr/bin/python

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


# import framework libraries
from myInteractionTool import*
from Object import*

class objectSelectionHandler:

  def __init__(self):
    self.selected_object = None
    

  def select(self, CURRENT_PICK,  CONTACT):

    if self.selected_object != CURRENT_PICK and CURRENT_PICK != None:
      if self.selected_object != None:        
        self.selected_object.remove_contact(CONTACT)
      self.selected_object = CURRENT_PICK
      self.selected_object.add_contact(CONTACT)
        

  def deselect(self, CONTACT):
        
    self.selected_object.remove_contact(CONTACT)
    self.selected_object = None

  def subgroup_select(self, OBJECT, MANIPULATION_MODE, CONTACT):

    if OBJECT.get_parent() == None or (len(OBJECT.child_objects) == 0 and OBJECT.active_manipulator != None):
      _object = OBJECT
      
    else:
      _object = OBJECT
      
      while _object.get_parent() != None and  _object.get_parent().get_manipulator(MANIPULATION_MODE) != None and _object.get_parent().get_manipulator(MANIPULATION_MODE).is_available:
        #_parent_manipulator = OBJECT.get_parent().get_manipulator(MANIPULATION_MODE)
        #if _parent_manipulator != None and _parent_manipulator.is_available:
        
     
        
        _object = _object.get_parent()
        
        
    
    CONTACT.set_object(_object)
    self.select(_object, CONTACT)
          
      
    

  def active_node_select(self, OBJECT, MANIPULATION_MODE):
    if OBJECT.number_of_contacts > 0:
      self.select(OBJECT)
      return
    while OBJECT.get_parent() != None:
      self.select(OBJECT)
      return
    self.select(OBJECT)

  def identify_parent(self, OBJECT1, OBJECT2):
    if OBJECT1.get_parent() ==  OBJECT2:
      return OBJECT2
    elif OBJECT2.get_parent() ==  OBJECT1:
      return OBJECT1
    else:
      return None

