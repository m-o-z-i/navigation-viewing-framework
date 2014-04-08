#!/usr/bin/python

## @file
# Contains class ConfigFileParser.

# import guacamole libraries
import avango
import avango.gua

## Class associated to a ViewingManager instance in order to parse and load XML configuration files for the setup.
#
# Gets a reference to ViewingManager and calls the create_navigation, create_powerwall_user, create_ovr_user and
# create_desktop_user according to the settings read from the configuration file.

class ConfigFileParser:

  ## Custom constructor.
  # @param VIEWING_MANAGER Reference to the one and only ViewingManager instance in the setup.
  def __init__(self, VIEWING_MANAGER):
    
    ## @param VIEWING_MANAGER
    # Reference to the one and only ViewingManager instance in the setup.
    self.VIEWING_MANAGER = VIEWING_MANAGER

    # global settings (can be overwritten by config file)
    ## @var transmitter_offset
    # Transmitter offset to be read in from configuration file
    #self.transmitter_offset = avango.gua.make_identity_mat()

    ## @var no_tracking_mat
    # Matrix to be used when no tracking is available to be read in from configuration file
    #self.no_tracking_mat = avango.gua.make_trans_mat(0.0, 1.5, 1.0)

    ## @var ground_following_settings
    # Settings for the GroundFollowing instance to be read in from configuration file: [activated, ray_start_height]
    self.ground_following_settings = [False, 0.75]

    ## @var enable_coupling_animation
    # Boolean indicating if an animation should be done when a coupling of Navigations is initiated.
    self.enable_coupling_animation = False

    ## @var enable_movementtraces
    #  Boolean indicating if the movement of every platform should be visualized by line segments.
    self.enable_movementtraces = False

  ## Parses a XML configuration file, saves settings and creates navigations and users.
  # @param FILENAME The path of the configuration file to be read in.
  def parse(self, FILENAME):
    print "\n=============================================================================="
    print "Loading configuration file", FILENAME
    print "==============================================================================\n"

    _in_comment = False
    _in_global = False
    _in_device = False
    _device_attributes = [None, None, None, 0, 0, 0, 0, [],              # [type, inputsensor, trackingstation, platformpos (x,y,z), platformrot (yaw), displays,
                          avango.gua.make_identity_mat(),                # transmitteroffset,
                          avango.gua.make_trans_mat(0.0, 1.5, 1.0),      # notrackingmat,
                          "joseph"]                                      # avatartype]
    _platform_size = [1.0, 1.0]                                          # [width, depth]
    _in_user = False
    _user_attributes = [None, None, None, False]                         # [type, headtrackingstation, startplatform, warnings]
    _window_size = [1920, 1080]                                          # [width, height]
    _screen_size = [1.6, 1.0]                                            # [width, height]
    _navs_created = 0

    _config_file = open(FILENAME, 'r')
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

        # get ground following attributes
        if _current_line.startswith("<groundfollowing>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<activated>", "")
          _current_line = _current_line.replace("</activated>", "")
          _current_line = _current_line.rstrip()
           
          if _current_line == "True":
            self.ground_following_settings[0] = True
          else:
            self.ground_following_settings[0] = False

          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<raystartheight>", "")
          _current_line = _current_line.replace("</raystartheight>", "")
          _current_line = _current_line.rstrip()
          self.ground_following_settings[1] = float(_current_line)
        
        # get end of ground following attributes
        if _current_line.startswith("</groundfollowing>"):
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        # get coupling animation boolean
        if _current_line.startswith("<animatecoupling>"):
          _current_line = _current_line.replace("<animatecoupling>", "")
          _current_line = _current_line.replace("</animatecoupling>", "")
          _current_line = _current_line.rstrip()
          if _current_line == "True":
            self.enable_coupling_animation = True

        # get platformtraces boolean
        if _current_line.startswith("<movementtraces>"):
          _current_line = _current_line.replace("<movementtraces>", "")
          _current_line = _current_line.replace("</movementtraces>", "")
          _current_line = _current_line.rstrip()
          if _current_line == "True":
            self.enable_movementtraces = True

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
          _device_attributes[8] = avango.gua.make_trans_mat(_transmitter_x, _transmitter_y, _transmitter_z)

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
      
      # detect end of device declaration
      if _current_line.startswith("</device>"):
        _in_device = False
       
        # error handling
        if _device_attributes[0] == None:
          raise IOError("No device type specified for navigation.")
        elif (_device_attributes[0] != "KeyboardMouse") and \
             (_device_attributes[0] != "Spacemouse") and \
             (_device_attributes[0] != "XBoxController") and \
             (_device_attributes[0] != "OldSpheron") and \
             (_device_attributes[0] != "NewSpheron"):
          raise IOError("Unknown device type: " + _device_attributes[0])

        _starting_matrix = avango.gua.make_trans_mat(_device_attributes[3], _device_attributes[4], _device_attributes[5]) * \
                           avango.gua.make_rot_mat(_device_attributes[6], 0, 1, 0)
      
        self.VIEWING_MANAGER.create_navigation(_device_attributes[0], 
                                               _device_attributes[1],
                                               _starting_matrix,
                                               _platform_size,
                                               self.enable_coupling_animation,
                                               self.enable_movementtraces,
                                               _device_attributes[9],
                                               self.ground_following_settings,
                                               _device_attributes[8],
                                               _device_attributes[7],
                                               _device_attributes[10],
                                               FILENAME,
                                               _device_attributes[2])

        print "Navigation loaded and created:"
        print "------------------------------"
        print _device_attributes
        print "Platform size: ", _platform_size, "\n"
        
        # reset device attributes
        _device_attributes = [None, None, None, 0, 0, 0, 0, [],          # [type, inputsensor, trackingstation, platformpos (x,y,z), platformrot (yaw)), displays,
                          avango.gua.make_identity_mat(),                # transmitteroffset,
                          avango.gua.make_trans_mat(0.0, 1.5, 1.0),      # notrackingmat,
                          "joseph"]                                      # avatartype]
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
        # get user type
        if _current_line.startswith("<type>"):
          _current_line = _current_line.replace("<type>", "")
          _current_line = _current_line.replace("</type>", "")
          _current_line = _current_line.rstrip()
          _user_attributes[0] = _current_line
        
        # get headtracking station name
        if _current_line.startswith("<headtrackingstation>"):
          _current_line = _current_line.replace("<headtrackingstation>", "")
          _current_line = _current_line.replace("</headtrackingstation>", "")
          _current_line = _current_line.rstrip()
          if _current_line != "None":
            _user_attributes[1] = _current_line

        # get starting platform name
        if _current_line.startswith("<startplatform>"):
          _current_line = _current_line.replace("<startplatform>", "")
          _current_line = _current_line.replace("</startplatform>", "")
          _current_line = _current_line.rstrip()
          _user_attributes[2] = int(_current_line)

        # get window size values
        if _current_line.startswith("<windowsize>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<width>", "")
          _current_line = _current_line.replace("</width>", "")
          _current_line = _current_line.rstrip()
          _window_size[0] = int(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<height>", "")
          _current_line = _current_line.replace("</height>", "")
          _current_line = _current_line.rstrip()
          _window_size[1] = int(_current_line)

        # get screen size values
        if _current_line.startswith("<screensize>"):
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<width>", "")
          _current_line = _current_line.replace("</width>", "")
          _current_line = _current_line.rstrip()
          _screen_size[0] = float(_current_line)
          _current_line = self.get_next_line_in_file(_config_file)
          _current_line = _current_line.replace("<height>", "")
          _current_line = _current_line.replace("</height>", "")
          _current_line = _current_line.rstrip()
          _screen_size[1] = float(_current_line)

        # get boolean for warning borders
        if _current_line.startswith("<warnings>"):
          _current_line = _current_line.replace("<warnings>", "")
          _current_line = _current_line.replace("</warnings>", "")
          _current_line = _current_line.rstrip()
          
          if _current_line == "True":
            _user_attributes[3] = True

      # detect end of user declaration
      if _current_line.startswith("</user>"):
        _in_user = False

        # error handling
        if _user_attributes[2] >= _navs_created:
          raise IOError("Navigation number to append to is too large.")
        elif (_user_attributes[0] != "LargePowerWallUser") and \
             (_user_attributes[0] != "SmallPowerWallUser") and \
             (_user_attributes[0] != "OVRUser") and \
             (_user_attributes[0] != "DesktopUser"):
          raise IOError("Unknown user type: " + _user_attributes[0])

        if _user_attributes[0] == "SmallPowerWallUser":
          self.VIEWING_MANAGER.create_powerwall_user(_user_attributes[1], _user_attributes[2], self.transmitter_offset, _user_attributes[3], self.no_tracking_mat, "small")
        elif _user_attributes[0] == "LargePowerWallUser":
          self.VIEWING_MANAGER.create_powerwall_user(_user_attributes[1], _user_attributes[2], self.transmitter_offset, _user_attributes[3], self.no_tracking_mat, "large")
        elif _user_attributes[0] == "OVRUser":
          print "Oculus Rift Messages:"
          print "----------------------"
          self.VIEWING_MANAGER.create_ovr_user(_user_attributes[1], _user_attributes[2], _user_attributes[3], self.no_tracking_mat)
        elif _user_attributes[0] == "DesktopUser":
          self.VIEWING_MANAGER.create_desktop_user(_user_attributes[2], _window_size, _screen_size)
        else:
          print "Unknown user type", _user_attributes[0]
          _current_line = self.get_next_line_in_file(_config_file)
          continue

        print "\nUser loaded and created:"
        print "-------------------------"
        print _user_attributes, "\n"

        if _user_attributes[0] == "DesktopUser":
          print "Window resolution:", _window_size[0], "x", _window_size[1]
          print "Screen size:", _screen_size[0], "x", _screen_size[1], "\n"
          # restore default values
          _window_size = [1920, 1080]
          _screen_size = [1.6, 1.0]

        _user_attributes = [None, None, None, False]
        _current_line = self.get_next_line_in_file(_config_file)
        continue

      # go to next line in file
      _current_line = self.get_next_line_in_file(_config_file)

    print "Global settings loaded:"
    print "------------------------"
    print "Ground Following settings:", self.ground_following_settings
    print "Coupling of Navigations animated:", self.enable_coupling_animation
    print "Movement traces animated:", self.enable_movementtraces, "\n"

    print "\n=============================================================================="
    print "Configuration file", FILENAME, "successfully loaded."
    print "=============================================================================="

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