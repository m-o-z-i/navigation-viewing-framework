#!/usr/bin/python

## @file
# Contains classes SceneObject and InteractiveObject.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Object import *
from StateHandler import *
from Intersection import *
import math
import time

class Manipulator:
    
  def __init__(self, NAME, OBJECT):
    self.name = NAME
    self.object = OBJECT
    self.inputs = []
    self.number_of_inputs = 0
    self.is_available = True
    self.activation_time = 0
    

  def is_available(self):
    return self.is_available

  def set_object(OBJECT):
    self.object = OBJECT


  def get_name(self):
    return self.name

class MatrixManipulator(Manipulator):

  def __init__(self, NAME, OBJECT):
    Manipulator.__init__(self, NAME, OBJECT)

    self.object_mat = self.object.get_world_transform()

    self.manipulation = StateHandler()
    self.manipulation.addState("idle")
    self.manipulation.addState("OneHandedManipulation", operation = self.OneHanded_operation, inTransition = self.OneHanded_inTransition, outTransition = self.OneHanded_outTransition)
    self.manipulation.addState("TwoHandedManipulation", operation = self.TwoHanded_operation, inTransition = self.TwoHanded_inTransition, outTransition = None)
    self.manipulation.setState("idle") # set initial state


    #self.manipulation_frame_trigger = avango.script.nodes.Update(Callback = self.manipulation_frame_callback, Active = False)

  def OneHanded_inTransition(self):
    self.object_mat = self.object.get_world_transform()
    self.dragging_offset = avango.gua.make_inverse_mat(self.inputs[0].output_mat.value) * self.object_mat
    self.activation_time = time.time()
    #print "start one-handed manipulation"
    #self.manipulation_frame_trigger.Active.value = True

  def OneHanded_outTransition(self):
    print self.object.parent_object
    print self.object.child_objects
    print "..."
    
  def OneHanded_operation(self):
    
    _time = time.time() - self.activation_time
    if _time > 0.5 and len(self.object.child_objects) > 0:
      self.is_available = False

    ray_matrix = self.inputs[0].output_mat.value

    _target_mat  = ray_matrix  * self.dragging_offset

    if self.object.parent_object != None:
      _target_mat = avango.gua.make_inverse_mat(self.object.parent_object.get_world_transform()) * _target_mat
    self.object.set_transform(_target_mat)
    
  def TwoHanded_inTransition(self):

    self.object_mat  = self.object.get_world_transform()
    

    self.dragging_offset = avango.gua.make_inverse_mat(self.inputs[0].output_mat.value) * self.object_mat

    self.transform = avango.gua.make_identity_mat()

    self._init_point1 = avango.gua.make_inverse_mat(self.inputs[0].output_mat.value) * self.inputs[0].intersection_point.value
    self._init_point1 = avango.gua.Vec3(self._init_point1.x,self._init_point1.y,self._init_point1.z)

    self._init_point2 = avango.gua.make_inverse_mat(self.inputs[1].output_mat.value) * self.inputs[1].intersection_point.value
    self._init_point2 = avango.gua.Vec3(self._init_point2.x,self._init_point2.y,self._init_point2.z)

    #self._point1_old = self.inputs[0].output_mat.value.get_translate()
    #self._point2_old = self.inputs[1].output_mat.value.get_translate()

    self._point1_old = self.inputs[0].intersection_point.value
    self._point2_old = self.inputs[1].intersection_point.value


    #print "..."
    #print self._point1_old
    #print self._point2_old
    #print "..."

    
    self.translation_offset =  avango.gua.make_trans_mat(self._init_point1) * self.object_mat
    #self.translation_offset =  avango.gua.make_inverse_mat(avango.gua.make_trans_mat(self._point1)) * self.object_mat
    
    #self.object.set_world_transform(self.translation_offset)

  def TwoHanded_outTransition(self):
    self.transform = avango.gua.make_identity_mat()

  def TwoHanded_operation(self):
    
    
    self._point1 =  self.inputs[0].output_mat.value * self._init_point1
    self._point1 = avango.gua.Vec3(self._point1.x,self._point1.y,self._point1.z)

    self._point2 = self.inputs[1].output_mat.value * self._init_point2 
    self._point2 = avango.gua.Vec3(self._point2.x,self._point2.y,self._point2.z)

    
    
    #print self._point1
    #print self._point2
    _transform_mat = self.transform
    
    # Calculate rotation

    _vec1 = self._point1_old - self._point2_old
    _vec2 = self._point1 - self._point2
    
    _vec1.normalize()
    _vec2.normalize()
    
    _axis  = _vec1.cross( _vec2)
    #print "vektor eins " , _vec1
    #print "vektor zweitausend ", _vec2
    #print _vec1.dot( _vec2)
    _angle  = round(math.degrees(math.acos(round(_vec1.dot( _vec2), 4))),4)
    

    # Calculate scaling factor

    _distance1 = (self._point1_old - self._point2_old).length()
    _distance2 = (self._point1 - self._point2).length()


    _factor = (_distance2 / _distance1)
    #print _distance1
    #print _distance2
    #print _factor
    _object_scale = _transform_mat.get_scale()
    
   
    _object_pos =  ((self._point1_old - self._point1) + (self._point2_old - self._point2))/2
    #_object_pos =  (self._point1 + self._point2)/2
    
    _object_quat = _transform_mat.get_rotate_scale_corrected()
    
    _target_scale = avango.gua.make_scale_mat(_object_scale.x*_factor,  _object_scale.y*_factor, _object_scale.z*_factor)
   
    # Calculate Target Matrix
    self.transform =  avango.gua.make_trans_mat(_object_pos) * avango.gua.make_rot_mat(_angle, _axis) * avango.gua.make_rot_mat(_object_quat) * _target_scale
    #print _target_mat
        
    # Save old Object points
    self._point1_old = self._point1
    self._point2_old = self._point2
    
    # Set new Object Matrix
    
    self.object.set_world_transform(self.object_mat * self.transform)
    
    


  def add_input(self, INPUT):
    if self.is_available:
      self.inputs.append(INPUT)
      if self.number_of_inputs == 0:
        self.manipulation.setState("OneHandedManipulation")
        self.number_of_inputs += 1
        return True

      elif self.number_of_inputs == 1:
        self.manipulation.setState("TwoHandedManipulation")
        self.number_of_inputs += 1
        self.is_available = False
        return True

    else:
      print self.number_of_inputs
      return False

  def remove_input(self, INPUT):

    self.inputs.remove(INPUT)
    print "WEG MIT DEM INPUT"
    if self.number_of_inputs == 2:
      self.manipulation.setState("OneHandedManipulation")
      self.is_available = True

    elif self.number_of_inputs == 1:
      self.manipulation.setState("idle")
      self.is_available = True

    self.number_of_inputs -= 1
    print self.number_of_inputs
  def manipulate(self):
    self.manipulation.run()

