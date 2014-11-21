#!/usr/bin/python

## @file
# avango daemon to initialize tracking and device stations.

# import avango-guacamole libraries
import avango.daemon

# import python libraries
import os
import sys
import subprocess

## Initizialies Oculus Rift sensors.
def init_oculus():
  _oculus = avango.daemon.Oculus()

  _oculus.stations[0] = avango.daemon.Station('oculus-0')
  _oculus.stations[1] = avango.daemon.Station('oculus-1')
  _oculus.stations[2] = avango.daemon.Station('oculus-2')

  print("Initialized 3 Oculus Rifts")
  device_list.append(_oculus)

## Initializes AR Track on LCD wall.
def init_lcd_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5000" # ART port at LCD wall
  
  _dtrack.stations[18] = avango.daemon.Station('tracking-oculus-stripe')   # oculus rift tracking
  _dtrack.stations[17] = avango.daemon.Station('tracking-oculus-front')    # oculus rift tracking
  _dtrack.stations[16] = avango.daemon.Station('tracking-oculus-stag')     # oculus rift tracking

  _dtrack.stations[3] = avango.daemon.Station('tracking-lcd-glasses-1')    # glasses powerwall user one
  _dtrack.stations[4] = avango.daemon.Station('tracking-lcd-glasses-2')    # glasses powerwall user two

  _dtrack.stations[7] = avango.daemon.Station('tracking-old-spheron')      # old spheron device

  device_list.append(_dtrack)
  print("ART Tracking started at LCD WALL")

## Initializes AR Track on DLP wall.
def init_dlp_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5002" # ART port at LED wall
  
  # glasses
  _dtrack.stations[1] = avango.daemon.Station('tracking-dlp-glasses-1')
  #_dtrack.stations[9] = avango.daemon.Station('tracking-dlp-glasses-1')     # camera shutter
  _dtrack.stations[2] = avango.daemon.Station('tracking-dlp-glasses-2')
  _dtrack.stations[3] = avango.daemon.Station('tracking-dlp-glasses-3')
  _dtrack.stations[4] = avango.daemon.Station('tracking-dlp-glasses-4')
  _dtrack.stations[5] = avango.daemon.Station('tracking-dlp-glasses-5')        
  _dtrack.stations[6] = avango.daemon.Station('tracking-dlp-glasses-6')

  # devices
  _dtrack.stations[19] = avango.daemon.Station('tracking-new-spheron')       # new spheron device

  _dtrack.stations[23] = avango.daemon.Station('tracking-dlp-pointer1')      # AUGUST1 pointer
  _dtrack.stations[26] = avango.daemon.Station('tracking-portal-camera-32')  # portal camera 3.2
  _dtrack.stations[25] = avango.daemon.Station('tracking-portal-camera-31')  # portal camera 3.1

  _dtrack.stations[20] = avango.daemon.Station('tracking-xbox-1')              # xbox target "horse"


  device_list.append(_dtrack)
  print("ART Tracking started at DLP WALL")


## Initializes touch input at the table.
def init_tuio_input():

  _tuio = avango.daemon.TUIOInput()
  _tuio.port = "3333" # tuio port

  offset = 0;
  for i in range(0, 20):
      _tuio.stations[i + offset] = avango.daemon.Station('gua-finger{}#cursor'.format(i))
  
  """
  offset = 20
  for i in range(0, 20):
      _tuio.stations[i + offset] = avango.daemon.Station('gua-finger{}#finger'.format(i))

  """
  
  offset = 20
  for i in range(0, 4):
      _tuio.stations[i + offset] = avango.daemon.Station('gua-finger{}#hand'.format(i))

  device_list.append(_tuio)


