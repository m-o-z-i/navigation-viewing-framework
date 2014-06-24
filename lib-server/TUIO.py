#!/bin/python

from Device import MultiDofDevice

import avango
import avango.daemon
import avango.script
from avango.script import field_has_changed
import subprocess
import math

class TUIODevice(MultiDofDevice):
    Cursors = avango.MFContainer()
    MovementChanged = avango.SFBool()
    PosChanged = avango.SFFloat()

    def __init__(self):
        """
        Initialize driver and touch cursors
        """
        self.super(TUIODevice).__init__()

        # display config
        self.display = None

        # multi-touch gestures to be registered
        self.gestures = []

        # start driver
        #_devnull = open('/dev/null', 'w')
        #subprocess.Popen(["sudo", "/usr/sbin/citmuto03drv"], stderr = _devnull, stdout = _devnull)

        self.activePoints = {}
        
        # append 20 touch cursors
        for i in range(0, 20):
            cursor = TUIOCursor(CursorID = i) 
            self.Cursors.value.append(cursor)
            self.MovementChanged.connect_from(cursor.IsMoving)
            self.PosChanged.connect_from(cursor.PosX)
            self.PosChanged.connect_from(cursor.PosY)


    def my_constructor(self, no_tracking_mat, display):
        self.init_station_tracking(None, no_tracking_mat)

        # register gestures
        # TODO: do this somewhere else
        self.registerGesture(DragGesture(display))
        self.registerGesture(PinchGesture(display))
        self.registerGesture(RotationGesture(display))

    def create_device_avatar(self, PLATFORM_NODE, PLATFORM_ID):
        pass


    @field_has_changed(PosChanged)
    def processChange(self):
        if -1.0 == self.PosChanged.value:
            return

        for touchPoint in self.Cursors.value:
            if touchPoint.IsTouched.value:
                self.activePoints[touchPoint.CursorID.value] = touchPoint
            elif touchPoint.CursorID.value in self.activePoints:
                del self.activePoints[touchPoint.CursorID.value]

        for gesture in self.gestures:
            gesture.processGesture(self.activePoints.values(), self.mf_dof)


    def registerGesture(self, gesture):
        """
        Register an object of type MultiTouchGesture for processing input events.

        @param gesture: MultiTouchGesture object
        """
        if gesture not in self.gestures:
            self.gestures.append(gesture)

    def unregisterGesture(self, gesture):
        """
        Unregister a previously registered MultiTouchGesture.

        @param gesture: the MultiTouchGesture object to unregister
        """
        if gesture in self.gestures:
            self.gestures.remove(gesture)


class MultiTouchGesture(object):
    """
    Base class for multi touch gestures.
    """

    def __init__(self, display):
        self.display = display

    def processGesture(self, activePoints, mfDof):
        """
        Process gesture. This method needs to be implemented in subclasses.

        @abstract
        @param activePoints: a list of currently active points
        @param mfDof: reference to multi-DoF field for navigation : [trans_x, trans_y, trans_z, pitch, head, roll, scale]
        @return True if gesture was executed, otherwise False
        """
        pass


class DragGesture(MultiTouchGesture):
    def __init__(self, display):
        super(DragGesture, self).__init__(display)
        # last position for relative panning
        self.lastPos = None
        self.posSumY = 0

    def processGesture(self, activePoints, mfDof):
        if 1 != len(activePoints):
            self.lastPos = None
            return False
        elif None == self.lastPos:
            self.lastPos = (activePoints[0].PosX.value, activePoints[0].PosY.value)
            return False

        point = activePoints[0]

        # map points from interval [0, 1] to [-1, 1]
        mappedPosX = point.PosX.value * 2 - 1
        mappedPosY = point.PosY.value * 2 - 1
        mappedLastPosX = self.lastPos[0] * 2 - 1
        mappedLastPosY = self.lastPos[1] * 2 - 1

        relDist               = (point.PosX.value - self.lastPos[0], point.PosY.value - self.lastPos[1])
        relDistSizeMapped     = (relDist[0] * self.display.size[0], relDist[1] * self.display.size[1])

        # pan in negative direction and boost calculated values by some
        # arbitrary number
        newPosX = -relDistSizeMapped[0] * 17
        newPosY = -relDistSizeMapped[1] * 17

        # cap values
        if .27 < abs(newPosX):
            newPosX = math.copysign(.27, newPosX)
        if .27 < abs(newPosY):
            newPosY = math.copysign(.27, newPosY)

        mfDof.value[0] += newPosX
        mfDof.value[2] += newPosY
        self.posSumY += newPosY

        self.lastPos = (point.PosX.value, point.PosY.value)

        return True

