#!/usr/bin/python

import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import subprocess
#import avango.utils

from MultiTouch.MultiTouchDevice import MultiTouchDevice
from MultiTouch.Gestures import *

class TUIODevice(MultiTouchDevice):
    """
    Multi touch device class to process TUIO input.
    """
    Cursors = avango.MFContainer()
    Hands = avango.MFContainer()
    MovementChanged = avango.SFBool()
    PosChanged = avango.SFFloat()

    def __init__(self):
        """
        Initialize driver and touch cursors
        """
        self.super(TUIODevice).__init__()

        """multi-touch gestures to be registered"""
        self.gestures = []

        """ all TUIO points found on the table """
        self._activePoints = {}

        self._frameCounter = 0

    def my_constructor(self, graph, display, NET_TRANS_NODE, SCENE_MANAGER, APPLICATION_MANAGER):
        self.super(TUIODevice).my_constructor(graph, display, NET_TRANS_NODE, SCENE_MANAGER, APPLICATION_MANAGER)
        
        # add touch cursors
        for i in range(0, 20):
            cursor = TUIOCursor(CursorID = i) 
            self.Cursors.value.append(cursor)
            self.MovementChanged.connect_from(cursor.IsMoving)
            self.PosChanged.connect_from(cursor.PosX)
            self.PosChanged.connect_from(cursor.PosY)

        # add hands (just one for now since we don't support separate views for users yet)
        for i in range(0, 4):
            hand = TUIOHand(HandID  = i)
            self.Hands.value.append(hand)

        # register gestures
        # TODO: do this somewhere else
        #self.registerGesture(DoubleTapGesture())
        self.registerGesture(DragGesture())
        self.registerGesture(PinchGesture())
        self.registerGesture(RotationGesture())
        self.registerGesture(PitchRollGesture())

        self.always_evaluate(True)


    def evaluate(self):
        self._frameCounter += 1
        self.processChange()


    #@field_has_changed(PosChanged)
    def processChange(self):
        if -1.0 == self.PosChanged.value:
            return

        # update active point list
        hands        = {}
        activePoints = []

        for touchPoint in self.Cursors.value:
            for hand in self.Hands.value:
                if touchPoint.IsTouched.value and touchPoint.SessionID.value in hand.FingerSIDs.value:
                    activePoints.append((hand.HandID.value, touchPoint))
                    hands[hand.HandID.value] = hand
                    break

        #print ("NAV_FRAMEWORK: anzahl an händen:  " , len(hands))


        for gesture in self.gestures:
            gesture.processGesture(activePoints, hands, self)
        
        # valid input is registered
        doSomething = True

        # reset all visualizations
        self.fingercenterpos_geometry.GroupNames.value = ["do_not_display_group"]
        self.handPos_geometry.GroupNames.value = ["do_not_display_group"]

        if len(activePoints) == 2:
            point1 = avango.gua.Vec3(activePoints[0][1].PosX.value, activePoints[0][1].PosY.value, 0)
            point2 = avango.gua.Vec3(activePoints[1][1].PosX.value, activePoints[1][1].PosY.value, 0)
            centerPos = (point1 + ((point2-point1) / 2))

        elif len(activePoints) == 3:
            point1 = avango.gua.Vec3(activePoints[0][1].PosX.value, activePoints[0][1].PosY.value, 0)
            point2 = avango.gua.Vec3(activePoints[1][1].PosX.value, activePoints[1][1].PosY.value, 0)
            point3 = avango.gua.Vec3(activePoints[2][1].PosX.value, activePoints[2][1].PosY.value, 0)
            centerPos = (point1 + point2 + point3) / 3

        elif len(activePoints) == 5:
            point1 = avango.gua.Vec3(activePoints[0][1].PosX.value, activePoints[0][1].PosY.value, 0)
            point2 = avango.gua.Vec3(activePoints[1][1].PosX.value, activePoints[1][1].PosY.value, 0)
            point3 = avango.gua.Vec3(activePoints[2][1].PosX.value, activePoints[2][1].PosY.value, 0)
            point4 = avango.gua.Vec3(activePoints[3][1].PosX.value, activePoints[3][1].PosY.value, 0)
            point5 = avango.gua.Vec3(activePoints[4][1].PosX.value, activePoints[4][1].PosY.value, 0)
            centerPos = (point1 + point2 + point3 + point4 + point5) / 5
            self.visualisizeHandPosition(self.mapInputPosition(centerPos))

        else:
            # only one ore more than 3 input points are not valid until now
            doSomething = False

        if doSomething:
            self.setFingerCenterPos(self.mapInputPosition(centerPos))
            self.intersectSceneWithFingerPos()
            self.update_object_highlight()
            self.applyTransformations()


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
    
    def evaluate(self):
        pass
        #print ("Finger: ID ", self.SessionID.value, " PosX: " , self.PosX.value, "  PosY" , self.PosY.value)

    def updateTouched(self):
        """
        Call whenever some touch input data has changed. This method will update self.IsTouched accordingly.
        """
        self.IsTouched.value = (self.PosX.value != -1.0 and self.PosY.value != -1.0)

    @field_has_changed(CursorID)
    def set_station(self):
        """
        Set station name.
        """
        self.device_sensor.Station.value = "gua-finger{}#cursor".format(self.CursorID.value)
        print ("HUBA HUB" , self.device_sensor.Station.value)

    @field_has_changed(PosX)
    def updatePosX(self):
        self.updateTouched()

    @field_has_changed(PosY)
    def updatePosY(self):
        self.updateTouched()

