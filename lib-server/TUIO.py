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

        # multi-touch gestures to be registered
        self.gestures = []

        # start driver
        #_devnull = open('/dev/null', 'w')
        #subprocess.Popen(["sudo", "/usr/sbin/citmuto03drv"], stderr = _devnull, stdout = _devnull)

        # append 20 touch cursors
        for i in range(0, 20):
            cursor = TUIOCursor(CursorID = i)
            self.Cursors.value.append(cursor)
            self.MovementChanged.connect_from(cursor.IsMoving)
            self.PosChanged.connect_from(cursor.PosX)


        self.activePoints = {}
        #self.DirectionAngle = 0 
        #self.distances = []

        # screen dimensions
        # TODO: don't hardcode this
        self.screenWidth = 1920 * 2
        self.screenHeight = 1080 * 2

        # register gestures
        # TODO: do this somewhere else
        self.registerGesture(DragGesture())
        self.registerGesture(PinchGesture())
        self.registerGesture(RotationGesture())

    def my_constructor(self, no_tracking_mat):
        self.init_station_tracking(None, no_tracking_mat)


    ## Creates a representation of the device in the virutal world.
    # @param PLATFORM_NODE The platform node to which the avatar should be appended to.
    # @param PLATFORM_ID The platform id used for setting the group name correctly.
    def create_device_avatar(self, PLATFORM_NODE, PLATFORM_ID):
        pass

        #_loader = avango.gua.nodes.TriMeshLoader()

        ## @var avatar_transform
        # Scenegraph transform node for the dekstop user's table.
        #self.avatar_transform = avango.gua.nodes.TransformNode(Name = 'avatar_transform')
        #self.avatar_transform.Transform.connect_from(self.tracking_reader.sf_avatar_body_mat)
        #PLATFORM_NODE.Children.value.append(self.avatar_transform)

        ## @var device_avatar
        # Scenegraph node representing the geometry and transformation of the device avatar.
        #self.device_avatar = _loader.create_geometry_from_file('device_avatar',
        #                                                       'data/objects/table/table.obj',
        #                                                       'data/materials/Stones.gmd',
        #                                                       avango.gua.LoaderFlags.LOAD_MATERIALS)
        #self.device_avatar.Transform.value = avango.gua.make_trans_mat(-0.8, 0.2, 0.8) * avango.gua.make_scale_mat(0.2, 0.5, 0.5)
        #self.avatar_transform.Children.value.append(self.device_avatar)
        #self.device_avatar.GroupNames.value = ['avatar_group_' + str(PLATFORM_ID)]
    

    def evaluate(self):
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

    def processGesture(self, activePoints, mfDof):
        """
        Process gesture. This method needs to be implemented in subclasses.

        @abstract
        @param activePoints: a list of currently active points
        @param mfDof: reference to multi-DoF field for navigation : [trans_x, trans_y, trans_z, pitch, head, roll, scale]
        @return True if gesture was executed, otherwise False
        """
        pass

    def linearlyInterpolate(self, point1, point2, weight = .5):
        """
        Linearly interpolate between two points given as (x, y) tuple.

        @param point1: first point
        @param point2: second point
        @param weight: weight for the interpolation
        @returns tuple (x, y) of interpolated coordinates
        """
        x = (1 - weight) * point1[0] + weight * point2[0]
        y = (1 - weight) * point1[1] + weight * point2[1]
        return (x, y)


class DragGesture(MultiTouchGesture):
    def __init__(self):
        # last position for relative panning
        self.lastPos = None

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

        #relPos = (point.PosX.value - self.lastPos[0], point.PosY.value - self.lastPos[1])

        relPos = (mappedPosX - mappedLastPosX, mappedPosY - mappedLastPosY)

        # pan in negative direction and boost calculated values by some
        # arbitrary number
        newPosX = -relPos[0] * 7
        newPosY = -relPos[1] * 7

        # cap values
        if .3 < abs(newPosX):
            newPosX = math.copysign(.3, newPosX)
        if .3 < abs(newPosY):
            newPosY = math.copysign(.3, newPosY)

        mfDof.value[0] += newPosX
        mfDof.value[2] += newPosY

        self.lastPos = (point.PosX.value, point.PosY.value)

        #print(mfDof.value[0], mfDof.value[2], relPos[0], relPos[1])

        return True

