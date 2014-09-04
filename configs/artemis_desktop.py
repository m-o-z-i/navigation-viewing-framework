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
from StaticNavigation import StaticNavigation

## Create Workspaces first ##
artemis = Workspace('artemis', avango.gua.make_trans_mat(0.0, 0.043, 0.0))

workspaces = [artemis]

## Create Navigation instances ##
spacemouse_navigation = SteeringNavigation()
spacemouse_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 0)
                                    , STARTING_SCALE = 1.0
                                    , INPUT_DEVICE_TYPE = 'Spacemouse'
                                    , INPUT_DEVICE_NAME = 'device-spacemouse'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.2, 0.6)
                                    , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                    , MOVEMENT_TRACES = True
                                    , INVERT = False
                                    , AVATAR_TYPE = 'joseph'
                                    , DEVICE_TRACKING_NAME = None)

keyboard_navigation = SteeringNavigation()
keyboard_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0, 0, 0)
                                    , STARTING_SCALE = 1.0
                                    , INPUT_DEVICE_TYPE = 'KeyboardMouse'
                                    , INPUT_DEVICE_NAME = None
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.2, 0.6)
                                    , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                    , MOVEMENT_TRACES = True
                                    , INVERT = False
                                    , AVATAR_TYPE = 'joseph'
                                    , DEVICE_TRACKING_NAME = None)

static_navigation = StaticNavigation()
static_navigation.my_constructor(STATIC_ABS_MAT = avango.gua.make_trans_mat(0, 10, 10)
                               , STATIC_SCALE = 1.0
                               , AVATAR_TYPE = 'joseph')

## Create Display instances. ##
artemis_desktop_display = Display(hostname = "artemis", transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0))

displays = [artemis_desktop_display]

## Create display groups ##
artemis.create_display_group( DISPLAY_LIST = [artemis_desktop_display]
                             , NAVIGATION_LIST = [spacemouse_navigation, keyboard_navigation, static_navigation]
                             , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0, 0, 0) )

## Create users ##
artemis.create_user(  VIP = False
                    , GLASSES_ID = None
                    , HEADTRACKING_TARGET_NAME = None
                    , EYE_DISTANCE = 0.065
                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.2, 0.6))