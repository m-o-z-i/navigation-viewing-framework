#!/bin/python

from Device import MultiDofDevice

import avango
import avango.gua
import avango.daemon
import avango.script
from avango.script import field_has_changed
import subprocess
import math
import avango.utils

class MultiTouchDevice(avango.script.Script):
    """
    Base class for multi touch devices.
    """

    def __init__(self):
        self.super(MultiTouchDevice).__init__()
        self._sceneGraph = None
        self._display    = None
        self._worldMat   = avango.gua.make_identity_mat()
        self._transMat   = avango.gua.make_identity_mat()
        self._rotMat     = avango.gua.make_identity_mat()
        self._scaleMat   = avango.gua.make_identity_mat()
        
        self._fingerCenterPos = avango.gua.Vec3(0,0,0)
        self._lastPos = None

        self.always_evaluate(True)


    def my_constructor(self, graph, display):
        """
        Initialize multi-touch device.

        @param graph: the scene graph on which to operate
        @param display: the physical display
        """
        self._sceneGraph = graph
        self._display    = display
        self._origMat    = graph.Root.value.Transform.value


    def evaluate(self):
        self.applyTransformations()

    def getDisplay(self):
        return self._display
    
    def getSceneGraph(self):
        return self._sceneGraph

    def setFingerCenterPosition(self, FingerCenterPos, touchDevice):

        point = FingerCenterPos

        # map points from interval [0, 1] to [-0.5, 0.5]
        mappedPosX = point[0] * 1 - 0.5
        mappedPosY = point[2] * 1 - 0.5

        self._fingerCenterPos = avango.gua.Vec3(mappedPosX * touchDevice.getDisplay().size[0], 0.0, mappedPosY * touchDevice.getDisplay().size[1])



    def addLocalTranslation(self, transMat):
        """
        Add local translation.

        @param transMat: the (relative) translation matrix
        """
        self._transMat *= transMat

    def addLocalRotation(self, rotMat):
        """
        Add local rotation.

        @param rotMat: the (relative) rotation matrix
        """
        self._rotMat *= rotMat

    def addLocalScaling(self, scaleMat):
        """
        Add local scaling.

        @param scaleMat: the (relative) scaling matrix
        """
        self._scaleMat *= scaleMat

    def applyTransformations(self):
        """
        Apply calculated world matrix to scene graph.
        Requires the scene graph to have a transform node as root node.
        """

        scenePos = self._sceneGraph["/net/MedievalTown"].Transform.value.get_translate()
        translateDistance = self._fingerCenterPos - scenePos

        TransformMatrix = self._sceneGraph["/net/MedievalTown"].Transform.value

        #transform world-space to object-space
        translateDistance = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * translateDistance
        translateDistance = avango.gua.Vec3(translateDistance.x, translateDistance.y, translateDistance.z)

        TransformMatrix = avango.gua.make_trans_mat(TransformMatrix.get_translate()) * \
                            avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                            avango.gua.make_trans_mat(translateDistance * 1.0) * \
                            self._rotMat * \
                            self._scaleMat * \
                            avango.gua.make_trans_mat(translateDistance * -1.0) * \
                            avango.gua.make_scale_mat(TransformMatrix.get_scale())

        TransformMatrix = self._transMat * TransformMatrix


        self._sceneGraph["/net/MedievalTown"].Transform.value = TransformMatrix #ScenePitotiTest

        #reset all data
        self._transMat   = avango.gua.make_identity_mat()
        self._rotMat     = avango.gua.make_identity_mat()
        self._scaleMat   = avango.gua.make_identity_mat()
        self._fingerCenterPos = avango.gua.Vec3(0,0,0)


class TUIODevice(MultiTouchDevice):
    """
    Multi touch device class to process TUIO input.
    """
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

        self._activePoints = {}


    def my_constructor(self, graph, display):
        self.super(TUIODevice).my_constructor(graph, display)
        
        # append 20 touch cursors
        for i in range(0, 20):
            cursor = TUIOCursor(CursorID = i) 
            self.Cursors.value.append(cursor)
            self.MovementChanged.connect_from(cursor.IsMoving)
            self.PosChanged.connect_from(cursor.PosX)
            self.PosChanged.connect_from(cursor.PosY)

        # register gestures
        # TODO: do this somewhere else
        self.registerGesture(DragGesture())
        self.registerGesture(PinchGesture())
        self.registerGesture(RotationGesture())
        #self.registerGesture(RollGesture())



    @field_has_changed(PosChanged)
    def processChange(self):
        if -1.0 == self.PosChanged.value:
            return 

        for touchPoint in self.Cursors.value:
            if touchPoint.IsTouched.value:
                self._activePoints[touchPoint.CursorID.value] = touchPoint
            elif touchPoint.CursorID.value in self._activePoints:
                del self._activePoints[touchPoint.CursorID.value]

        for gesture in self.gestures:
            gesture.processGesture(self._activePoints.values(), self)

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


