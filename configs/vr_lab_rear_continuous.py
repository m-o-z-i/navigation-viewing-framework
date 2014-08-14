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
spheron_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 0) * \
                                                     avango.gua.make_rot_mat(0, 0, 1, 0)
                                 , STARTING_SCALE = 1.0
                                 , INPUT_DEVICE_TYPE = 'Spacemouse'
                                 , INPUT_DEVICE_NAME = 'device-spacemouse'
                                 , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.75, 1.6)
                                 , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                 , MOVEMENT_TRACES = False
                                 , INVERT = False
                                 , AVATAR_TYPE = 'joseph'
                                 , DEVICE_TRACKING_NAME = 'tracking-new-spheron')

spacemouse_navigation = SteeringNavigation()
spacemouse_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 0) * \
                                                        avango.gua.make_rot_mat(0, 0, 1, 0)
                                    , STARTING_SCALE = 1.0
                                    , INPUT_DEVICE_TYPE = 'Spacemouse'
                                    , INPUT_DEVICE_NAME = 'device-spacemouse'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                    , MOVEMENT_TRACES = True
                                    , INVERT = False
                                    , AVATAR_TYPE = None
                                    , DEVICE_TRACKING_NAME = None)

## Create Display instances. ##
large_powerwall = LargePowerwall()
touch_table_3D = TouchTable3D()

displays = [large_powerwall, touch_table_3D]

## Create display groups ##
vr_lab_rear.create_display_group( DISPLAY_LIST = [large_powerwall, touch_table_3D]
                                , NAVIGATION_LIST = [spheron_navigation]
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0, 0, 1.6) )

## Create users ##
vr_lab_rear.create_user( VIP = False
                       , GLASSES_ID = 1
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-1'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , GLASSES_ID = 4
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-4'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , GLASSES_ID = 5
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-5'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , GLASSES_ID = 6
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-6'
                       , EYE_DISTANCE = 0.065)