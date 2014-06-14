#!/usr/bin/python

## @file
# Contains class ClientPortal.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
# ...

class ClientPortalManager(avango.script.Script):

  ##
  #
  mf_portal_group_children = avango.gua.MFNode()

  def __init__(self):
    self.super(ClientPortalManager).__init__()

    ##
    #
    self.mf_portal_group_children_connected = False

    ##
    #
    self.portals = []

    self.always_evaluate(True)

  def my_constructor(self, SCENEGRAPH, VIEW_LIST):

    ##
    #
    self.SCENEGRAPH = SCENEGRAPH

    ##
    #
    self.VIEW_LIST = VIEW_LIST

  ##
  #
  def notify_views_on_added_portal(self, LOCAL_PORTAL_NODE):

    for _view in self.VIEW_LIST:
      _view.create_portal_preview(LOCAL_PORTAL_NODE)


  def evaluate(self):

    try:
      _portal_group_node = self.SCENEGRAPH["/net/portal_group"]
    except:
      return

    # connect mf_portal_group_children only once
    if _portal_group_node != None and self.mf_portal_group_children_connected == False:
      self.mf_portal_group_children.connect_from(_portal_group_node.Children)
      self.mf_portal_group_children_connected = True

  @field_has_changed(mf_portal_group_children)
  def mf_portal_group_children_changed(self):
    
    for _node in self.mf_portal_group_children.value:

      _portal_instance_found = False

      for _portal in self.portals:

        if _portal.compare_server_portal_node(_node) == True:
          _portal_instance_found = True
          break

      if _portal_instance_found == False:
        _portal = ClientPortal(self.SCENEGRAPH["/local_portal_group"], _node)
        self.portals.append(_portal)
        self.notify_views_on_added_portal(_portal.portal_node)




class ClientPortal:

  def __init__(self, LOCAL_PORTAL_GROUP_NODE, SERVER_PORTAL_NODE):

    self.SERVER_PORTAL_NODE = SERVER_PORTAL_NODE

    self.portal_node = avango.gua.nodes.TransformNode(Name = SERVER_PORTAL_NODE.Name.value)
    LOCAL_PORTAL_GROUP_NODE.Children.value.append(self.portal_node)

    self.portal_matrix_node = avango.gua.nodes.TransformNode(Name = "portal_matrix")
    self.portal_matrix_node.Transform.connect_from(SERVER_PORTAL_NODE.Children.value[0].Transform)
    self.portal_node.Children.value.append(self.portal_matrix_node)

    self.scene_matrix_node = avango.gua.nodes.TransformNode(Name = "scene_matrix")
    self.scene_matrix_node.Transform.connect_from(SERVER_PORTAL_NODE.Children.value[1].Transform)
    self.portal_node.Children.value.append(self.scene_matrix_node)

    self.portal_screen_node = avango.gua.nodes.ScreenNode(Name = "portal_screen")
    self.portal_screen_node.Width.connect_from(SERVER_PORTAL_NODE.Children.value[1].Children.value[0].Width)
    self.portal_screen_node.Height.connect_from(SERVER_PORTAL_NODE.Children.value[1].Children.value[0].Height)
    self.scene_matrix_node.Children.value.append(self.portal_screen_node)

    # debug screen visualization
    _loader = avango.gua.nodes.TriMeshLoader()
    _node = _loader.create_geometry_from_file("screen_visualization", "data/objects/screen.obj", "data/materials/ShadelessBlack.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    _node.ShadowMode.value = avango.gua.ShadowMode.OFF
    _node.Transform.value = avango.gua.make_scale_mat(self.portal_screen_node.Width.value, self.portal_screen_node.Height.value, 1.0)
    self.scene_matrix_node.Children.value.append(_node)


  def compare_server_portal_node(self, SERVER_PORTAL_NODE):
    if self.SERVER_PORTAL_NODE == SERVER_PORTAL_NODE:
      return True

    return False



class PortalPreView(avango.script.Script):

  def __init__(self):
    self.super(PortalPreView).__init__()

  def my_constructor(self, PORTAL_NODE, VIEW):

    print "constructor portal pre view for " + "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id)
    
    self.PORTAL_NODE = PORTAL_NODE

    self.VIEW = VIEW

    self.view_node = avango.gua.nodes.TransformNode(Name = "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id))
    self.PORTAL_NODE.Children.value[1].Children.value.append(self.view_node)

    if VIEW.is_stereo:

      self.left_eye_node = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.left_eye_node.Transform.value = avango.gua.make_trans_mat(-0.03, 0.0, 0.0)
      self.view_node.Children.value.append(self.left_eye_node)

      self.right_eye_node = avango.gua.nodes.TransformNode(Name = "eyeR")
      self.right_eye_node.Transform.value = avango.gua.make_trans_mat(0.03, 0.0, 0.0)
      self.view_node.Children.value.append(self.right_eye_node)

    else:

      self.eye_node = avango.gua.nodes.TransformNode(Name = "eye")
      self.view_node.Children.value.append(self.eye_node)

      # debug eye visualization
      _loader = avango.gua.nodes.TriMeshLoader()
      self.eye_geometry = _loader.create_geometry_from_file("eye_visualization", "data/objects/sphere.obj", "data/materials/ShadelessBlack.gmd", avango.gua.LoaderFlags.DEFAULTS)
      self.eye_geometry.Transform.value = avango.gua.make_scale_mat(0.03)
      self.view_node.Children.value.append(self.eye_geometry)

    self.view_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.6)

    self.screen_node = self.PORTAL_NODE.Children.value[1].Children.value[0]

    print "EYE", self.eye_node.WorldTransform.value
    print "SCREEN", self.screen_node.WorldTransform.value

    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = VIEW.SCENEGRAPH.Name.value
    self.camera.RenderMask.value = "!do_not_display_group"
    #self.camera.RenderMask.value = VIEW.camera.RenderMask.value

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
    
    self.pipeline.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
    self.pipeline.BackgroundTexture.value = "data/textures/sky.jpg"

    self.VIEW.pipeline.PreRenderPipelines.value.append(self.pipeline)

    self.textured_quad = avango.gua.nodes.TexturedQuadNode(Name = "texture_s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id),
                                                           Texture = self.PORTAL_NODE.Name.value + "_" + "s" + str(VIEW.screen_num) + "_slot" + str(VIEW.slot_id),
                                                           IsStereoTexture = VIEW.is_stereo,
                                                           Width = self.screen_node.Width.value,
                                                           Height = self.screen_node.Height.value)

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