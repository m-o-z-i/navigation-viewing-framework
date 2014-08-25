#!/usr/bin/python

## @file
# Contains class ClientPortal.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ConsoleIO import *

# import python libraries
import math

## Class to create, handle and destroy Portal instances on client side.
class ClientPortalManager(avango.script.Script):

  ## @var mf_portal_group_children
  # Children field of the server portal group to be checked for changes.
  mf_portal_group_children = avango.gua.MFNode()

  ## Default constructor.
  def __init__(self):
    self.super(ClientPortalManager).__init__()

    ## @var mf_portal_group_children_connected
    # Boolean indicating if the field connection to mf_portal_group_children was established.
    self.mf_portal_group_children_connected = False

    ## @var portals
    # List of currently active ClientPortal instances.
    self.portals = []

    self.always_evaluate(True)

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param VIEW_LIST List of all View instances in the scene.
  def my_constructor(self, SCENEGRAPH, VIEW_LIST):

    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var VIEW_LIST
    # List of all View instances in the scene.
    self.VIEW_LIST = VIEW_LIST

    ## @var local_portal_node
    # Scenegraph node to which the portal viewing nodes are copied and appended.
    self.local_portal_node = avango.gua.nodes.TransformNode(Name = "local_portal_group")
    self.SCENEGRAPH.Root.value.Children.value.append(self.local_portal_node)

  ## Tells all view instances that a new portal was added to the scene.
  # @param LOCAL_PORTAL_NODE Local copied portal node that was added.
  def notify_views_on_added_portal(self, LOCAL_PORTAL_NODE):

    for _view in self.VIEW_LIST:
      _view.create_portal_preview(LOCAL_PORTAL_NODE)

  ## Tells all view instances that a new portal was removed from the scene.
  # @param LOCAL_PORTAL_NODE Local copied portal node that was added.
  def notify_views_on_removed_portal(self, LOCAL_PORTAL_NODE):

    for _view in self.VIEW_LIST:
      _view.remove_portal_preview(LOCAL_PORTAL_NODE)

  ## Evaluated every frame.
  def evaluate(self):

    try:
      _portal_group_node = self.SCENEGRAPH["/net/portal_group"]
    except:
      return

    # connect mf_portal_group_children only once
    if _portal_group_node != None and self.mf_portal_group_children_connected == False:
      self.mf_portal_group_children.connect_from(_portal_group_node.Children)
      self.mf_portal_group_children_connected = True

  ## Called whenever mf_portal_group_children changes.
  @field_has_changed(mf_portal_group_children)
  def mf_portal_group_children_changed(self):

    # boolean list of which Portal instances have already been parsed.
    _instances_matched = [False for i in range(len(self.portals))]

    # iterate over all children of the server portal node
    for _node in self.mf_portal_group_children.value:

      _portal_instance_found = False
      
      # iterate over all Portal instances
      for _i in range(len(self.portals)):

        _portal = self.portals[_i]

        # check for matching instance and break when found
        if _portal.compare_server_portal_node(_node) == True:
          _portal_instance_found = True
          _instances_matched[_i] = True
          break

      # if no matching instance was found, add a new ClientPortal for the node
      if _portal_instance_found == False:
        _portal = ClientPortal(self.SCENEGRAPH["/local_portal_group"], _node)
        self.portals.append(_portal)
        self.notify_views_on_added_portal(_portal.portal_node)

    # check for instances that have not been matched (removed on server side)
    for _i in range(len(_instances_matched)):
      _bool = _instances_matched[_i]

      if _bool == False:

        _portal_to_delete = self.portals[_i]
        self.notify_views_on_removed_portal(_portal_to_delete.portal_node)

        self.SCENEGRAPH["/local_portal_group"].Children.value.remove(_portal_to_delete.portal_node)

        _portal_to_delete.deactivate()
        self.portals.remove(_portal_to_delete)

        # object destruction
        del _portal_to_delete.portal_node
        del _portal_to_delete


