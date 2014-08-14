#!/usr/bin/python

## @file
# Contains classes UserRepresentation and User.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from Intersection import *
from TrackingReader import *
from ConsoleIO import *
import Tools

# import math libraries
import math

## A User instances has UserRepresentations for each display group of his workspace.
# It handles the selection of the display group's navigations.
class UserRepresentation(avango.script.Script):

  ## Default constructor.
  def __init__(self):
    self.super(UserRepresentation).__init__()

  ## Custom constructor.
  # @param USER Reference to the user to be represented.
  # @param DISPLAY_GROUP Reference to the display group this user representation is responsible for.
  # @param VIEW_TRANSFORM_NODE Transform node to be filled by one navigation of the display group.
  def my_constructor(self, USER, DISPLAY_GROUP, VIEW_TRANSFORM_NODE):

    ## @var USER
    # Reference to the user to be represented.
    self.USER = USER

    ## @var DISPLAY_GROUP
    # Reference to the display group this user representation is responsible for.
    self.DISPLAY_GROUP = DISPLAY_GROUP

    ## @var view_transform_node
    # Transform node to be filled by one navigation of the display group.
    self.view_transform_node = VIEW_TRANSFORM_NODE

    ## @var workspace_id
    # Identification number of the workspace the associated user is belonging to.
    self.workspace_id = int(VIEW_TRANSFORM_NODE.Name.value.split("_")[0].replace("w", ""))

    ## @var screens
    # List of screen nodes for each display of the display group.
    self.screens = []

    ## create user representation nodes ##

    _stereo_display_group = True

    for _display in DISPLAY_GROUP.displays:

      if _display.stereo == False:
        _stereo_display_group = False
        break

    if _stereo_display_group:
      _eye_distance = self.USER.eye_distance
    else:
      _eye_distance = 0.0

    ##
    #
    self.head = avango.gua.nodes.TransformNode(Name = "head")
    self.view_transform_node.Children.value.append(self.head)

    self.left_eye = avango.gua.nodes.TransformNode(Name = "eyeL")
    self.left_eye.Transform.value = avango.gua.make_trans_mat(-_eye_distance / 2, 0.0, 0.0)
    self.head.Children.value.append(self.left_eye)

    self.right_eye = avango.gua.nodes.TransformNode(Name = "eyeR")
    self.right_eye.Transform.value = avango.gua.make_trans_mat(_eye_distance / 2, 0.0, 0.0)
    self.head.Children.value.append(self.right_eye)

    ## @var connected_navigation_id
    # Navigation ID within the display group that is currently used.
    self.connected_navigation_id = -1

    # set evaluation policy
    self.always_evaluate(True)

  ## Evaluated every frame.
  def evaluate(self):
      
    # update head node with respect to workspace offset
    self.head.Transform.value = self.DISPLAY_GROUP.offset_to_workspace * \
                                self.USER.headtracking_reader.sf_abs_mat.value


    # update avatar body matrix if present at this view transform node
    _head_pos = self.head.Transform.value.get_translate()
    _forward_yaw = Tools.get_yaw(self.head.Transform.value)

    try:
      self.body_avatar
    except:
      return

    #print "update body"
    self.body_avatar.Transform.value = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(self.head.Transform.value.get_rotate())) * \
                                       avango.gua.make_trans_mat(0.0, -_head_pos.y / 2, 0.0) * \
                                       avango.gua.make_rot_mat(math.degrees(_forward_yaw) - 90, 0, 1, 0) * \
                                       avango.gua.make_scale_mat(0.45, _head_pos.y / 2, 0.45)

  ##
  #
  def add_screen_node_for(self, DISPLAY_INSTANCE):

    # create avatar representation when first screen is added
    if len(self.screens) == 0:
      self.create_joseph_avatar_representation()

    _screen = DISPLAY_INSTANCE.create_screen_node("screen_" + str(len(self.screens)))
    self.view_transform_node.Children.value.append(_screen)
    self.screens.append(_screen)

    _loader = avango.gua.nodes.TriMeshLoader()

    _navigation_color_geometry = _loader.create_geometry_from_file('nav_color_plane',
                                                                   'data/objects/plane.obj',
                                                                   'data/materials/' + self.DISPLAY_GROUP.navigations[0].trace_material + 'Shadeless.gmd',
                                                                    avango.gua.LoaderFlags.LOAD_MATERIALS)

    _trans = avango.gua.Vec3(-0.45 * _screen.Width.value, 0.4 * _screen.Height.value, 0.0)
    _scale = 0.05 * _screen.Height.value
    _navigation_color_geometry.Transform.value =  avango.gua.make_trans_mat(_trans) * \
                                                  avango.gua.make_rot_mat(90, 1, 0, 0) * \
                                                  avango.gua.make_scale_mat(_scale, _scale, _scale)
    _navigation_color_geometry.ShadowMode.value = avango.gua.ShadowMode.OFF
    #_navigation_color_geometry.GroupNames.value = ["w" + str(_w_id) + "_dg" + str(_dg_id) + "_s" + str(_s_id) + "_u" + str(_u_id)]
    _screen.Children.value.append(_navigation_color_geometry)


  ##
  # 
  #
  def create_joseph_avatar_representation(self):
    
    _loader = avango.gua.nodes.TriMeshLoader()
    
    # create avatar head
    ## @var head_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's head.
    self.head_avatar = _loader.create_geometry_from_file('head_avatar',
                                                         'data/objects/Joseph/JosephHead.obj',
                                                         'data/materials/ShadelessWhite.gmd',
                                                         avango.gua.LoaderFlags.LOAD_MATERIALS)

    self.head_avatar.Transform.value = avango.gua.make_rot_mat(-90, 0, 1, 0) * avango.gua.make_scale_mat(0.4, 0.4, 0.4)
    self.head_avatar.GroupNames.value = ['w' + str(self.workspace_id) + "_dg" + str(self.DISPLAY_GROUP.id) + "_u" + str(self.USER.id)]
    self.head.Children.value.append(self.head_avatar)

    # create avatar body
    ## @var body_avatar
    # Scenegraph node representing the geometry and transformation of the basic avatar's body.
    self.body_avatar = _loader.create_geometry_from_file('body_avatar',
                                                         'data/objects/Joseph/JosephBody.obj',
                                                         'data/materials/ShadelessWhite.gmd',
                                                         avango.gua.LoaderFlags.LOAD_MATERIALS)
    
    self.body_avatar.GroupNames.value = ['w' + str(self.workspace_id) + "_dg" + str(self.DISPLAY_GROUP.id) + "_u" + str(self.USER.id)]
    self.head.Children.value.append(self.body_avatar)


  ## Connects a specific navigation of the display group to the user.
  # @param ID The ID of the navigation to connect with.
  def connect_navigation_of_display_group(self, ID):

    # change is not necessary
    if ID == self.connected_navigation_id:
      print_message("User " + str(self.USER.id) + " at display group " + str(self.DISPLAY_GROUP.id) + \
                    ": Already on Navigaton " + str(ID)) 

    # change is necessary
    elif ID < len(self.DISPLAY_GROUP.navigations):

      _old_navigation = self.DISPLAY_GROUP.navigations[self.connected_navigation_id]
      _new_navigation = self.DISPLAY_GROUP.navigations[ID]

      if len(_new_navigation.active_user_representations) == 0 and self.connected_navigation_id != -1:

        try:
          _new_navigation.inputmapping.set_abs_mat(_old_navigation.sf_abs_mat.value)
          _new_navigation.inputmapping.set_scale(_old_navigation.sf_scale.value)
        except:
          pass

      _old_navigation.remove_user_representation(self)
      _new_navigation.add_user_representation(self)

      # connect all view transform nodes to this navigation
      self.view_transform_node.Transform.disconnect()
      self.view_transform_node.Transform.connect_from(_new_navigation.sf_nav_mat)

      self.connected_navigation_id = ID

      try:
        print_message("User " + str(self.USER.id) + " at display group " + str(self.DISPLAY_GROUP.id) + \
         ": Switch navigation to " + str(ID) + " (" + _new_navigation.input_device_name + ")")
      except:
        print_message("User " + str(self.USER.id) + " at display group " + str(self.DISPLAY_GROUP.id) + \
         ": Switch navigation to " + str(ID) + " (no input device)")

      # trigger avatar visibility
      if _new_navigation.avatar_type == 'joseph':
        self.head_avatar.Material.value = 'data/materials/' + _new_navigation.trace_material + ".gmd"
        self.body_avatar.Material.value = 'data/materials/' + _new_navigation.trace_material + ".gmd"
        self.head_avatar.GroupNames.value.remove("do_not_display_group")
        self.body_avatar.GroupNames.value.remove("do_not_display_group")
      else:
        self.head_avatar.GroupNames.value.append("do_not_display_group")
        self.body_avatar.GroupNames.value.append("do_not_display_group")

    else:
      print_error("Error. Navigation ID does not exist.", False)

  ##
  #
  def disable_avatars(self):
    self.head_avatar.GroupNames.value.append("do_not_display_group")
    self.body_avatar.GroupNames.value.append("do_not_display_group")