## Initializes a spacemouse for navigation.
def init_spacemouse():

  _string = os.popen("python find_device.py 1 3Dconnexion SpaceNavigator").read()

  if len(_string) == 0:
    _string = os.popen("python find_device.py 1 3Dconnexion SpaceTraveler USB").read()

  _string = _string.split()
  if len(_string) > 0:  

    _string = _string[0]
  
    # create a station to propagate the input events
    _spacemouse = avango.daemon.HIDInput()
    _spacemouse.station = avango.daemon.Station('device-spacemouse')
    _spacemouse.device = _string

    # map incoming spacemouse events to station values
    _spacemouse.values[0] = "EV_ABS::ABS_X"   # trans X
    _spacemouse.values[1] = "EV_ABS::ABS_Z"   # trans Y
    _spacemouse.values[2] = "EV_ABS::ABS_Y"   # trans Z
    _spacemouse.values[3] = "EV_ABS::ABS_RX"  # rotate X
    _spacemouse.values[4] = "EV_ABS::ABS_RZ"  # rotate Y
    _spacemouse.values[5] = "EV_ABS::ABS_RY"  # rotate Z

    # buttons
    _spacemouse.buttons[0] = "EV_KEY::BTN_0"  # left button
    _spacemouse.buttons[1] = "EV_KEY::BTN_1"  # right button

    device_list.append(_spacemouse)
    print("SpaceMouse started at:", _string)

  else:
    print("SpaceMouse NOT found !")

## Initializes an old spheron for navigation.
def init_old_spheron():

  _string = os.popen("python find_device.py 1 BUWEIMAR RAPID DEVEL DEVICE").read()
  _string = _string.split()

  if len(_string) > 0:
  
    _string = _string[0]

    # create a station to propagate the input events
    _spheron = avango.daemon.HIDInput()
    _spheron.station = avango.daemon.Station("device-old-spheron")
    _spheron.device = _string
    
    # map incoming spheron events to station values
    _spheron.values[0] = "EV_ABS::ABS_X"   # trans X    
    _spheron.values[1] = "EV_ABS::ABS_Y"   # trans Y
    _spheron.values[2] = "EV_ABS::ABS_Z"   # trans Z
    _spheron.values[3] = "EV_ABS::ABS_RX"  # rotate X
    _spheron.values[4] = "EV_ABS::ABS_RY"  # rotate Y
    _spheron.values[5] = "EV_ABS::ABS_RZ"  # rotate Z
    
    device_list.append(_spheron)
    
    print('Old Spheron started at:', _string)
    
  else:
    print("Old Spheron NOT found !")
    
  _string = os.popen("python find_device.py 1 PIXART USB OPTICAL MOUSE").read()
  _string = _string.split()

  if len(_string) > 0:
  
    _string = _string[0]
    
    # create a station to propagate the input events
    _spheron_buttons = avango.daemon.HIDInput()
    _spheron_buttons.station = avango.daemon.Station("device-old-spheron-buttons") 
    _spheron_buttons.device = _string
    
    # map buttons
    _spheron_buttons.buttons[0] = "EV_KEY::BTN_LEFT"   # left button
    _spheron_buttons.buttons[1] = "EV_KEY::BTN_MIDDLE" # middle button 
    _spheron_buttons.buttons[2] = "EV_KEY::BTN_RIGHT"  # right button
    
    device_list.append(_spheron_buttons)
    print('Old Spheron Buttons started at:', _string)
    
  else:
    print("Old Spheron ButTons NOT found !")

## Initializes a new spheron for navigation.
def init_new_spheron():

  _string_right = os.popen("python find_device.py 1 BUW Spheron").read()
  _string_left = os.popen("python find_device.py 2 BUW Spheron").read()

  _string_left = _string_left.split()
  _string_right = _string_right.split()

  if len(_string_right) > 0:
    
    _string1 = _string_right[0]

    # create a station to propagate the input events
    _spheron1 = avango.daemon.HIDInput()
    _spheron1.station = avango.daemon.Station("device-new-spheron-right")
    _spheron1.device = _string1
    _spheron1.timeout = '30'
    
    # map incoming events to station values
    _spheron1.values[0] = "EV_ABS::ABS_X"            # joystick trans x
    _spheron1.values[1] = "EV_ABS::ABS_Y"            # joystick trans y
    _spheron1.values[2] = "EV_ABS::ABS_Z"            # joystick trans z
    _spheron1.values[6] = "EV_ABS::ABS_THROTTLE"     # joystick rot y
    
    _spheron1.values[3] = "EV_REL::REL_RX" 
    _spheron1.values[4] = "EV_REL::REL_RY"
    _spheron1.values[5] = "EV_REL::REL_RZ"
    
    # buttons
    _spheron1.buttons[0] = "EV_KEY::BTN_B"           # left button
    _spheron1.buttons[1] = "EV_KEY::BTN_C"           # middle button
    _spheron1.buttons[2] = "EV_KEY::BTN_A"           # right button
    
    device_list.append(_spheron1)

    print("New Spheron (right) found at:", _string1)

  else:

    print("New Spheron (right) NOT found !")

  if len(_string_left) > 0:
    
    _string2 = _string_left[0]

    # create a station to propagate the input events
    _spheron2 = avango.daemon.HIDInput()
    _spheron2.station = avango.daemon.Station("device-new-spheron-left")
    _spheron2.device = _string2
    _spheron2.timeout = '30'
    
    # map incoming events to station values
    _spheron2.values[0] = "EV_ABS::ABS_X"            # joystick trans x
    _spheron2.values[1] = "EV_ABS::ABS_Y"            # joystick trans z
    _spheron2.values[2] = "EV_ABS::ABS_Z"            # joystick trans y
    _spheron2.values[3] = "EV_ABS::ABS_THROTTLE"     # joystick rot y      
        
    device_list.append(_spheron2)

    print("New Spheron (left) found at:", _string2)
  
  else:
    print("New Spheron (left) NOT found !")


