#!/usr/bin/python

## @file
# Contains class Avatar.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
from ApplicationManager import *
import Utilities

# import python libraries
import math


##
class Avatar(avango.script.Script):

  ##
  def __init__(self):
    self.super(Avatar).__init__()


  def my_constructor(self, USER_REPRESENTATION):
    
    ##
    #
    self.USER_REPRESENTATION = USER_REPRESENTATION

    
    _loader = avango.gua.nodes.TriMeshLoader()
    
    # create avatar head
    ## @var head_geometry
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_geometry = _loader.create_geometry_from_file('head_avatar',
                                                           'data/objects/Joseph/JosephHead.obj',
                                                           'data/materials/ShadelessWhite.gmd',
                                                           avango.gua.LoaderFlags.LOAD_MATERIALS)

    self.head_geometry.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
    self.USER_REPRESENTATION.head.Children.value.append(self.head_geometry)

    # create avatar body
    ## @var body_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_geometry = _loader.create_geometry_from_file('body_avatar',
                                                           'data/objects/Joseph/JosephBody.obj',
                                                           'data/materials/ShadelessWhite.gmd',
                                                           avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.USER_REPRESENTATION.head.Children.value.append(self.body_geometry)

    # set evaluation policy
    self.always_evaluate(True)


  ## Sets the GroupNames field on all avatar parts to a list of strings.
  # @param LIST_OF_STRINGS A list of group names to be set for the avatar parts.
  def set_group_names(self, LIST_OF_STRINGS):

    self.head_geometry.GroupNames.value = LIST_OF_STRINGS
    self.body_geometry.GroupNames.value = LIST_OF_STRINGS


  ## Appends a string to the GroupNames field of all avatar parts.
  # @param STRING The string to be appended to the GroupNames field.
  def append_to_group_names(self, STRING):

    self.head_geometry.GroupNames.value.append(STRING)
    self.body_geometry.GroupNames.value.append(STRING)

  ##
  #
  def set_material(self, MATERIAL_STRING):

    self.head_geometry.Material.value = MATERIAL_STRING
    self.body_geometry.Material.value = MATERIAL_STRING

  ##
  def set_visible(self, VISIBILITY_BOOL):

    if VISIBILITY_BOOL:
      self.head_geometry.GroupNames.value.remove("do_not_display_group")
      self.body_geometry.GroupNames.value.remove("do_not_display_group")
    else:
      self.head_geometry.GroupNames.value.append("do_not_display_group")
      self.body_geometry.GroupNames.value.append("do_not_display_group")


  ##
  def evaluate(self):

    # update avatar body matrix if present at this view transform node
    _head_pos = self.USER_REPRESENTATION.head.Transform.value.get_translate()
    _forward_yaw = Utilities.get_yaw(self.USER_REPRESENTATION.head.Transform.value)

    self.body_geometry.Transform.value = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(self.USER_REPRESENTATION.head.Transform.value.get_rotate())) * \
                                         avango.gua.make_trans_mat(0.0, -_head_pos.y / 2, 0.0) * \
                                         avango.gua.make_rot_mat(math.degrees(_forward_yaw) - 90, 0, 1, 0) * \
                                         avango.gua.make_scale_mat(0.45, _head_pos.y / 2, 0.45)