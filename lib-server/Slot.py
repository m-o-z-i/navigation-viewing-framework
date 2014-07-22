#!/usr/bin/python

## @file
# Contains class Slot.

# import avango-guacamole libraries
import avango
import avango.gua

## Internal representation of a display slot. A Slot is one rendering output that can be handled
# by a display. User can have multiple slots to obtain a brighter image.
class Slot:

  ## Custom constructor.
  # @param DISPLAY Display instance for which this slot is being created.
  # @param SLOT_ID Identification number of the slot within the display.
  # @param SCREEN_NUM Number of the screen / display on the platform.
  # @param STEREO Boolean indicating if the slot to be created is a stereo one.
  # @param PLATFORM Platform instance to which the slot is to be appended to.
  def __init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM):

    ## @var slot_id
    # Identification number of the slot within the display.
    self.slot_id = SLOT_ID

    ## @var screen_num
    # Number of the screen / display on the platform.
    self.screen_num = SCREEN_NUM

    ## @var stereo
    # Boolean indicating if this slot is a stereo one.
    self.stereo = STEREO

    ##
    #
    self.PLATFORM = PLATFORM

    ## @var PLATFORM_NODE
    # Scenegraph transformation node of the platform where the slot is appended to.
    self.PLATFORM_NODE = self.PLATFORM.platform_transform_node

    ## @var assigned_user
    # User instance which was assigned to this Slot by the SlotManager.
    self.assigned_user = None

    ## @var shutter_timing
    # A list of opening and closing times of shutter glasses for this slot.
    if self.stereo and DISPLAY.stereomode == "SIDE_BY_SIDE":
      self.shutter_timing = DISPLAY.shutter_timings[SLOT_ID]
    else:
      self.shutter_timing = None

    ## @var shutter_value
    # A list of hexadecimal commands for shutter glasses associated with the timings for this slot.
    if self.stereo and DISPLAY.stereomode == "SIDE_BY_SIDE":
      self.shutter_value = DISPLAY.shutter_values[SLOT_ID]
    else:
      self.shutter_value = None

    # append nodes to platform transform node

    ## @var slot_node
    # Scenegraph transformation node of this slot.
    self.slot_node = avango.gua.nodes.TransformNode(Name = "s" + str(SCREEN_NUM) + "_slot" + str(SLOT_ID))
    self.slot_node.Transform.connect_from(self.PLATFORM.sf_abs_mat)
    self.PLATFORM_NODE.Children.value.append(self.slot_node)

    ## @var slot_scale_node
    # Scenegraph node representing this slot's scale. Is below slot_node.
    self.slot_scale_node = avango.gua.nodes.TransformNode(Name = "scale")
    self.slot_node.Children.value = [self.slot_scale_node]

    ##
    #
    self.screen = DISPLAY.create_screen_node("screen")

    if self.screen != None:
      self.slot_scale_node.Children.value.append(self.screen)

    ##
    #
    self.head_node = avango.gua.nodes.TransformNode(Name = "head")
    self.slot_scale_node.Children.value.append(self.head_node)

    ## @var information_node
    # Node whose name is set to the headtracking target name of the current user. Used for the local
    # headtracking update on client side. Transform is transmitter offset to be applied
    self.information_node = avango.gua.nodes.TransformNode(Name = "None")
    self.head_node.Children.value.append(self.information_node)

    ## @var no_tracking_node
    # Node whose Transform field contains the no tracking matrix to be applied for the headtracking.
    # Used for the local headtracking update on client side.
    self.no_tracking_node = avango.gua.nodes.TransformNode(Name = "no_tracking_mat")
    self.information_node.Children.value.append(self.no_tracking_node)

    # create the eyes
    ## @var left_eye
    # Representation of the slot's user's left eye.
    self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
    self.left_eye.Transform.value = avango.gua.make_identity_mat()
    self.head_node.Children.value.append(self.left_eye)

    ## @var right_eye
    # Representation of the slot's user's right eye.
    self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
    self.right_eye.Transform.value = avango.gua.make_identity_mat()
    self.head_node.Children.value.append(self.right_eye)

    if self.stereo == False:
      self.set_eye_distance(0.0)


  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    if self.stereo:
      self.left_eye.Transform.value  = avango.gua.make_trans_mat(VALUE * -0.5, 0.0, 0.0)
      self.right_eye.Transform.value = avango.gua.make_trans_mat(VALUE * 0.5, 0.0, 0.0)

  ## Assigns a user to this slot. Therefore, the slot_node is connected with the user's headtracking matrix.
  # @param USER_INSTANCE An instance of User which is to be assigned.
  def assign_user(self, USER_INSTANCE):
    # connect tracking matrix
    self.head_node.Transform.connect_from(USER_INSTANCE.headtracking_reader.sf_abs_mat)
    self.assigned_user = USER_INSTANCE

    if self.stereo:
      self.set_eye_distance(self.assigned_user.eye_distance)
 
    # set information node
    if USER_INSTANCE.headtracking_target_name == None:
      self.information_node.Name.value = "None"
    else:
      self.information_node.Name.value = USER_INSTANCE.headtracking_target_name

    # feed Transform field of information node with transmitter_offset
    self.information_node.Transform.value = USER_INSTANCE.transmitter_offset

    # feed Transform field of no tracking node with no_tracking_mat
    self.no_tracking_node.Transform.value = USER_INSTANCE.no_tracking_mat

  ## Clears the user assignment.
  def clear_user(self):
    if self.assigned_user != None:
      self.head_node.Transform.disconnect()
      self.head_node.Transform.value = avango.gua.make_identity_mat()
      self.assigned_user = None
      self.information_node.Name.value = "None"
      self.information_node.Transform.value = avango.gua.make_identity_mat()
      self.no_tracking_node.Transform.value = avango.gua.make_identity_mat()

