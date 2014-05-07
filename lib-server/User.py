#!/usr/bin/python

## @file
# Contains class User.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from TrackingReader import *

# import math libraries
import math

## Internal representation of a user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates eyes
# and initializes the headtracking.

class User(avango.script.Script):

  def __init__(self):
    self.super(User).__init__()

  ## Custom constructor.
  # @param APPLICATION_MANAGER Reference to the ApplicationManager instance from which this user is created.
  # @param USER_ID Global user ID to be applied.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param PLATFORM_ID Platform ID to which this user should be appended to.
  # @param AVATAR_MATERIAL The material string for the user avatar to be created.
  def my_constructor(self, APPLICATION_MANAGER, USER_ID, VIP, HEADTRACKING_TARGET_NAME, PLATFORM_ID, AVATAR_MATERIAL):

    # flags 
    ## @var is_vip
    # Boolean indicating if this user has vip status.
    self.is_vip = VIP

    ## @var is_active
    # Boolean indicating if this user is currently active.
    self.is_active = True

    # variables
    ## @var APPLICATION_MANAGER
    # Reference to the ApplicationManager instance from which the user is created.
    self.APPLICATION_MANAGER = APPLICATION_MANAGER

    ## @var id
    # Identification number of the user, starting from 0.
    self.id = USER_ID

    ## @var platform_id
    # ID of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID

    ## @var platform
    # Instance of the platform the user is belonging to.
    self.platform = self.APPLICATION_MANAGER.navigation_list[self.platform_id].platform

    ## @var current_display
    # Display instance on which the user physically is currently looking at.
    self.current_display = self.platform.displays[0]

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset   = self.platform.transmitter_offset

    ## @var no_tracking_mat
    # The matrix to be applied when no tracking is available.
    self.no_tracking_mat      = self.platform.no_tracking_mat
    
    ## @var avatar_material
    # Material of the user's avatar.
    self.avatar_material = AVATAR_MATERIAL

    ## @var headtracking_target_name
    # Name of the headtracking station as registered in daemon.
    self.headtracking_target_name = HEADTRACKING_TARGET_NAME

    ##
    #
    if self.headtracking_target_name.startswith("tracking-dlp-glasses-"):
      self.glasses_id = int(self.headtracking_target_name.replace("tracking-dlp-glasses-", ""))
      print "USER", self.id, "WEARS GLASSES", self.glasses_id

    ## @var headtracking_reader
    # Instance of a child class of TrackingReader to supply translation input.
    if HEADTRACKING_TARGET_NAME == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(self.no_tracking_mat)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    # create avatar representation
    if self.platform.avatar_type == "joseph":
      self.create_avatar_representation(self.headtracking_reader.sf_avatar_head_mat, self.headtracking_reader.sf_avatar_body_mat, False)
    elif self.platform.avatar_type == "joseph_table":
      self.create_avatar_representation(self.headtracking_reader.sf_avatar_head_mat, self.headtracking_reader.sf_avatar_body_mat, True)

    # toggles avatar display and activity
    self.toggle_user_activity(self.is_active, False)

    # set evaluation policy
    self.always_evaluate(True)


  ## Evaluated every frame.
  def evaluate(self):
    # Set active flag, current platform and current display
    # call slot manager.
    pass

  ## Sets the user's active flag.
  # @param ACTIVE Boolean to which the active flag should be set.
  # @param RESEND_CONFIG Boolean indicating if the shutter configuration should be directly resent.
  def toggle_user_activity(self, ACTIVE, RESEND_CONFIG):

    if ACTIVE:
      self.is_active = True
      self.head_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
      self.body_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    else:
      self.is_active = False
      self.head_avatar.GroupNames.value.append("do_not_display_group")
      self.body_avatar.GroupNames.value.append("do_not_display_group")

    if RESEND_CONFIG:
      self.APPLICATION_MANAGER.slot_manager.update_slot_configuration()

  ## Changes the user's current platform.
  # @param PLATFORM_ID The new platform id to be set.
  def set_user_location(self, PLATFORM_ID):
    self.remove_from_platform(self.head_avatar)
    self.remove_from_platform(self.body_avatar)

    self.platform_id = PLATFORM_ID
    self.platform = self.APPLICATION_MANAGER.navigation_list[self.platform_id].platform
    self.current_display = self.platform.displays[0]
    self.head_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    self.head_avatar.Material.value = 'data/materials/' + self.avatar_material + '.gmd'
    self.body_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    self.body_avatar.Material.value = 'data/materials/' + self.avatar_material + '.gmd'

    self.append_to_platform(self.head_avatar)
    self.append_to_platform(self.body_avatar)

    self.APPLICATION_MANAGER.slot_manager.update_slot_configuration()

  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    self.eye_distance = VALUE
    self.left_eye.Transform.value  = avango.gua.make_trans_mat(self.eye_distance * -0.5, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(self.eye_distance * 0.5, 0.0, 0.0)

  ## Appends a node to the children of a platform in the scenegraph.
  # @param NODE The node to be appended to the platform node.
  def append_to_platform(self, NODE):
    
    self.platform.platform_scale_transform_node.Children.value.append(NODE)

  ## Removes a node from the children of a platform in the scenegraph.
  # @param NODE The node to be removed from the platform node.
  def remove_from_platform(self, NODE):

    self.platform.platform_scale_transform_node.Children.value.remove(NODE)

  ## Creates a basic "joseph" avatar for this user.
  # @param SF_AVATAR_HEAD_MATRIX Field containing the transformation matrix for the avatar's head on the platform.
  # @param SF_AVATAR_BODY_MATRIX Field containing the transformation matrix for the avatar's body on the platform.
  # @param TABLE_ENABLED Boolean indicating if a table should be added to the avatar.
  def create_avatar_representation(self, SF_AVATAR_HEAD_MATRIX, SF_AVATAR_BODY_MATRIX, TABLE_ENABLED):

    _loader = avango.gua.nodes.GeometryLoader()
    
    # create avatar head
    ## @var head_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_avatar = _loader.create_geometry_from_file( 'head_avatar_' + str(self.id),
                                                          'data/objects/Joseph/JosephHead.obj',
                                                          'data/materials/' + self.avatar_material + '.gmd',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.head_avatar.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
    self.head_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]

    # create avatar body
    ## @var body_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_avatar = _loader.create_geometry_from_file( 'body_avatar_' + str(self.id),
                                                          'data/objects/Joseph/JosephBody.obj',
                                                          'data/materials/' + self.avatar_material + '.gmd',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.body_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    
    self.append_to_platform(self.head_avatar)
    self.append_to_platform(self.body_avatar)

    self.head_avatar.Transform.connect_from(SF_AVATAR_HEAD_MATRIX)
    self.body_avatar.Transform.connect_from(SF_AVATAR_BODY_MATRIX)

    # create table avatar if enabled
    if TABLE_ENABLED:

      ## @var table_transform
      # Scenegraph transform node for the dekstop user's table.
      self.table_transform = avango.gua.nodes.TransformNode(Name = 'table_transform')
      self.table_transform.Transform.value = avango.gua.make_trans_mat(-0.8, 0.2, 0.8)
      self.body_avatar.Children.value.append(self.table_transform)

      ## @var table_avatar
      # Scenegraph node representing the geometry and transformation of the desktop user's table.
      self.table_avatar = _loader.create_geometry_from_file( 'table_avatar_' + str(self.id),
                                                             'data/objects/table/table.obj',
                                                             'data/materials/' + self.avatar_material + '.gmd',
                                                             avango.gua.LoaderFlags.LOAD_MATERIALS)
      self.table_avatar.Transform.value = avango.gua.make_scale_mat(0.2, 0.5, 0.5)
      self.table_transform.Children.value.append(self.table_avatar)

      self.table_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
