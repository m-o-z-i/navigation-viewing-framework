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
        self.DirectionAngle = 0 
        self.distances=[]

    def my_constructor(self, no_tracking_mat):
        self.init_station_tracking(None, no_tracking_mat)


    ## Creates a representation of the device in the virutal world.
    # @param PLATFORM_NODE The platform node to which the avatar should be appended to.
    # @param PLATFORM_ID The platform id used for setting the group name correctly.
    def create_device_avatar(self, PLATFORM_NODE, PLATFORM_ID):

        _loader = avango.gua.nodes.TriMeshLoader()

        ## @var avatar_transform
        # Scenegraph transform node for the dekstop user's table.
        self.avatar_transform = avango.gua.nodes.TransformNode(Name = 'avatar_transform')
        self.avatar_transform.Transform.connect_from(self.tracking_reader.sf_avatar_body_mat)
        PLATFORM_NODE.Children.value.append(self.avatar_transform)

        ## @var device_avatar
        # Scenegraph node representing the geometry and transformation of the device avatar.
        self.device_avatar = _loader.create_geometry_from_file('device_avatar',
                                                               'data/objects/table/table.obj',
                                                               'data/materials/Stones.gmd',
                                                               avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.device_avatar.Transform.value = avango.gua.make_trans_mat(-0.8, 0.2, 0.8) * avango.gua.make_scale_mat(0.2, 0.5, 0.5)
        self.avatar_transform.Children.value.append(self.device_avatar)
        self.device_avatar.GroupNames.value = ['avatar_group_' + str(PLATFORM_ID)]
    

    def evaluate(self):
        for touchPoint in self.Cursors.value:
            if touchPoint.IsTouched.value:
                self.activePoints[touchPoint.CursorID.value] = touchPoint
            elif touchPoint.CursorID.value in self.activePoints:
                del self.activePoints[touchPoint.CursorID.value]

        #print len(self.activePoints)





        self.processGesture()


    def processGesture(self):
        """
        Detect and process multi touch gestures.
        """
        #manipulate mf_dof for navigation : [trans_x, trans_y, trans_z, pitch, head, roll, scale]

        pointList = self.activePoints.values()

        if len(self.activePoints) > 1:
            pass
            #sort the list and group points
        
        if len(self.activePoints) == 1:
            self.mf_dof.value[0] += (pointList[0].SpeedX.value)
            self.mf_dof.value[2] += -(pointList[0].SpeedY.value)

        if len(self.activePoints) == 2:
            # DirectionAngle = acos (DirectionOld[0] scalar TouchDirection / |1 * 1|)
            distance = pointList[0].touchPosition - pointList[1].touchPosition
            print pointList[0].MovementVector.value.dot(pointList[1].MovementVector.value)
            self.DirectionAngle = math.acos(pointList[0].MovementVector.value.dot(pointList[1].MovementVector.value))

            #save old distance
            if 2 == len(self.distances):
                self.distances.append(distance)
                self.distances.pop(0)
            else:
                self.distances.append(distance)

            # from radians to degrees
            self.DirectionAngle = self.DirectionAngle * (180 / math.pi)

            if 90 < self.DirectionAngle:
                movement = pointList[0].MotionSpeed.value + pointList[1].MotionSpeed.value

                if abs(self.distances[0].length()) < abs(self.distances[-1].length()):
                    self.mf_dof.value[1] += -movement
                else:
                    self.mf_dof.value[1] += movement

            else:
                pass




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