## Logical representation of a user within a Workspace. Stores the relevant parameters
# and cares for receiving the headtracking input.
class User(avango.script.Script):

  ## Default constructor.
  def __init__(self):
    self.super(User).__init__()

  ## Custom constructor.
  # @param WORKSPACE_INSTANCE Workspace instance in which this user is active.
  # @param USER_ID Global user ID to be applied.
  # @param VIP Boolean indicating if the user to be created is a vip.
  # @param GLASSES_ID ID of the shutter glasses worn by the user.
  # @param HEADTRACKING_TARGET_NAME Name of the headtracking station as registered in daemon.
  # @param EYE_DISTANCE The eye distance of the user to be applied.
  # @param NO_TRACKING_MAT Matrix to be applied when HEADTRACKING_TARGET_NAME is None.
  def my_constructor(self
                   , WORKSPACE_INSTANCE
                   , USER_ID
                   , VIP
                   , GLASSES_ID
                   , HEADTRACKING_TARGET_NAME
                   , EYE_DISTANCE
                   , NO_TRACKING_MAT
                   ):

    # flags 
    ## @var is_vip
    # Boolean indicating if this user has vip status.
    self.is_vip = VIP

    ## @var is_active
    # Boolean indicating if this user is currently active.
    self.is_active = True

    ## @var eye_distance
    # The eye distance of the user to be applied.
    self.eye_distance = EYE_DISTANCE

    # variables
    ## @var WORKSPACE_INSTANCE
    # Workspace instance at which this user is registered.
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ## @var id
    # Identification number of the user within the workspace, starting from 0.
    self.id = USER_ID

    ## @var headtracking_target_name
    # Name of the headtracking station as registered in daemon.
    self.headtracking_target_name = HEADTRACKING_TARGET_NAME

    ## @var headtracking_reader
    # TrackingTargetReader for the user's glasses.
    if self.headtracking_target_name == None:
      self.headtracking_reader = TrackingDefaultReader()
      self.headtracking_reader.set_no_tracking_matrix(NO_TRACKING_MAT)
    else:
      self.headtracking_reader = TrackingTargetReader()
      self.headtracking_reader.my_constructor(HEADTRACKING_TARGET_NAME)
      self.headtracking_reader.set_transmitter_offset(self.WORKSPACE_INSTANCE.transmitter_offset)
      self.headtracking_reader.set_receiver_offset(avango.gua.make_identity_mat())

    ## @var glasses_id
    # ID of the shutter glasses worn by the user. Used for frequency updates.
    self.glasses_id = GLASSES_ID

    ## @var user_representations
    # List of UserRepresentation instances for all display groups in the user's workspace.
    self.user_representations = []

    # toggles activity
    self.toggle_user_activity(self.is_active)

    # set evaluation policy
    self.always_evaluate(True)

  ## Creates a UserRepresentation instance for a given display group.
  # @param DISPLAY_GROUP Reference to the DisplayGroup instance to create the user representation for.
  # @param VIEW_TRANSFORM_NODE Transform node to be filled by one navigation of the display group.
  def create_user_representation_for(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE):

    _user_repr = UserRepresentation()
    _user_repr.my_constructor(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE)
    self.user_representations.append(_user_repr)
    return _user_repr

  ## Switches the navigation for a display group that is stored at the corresponding node in 
  # matrices_per_display_group.
  # @param DISPLAY_GROUP_ID Identification number of the display group to switch the navigation for.
  # @param NAVIGATION_ID Identification number of the navigation to be used within the display group.
  def switch_navigation_at_display_group(self, DISPLAY_GROUP_ID, NAVIGATION_ID):
    
    if DISPLAY_GROUP_ID < len(self.user_representations):
      self.user_representations[DISPLAY_GROUP_ID].connect_navigation_of_display_group(NAVIGATION_ID)
    else:
      print_error("Error. Display Group ID does not exist.", False)

  ## Evaluated every frame.
  def evaluate(self):
    pass
    
  ## Sets the user's active flag.
  # @param ACTIVE Boolean to which the active flag should be set.
  def toggle_user_activity(self, ACTIVE):

    if ACTIVE:
      self.is_active = True
    else:
      self.is_active = False