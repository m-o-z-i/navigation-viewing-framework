#!/usr/bin/python

## @file
# Contains classes Portal and PortalManager.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
# ...

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
                    avango.gua.make_trans_mat(0.0, 2.0, -1.5),
                    1.0,
                    1.0)

    self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0), 
                    avango.gua.make_trans_mat(-1.2, 2.0, -2.5),
                    1.0,
                    1.0)
    #portal_manager.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0), avango.gua.make_trans_mat(-1.2, 2.0, -2.5))

    self.add_portal(avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(90, 0, 1, 0),
                    avango.gua.make_trans_mat(1.2, 2.0, -2.5),
                    1.0,
                    1.0)

  ##
  def add_portal(self, SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT):
    _portal = Portal(self, self.counter,  SCENE_MATRIX, PORTAL_MATRIX, WIDTH, HEIGHT)
    self.counter += 1
    self.portals.append(_portal)


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


    self.append_portal_nodes()

  ##
  #
  def append_portal_nodes(self):

    self.portal_node = avango.gua.nodes.TransformNode(Name = "portal_" + str(self.id))
    self.PORTAL_MANAGER.portal_group_node.Children.value.append(self.portal_node)

    self.portal_matrix_node = avango.gua.nodes.TransformNode(Name = "portal_matrix")
    self.portal_matrix_node.Transform.value = self.portal_matrix
    self.portal_node.Children.value.append(self.portal_matrix_node)

    self.scene_matrix_node = avango.gua.nodes.TransformNode(Name = "scene_matrix")
    self.scene_matrix_node.Transform.value = self.scene_matrix
    self.portal_node.Children.value.append(self.scene_matrix_node)

    self.portal_screen_node = avango.gua.nodes.ScreenNode(Name = "portal_screen")
    self.portal_screen_node.Width.value = self.width
    self.portal_screen_node.Height.value = self.height
    self.scene_matrix_node.Children.value.append(self.portal_screen_node)