## Initializes a new spheron for navigation.
def init_new_globefish():

  _string = os.popen("python find_device.py 1 BUW Spheron").read()
  _string = _string.split()

  if len(_string) > 0:
    
    _string1 = _string[0]

    # create a station to propagate the input events
    _globefish = avango.daemon.HIDInput()
    _globefish.station = avango.daemon.Station("device-new-globefish")
    _globefish.device = _string1
    _globefish.timeout = '30'
    
    # map incoming events to station values
    _globefish.values[0] = "EV_ABS::ABS_THROTTLE" # X
    _globefish.values[1] = "EV_ABS::ABS_Z" # Y    
    _globefish.values[2] = "EV_ABS::ABS_X" # Z
    
    _globefish.values[3] = "EV_REL::REL_RY" # PITCH
    _globefish.values[4] = "EV_REL::REL_RX" # HEAD 
    _globefish.values[5] = "EV_REL::REL_RZ" # ROLL
    
    # buttons
    # ...
        
    device_list.append(_globefish)

    print("New Globefish found at:", _string1)

  else:
    print("New Globefish NOT found !")
  


## Initalizes a mouse for navigation.
def init_mouse():

  _string = os.popen("python find_device.py 1 Logitech USB").read()
  _string = _string.split()

  if len(_string) > 0:
    
    _string1 = _string[0]

    # create a station to propagate the input events
    mouse = avango.daemon.HIDInput()
    mouse.station = avango.daemon.Station('device-mouse')
    mouse.device = _string1
    mouse.timeout = '30'

    mouse.values[0] = "EV_REL::REL_X"
    mouse.values[1] = "EV_REL::REL_Y"

    mouse.buttons[0] = "EV_KEY::BTN_LEFT"
    mouse.buttons[1] = "EV_KEY::BTN_MIDDLE"
    mouse.buttons[2] = "EV_KEY::BTN_RIGHT"

    device_list.append(mouse)

    print("Mouse started at:", _string1)

  else:
    print("Mouse NOT found !")

'''
## Initalizes a mouse for navigation.
def init_mouse():

  mouse_name = os.popen("ls /dev/input/by-id | grep \"-event-mouse\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

  mouse_name = mouse_name.split()
  if len(mouse_name) > 0:

    mouse_name = mouse_name[0]

    # create a station to propagate the input events
    mouse = avango.daemon.HIDInput()
    mouse.station = avango.daemon.Station('device-mouse')
    mouse.device = "/dev/input/by-id/" + mouse_name

    mouse.values[0] = "EV_REL::REL_X"
    mouse.values[1] = "EV_REL::REL_Y"

    mouse.buttons[0] = "EV_KEY::BTN_LEFT"
    mouse.buttons[1] = "EV_KEY::BTN_MIDDLE"
    mouse.buttons[2] = "EV_KEY::BTN_RIGHT"

    device_list.append(mouse)

    print "Mouse started at:", mouse_name

  else:
    print "Mouse NOT found !"
'''


