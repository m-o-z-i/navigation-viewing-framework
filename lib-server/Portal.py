#!/usr/bin/python

## @file
# Contains classes Portal and PortalManager.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ConsoleIO import *

## Class to create, handle and destoy Portal instances.
class PortalManager:

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph.
  def __init__(self, SCENEGRAPH):

    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var portal_group_node
    # Scenegraph grouping node for portals on server side.
    self.portal_group_node = avango.gua.nodes.TransformNode(Name = "portal_group")
    self.SCENEGRAPH["/net"].Children.value.append(self.portal_group_node)

    ## @var portals
    # List of currently active Portal instances.
    self.portals = []

    ## @var counter
    # Integer which counts the number of portals already created. Used for portal IDs.
    self.counter = 0

    # add portal instances
    self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(-90, 0, 1, 0),
                    avango.gua.make_trans_mat(0.0, 2.0, -1.5) * avango.gua.make_rot_mat(45, 1, 0, 0),
                    1.0,
                    1.0)

    self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0), 
                    avango.gua.make_trans_mat(-1.2, 2.0, -2.5),
                    1.0,
                    1.0)

    #self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(90, 0, 1, 0),
    #                avango.gua.make_trans_mat(1.2, 2.0, -2.5),
    #                1.0,
    #                1.0)

  ## Adds a new Portal instance to the scene.
  # @param SCENE_MATRIX Matrix where the portal looks from (exit).
  # @param PORTAL_MATRIX Matrix where the portal display is located (entry).
  # @param WIDTH Width of the portal in meters.
  # @param HEIGHT Height of the portal in meters.
  def add_portal(self, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT):
    _portal = Portal(self, self.counter, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT)
    self.counter += 1
    self.portals.append(_portal)

  ## Add a new bidirectional portal to the scene.
  # @param FIRST_MATRIX First matrix defining the portal.
  # @param SECOND_MATRIX Second matrix defining the portal.
  # @param WIDTH Width of the portal in meters.
  # @param HEIGHT Height of the portal in meters.
  def add_bidirectional_portal(self, FIRST_MATRIX, SECOND_MATRIX, WIDTH, HEIGHT):
    self.add_portal(FIRST_MATRIX, SECOND_MATRIX, WIDTH, HEIGHT)

    # mirror matrices for opposite portal
    _mirrored_scene_matrix = SECOND_MATRIX * avango.gua.make_rot_mat(180, 0, 1, 0)
    _mirrored_portal_matrix = FIRST_MATRIX * avango.gua.make_rot_mat(180, 0, 1, 0)

    self.add_portal(_mirrored_scene_matrix, _mirrored_portal_matrix, WIDTH, HEIGHT)

  ## Removes a portal from the scene.
  # @param ID The portal ID to be removed.
  def remove_portal(self, ID):

    # find corresponding portal instance
    _portal_to_remove = None

    for _portal in self.portals:
      if _portal.id == ID:
        _portal_to_remove = _portal

    if _portal_to_remove == None:
      print_error("Error: Portal ID could not be matched.", False)
      return

    # destroy portal on server side
    _portal_to_remove.deactivate()
    self.portals.remove(_portal_to_remove)
    del _portal_to_remove