## Internal representation of a display slot on a head mounted display. A Slot is one rendering output that can be handled
# by a display, for HMDs usually one per device.
class SlotHMD(Slot):

  ## Custom constructor.
  # @param DISPLAY Display instance for which this slot is being created.
  # @param SLOT_ID Identification number of the slot within the display.
  # @param SCREEN_NUM Number of the screen / display on the platform.
  # @param STEREO Boolean indicating if the slot to be created is a stereo one.
  # @param PLATFORM_NODE Scenegraph transformation node of the platform where the slot is to be appended to.
  def __init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM_NODE):
    Slot.__init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM_NODE)

    self.left_screen = avango.gua.nodes.ScreenNode(Name = "screenL")
    self.left_screen.Width.value = DISPLAY.size[0] / 2
    self.left_screen.Height.value = DISPLAY.size[1]
    self.left_screen.Transform.value = avango.gua.make_trans_mat(-0.04, 0.0, -0.05)
    self.slot_node.Children.value.append(self.left_screen)

    self.right_screen = avango.gua.nodes.ScreenNode(Name = "screenR")
    self.right_screen.Width.value = DISPLAY.size[0] / 2
    self.right_screen.Height.value = DISPLAY.size[1]
    self.right_screen.Transform.value = avango.gua.make_trans_mat(0.04, 0.0, -0.05)
    self.slot_node.Children.value.append(self.right_screen)

  ## Assigns a user to this slot. Therefore, the slot_node is connected with the user's headtracking matrix.
  # In the HMD case, the InputMapping's station matrix is overwritten.
  # @param USER_INSTANCE An instance of User which is to be assigned.
  def assign_user(self, USER_INSTANCE):
    Slot.assign_user(self, USER_INSTANCE)

    # connect station mat with headtracking matrix
    USER_INSTANCE.platform.INPUT_MAPPING_INSTANCE.DEVICE_INSTANCE.sf_station_mat.disconnect()
    USER_INSTANCE.platform.INPUT_MAPPING_INSTANCE.DEVICE_INSTANCE.sf_station_mat.connect_from(USER_INSTANCE.headtracking_reader.sf_abs_mat)