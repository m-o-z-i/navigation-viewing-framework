#!/usr/bin/python

## @file
# Contains classes ManipulationManager and RayPointer.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon
import math

# import framework libraries
from Intersection import *

## Class for moving the ray with the mouse
## Still manipulation with the mouse

# We just get relativ values of the mouse position.
# So we have to calculate where the mouse goes.

class MouseMovement(avango.script.Script):

  sf_mouse_x = avango.SFFloat()
  sf_mouse_y = avango.SFFloat()
  sf_output_mat = avango.gua.SFMatrix4()

  def __init__(self):
    self.super(MouseMovement).__init__()
    self.plane_mat = None
    self.mouse_mat = None

  def my_constructor(self, MOUSE, PLANE_MATRIX):
    self.sf_mouse_x.connect_from(MOUSE.Value0)
    self.sf_mouse_y.connect_from(MOUSE.Value1)
    
    self.mouse = MOUSE
    self.plane_mat = avango.gua.make_trans_mat(0,1.18,3)
    print "plane:"
    print self.plane_mat.get_translate()
    self.mouse_mat = avango.gua.make_trans_mat(0,1.18,0.5)
    
    self.sf_output_mat.value = avango.gua.make_trans_mat(0,1.18,0.5)

    self._point2_old = avango.gua.Vec3(0,1,0)
   
    #self._point2_old = avango.gua.Vec3(self.sf_mouse_x.value, self.sf_mouse_y.value,self.sf_mouse_x.value*self.sf_mouse_y.value) 

    self.old_axis = avango.gua.Vec3(0,0,0)
    self.old_vec3 = avango.gua.Vec3(0,0,0)

  #callbacks:
  @field_has_changed(sf_mouse_x)
  def sf_mouse_x_changed(self):
    
    if self.plane_mat != None and self.mouse_mat != None: 

      _mat = self.mouse_mat * avango.gua.make_trans_mat((0.01)*self.sf_mouse_x.value, (-0.03)*self.sf_mouse_y.value, 0)

      
      #if _mat.get_translate().x < 3 and _mat.get_translate().x > -3:
      #  self.mouse_mat = self.mouse_mat * avango.gua.make_trans_mat((0.01)*self.sf_mouse_x.value,0, 0)

      #if _mat.get_translate().y < 3 and _mat.get_translate().y > -3:
      #  self.mouse_mat = self.mouse_mat * avango.gua.make_trans_mat(0, (-0.03)*self.sf_mouse_y.value, 0)

      self.mouse_mat = _mat
      _point1 = self.plane_mat.get_translate()
      _point2 = self.mouse_mat.get_translate()
      
      _vec1 = _point1 - self._point2_old
      _vec2 = _point1 - _point2
      _vec3 = _vec1.cross(_vec2)

   
      _axis = _vec3
      if _vec1.x == _vec2.x and _vec1.y == _vec2.y and _vec1.z == _vec2.z :
        _axis = self.old_axis

      #self.old_vec3 = _vec3
      #_vec3.normalize()
      #_axis = avango.gua.Vec3(0,1,0).cross(_vec3)
      #if _vec3.x == 0 and _vec3.y != 0 and _vec3.z == 0 :
      #  _axis = self.old_axis

      
      self.old_axis = _axis
      _axis.normalize()
      _angle = math.degrees(math.acos( round(_vec1.dot( _vec2) / (_vec1.length() * _vec2.length()),6)))

      _rotation_mat = avango.gua.make_rot_mat(_angle, _axis)

      self.sf_output_mat.value =  self.sf_output_mat.value * _rotation_mat
      
      self._point2_old = _point2
        
