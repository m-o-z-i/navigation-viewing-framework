#!/usr/bin/python

## @file
# Contains class Video3D.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ApplicationManager import *
from ConsoleIO import *
from VisibilityHandler import *
from scene_config import scenegraphs

##
class Video3DRepresentation:

  ##
  #
  def __init__( self
              , VIDEO_3D_INSTANCE
              , NAME
              , PARENT_NODE
              , NAVIGATION_INSTANCE ):

    ##
    #
    self.VIDEO_3D_INSTANCE = VIDEO_3D_INSTANCE

    ##
    #
    self.NAVIGATION_INSTANCE = NAVIGATION_INSTANCE


    _loader = avango.gua.nodes.Video3DLoader()
    
    ##
    #
    self.video_node = _loader.load(NAME, self.VIDEO_3D_INSTANCE.filename)
    self.video_node.Transform.value = self.VIDEO_3D_INSTANCE.offset
    self.video_node.ShadowMode.value = avango.gua.ShadowMode.OFF

    PARENT_NODE.Children.value.append(self.video_node)

    # init trigger callback
    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

  ##
  #
  def set_group_names(self, LIST_OF_STRINGS):

    self.video_node.GroupNames.value = LIST_OF_STRINGS

  ##
  #
  def append_to_group_names(self, STRING):

    self.video_node.GroupNames.value.append(STRING)

  ##
  def frame_callback(self):

    self.video_node.Transform.value = self.NAVIGATION_INSTANCE.sf_nav_mat.value * \
                                      self.VIDEO_3D_INSTANCE.offset


###############################################################################################


## 
class Video3D(VisibilityHandler2D):

  ##
  def __init__(self):
    self.super(Video3D).__init__()

  ##
  def my_constructor(self, WORKSPACE_INSTANCE, FILENAME, OFFSET, VISIBILITY_TABLE, ALL_USER_REPRESENTATIONS):

    self.table_constructor(VISIBILITY_TABLE)

    ##
    #
    self.WORKSPACE_INSTANCE = WORKSPACE_INSTANCE

    ##
    #
    self.filename = FILENAME

    ##
    #
    self.offset = OFFSET

    ##
    #
    self.video_3D_representations = []

    ## @var ALL_USER_REPRESENTATIONS
    # Reference to ApplicationManager.all_user_representations as the import of it strangely fails in this class.
    self.ALL_USER_REPRESENTATIONS = ALL_USER_REPRESENTATIONS

  ## Changes the visibility table during runtime.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def change_visiblity_table(self, VISIBILITY_TABLE):

    self.visibility_table = VISIBILITY_TABLE

    for _display_group in self.WORKSPACE_INSTANCE.display_groups:
      for _navigation in _display_group.navigations:
        self.handle_correct_visibility_groups_for(_navigation)


  ##
  #
  def create_video_3D_representation_for(self, NAME, NAVIGATION_INSTANCE):

    _video_3D_repr = Video3DRepresentation( self
                                          , NAME
                                          , scenegraphs[0]["/net"]
                                          , NAVIGATION_INSTANCE)

    self.video_3D_representations.append(_video_3D_repr)

  ##
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

    # if the navigation is not used, hide the video representation
    if len(NAVIGATION_INSTANCE.active_user_representations) > 0:

      # loop over all user representations to find the ones for which the video is visible
      for _user_repr in self.ALL_USER_REPRESENTATIONS:

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
    


  