class MultiTouchGesture(object): #object
    """
    Base class for multi touch gestures.
    """

    def __init__(self):
        #self.super(MultiTouchGesture).__init__()
        self.resetMovingAverage()


    def processGesture(self, activePoints, touchDevice):
        """
        Process gesture. This method needs to be implemented in subclasses.

        @abstract
        @param activePoints: a list of currently active points
        @param mDofDevice: reference to multi-DoF device
        @return True if gesture was executed, otherwise False
        """
        pass

    def movingAverage(self, lastDataPoint, windowSize):
        """
        Stateful iterative moving average implementation to continuously _smooth
        input data. Smooths lastDataPoint based on previous inputs depending
        on windowSize. If you want to start a fresh input series, you have to
        call resetMovingAverage().

        @param lastDataPoint: the latest data point to smooth
        @param windowSize: the size of the window (smoothing factor)
        """
        if windowSize == self._maSamples:
            self._totalMA -= self._totalMA / windowSize
            self._maSamples -= 1
        self._totalMA += lastDataPoint
        self._maSamples += 1
        return self._totalMA / self._maSamples

    def resetMovingAverage(self):
        self._totalMA   = 0
        self._maSamples = 0

class DragGesture(MultiTouchGesture):
    def __init__(self):
        super(DragGesture, self).__init__()
        # last position for relative panning
        self._lastPos = None

    def processGesture(self, activePoints, touchDevice):
        if 2 != len(activePoints):
            self._lastPos = None
            return False

        point1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
        point2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
        
        point = point1.lerp_to(point2, .5)

        if None == self._lastPos:
            self._lastPos = point
            return False

        # map points from interval [0, 1] to [-1, 1]
        mappedPosX = point[0] * 2 - 1
        mappedPosY = point[1] * 2 - 1
        mappedLastPosX = self._lastPos[0] * 2 - 1
        mappedLastPosY = self._lastPos[1] * 2 - 1

        relDist               = (point[0] - self._lastPos[0], point[1] - self._lastPos[1])
        relDistSizeMapped     = (relDist[0] * touchDevice.getDisplay().size[0], relDist[1] * touchDevice.getDisplay().size[1])

        # multiply the distance by .5 * scaling factor
        # TODO: don't hardcode values --> CHECK :)

        newPosX = relDistSizeMapped[0]
        newPosY = relDistSizeMapped[1]


        centerPos = (point1 + ((point2-point1) / 2))
        self._fingerCenterPos = avango.gua.Vec3(centerPos.x, 0, centerPos.y)
        touchDevice.setFingerCenterPosition(self._fingerCenterPos, touchDevice)

        touchDevice.addLocalTranslation(avango.gua.make_trans_mat(newPosX, 0, newPosY))

        self._lastPos = (point[0], point[1])


        return True

class PinchGesture(MultiTouchGesture):
    def __init__(self):
        super(PinchGesture, self).__init__()
        self.distances = []

    def processGesture(self, activePoints, touchDevice):
        if len(activePoints) != 2:
            self.distances = []
            self.scaleCenter = None
            self.centerDirection = None
            return False

        vec1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
        vec2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
        distance = vec2 - vec1

        # save old distance
        if 3 == len(self.distances):
            self.distances.append(distance)
            self.distances.pop(0)
        else:
            self.distances.append(distance)
            return False

        relDistance = (self.distances[0].length() - self.distances[-1].length())

        # return if no significant movement occurred
        #if abs(relDistance) < .0005:
        #    return False

        #center = avango.gua.make_trans_mat(-.5, -.5, 0) * (vec1 + (vec2 - vec1) / 2)
        #rotMat = avango.gua.make_trans_mat(center[0], 0, center[1]) * mDofDevice.no_tracking_mat

        #mDofDevice.mf_dof.value[6] += relDistance * 16.3
        #mDofDevice.mf_dof.value[0] -= self.centerDirection.x * relDistance * 15 * self.display.size[0]
        #mDofDevice.mf_dof.value[2] -= self.centerDirection.y * relDistance * 15 * self.display.size[1]

        centerPos = (vec1 + ((vec2-vec1) / 2))
        self._fingerCenterPos = avango.gua.Vec3(centerPos.x, 0, centerPos.y)
        touchDevice.setFingerCenterPosition(self._fingerCenterPos, touchDevice)

        touchDevice.addLocalScaling(avango.gua.make_scale_mat(1 - relDistance))

        return True


