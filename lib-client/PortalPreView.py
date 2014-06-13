#!/usr/bin/python

## @file
# Contains class PortalPreView.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
# ...

class PortalPreView(avango.script.Script):

  def __init__(self):
    self.super(PortalPreView).__init__()

  def my_constructor(self, PORTAL_NODE, VIEW):
    
    self.PORTAL_NODE = PORTAL_NODE

    self.VIEW = VIEW

    self.view_node = avango.gua.nodes.TransformNode(Name = "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id))
    self.PORTAL_NODE.Children.value[1].Children.value.append(self.view_node)

    self.left_eye_node = avango.gua.nodes.TransformNode(Name = "eyeL")
    self.view_node.Children.value.append(self.left_eye_node)

    self.right_eye_node = avango.gua.nodes.TransformNode(Name = "eyeR")
    self.view_node.Children.value.append(self.right_eye_node)

    print "constructor portal pre view for " + "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id)


  def compare_portal_node(self, PORTAL_NODE):
    if self.PORTAL_NODE == PORTAL_NODE:
      return True

    return False

    
  def evaluate(self):
    
    # update view node with transformed head position
    # update view distance
    # update visibility

    pass