class TUIOHand(avango.script.Script):
    HandID           = avango.SFInt()
    SessionID        = avango.SFFloat()
    
    PosX             = avango.SFFloat()
    PosY             = avango.SFFloat()

    Finger1SID       = avango.SFFloat()
    Finger2SID       = avango.SFFloat()
    Finger3SID       = avango.SFFloat()
    Finger4SID       = avango.SFFloat()
    Finger5SID       = avango.SFFloat()
    FingerSIDs       = avango.MFFloat()

    BoundingBox_MinX = avango.SFFloat()
    BoundingBox_MinY = avango.SFFloat()
    BoundingBox_MaxX = avango.SFFloat()
    BoundingBox_MaxY = avango.SFFloat()
    
    HandClass        = avango.SFFloat()

    ArmCenterX       = avango.SFFloat()
    ArmCenterY       = avango.SFFloat()
    ArmMinor         = avango.SFFloat()
    ArmMajor         = avango.SFFloat()
    ArmInclination   = avango.SFFloat()

    def __init__(self):
        self.super(TUIOHand).__init__()

        self.FingerSIDs.value = [-1.0, -1.0, -1.0, -1.0, 1.0]
        self.SessionID.value  = -1.0
        self.Finger1SID.value = -1.0
        self.Finger2SID.value = -1.0
        self.Finger3SID.value = -1.0
        self.Finger4SID.value = -1.0
        self.Finger5SID.value = -1.0

        self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.SessionID.connect_from(self.device_sensor.Value0)
        
        self.PosX.connect_from(self.device_sensor.Value1)
        self.PosY.connect_from(self.device_sensor.Value2)

        self.Finger1SID.connect_from(self.device_sensor.Value3)
        self.Finger2SID.connect_from(self.device_sensor.Value4)
        self.Finger3SID.connect_from(self.device_sensor.Value5)
        self.Finger4SID.connect_from(self.device_sensor.Value6)
        self.Finger5SID.connect_from(self.device_sensor.Value7)

        self.BoundingBox_MinX.connect_from(self.device_sensor.Value8)
        self.BoundingBox_MinY.connect_from(self.device_sensor.Value9)
        self.BoundingBox_MaxX.connect_from(self.device_sensor.Value10)
        self.BoundingBox_MaxY.connect_from(self.device_sensor.Value11)

        self.HandClass.connect_from(self.device_sensor.Value12)

        self.ArmCenterX.connect_from(self.device_sensor.Value13)
        self.ArmCenterY.connect_from(self.device_sensor.Value14)
        self.ArmMajor.connect_from(self.device_sensor.Value15)
        #self.ArmMinor.connect_from(self.device_sensor.Value16)
        #self.ArmInclination.connect_from(self.device_sensor.Value17)

    @field_has_changed(PosX)
    def test(self):
        print("NAV_FRAMEWORK: handpos changed " , self.PosX.value, "  ; arm major : " , self.ArmMajor.value)

    @field_has_changed(HandID)
    def set_station(self):
        """
        Set station name.
        """
        self.device_sensor.Station.value = "gua-finger{}#hand".format(self.HandID.value)


    @field_has_changed(Finger1SID)
    def updateFinger1InField(self):
        self.FingerSIDs.value[0] = self.Finger1SID.value

    @field_has_changed(Finger2SID)
    def updateFinger2InField(self):
        self.FingerSIDs.value[1] = self.Finger2SID.value

    @field_has_changed(Finger3SID)
    def updateFinger3InField(self):
        self.FingerSIDs.value[2] = self.Finger3SID.value

    @field_has_changed(Finger4SID)
    def updateFinger4InField(self):
        self.FingerSIDs.value[3] = self.Finger4SID.value

    @field_has_changed(Finger5SID)
    def updateFinger5InField(self):
        self.FingerSIDs.value[4] = self.Finger5SID.value
