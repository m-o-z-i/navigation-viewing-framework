#!/usr/bin/python

## @file
# Contains classes TouchCursor and TouchDevice.

# import avango-guacamole libraries
import avango
import avango.script

class TouchCursor(avango.script.Script):

  CursorID = avango.SFInt();

  PosX = avango.SFFloat()
  PosY = avango.SFFloat()

  SpeedX = avango.SFFloat()
  SpeedY = avango.SFFloat()

  MotionSpeed = avango.SFFloat()
  MotionAcceleration = avango.SFFloat()

  IsMoving = avango.SFBool()
  State = avango.SFInt()

  SessionID = avango.SFInt()

  ## Default constructor.
  def __init__(self):
    self.super(TouchCursor).__init__()

    self.__device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())

    self.PosX.value = -1
    self.PosY.value = -1

    self.always_evaluate(True)

  @field_has_changed(CursorID)
  def set_station(self):
    self.__device_sensor.Station.value = "gua-finger" + str(self.CursorID.value)

  def evaluate(self):

    self.PosX.value = self.__device_sensor.Value0.value
    self.PosY.value = self.__device_sensor.Value1.value

    self.SpeedX.value = self.__device_sensor.Value2.value
    self.SpeedY.value = self.__device_sensor.Value3.value

    self.MotionSpeed.value = self.__device_sensor.Value4.value
    self.MotionAcceleration.value = self.__device_sensor.Value5.value

    self.IsMoving.value = bool(self.__device_sensor.Value6.value)
    self.State.value = int(self.__device_sensor.Value7.value)

    self.SessionID.value = int(self.__device_sensor.Value8.value)


class TouchDevice(avango.script.Script):

  TouchCursors = []
  
  ## Default constructor.
  def __init__(self):
    self.super(TouchDevice).__init__()

    for i in range(0, 20):
      self.TouchCursors.append(TouchCursor(CursorID = i))