## Client counterpart for the server Portal class.
class ClientPortal:

  ## Custom constructor.
  # @param LOCAL_PORTAL_GROUP_NODE Local scenegraph node for grouping portal nodes.
  # @param SERVER_PORTAL_NODE New portal scenegraph node that was added on server side.
  def __init__(self, LOCAL_PORTAL_GROUP_NODE, SERVER_PORTAL_NODE):

    ## @var SERVER_PORTAL_NODE
    # New portal scenegraph node that was added on server side.
    self.SERVER_PORTAL_NODE = SERVER_PORTAL_NODE

    ## @var portal_node
    # Grouping node for this portal below the group node for all portals.
    self.portal_node = avango.gua.nodes.TransformNode(Name = SERVER_PORTAL_NODE.Name.value)
    LOCAL_PORTAL_GROUP_NODE.Children.value.append(self.portal_node)

    ## @var portal_matrix_node
    # Scenegraph node representing the location where the portal display is located (entry).
    self.portal_matrix_node = avango.gua.nodes.TransformNode(Name = "portal_matrix")
    self.portal_matrix_node.Transform.connect_from(SERVER_PORTAL_NODE.Children.value[1].Transform)
    self.portal_node.Children.value.append(self.portal_matrix_node)


  ## Disconnects all scenegraph node fields and deletes the nodes except portal_node.
  def deactivate(self):
    # disconnect fields
    self.portal_matrix_node.Transform.disconnect()

    # object destruction
    del self.portal_matrix_node

  ## Checks if a given server portal node matches with the server portal node of this instance.
  # @param SERVER_PORTAL_NODE The server portal node to be checked for.
  def compare_server_portal_node(self, SERVER_PORTAL_NODE):
    if self.SERVER_PORTAL_NODE == SERVER_PORTAL_NODE:
      return True

    return False


