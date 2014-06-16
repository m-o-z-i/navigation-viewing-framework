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

##
#
class PortalManager:

  ##
  def __init__(self, SCENEGRAPH):

    self.SCENEGRAPH = SCENEGRAPH

    self.portal_group_node = avango.gua.nodes.TransformNode(Name = "portal_group")
    self.SCENEGRAPH["/net"].Children.value.append(self.portal_group_node)

    self.portals = []
    self.counter = 0

    self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(-90, 0, 1, 0),
                    avango.gua.make_trans_mat(0.0, 2.0, -1.5) * avango.gua.make_rot_mat(45, 1, 0, 0),
                    1.0,
                    1.0)

    self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0), 
                    avango.gua.make_trans_mat(-1.2, 2.0, -2.5),
                    1.0,
                    1.0)
    #portal_manager.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0), avango.gua.make_trans_mat(-1.2, 2.0, -2.5), 1.0, 1.0)

    #self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(90, 0, 1, 0),
    #                avango.gua.make_trans_mat(1.2, 2.0, -2.5),
    #                1.0,
    #                1.0)

  ##
  #
  def add_portal(self, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT):
    _portal = Portal(self, self.counter, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT)
    self.counter += 1
    self.portals.append(_portal)

  def remove_portal(self, ID):

    _portal_to_remove = None

    for _portal in self.portals:
      if _portal.id == ID:
        _portal_to_remove = _portal

    if _portal_to_remove == None:
      print_error("Error: Portal ID could not be matched.", False)
      return

    _portal_to_remove.deactivate()
    self.portals.remove(_portal_to_remove)
    del _portal_to_remove

  ##
  #
  def add_bidirectional_portal(self, FIRST_MATRIX, SECOND_MATRIX, WIDTH, HEIGHT):
    self.add_portal(FIRST_MATRIX, SECOND_MATRIX, WIDTH, HEIGHT)

    _mirrored_scene_matrix = SECOND_MATRIX * avango.gua.make_rot_mat(180, 0, 1, 0)
    _mirrored_portal_matrix = FIRST_MATRIX * avango.gua.make_rot_mat(180, 0, 1, 0)

    self.add_portal(_mirrored_scene_matrix, _mirrored_portal_matrix, WIDTH, HEIGHT)


##
#
class Portal:

  ##
  def __init__(self, PORTAL_MANAGER, ID, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT):

    self.PORTAL_MANAGER = PORTAL_MANAGER

    self.id = ID

    ##
    # Matrix representing the remote camera of the portal.
    self.scene_matrix = SCENE_MATRIX

    ##
    # Matrix representing the portal screen location.
    self.portal_matrix = PORTAL_MATRIX

    ##
    #
    self.width = WIDTH

    ##
    #
    self.height = HEIGHT

    ##
    #
    self.NET_TRANS_NODE = PORTAL_MANAGER.SCENEGRAPH["/net"]

    ##
    #
    self.viewing_mode = "3D"

    ##
    #
    self.camera_mode = "PERSPECTIVE"

    ##
    #
    self.negative_parallax = "True"

    ##
    #
    self.scale = 1.0


    self.append_portal_nodes()

  ##
  #
  def switch_viewing_mode(self):
    if self.viewing_mode == "2D":
      self.viewing_mode = "3D"
    else:
      self.viewing_mode = "2D"

    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]

  ##
  #
  def switch_camera_mode(self):
    if self.camera_mode == "PERSPECTIVE":
      self.camera_mode = "ORTHOGRAPHIC"
    else:
      self.camera_mode = "PERSPECTIVE"

    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]

  ##
  #
  def switch_negative_parallax(self):
    if self.negative_parallax == "True":
      self.negative_parallax = "False"
    else:
      self.negative_parallax = "True"

    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]

  ##
  #
  def set_scale(self, SCALE):
    self.scale_node.Transform.value = avango.gua.make_scale_mat(SCALE)

  ##
  #
  def append_portal_nodes(self):

    self.portal_node = avango.gua.nodes.TransformNode(Name = "portal_" + str(self.id))
    self.portal_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax]
    self.PORTAL_MANAGER.portal_group_node.Children.value.append(self.portal_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_node)

    self.portal_matrix_node = avango.gua.nodes.TransformNode(Name = "portal_matrix")
    self.portal_matrix_node.Transform.value = self.portal_matrix
    self.portal_node.Children.value.append(self.portal_matrix_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_matrix_node)

    self.scene_matrix_node = avango.gua.nodes.TransformNode(Name = "scene_matrix")
    self.scene_matrix_node.Transform.value = self.scene_matrix
    self.portal_node.Children.value.append(self.scene_matrix_node)
    self.NET_TRANS_NODE.distribute_object(self.scene_matrix_node)

    self.scale_node = avango.gua.nodes.TransformNode(Name = "scale")
    self.set_scale(self.scale)
    self.scene_matrix_node.Children.value.append(self.scale_node)
    self.NET_TRANS_NODE.distribute_object(self.scale_node)

    self.portal_screen_node = avango.gua.nodes.ScreenNode(Name = "portal_screen")
    self.portal_screen_node.Width.value = self.width
    self.portal_screen_node.Height.value = self.height
    self.scale_node.Children.value.append(self.portal_screen_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_screen_node)

  ##
  #
  def deactivate(self):
    self.PORTAL_MANAGER.portal_group_node.Children.value.remove(self.portal_node)

    del self.portal_screen_node
    del self.scale_node
    del self.scene_matrix_node
    del self.portal_matrix_node
    del self.portal_node