## Initializes a keyboard for navigation.
def init_keyboard():

  keyboard_name = os.popen("ls /dev/input/by-id | grep \"-event-kbd\" | sed -e \'s/\"//g\'  | cut -d\" \" -f4").read()

  keyboard_name = keyboard_name.split()

  for i, name in enumerate(keyboard_name):
    
    # create a station to propagate the input events
    keyboard = avango.daemon.HIDInput()
    keyboard.station = avango.daemon.Station('device-keyboard' + str(i))
    keyboard.device = "/dev/input/by-id/" + name


    keyboard.buttons[0] = "EV_KEY::KEY_W"
    keyboard.buttons[1] = "EV_KEY::KEY_A"
    keyboard.buttons[2] = "EV_KEY::KEY_S"
    keyboard.buttons[3] = "EV_KEY::KEY_D"
    keyboard.buttons[4] = "EV_KEY::KEY_R"
    keyboard.buttons[5] = "EV_KEY::KEY_C"
    keyboard.buttons[6] = "EV_KEY::KEY_G"
    keyboard.buttons[7] = "EV_KEY::KEY_UP"
    keyboard.buttons[8] = "EV_KEY::KEY_DOWN"
    keyboard.buttons[9] = "EV_KEY::KEY_0"
    keyboard.buttons[10] = "EV_KEY::KEY_1"
    keyboard.buttons[11] = "EV_KEY::KEY_2"
    keyboard.buttons[12] = "EV_KEY::KEY_3"
    keyboard.buttons[13] = "EV_KEY::KEY_4"
    keyboard.buttons[14] = "EV_KEY::KEY_5"
    keyboard.buttons[15] = "EV_KEY::KEY_6"
    keyboard.buttons[16] = "EV_KEY::KEY_7"
    keyboard.buttons[17] = "EV_KEY::KEY_8"
    keyboard.buttons[18] = "EV_KEY::KEY_9"
    keyboard.buttons[19] = "EV_KEY::KEY_F1"
    keyboard.buttons[20] = "EV_KEY::KEY_F2"
    keyboard.buttons[21] = "EV_KEY::KEY_F3"
    keyboard.buttons[22] = "EV_KEY::KEY_F4"
    keyboard.buttons[23] = "EV_KEY::KEY_F5"
    keyboard.buttons[24] = "EV_KEY::KEY_F6"
    keyboard.buttons[25] = "EV_KEY::KEY_F7"
    keyboard.buttons[26] = "EV_KEY::KEY_F8"
    keyboard.buttons[27] = "EV_KEY::KEY_F9"
    keyboard.buttons[28] = "EV_KEY::KEY_F10"
    keyboard.buttons[29] = "EV_KEY::KEY_F11"
    keyboard.buttons[30] = "EV_KEY::KEY_F12"
    keyboard.buttons[31] = "EV_KEY::KEY_HOME"



    device_list.append(keyboard)

    print("Keyboard " + str(i) + " started at:", name)

## Initializes a X-Box controller for navigation.
def xbox_controller(PLAYER_NUMBER):

  _string = os.popen("python find_device.py " + str(PLAYER_NUMBER) + " Xbox 360 Wireless Receiver").read()
  _string = _string.split()

  if len(_string) > 0:
    _string = _string[0]
    
    # create a station to propagate the input events
    _xbox = avango.daemon.HIDInput()
    _xbox.station = avango.daemon.Station('device-xbox-' + str(PLAYER_NUMBER))
    _xbox.device = _string
    
    _xbox.values[0] = "EV_ABS::ABS_X"         # left joystick
    _xbox.values[1] = "EV_ABS::ABS_Y"         # left joystick
    _xbox.values[2] = "EV_ABS::ABS_RX"        # right joystick
    _xbox.values[3] = "EV_ABS::ABS_RY"        # right joystick

    _xbox.values[4] = "EV_ABS::ABS_Z"         # left bumper
    _xbox.values[5] = "EV_ABS::ABS_RZ"        # right bumper

    _xbox.buttons[0] = "EV_KEY::BTN_X"        # Button X
    _xbox.buttons[1] = "EV_KEY::BTN_B"        # Button B
    _xbox.buttons[2] = "EV_KEY::BTN_A"        # Button A
    _xbox.buttons[3] = "EV_KEY::BTN_Y"        # Button Y

    _xbox.buttons[4] = "EV_KEY::BTN_START"    # Start button
    _xbox.buttons[5] = "EV_KEY::BTN_SELECT"   # Select button

    _xbox.buttons[6] = "EV_KEY::BTN_TL"
    _xbox.buttons[7] = "EV_KEY::BTN_TR"

    device_list.append(_xbox)
    
    print("XBox Controller " + str(PLAYER_NUMBER) + " started at:", _string)
    
  else:
    print("XBox Controller NOT found !")


