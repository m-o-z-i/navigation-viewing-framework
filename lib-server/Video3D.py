#!/usr/bin/python

## @file
# Contains class Video3D.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ConsoleIO import *
from VisibilityHandler import *
from scene_config import scenegraphs

## Geometric representation of a Video3D object in a Navigation.
class Video3DRepresentation:

  ## Custom constructor.
  # @param VIDEO_3D_INSTANCE An instance of Video3D to which this Video3DRepresentation is associated.
  # @param NAME Name to be used for the instantiated video node.
  # @param PARENT_NODE Scenegraph node to which the video node should be attached.
  # @param NAVIGATION_INSTANCE Instance to a subclass of Navigation to which this Video3DRepresentation is associated.
  def __init__( self
              , VIDEO_3D_INSTANCE
              , NAME
              , PARENT_NODE
              , NAVIGATION_INSTANCE ):

    ## @var VIDEO_3D_INSTANCE
    # An instance of Video3D to which this Video3DRepresentation is associated.
    self.VIDEO_3D_INSTANCE = VIDEO_3D_INSTANCE

    ## @var NAVIGATION_INSTANCE
    # Instance to a subclass of Navigation to which this Video3DRepresentation is associated.
    self.NAVIGATION_INSTANCE = NAVIGATION_INSTANCE

    # create video loader
    _loader = avango.gua.nodes.Video3DLoader()
    
    ## @var video_node
    # Scenegraph node containing the video geometry information of this representation.
    self.video_node = _loader.load(NAME, self.VIDEO_3D_INSTANCE.filename)
    self.video_node.Transform.value = self.VIDEO_3D_INSTANCE.offset
    self.video_node.ShadowMode.value = avango.gua.ShadowMode.OFF

    PARENT_NODE.Children.value.append(self.video_node)

    # init trigger callback
    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

  ## Sets a list of strings at the GroupNames field of the video node.
  # @param LIST_OF_STRINGS The list of group names to be set.
  def set_group_names(self, LIST_OF_STRINGS):

    self.video_node.GroupNames.value = LIST_OF_STRINGS

  ## Appends a string to the GroupNames field of the video node.
  # @param STRING The string to be appended.
  def append_to_group_names(self, STRING):

    self.video_node.GroupNames.value.append(STRING)

  ## Callback: evaluated every frame
  def frame_callback(self):

    self.video_node.Transform.value = self.NAVIGATION_INSTANCE.sf_nav_mat.value * \
                                      self.VIDEO_3D_INSTANCE.offset


###############################################################################################


## Logical representation of a 3D video stream of a Workspace.
class Video3D(VisibilityHandler2D):

  ## Default constructor.
  def __init__(self):
    self.super(Video3D).__init__()

    # import ApplicationManager as it strangely does not work at the top of this file
    exec('from ApplicationManager import *', globals())

  ## Custom constructor.
  # @param WORKSPACE_INSTANCE The instance of Workspace to which this Tool belongs to.
  # @param FILENAME The path of the file containing the video stream.
  # @param OFFSET The offset to be stored at the representations' video nodes.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags.
  def my_constructor(self, WORKSPACE_INSTANCE, FILENAME, OFFSET, VISIBILITY_TABLE):

    self.table_constructor(VISIBILITY_TABLE)

    ## @var WORKSPACE_INSTANCE
    # The instance of Workspace to which this Tool belongs to.
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ## @var filename
    # The path of the file containing the video stream.
    self.filename = FILENAME

    ## @var offset
    # The offset to be stored at the representations' video nodes.
    self.offset = OFFSET

    ## @var video_3D_representations
    # List of Video3DRepresentation instances belonging to this Video3D.
    self.video_3D_representations = []


  ## Changes the visibility table during runtime.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def change_visiblity_table(self, VISIBILITY_TABLE):

    self.visibility_table = VISIBILITY_TABLE

    for _display_group in self.WORKSPACE_INSTANCE.display_groups:
      for _navigation in _display_group.navigations:
        self.handle_correct_visibility_groups_for(_navigation)

  ## Creates a Video3DRepresentation for this Video3D at a NAVIGATION_INSTANCE.
  # @param NAME Name to be used for the instantiated video node.
  # @param NAVIGATION_INSTANCE Instance to a subclass of Navigation to which the new Video3DRepresentation is associated.
  def create_video_3D_representation_for(self, NAME, NAVIGATION_INSTANCE):

    _video_3D_repr = Video3DRepresentation( self
                                          , NAME
                                          , scenegraphs[0]["/net"]
                                          , NAVIGATION_INSTANCE)

    self.video_3D_representations.append(_video_3D_repr)

  ## Handles the correct GroupNames of the Video3DRepresentation at a specific Navigation.
  # @param NAVIGATION_INSTANCE The Navigation instance to get the Video3DRepresentation from.
  def handle_correct_visibility_groups_for(self, NAVIGATION_INSTANCE):

    # get the corresponding video representation
    _video_representation_at_navigation = None

    for _video_repr in self.video_3D_representations:
      if _video_repr.NAVIGATION_INSTANCE == NAVIGATION_INSTANCE:
        _video_representation_at_navigation = _video_repr
        break

    # get the navigation's display group
    _nav_display_group = None

    for _display_group in self.WORKSPACE_INSTANCE.display_groups:
      if NAVIGATION_INSTANCE in _display_group.navigations:
        _nav_display_group = _display_group
        break

    ## determine which group names have to be added to the video representation ##
    _video_visible_for = []

    # if the navigation is not used, hide the video representation, also when avatar mode is not set to video
    if len(NAVIGATION_INSTANCE.active_user_representations) > 0 and ApplicationManager.current_avatar_mode == "VIDEO":

      # loop over all user representations to find the ones for which the video is visible
      for _user_repr in ApplicationManager.all_user_representations:

        # video is only visible for users not on the corresponding navigation to avoid physical overlap
        if _user_repr.DISPLAY_GROUP.navigations[_user_repr.connected_navigation_id] != NAVIGATION_INSTANCE:

          _nav_display_group_tag = _nav_display_group.visibility_tag
          _user_repr_display_group_tag = _user_repr.DISPLAY_GROUP.visibility_tag

          # if tags are identical, show video due to different navigations (see above)
          if _nav_display_group_tag == _user_repr_display_group_tag:
            _visible = True
          else:
            try:
              _visible = self.visibility_table[_user_repr_display_group_tag][_nav_display_group_tag]
            except:
              _visible = False


          if _visible:
            if _user_repr.view_transform_node.Name.value == "scene_matrix":
              _video_visible_for.append(_user_repr.view_transform_node.Parent.value.Name.value + "_" + _user_repr.head.Name.value)
            else:
              _video_visible_for.append(_user_repr.view_transform_node.Name.value)


    # apply the obtained group names to the video representation
    if len(_video_visible_for) == 0:

      # prevent wildcard from rendering the avatar
      _video_representation_at_navigation.set_group_names(["do_not_display_group"])

    else:

      for _string in _video_visible_for:
        _video_representation_at_navigation.set_group_names(_video_visible_for)