class PinchGesture(MultiTouchGesture):
    def __init__(self):
        self.distances = []


    def processGesture(self, activePoints, mfDof):
        if len(activePoints) != 2:
            self.distances = []
            return False
        elif not activePoints[0].IsMoving.value and not activePoints[0].IsMoving:
            return False

        # DirectionAngle = acos (DirectionOld[0] scalar TouchDirection / |1 * 1|)
        vec1 = avango.gua.Vec2(activePoints[0].PosX.value, activePoints[0].PosY.value)
        vec2 = avango.gua.Vec2(activePoints[1].PosX.value, activePoints[1].PosY.value)
        distance = vec1 - vec2
        #self.DirectionAngle = math.acos(activePoints[0].MovementVector.value.dot(activePoints[1].MovementVector.value))

        #if len(self.distances) > 1 and abs(self.distances[-1].length() - distance.length()) < .005:
        #    self.distances = []
        #    return False

        #save old distance
        if 2 == len(self.distances):
            self.distances.append(distance)
            self.distances.pop(0)
        else:
            self.distances.append(distance)

        # from radians to degrees
        #self.DirectionAngle = self.DirectionAngle * (180 / math.pi)

        #if 90 < self.DirectionAngle:
        #    movement = activePoints[0].MotionSpeed.value + activePoints[1].MotionSpeed.value
#
        #    if abs(self.distances[0].length()) < abs(self.distances[-1].length()):
        #        mfDof.value[6] += -movement * 2
        #    else:
        #        mfDof.value[6] += movement * 2
        
        movement = activePoints[0].MotionSpeed.value + activePoints[1].MotionSpeed.value

        zoom  = self.distances[0].length() > self.distances[-1].length()
        pinch = self.distances[0].length() < self.distances[-1].length()

        if zoom:
            mfDof.value[6] = distance.length() * 3
        elif pinch:
            mfDof.value[6] = -distance.length() * 3

        return True


class RotationGesture(MultiTouchGesture):
    def __init__(self):
        self.distances = []


    def processGesture(self, activePoints, mfDof):
        if len(activePoints) != 2:
            self.distances = []
            return False
        elif not activePoints[0].IsMoving.value and not activePoints[0].IsMoving:
            return False

        # DirectionAngle = acos (DirectionOld[0] scalar TouchDirection / |1 * 1|)
        vec1 = avango.gua.Vec2(activePoints[0].PosX.value, activePoints[0].PosY.value)
        vec2 = avango.gua.Vec2(activePoints[1].PosX.value, activePoints[1].PosY.value)
        distance = vec1 - vec2
        #self.DirectionAngle = math.acos(activePoints[0].MovementVector.value.dot(activePoints[1].MovementVector.value))

        #if len(self.distances) > 1 and abs(self.distances[-1].length() - distance.length()) < .005:
        #    self.distances = []
        #    return False

        #save old distance
        if 2 == len(self.distances):
            self.distances.append(distance)
            self.distances.pop(0)
        else:
            self.distances.append(distance)

        # from radians to degrees
        #self.DirectionAngle = self.DirectionAngle * (180 / math.pi)

        #if 90 < self.DirectionAngle:
        #    movement = activePoints[0].MotionSpeed.value + activePoints[1].MotionSpeed.value
#
        #    if abs(self.distances[0].length()) < abs(self.distances[-1].length()):
        #        mfDof.value[6] += -movement * 2
        #    else:
        #        mfDof.value[6] += movement * 2
        
        #movement = activePoints[0].MotionSpeed.value + activePoints[1].MotionSpeed.value

        #zoom  = self.distances[0].length() > self.distances[-1].length()
        #pinch = self.distances[0].length() < self.distances[-1].length()

        #if zoom:
        #    mfDof.value[6] = distance.length() * 3
        #elif pinch:
        #    mfDof.value[6] = -distance.length() * 3

        #mfDof[5] = math.atan2(self.distances[0].y - self.distances[-1].y, 

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
    IsTap = avango.SFBool()
    IsTouched = avango.SFBool()
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

        self.touchPosition = avango.gua.Vec2(0,0)


    @field_has_changed(CursorID)
    def set_station(self):
        """
        Set station ID.
        """
        self.device_sensor.Station.value = "gua-finger{}".format(self.CursorID.value)

    def evaluate(self):
        # evaluate simple gestures
        self.IsTap.value = (self.PosX.value != -1 and not self.IsMoving.value)
        self.IsTouched.value = (self.PosX.value != -1 and self.State.value != 4.0)
        
        if self.IsTouched:
            self.touchPosition = avango.gua.Vec2(self.PosX.value, self.PosY.value)
        #print("Event!")

        # evaluate movement vector over 10 frames
        if 0 == self.frameCounter:
            self.firstPos.x = self.PosX.value
            self.firstPos.y = self.PosY.value
            self.frameCounter += 1
        elif 9 == self.frameCounter:
            vec = avango.gua.Vec2(self.PosX.value - self.firstPos.x, self.PosY.value - self.firstPos.y)
            vec.normalize()
            self.MovementVector.value = vec
            self.firstPos = avango.gua.Vec2(0, 0)
            self.frameCounter = 0
        else:
            self.frameCounter += 1

