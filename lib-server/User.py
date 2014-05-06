#!/usr/bin/python

## @file
# Contains class User.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from TrackingReader import *

# import math libraries
import math

## Internal representation of a user.
#
# Upon construction, this class appends the necessary nodes to the scenegraph, creates eyes
# and initializes the headtracking.

class User:

  ## Custom constructor.
  # @param APPLICATION_MANAGER Reference to the ApplicationManager instance from which this user is created.
  # @param USER_ID Global user ID to be applied.
  # @param STEREO Boolean indicating if this user is a stereo or mono one.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param PLATFORM_ID Platform ID to which this user should be appended to.
  # @param AVATAR_MATERIAL The material string for the user avatar to be created.
  def __init__(self, APPLICATION_MANAGER, USER_ID, STEREO, HEADTRACKING_TARGET_NAME, PLATFORM_ID, AVATAR_MATERIAL):

    # variables
    ## @var APPLICATION_MANAGER
    # Reference to the ApplicationManager instance from which the user is created.
    self.APPLICATION_MANAGER = APPLICATION_MANAGER

    ## @var id
    # Identification number of the PowerWallUser, starting from 0.
    self.id = USER_ID

    ## @var platform_id
    # ID of the platform the user is belonging to.
    self.platform_id = PLATFORM_ID

    ## @var platform
    # Instance of the platform the user is belonging to.
    self.platform = self.APPLICATION_MANAGER.navigation_list[self.platform_id].platform

    ## @var transmitter_offset
    # The transmitter offset to be applied.
    self.transmitter_offset   = self.platform.transmitter_offset

    ## @var no_tracking_mat
    # The matrix to be applied when no tracking is available.
    self.no_tracking_mat      = self.platform.no_tracking_mat
    
    ## @var avatar_material
    # Material of the user's avatar.
    self.avatar_material = AVATAR_MATERIAL

    self.eye_distance = 0.0

    # init viewing setup 
    ## @var head_transform
    # Scenegraph node representing the head position of the user with respect to platform.
    self.head_transform = avango.gua.nodes.TransformNode(Name = "head_" + str(self.id))
    #self.platform.platform_transform_node.Children.value.append(self.head_transform)
    self.platform.platform_scale_transform_node.Children.value.append(self.head_transform)

    ## @var headtracking_reader
    # Instance of a child class of TrackingReader to supply translation input.
    if HEADTRACKING_TARGET_NAME == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(self.no_tracking_mat)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())
   
    # connect the tracking input to the scenegraph node
    self.head_transform.Transform.connect_from(self.headtracking_reader.sf_abs_mat)

    if STEREO:
      # create the eyes
      ## @var left_eye
      # Scenegraph node representing the user's left eye.
      self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
      self.left_eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.left_eye)

      ## @var right_eye
      # Scenegraph node representing the user's right eye.
      self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
      self.right_eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.right_eye)

      self.set_eye_distance(0.065)
      
    else:
      # create the eye
      ## @var eye
      # Scenegraph node representing the user's eye.
      self.eye = avango.gua.nodes.TransformNode(Name = "eye")
      self.eye.Transform.value = avango.gua.make_identity_mat()
      self.head_transform.Children.value.append(self.eye)

    # create avatar representation
    if self.platform.avatar_type == "joseph":
      self.create_avatar_representation(self.APPLICATION_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat, False)
    elif self.platform.avatar_type == "joseph_table":
      self.create_avatar_representation(self.APPLICATION_MANAGER.SCENEGRAPH, self.headtracking_reader.sf_avatar_body_mat, True)
    
    # create coupling notification plane
    self.create_coupling_plane()

    # create coupling status notifications
    self.create_coupling_status_overview()

  
  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    self.eye_distance = VALUE
  
    self.left_eye.Transform.value  = avango.gua.make_trans_mat(self.eye_distance * -0.5, 0.0, 0.0)
    self.right_eye.Transform.value = avango.gua.make_trans_mat(self.eye_distance * 0.5, 0.0, 0.0)

  ## Appends a node to the children of a platform in the scenegraph.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param NODE The node to be appended to the platform node.
  def append_to_platform(self, SCENEGRAPH, NODE):
    
    # find corresponding platform node
    _platform_path = "/net/platform_" + str(self.platform_id) + "/scale"
    _node = SCENEGRAPH.get_node(_platform_path)
    _node.Children.value.append(NODE)

    '''
    # find corresponding platform node
    for _node in self.APPLICATION_MANAGER.NET_TRANS_NODE.Children.value:
      if _node.Name.value == "platform_" + str(self.platform_id):
        _node.Children.value.append(NODE)
        break
    '''

  ## Creates a basic "joseph" avatar for this user.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param SF_AVATAR_BODY_MATRIX Field containing the transformation matrix for the avatar's body on the platform.
  # @param TABLE_ENABLED Boolean indicating if a table should be added to the avatar.
  def create_avatar_representation(self, SCENEGRAPH, SF_AVATAR_BODY_MATRIX, TABLE_ENABLED):

    _loader = avango.gua.nodes.GeometryLoader()
    
    # create avatar head
    ## @var head_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_avatar = _loader.create_geometry_from_file( 'head_avatar_' + str(self.id),
                                                          'data/objects/Joseph/JosephHead.obj',
                                                          'data/materials/' + self.avatar_material + '.gmd',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.head_avatar.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
    self.head_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    self.head_transform.Children.value.append(self.head_avatar)

    # create avatar body
    ## @var body_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_avatar = _loader.create_geometry_from_file( 'head_avatar_' + str(self.id),
                                                          'data/objects/Joseph/JosephBody.obj',
                                                          'data/materials/' + self.avatar_material + '.gmd',
                                                          avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.body_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]
    
    self.append_to_platform(SCENEGRAPH, self.body_avatar)

    self.body_avatar.Transform.connect_from(SF_AVATAR_BODY_MATRIX)

    # create table avatar if enabled
    if TABLE_ENABLED:

      ## @var table_transform
      # Scenegraph transform node for the dekstop user's table.
      self.table_transform = avango.gua.nodes.TransformNode(Name = 'table_transform')
      self.table_transform.Transform.value = avango.gua.make_trans_mat(-0.8, 0.2, 0.8)
      self.body_avatar.Children.value.append(self.table_transform)

      ## @var table_avatar
      # Scenegraph node representing the geometry and transformation of the desktop user's table.
      self.table_avatar = _loader.create_geometry_from_file( 'table_avatar_' + str(self.id),
                                                             'data/objects/table/table.obj',
                                                             'data/materials/' + self.avatar_material + '.gmd',
                                                             avango.gua.LoaderFlags.LOAD_MATERIALS)
      self.table_avatar.Transform.value = avango.gua.make_scale_mat(0.2, 0.5, 0.5)
      self.table_transform.Children.value.append(self.table_avatar)
      self.table_avatar.GroupNames.value = ['avatar_group_' + str(self.platform_id)]


  ## Creates a plane in front of the user used for displaying coupling messages.
  def create_coupling_plane(self):
    
    _loader = avango.gua.nodes.GeometryLoader()

    ## @var message_plane_node
    # Transform node combining coupling and decoupling message geometry nodes.
    self.message_plane_node = avango.gua.nodes.TransformNode(Name = "message_plane_node")

    # set transform values and extend scenegraph
    self.handle_message_plane_node()

    ## @var coupling_plane_node
    # Geometry node representing a plane for displaying messages to users.
    # Visibility will be toggled by StatusManager.
    self.coupling_plane_node = _loader.create_geometry_from_file('notification_geometry',
                                                                 'data/objects/plane.obj',
                                                                 'data/materials/CouplingPlane.gmd',
                                                                 avango.gua.LoaderFlags.LOAD_MATERIALS)

    self.coupling_plane_node.Transform.value = avango.gua.make_scale_mat(0.6 * self.platform.screens[0].Width.value, 0.1, 0.2 * self.platform.screens[0].Height.value)

    self.coupling_plane_node.GroupNames.value = ["do_not_display_group", "platform_group_" + str(self.platform_id)]

    self.message_plane_node.Children.value.append(self.coupling_plane_node)

    ## @var decoupling_notifier
    # Geometry node representing a plane showing the color of a navigation that was recently decoupled.
    # Actual material and visibility will be toggled by StatusManager.
    self.decoupling_notifier = _loader.create_geometry_from_file('decoupling_notifier',
                                                                 'data/objects/plane.obj',
                                                                 'data/materials/AvatarWhiteShadeless.gmd',
                                                                 avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.decoupling_notifier.Transform.value =  avango.gua.make_trans_mat(0.0, 0.0, -0.2 * self.platform.screens[0].Height.value) * \
                                                avango.gua.make_scale_mat(0.2, 0.2, 0.2)

    self.decoupling_notifier.GroupNames.value = ["do_not_display_group", "platform_group_" + str(self.platform_id)]

    self.message_plane_node.Children.value.append(self.decoupling_notifier)


  ## Creates an overview of the user's current couplings in his or her field of view.
  def create_coupling_status_overview(self):
    
    _loader = avango.gua.nodes.GeometryLoader()
 
    # create transformation node
    ## @var coupling_status_node
    # Scenegraph transformation node for coupling icons in the user's field of view.
    self.coupling_status_node = avango.gua.nodes.TransformNode(Name = "coupling_status_" + str(self.id))
    self.coupling_status_node.GroupNames.value = ["display_group", "platform_group_" + str(self.platform_id)]

    # sets the necessary attributes for correct positioning of coupling status notifiers
    self.handle_coupling_status_attributes()

    # create icon indicating the own color
    ## @var own_color_geometry
    # Plane visible to the user indictating his or her own avatar color.
    self.own_color_geometry = _loader.create_geometry_from_file('user_' + str(self.id) +'_own_notifier',
                                                                'data/objects/plane.obj',
                                                                'data/materials/' + self.avatar_material + 'Shadeless.gmd',
                                                                avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.own_color_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF

    self.coupling_status_node.Children.value.append(self.own_color_geometry)

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
        _scale = self.start_scale * 0.6
      else:
        _scale = self.start_scale

      _current_node.Transform.value = avango.gua.make_trans_mat(_current_trans) * \
                                      avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                      avango.gua.make_scale_mat(_scale, _scale, _scale)

  ## Correctly places and appends the message plane node in and to the scenegraph.
  def handle_message_plane_node(self):
    self.message_plane_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * \
                                              avango.gua.make_rot_mat(90, 1, 0, 0)

    _screen = self.platform.screens[0] # primary screen
    _screen.Children.value.append(self.message_plane_node)
    

  ## Handles all the specialized settings for the coupling status overview.
  def handle_coupling_status_attributes(self):
    self.coupling_status_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    
    self.platform.screens[0].Children.value.append(self.coupling_status_node)

    # TODO: Make generic size

    ## @var start_trans
    # Translation of the first coupling status notifier (own color).
    self.start_trans = avango.gua.Vec3(-0.45 * self.platform.screens[0].Width.value, 0.4 * self.platform.screens[0].Height.value, 0.0)

    ## @var start_scale
    # Scaling of the first coupling status notifier (own color).
    self.start_scale = 0.05 * self.platform.screens[0].Height.value
      
    ## @var y_increment
    # Y offset for all coupling status notifiers after the own color.
    self.y_increment = -self.start_scale