## A Portal is the display of another location on a virtual display.
class Portal:

  ## Custom constructor.
  # @param PORTAL_MANAGER Reference to the PortalManager to be used.
  # @param ID The portal ID to be assigned to the new portal.
  # @param SCENE_MATRIX Matrix where the portal looks from (exit).
  # @param PORTAL_MATRIX Matrix where the portal display is located (entry).
  # @param WIDTH Width of the portal in meters.
  # @param HEIGHT Height of the portal in meters.
  def __init__(self, PORTAL_MANAGER, ID, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT):

    ## @var PORTAL_MANAGER
    # Reference to the PortalManager to be used.
    self.PORTAL_MANAGER = PORTAL_MANAGER

    ## @var id
    # The portal ID assigned to the portal.
    self.id = ID

    ## @var scene_matrix
    # Matrix where the portal looks from (exit).
    self.scene_matrix = SCENE_MATRIX

    ## @var portal_matrix
    # Matrix where the portal display is located (entry).
    self.portal_matrix = PORTAL_MATRIX

    ## @var width
    # Width of the portal in meters.
    self.width = WIDTH

    ## @var height
    # Height of the portal in meters.
    self.height = HEIGHT

    ## @var NET_TRANS_NODE
    # Reference to the nettrans node used for distribution.
    self.NET_TRANS_NODE = PORTAL_MANAGER.SCENEGRAPH["/net"]

    ## @var viewing_mode
    # Viewing mode of the portal, can be either "2D" or "3D".
    self.viewing_mode = "3D"

    ## @var camera_mode
    # Projection mode of the portal camera, can be either "PERSPECTIVE" or "ORTHOGRAPHIC".
    self.camera_mode = "PERSPECTIVE"

    ## @var negative_parallax
    # Indicating if negative parallax is allowed in the portal, can be either "True" or "False".
    self.negative_parallax = "True"

    ## @var scale
    # Scaling factor within the portal.
    self.scale = 1.0

    self.append_portal_nodes()

  ## Switches viewing_mode to the other state.
  def switch_viewing_mode(self):
    if self.viewing_mode == "2D":
      self.viewing_mode = "3D"
    else:
      self.viewing_mode = "2D"

    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]

  ## Switches camera_mode to the other state.
  def switch_camera_mode(self):
    if self.camera_mode == "PERSPECTIVE":
      self.camera_mode = "ORTHOGRAPHIC"
    else:
      self.camera_mode = "PERSPECTIVE"

    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]

  ## Switches negative_parallax to the other state.
  def switch_negative_parallax(self):
    if self.negative_parallax == "True":
      self.negative_parallax = "False"
    else:
      self.negative_parallax = "True"

    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]

  ## Sets a new scaling factor for the portal.
  # @param SCALE The new scaling factor to be set
  def set_scale(self, SCALE):
    self.scale_node.Transform.value = avango.gua.make_scale_mat(SCALE)

  ## Appends the necessary portal scenegraph nodes on server side.
  def append_portal_nodes(self):

    ## @var portal_node
    # Grouping node for this portal below the group node for all portals.
    self.portal_node = avango.gua.nodes.TransformNode(Name = "portal_" + str(self.id))
    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]
    self.PORTAL_MANAGER.portal_group_node.Children.value.append(self.portal_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_node)

    ## @var portal_matrix_node
    # Scenegraph node representing the location where the portal display is located (entry).
    self.portal_matrix_node = avango.gua.nodes.TransformNode(Name = "portal_matrix")
    self.portal_matrix_node.Transform.value = self.portal_matrix
    self.portal_node.Children.value.append(self.portal_matrix_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_matrix_node)

    ## @var scene_matrix_node
    # Scenegraph node representing the location where the portal looks from (exit).
    self.scene_matrix_node = avango.gua.nodes.TransformNode(Name = "scene_matrix")
    self.scene_matrix_node.Transform.value = self.scene_matrix
    self.portal_node.Children.value.append(self.scene_matrix_node)
    self.NET_TRANS_NODE.distribute_object(self.scene_matrix_node)

    ## @var scale_node
    # Scenegraph node representing the portal's scaling factor.
    self.scale_node = avango.gua.nodes.TransformNode(Name = "scale")
    self.set_scale(self.scale)
    self.scene_matrix_node.Children.value.append(self.scale_node)
    self.NET_TRANS_NODE.distribute_object(self.scale_node)

    ## @var portal_screen_node
    # Screen node representing the portal's screen in the scene.
    self.portal_screen_node = avango.gua.nodes.ScreenNode(Name = "portal_screen")
    self.portal_screen_node.Width.value = self.width
    self.portal_screen_node.Height.value = self.height
    self.scale_node.Children.value.append(self.portal_screen_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_screen_node)

  ## Removes this portal from the portal group and destroys all the scenegraph nodes.
  def deactivate(self):
    self.PORTAL_MANAGER.portal_group_node.Children.value.remove(self.portal_node)

    del self.portal_screen_node
    del self.scale_node
    del self.scene_matrix_node
    del self.portal_matrix_node
    del self.portal_node