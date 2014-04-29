#!/usr/bin/python

## @file
# Contains class View.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ClientTrackingReader import *

## Base class to represent attributes and functions that all users have in common on client side. 
# Not to be instantiated.
class View(avango.script.Script):

  ## Default constructor.
  def __init__(self):
  	self.super(ClientUser).__init__()
  	self.always_evaluate(True)

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph to be displayed.
  # @param PLATFORM_ID Identification number of the platform the view user is standing on.
  # @param SLOT_ID The identification number of the slot to display.
  # @param SCREEN_NUM The number of the screen node on the platform.
  # @param ONLY_TRANSLATION_UPDATE Boolean indicating if only the tracking translation is to be
  #                                locally updated on client side. Otherwise, the full matrix is refreshed.
  def construct_view(self, SCENEGRAPH, PLATFORM_ID, SLOT_ID, SCREEN_NUM, ONLY_TRANSLATION_UPDATE):

    ## @var SCENEGRAPH
    # Reference to the scenegraph to be displayed.
    self.SCENEGRAPH = SCENEGRAPH

  	## @var platform_id
    # The platform id for which this client process is responsible for.
    self.platform_id = PLATFORM_ID

    ## @var slot_id
    # The identification number of the slot to display.
    self.slot_id = SLOT_ID

    ## @var screen_num
    # The number of the screen node on the platform.
    self.screen_num = SCREEN_NUM

    ## @var ONLY_TRANSLATION_UPDATE
    # In case this boolean is true, only the translation values will be locally updated from the tracking system.
    self.ONLY_TRANSLATION_UPDATE = ONLY_TRANSLATION_UPDATE

  ## Adds a tracking reader to the view instance.
  # @param TRACKING_TARGET_NAME The target name of the tracked object as chosen in daemon.
  # @param TRANSMITTER_OFFSET The transmitter offset to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied if no headtracking of the Oculus Rift is available.
  def add_tracking_reader(self, TRACKING_TARGET_NAME, TRANSMITTER_OFFSET, NO_TRACKING_MAT):

    ## @var TRACKING_TARGET_NAME
    # The target name of the tracked object as chosen in daemon.
    self.TRACKING_TARGET_NAME = TRACKING_TARGET_NAME

    ## @var TRANSMITTER_OFFSET
    # The transmitter offset to be applied.
    self.TRANSMITTER_OFFSET = TRANSMITTER_OFFSET

    ## @var NO_TRACKING_MAT
    # Matrix to be applied if no headtracking of the Oculus Rift is available.
    self.NO_TRACKING_MAT = NO_TRACKING_MAT

  	## @var headtracking_reader
    # Instance of a child class of ClientTrackingReader to supply translation input.
    if self.TRACKING_TARGET_NAME != None:
      self.headtracking_reader = ClientTrackingTargetReader()
      self.headtracking_reader.my_constructor(TRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(TRANSMITTER_OFFSET)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())
  
  ## Evaluated every frame.
  def evaluate(self):
    
    _node_to_update = self.SCENEGRAPH["/net/platform_" + str(self.platform_id) + "/s" + str(self.screen_num) + "_slot" + str(self.slot_id)]
    
    _information_node = _node_to_update.Children.value[0]
    _tracking_target_name = _information_node.Name.value

    if _tracking_target_name == "None":
      _tracking_target_name = None

    # create new tracking reader when tracking target changes
    # TODO: when transmitter offset and no tracking mat change, propagate them in the scenegraph
    if _tracking_target_name != self.TRACKING_TARGET_NAME:
      self.add_tracking_reader(_tracking_target_name, self.TRANSMITTER_OFFSET, self.NO_TRACKING_MAT)

    # when no value is to be updated, stop evaluation
    if self.TRACKING_TARGET_NAME == None:
      return
    
    # update slot node
    if _node_to_update != None:

      if self.ONLY_TRANSLATION_UPDATE:
        _vec = self.headtracking_reader.sf_abs_mat.value.get_translate()
        _mat = _node_to_update.Transform.value
        _mat.set_translate(_vec)
        _node_to_update.Transform.value = _mat
      else:
        _node_to_update.Transform.value = self.headtracking_reader.sf_abs_mat.value
    

