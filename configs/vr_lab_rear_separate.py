#!/usr/bin/python

## @file
# Contains workspace, display, navigation, display group and user configuration classes to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from Display import *
from Workspace import Workspace
from SteeringNavigation import SteeringNavigation

## Create Workspaces first ##
vr_lab_rear = Workspace('VR-Lab-Rear', avango.gua.make_trans_mat(0.0, 0.043, 0.0))

workspaces = [vr_lab_rear]

## Create Navigation instances ##
spheron_navigation = SteeringNavigation()
spheron_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 15) * \
                                                     avango.gua.make_rot_mat(0, 0, 1, 0)
                                 , STARTING_SCALE = 1.0
                                 , INPUT_DEVICE_TYPE = 'NewSpheron'
                                 , INPUT_DEVICE_NAME = 'device-new-spheron'
                                 , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.75, 1.6)
                                 , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                 , MOVEMENT_TRACES = False
                                 , INVERT = False
                                 , DEVICE_TRACKING_NAME = 'tracking-new-spheron')

spacemouse_navigation = SteeringNavigation()
spacemouse_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 20) * \
                                                        avango.gua.make_rot_mat(0, 0, 1, 0)
                                    , STARTING_SCALE = 50.0
                                    , INPUT_DEVICE_TYPE = 'Spacemouse'
                                    , INPUT_DEVICE_NAME = 'device-spacemouse'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , GROUND_FOLLOWING_SETTINGS = [False, 0.75]
                                    , MOVEMENT_TRACES = False
                                    , INVERT = False
                                    , DEVICE_TRACKING_NAME = None)


xbox_navigation = SteeringNavigation()
xbox_navigation.my_constructor(       STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 0)
                                    , STARTING_SCALE = 1.0
                                    , INPUT_DEVICE_TYPE = 'XBoxController'
                                    , INPUT_DEVICE_NAME = 'device-xbox-1'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.2, 0.6)
                                    , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                    , MOVEMENT_TRACES = False
                                    , INVERT = False
                                    , DEVICE_TRACKING_NAME = 'tracking-xbox-1'
                                    , IS_REQUESTABLE = True
                                    , REQUEST_BUTTON_NUM = 3)

## Create Display instances. ##
large_powerwall = LargePowerwall()
touch_table_3D = TouchTable3D()

displays = [large_powerwall, touch_table_3D]

## Create display groups ##
vr_lab_rear.create_display_group( DISPLAY_LIST = [large_powerwall]
                                , NAVIGATION_LIST = [spheron_navigation, xbox_navigation]
                                , VISIBILITY_TAG = "wall"
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0, 0, 1.6) )

vr_lab_rear.create_display_group( DISPLAY_LIST = [touch_table_3D]
                                , NAVIGATION_LIST = [spacemouse_navigation]
                                , VISIBILITY_TAG = "table"
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0.79, -0.96, 1.96) * \
                                                        avango.gua.make_rot_mat(-90, 0, 1, 0) )

## Create users ##
avatar_visibility_table = {
                            "wall"  : {"table" : False}
                          , "table" : {"wall" : True} 
                          }

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-4'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-5'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-6'
                       , EYE_DISTANCE = 0.065)

## Create tools ##


# visibility table
# format: A : { B : bool}
# interpretation: does display with tag A see representation of tool in displays with tag B?
ray_visibility_table = {
                          "wall"  : {"table" : False}
                        , "table" : {"wall" : True}  
                       }

vr_lab_rear.create_ray_pointer( POINTER_TRACKING_STATION = 'tracking-dlp-pointer1' 
                              , POINTER_DEVICE_STATION = 'device-pointer1'
                              , VISIBILITY_TABLE = ray_visibility_table)