#!/usr/bin/python

## @file
# Contains class Workspace.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ConsoleIO import *
from DisplayGroup import *
from PortalCamera import *
from RayPointer import *
from User import *
from Video3D import *
import Utilities

## Representation of the physical space holding several users, tools and display groups.
class Workspace:

  ## @var number_of_instances
  # Number of Workspace instances that have already been created. Used for assigning correct IDs.
  number_of_instances = 0

  ## Custom constructor.
  # @param NAME Name of the Workspace to be created.
  # @param TRANSMITTER_OFFSET Transmitter offset to be applied within this workspace.
  def __init__(self, NAME, TRANSMITTER_OFFSET):

    ## @var id
    # Identification number of this workspace.
    self.id = Workspace.number_of_instances
    Workspace.number_of_instances += 1

    # @var name
    # Name of this Workspace.
    self.name = NAME

    ## @var transmitter_offset
    # Transmitter offset to be applied within this workspace.
    self.transmitter_offset = TRANSMITTER_OFFSET

    ## @var users
    # List of users that are active within this workspace.
    self.users = []

    ## @var display_groups
    # List of DisplayGroups present within this workspace.
    self.display_groups = []

    ## @var tools
    # List of RayPointer, ... (tool) instances present within this workspace.
    self.tools = []

    ## @var size
    # Physical size of this workspace in meters.
    self.size = (3.8, 3.6)

    ## @var video_3D
    # Instance of Video3D capturing this workspace if it was associated.
    self.video_3D = None



  ## Computes a list of users whose tracking targets are not farer away than DISTANCE from a user, taking the line to ground.
  # @param POINT The point to compute the proximity to.
  # @param DISTANCE The tolerance distance to be applied.
  def get_all_users_in_range(self, POINT, DISTANCE):

    _users_in_range = []

    for _user in self.users:

      if Utilities.compute_point_to_line_distance(POINT, _user.headtracking_reader.sf_abs_vec.value, avango.gua.Vec3(0, -1, 0)) < DISTANCE:
        _users_in_range.append(_user)
        #print "In range", _user.id, Utilities.compute_point_to_line_distance(POINT, _user.headtracking_reader.sf_abs_vec.value, avango.gua.Vec3(0, -1, 0))

      else:
        pass
        #print "not in range", _user.id, Utilities.compute_point_to_line_distance(POINT, _user.headtracking_reader.sf_abs_vec.value, avango.gua.Vec3(0, -1, 0))

    return _users_in_range


  ## Creates a DisplayGroup instance and adds it to this workspace.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assiged to the display group.
  # @param VISIBILITY_TAG Tag used by the Tools' visibility matrices to define if they are visible for this display group.
  # @param OFFSET_TO_WORKSPACE Offset describing the origin of this display group with respect to the origin of the workspace.
  def create_display_group( self
                          , DISPLAY_LIST
                          , NAVIGATION_LIST
                          , VISIBILITY_TAG
                          , OFFSET_TO_WORKSPACE):

    _dg = DisplayGroup(len(self.display_groups), DISPLAY_LIST, NAVIGATION_LIST, VISIBILITY_TAG, OFFSET_TO_WORKSPACE, self.transmitter_offset)
    self.display_groups.append(_dg)

  ## Creates a User instance and adds it to this workspace.
  # To be called after all display groups have been created.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param AVATAR_VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied when HEADTRACKING_TARGET_NAME is None.
  def create_user( self
                 , VIP
                 , AVATAR_VISIBILITY_TABLE
                 , HEADTRACKING_TARGET_NAME
                 , EYE_DISTANCE
                 , NO_TRACKING_MAT = avango.gua.make_trans_mat(0,0,0)):
    
    _user = User()
    _user.my_constructor( self
                        , len(self.users)
                        , VIP
                        , AVATAR_VISIBILITY_TABLE
                        , HEADTRACKING_TARGET_NAME
                        , EYE_DISTANCE
                        , NO_TRACKING_MAT)

    self.users.append(_user)

  ## Creates a RayPointer instance and adds it to the tools of this workspace.
  # @param POINTER_TRACKING_STATION The tracking target name of this RayPointer.
  # @param POINTER_DEVICE_STATION The device station name of this RayPointer.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def create_ray_pointer( self
                        , POINTER_TRACKING_STATION
                        , POINTER_DEVICE_STATION
                        , VISIBILITY_TABLE):

    _ray_pointer = RayPointer()
    _ray_pointer.my_constructor( self
                               , len(self.tools)
                               , POINTER_TRACKING_STATION
                               , POINTER_DEVICE_STATION
                               , VISIBILITY_TABLE)
    self.tools.append(_ray_pointer)


  ## Creates a PortalCamera instance and adds it to the tools of this workspace.
  # @param CAMERA_TRACKING_STATION The tracking target name of this PortalCamera.
  # @param CAMERA_DEVICE_STATION The device station name of this PortalCamera.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags.
  def create_portal_cam( self
                       , CAMERA_TRACKING_STATION
                       , CAMERA_DEVICE_STATION
                       , VISIBILITY_TABLE):

    _portal_cam = PortalCamera()
    _portal_cam.my_constructor( self
                              , len(self.tools)
                              , CAMERA_TRACKING_STATION
                              , CAMERA_DEVICE_STATION
                              , VISIBILITY_TABLE)
    self.tools.append(_portal_cam)

  ## Creates a Video3D object and associates it to this workspace.
  # @param FILENAME The path of the video file to be associated.
  # @param OFFSET The offset matrix to be applied to the Video3D node.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags.
  def associate_video_3D( self
                        , FILENAME
                        , OFFSET
                        , VISIBILITY_TABLE ):

    self.video_3D = Video3D()
    self.video_3D.my_constructor(self
                               , FILENAME
                               , OFFSET
                               , VISIBILITY_TABLE)