## A PortalPreView is instantiated for each View for each ClientPortal and displays the correct 
# perspective for the view within the portal.
class PortalPreView(avango.script.Script):

  ## @var sf_screen_width
  # Field containing the current width of the portal screen.
  sf_screen_width = avango.SFFloat()

  ## @var sf_screen_height
  # Field containing the current height of the portal screen.
  sf_screen_height = avango.SFFloat()

  ## @var mf_portal_modes
  # Field containing the GroupNames of the associated portal node. Used for transferring portal mode settings.
  mf_portal_modes = avango.MFString()


  # Default constructor.
  def __init__(self):
    self.super(PortalPreView).__init__()

  # Custom constructor.
  # @param PORTAL_NODE The portal scenegraph node on client side to be associated with this instance.
  # @param VIEW The View instance to be associated with this instance.
  def my_constructor(self, PORTAL_NODE, VIEW):
    
    ## @var PORTAL_NODE
    # The portal scenegraph node on client side to be associated with this instance.
    self.PORTAL_NODE = PORTAL_NODE

    # @var VIEW
    # The View instance to be associated with this instance.
    self.VIEW = VIEW

    ## @var left_eye_node
    # Scenegraph node representing the left eye's position in the portal's exit space.
    _user_left_eye = VIEW.SCENEGRAPH["/net/w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id) + "/head/eyeL"]

    # if no node is present, this view is not occupied, stop pre view creation
    if _user_left_eye == None:
      print_warning("No user nodes present for " + "w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id))
      return
    else:
      print_message("Construct PortalPreView for " + PORTAL_NODE.Name.value + " and w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id))

    ##
    #
    self.transformed_head_node = VIEW.SCENEGRAPH["/net/portal_group/" + PORTAL_NODE.Name.value + "/scene_matrix/head_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]

    ##
    #
    self.left_eye_node = self.transformed_head_node.Children.value[0]

    ##
    #
    self.right_eye_node = self.transformed_head_node.Children.value[1]

    ##
    #
    self.portal_matrix_node = VIEW.SCENEGRAPH["/net/portal_group/" + PORTAL_NODE.Name.value + "/portal_matrix/"]

    ##
    #
    self.client_portal_matrix_node = self.PORTAL_NODE.Children.value[0]

    ##
    #
    self.scene_matrix_node = VIEW.SCENEGRAPH["/net/portal_group/" + PORTAL_NODE.Name.value + "/scene_matrix/"]

    ## @var screen_node
    # Screen node representing the screen position in the portal's exit space.
    self.screen_node = VIEW.SCENEGRAPH["/net/portal_group/" + PORTAL_NODE.Name.value + "/scene_matrix/portal_screen"]
    
    ## @var camera
    # The camera from which this PortalPreView will be rendered.
    self.camera = avango.gua.nodes.Camera()
    self.camera.SceneGraph.value = VIEW.SCENEGRAPH.Name.value

    self.camera.LeftScreen.value = self.screen_node.Path.value
    self.camera.RightScreen.value = self.screen_node.Path.value
    self.camera.LeftEye.value = self.left_eye_node.Path.value
    self.camera.RightEye.value = self.right_eye_node.Path.value

    self.camera.RenderMask.value = "main_scene"

    ## @var pipeline
    # The pipeline used to render this PortalPreView. 
    self.pipeline = avango.gua.nodes.Pipeline()
    self.pipeline.Enabled.value = True
    self.pipeline.EnableGlobalClippingPlane.value = True
    self.pipeline.Camera.value = self.camera

    # init pipline value connections
    #self.pipeline.BackgroundMode.connect_from(VIEW.pipeline.BackgroundMode)
    self.pipeline.BackgroundTexture.connect_from(VIEW.pipeline.BackgroundTexture)
    self.pipeline.FogTexture.connect_from(VIEW.pipeline.FogTexture)
    self.pipeline.EnableBloom.connect_from(VIEW.pipeline.EnableBloom)
    self.pipeline.BloomIntensity.connect_from(VIEW.pipeline.BloomIntensity)
    self.pipeline.BloomThreshold.connect_from(VIEW.pipeline.BloomThreshold)
    self.pipeline.BloomRadius.connect_from(VIEW.pipeline.BloomRadius)
    self.pipeline.EnableSsao.connect_from(VIEW.pipeline.EnableSsao)
    self.pipeline.SsaoRadius.connect_from(VIEW.pipeline.SsaoRadius)
    self.pipeline.SsaoIntensity.connect_from(VIEW.pipeline.SsaoIntensity)
    #self.pipeline.EnableBackfaceCulling.connect_from(VIEW.pipeline.EnableBackfaceCulling)
    self.pipeline.EnableBackfaceCulling.value = False
    self.pipeline.EnableFrustumCulling.connect_from(VIEW.pipeline.EnableFrustumCulling)
    self.pipeline.EnableFXAA.connect_from(VIEW.pipeline.EnableFXAA)
    self.pipeline.AmbientColor.connect_from(VIEW.pipeline.AmbientColor)
    self.pipeline.EnableFog.connect_from(VIEW.pipeline.EnableFog)
    self.pipeline.FogStart.connect_from(VIEW.pipeline.FogStart)
    self.pipeline.FogEnd.connect_from(VIEW.pipeline.FogEnd)


    self.pipeline.LeftResolution.value = avango.gua.Vec2ui(1024, 1024)
    self.pipeline.RightResolution.value = self.pipeline.LeftResolution.value

    if VIEW.is_stereo:  
      self.pipeline.EnableStereo.value = True
    else:
      self.pipeline.EnableStereo.value = False

    self.pipeline.OutputTextureName.value = self.PORTAL_NODE.Name.value + "_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)
    
    self.pipeline.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
    self.pipeline.BackgroundTexture.value = "data/textures/sky.jpg"

    self.VIEW.pipeline.PreRenderPipelines.value.append(self.pipeline)

    # set render mask
    self.camera.RenderMask.value = "main_scene"

    ## @var textured_quad
    # The textured quad instance in which the portal view will be rendered.

    _loader = avango.gua.nodes.TriMeshLoader()

    #self.textured_plane = _loader.create_geometry_from_file('textured_plane',
    #                                                        'data/objects/plane.obj',
    #                                                        'data/materials/Stones.gmd',
    #                                                        avango.gua.LoaderFlags.LOAD_MATERIALS)
    #self.textured_plane.Transform.value =  avango.gua.make_rot_mat(90, 1, 0, 0) * \
    #                                       avango.gua.make_scale_mat(self.screen_node.Width.value, 1.0, self.screen_node.Height.value)
    #self.textured_plane.GroupNames.value = ["w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]
    #avango.gua.set_material_uniform('data/materials/Portal.gmd', "portal_texture", self.PORTAL_NODE.Name.value + "_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id))
    #print repr(self.PORTAL_NODE.Name.value + "_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id))
    #self.portal_matrix_node.Children.value.append(self.textured_plane)

    self.textured_quad = avango.gua.nodes.TexturedQuadNode(Name = "texture_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id),
                                                           Texture = self.PORTAL_NODE.Name.value + "_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id),
                                                           IsStereoTexture = self.VIEW.is_stereo,
                                                           Width = self.screen_node.Width.value,
                                                           Height = self.screen_node.Height.value)
    self.textured_quad.GroupNames.value = ["w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]

    #
    #self.textured_quad.GroupNames.value = ["main_scene"]
    self.client_portal_matrix_node.Children.value.append(self.textured_quad)


    ## @var back_geometry
    # Geometry being displayed when portal pre view is seen from behind.
    #self.back_geometry = _loader.create_geometry_from_file("back_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id), "data/objects/plane.obj", "data/materials/ShadelessBlue.gmd", avango.gua.LoaderFlags.DEFAULTS)
    #self.back_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.01) * avango.gua.make_rot_mat(90, 1, 0, 0) * avango.gua.make_scale_mat(self.screen_node.Width.value, 1.0, self.screen_node.Height.value)
    #self.back_geometry.GroupNames.value = ["do_not_display_groupasdf", "w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]
    #self.client_portal_matrix_node.Children.value.append(self.back_geometry)

    ## @var portal_border
    # Geometry node containing the portal's frame.
    self.portal_border = _loader.create_geometry_from_file("border_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id), "data/objects/screen.obj", "data/materials/ShadelessBlue.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.portal_border.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.portal_border.GroupNames.value = ["do_not_display_group", "w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]
    self.portal_border.Transform.value = avango.gua.make_scale_mat(self.textured_quad.Width.value, self.textured_quad.Height.value, 1.0)
    self.client_portal_matrix_node.Children.value.append(self.portal_border)

    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method.
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

    # init field connections
    self.mf_portal_modes.connect_from(VIEW.SCENEGRAPH["/net/portal_group/" + PORTAL_NODE.Name.value + "/settings"].GroupNames)
    self.sf_screen_width.connect_from(self.screen_node.Width)
    self.sf_screen_height.connect_from(self.screen_node.Height)

    # set evaluation policy
    self.always_evaluate(True)

  ## Compares a given portal node with the portal node associated with this instance.
  # @param PORTAL_NODE The portal node to be compared with.
  def compare_portal_node(self, PORTAL_NODE):
    if self.PORTAL_NODE == PORTAL_NODE:
      return True

    return False

  ## Updates the size of the portal according to the screen node.
  def update_size(self):
    try:
      self.textured_quad
    except:
      return

    self.textured_quad.Width.value = self.screen_node.Width.value
    self.textured_quad.Height.value = self.screen_node.Height.value
    #self.back_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.0001) * avango.gua.make_rot_mat(90, 1, 0, 0) * avango.gua.make_scale_mat(self.screen_node.Width.value, 1.0, self.screen_node.Height.value)
    self.portal_border.Transform.value = self.portal_border.Transform.value = avango.gua.make_scale_mat(self.textured_quad.Width.value, self.textured_quad.Height.value, 1.0)

  ## Removes this portal from the local portal group and destroys all the scenegraph nodes.
  def deactivate(self):

    # disable pipeline and evaluation loop
    self.frame_trigger.Active.value = False
    self.pipeline.Enabled.value = False

    self.portal_matrix_node.Children.value.remove(self.portal_border)
    del self.portal_border
    
    self.portal_matrix_node.Children.value.remove(self.textured_quad)
    del self.textured_quad
    #del self.back_geometry

    del self.pipeline
    del self.camera

  ## Computes the WorldTransform of a scenegraph node manually without using the pre-defined field.
  # @param NODE The scenegraph node to compute the world transformation for.
  def compute_world_transform(self, NODE):

    if NODE == None:
      return avango.gua.make_identity_mat()
    else:   
      return self.compute_world_transform(NODE.Parent.value) * NODE.Transform.value

  ## Called whenever mf_portal_modes changes.
  @field_has_changed(mf_portal_modes)
  def mf_portal_modes_changed(self):

    # check for deletion
    try:
      self.pipeline
    except:
      return

    # check for visibility
    if self.mf_portal_modes.value[4] == "4-False":
      self.frame_trigger.Active.value = False
      self.pipeline.Enabled.value = False
      self.textured_quad.GroupNames.value.append("do_not_display_group")
      self.portal_border.GroupNames.value.append("do_not_display_group")
      #self.back_geometry.GroupNames.value.append("do_not_display_group")
      return
    else:
      self.frame_trigger.Active.value = True
      self.pipeline.Enabled.value = True
      self.textured_quad.GroupNames.value.remove("do_not_display_group")
      self.portal_border.GroupNames.value.remove("do_not_display_group")

    # check for camera mode
    if self.mf_portal_modes.value[1] == "1-ORTHOGRAPHIC":
      self.camera.Mode.value = avango.gua.ProjectionMode.ORTHOGRAPHIC
    else:
      self.camera.Mode.value = avango.gua.ProjectionMode.PERSPECTIVE

    # check for negative parallax
    if self.mf_portal_modes.value[2] == "2-True":
      self.pipeline.EnableGlobalClippingPlane.value = False
    else:
      self.pipeline.EnableGlobalClippingPlane.value = True

    # set correct border material
    if self.portal_border.Material.value != self.mf_portal_modes.value[3].replace("3-", ""):
      
      _material = self.mf_portal_modes.value[3].replace("3-", "")

      if _material != "None":
        self.portal_border.Material.value = _material
        #self.back_geometry.Material.value = _material
        self.portal_border.GroupNames.value.remove("do_not_display_group")
        #self.back_geometry.GroupNames.value.remove("do_not_display_group")
      else:
        
        self.portal_border.GroupNames.value.append("do_not_display_group")
        #self.back_geometry.GroupNames.value.append("do_not_display_group")


  ## Evaluated every frame when active.
  def frame_callback(self):
    
    #print "frame callback"

    # update global clipping plane when negative parallax is false
    if self.mf_portal_modes.value[2] == "2-False":
      _portal_scene_mat = self.scene_matrix_node.Transform.value
      _vec = avango.gua.Vec3(0.0, 0.0, -1.0)
      _vec = avango.gua.make_rot_mat(_portal_scene_mat.get_rotate_scale_corrected()) * _vec
      _vec2 = _portal_scene_mat.get_translate()
      _vec2 = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_portal_scene_mat.get_rotate_scale_corrected())) * _vec2
      _dist = _vec2.z
      self.pipeline.GlobalClippingPlane.value = avango.gua.Vec4(_vec.x, _vec.y, _vec.z, _dist)

    _head_world_mat = self.compute_world_transform(self.VIEW.SCENEGRAPH["/net/w" + str(self.VIEW.workspace_id) + "_dg" + \
                      str(self.VIEW.display_group_id) + "_u" + str(self.VIEW.user_id) + "/head"])

    _view_in_portal_space = self.compute_world_transform(self.transformed_head_node)
    
    #print "Cat"

    # determine view in portal space and decide if renering is necessary
    _view_vec = avango.gua.make_rot_mat(_head_world_mat.get_rotate_scale_corrected()) * avango.gua.Vec3(0, 0, -1)
    _view_vec = avango.gua.Vec3(_view_vec.x, _view_vec.y, _view_vec.z)
    _portal_vec = avango.gua.make_rot_mat(self.portal_matrix_node.Transform.value.get_rotate()) * avango.gua.Vec3(0, 0, -1)
    _portal_vec = avango.gua.Vec3(_portal_vec.x, _portal_vec.y, _portal_vec.z)
    _angle = math.acos(_view_vec.dot(_portal_vec))

    #print "still Cat"

    if _view_in_portal_space.get_translate().z < 0 or math.degrees(_angle) > 100.0:

      if self.pipeline.Enabled.value == True:
        self.pipeline.Enabled.value = False
        #self.textured_quad.GroupNames.value.append("do_not_display_group")
        #self.back_geometry.GroupNames.value.remove("do_not_display_group")

    else:

      if self.pipeline.Enabled.value == False:
        self.pipeline.Enabled.value = True
        #self.textured_quad.GroupNames.value.remove("do_not_display_group")
        #self.back_geometry.GroupNames.value.append("do_not_display_group")

    #print "complete Cat"


  ## Called whenever sf_screen_width changes.
  @field_has_changed(sf_screen_width)
  def sf_screen_width_changed(self):
    self.update_size()

  ## Called whenever sf_screen_height changes.
  @field_has_changed(sf_screen_height)
  def sf_screen_height_changed(self):
    self.update_size()
