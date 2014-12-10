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


## Representation of an Avatar belonging to a UserRepresentation.
# Contains of several parts of geometry.
class Avatar:

  ## Default constructor.
  def __init__(self):
    pass

  ## Custom constructor.
  # @param USER_REPRESENTATION The UserRepresentation instance to create the avatar for.
  def my_constructor(self, USER_REPRESENTATION):
    
    ## @var USER_REPRESENTATION
    # The UserRepresentation instance to which this Avatar belongs to.
    self.USER_REPRESENTATION = USER_REPRESENTATION

    _loader = avango.gua.nodes.TriMeshLoader()
    
    ## @var head_geometry
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_geometry = _loader.create_geometry_from_file('head_avatar',
                                                           'data/objects/Joseph/JosephHead.obj',
                                                           'data/materials/ShadelessWhite.gmd',
                                                           avango.gua.LoaderFlags.LOAD_MATERIALS)

    self.head_geometry.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
    self.USER_REPRESENTATION.head.Children.value.append(self.head_geometry)

    ## @var body_geometry
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_geometry = _loader.create_geometry_from_file('body_avatar',
                                                           'data/objects/Joseph/JosephBody.obj',
                                                           'data/materials/ShadelessWhite.gmd',
                                                           avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.USER_REPRESENTATION.head.Children.value.append(self.body_geometry)

    ## @var screen_visualizations
    # Geometry nodes representing all the screens at the DisplayGroup the UserRepresentation belongs to.
    self.screen_visualizations = []

    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method.
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)
    

  ## Adds a screen visualization for a display instance to the view transformation node.
  # @param DISPLAY_INSTANCE The Display instance to retrieve the screen visualization from.
  def add_screen_visualization_for(self, DISPLAY_INSTANCE):
    _screen_visualization = DISPLAY_INSTANCE.create_screen_visualization(DISPLAY_INSTANCE.name + "_vis")
    self.USER_REPRESENTATION.view_transform_node.Children.value.append(_screen_visualization)
    self.screen_visualizations.append(_screen_visualization)


  ## Sets the GroupNames field on all avatar parts to a list of strings.
  # @param LIST_OF_STRINGS A list of group names to be set for the avatar parts.
  def set_group_names(self, LIST_OF_STRINGS):

    self.head_geometry.GroupNames.value = LIST_OF_STRINGS
    self.body_geometry.GroupNames.value = LIST_OF_STRINGS

    for _screen_vis in self.screen_visualizations:
      _screen_vis.GroupNames.value = LIST_OF_STRINGS


  ## Appends a string to the GroupNames field of all avatar parts.
  # @param STRING The string to be appended to the GroupNames field.
  def append_to_group_names(self, STRING):

    self.head_geometry.GroupNames.value.append(STRING)
    self.body_geometry.GroupNames.value.append(STRING)

    for _screen_vis in self.screen_visualizations:
      _screen_vis.GroupNames.value.append(STRING)

  ## Sets a material for all avatar parts.
  # @param JOSEPH_MATERIAL Material string to be applied to head_geometry and body_geometry.
  # @param SCREEN_MATERIAL Material string to be applied to all screen visualizations.
  def set_material(self, JOSEPH_MATERIAL, SCREEN_MATERIAL):

    self.head_geometry.Material.value = JOSEPH_MATERIAL
    self.body_geometry.Material.value = JOSEPH_MATERIAL

    for _screen_vis in self.screen_visualizations:
      _screen_vis.Material.value = SCREEN_MATERIAL

  ## Evaluated every frame.
  def frame_callback(self):

    # update avatar body matrix if present at this view transform node
    _head_pos = self.USER_REPRESENTATION.head.Transform.value.get_translate()
    _forward_yaw = Utilities.get_yaw(self.USER_REPRESENTATION.head.Transform.value)

    self.body_geometry.Transform.value = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(self.USER_REPRESENTATION.head.Transform.value.get_rotate_scale_corrected())) * \
                                         avango.gua.make_trans_mat(0.0, -_head_pos.y / 2, 0.0) * \
                                         avango.gua.make_rot_mat(math.degrees(_forward_yaw) - 90, 0, 1, 0) * \
                                         avango.gua.make_scale_mat(0.45, _head_pos.y / 2, 0.45)