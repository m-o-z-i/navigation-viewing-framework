#!/usr/bin/python

## @file
# Contains base class Display.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ConsoleIO import *

## 
class Display:

  ##
  def base_constructor( self
                      , name
                      , resolution
                      , size 
                      , stereo):

    ## @var name
    # A name to be associated to that display. Will be used in XML configuration file.
    self.name = name

    ## @var resolution
    # The display's resolution to be used.
    self.resolution = resolution

    ## @var size
    # A list of strings on which the windows for each user will pop up.
    self.size = size

    ## @var stereo
    # Boolean indicating if the stereo mode is to be used.
    self.stereo = stereo