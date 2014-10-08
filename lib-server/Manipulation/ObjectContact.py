#!/usr/bin/python


import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

class ObjectContact(avango.script.Script):
  ### default constructor
  output_mat = avango.gua.SFMatrix4()
  
  intersection_point = avango.gua.SFVec3()

  def __init__(self):
    self.super(ObjectContact).__init__() # call base class constructor

  def my_constructor(self, OBJECT, SF_MATRIX, SF_POINT, MANIPULATOR, SELECTION_HANDLER):
    self.object = OBJECT
    self.output_mat.connect_from(SF_MATRIX)
    self.intersection_point.connect_from(SF_POINT)
    self.selection_handler = SELECTION_HANDLER
    self.manipulator = MANIPULATOR
    #print "punkt:"
    #print self.output_mat.value.get_translate()

  def set_object(self, OBJECT):
    self.object = OBJECT

  def update_selection(self):
    self.selection_handler.deselect(self)
    self.selection_handler.select(self.object, self)

  def get_object(self):
    return self.object


