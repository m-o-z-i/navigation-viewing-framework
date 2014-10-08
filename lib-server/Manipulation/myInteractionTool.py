#!/usr/bin/python

## @file
# Contains class myInteractionTool

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

from Input import *
from StateHandler import *
from objectSelectionHandler import *
from ObjectContact import *



class myInteractionTool(avango.script.Script):

  ### init fields
  sf_button1 = avango.SFBool()
  sf_button2 = avango.SFBool()
  sf_button3 = avango.SFBool()

  init_flag = False
  sf_output_mat = avango.gua.SFMatrix4()
  sf_output_point = avango.gua.SFVec3()
  
  ### default constructor
  def __init__(self):
    self.super(myInteractionTool).__init__() # call base class constructor

  def my_constructor(self, RAY, SF_MATRIX, POINTER_DEVICE_STATION, DISTANCE_SELECTOR):
    ### init sensors
    self.button_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    #self.button_sensor = POINTER_DEVICE_STATION
    self.button_sensor.Station.value = POINTER_DEVICE_STATION

    self.sf_button1.connect_from(self.button_sensor.Button0)
    self.sf_button2.connect_from(self.button_sensor.Button1)
    self.sf_button3.connect_from(self.button_sensor.Button2)     

    self.ray = RAY
    self.distance_selector = DISTANCE_SELECTOR

    self.selection_handler = objectSelectionHandler()     
    self.dragging_offset = None
    self.contact = None

    self.selection_frame_trigger = avango.script.nodes.Update(Callback = self.selection_frame_callback, Active = False)

    ### init selection state machine
    self.selection = StateHandler()
    self.selection.addState("idle")
    self.selection.addState("object", operation = self.objectSelection_operation, inTransition = self.objectSelection_inTransition, outTransition = self.objectSelection_outTransition)
    self.selection.addState("edge", operation = self.edgeSelection_operation, inTransition = self.edgeSelection_inTransition, outTransition = self.edgeSelection_outTransition)
    self.selection.setState("idle") # set initial state

    self.init_flag = True

  ### functions  

  # init object selection state functions
  def objectSelection_operation(self):
    #print "selecting objects ..."
    #print self.sf_output_mat.value.get_translate()
    self.sf_output_mat.value = self.ray.ray_transform.WorldTransform.value# * self.dragging_offset
    #_offset_point = self.contact.object.get_world_transform() * self.point
   
    if len(self.ray.mf_pointer_pick_result.value) > 0 and self.ray.mf_pointer_pick_result.value[0].Object.value.has_field("InteractiveObject") == True:
      _pick_result = self.ray.mf_pointer_pick_result.value[0]
      _point = _pick_result.Position.value # intersection point in object coordinate system
      _node = _pick_result.Object.value
      _point = _node.WorldTransform.value * _point
      
      self.sf_output_point.value = avango.gua.Vec3(_point.x,_point.y,_point.z)

    self.contact.object.active_manipulator.manipulate()

  def objectSelection_inTransition(self):
    print "enter object selection"
    
    _pick_result = self.ray.mf_pointer_pick_result.value[0] # get first intersection target
    _point = _pick_result.Position.value # intersection point in object coordinate system
    _node = _pick_result.Object.value
    _object = _node.InteractiveObject.value
    
    _point = _node.WorldTransform.value * _point # transform point into world coordinates
    self.sf_output_point.value = avango.gua.Vec3(_point.x,_point.y,_point.z)
    

    self.dragging_offset = avango.gua.make_inverse_mat(self.ray.ray_transform.WorldTransform.value) * _object.get_world_transform()
    self.sf_output_mat.value = self.ray.ray_transform.WorldTransform.value# * self.dragging_offset  

    self.contact = ObjectContact()
    self.contact.output_mat.connect_from(self.sf_output_mat)
    self.contact.my_constructor(_object, self.sf_output_mat, self.sf_output_point, "MatrixManipulator", self.selection_handler)
    self.selection_handler.subgroup_select(_object, "MatrixManipulator", self.contact)
    self.distance_selector.add_candidate(self.contact)

    self.selection_frame_trigger.Active.value = True # activate selection frame callaback


  def objectSelection_outTransition(self):
    print "exit object selection"
    self.selection_frame_trigger.Active.value = False # deactivate selection frame callaback
    self.selection_handler.deselect(self.contact)
    for _candidate in self.distance_selector.candidates:
      if _candidate == self.contact:
        self.distance_selector.remove_candidate(self.contact)
 
  # init edge selection state functions
  def edgeSelection_operation(self):
    print "selecting edges ..."


  def edgeSelection_inTransition(self):
    print "enter edge selection"
    self.selection_frame_trigger.Active.value = True # activate selection frame callaback


  def edgeSelection_outTransition(self):
    print "exit edge selection"
    self.selection_frame_trigger.Active.value = False # deactivate selection frame callaback


 
  def selection_frame_callback(self):
    self.selection.run()
  

  ### callbacks
  @field_has_changed(sf_button1)
  def sf_button1_changed(self):
  
    if self.init_flag == True:
    
      if self.sf_button1.value == True: # button pressed
        if len(self.ray.mf_pointer_pick_result.value) > 0 and self.ray.mf_pointer_pick_result.value[0].Object.value.has_field("InteractiveObject") == True:
          print "!"
          self.selection.setState("object")

      else: # button released
        self.selection.setState("idle")        
    

  @field_has_changed(sf_button2)
  def sf_button2_changed(self):
  
    if self.init_flag == True:
    
      if self.sf_button2.value == True: # button pressed
        self.selection.nextState()


  @field_has_changed(sf_button3)
  def sf_button3_changed(self):    

    if self.init_flag == True:

      if self.sf_button3.value == True: # button pressed
        self.selection.setState("idle")
