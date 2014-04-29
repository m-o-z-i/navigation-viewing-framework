#!/usr/bin/python

## @file
# Contains class Slot.

# import avango-guacamole libraries
import avango
import avango.gua

## 
#
class Slot:

  ## Custom constructor.
  #
  #
  def __init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM_NODE):

    ##
    #
    self.slot_id = SLOT_ID

    ##
    #
    self.screen_num = SCREEN_NUM

    ##
    #
    self.stereo = STEREO

    ##
    #
    self.PLATFORM_NODE = PLATFORM_NODE

    ##
    #
    self.assigned_user = None

    ##
    #
    if self.stereo:
      self.shutter_timing = DISPLAY.shutter_timings[SLOT_ID]
    else:
      self.shutter_timing = None

    ##
    #
    if self.stereo:
      self.shutter_value = DISPLAY.shutter_values[SLOT_ID]
    else:
      self.shutter_value = None

    # append nodes to platform transform node

    ## 
    #
    self.slot_node = avango.gua.nodes.TransformNode(Name = "s" + str(SCREEN_NUM) + "_slot" + str(SLOT_ID))
    self.PLATFORM_NODE.Children.value.append(self.slot_node)

    if self.stereo:
      # create the eyes
      ## @var left_eye
      #
      self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.left_eye.Transform.value = avango.gua.make_identity_mat()
      self.slot_node.Children.value.append(self.left_eye)

      ## @var right_eye
      #
      self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
      self.right_eye.Transform.value = avango.gua.make_identity_mat()
      self.slot_node.Children.value.append(self.right_eye)

      self.set_eye_distance(0.06)
    else:
      ##
      #
      self.eye = avango.gua.nodes.TransformNode(Name = "eye")
      self.eye.Transform.value = avango.gua.make_identity_mat()
      self.slot_node.Children.value.append(self.eye)


  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    self.left_eye.Transform.value  = avango.gua.make_trans_mat(VALUE * -0.5, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(VALUE * 0.5, 0.0, 0.0)

  ##
  #
  def assign_user(self, USER_INSTANCE):
    self.slot_node.Transform.connect_from(USER_INSTANCE.headtracking_reader.sf_abs_mat)
    self.assigned_user = USER_INSTANCE