## Initializes the August pointing device.
def init_august_pointer(ID, DEVICE_STATION_STRING):

  _string = os.popen("python find_device.py 1 MOUSE USB MOUSE").read()
  _string = _string.split()

  if len(_string) > ID:
    
    _string = _string[ID]

    _pointer = avango.daemon.HIDInput()
    _pointer.station = avango.daemon.Station(DEVICE_STATION_STRING) # create a station to propagate the input events
    _pointer.device = _string
    #_pointer.timeout = '15'

    # map incoming events to station values
    _pointer.buttons[0] = "EV_KEY::KEY_F5" # front button
    #_pointer.buttons[0] = "EV_KEY::KEY_ESC" # front button
    _pointer.buttons[1] = "EV_KEY::KEY_PAGEDOWN" # back button
    _pointer.buttons[2] = "EV_KEY::KEY_PAGEUP" # center button

    device_list.append(_pointer)
    print('August Pointer found at:', _string)
    
    os.system("xinput --set-prop keyboard:'MOUSE USB MOUSE' 'Device Enabled' 0") # disable X-forwarding of events
    
  else:
    print("August Pointer NOT found !")

## Initializes a portal camera for portal features.
def init_portal_camera(VERSION_NUMBER):

  _string = os.popen("python find_device.py 1 portalCam " + str(VERSION_NUMBER)).read()
  _string = _string.split()

  if len(_string) > 0:  

    _string = _string[0]
  
    # create a station to propagate the input events
    _portal_camera = avango.daemon.HIDInput()
    _splitted_number = VERSION_NUMBER.split(".")
    _portal_camera.station = avango.daemon.Station('device-portal-camera-' + _splitted_number[0] + _splitted_number[1])
    _portal_camera.device = _string

    print('device-portal-camera' + _splitted_number[0] + _splitted_number[1])

    # map incoming portal camera buttons to station
    _portal_camera.buttons[0] = "EV_KEY::BTN_START"  # trigger button half step
    _portal_camera.buttons[1] = "EV_KEY::BTN_MODE"   # trigger button full step
    _portal_camera.buttons[2] = "EV_KEY::BTN_X"      # top left of trigger
    _portal_camera.buttons[3] = "EV_KEY::BTN_C"      # top right of trigger
    _portal_camera.buttons[4] = "EV_KEY::BTN_TL"     # top left button left
    _portal_camera.buttons[5] = "EV_KEY::BTN_Y"      # top left button right
    _portal_camera.buttons[6] = "EV_KEY::BTN_Z"      # top left button center
    _portal_camera.buttons[7] = "EV_KEY::BTN_TR2"    # left thumb left button
    _portal_camera.buttons[8] = "EV_KEY::BTN_SELECT" # left thumb right button
    _portal_camera.buttons[9] = "EV_KEY::BTN_B"      # top right button top
    _portal_camera.buttons[10] = "EV_KEY::BTN_DEAD"  # top right button bottom
    _portal_camera.buttons[11] = "EV_KEY::BTN_A"     # top right button center
    _portal_camera.buttons[12] = "EV_KEY::BTN_THUMBR"# right thumb left button
    _portal_camera.buttons[13] = "EV_KEY::BTN_THUMBL"# right thumb right button
    _portal_camera.buttons[14] = "EV_KEY::BTN_TL2"   # left and right head button
    _portal_camera.buttons[15] = "EV_KEY::BTN_TR"    # center head button


    device_list.append(_portal_camera)
    print("Portal Cam " + VERSION_NUMBER + " started at:", _string)

  else:
    print("Portal Cam " + VERSION_NUMBER + " NOT found !")

## @var device_list
# List of devices to be handled by daemon.
device_list = []

# init oculus rift sensors
#init_oculus()

# initialize trackings
init_lcd_wall_tracking()
init_dlp_wall_tracking()

# initialize x-box controllers
xbox_controller(1)
#xbox_controller(2)
#xbox_controller(3)
#xbox_controller(4)

# init spherons
init_old_spheron()
init_new_spheron()
#init_new_globefish()

# init pointers
init_august_pointer(0, "device-pointer1")

# init desktop devices
init_keyboard()
#init_mouse()
init_spacemouse()

# init portal camera
init_portal_camera("3.1")
init_portal_camera("3.2")

# init touch input
init_tuio_input() # crash ???

avango.daemon.run(device_list)
