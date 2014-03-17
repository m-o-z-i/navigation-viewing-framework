#!/usr/bin/python

## @file
# Contains class ClientUser.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ClientTrackingReader import *

## Base class to represent attributes and functions that all users have in common on client side. 
# Not to be instantiated.
class ClientUser(avango.script.Script):

  ## Default constructor.
  def __init__(self):
  	self.super(ClientUser).__init__()
  	self.always_evaluate(True)

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph in the viewing setup.
  # @param PLATFORM_ID Platform on which the user is standing.
  # @param USER_ID Identification number of the user to be constructed, counts within each user category.
  # @param NODE_PRETEXT The prefix to be used when creating scenegraph nodes.
  def construct_user(self, SCENEGRAPH, PLATFORM_ID, USER_ID, NODE_PRETEXT):

    ## @var SCENEGRAPH
    # Reference to the scenegraph to be displayed.
    self.SCENEGRAPH = SCENEGRAPH

  	## @var platform_id
    # The platform id for which this client process is responsible for.
    self.platform_id = PLATFORM_ID

    ## @var user_id
    # User ID of this user within his or her user group.
    self.user_id = USER_ID

    ## @var node_pretext
    # Prefix of the scenegraph nodes this user creates.
    self.node_pretext = NODE_PRETEXT

  ## Adds a tracking reader to the user instance.
  # @param TRACKING_TARGET_NAME The target name of the tracked object as chosen in daemon.
  # @param TRANSMITTER_OFFSET The transmitter offset to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied if no headtracking of the Oculus Rift is available.
  def add_tracking_reader(self, TRACKING_TARGET_NAME, TRANSMITTER_OFFSET, NO_TRACKING_MAT):

    ## @var TRACKING_TARGET_NAME
    # The target name of the tracked object as chosen in daemon.
    self.TRACKING_TARGET_NAME = TRACKING_TARGET_NAME

  	## @var headtracking_reader
    # Instance of a child class of ClientTrackingReader to supply translation input.
    if self.TRACKING_TARGET_NAME != None:
      self.headtracking_reader = ClientTrackingTargetReader()
      self.headtracking_reader.my_constructor(TRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(TRANSMITTER_OFFSET)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())
  
  ## Evaluated every frame.
  def evaluate(self):

    if self.TRACKING_TARGET_NAME == None:
      return
   
    _node_to_update = self.SCENEGRAPH["/net/platform_" + str(self.platform_id) + "/" + self.node_pretext + "_head_" + str(self.user_id)]

    if _node_to_update != None:

      if self.node_pretext == "ovr":
        _vec = self.headtracking_reader.sf_abs_mat.value.get_translate()
        _mat = _node_to_update.Transform.value
        _mat.set_translate(_vec)
        _node_to_update.Transform.value = _mat
      else:
        _node_to_update.Transform.value = self.headtracking_reader.sf_abs_mat.value