#!/usr/bin/python

## @file
# Contains workspace, display, navigation, display group and user configuration classes to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from DisplayGroup import *
from PhysicalDisplay import *
from Portal import *
from Workspace import Workspace
from SteeringNavigation import SteeringNavigation
from StaticNavigation import StaticNavigation

## Create Workspaces first ##
vr_lab_rear = Workspace('VR-Lab-Rear', avango.gua.make_trans_mat(0.0, 0.043, 0.0))

workspaces = [vr_lab_rear]

## Create Navigation instances ##
trace_visibility_list_table_nav = {  "dlp_wall"  : False
                                   , "table" : False 
                                   , "portal" : False
                                  }



spacemouse_navigation = SteeringNavigation()
spacemouse_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 20) * \
                                                        avango.gua.make_rot_mat(0, 0, 1, 0)
                                    , STARTING_SCALE = 50.0
                                    , INPUT_DEVICE_TYPE = 'Spacemouse'
                                    , INPUT_DEVICE_NAME = 'device-spacemouse'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , GROUND_FOLLOWING_SETTINGS = [False, 0.75]
                                    , INVERT = True
                                    , TRACE_VISIBILITY_LIST = trace_visibility_list_table_nav
                                    , DEVICE_TRACKING_NAME = None
                                    , REACTS_ON_PORTAL_TRANSIT = False)


## Create Display instances. ##
touch_table_3D = TouchTable3D()

displays = [touch_table_3D]

## Create display groups ##


vr_lab_rear.create_display_group( DISPLAY_LIST = [touch_table_3D]
                                , NAVIGATION_LIST = [spacemouse_navigation]
                                , VISIBILITY_TAG = "table"
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0.6975, -0.96, 1.9825) * \
                                                        avango.gua.make_rot_mat(-90, 0, 1, 0) )


## Create users ##
avatar_visibility_table = { "table" : {"portal" : False}
                          , "portal" : {"table" : False}
                          }

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-6'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-4'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-3'
                       , EYE_DISTANCE = 0.065)

## Create tools ##

# visibility table
# format: A : { B : bool}
# interpretation: does display with tag A see representation of tool in displays with tag B?
"""
tool_visibility_table = {
                          "dlp_wall"  : {"table" : False, "portal" : False}
                        , "table" : {"dlp_wall" : True, "portal" : False}  
                        , "portal" : {"dlp_wall" : True, "table" : False}
                       }

vr_lab_rear.create_ray_pointer( POINTER_TRACKING_STATION = 'tracking-dlp-pointer1' 
                              , POINTER_DEVICE_STATION = 'device-pointer1'
                              , VISIBILITY_TABLE = tool_visibility_table)

vr_lab_rear.create_portal_cam(  CAMERA_TRACKING_STATION = 'tracking-portal-camera-32'
                             ,  CAMERA_DEVICE_STATION = 'device-portal-camera-32'
                             ,  VISIBILITY_TABLE = tool_visibility_table)
"""

## Create portal navigations. ##
'''
tower_portal_1_nav = StaticNavigation()
tower_portal_1_nav.my_constructor(STATIC_ABS_MAT = avango.gua.make_trans_mat(-12.0, 17.3, -7.0)
                                , STATIC_SCALE = 1.0)

tower_portal_2_nav = StaticNavigation()
tower_portal_2_nav.my_constructor(STATIC_ABS_MAT = avango.gua.make_trans_mat(-23.0, 1.3, 21.0) * avango.gua.make_rot_mat(-90, 0, 1, 0)
                                , STATIC_SCALE = 1.0)

## Create portal displays. ##
tower_portal_1 = Portal(PORTAL_MATRIX = avango.gua.make_trans_mat(-23.0, 1.3, 21.0) * avango.gua.make_rot_mat(90, 0, 1, 0)
                      , WIDTH = 4.0
                      , HEIGHT = 2.6
                      , VIEWING_MODE = "3D"
                      , CAMERA_MODE = "PERSPECTIVE"
                      , NEGATIVE_PARALLAX = "False"
                      , BORDER_MATERIAL = "data/materials/White.gmd"
                      , TRANSITABLE = True)

side_portal = Portal(PORTAL_MATRIX = avango.gua.make_trans_mat(-21.0, 1.3, 19.0)
                      , WIDTH = 4.0
                      , HEIGHT = 2.6
                      , VIEWING_MODE = "3D"
                      , CAMERA_MODE = "PERSPECTIVE"
                      , NEGATIVE_PARALLAX = "False"
                      , BORDER_MATERIAL = "data/materials/White.gmd"
                      , TRANSITABLE = True)

tower_portal_2 = Portal(PORTAL_MATRIX = avango.gua.make_trans_mat(-12.0, 17.3, -7.0) * avango.gua.make_rot_mat(180, 0, 1, 0)
                      , WIDTH = 4.0
                      , HEIGHT = 2.6
                      , VIEWING_MODE = "3D"
                      , CAMERA_MODE = "PERSPECTIVE"
                      , NEGATIVE_PARALLAX = "False"
                      , BORDER_MATERIAL = "data/materials/White.gmd"
                      , TRANSITABLE = True)

## Create virtual display groups ##
tower_portal_1_dg = DisplayGroup(ID = None
                               , DISPLAY_LIST = [tower_portal_1, side_portal]
                               , NAVIGATION_LIST = [tower_portal_1_nav]
                               , VISIBILITY_TAG = "portal"
                               , OFFSET_TO_WORKSPACE = avango.gua.make_identity_mat()
                               , WORKSPACE_TRANSMITTER_OFFSET = avango.gua.make_identity_mat()
                               )

tower_portal_2_dg = DisplayGroup(ID = None
                               , DISPLAY_LIST = [tower_portal_2]
                               , NAVIGATION_LIST = [tower_portal_2_nav]
                               , VISIBILITY_TAG = "portal"
                               , OFFSET_TO_WORKSPACE = avango.gua.make_identity_mat()
                               , WORKSPACE_TRANSMITTER_OFFSET = avango.gua.make_identity_mat()
                               )

portal_display_groups = [tower_portal_1_dg, tower_portal_2_dg]
'''
portal_display_groups = []
