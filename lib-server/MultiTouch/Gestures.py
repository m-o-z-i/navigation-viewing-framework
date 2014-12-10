#!/usr/bin/python


import avango
import avango.gua
import time
import math

class MultiTouchGesture(object):
	"""
	Base class for multi touch gestures.
	"""

	def __init__(self):
		self.resetMovingAverage()

	def processGesture(self, activePoints, hands, touchDevice):
		"""
		Process gesture. This method needs to be implemented in subclasses.

		@abstract
		@param activePoints: a list of currently active points as tuples of hand ID and touch point
		@param hands: the active hands as dict with hand IDs as keys
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

	def getTouchPointsPerHand(self, touchPoints, hands):
		"""
		Return a dict with touchPoints grouped by hand.

		@param touchPoints: the touch points to group as a list of (handID, touchPoint) tuples
		@param hands: the hands to group by as dict with hand IDs as keys
		"""
		pointsPerHand = dict((handID, []) for handID in hands)
		for p in touchPoints:
			pointsPerHand[p[0]].append(p[1])
		return pointsPerHand

	def guardSingleHandGesture(self, touchPoints, hands, numberOfTouchPoints):
		"""
		Return a valid hand ID if there is a single hand with specified number of touch points.

		@param touchPoints: the currently active touch points as a list of (handID, touchPoint) tuples
		@param hands: then active hands as dict with hand IDs as keys
		@param numberOfTouchPoints: the number of touch points to accep
		@return: the ID of the first hand matching the number criteria or -1 if none could be found
		"""
		pointsPerHand = self.getTouchPointsPerHand(touchPoints, hands)
		for h, p in pointsPerHand.items():
			if len(p) == numberOfTouchPoints:
				return h
		return -1


class DoubleTapGesture(MultiTouchGesture):
	"""
	DoubleTapGesture to toggle between object and navigation mode
	"""
	def __init__(self):
		super(DoubleTapGesture, self).__init__()

		self._lastmilliseconds = 0 
		self._objectMode = False
		
		""" is necessary as a threshold for the first tap  """
		self._frameCounter = 0

		""" first tap is declared as a first first """
		self._firstTap = False
		self._lastCounter = 0

		""" doubletap intervall: between 100ms and 200ms """
		self._intervall = [100, 250]

	def processGesture(self, activePoints, hands, touchDevice):
		if len(activePoints) != 2:
			return False

		self._frameCounter += 1

		""" last call of method """ 
		lastDetectedActivity = int(round(time.time() * 1000)) - self._lastmilliseconds

		if 150 < lastDetectedActivity:
			self._firstTap = True
			self._frameCounter = 0

		""" 
		doubletap intervall: between 100ms and 200ms
		"""
		if self._intervall[1] > lastDetectedActivity and self._intervall[0] < lastDetectedActivity and self._firstTap:
			if not self._objectMode:
				self._objectMode = touchDevice.setObjectMode(True)
			
			else:
				self._objectMode = touchDevice.setObjectMode(False)

			self._firstTap = False
			self._frameCounter = 0

		else:
			if self._intervall[1] > lastDetectedActivity and 10 < self._frameCounter:
				self._firstTap = False
				self._frameCounter = 0

		#print "firstTap: " , self._firstTap , " ; detectedActivity: " ,  lastDetectedActivity , " ; frameCounter = " , self._frameCounter
		
		self._lastmilliseconds = int(round(time.time() * 1000))


class DragGesture(MultiTouchGesture):
	""" 
	DragGesture to move scene or objects 
	"""
	def __init__(self):
		super(DragGesture, self).__init__()
		""" last position for relative panning """
		self._lastPos = None

	def processGesture(self, activePoints, hands, touchDevice):
		handID = self.guardSingleHandGesture(activePoints, hands, 2)

		if -1 == handID:
			self._lastPos = None
			return

		pointsPerHand = self.getTouchPointsPerHand(activePoints, hands)
		activePoints  = pointsPerHand[handID]

		point1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
		point2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
		
		point = point1.lerp_to(point2, .5)

		if None == self._lastPos:
			self._lastPos = point
			return False

		""" map points from interval [0, 1] to [-1, 1] """
		mappedPosX = point[0] * 2 - 1
		mappedPosY = point[1] * 2 - 1
		mappedLastPosX = self._lastPos[0] * 2 - 1
		mappedLastPosY = self._lastPos[1] * 2 - 1

		""" movement vector between old and new point """
		relDist               = (point[0] - self._lastPos[0], point[1] - self._lastPos[1])
		relDistSizeMapped     = (relDist[0] * touchDevice.getDisplay().size[0] , relDist[1] * touchDevice.getDisplay().size[1])

		newPosX = relDistSizeMapped[0]
		newPosY = relDistSizeMapped[1]

		#print ("display size: " , touchDevice.getDisplay().size[0] , ", " , touchDevice.getDisplay().size[1], "; pos: " , newPosX , ", " , newPosY)


		touchDevice.addLocalTranslation(avango.gua.make_trans_mat(newPosX, 0, newPosY))

		self._lastPos = (point[0], point[1])


		return True


class PinchGesture(MultiTouchGesture):
	""" 
	PinchGesture to scale scene or objects 
	"""
	def __init__(self):
		super(PinchGesture, self).__init__()
		self.distances = []

	def processGesture(self, activePoints, hands, touchDevice):
		if 2 != len(activePoints):
			self.distances = []
			self.scaleCenter = None
			self.centerDirection = None
			return False

		vec1 = avango.gua.Vec3(activePoints[0][1].PosX.value, activePoints[0][1].PosY.value, 0)
		vec2 = avango.gua.Vec3(activePoints[1][1].PosX.value, activePoints[1][1].PosY.value, 0)
		distance = vec2 - vec1

		""" save old distance """
		if 3 == len(self.distances):
			self.distances.append(distance)
			self.distances.pop(0)
		else:
			self.distances.append(distance)
			return False

		""" distance covered after 3 frames """
		relDistance = (self.distances[0].length() - self.distances[-1].length())

		touchDevice.addLocalScaling(avango.gua.make_scale_mat(1 - relDistance))

		return True


class PitchRollGesture(MultiTouchGesture):
	""" 
	PitchRollGesture to pitch and roll scene or objects
	"""
	def __init__(self):
		super(PitchRollGesture, self).__init__()

		""" distance between first and second point """
		self._distances12 = []
		
		""" distance between second and third point """
		self._distances23 = []

		""" save old positions """
		self._positions = []


	def processGesture(self, activePoints, hands, touchDevice):
		handID = self.guardSingleHandGesture(activePoints, hands, 3)

		if -1 == handID:
			self._positions = []
			return False

		pointsPerHand = self.getTouchPointsPerHand(activePoints, hands)
		activePoints  = pointsPerHand[handID]

		vec1 = avango.gua.Vec3(activePoints[0].PosX.value, activePoints[0].PosY.value, 0)
		vec2 = avango.gua.Vec3(activePoints[1].PosX.value, activePoints[1].PosY.value, 0)
		vec3 = avango.gua.Vec3(activePoints[2].PosX.value, activePoints[1].PosY.value, 0)

		""" save positions from vec2 """
		if 2 == len(self._positions):
			self._positions.append(vec2)
			self._positions.pop(0)
		else:
			self._positions.append(vec2)
			return False
		
		distance12 = vec2 - vec1
		distance23 = vec3 - vec1

		""" return when the distance between points is too big (can't be the fingers of one hand)"""
		if 0.1 < distance12.length() or 0.1 < distance23.length():
			return False

		""" direction vector of all 3 fingers """
		directionVec = self._positions[0] - self._positions[-1]

		""" orthogonal rotation axis """
		rotationalAxis = avango.gua.Vec3(-directionVec.y, 0, directionVec.x)
		angle = directionVec.length() * 360
		
		""" to avoid noisy discontinuous points """
		if 10 < angle:
			#print angle , "; 1: " , self._positions[0] , "; 2: " , self._positions[-1] , " ; dirVec: " , directionVec , "; dirVec lenght: " , directionVec.length()
			return False

		touchDevice.addLocalRotation(avango.gua.make_rot_mat(angle, rotationalAxis))

		return True

class RotationGesture(MultiTouchGesture):
	"""
	RotationGesture to ratate scene or objects
	"""
	def __init__(self):
		super(RotationGesture, self).__init__()
		self._distances = []
		self._lastAngle = 0

		""" smoothing factor for rotation angles """
		self._smoothingFactor = 8

	def processGesture(self, activePoints, hands, touchDevice):
		handID = self.guardSingleHandGesture(activePoints, hands, 2)

		if -1 == handID:
			self._distances = []
			return False

		vec1 = avango.gua.Vec3(activePoints[0][1].PosX.value, activePoints[0][1].PosY.value, 0)
		vec2 = avango.gua.Vec3(activePoints[1][1].PosX.value, activePoints[1][1].PosY.value, 0)
		distance = vec2 - vec1
		distance = avango.gua.Vec3(distance.x * touchDevice.getDisplay().size[0], distance.y * touchDevice.getDisplay().size[1], 0)

		""" save old distance """
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

		""" make sure have no overflows due to rounding issues """
		if 1.0 < dotProduct:
			dotProduct = 1.0
		
		""" covered angle after 2 frames """
		angle = math.copysign(math.acos(dotProduct) * 180 / math.pi, -crossProduct.z)
		angle = self.movingAverage(angle, self._smoothingFactor)
		
		touchDevice.addLocalRotation(avango.gua.make_rot_mat(angle, avango.gua.Vec3(0, 1, 0)))
		self._lastAngle = angle
		self._fingerCenterPos = avango.gua.Vec3(0,0,0)

		return True

