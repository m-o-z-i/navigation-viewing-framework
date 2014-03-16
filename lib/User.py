#!/usr/bin/python

## @file
# Contains class User.

# import guacamole libraries
import avango
import avango.gua

# import python libraries
import math

## Base class to represent attributes and functions that all users have in common. Not to be instantiated.
class User:
  
  # output fields
  ## @var sf_abs_head_mat
  # Position and rotation of the user's head with respect to the platform.
  sf_abs_head_mat = avango.gua.SFMatrix4()
  sf_abs_head_mat = avango.gua.make_identity_mat()

  # pipeline values to be used
  ## @var enable_bloom
  # Boolean variable to enable bloom on all pipelines.
  enable_bloom = True

  ## @var bloom_intensity
  # Bloom intensity value for all pipelines.
  bloom_intensity = 0.1

  ## @var bloom_threshold
  # Bloom threshold value for all pipelines.
  bloom_threshold = 1.0

  ## @var bloom_radius
  # Bloom radius value for all pipelines.
  bloom_radius = 10

  ## @var enable_fxaa
  # Boolean variable to enable FXAA on all pipelines.
  enable_fxaa = False

  ## @var enable_fog
  # Boolean variable to enable fog on all pipelines.
  enable_fog = True

  ## @var fog_start
  # Fog starting distance for all pipelines.
  fog_start = 300.0

  ## @var fog_end
  # Fog ending distance for all pipelines.
  fog_end = 400.0

  ## @var enable_frustum_culling
  # Boolean variable to enable frustum culling on all pipelines.
  enable_frustum_culling = False

  ## @var ambient_color
  # Ambient color value for all pipelines.
  ambient_color = avango.gua.Color(0.5, 0.5, 0.5)

  ## @var far_clip
  # Distance of the far clipping plane for all pipelines.
  far_clip = 800.0

  ## @var enable_backface_culling
  # Boolean variable to enable backface culling on all pipelines.
  enable_backface_culling = False

  ## @var enable_ssao
  # Boolean variable to enable Ssao on all pipelines.
  enable_ssao = True

  ## @var ssao_radius
  # Ssao radius value for all pipelines.
  ssao_radius = 2.0

  ## @var ssao_intensity
  # Ssao intensity value for all pipelines.
  ssao_intensity = 2.0

  ## @var enable_fps_display
  # Boolean variable to enable FPS display on all pipelines.
  enable_fps_display = True

  ## Custom constructor.
  # @param NODE_PRETEXT The prefix to be used when creating scenegraph nodes.
  # @param AVATAR_MATERIAL Material to be used for the user's avatar.
  def __init__(self, NODE_PRETEXT, AVATAR_MATERIAL):

    ## @var node_pretext
    # Prefix of the scenegraph nodes this user creates.
    self.node_pretext = NODE_PRETEXT

    ## @var avatar_material
    # Material of the user's avatar.
    self.avatar_material = AVATAR_MATERIAL

  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    self.left_eye.Transform.value  = avango.gua.make_trans_mat(VALUE * -0.5, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(VALUE * 0.5, 0.0, 0.0)

  ## Sets all the pipeline values to the ones specified in User class.
  def set_pipeline_values(self):
    self.pipeline.EnableBloom.value             = self.enable_bloom
    self.pipeline.BloomIntensity.value          = self.bloom_intensity
    self.pipeline.BloomThreshold.value          = self.bloom_threshold
    self.pipeline.BloomRadius.value             = self.bloom_radius
    self.pipeline.EnableFXAA.value              = self.enable_fxaa
    self.pipeline.EnableFog.value               = self.enable_fog
    self.pipeline.FogStart.value                = self.fog_start
    self.pipeline.FogEnd.value                  = self.fog_end
    self.pipeline.EnableFrustumCulling.value    = self.enable_frustum_culling
    self.pipeline.AmbientColor.value            = self.ambient_color
    self.pipeline.FarClip.value                 = self.far_clip
    self.pipeline.EnableBackfaceCulling.value   = self.enable_backface_culling
    self.pipeline.EnableSsao.value              = self.enable_ssao
    self.pipeline.SsaoRadius.value              = self.ssao_radius
    self.pipeline.SsaoIntensity.value           = self.ssao_intensity
    self.pipeline.EnableFPSDisplay.value        = self.enable_fps_display
    #self.pipeline.BackgroundMode.value          = avango.gua.BackgroundMode.SKYMAP_TEXTURE
    self.pipeline.FogTexture.value              = self.pipeline.BackgroundTexture.value

  ## Appends a node to the children of a platform in the scenegraph.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param NODE The node to be appended to the platform node.
  def append_to_platform(self, SCENEGRAPH, NODE):
    SCENEGRAPH['/platform_' + str(self.platform_id)].Children.value.append(NODE)

  ## Creates a basic avatar for this user.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param SF_AVATAR_BODY_MATRIX Field containing the transformation matrix for the avatar's body on the platform.
  def create_avatar_representation(self, SCENEGRAPH, SF_AVATAR_BODY_MATRIX):

    _loader = avango.gua.nodes.GeometryLoader()
    
    # create avatar head
    ## @var head_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_avatar = _loader.create_geometry_from_file( self.node_pretext + '_head_avatar_' + str(self.platform_id),
                                                          'data/objects/default_avatar_head.obj',
                                                          self.avatar_material,
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.head_avatar.Transform.value = avango.gua.make_rot_mat(90, 0, 1, 0) * avango.gua.make_scale_mat(0.2, 0.2, 0.2)
    self.head_avatar.GroupNames.value = [self.node_pretext + '_avatar_group_' + str(self.platform_id)]
    self.head_transform.Children.value.append(self.head_avatar)

    # create avatar body
    ## @var body_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_avatar = _loader.create_geometry_from_file( self.node_pretext + '_body_avatar_' + str(self.platform_id),
                                                          'data/objects/default_avatar_body.obj',
                                                          self.avatar_material,
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.body_avatar.GroupNames.value = [self.node_pretext + '_avatar_group_' + str(self.platform_id)]
    SCENEGRAPH['/platform_' + str(self.platform_id)].Children.value.append(self.body_avatar)

    self.body_avatar.Transform.connect_from(SF_AVATAR_BODY_MATRIX)

    # create desktop user table
    if self.node_pretext == "desktop":

      ## @var table_transform
      # Scenegraph transform node for the dekstop user's table.
      self.table_transform = avango.gua.nodes.TransformNode(Name = 'table_transform')
      self.table_transform.Transform.value = avango.gua.make_trans_mat(0, -0.5, -3)
      self.body_avatar.Children.value.append(self.table_transform)

      ## @var table_avatar
      # Scenegraph node representing the geometry and transformation of the desktop user's table.
      self.table_avatar = _loader.create_geometry_from_file( self.node_pretext + '_desktop_avatar_' + str(self.platform_id),
                                                             'data/objects/cube.obj',
                                                             self.avatar_material,
                                                             avango.gua.LoaderFlags.LOAD_MATERIALS)
      self.table_avatar.Transform.value =  avango.gua.make_scale_mat(3.0, 0.5, 1.0)
      self.table_transform.Children.value.append(self.table_avatar)
      self.table_avatar.GroupNames.value = [self.node_pretext + '_avatar_group_' + str(self.platform_id)]

  ## Creates a plane in front of the user used for displaying coupling messages.
  def create_coupling_plane(self):
    
    _loader = avango.gua.nodes.GeometryLoader()

    ## @var message_plane_node
    # Transform node combining coupling and decoupling message geometry nodes.
    self.message_plane_node = avango.gua.nodes.TransformNode(Name = "message_plane_node")

    # set transform values and extend scenegraph
    if self.node_pretext == "ovr":
      self.message_plane_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.98) * \
                                                avango.gua.make_rot_mat(90, 1, 0, 0)
      self.head_transform.Children.value.append(self.message_plane_node)
    else:
      self.message_plane_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.18) * \
                                                avango.gua.make_rot_mat(90, 1, 0, 0)
      self.screen.Children.value.append(self.message_plane_node)


    ## @var coupling_plane_node
    # Geometry node representing a plane for displaying messages to users.
    # Visibility will be toggled by StatusManager.
    self.coupling_plane_node = _loader.create_geometry_from_file('notification_geometry',
                                                                 'data/objects/plane.obj',
                                                                 'CouplingPlane',
                                                                 avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.coupling_plane_node.Transform.value = avango.gua.make_scale_mat(1.0, 0.2, 0.2)

    self.coupling_plane_node.GroupNames.value = ["do_not_display_group", "platform_group_" + str(self.platform_id)]

    self.message_plane_node.Children.value.append(self.coupling_plane_node)

    ## @var decoupling_notifier
    # Geometry node representing a plane showing the color of a navigation that was recently decoupled.
    # Actual material and visibility will be toggled by StatusManager.
    self.decoupling_notifier = _loader.create_geometry_from_file('decoupling_notifier',
                                                                 'data/objects/plane.obj',
                                                                 'AvatarWhiteShadeless',
                                                                 avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.decoupling_notifier.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.25) * \
                                               avango.gua.make_scale_mat(0.2, 0.2, 0.2)

    self.decoupling_notifier.GroupNames.value = ["do_not_display_group", "platform_group_" + str(self.platform_id)]

    self.message_plane_node.Children.value.append(self.decoupling_notifier)


  ## Creates an overview of the user's current couplings in his or her field of view.
  def create_coupling_status_overview(self):
    
    _loader = avango.gua.nodes.GeometryLoader()
 
    # create transformation node
    ## @var coupling_status_node
    # Scenegraph transformation node for coupling icons in the user's field of view.
    self.coupling_status_node = avango.gua.nodes.TransformNode(Name = self.node_pretext + "_status_" + str(self.platform_id))
    self.coupling_status_node.GroupNames.value = ["display_group", "platform_group_" + str(self.platform_id)]

    if self.node_pretext == "ovr":
      self.coupling_status_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -1.0)
      self.head_transform.Children.value.append(self.coupling_status_node)
    else:
      self.coupling_status_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.2)
      self.screen.Children.value.append(self.coupling_status_node)
 

    # create icon indicating the own color
    ## @var own_color_geometry
    # Plane visible to the user indictating his or her own avatar color.
    self.own_color_geometry = _loader.create_geometry_from_file(self.node_pretext + str(self.id) +'_own_notifier',
                                                                'data/objects/plane.obj',
                                                                self.avatar_material + 'Shadeless',
                                                                avango.gua.LoaderFlags.LOAD_MATERIALS)

    self.coupling_status_node.Children.value.append(self.own_color_geometry)

    # sets the necessary attributes for correct positioning of coupling status notifiers
    if self.node_pretext == "ovr":

      ## @var start_trans
      # Translation of the first coupling status notifier (own color).
      self.start_trans = avango.gua.Vec3(-0.3, 0.35, 0.0)
      
      ## @var start_scale
      # Scaling of the first coupling status notifier (own color).
      self.start_scale = 0.05
      
      ## @var y_increment
      # Y offset for all coupling status notifiers after the own color.
      self.y_increment = -0.06

    elif self.node_pretext == "wall":
      self.start_trans = avango.gua.Vec3(-0.433 * self.screen.Width.value, 0.454 * self.screen.Height.value, 0.0)
      self.start_scale = 0.1
      self.y_increment = -0.14
    else:
      # adapt values according to physical screen size
      self.start_trans = avango.gua.Vec3(-0.5 * self.screen.Width.value, 0.47 * self.screen.Height.value, 0.0)
      self.start_scale = 0.05
      self.y_increment = -0.06

    self.update_coupling_status_overview()

  ## Updates the Transform fields of coupling_status_node's children.
  # Can only be called after create_coupling_status_overview()
  def update_coupling_status_overview(self):

    # get all children nodes
    _children_nodes = self.coupling_status_node.Children.value

    # write transformation for all children with respect to y increments
    for i in range(0, len(_children_nodes)):
      _current_node = _children_nodes[i]

      # set translation of notifiers properly
      _current_trans = avango.gua.Vec3(self.start_trans)
      _current_trans.y += i * self.y_increment

      # make coupling notifiers smaller
      if i != 0:
        _scale = self.start_scale - 0.02
      else:
        _scale = self.start_scale

      _current_node.Transform.value = avango.gua.make_trans_mat(_current_trans) * \
                                      avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                      avango.gua.make_scale_mat(_scale, _scale, _scale)