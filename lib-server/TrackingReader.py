#!/usr/bin/python

## @file
# Contains classes TrackingReader, TrackingTargetReader and TrackingDefaultReader.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
import avango.daemon
from avango.script import field_has_changed

# import framework libraries
import Utilities

# import python libraries
import math

## Base class for a reader of tracking values. Not to be instantiated.
class TrackingReader(avango.script.Script):

  # output field
  ## @var sf_abs_mat 
  # The absolute matrix read from the tracking system.
  sf_abs_mat = avango.gua.SFMatrix4()
  sf_abs_mat.value = avango.gua.make_identity_mat()

  ## @var sf_abs_vec
  # Just the translation vector read from the tracking system.
  sf_abs_vec = avango.gua.SFVec3()
  sf_abs_vec.value = avango.gua.Vec3(0.0, 0.0, 0.0)

  ## @var sf_global_mat
  # Tracking matrix without the consideration of the transmitter offset.
  sf_global_mat = avango.gua.SFMatrix4()
  sf_global_mat.value = avango.gua.make_identity_mat()


## Reads tracking values of a device registered in daemon.
class TrackingTargetReader(TrackingReader):

  # internal field
  ## @var sf_tracking_mat
  # Field containing the tracked values used for evaluation purposes.
  sf_tracking_mat = avango.gua.SFMatrix4()
  sf_tracking_mat.value = avango.gua.make_identity_mat()

  ## Default constructor.
  def __init__(self):
    self.super(TrackingReader).__init__()

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

  ## Called whenever sf_tracking_mat changes.
  @field_has_changed(sf_tracking_mat)
  def sf_tracking_mat_changed(self):
  
    self.sf_abs_mat.value = self.tracking_sensor.Matrix.value
    self.sf_global_mat.value = avango.gua.make_inverse_mat(self.tracking_sensor.TransmitterOffset.value) * self.tracking_sensor.Matrix.value
    self.sf_abs_vec.value = self.sf_abs_mat.value.get_translate()
    _yaw = Utilities.get_yaw(self.sf_abs_mat.value)

  ## Sets the transmitter offset for this tracking reader.
  # @param TRANSMITTER_OFFSET The transmitter offset to be set.
  def set_transmitter_offset(self, TRANSMITTER_OFFSET):
    self.tracking_sensor.TransmitterOffset.value = TRANSMITTER_OFFSET

  ## Sets the receiver offset for this tracking reader.
  # @param RECEIVER_OFFSET The receiver offset to be set.
  def set_receiver_offset(self, RECEIVER_OFFSET):
    self.tracking_sensor.ReceiverOffset.value = RECEIVER_OFFSET


## Supplies constant tracking values if no real tracking is available.
class TrackingDefaultReader(TrackingReader):

  ## Default constructor
  def __init__(self):
    self.super(TrackingReader).__init__()

  ## Sets the transmitter offset for this tracking reader.
  # @param TRANSMITTER_OFFSET The transmitter offset to be set.
  def set_transmitter_offset(self, TRANSMITTER_OFFSET):
    pass

  ## Sets the receiver offset for this tracking reader.
  # @param RECEIVER_OFFSET The receiver offset to be set.
  def set_receiver_offset(self, RECEIVER_OFFSET):
    pass

  ## Sets the constant data to be supplied by this tracking "reader"
  # @param CONSTANT_MATRIX The constant matrix to be supplied as tracking values.
  def set_no_tracking_matrix(self, CONSTANT_MATRIX):
    self.sf_abs_mat.value = CONSTANT_MATRIX
    self.sf_global_mat.value = CONSTANT_MATRIX
    self.sf_abs_vec.value = self.sf_abs_mat.value.get_translate()
