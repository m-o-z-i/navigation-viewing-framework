#!/usr/bin/python

## @file
# Contains classes TrackingReader, TrackingTargetReader and TrackingDefaultReader.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
import avango.daemon
from avango.script import field_has_changed

# import python libraries
# ...
 

## Reads tracking values of a device registered in daemon.
class ClientTrackingTargetReader(avango.script.Script):

  # output field
  ## @var sf_tracking_mat 
  # The absolute matrix read from the tracking system.
  sf_tracking_mat = avango.gua.SFMatrix4()
  sf_tracking_mat.value = avango.gua.make_identity_mat()

  ## Default constructor.
  def __init__(self):
    self.super(ClientTrackingTargetReader).__init__()

  ## Custom constructor
  # @param TARGET_NAME The target name of the tracked object as chosen in daemon.
  def my_constructor(self, TARGET_NAME):
    
    ## @var tracking_sensor
    # A device sensor to capture the tracking values.
    self.tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.tracking_sensor.Station.value = TARGET_NAME

    self.tracking_sensor.TransmitterOffset.value = avango.gua.make_trans_mat(0.0, 0.043, 1.6)
    self.tracking_sensor.ReceiverOffset.value = avango.gua.make_identity_mat()

    self.sf_tracking_mat.connect_from(self.tracking_sensor.Matrix)


  ## Sets the transmitter offset for this tracking reader.
  # @param TRANSMITTER_OFFSET The transmitter offset to be set.
  def set_transmitter_offset(self, TRANSMITTER_OFFSET):
    self.tracking_sensor.TransmitterOffset.value = TRANSMITTER_OFFSET

  ## Sets the receiver offset for this tracking reader.
  # @param RECEIVER_OFFSET The receiver offset to be set.
  def set_receiver_offset(self, RECEIVER_OFFSET):
    self.tracking_sensor.ReceiverOffset.value = RECEIVER_OFFSET

