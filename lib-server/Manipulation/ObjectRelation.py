#!/usr/bin/python


import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import time

from UIGeoFeature import *
from ObjectContact import *
from Object import *
import math

class ObjectRelation(avango.script.Script):
  #
  sf_point_1 = avango.gua.SFVec3()
  sf_point_2 = avango.gua.SFVec3()

  sf_number_of_contacts1 = avango.SFInt()
  sf_number_of_contacts2 = avango.SFInt()

  def __init__(self):
    self.super(ObjectRelation).__init__()
    self.frame_skip = True
    self.frame_skip2 = True
    self.object_rotation = avango.gua.make_identity_mat()

 # call base class constructor
  def my_constructor(self, UI_EDGE, OBJECT_CONTACT1, OBJECT_CONTACT2, DISTANCE_SELECTOR):
    self.object_contact_1 = OBJECT_CONTACT1
    self.object_contact_2 = OBJECT_CONTACT2
    self.edge = UI_EDGE
    self.distance_selector = DISTANCE_SELECTOR

    self.sf_point_1.connect_from(OBJECT_CONTACT1.intersection_point)
    self.sf_point_2.connect_from(OBJECT_CONTACT2.intersection_point)

    self.sf_number_of_contacts1.connect_from(OBJECT_CONTACT1.object.sf_number_of_contacts)
    self.sf_number_of_contacts2.connect_from(OBJECT_CONTACT2.object.sf_number_of_contacts)

    self.point1_old = avango.gua.Vec3(0,1,0)
    self.point2_old = self.sf_point_1.value.cross(self.sf_point_2.value)
  
    self.connection_bool = True
    

    self.update_transform()

  def update_transform(self):
    
    if self.frame_skip == False and self.frame_skip2 == False:
      _point1 = self.sf_point_1.value
      _point2 = self.sf_point_2.value

      _vec1 = avango.gua.Vec3(0.0,1.0,0.0)
      _vec2 = _point1 - _point2

      _distance = _vec2.length()
      
      _vec1.normalize()
      _vec2.normalize()

      _axis  = _vec1.cross(_vec2)
      
      _angle  = math.degrees(math.acos(round(_vec1.dot( _vec2), 6)))

      _object_rotation_mat = avango.gua.make_rot_mat(_angle, _axis)
      
      _object_pos = (_point1 + _point2) * 0.5
      
      _mat = avango.gua.make_trans_mat(_object_pos) * _object_rotation_mat * avango.gua.make_scale_mat(0.01, _distance, 0.01)
      self.edge.set_transform(_mat)
      
    elif self.frame_skip == True and self.frame_skip2 == True:
      self.frame_skip2 = False
    else:
      self.frame_skip = False

  def group_objects(self, OBJECT_CONTACT1, OBJECT_CONTACT2):
    OBJECT1 = OBJECT_CONTACT1.get_object()
    OBJECT2 = OBJECT_CONTACT2.get_object()

   

    if OBJECT2.parent_object != None:    
      OBJECT2.parent_object.remove_child(OBJECT2)
     
    else:
      self.distance_selector.net_trans_node.distribute_object(OBJECT1.scene_root)
      OBJECT2.scene_root.Children.value.remove(OBJECT2.get_node())

    if len(OBJECT1.child_objects) > 0:
      OBJECT1.add_child(OBJECT2)

    else:
      _group = Object()
      _group.my_constructor(OBJECT1.scene, avango.gua.nodes.TransformNode(), avango.gua.make_identity_mat(), None, OBJECT1.scene_root, ["MatrixManipulator"], [])
      self.distance_selector.net_trans_node.distribute_object(OBJECT1.scene_root)
      OBJECT1.scene_root.Children.value.remove(OBJECT1.get_node())
      _group.add_child(OBJECT1)
      self.distance_selector.net_trans_node.distribute_object(OBJECT1.scene_root)
      _group.add_child(OBJECT2)
      self.distance_selector.net_trans_node.distribute_object(OBJECT1.scene_root)

      OBJECT_CONTACT1.set_object(_group)
      OBJECT_CONTACT1.update_selection()

      self.distance_selector.net_trans_node.distribute_object(OBJECT1.scene_root)
      self.distance_selector.net_trans_node.distribute_object(OBJECT1.get_node())
      self.distance_selector.net_trans_node.distribute_object(OBJECT2.get_node())
      self.distance_selector.net_trans_node.distribute_object(_group.get_node())

  def degroup_objects(self, OBJECT_CONTACT1, OBJECT_CONTACT2):
    OBJECT1 = OBJECT_CONTACT1.get_object()
    OBJECT2 = OBJECT_CONTACT2.get_object()
   
    OBJECT1.remove_child(OBJECT2)
    OBJECT2.scene_root.Children.value.append(OBJECT2.get_node())

    
    
    if len(OBJECT1.child_objects) == 1 and len(OBJECT1.child_objects[0].child_objects) == 0:
      _child = OBJECT1.child_objects[0]
      OBJECT1.remove_child(_child)
      OBJECT1.scene_root.Children.value.append(_child.get_node())
      OBJECT1.scene_root.Children.value.remove(OBJECT1.get_node())

      OBJECT_CONTACT1.set_object(_child)
      OBJECT_CONTACT1.update_selection()

  def delete(self):
    self.edge.delete()
    
  
  # callbacks
  @field_has_changed(sf_point_1)
  def sf_point_1_changed(self):
    self.update_transform()
  
  @field_has_changed(sf_point_2)
  def sf_point_2_changed(self):
    self.update_transform()

  @field_has_changed(sf_number_of_contacts1)
  def sf_number_of_contacts1_changed(self):
    if self.sf_number_of_contacts1.value == 0 and self.connection_bool == True:
      self.distance_selector.add_candidate(self.object_contact_2)
      self.connection_bool = False

      if self.object_contact_1.object.parent_object == self.object_contact_2.object:
       
        self.degroup_objects(self.object_contact_2, self.object_contact_1)

      elif self.object_contact_2.object.parent_object == self.object_contact_1.object:
        self.degroup_objects(self.object_contact_1, self.object_contact_2)
      else:
        self.group_objects(self.object_contact_2, self.object_contact_1)
       

      
      self.sf_number_of_contacts1.disconnect_from(self.object_contact_1.object.sf_number_of_contacts)

      self.delete()

  @field_has_changed(sf_number_of_contacts2)
  def sf_number_of_contacts2_changed(self):
    if self.sf_number_of_contacts2.value == 0 and self.connection_bool == True:
      self.distance_selector.add_candidate(self.object_contact_1)
      self.connection_bool = False

      if self.object_contact_1.object.parent_object == self.object_contact_2.object:
       
        self.degroup_objects(self.object_contact_2, self.object_contact_1)

      elif self.object_contact_2.object.parent_object == self.object_contact_1.object:
        self.degroup_objects(self.object_contact_1, self.object_contact_2)
      else:
        self.group_objects(self.object_contact_1, self.object_contact_2)

      
      self.sf_number_of_contacts2.disconnect_from(self.object_contact_2.object.sf_number_of_contacts)

      self.delete()