class PinchGesture(MultiTouchGesture):
    def __init__(self, display):
        super(PinchGesture, self).__init__(display)
        self.distances = []
        self.scaleCenter = None
        self.centerDirection = None

    def _calculateScaleCenter(self, vec1, vec2):
        vec1Trans = vec1 * 2 - 1
        vec2Trans = vec2 * 2 - 1
        distanceTrans = vec2Trans - vec1Trans
        self.scaleCenter = vec1Trans + distanceTrans / 2.0
        self.centerDirection = self.scaleCenter
        self.centerDirection.normalize()


    def processGesture(self, activePoints, mfDof):
        if len(activePoints) != 2:
            self.distances = []
            self.scaleCenter = None
            self.centerDirection = None
            return False

        vec1 = avango.gua.Vec2(activePoints[0].PosX.value, activePoints[0].PosY.value)
        vec2 = avango.gua.Vec2(activePoints[1].PosX.value, activePoints[1].PosY.value)
        distance = vec2 - vec1
        if None == self.scaleCenter:
            self._calculateScaleCenter(vec1, vec2)

        # save old distance
        if 3 == len(self.distances):
            self.distances.append(distance)
            self.distances.pop(0)
        else:
            self.distances.append(distance)
            return False

        relDistance = (self.distances[0].length() - self.distances[-1].length()) / 2

        # return if no significant movement occurred
        #if abs(relDistance) < .0005:
        #    return False

        mfDof.value[6] += relDistance * 16.3
        mfDof.value[0] -= self.centerDirection.x * relDistance * 15 * self.display.size[0]
        mfDof.value[2] -= self.centerDirection.y * relDistance * 15 * self.display.size[1]

        return True


class RotationGesture(MultiTouchGesture):
    def __init__(self, display):
        super(RotationGesture, self).__init__(display)
        self.distances = []


    def processGesture(self, activePoints, mfDof):
        if len(activePoints) != 2:
            self.distances = []
            return False

        vec1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
        vec2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
        distance = vec1 - vec2
        distance = avango.gua.Vec3(distance.x * self.display.size[0], distance.y * self.display.size[1], 0)
        distance.normalize()

        # save old distance
        if 2 == len(self.distances):
            self.distances.append(distance)
            self.distances.pop(0)
        else:
            self.distances.append(distance)

        dotProduct   = self.distances[0].dot(self.distances[-1])
        crossProduct = self.distances[0].cross(self.distances[-1])

        # just take care we have no overflows
        if 1.0 < dotProduct:
            dotProduct = 1.0

        angle = math.copysign(math.acos(dotProduct) * 180 / math.pi, crossProduct.z)
        mfDof.value[4] += angle

        return True

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
    IsTouched = avango.SFBool()
    MovementVector = avango.gua.SFVec2()

    def __init__(self):
        self.super(TUIOCursor).__init__()

        # initialize fields
        self.PosX.value           = -1.0
        self.PosY.value           = -1.0
        self.State.value          =  4.0
        self.SessionID.value      = -1.0
        self.MovementVector.value = avango.gua.Vec2(0, 0)

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
        

    def updateTouched(self):
        """
        Call whenever some touch input data has changed. This method will update self.IsTouched accordingly.
        """
        self.IsTouched.value = (self.PosX.value != -1.0 and self.PosY.value != -1.0)

    @field_has_changed(CursorID)
    def set_station(self):
        """
        Set station ID.
        """
        self.device_sensor.Station.value = "gua-finger{}".format(self.CursorID.value)

    @field_has_changed(PosX)
    def updatePosX(self):
        self.updateTouched()

    @field_has_changed(PosY)
    def updatePosY(self):
        self.updateTouched()

    #@field_has_changed(State)
    #def updateState(self):
    #    self.updateTouched()

