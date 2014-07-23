#!/usr/bin/python

## @file
# Contains class Slot.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from BorderObserver import *

# import python libraries
import time

## Internal representation of a display slot. A Slot is one rendering output that can be handled
# by a display. User can have multiple slots to obtain a brighter image.
class Slot(avango.script.Script):

  ## Default constructor.
  def __init__(self):
    self.super(Slot).__init__()

  ## Custom constructor.
  # @param DISPLAY Display instance for which this slot is being created.
  # @param SLOT_ID Identification number of the slot within the display.
  # @param SCREEN_NUM Number of the screen / display on the platform.
  # @param STEREO Boolean indicating if the slot to be created is a stereo one.
  # @param PLATFORM Platform instance to which the slot is to be appended to.
  def my_constructor(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM):

    ## @var start_time
    # Time when a decoupling notifier was displayed.
    self.start_time = None

    ## @var slot_id
    # Identification number of the slot within the display.
    self.slot_id = SLOT_ID

    ## @var screen_num
    # Number of the screen / display on the platform.
    self.screen_num = SCREEN_NUM

    ## @var stereo
    # Boolean indicating if this slot is a stereo one.
    self.stereo = STEREO

    ## @var PLATFORM
    # Platform instance to which the slot is to be appended to.
    self.PLATFORM = PLATFORM

    ## @var PLATFORM_NODE
    # Scenegraph transformation node of the platform where the slot is appended to.
    self.PLATFORM_NODE = self.PLATFORM.platform_transform_node

    ## @var assigned_user
    # User instance which was assigned to this Slot by the SlotManager.
    self.assigned_user = None

    ## @var shutter_timing
    # A list of opening and closing times of shutter glasses for this slot.
    if self.stereo and DISPLAY.stereomode == "SIDE_BY_SIDE":
      self.shutter_timing = DISPLAY.shutter_timings[SLOT_ID]
    else:
      self.shutter_timing = None

    ## @var shutter_value
    # A list of hexadecimal commands for shutter glasses associated with the timings for this slot.
    if self.stereo and DISPLAY.stereomode == "SIDE_BY_SIDE":
      self.shutter_value = DISPLAY.shutter_values[SLOT_ID]
    else:
      self.shutter_value = None

    # append nodes to platform transform node

    ## @var slot_node
    # Scenegraph transformation node of this slot.
    self.slot_node = avango.gua.nodes.TransformNode(Name = "s" + str(SCREEN_NUM) + "_slot" + str(SLOT_ID))
    self.PLATFORM_NODE.Children.value.append(self.slot_node)

    ## @var slot_scale_node
    # Scenegraph node representing this slot's scale. Is below slot_node.
    self.slot_scale_node = avango.gua.nodes.TransformNode(Name = "scale")
    self.slot_node.Children.value = [self.slot_scale_node]

    if self.PLATFORM.avatar_type == "joseph":

      _loader = avango.gua.nodes.TriMeshLoader()

      ## @var head_avatar
      # Scenegraph node representing the geometry and transformation of the basic avatar's head.
      self.head_avatar = _loader.create_geometry_from_file( 'head_avatar',
                                                            'data/objects/Joseph/JosephHead.obj',
                                                            'data/materials/' + self.PLATFORM.avatar_material + '.gmd',
                                                            avango.gua.LoaderFlags.LOAD_MATERIALS)
      self.head_avatar.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
      self.head_avatar.GroupNames.value = ['do_not_display_group', 'avatar_group_' + str(self.PLATFORM.platform_id)]
      self.slot_scale_node.Children.value.append(self.head_avatar)

      ## @var body_avatar
      # Scenegraph node representing the geometry and transformation of the basic avatar's body.
      self.body_avatar = _loader.create_geometry_from_file( 'body_avatar',
                                                            'data/objects/Joseph/JosephBody.obj',
                                                            'data/materials/' + self.PLATFORM.avatar_material + '.gmd',
                                                            avango.gua.LoaderFlags.LOAD_MATERIALS)
      self.body_avatar.GroupNames.value = ['do_not_display_group', 'avatar_group_' + str(self.PLATFORM.platform_id)]
      self.slot_scale_node.Children.value.append(self.body_avatar)

    elif self.PLATFORM.avatar_type.endswith(".ks"):

      _loader = avango.gua.nodes.TriMeshLoader()
      _video_loader = avango.gua.nodes.Video3DLoader()

      ## @var video_geode
      # Video3D node containing the caputred video geometry.
      self.video_geode = _video_loader.load("kinect", self.PLATFORM.avatar_type)

      self.video_geode.Transform.value = self.PLATFORM.transmitter_offset
      self.slot_scale_node.Children.value.append(self.video_geode)
      self.video_geode.GroupNames.value = ['do_not_display_group', 'avatar_group_' + str(self.PLATFORM.platform_id), 'video'] # own group avatars not visible (only for WALL setups)

      ## @var video_abstraction_transform
      # Transform node for the placement of the video abstraction.
      self.video_abstraction_transform = avango.gua.nodes.TransformNode(Name = "video_abstraction_transform")
      self.video_abstraction_transform.Transform.connect_from(self.PLATFORM.INPUT_MAPPING_INSTANCE.DEVICE_INSTANCE.sf_station_mat)
      self.slot_scale_node.Children.value.append(self.video_abstraction_transform)

      ## @var video_abstraction
      # Abstract geometry displayed when too far away from the video geode.
      self.video_abstraction = _loader.create_geometry_from_file('video_abstraction',
                                                                 'data/objects/sphere.obj',
                                                                 'data/materials/' + self.PLATFORM.avatar_material + 'Shadeless.gmd',
                                                                 avango.gua.LoaderFlags.DEFAULTS)
      self.video_abstraction.Transform.value = avango.gua.make_scale_mat(2.0)
      self.video_abstraction.GroupNames.value = ["do_not_display_group", "video_abstraction", "server_do_not_display_group"]
      self.video_abstraction_transform.Children.value.append(self.video_abstraction)

    ## @var screen
    # Screen of this Slot.
    self.screen = DISPLAY.create_screen_node("screen")

    if self.screen != None:
      self.slot_scale_node.Children.value.append(self.screen)

    ## @var head_node
    # Scenegraph node to which the headtracking matrix of the assigned user is connected to.
    self.head_node = avango.gua.nodes.TransformNode(Name = "head")
    self.slot_scale_node.Children.value.append(self.head_node)

    ## @var information_node
    # Node whose name is set to the headtracking target name of the current user. Used for the local
    # headtracking update on client side. Transform is transmitter offset to be applied
    self.information_node = avango.gua.nodes.TransformNode(Name = "None")
    self.head_node.Children.value.append(self.information_node)

    ## @var no_tracking_node
    # Node whose Transform field contains the no tracking matrix to be applied for the headtracking.
    # Used for the local headtracking update on client side.
    self.no_tracking_node = avango.gua.nodes.TransformNode(Name = "no_tracking_mat")
    self.information_node.Children.value.append(self.no_tracking_node)

    # create the eyes
    ## @var left_eye
    # Representation of the slot's user's left eye.
    self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
    self.left_eye.Transform.value = avango.gua.make_identity_mat()
    self.head_node.Children.value.append(self.left_eye)

    ## @var right_eye
    # Representation of the slot's user's right eye.
    self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
    self.right_eye.Transform.value = avango.gua.make_identity_mat()
    self.head_node.Children.value.append(self.right_eye)

    if self.stereo == False:
      self.set_eye_distance(0.0)

    self.append_platform_border_nodes()
    self.create_coupling_status_overview()
    self.create_coupling_plane()

    # set evaluation policy
    self.always_evaluate(True)

  ## Sets the transformation values of left and right eye.
  # @param VALUE The eye distance to be applied.
  def set_eye_distance(self, VALUE):
    if self.stereo:
      self.left_eye.Transform.value  = avango.gua.make_trans_mat(VALUE * -0.5, 0.0, 0.0)
      self.right_eye.Transform.value = avango.gua.make_trans_mat(VALUE * 0.5, 0.0, 0.0)

  ## Assigns a user to this slot. Therefore, the slot_node is connected with the user's headtracking matrix.
  # @param USER_INSTANCE An instance of User which is to be assigned.
  def assign_user(self, USER_INSTANCE):
    
    # connect tracking matrix
    self.head_node.Transform.connect_from(USER_INSTANCE.headtracking_reader.sf_abs_mat)

    self.assigned_user = USER_INSTANCE

    if self.stereo:
      self.set_eye_distance(self.assigned_user.eye_distance)
 
    # set information node
    if USER_INSTANCE.headtracking_target_name == None:
      self.information_node.Name.value = "None"
    else:
      self.information_node.Name.value = USER_INSTANCE.headtracking_target_name

    # feed Transform field of information node with transmitter_offset
    self.information_node.Transform.value = USER_INSTANCE.transmitter_offset

    # feed Transform field of no tracking node with no_tracking_mat
    self.no_tracking_node.Transform.value = USER_INSTANCE.no_tracking_mat

  ## Clears the user assignment.
  def clear_user(self):

    if self.assigned_user != None:

      self.head_node.Transform.disconnect()
      self.head_node.Transform.value = avango.gua.make_identity_mat()

      if self.PLATFORM.avatar_type == "joseph":
        self.head_avatar.Transform.disconnect()
        self.body_avatar.Transform.disconnect()
        self.head_avatar.GroupNames.value.append('do_not_display_group')
        self.body_avatar.GroupNames.value.append('do_not_display_group')
      elif self.PLATFORM.avatar_type.endswith(".ks"):
        self.video_geode.GroupNames.value.append('do_not_display_group')

      self.assigned_user = None
      self.information_node.Name.value = "None"
      self.information_node.Transform.value = avango.gua.make_identity_mat()
      self.no_tracking_node.Transform.value = avango.gua.make_identity_mat()

  ## Appends the four platform border nodes to slot_scale_nodes and create a BorderObserver.
  def append_platform_border_nodes(self):

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var left_border
    # Geometry scenegraph node of the platform's left border
    self.left_border = _loader.create_geometry_from_file('left_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.left_border.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.left_border.Transform.value = avango.gua.make_trans_mat(-self.PLATFORM.width/2, 1.0, self.PLATFORM.depth/2) * \
                                       avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                       avango.gua.make_rot_mat(270, 0, 0, 1) * \
                                       avango.gua.make_scale_mat(self.PLATFORM.depth, 1, 2)
    self.left_border.GroupNames.value = ["do_not_display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]
    self.slot_scale_node.Children.value.append(self.left_border)    
    
    ## @var right_border
    # Geometry scenegraph node of the platform's left border
    self.right_border = _loader.create_geometry_from_file('right_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.right_border.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.right_border.Transform.value = avango.gua.make_trans_mat(self.PLATFORM.width/2, 1.0, self.PLATFORM.depth/2) * \
                                        avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                        avango.gua.make_rot_mat(90, 0, 0, 1) * \
                                        avango.gua.make_scale_mat(self.PLATFORM.depth, 1, 2)
    self.right_border.GroupNames.value = ["do_not_display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]
    self.slot_scale_node.Children.value.append(self.right_border)    

    ## @var front_border
    # Geometry scenegraph node of the platform's front border
    self.front_border = _loader.create_geometry_from_file('front_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.front_border.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.front_border.Transform.value = avango.gua.make_trans_mat(0, 1, 0) * \
                                        avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                        avango.gua.make_scale_mat(self.PLATFORM.width, 1, 2)
    self.front_border.GroupNames.value = ["do_not_display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]
    self.slot_scale_node.Children.value.append(self.front_border)

    ## @var back_border
    # Geometry scenegraph node of the platform's back border
    self.back_border = _loader.create_geometry_from_file('back_border_geometry',
                                                         'data/objects/plane.obj',
                                                         'data/materials/PlatformBorder.gmd',
                                                         avango.gua.LoaderFlags.DEFAULTS)
    self.back_border.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.back_border.Transform.value = avango.gua.make_trans_mat(0.0, 1.0, self.PLATFORM.depth) * \
                                        avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                        avango.gua.make_rot_mat(180, 0, 0, 1) * \
                                        avango.gua.make_scale_mat(self.PLATFORM.width, 1, 2)
    self.back_border.GroupNames.value = ["do_not_display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]
    self.slot_scale_node.Children.value.append(self.back_border)

    ## @var border_observer
    # Instance of BorderObserver to toggle border visibilities for this slot.
    self.border_observer = BorderObserver()
    self.border_observer.my_constructor([True, True, True, True], self, self.PLATFORM.width, self.PLATFORM.depth)

  ## Toggles visibility of left border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_left_border(self, VISIBLE):
    if VISIBLE:
      self.left_border.GroupNames.value[0] = "display_group"
    else:
      self.left_border.GroupNames.value[0] = "do_not_display_group"

  ## Toggles visibility of right border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_right_border(self, VISIBLE):
    if VISIBLE:
      self.right_border.GroupNames.value[0] = "display_group"
    else:
      self.right_border.GroupNames.value[0] = "do_not_display_group"

  ## Toggles visibility of front border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_front_border(self, VISIBLE):
    if VISIBLE:
      self.front_border.GroupNames.value[0] = "display_group"
    else:
      self.front_border.GroupNames.value[0] = "do_not_display_group"

  ## Toggles visibility of back border.
  # @param VISIBLE A boolean value if the border should be set visible or not.
  def display_back_border(self, VISIBLE):
    if VISIBLE:
      self.back_border.GroupNames.value[0] = "display_group"
    else:
      self.back_border.GroupNames.value[0] = "do_not_display_group"


  ## Creates an overview of the user's current couplings in his or her field of view.
  def create_coupling_status_overview(self):
    
    _loader = avango.gua.nodes.TriMeshLoader()
 
    # create transformation node
    ## @var coupling_status_node
    # Scenegraph transformation node for coupling icons in the user's field of view.
    self.coupling_status_node = avango.gua.nodes.TransformNode(Name = "coupling_status")
    self.coupling_status_node.GroupNames.value = ["display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]

    # sets the necessary attributes for correct positioning of coupling status notifiers
    self.handle_coupling_status_attributes()

    # create icon indicating the own color
    ## @var own_color_geometry
    # Plane visible to the user indictating his or her own avatar color.
    self.own_color_geometry = _loader.create_geometry_from_file('own_notifier',
                                                                'data/objects/plane.obj',
                                                                'data/materials/' + self.PLATFORM.avatar_material + 'Shadeless.gmd',
                                                                avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.own_color_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.own_color_geometry.GroupNames.value = ["p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]

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

  ## Handles all the specialized settings for the coupling status overview.
  def handle_coupling_status_attributes(self):
    self.coupling_status_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    
    # append to primary screen
    self.screen.Children.value.append(self.coupling_status_node)

    ## @var start_trans
    # Translation of the first coupling status notifier (own color).
    self.start_trans = avango.gua.Vec3(-0.45 * self.screen.Width.value, 0.4 * self.screen.Height.value, 0.0)

    ## @var start_scale
    # Scaling of the first coupling status notifier (own color).
    self.start_scale = 0.05 * self.screen.Height.value
      
    ## @var y_increment
    # Y offset for all coupling status notifiers after the own color.
    self.y_increment = -self.start_scale

  ## Displays coupling status notifiers for all navigations in COUPLED_NAVIGATION_LIST
  # @param COUPLED_NAVIGATION_LIST List of Navigation instances that are now coupled.
  def display_coupling(self, COUPLED_NAVIGATION_LIST):

    _loader = avango.gua.nodes.TriMeshLoader()

    # check for every user that could be updated
    for _nav in COUPLED_NAVIGATION_LIST:
      if _nav.platform != self:
            
        # check if desired plane is not already present
        _new_node_needed = True

        for _node in self.coupling_status_node.Children.value:
          if (_node.Name.value == ('coupl_notifier_' + str(self.PLATFORM.platform_id))):
            _new_node_needed = False
            break

        # if the desired plane is not yet present, create and draw it
        if _new_node_needed:
          _plane = _loader.create_geometry_from_file('coupl_notifier_' + str(self.PLATFORM.platform_id),
                                                     'data/objects/plane.obj',
                                                     'data/materials/' +_nav.trace_material + 'Shadeless.gmd',
                                                     avango.gua.LoaderFlags.LOAD_MATERIALS)
          _plane.GroupNames.value = ["p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]
          _plane.ShadowMode.value = avango.gua.ShadowMode.OFF
          self.NET_TRANS_NODE.distribute_object(_plane)
          self.coupling_status_node.Children.value.append(_plane)
      
      # update the offsets of the notifiers to have a proper display
      self.update_coupling_status_overview()

  ## Removes a platform indicator from the coupling display and shows a message to all other platforms.
  # @param NAVIGATION The Navigation instance to be removed from all couplings.
  # @param SHOW_NOTIFICATION Boolean saying if a notification should be displayed to all other platforms involved.
  def remove_from_coupling_display(self, NAVIGATION, SHOW_NOTIFICATION):

    _loader = avango.gua.nodes.TriMeshLoader()

    # if the platform has a notifier for being coupled with NAVIGATION, remove this node from the scenegraph
    for _node in self.coupling_status_node.Children.value:
      if (_node.Name.value == ('coupl_notifier_' + str(NAVIGATION.platform.platform_id))):
        self.coupling_status_node.Children.value.remove(_node)
        self.update_coupling_status_overview()
        
        if SHOW_NOTIFICATION:
          
          # display notification that a user was decoupled
          self.coupling_plane_node.GroupNames.value[0] = "display_group"
          self.coupling_plane_node.Material.value = "data/materials/DecouplingPlane.gmd"

          # display color of decoupled navigation
          self.decoupling_notifier.GroupNames.value[0] = "display_group"
          self.decoupling_notifier.Material.value = 'data/materials/' + NAVIGATION.trace_material + 'Shadeless.gmd'

          # add user to watchlist such that the notifications are removed again after a certain
          # amount of time
          self.start_time = time.time()

        break

  ## Creates a plane in front of the user used for displaying coupling messages.
  def create_coupling_plane(self):
    
    _loader = avango.gua.nodes.TriMeshLoader()

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
    self.coupling_plane_node.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.coupling_plane_node.Transform.value = avango.gua.make_scale_mat(0.6 * self.screen.Width.value, 0.1, 0.2 * self.screen.Height.value)

    self.coupling_plane_node.GroupNames.value = ["do_not_display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]

    self.message_plane_node.Children.value.append(self.coupling_plane_node)

    ## @var decoupling_notifier
    # Geometry node representing a plane showing the color of a navigation that was recently decoupled.
    # Actual material and visibility will be toggled by StatusManager.
    self.decoupling_notifier = _loader.create_geometry_from_file('decoupling_notifier',
                                                                 'data/objects/plane.obj',
                                                                 'data/materials/AvatarWhiteShadeless.gmd',
                                                                 avango.gua.LoaderFlags.LOAD_MATERIALS)
    self.decoupling_notifier.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.decoupling_notifier.Transform.value =  avango.gua.make_trans_mat(0.0, 0.0, -0.2 * self.screen.Height.value) * \
                                                avango.gua.make_scale_mat(self.screen.Height.value * 0.1, self.screen.Height.value * 0.1, self.screen.Height.value * 0.1)

    self.decoupling_notifier.GroupNames.value = ["do_not_display_group", "p" + str(self.PLATFORM.platform_id) + "_s" + str(self.screen_num) + "_slot" + str(self.slot_id)]

    self.message_plane_node.Children.value.append(self.decoupling_notifier)

  ## Correctly places and appends the message plane node in and to the scenegraph.
  def handle_message_plane_node(self):
    self.message_plane_node.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * \
                                              avango.gua.make_rot_mat(90, 1, 0, 0)
    # append to primary screen
    self.screen.Children.value.append(self.message_plane_node)

  ## Displays the coupling plane with the "Coupling" texture.
  def show_coupling_plane(self):

    # display coupling plane
    self.coupling_plane_node.Material.value = "data/materials/CouplingPlane.gmd"
    self.coupling_plane_node.GroupNames.value[0] = "display_group"

    # hide decoupling notifier if it isn't already
    self.decoupling_notifier.GroupNames.value[0] = "do_not_display_group"

  ## Hides the coupling plane.
  def hide_coupling_plane(self):
    self.coupling_plane_node.GroupNames.value[0] = "do_not_display_group"

  ## Evaluated every frame.
  def evaluate(self):

    # update matrices as given by assigned user
    if self.assigned_user != None:
      self.slot_node.Transform.value = self.assigned_user.matrices_per_platform[self.PLATFORM.platform_id]
      self.slot_scale_node.Transform.value = avango.gua.make_scale_mat(self.assigned_user.scales_per_platform[self.PLATFORM.platform_id])

      # trigger correct avatar visibilities
      if self.PLATFORM.avatar_type == "joseph":

        if len(self.PLATFORM.get_slots_of(self.assigned_user)) == 1:
          if 'do_not_display_group' in self.head_avatar.GroupNames.value:
            self.head_avatar.Transform.disconnect()
            self.head_avatar.Transform.disconnect()
            self.head_avatar.Transform.connect_from(self.assigned_user.headtracking_reader.sf_avatar_head_mat)
            self.body_avatar.Transform.connect_from(self.assigned_user.headtracking_reader.sf_avatar_body_mat)
            self.head_avatar.GroupNames.value.remove('do_not_display_group')
            self.body_avatar.GroupNames.value.remove('do_not_display_group')

      elif self.PLATFORM.avatar_type.endswith(".ks"):

        if self.assigned_user.use_group_navigation[self.PLATFORM.platform_id] == False:
          if len(self.PLATFORM.get_slots_of(self.assigned_user)) == 1 and \
            'do_not_display_group' in self.video_geode.GroupNames.value:

            self.video_geode.GroupNames.value.remove('do_not_display_group')

        else:
          if self.PLATFORM.video_avatar_visible() == False and \
             'do_not_display_group' in self.video_geode.GroupNames.value:

            self.video_geode.GroupNames.value.remove('do_not_display_group')

    # if a time update is required
    if self.start_time != None:
      
      # hide decoupling notifiers again after a certain amount of time
      if time.time() - self.start_time > 3.0:

        # hide message plane and reset its material
        self.coupling_plane_node.GroupNames.value[0] = "do_not_display_group"

        # hide decoupling notifier
        self.decoupling_notifier.GroupNames.value[0] = "do_not_display_group"

        self.start_time = None


## Internal representation of a display slot on a head mounted display. A Slot is one rendering output that can be handled
# by a display, for HMDs usually one per device.
class SlotHMD(Slot):

  ## Custom constructor.
  # @param DISPLAY Display instance for which this slot is being created.
  # @param SLOT_ID Identification number of the slot within the display.
  # @param SCREEN_NUM Number of the screen / display on the platform.
  # @param STEREO Boolean indicating if the slot to be created is a stereo one.
  # @param PLATFORM Platform instance to which the slot is to be appended to.
  def __init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM):
    Slot.__init__(self, DISPLAY, SLOT_ID, SCREEN_NUM, STEREO, PLATFORM)

    self.left_screen = avango.gua.nodes.ScreenNode(Name = "screenL")
    self.left_screen.Width.value = DISPLAY.size[0] / 2
    self.left_screen.Height.value = DISPLAY.size[1]
    self.left_screen.Transform.value = avango.gua.make_trans_mat(-0.04, 0.0, -0.05)
    self.slot_node.Children.value.append(self.left_screen)

    self.right_screen = avango.gua.nodes.ScreenNode(Name = "screenR")
    self.right_screen.Width.value = DISPLAY.size[0] / 2
    self.right_screen.Height.value = DISPLAY.size[1]
    self.right_screen.Transform.value = avango.gua.make_trans_mat(0.04, 0.0, -0.05)
    self.slot_node.Children.value.append(self.right_screen)

  ## Assigns a user to this slot. Therefore, the slot_node is connected with the user's headtracking matrix.
  # In the HMD case, the InputMapping's station matrix is overwritten.
  # @param USER_INSTANCE An instance of User which is to be assigned.
  def assign_user(self, USER_INSTANCE):
    Slot.assign_user(self, USER_INSTANCE)

    # connect station mat with headtracking matrix
    USER_INSTANCE.platform.INPUT_MAPPING_INSTANCE.DEVICE_INSTANCE.sf_station_mat.disconnect()
    USER_INSTANCE.platform.INPUT_MAPPING_INSTANCE.DEVICE_INSTANCE.sf_station_mat.connect_from(USER_INSTANCE.headtracking_reader.sf_abs_mat)