#!/usr/bin/python

# import avango-guacamole libraries
import avango
import avango.gua

from display_config import display_config

def create_displays():
	displays = [ ]
	for config in display_config:
		if ("name" and "hostname") in config:
			displays.append(Display(config))
	return displays


class Display:

	DEFAULT_DISPLAYSTRINGS 	= [":0.0"]
	DEFAULT_RESOLUTION			= (800, 600)
	DEFAULT_SIZE						= (1.6, 0.9)
	DEFAULT_TRANSFORM				= (0.0, 0.0, 0.0)

	def __init__(self, config):
		# get data from config-dict
		self.name = config.get("name")
		self.hostname = config.get("hostname")
		self.displaystrings = config.get("displaystrings", self.DEFAULT_DISPLAYSTRINGS)
		_width, _height = config.get("size", self.DEFAULT_SIZE)
		_trans_x, _trans_y, _trans_z = config.get("transform", self.DEFAULT_TRANSFORM)
