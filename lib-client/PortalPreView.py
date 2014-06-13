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

    if VIEW.is_stereo:

      self.left_eye_node = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.view_node.Children.value.append(self.left_eye_node)

      self.right_eye_node = avango.gua.nodes.TransformNode(Name = "eyeR")
      self.view_node.Children.value.append(self.right_eye_node)

    else:

      self.eye_node = avango.gua.nodes.TransformNode(Name = "eye")
      self.view_node.Children.value.append(self.eye_node)


    self.screen_node = self.PORTAL_NODE.Children.value[1].Children.value[0]

    print "constructor portal pre view for " + "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id)

    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = VIEW.SCENEGRAPH.Name.value
    self.camera.RenderMask.value = VIEW.camera.RenderMask.value

    if VIEW.is_stereo:
      self.camera.LeftScreen.value = self.screen_node.Path.value
      self.camera.RightScreen.value = self.screen_node.Path.value
      self.camera.LeftEye.value = self.left_eye_node.Path.value
      self.camera.RightEye.value = self.right_eye_node.Path.value
    else:
      self.camera.LeftScreen.value = self.screen_node.Path.value
      self.camera.LeftEye.value = self.eye_node.Path.value


    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.Enabled.value = True
    self.pipeline.Camera.value = self.camera


    if VIEW.is_stereo:
      self.pipeline.LeftResolution.value = avango.gua.Vec2ui(1000, 1000)
      self.pipeline.RightResolution.value = avango.gua.Vec2ui(1000, 1000)   
      self.pipeline.EnableStereo.value = True
    else:
      self.pipeline.LeftResolution.value = avango.gua.Vec2ui(1000, 1000)
      self.pipeline.EnableStereo.value = False
    

    self.pipeline.OutputTextureName.value = self.PORTAL_NODE.Name.value + "_" + "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id)
    self.pipeline.BackgroundTexture.value = "data/textures/sky.jpg"

    self.VIEW.pipeline.PreRenderPipelines.value.append(self.pipeline)

    self.textured_quad = avango.gua.nodes.TexturedQuadNode(Name = "texture_s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id),
                                                           Texture = self.PORTAL_NODE.Name.value + "_" + "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id),
                                                           IsStereoTexture = VIEW.is_stereo,
                                                           Width = 1.0,
                                                           Height = 1.0)

    self.PORTAL_NODE.Children.value[0].Children.value.append(self.textured_quad)

    # TODO: Set proper RenderMask of self.textured_quad


  def compare_portal_node(self, PORTAL_NODE):
    if self.PORTAL_NODE == PORTAL_NODE:
      return True

    return False

    
  def evaluate(self):
    
    # update view node with transformed head position
    # update view distance
    # update visibility

    pass
