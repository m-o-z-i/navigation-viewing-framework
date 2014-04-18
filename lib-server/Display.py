#!/usr/bin/python

## @file
# Contains class Display.

# import avango-guacamole libraries
import avango
import avango.gua

## Class representing a display. A display is a physical projection medium
# running on a host and having certain resolution, size and transformation. It
# supports a specific amount of users. In the Platform class, a screen node 
# is associated for each display.
class Display:
  
  ## Custom constructor
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__( self
              , hostname
              , name = None
              , resolution = (2560, 1440)
              , displaystrings = [":0.0"]
              , size = (0.595, 0.335)
              , transformation = avango.gua.make_trans_mat(0.0, 1.75, 0.0)
              ):

    # save values in members
    self.hostname = hostname
    
    # default naming for desktop setups
    if not name:
      self.name = hostname + "_display"
    else:
      self.name = name

    self.resolution = resolution
    self.displaystrings = displaystrings
    self.size = size
    self.transformation = transformation

    # init counter
    self.num_users = 0

  ## Registers a new user at this display and return the display string assigned to the new user.
  def register_user(self):
    user_num = self.num_users
    if user_num < len(self.displaystrings):
      self.num_users += 1
      return [self.displaystrings[user_num]]
    else:
      return None

  ## Creates the screen node of this display to be appended to the Platform transformation node.
  # @param name The name of the screen scenegraph node.
  def create_screen_node(self, name = "screen_node"):
    _screen = avango.gua.nodes.ScreenNode(Name = name)
    _w, _h = self.size
    _screen.Width.value = _w
    _screen.Height.value = _h
    _screen.Transform.value = self.transformation
    return _screen