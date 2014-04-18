#!/usr/bin/python

## @file
# Contains a function for parsing configuration files for client purposes.

# import avango-guacamole libraries
import avango
import avango.gua

## Parses the configuration file in order to find out the attributes of this client's users
# Outputs a list of lists of user attributes in the format:
# [stereo, headtrackingstation, startplatform, user_id, transmitteroffset, notrackingmat]
# In case resolution and screensize are not needed, the value 0 is saved.
# @param CONFIG_FILE The configuration file to parse.
# @param PLATFORM_ID The platform id to look for users on.
def parse(CONFIG_FILE, PLATFORM_ID):
  _in_user = False
  _in_comment = False
  _in_global = False
  _in_device = False

  _user_list = []
  _user_count = 0

  _transmitter_offsets = []
  _no_tracking_mats = []

  _user_attributes = [None, None, None, 0, avango.gua.make_identity_mat(), avango.gua.make_trans_mat(0.0, 1.5, 1.0)]

  _config_file = open(CONFIG_FILE, 'r')
  _current_line = get_next_line_in_file(_config_file)

  while _current_line != "":

    # handle end of block comments
    if _in_comment and _current_line.rstrip().endswith("-->"):
      _in_comment = False
      _current_line = get_next_line_in_file(_config_file)
      continue
    elif _in_comment:
      _current_line = get_next_line_in_file(_config_file)
      continue

    # ignore one line comments
    if _current_line.startswith("<!--") and _current_line.rstrip().endswith("-->"):
      _current_line = get_next_line_in_file(_config_file)
      continue

    # handle start of block comments
    if _current_line.startswith("<!--"):
      _in_comment = True
      _current_line = get_next_line_in_file(_config_file)
      continue
    
    # ignore XML declaration
    if _current_line.startswith("<?xml"):
      _current_line = get_next_line_in_file(_config_file)
      continue
  
    # ignore doctype declaration
    if _current_line.startswith("<!DOCTYPE"):
      _current_line = get_next_line_in_file(_config_file)
      continue

    # ignore opening setup tag
    if _current_line.startswith("<setup>"):
      _current_line = get_next_line_in_file(_config_file)
      continue
    
    # detect end of configuration file
    if _current_line.startswith("</setup>"):
      break

    # detect start of device declaration
    if _current_line.startswith("<device>"):
      _in_device = True
      _current_line = get_next_line_in_file(_config_file)
      continue

    # read device values
    if _in_device:

      # get transmitter offset values
      if _current_line.startswith("<transmitteroffset>"):
        _current_line = get_next_line_in_file(_config_file)
        _current_line = _current_line.replace("<x>", "")
        _current_line = _current_line.replace("</x>", "")
        _current_line = _current_line.rstrip()
        _transmitter_x = float(_current_line)
        _current_line = get_next_line_in_file(_config_file)
        _current_line = _current_line.replace("<y>", "")
        _current_line = _current_line.replace("</y>", "")
        _current_line = _current_line.rstrip()
        _transmitter_y = float(_current_line)
        _current_line = get_next_line_in_file(_config_file)
        _current_line = _current_line.replace("<z>", "")
        _current_line = _current_line.replace("</z>", "")
        _current_line = _current_line.rstrip()
        _transmitter_z = float(_current_line)
        _transmitter_offsets.append(avango.gua.make_trans_mat(_transmitter_x, _transmitter_y, _transmitter_z))

      # get end of transmitter offset values
      if _current_line.startswith("</transmitteroffset>"):
        _current_line = get_next_line_in_file(_config_file)
        continue

      # get no tracking position values
      if _current_line.startswith("<notrackingposition>"):
        _current_line = get_next_line_in_file(_config_file)
        _current_line = _current_line.replace("<x>", "")
        _current_line = _current_line.replace("</x>", "")
        _current_line = _current_line.rstrip()
        _no_tracking_x = float(_current_line)
        _current_line = get_next_line_in_file(_config_file)
        _current_line = _current_line.replace("<y>", "")
        _current_line = _current_line.replace("</y>", "")
        _current_line = _current_line.rstrip()
        _no_tracking_y = float(_current_line)
        _current_line = get_next_line_in_file(_config_file)
        _current_line = _current_line.replace("<z>", "")
        _current_line = _current_line.replace("</z>", "")
        _current_line = _current_line.rstrip()
        _no_tracking_z = float(_current_line)
        _no_tracking_mats.append(avango.gua.make_trans_mat(_no_tracking_x, _no_tracking_y, _no_tracking_z))

      # get end of no tracking position values
      if _current_line.startswith("</notrackingposition>"):
        _current_line = get_next_line_in_file(_config_file)
        continue

    # detect start of user declaration
    if _current_line.startswith("<user>"):
      _in_user = True
      _current_line = get_next_line_in_file(_config_file)
      continue

    # read user values
    if _in_user:

      # get stereo value
      if _current_line.startswith("<stereo>"):
        _current_line = _current_line.replace("<stereo>", "")
        _current_line = _current_line.replace("</stereo>", "")
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

    # detect end of user declaration
    if _current_line.startswith("</user>"):
      _in_user = False
      
      # determine transmitter offset and no tracking mat
      _user_attributes[4] = _transmitter_offsets[int(PLATFORM_ID)]
      _user_attributes[5] = _no_tracking_mats[int(PLATFORM_ID)]

      # find out user id and increment counters
      _user_attributes[3] = _user_count
      _user_count += 1

      # append user to list if he belongs to platform responsible for
      if int(_user_attributes[2]) == int(PLATFORM_ID):
        _user_list.append(list(_user_attributes))

      _user_attributes = [None, None, None, 0, avango.gua.make_identity_mat(), avango.gua.make_trans_mat(0.0, 1.5, 1.0)]
      _current_line = get_next_line_in_file(_config_file)
      continue

    # go to next line in file
    _current_line = get_next_line_in_file(_config_file)

  return _user_list

## Gets the next line in the file. Thereby, empty lines are skipped.
# @param FILE The opened file to get the line from.
def get_next_line_in_file(FILE):
  _next_line = FILE.readline()
  _next_line = _next_line.replace(" ", "")

  # skip empty lines
  while _next_line == "\r\n":
    _next_line = FILE.readline()
    _next_line = _next_line.replace(" ", "")

  return _next_line
