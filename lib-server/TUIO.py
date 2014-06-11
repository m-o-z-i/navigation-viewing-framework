#!/bin/python

import avango
import avango.daemon
import avango.script
from avango.script import field_has_changed
import subprocess

class TUIOManager(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        """
        Override __new__() method to make this class a singleton.
        """
        if not cls._instance:
            cls._instance = super(TUIOManager, cls).__new__(cls, *args, **kwargs)
            return cls._instance
    
    def __init__(self):
        """
        Initialize driver and touch cursors
        """
        # start driver
        #_devnull = open('/dev/null', 'w')
        #subprocess.Popen(["sudo", "/usr/sbin/citmuto03drv"], stderr = _devnull, stdout = _devnull)

        self.multi_touch = MultiTouchGesture()

        # append 20 touch cursors
        for i in range(0, 20):
            cursor = TUIOCursor(CursorID = i)
            self.multi_touch.Cursors.value.append(cursor)
            self.multi_touch.MovementChanged.connect_from(cursor.IsMoving)
            self.multi_touch.PosChanged.connect_from(cursor.PosX)

class MultiTouchGesture(avango.script.Script):
    Cursors = avango.MFContainer()
    MovementChanged = avango.SFBool()
    PosChanged = avango.SFFloat()

    def evaluate(self):
        self.processGesture()


    def processGesture(self):
        """
        Detect and process multi touch gestures.
        """
        taps = []
        # detect taps
        for i in self.Cursors.value:
            if i.IsTap.value:
                taps.append(i)



class TUIOCursor(avango.script.Script):
    PosX = avango.SFFloat()
    PosY = avango.SFFloat()
    SpeedX = avango.SFFloat()
    SpeedY = avango.SFFloat()
    MotionSpeed = avango.SFFloat()
    MotionAcceleration = avango.SFFloat()
    IsMoving = avango.SFBool()
    State = avango.SFFloat()
    SessionID = avango.SFFloat()
    CursorID = avango.SFInt()
    IsTap = avango.SFBool()
    MovementVector = avango.gua.SFVec2()

    def __init__(self):
        self.super(TUIOCursor).__init__()

        # initialize fields
        self.PosX.value      = -1.0
        self.PosY.value      = -1.0
        self.State.value     = 4.0
        self.SessionID.value = -1.0

        self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.PosX.connect_from(self.device_sensor.Value0)
        self.PosY.connect_from(self.device_sensor.Value1)
        self.SpeedX.connect_from(self.device_sensor.Value2)
        self.SpeedY.connect_from(self.device_sensor.Value3)
        self.MotionSpeed.connect_from(self.device_sensor.Value4)
        self.MotionAcceleration.connect_from(self.device_sensor.Value5)
        self.IsMoving.connect_from(self.device_sensor.Value6)
        self.State.connect_from(self.device_sensor.Value7)
        self.SessionID.connect_from(self.device_sensor.Value8)

        # temporary properties for calculating movement vectors
        self.frameCounter = 0
        self.firstPos = avango.gua.Vec2()
        self.MovementVector.value = avango.gua.Vec2(0, 0)

    @field_has_changed(CursorID)
    def set_station(self):
        """
        Set station ID.
        """
        self.device_sensor.Station.value = "gua-finger{}".format(self.CursorID.value)

    def evaluate(self):
        # evaluate simple gestures
        self.IsTap.value = (self.PosX.value != -1 and not self.IsMoving.value)

        # evaluate movement vector over 10 frames
        if 0 == self.frameCounter:
            self.firstPos.x = self.PosX.value
            self.firstPos.y = self.PosY.value
            self.frameCounter += 1
        elif 9 == self.frameCounter:
            self.MovementVector.value = avango.gua.Vec2(self.PosX.value - self.firstPos.x, self.PosY.value - self.firstPos.y)
            self.firstPos = avango.gua.Vec2(0, 0)
            self.frameCounter = 0
        else:
            self.frameCounter += 1

