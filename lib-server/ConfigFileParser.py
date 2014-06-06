#!/usr/bin/python

## @file
# Contains class ConfigFileParser.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ConsoleIO   import *

## Class associated to a ApplicationManager instance in order to parse and load XML configuration files for the setup.
#
# Gets a reference to ApplicationManager and calls the create_navigation and create_standard_user functions
# according to the settings read from the configuration file.

class ConfigFileParser:

  ## Custom constructor.
  # @param APPLICATION_MANAGER Reference to the one and only ApplicationManager instance in the setup.
  def __init__(self, APPLICATION_MANAGER):
    
    ## @var APPLICATION_MANAGER
    # Reference to the one and only ApplicationManager instance in the setup.
    self.APPLICATION_MANAGER = APPLICATION_MANAGER

    # global settings (can be overwritten by config file)
    ## @var enable_coupling_animation
    # Boolean indicating if an animation should be done when a coupling of Navigations is initiated.
    self.enable_coupling_animation = False


  ## Parses a XML configuration file, saves settings and creates navigations and users.
  # @param FILENAME The path of the configuration file to be read in.
  def parse(self, FILENAME):

    print_headline("Loading configuration file " + FILENAME)

    _in_comment = False
    _in_global = False
    _in_device = False
    _device_attributes = [None, None, None, 0, 0, 0, 0, [],              # [type, inputsensor, trackingstation, platformpos (x,y,z), platformrot (yaw), displays,
                          avango.gua.make_identity_mat(),                # transmitteroffset,
                          avango.gua.make_trans_mat(0.0, 1.5, 1.0),      # notrackingmat,
                          "joseph", [False, 0.75], False, 1.0, False]    # avatartype, ground_following_settings, enable_traces, scale, invert]
    _platform_size = [1.0, 1.0]                                          # [width, depth]
    _in_user = False
    _user_attributes = [None, None, False, False, None, None, 0.0]       # [headtrackingstation, startplatform, warnings, vip, glasses, hmd_sensor, eyedist]
    _navs_created = 0

    try:
      _config_file = open(FILENAME, 'r')
    except:
      print_error("Error: could not find configuration file " + str(FILENAME), True)

    _current_line = self.get_next_line_in_file(_config_file)

    while _current_line != "":
      
      # handle end of block comments
      if _in_comment and _current_line.rstrip().endswith("-->"):
        _in_comment = False
        _current_line = self.get_next_line_in_file(_config_file)
        continue
      elif _in_comment:
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # ignore one line comments
      if _current_line.startswith("<!--") and _current_line.rstrip().endswith("-->"):
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # handle start of block comments
      if _current_line.startswith("<!--"):
        _in_comment = True
        _current_line = self.get_next_line_in_file(_config_file)
        continue
      
      # ignore XML declaration
      if _current_line.startswith("<?xml"):
        _current_line = self.get_next_line_in_file(_config_file)
        continue
    
      # ignore doctype declaration
      if _current_line.startswith("<!DOCTYPE"):
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # ignore opening setup tag
      if _current_line.startswith("<setup>"):
        _current_line = self.get_next_line_in_file(_config_file)
        continue
      
      # detect end of configuration file
      if _current_line.startswith("</setup>"):
        break

      # detect start of global settings
      if _current_line.startswith("<global>"):
        _in_global = True
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      if _in_global:

        # get coupling animation boolean
        if _current_line.startswith("<animatecoupling>"):
          _current_line = _current_line.replace("<animatecoupling>", "")
          _current_line = _current_line.replace("</animatecoupling>", "")
          _current_line = _current_line.rstrip()
          if _current_line == "True":
            self.enable_coupling_animation = True

      # detect end of global settings
      if _current_line.startswith("</global>"):
        _in_global = False
        _current_line = self.get_next_line_in_file(_config_file)

        continue

      # detect start of device declaration
      if _current_line.startswith("<device>"):
        _in_device = True
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # read device values
      if _in_device:
        # get device type
        if _current_line.startswith("<type>"):
          _current_line = _current_line.replace("<type>", "")
          _current_line = _current_line.replace("</type>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[0] = _current_line
       
        # get inputsensor name
        if _current_line.startswith("<inputsensor>"):
          _current_line = _current_line.replace("<inputsensor>", "")
          _current_line = _current_line.replace("</inputsensor>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[1] = _current_line
        
        # get trackingstation name
        if _current_line.startswith("<trackingstation>"):
          _current_line = _current_line.replace("<trackingstation>", "")
          _current_line = _current_line.replace("</trackingstation>", "")
          _current_line = _current_line.rstrip()
          if _current_line != "None":
            _device_attributes[2] = _current_line

        # get display names
        if _current_line.startswith("<display>"):
          _current_line = _current_line.replace("<display>", "")
          _current_line = _current_line.replace("</display>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[7].append(_current_line)

        # get avatar type
        if _current_line.startswith("<avatartype>"):
          _current_line = _current_line.replace("<avatartype>", "")
          _current_line = _current_line.replace("</avatartype>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[10] = _current_line

        # get transmitter offset values
        if _current_line.startswith("<transmitteroffset>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<x>", "")
          _current_line = _current_line.replace("</x>", "")
          _current_line = _current_line.rstrip()
          _transmitter_x = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<y>", "")
          _current_line = _current_line.replace("</y>", "")
          _current_line = _current_line.rstrip()
          _transmitter_y = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<z>", "")
          _current_line = _current_line.replace("</z>", "")
          _current_line = _current_line.rstrip()
          _transmitter_z = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<rx>", "")
          _current_line = _current_line.replace("</rx>", "")
          _current_line = _current_line.rstrip()
          _transmitter_rx = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<ry>", "")
          _current_line = _current_line.replace("</ry>", "")
          _current_line = _current_line.rstrip()
          _transmitter_ry = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<rz>", "")
          _current_line = _current_line.replace("</rz>", "")
          _current_line = _current_line.rstrip()
          _transmitter_rz = float(_current_line)
          _device_attributes[8] = avango.gua.make_trans_mat(_transmitter_x, _transmitter_y, _transmitter_z) * \
                                  avango.gua.make_rot_mat(_transmitter_rz, 0, 0, 1) * \
                                  avango.gua.make_rot_mat(_transmitter_rx, 1, 0, 0) * \
                                  avango.gua.make_rot_mat(_transmitter_ry, 0, 1, 0)

        # get end of transmitter offset values
        if _current_line.startswith("</transmitteroffset>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get no tracking position values
        if _current_line.startswith("<notrackingposition>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<x>", "")
          _current_line = _current_line.replace("</x>", "")
          _current_line = _current_line.rstrip()
          _no_tracking_x = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<y>", "")
          _current_line = _current_line.replace("</y>", "")
          _current_line = _current_line.rstrip()
          _no_tracking_y = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<z>", "")
          _current_line = _current_line.replace("</z>", "")
          _current_line = _current_line.rstrip()
          _no_tracking_z = float(_current_line)
          _device_attributes[9] = avango.gua.make_trans_mat(_no_tracking_x, _no_tracking_y, _no_tracking_z)

        # get end of no tracking position values
        if _current_line.startswith("</notrackingposition>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get platform position values
        if _current_line.startswith("<platformpos>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<x>", "")
          _current_line = _current_line.replace("</x>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[3] = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<y>", "")
          _current_line = _current_line.replace("</y>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[4] = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<z>", "")
          _current_line = _current_line.replace("</z>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[5] = float(_current_line)

        # get end of platform position
        if _current_line.startswith("</platformpos>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get platform size values
        if _current_line.startswith("<platformsize>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<width>", "")
          _current_line = _current_line.replace("</width>", "")
          _current_line = _current_line.rstrip()
          _platform_size[0] = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<depth>", "")
          _current_line = _current_line.replace("</depth>", "")
          _current_line = _current_line.rstrip()
          _platform_size[1] = float(_current_line)

        # get end of platform size values
        if _current_line.startswith("</platformsize>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get platform rotation values
        if _current_line.startswith("<platformrot>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<yaw>", "")
          _current_line = _current_line.replace("</yaw>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[6] = float(_current_line)

        # get end of platform rotation
        if _current_line.startswith("</platformrot>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get scale
        if _current_line.startswith("<scale>"):
          _current_line = _current_line.replace("<scale>", "")
          _current_line = _current_line.replace("</scale>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[13] = float(_current_line)

        # get ground following attributes
        if _current_line.startswith("<groundfollowing>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<activated>", "")
          _current_line = _current_line.replace("</activated>", "")
          _current_line = _current_line.rstrip()
           
          if _current_line == "True":
            _device_attributes[11][0] = True
          else:
            _device_attributes[11][0] = False

          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<raystartheight>", "")
          _current_line = _current_line.replace("</raystartheight>", "")
          _current_line = _current_line.rstrip()
          _device_attributes[11][1] = float(_current_line)
        
        # get end of ground following attributes
        if _current_line.startswith("</groundfollowing>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get platformtraces boolean
        if _current_line.startswith("<movementtraces>"):
          _current_line = _current_line.replace("<movementtraces>", "")
          _current_line = _current_line.replace("</movementtraces>", "")
          _current_line = _current_line.rstrip()
          if _current_line == "True":
            _device_attributes[12] = True

        # get invert boolean
        if _current_line.startswith("<invert>"):
          _current_line = _current_line.replace("<invert>", "")
          _current_line = _current_line.replace("</invert>", "")
          _current_line = _current_line.rstrip()
          if _current_line == "True":
            _device_attributes[14] = True
      
      # detect end of device declaration
      if _current_line.startswith("</device>"):
        _in_device = False
       
        # error handling
        if _device_attributes[0] == None:
          print_error("No device type specified for navigation.", True)
        elif (_device_attributes[0] != "KeyboardMouse") and \
             (_device_attributes[0] != "Spacemouse") and \
             (_device_attributes[0] != "Globefish") and \
             (_device_attributes[0] != "XBoxController") and \
             (_device_attributes[0] != "OldSpheron") and \
             (_device_attributes[0] != "NewSpheron"):
          print_error("Unknown device type: " + _device_attributes[0], True)

        _starting_matrix = avango.gua.make_trans_mat(_device_attributes[3], _device_attributes[4], _device_attributes[5]) * \
                           avango.gua.make_rot_mat(_device_attributes[6], 0, 1, 0)
      
        self.APPLICATION_MANAGER.create_navigation(_device_attributes[0], 
                                                   _device_attributes[1],
                                                   _starting_matrix,
                                                   _platform_size,
                                                   _device_attributes[13],
                                                   self.enable_coupling_animation,
                                                   _device_attributes[12],
                                                   _device_attributes[14],
                                                   _device_attributes[9],
                                                   _device_attributes[11],
                                                   _device_attributes[8],
                                                   _device_attributes[7],
                                                   _device_attributes[10],
                                                   FILENAME,
                                                   _device_attributes[2])

        print_subheadline("Navigation loaded and created")
        print _device_attributes
        print "Platform size: ", _platform_size, "\n"
       
        # reset device attributes
        _device_attributes = [None, None, None, 0, 0, 0, 0, [],          # [type, inputsensor, trackingstation, platformpos (x,y,z), platformrot (yaw)), displays,
                          avango.gua.make_identity_mat(),                # transmitteroffset,
                          avango.gua.make_trans_mat(0.0, 1.5, 1.0),      # notrackingmat,
                          "joseph", [False, 0.75], False, 1.0, False]    # avatartype, groundfollowing_settings, enable_traces, scale, invert]
        _navs_created += 1
        _current_line = self.get_next_line_in_file(_config_file)
        continue
     
      # detect start of user declaration
      if _current_line.startswith("<user>"):
        _in_user = True
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # read user values
      if _in_user:

        # get headtracking station name
        if _current_line.startswith("<headtrackingstation>"):
          _current_line = _current_line.replace("<headtrackingstation>", "")
          _current_line = _current_line.replace("</headtrackingstation>", "")
          _current_line = _current_line.rstrip()
          if _current_line != "None":
            _user_attributes[0] = _current_line

        # get hmd sensor name
        if _current_line.startswith("<hmdsensor>"):
          _current_line = _current_line.replace("<hmdsensor>", "")
          _current_line = _current_line.replace("</hmdsensor>", "")
          _current_line = _current_line.rstrip()
          if _current_line != "None":
            _user_attributes[5] = _current_line

        # get starting platform name
        if _current_line.startswith("<eyedist>"):
          _current_line = _current_line.replace("<eyedist>", "")
          _current_line = _current_line.replace("</eyedist>", "")
          _current_line = _current_line.rstrip()
          _user_attributes[6] = float(_current_line)

        # get glasses id
        if _current_line.startswith("<glasses>"):
          _current_line = _current_line.replace("<glasses>", "")
          _current_line = _current_line.replace("</glasses>", "")
          _current_line = _current_line.rstrip()
          _user_attributes[4] = int(_current_line)

        # get starting platform name
        if _current_line.startswith("<startplatform>"):
          _current_line = _current_line.replace("<startplatform>", "")
          _current_line = _current_line.replace("</startplatform>", "")
          _current_line = _current_line.rstrip()
          _user_attributes[1] = int(_current_line)

        # get boolean for warning borders
        if _current_line.startswith("<warnings>"):
          _current_line = _current_line.replace("<warnings>", "")
          _current_line = _current_line.replace("</warnings>", "")
          _current_line = _current_line.rstrip()
          
          if _current_line == "True":
            _user_attributes[2] = True

        # get vip flag
        if _current_line.startswith("<vip>"):
          _current_line = _current_line.replace("<vip>", "")
          _current_line = _current_line.replace("</vip>", "")
          _current_line = _current_line.rstrip()
          
          if _current_line == "True":
            _user_attributes[3] = True

      # detect end of user declaration
      if _current_line.startswith("</user>"):
        _in_user = False

        # error handling
        if _user_attributes[1] >= _navs_created:
          print_error("User parsing: Navigation number to append to is too large.", True)

        self.APPLICATION_MANAGER.create_user(_user_attributes[3], _user_attributes[4], _user_attributes[1], _user_attributes[0], _user_attributes[5], _user_attributes[6], _user_attributes[2])

        print_subheadline("User loaded and created")
        print _user_attributes, "\n"

        _user_attributes = [None, None, False, False, None, None, 0.0]
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # go to next line in file
      _current_line = self.get_next_line_in_file(_config_file)

    print_subheadline("Global settings loaded")
    print "Coupling of Navigations animated:", self.enable_coupling_animation

    print_message("Configuration file " + FILENAME + " successfully loaded.")

  ## Gets the next line in the file. Thereby, empty lines are skipped.
  # @param FILE The opened file to get the line from.
  def get_next_line_in_file(self, FILE):
    _next_line = FILE.readline()
    _next_line = _next_line.replace(" ", "")

    # skip empty lines
    while _next_line == "\r\n":
      _next_line = FILE.readline()
      _next_line = _next_line.replace(" ", "")

    return _next_line
