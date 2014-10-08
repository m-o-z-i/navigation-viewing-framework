#!/usr/bin/python

## @file
# Contains classes MouseRayInput und 3DRayInput


# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon


# import framework classes
from MouseMovement import *

####### Class MouseRayInput #########################################################################################
class MouseRayInput :
  
  def __init__(self, PARENT_NODE, TRACKING_STATION):
    self.tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.tracking_sensor.Station.value = TRACKING_STATION
    #self.tracking_sensor.ReceiverOffset.value = avango.gua.make_identity_mat()
    #self.tracking_sensor.TransmitterOffset.value = avango.gua.make_identity_mat()
    
    
    self.mouse_mover = MouseMovement()
    self.mouse_mover.my_constructor(self.tracking_sensor, PARENT_NODE.WorldTransform.value)
    self.pickray_matrix = self.mouse_mover.sf_output_mat



####### Class 3DRayInput ############################################################################################

class RayInput :

  def __init__(self, TRACKING_TRANSMITTER_OFFSET, POINTER_TRACKING_STATION):

    self.tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.tracking_sensor.Station.value = POINTER_TRACKING_STATION
    self.tracking_sensor.ReceiverOffset.value = avango.gua.make_identity_mat()
    self.tracking_sensor.TransmitterOffset.value = TRACKING_TRANSMITTER_OFFSET

    self.pickray_matrix = self.tracking_sensor.Matrix