class RotationGesture(MultiTouchGesture):
    
    def __init__(self):
        super(RotationGesture, self).__init__()
        self._distances = []
        self._lastAngle = 0

        # smoothing factor for rotation angles
        self._smoothingFactor = 30

        self._fingerCenterPos = avango.gua.Vec3(0,0,0)

    def processGesture(self, activePoints, touchDevice):
        if len(activePoints) != 2:
            self._distances = []
            return False

        vec1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
        vec2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
        distance = vec2 - vec1
        distance = avango.gua.Vec3(distance.x * touchDevice.getDisplay().size[0], distance.y * touchDevice.getDisplay().size[1], 0)

        # save old distance
        if 2 == len(self._distances):
            self._distances.append(distance)
            self._distances.pop(0)
        else:
            self._distances.append(distance)
            return False

        dist1 = self._distances[0]
        dist1.normalize()
        dist2 = self._distances[-1]
        dist2.normalize()
        dotProduct   = dist1.dot(dist2)
        crossProduct = self._distances[0].cross(self._distances[-1])

        # make sure have no overflows due to rounding issues
        if 1.0 < dotProduct:
            dotProduct = 1.0

        #print(crossProduct.z, self._distances[0], self._distances[-1])

        #center = avango.gua.make_trans_mat(-.5, -.5, 0) * (vec1 + (vec2 - vec1) / 2)
        #rotMat = avango.gua.make_trans_mat(center[0], 0, center[1]) * mDofDevice.no_tracking_mat
        angle = math.copysign(math.acos(dotProduct) * 180 / math.pi, -crossProduct.z)
        #angle = self.movingAverage(angle, self._smoothingFactor)

        #if 1 < abs(angle) - abs(self._lastAngle):
        #    self._lastAngle = angle
        #    return False

        #if .04 > abs(self._lastAngle - angle) and 0 == math.copysign(1, self._lastAngle) + math.copysign(1, angle):
        #    angle *= -1

        # calculate moving average to prevent oscillation
        #print(angle)
        
        centerPos = (vec1 + ((vec2-vec1) / 2))
        self._fingerCenterPos = avango.gua.Vec3(centerPos.x, 0, centerPos.y)
        touchDevice.setFingerCenterPosition(self._fingerCenterPos, touchDevice)

        touchDevice.addLocalRotation(avango.gua.make_rot_mat(angle, avango.gua.Vec3(0, 1, 0)))
        self._lastAngle = angle
        self._fingerCenterPos = avango.gua.Vec3(0,0,0)

        return True

# todo class viewgesture(MultiTouchGesture):
#  3 finger um den mittelpunit objekt drehen..
"""
class RollGesture(MultiTouchGesture):
    def __init__(self):
        super(RollGesture, self).__init__()

        self._distances12 = []
        self._distances23 = []
        self._positions = []


    def processGesture(self, activePoints, touchDevice):
        if len(activePoints) != 3:
            self._distances = []
            return False
        vec1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
        vec2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
        vec3 = avango.gua.Vec3(activePoints[2].PosX.value, activePoints[1].PosY.value, 0)

        distance12 = vec2 - vec1
        distance23 = vec3 - vec1

        #check if all distances are nearly the same
        if 2 == len(self._distances12):
            self._distances12.append(distance12)
            self._distances12.pop(0)
        else:
            self._distances12.append(distance12)
            return False

        # save old distance2
        if 2 == len(self._distances23):
            self._distances23.append(distance23)
            self._distances23.pop(0)
        else:
            self._distances23.append(distance23)
            return False

        # save positions from vec2
        if 2 == len(self._positions):
            self._positions.append(vec2)
            self._positions.pop(0)
        else:
            self._positions.append(vec2)
            return False

        distanceDiff12 = self._distances12[0] - self._distances12[-1]
        distanceDiff23 = self._distances23[0] - self._distances23[-1]

        if (math.fabs(distanceDiff12.length()) > 0.01 or math.fabs(distanceDiff23.length()) > 0.01):
            return False

        directionVec = self._positions[0] - self._positions[-1]
        rotationalAxis = avango.gua.Vec3(directionVec.y, 0, directionVec.x)

        angle = directionVec.length() * 360
        touchDevice.addLocalRotation(avango.gua.make_rot_mat(angle, rotationalAxis))

        return True
"""
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

