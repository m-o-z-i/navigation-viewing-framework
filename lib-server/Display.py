#!/usr/bin/python

# import avango-guacamole libraries
import avango
import avango.gua

class Display:

	def __init__(	self
							, hostname
							, name = None
							, resolution = (1920, 1080)
							, displaystrings = [":0.0"]
							, size = (1.6, 0.9)
							, transform = (0, 1.0, 0)
							):
		# save values in members
		self.hostname = hostname
		if not name:
			self.name = hostname + "_display"
		else:
			self.name = name
		self.resolution = resolution
		self.displaystrings = displaystrings
		self.size = size
		self.transform = transform

	def register_user(self, user_num):
		if user_num < len(self.displaystrings):
			return self.displaystrings[user_num]
		else:
			return None

	def create_screen_node(self, name = "screen_node"):
		_screen = avango.gua.nodes.ScreenNode(Name = name)
		_w, _h = self.resolution
		_screen.Width.value = _w
		_screen.Height.value = _h
		_x, _y, _z = self.transform
		_screen.Transform.value = avango.gua.make_trans_mat(_x, _y, _z)
		return _screen
