#!/bin/python

from Device import MultiDofDevice
from SceneManager import SceneManager 
from Intersection import *

import avango
import avango.gua
import avango.daemon
import avango.script
from avango.script import field_has_changed
import subprocess
import math
import avango.utils
import time

class MultiTouchDevice(avango.script.Script):
    """
    Base class for multi touch devices.
    """
    _rayOrientation = avango.gua.SFMatrix4()
    _fingerCenterPos = avango.gua.SFVec3()

    def __init__(self):
        self.super(MultiTouchDevice).__init__()
        self._sceneGraph = None
        self._display    = None
        self._worldMat   = avango.gua.make_identity_mat()
        self._transMat   = avango.gua.make_identity_mat()
        self._rotMat     = avango.gua.make_identity_mat()
        self._scaleMat   = avango.gua.make_identity_mat()
        
        self._localMatrix = avango.gua.make_identity_mat()
        self._globalMatrix = avango.gua.make_identity_mat()

        #self._fingerCenterPos.value = avango.gua.Vec3(0,0,0)
        self._lastPos = None

        self._sceneName = None
        self._objectName = None
        self._objectMode = False

        self._intersectionPoint = avango.gua.Vec3(0,0,0)
        self._intersectionObject = None

        self.ray_length = 1000
        self.ray_thickness = 0.0075
        self.intersection_sphere_size = 0.025
        self.highlighted_object = None
        self.hierarchy_selection_level = -1
        self._last_pick_result = None


        self.always_evaluate(True)


    def my_constructor(self, graph, display, NET_TRANS_NODE, SCENE_MANAGER):
        """
        Initialize multi-touch device.

        @param graph: the scene graph on which to operate
        @param display: the physical display
        """
        self._sceneGraph = graph
        self._display    = display
        self._origMat    = graph.Root.value.Transform.value

        self._intersection = Intersection() # ray intersection for target identification
        self._intersection.my_constructor(self._sceneGraph, self._rayOrientation, self.ray_length, "") # parameters: SCENEGRAPH, SF_PICK_MATRIX, PICK_LENGTH, PICKMASK
        self._intersectionFound = False

        _parent_node = self._sceneGraph["/net/platform_0/scale"]

        # init scenegraph node
        ## @var ray_transform
        # Transformation node of the pointer's ray.
        self.ray_transform = avango.gua.nodes.TransformNode(Name = "ray_transform")
        _parent_node.Children.value.append(self.ray_transform)

        _loader = avango.gua.nodes.TriMeshLoader()
        
        ## @var ray_geometry
        # Geometry node representing the ray graphically.
        self.ray_geometry = _loader.create_geometry_from_file("ray_geometry", "data/objects/cylinder.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.ray_transform.Children.value.append(self.ray_geometry)

        self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0,0,0) * \
                                            avango.gua.make_rot_mat(0,0,0,0) * \
                                            avango.gua.make_scale_mat(0,0,0)
        
        ## @var intersection_point_geometry
        # Geometry node representing the intersection point of the ray with an object in the scene.
        self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry", "data/objects/sphere.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
        NET_TRANS_NODE.Children.value.append(self.intersection_point_geometry)
        self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible

        self.ray_transform.Transform.connect_from(self._rayOrientation)


    def getDisplay(self):
        return self._display
    

    def getSceneGraph(self):
        return self._sceneGraph


    def setFingerCenterPosition(self, FingerCenterPos):

        point = FingerCenterPos

        # map points from interval [0, 1] to [-0.5, 0.5]
        mappedPosX = point[0] * 1 - 0.5
        mappedPosY = point[1] * 1 - 0.5

        self._fingerCenterPos.value = avango.gua.Vec3(mappedPosX * self.getDisplay().size[0], 0.0, mappedPosY * self.getDisplay().size[1])    


    def setObjectMode(self, active):
        if active and len(self._intersection.mf_pick_result.value) > 0:
            self._objectMode = True
            self._objectName = self._intersectionObject.Parent.value.Name.value
            return True
            
        self._objectMode = False
        self._objectName = None
        return False


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


    def intersectSceneWithFingerPos(self):
        self._rayOrientation.value = avango.gua.make_trans_mat(self._fingerCenterPos.value.x , 1 , self._fingerCenterPos.value.z) * avango.gua.make_rot_mat(-90,1,0,0) * avango.gua.make_scale_mat(1,1,1)
        
        # intersection found
        if len(self._intersection.mf_pick_result.value) > 0:
            self._intersectionFound = True

            #first intersected object
            _pick_result = self._intersection.mf_pick_result.value[0]

            self._intersectionPoint = _pick_result.Position.value 
            self._intersectionObject = _pick_result.Object.value
            
            #update intersectionObject until you insert object Mode
            if not self._objectMode:
                self._lastIntersectionObject = self._intersectionObject

            # VISUALISATION:
            # transform point into world coordinates
            self._intersectionPoint = self._intersectionObject.WorldTransform.value * self._intersectionPoint 
            # make Vec3 from Vec4
            self._intersectionPoint = avango.gua.Vec3(self._intersectionPoint.x,self._intersectionPoint.y,self._intersectionPoint.z) 
            
            # update intersection sphere
            self.intersection_point_geometry.Transform.value = avango.gua.make_trans_mat(self._intersectionPoint) * \
                                                               avango.gua.make_scale_mat(self.intersection_sphere_size, self.intersection_sphere_size, self.intersection_sphere_size)
            # set sphere visible                                           
            self.intersection_point_geometry.GroupNames.value = [] 

            # update ray
            _distance = (self._intersectionPoint - self.ray_transform.WorldTransform.value.get_translate()).length()
            self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,_distance * -0.5) * \
                                                avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                                avango.gua.make_scale_mat(self.ray_thickness, _distance, self.ray_thickness)

        else:
            # set geometry invisible
            self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] 
          
            # set to default ray length
            self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                                                avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                                avango.gua.make_scale_mat(self.ray_thickness, self.ray_length, self.ray_thickness)
            self._intersectionFound = False


    def update_object_highlight(self):
        #highlight active object:
        if self._objectMode:
            _node = self._lastIntersectionObject

            if _node.has_field("InteractiveObject") == True:
                _object = _node.InteractiveObject.value
              
                if self.hierarchy_selection_level >= 0:          
                    _object = _object.get_higher_hierarchical_object(self.hierarchy_selection_level)
              
                if _object == None:
                # evtl. disable highlight of prior object
                    if self.highlighted_object != None:
                        self.highlighted_object.enable_highlight(False)

                else:
                    if _object != self.highlighted_object: # new object hit
                    
                        # evtl. disable highlight of prior object
                        if self.highlighted_object != None:
                            self.highlighted_object.enable_highlight(False)

                        self.highlighted_object = _object
                        
                        # enable highlight of new object
                        self.highlighted_object.enable_highlight(True)

        #don't highlight something
        else:
            # evtl. disable highlight of prior object
            if self.highlighted_object != None:
                self.highlighted_object.enable_highlight(False)
                self.highlighted_object = None


    def applyTransformations(self):
        """
        Apply calculated world matrix to scene graph.
        Requires the scene graph to have a transform node as root node.
        """

        self._sceneName = SceneManager.active_scene_name

        if (None != self._sceneName):
            
            sceneNode = "/net/" + self._sceneName
            self._globalMatrix = self._sceneGraph[sceneNode].Transform.value
            
            #object Mode
            if self._objectMode:
                objectNode = "/net/" + self._sceneName + "/" + self._objectName
                scenePos = self._sceneGraph[objectNode].Transform.value.get_translate()
                TransformMatrix = self._sceneGraph[objectNode].Transform.value
            else: 
                scenePos = self._sceneGraph[sceneNode].Transform.value.get_translate()
                TransformMatrix = self._sceneGraph[sceneNode].Transform.value


            #print "scenePos: ", scenePos ,  "  ; fingerpos: " , self._fingerCenterPos.value
            
            translateDistance = self._fingerCenterPos.value - scenePos

            #transform world-space to object-space
            translateDistance = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * translateDistance
            translateDistance = avango.gua.Vec3(translateDistance.x, translateDistance.y, translateDistance.z)

            #first translate and rotate to origin, second calculate new position, third translate and rotate back
            
            if self._objectMode:
                TransformMatrix = avango.gua.make_trans_mat(TransformMatrix.get_translate()) * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_trans_mat(translateDistance * 1.0) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(self._globalMatrix.get_rotate_scale_corrected())) * \
                                  self._rotMat * \
                                  self._scaleMat * \
                                  self._transMat * \
                                  avango.gua.make_rot_mat(self._globalMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_trans_mat(translateDistance * -1.0) * \
                                  avango.gua.make_scale_mat(TransformMatrix.get_scale())

            else:
                TransformMatrix = avango.gua.make_trans_mat(TransformMatrix.get_translate()) * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_trans_mat(translateDistance * 1.0) * \
                                  avango.gua.make_trans_mat(avango.gua.Vec3(0, self._intersectionPoint.y * -1.0 , 0)) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * \
                                  self._rotMat * \
                                  self._scaleMat * \
                                  self._transMat * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_trans_mat(avango.gua.Vec3(0, self._intersectionPoint.y * 1.0 , 0)) * \
                                  avango.gua.make_trans_mat(translateDistance * -1.0) * \
                                  avango.gua.make_scale_mat(TransformMatrix.get_scale())

            #object Mode
            if self._objectMode:
                self._sceneGraph[objectNode].Transform.value = TransformMatrix
            else:
                self._sceneGraph[sceneNode].Transform.value = TransformMatrix


            #print TransformMatrix
            #print "trans: ", TransformMatrix.get_translate(), "  rot: " , TransformMatrix.get_rotate_scale_corrected() , "  scale: " , TransformMatrix.get_scale()

            #reset all data
            self._transMat   = avango.gua.make_identity_mat()
            self._rotMat     = avango.gua.make_identity_mat()
            self._scaleMat   = avango.gua.make_identity_mat()
            self._globalMatrix = avango.gua.make_identity_mat()


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
        self._frameCounter = 0

    def my_constructor(self, graph, display, NET_TRANS_NODE, SCENE_MANAGER):
        self.super(TUIODevice).my_constructor(graph, display, NET_TRANS_NODE, SCENE_MANAGER)
        
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
        self.registerGesture(RollGesture())
        self.registerGesture(DoubleTapGesture())
        self.always_evaluate(True)


    def evaluate(self):
        self._frameCounter += 1
        self.processChange()

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

        activePoints = self._activePoints.values()

        doSomething = True

        if len(activePoints) == 2:
            point1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
            point2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
            centerPos = (point1 + ((point2-point1) / 2))

        elif len(activePoints) == 3:
            point1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
            point2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
            point3 = avango.gua.Vec3(activePoints[2].PosX.value, activePoints[2].PosY.value, 0)
            centerPos = (point1 + point2 + point3) / 3

        else:
            doSomething = False

        if (doSomething):
            self.setFingerCenterPosition(centerPos)
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

        touchDevice.addLocalScaling(avango.gua.make_scale_mat(1 - relDistance))

        return True


class RotationGesture(MultiTouchGesture):
    
    def __init__(self):
        super(RotationGesture, self).__init__()
        self._distances = []
        self._lastAngle = 0

        # smoothing factor for rotation angles
        self._smoothingFactor = 8

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
        dotProduct   = abs(dist1.dot(dist2))
        crossProduct = self._distances[0].cross(self._distances[-1])

        # make sure have no overflows due to rounding issues
        if 1.0 < dotProduct:
            dotProduct = 1.0

        #print(crossProduct.z, self._distances[0], self._distances[-1])

        #center = avango.gua.make_trans_mat(-.5, -.5, 0) * (vec1 + (vec2 - vec1) / 2)
        #rotMat = avango.gua.make_trans_mat(center[0], 0, center[1]) * mDofDevice.no_tracking_mat
        
        angle = math.copysign(math.acos(dotProduct) * 180 / math.pi, -crossProduct.z)
        angle = self.movingAverage(angle, self._smoothingFactor)

        #if 1 < abs(angle) - abs(self._lastAngle):
        #    self._lastAngle = angle
        #    return False

        #if .04 > abs(self._lastAngle - angle) and 0 == math.copysign(1, self._lastAngle) + math.copysign(1, angle):
        #    angle *= -1

        # calculate moving average to prevent oscillation
        #print(angle)
        
        touchDevice.addLocalRotation(avango.gua.make_rot_mat(angle, avango.gua.Vec3(0, 1, 0)))
        self._lastAngle = angle
        self._fingerCenterPos = avango.gua.Vec3(0,0,0)

        return True

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
        rotationalAxis = avango.gua.Vec3(-directionVec.y, 0, directionVec.x)

        angle = directionVec.length() * 360
        touchDevice.addLocalRotation(avango.gua.make_rot_mat(angle, rotationalAxis))

        return True


class DoubleTapGesture(MultiTouchGesture):
    def __init__(self):
        super(DoubleTapGesture, self).__init__()

        self._lastmilliseconds = 0 
        self._objectMode = False
        self._frameCounter = 0
        self._firstTap = False
        self._lastCounter = 0

    def processGesture(self, activePoints, touchDevice):
        if len(activePoints) != 2:
            return False

        self._frameCounter += 1

        lastDetectedActivity = int(round(time.time() * 1000)) - self._lastmilliseconds

        if 150 < lastDetectedActivity:
            self._firstTap = True
            self._frameCounter = 0

        #doubletap intervall
        if 150 > lastDetectedActivity and 50 < lastDetectedActivity and self._firstTap:
            if not self._objectMode:
                self._objectMode = touchDevice.setObjectMode(True)
                #print "object mode = " , self._objectMode , " old: True"
            
            else:
                self._objectMode = touchDevice.setObjectMode(False)
                #print "object mode = " , self._objectMode , " old: False"

            self._firstTap = False
            self._frameCounter = 0

        else:
            if 150 > lastDetectedActivity and 7 < self._frameCounter:
                self._firstTap = False

        
        #print "firstTap: " , self._firstTap , " ; detectedActivity: " ,  lastDetectedActivity , " ; object mode = " , self._objectMode
        self._lastmilliseconds = int(round(time.time() * 1000))


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

