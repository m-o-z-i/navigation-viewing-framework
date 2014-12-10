#!/usr/bin/python

## @file
# Contains classes RayPointerRepresentation and RayPointer.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
from Tool import *
import Utilities
from TrackingReader import TrackingTargetReader
from scene_config import *
from SceneManager import *


## Geometric representation of a RayPointer in a DisplayGroup.
class RayPointerRepresentation(ToolRepresentation):

  ## Default constructor.
  def __init__(self):
    self.super(RayPointerRepresentation).__init__()

    ## @var intersection_sphere_size
    # Radius of the intersection sphere in meters.
    self.intersection_sphere_size = 0.05

  ## Custom constructor.
  # @param RAY_POINTER_INSTANCE An instance of RayPointer to which this RayPointerRepresentation is associated.
  # @param DISPLAY_GROUP DisplayGroup instance for which this RayPointerRepresentation is responsible for. 
  # @param USER_REPRESENTATION Corresponding UserRepresentation instance under which's view_transform_node the RayPointerRepresentation is appended.
  def my_constructor(self, RAY_POINTER_INSTANCE, DISPLAY_GROUP, USER_REPRESENTATION):
    
    # call base class constructor
    self.base_constructor(RAY_POINTER_INSTANCE
                        , DISPLAY_GROUP
                        , USER_REPRESENTATION
                        , "pick_ray_" + str(RAY_POINTER_INSTANCE.id))

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var ray_geometry
    # Geometry node representing the ray graphically.
    self.ray_geometry = _loader.create_geometry_from_file( "ray_geometry"
                                                         , "data/objects/cylinder.obj"
                                                         , "data/materials/White.gmd"
                                                         , avango.gua.LoaderFlags.DEFAULTS)
    self.ray_geometry.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value)
    self.set_ray_distance(self.TOOL_INSTANCE.ray_length)
    self.tool_transform_node.Children.value.append(self.ray_geometry)

    ## @var intersection_point_geometry
    # Geometry node representing the intersection point of the ray if any.
    self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry"
                                                                       , "data/objects/sphere.obj"
                                                                       , "data/materials/White.gmd"
                                                                       , avango.gua.LoaderFlags.DEFAULTS)
    self.intersection_point_geometry.GroupNames.value.append("do_not_display_group")
    self.intersection_point_geometry.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value)
    self.tool_transform_node.Children.value.append(self.intersection_point_geometry)

    ## @var ray_start_geometry
    # Geometry node representing the origin of the ray graphically.
    self.ray_start_geometry = _loader.create_geometry_from_file("ray_start_geometry"
                                                               , "data/objects/cube.obj"
                                                               , "data/materials/White.gmd"
                                                               , avango.gua.LoaderFlags.DEFAULTS)
    self.ray_start_geometry.Transform.value = avango.gua.make_scale_mat(0.015, 0.015, 0.015)
    self.ray_start_geometry.GroupNames.value.append(self.USER_REPRESENTATION.view_transform_node.Name.value) 
    self.tool_transform_node.Children.value.append(self.ray_start_geometry)

    ## @var highlighted
    # Boolean indicating if this representation is highlighted. Usually used to color the assigned user's representation.
    self.highlighted = False


  ## Sets ray_geometry to a specific length.
  # @param NEW_RAY_DISTANCE The new distance of the ray to be set.
  def set_ray_distance(self, NEW_RAY_DISTANCE):

    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, NEW_RAY_DISTANCE * -0.5) * \
                                        avango.gua.make_rot_mat(-90.0, 1, 0, 0) * \
                                        avango.gua.make_scale_mat(self.TOOL_INSTANCE.ray_thickness, NEW_RAY_DISTANCE, self.TOOL_INSTANCE.ray_thickness)

  ## Shows the intersection geometry at a specific matrix in this coordinate system and sets the ray distance accordingly.
  # @param MATRIX The position matrix to be set for the intersection geometry.
  # @param NEW_RAY_DISTANCE The new distance of the ray to be set.
  def show_intersection_geometry_at(self, MATRIX, NEW_RAY_DISTANCE):

    self.intersection_point_geometry.GroupNames.value.remove("do_not_display_group")
    self.intersection_point_geometry.Transform.value = MATRIX * avango.gua.make_scale_mat(self.intersection_sphere_size)
    self.set_ray_distance(NEW_RAY_DISTANCE)

  ## Hides the intersection geometry and resets the ray distance.
  def hide_intersection_geometry(self):
    self.intersection_point_geometry.GroupNames.value.append("do_not_display_group")
    self.set_ray_distance(self.TOOL_INSTANCE.ray_length)

  ## Hides the ray geometry.
  def hide_ray(self):
    self.ray_geometry.GroupNames.value.append("do_not_display_group")

  ## Appends a string to the GroupNames field of this RayPointerRepresentation's visualization.
  # @param STRING The string to be appended.
  def append_to_visualization_group_names(self, STRING):
    self.ray_geometry.GroupNames.value.append(STRING)
    self.intersection_point_geometry.GroupNames.value.append(STRING)
    self.ray_start_geometry.GroupNames.value.append(STRING)

  ## Removes a string from the GroupNames field of this RayPointerRepresentation's visualization.
  # @param STRING The string to be removed.
  def remove_from_visualization_group_names(self, STRING):
    self.ray_geometry.GroupNames.value.remove(STRING)
    self.intersection_point_geometry.GroupNames.value.remove(STRING)
    self.ray_start_geometry.GroupNames.value.remove(STRING)

  ## Resets the GroupNames field of this RayPointerRepresentation's visualization to the user representation's view_transform_node.
  def reset_visualization_group_names(self):
    self.ray_geometry.GroupNames.value = [self.USER_REPRESENTATION.view_transform_node.Name.value]
    self.intersection_point_geometry.GroupNames.value = [self.USER_REPRESENTATION.view_transform_node.Name.value]
    self.ray_start_geometry.GroupNames.value = [self.USER_REPRESENTATION.view_transform_node.Name.value]

  ## Enables a highlight for this RayPointerRepresentation.
  def enable_highlight(self):
  
    self.highlighted = True

  ## Disables the highlight for this RayPointerRepresentation.
  def disable_highlight(self):

    self.highlighted = False

  ## Sets a different matrial for the ray's start geometry to visualize the selection level.
  # @param MATERIAL The material string to be set.
  def set_ray_start_geometry_material(self, MATERIAL):

    self.ray_start_geometry.Material.value = MATERIAL

  ## Evaluated every frame.
  def evaluate(self):

    # base class evaluate
    self.perform_tool_node_transformation()

    # update border color according to highlight enabled
    
    if self.highlighted:
      if self.ray_geometry.Material.value != "data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd":
        self.ray_geometry.Material.value = "data/materials/" + self.USER_REPRESENTATION.DISPLAY_GROUP.navigations[self.USER_REPRESENTATION.connected_navigation_id].trace_material + "Shadeless.gmd"
    else:
      if self.ray_geometry.Material.value != "data/materials/White.gmd":
        self.ray_geometry.Material.value = "data/materials/White.gmd"


###############################################################################################

## Logical representation of a RayPointer in a Workspace.
class RayPointer(Tool):

  # internal fields
  ## @var sf_pointer_button0
  # Boolean field representing the first button of the pointer.
  sf_pointer_button0 = avango.SFBool()

  ## @var sf_pointer_button1
  # Boolean field representing the second button of the pointer.
  sf_pointer_button1 = avango.SFBool()

  ## @var sf_pointer_button2
  # Boolean field representing the third button of the pointer.
  sf_pointer_button2 = avango.SFBool()  

  ## @var mf_pointer_pick_result
  # Intersections of the picking ray with the objects in the scene.
  mf_pointer_pick_result = avango.gua.MFPickResult()

  ## Default constructor.
  def __init__(self):
    self.super(RayPointer).__init__()

  ## Custom constructor.
  # @param WORKSPACE_INSTANCE The instance of Workspace to which this Tool belongs to.
  # @param TOOL_ID The identification number of this Tool within the workspace.
  # @param POINTER_TRACKING_STATION The tracking target name of this RayPointer.
  # @param POINTER_DEVICE_STATION The device station name of this RayPointer. 
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def my_constructor(self, WORKSPACE_INSTANCE, TOOL_ID, POINTER_TRACKING_STATION, POINTER_DEVICE_STATION, VISIBILITY_TABLE):

    # call base class constructor
    self.base_constructor(WORKSPACE_INSTANCE, TOOL_ID, POINTER_TRACKING_STATION, VISIBILITY_TABLE)

    # parameters
    ## @var ray_length
    # Length of the pointer's ray in meters.
    self.ray_length = 10.0

    ## @var ray_thickness
    # Thickness of the pointer's ray in meters.
    self.ray_thickness = 0.01

    ## @var hierarchy_selection_level
    # Hierarchy level which is selected by this pointer.
    self.hierarchy_selection_level = 0

    # variables

    ## @var highlighted_object
    # Reference to the currently highlighted object.
    self.highlighted_object = None

    ## @var dragged_interactive_object
    # Reference to the currently dragged object.
    self.dragged_interactive_object = None

    ## @var dragging_tool_representation
    # ToolRepresentation instance from which dragging was initiated.
    self.dragging_tool_representation = None

    ## @var dragging_offset
    # Offset to be applied during the dragging process.
    self.dragging_offset = None
    
    ## @var device_sensor
    # Device sensor capturing the pointer's button input values.
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = POINTER_DEVICE_STATION
    
    # init field connections
    self.sf_pointer_button0.connect_from(self.device_sensor.Button0)
    self.sf_pointer_button1.connect_from(self.device_sensor.Button1)
    self.sf_pointer_button2.connect_from(self.device_sensor.Button2)

  ## Creates a RayPointerRepresentation for this RayPointer at a DISPLAY_GROUP.
  # @param DISPLAY_GROUP The DisplayGroup instance to create the representation for.
  # @param USER_REPRESENTATION The UserRepresentation this representation will belong to.
  def create_tool_representation_for(self, DISPLAY_GROUP, USER_REPRESENTATION):

    _ray_pointer_repr = RayPointerRepresentation()
    _ray_pointer_repr.my_constructor(self, DISPLAY_GROUP, USER_REPRESENTATION)
    self.tool_representations.append(_ray_pointer_repr)
    return _ray_pointer_repr

  ## Computes the pick result of a matrix with the scene.
  # @param MATRIX The matrix to shoot the pick ray from.
  def compute_pick_result(self, MATRIX):

    _ray = avango.gua.nodes.RayNode()
    _ray.Transform.value = MATRIX * avango.gua.make_scale_mat(1.0, 1.0, self.ray_length)

    _picking_options = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                     | avango.gua.PickingOptions.GET_WORLD_POSITIONS \
                     | avango.gua.PickingOptions.GET_WORLD_NORMALS

    _picking_mask = "man_pick_group"

    _pick_result = scenegraphs[0].ray_test(_ray, _picking_options, _picking_mask)
    return _pick_result

  ## Selects a list of potentially currently active RayPointerRepresentations by computing picks for them.
  def create_candidate_list(self):
    
    _candidate_list = []

    # only go on if a user is assigned to the ray
    if self.assigned_user != None:

      # iterate over all tool representations of assigned user
      for _tool_repr in self.tool_representations:

        if _tool_repr.user_id == self.assigned_user.id:
        
          # compute pick result for current tool representation

          _world_transform = _tool_repr.get_world_transform()
          _mf_pick_result = self.compute_pick_result(_world_transform)

          # if a pick was found
          if len(_mf_pick_result.value) > 0:

            _pick_result = _mf_pick_result.value[0]
            _pick_world_position = _pick_result.Object.value.WorldTransform.value * _pick_result.Position.value
            _pick_world_position = avango.gua.Vec3(_pick_world_position.x, _pick_world_position.y, _pick_world_position.z)
            
            # is pick in frustum of user?
            _user_repr = self.assigned_user.get_user_representation_at(_tool_repr.DISPLAY_GROUP.id)
            _pick_visible = False

            _user_head_mat = _user_repr.head.WorldTransform.value
            _user_nav_mat = _user_repr.view_transform_node.Transform.value

            # pick is visible when visible in one of the display group's screens
            for _screen in _user_repr.screens:

              if self.is_inside_frustum(_pick_world_position
                                      , _user_head_mat
                                      , _user_nav_mat
                                      , _screen) == True:
                _pick_visible = True
                break

            # append to candidate list if visible
            if _pick_visible:

              _tool_world_transform = _tool_repr.tool_transform_node.WorldTransform.value

              _intersection_in_nav_space = avango.gua.make_inverse_mat(_tool_world_transform) * \
                                           (avango.gua.make_trans_mat(_pick_world_position) * \
                                           avango.gua.make_scale_mat(_user_nav_mat.get_scale() * -1))

              _candidate_list.append( (_pick_result, _tool_repr, _intersection_in_nav_space) )

    return _candidate_list


  ## Chooses one RayPointerRepresentation among the potentially active ones in a candidate list.
  # @param CANDIDATE_LIST The list of candidates to be checked.
  def choose_from_candidate_list(self, CANDIDATE_LIST):
    
    _closest_index = -1
    _closest_distance = 1000

    for _i in range(len(CANDIDATE_LIST)):
      
      _pick_result = CANDIDATE_LIST[_i][0]

      # check for pick result with closest distance
      if _pick_result.Distance.value < _closest_distance:
        _closest_distance = _pick_result.Distance.value
        _closest_index = _i 

    if _closest_index != -1:
      return CANDIDATE_LIST[_closest_index]
    else:
      return None


  ## Create candidate list and select one of the candidates.
  def get_pick_result_tuple(self):

    _candidate_representations = self.create_candidate_list()
    _chosen_pick_result_tuple = self.choose_from_candidate_list(_candidate_representations)
    return _chosen_pick_result_tuple

  ## Evaluated every frame.
  def evaluate(self):

    if self.dragged_interactive_object == None:
      
      # update user assignment
      self.check_for_user_assignment()

      # compute active pick result
      _pick_result_tuple = self.get_pick_result_tuple()

      # a pick was found and selected
      if _pick_result_tuple != None:
        
        _pick_result = _pick_result_tuple[0]
        _hit_repr = _pick_result_tuple[1]
        _intersection_in_nav_space = _pick_result_tuple[2]

        _hit_display_group = _hit_repr.DISPLAY_GROUP

        # iterate over all tool representations
        for _repr in self.tool_representations:
        
          # hide intersection point when not at hit display group
          # or when user does not share the assigned user's navigation
          if _repr.DISPLAY_GROUP != _hit_display_group or \
             _repr.USER_REPRESENTATION.connected_navigation_id != self.assigned_user.user_representations[_hit_display_group.id].connected_navigation_id :

            _repr.hide_intersection_geometry()
            _repr.set_ray_distance(_pick_result.Distance.value * self.ray_length)

          # otherwise show the intersection geometry
          else:
            _repr.show_intersection_geometry_at(_intersection_in_nav_space, _pick_result.Distance.value * self.ray_length)

      # no pick was found
      else:
        
        for _repr in self.tool_representations:
          _repr.hide_intersection_geometry()

      #self.update_object_highlight(_pick_result)

    # an object is dragged
    else:

      self.drag_object()


  ## Function called on a framewise basis when dragging is in progress.
  def drag_object(self):

    _mat = self.dragging_tool_representation.get_world_transform() * self.dragging_offset
    self.dragged_interactive_object.set_world_transform(_mat)


  ## Change the hierarchy selection level to a given level.
  # @param HIERARCHY_LEVEL The new hierarchy selection level to be set.
  def set_hierarchy_selection_level(self, HIERARCHY_LEVEL):

    self.hierarchy_selection_level = HIERARCHY_LEVEL
    
    print("hierarchy selection level", self.hierarchy_selection_level)
    
    if self.hierarchy_selection_level >= 0:
      _material = SceneManager.hierarchy_materials[HIERARCHY_LEVEL]
     
      for _ray_pointer_repr in self.tool_representations:

        if _ray_pointer_repr.USER_REPRESENTATION.USER == self.assigned_user:
          _ray_pointer_repr.set_ray_start_geometry_material(_material)

    else:

      for _ray_pointer_repr in self.tool_representations:
        
        if _ray_pointer_repr.USER_REPRESENTATION.USER == self.assigned_user:
          _ray_pointer_repr.set_ray_start_geometry_material("data/materials/White.gmd")


  ## Updates the object to be highlighted according to a pick result found.
  # @param PICK_RESULT The PickResult for which the object should be highlighted.
  def update_object_highlight(self, PICK_RESULT):
  
    if PICK_RESULT != None: # intersection found     
      
      _node = PICK_RESULT.Object.value
      
      if _node.has_field("InteractiveObject") == True:
        _object = _node.InteractiveObject.value
        #print _object
        
        if self.hierarchy_selection_level >= 0:          
          _object = _object.get_higher_hierarchical_object(self.hierarchy_selection_level)
        
        if _object == None:
          # evtl. disable highlight of prior object
          if self.highlighted_object != None:
            self.highlighted_object.enable_highlight(False)

        else:
          if _object != self.highlighted_object: # new object hit
          
            # evtl. disable highlight of prior object
            if self.highlighted_object != None:
              self.highlighted_object.enable_highlight(False)

            self.highlighted_object = _object
              
            # enable highlight of new object
            self.highlighted_object.enable_highlight(True)
 
    else: # no intersection found
    
      # evtl. disable highlight of prior object
      if self.highlighted_object != None:
        self.highlighted_object.enable_highlight(False)

        self.highlighted_object = None

  ## Called whenever sf_pointer_button0 changes.
  @field_has_changed(sf_pointer_button0)
  def sf_pointer_button0_changed(self):

    # button was pressed
    if self.sf_pointer_button0.value == True:
      
      # compute active pick result
      _pick_result_tuple = self.get_pick_result_tuple()

      # a pick was found and selected
      if _pick_result_tuple != None:
      
        _pick_result = _pick_result_tuple[0]
        _hit_tool_repr = _pick_result_tuple[1]

        _hit_node = _pick_result.Object.value

        # retrieve InteractiveObject instance
        if _hit_node.has_field("InteractiveObject"):

          _object = _hit_node.InteractiveObject.value
          self.dragged_interactive_object = _object
          self.dragging_tool_representation = _hit_tool_repr
          self.dragging_offset = avango.gua.make_inverse_mat(self.dragging_tool_representation.get_world_transform()) * self.dragged_interactive_object.get_world_transform()


    # button was released
    else:

      # stop dragging
      if self.dragged_interactive_object != None:
        self.dragged_interactive_object = None
        self.dragging_tool_representation = None
        self.dragging_offset = None


  ## Called whenever sf_pointer_button1 changes.
  @field_has_changed(sf_pointer_button1)
  def sf_pointer_button1_changed(self):

    if self.sf_pointer_button1.value == True:
      self.set_hierarchy_selection_level(min(self.hierarchy_selection_level + 1, 3))
      
  ## Called whenever sf_pointer_button2 changes.
  @field_has_changed(sf_pointer_button2)
  def sf_pointer_button2_changed(self):

    if self.sf_pointer_button2.value == True:
      self.set_hierarchy_selection_level(max(self.hierarchy_selection_level - 1, -1))

  ## Checks if a point is inside the viewing frustum of a user.
  # @param POINT The point to be checked.
  # @param USER_HEAD_WORLD_MAT The user's headtracking matrix in world coordinates.
  # @param USER_NAV_WORLD_MAT The user's navigation matrix in world coordinates.
  # @param SCREEN The screen to create the viewing frustum for. 
  def is_inside_frustum(self, POINT, USER_HEAD_WORLD_MAT, USER_NAV_WORLD_MAT, SCREEN):
    
    _near_clip = SceneManager.current_near_clip
    _far_clip = SceneManager.current_far_clip

    # compute screen corner points
    _screen_mat = SCREEN.WorldTransform.value
    _screen_width = SCREEN.Width.value
    _screen_height = SCREEN.Height.value
    
    _tl_pos = _screen_mat * avango.gua.Vec3(-_screen_width * 0.5, _screen_height * 0.5, 0.0)
    _tr_pos = _screen_mat * avango.gua.Vec3(_screen_width * 0.5, _screen_height * 0.5, 0.0)
    _bl_pos = _screen_mat * avango.gua.Vec3(-_screen_width * 0.5, -_screen_height * 0.5, 0.0)
    _br_pos = _screen_mat * avango.gua.Vec3(_screen_width * 0.5, -_screen_height * 0.5, 0.0)

    _tl_pos = avango.gua.Vec3(_tl_pos.x, _tl_pos.y, _tl_pos.z)
    _tr_pos = avango.gua.Vec3(_tr_pos.x, _tr_pos.y, _tr_pos.z)    
    _bl_pos = avango.gua.Vec3(_bl_pos.x, _bl_pos.y, _bl_pos.z)
    _br_pos = avango.gua.Vec3(_br_pos.x, _br_pos.y, _br_pos.z)

    # transform head matrix and corner points in screen coordinate system
    _head_abs_mat = avango.gua.make_trans_mat(USER_HEAD_WORLD_MAT.get_translate()) * \
                    avango.gua.make_rot_mat(USER_NAV_WORLD_MAT.get_rotate_scale_corrected()) * \
                    avango.gua.make_rot_mat(SCREEN.Transform.value.get_rotate())
    _inv_head_abs_mat = avango.gua.make_inverse_mat(_head_abs_mat)

    _tl_pos_in_head_space = _inv_head_abs_mat * _tl_pos    
    _tr_pos_in_head_space = _inv_head_abs_mat * _tr_pos
    _bl_pos_in_head_space = _inv_head_abs_mat * _bl_pos
    _br_pos_in_head_space = _inv_head_abs_mat * _br_pos

    _tl_pos_in_head_space = avango.gua.Vec3(_tl_pos_in_head_space.x, _tl_pos_in_head_space.y, _tl_pos_in_head_space.z)
    _tr_pos_in_head_space = avango.gua.Vec3(_tr_pos_in_head_space.x, _tr_pos_in_head_space.y, _tr_pos_in_head_space.z)
    _bl_pos_in_head_space = avango.gua.Vec3(_bl_pos_in_head_space.x, _bl_pos_in_head_space.y, _bl_pos_in_head_space.z)
    _br_pos_in_head_space = avango.gua.Vec3(_br_pos_in_head_space.x, _br_pos_in_head_space.y, _br_pos_in_head_space.z)

    _head_to_screen_distance = abs(_tl_pos_in_head_space.z)

    # compute scaling factors for corner vectors
    if _head_to_screen_distance == 0.0:
      _head_to_screen_distance = 0.001

    _tl_near_plane_scale_factor = (_tl_pos_in_head_space.length() * _near_clip) / _head_to_screen_distance
    _tr_near_plane_scale_factor = (_tr_pos_in_head_space.length() * _near_clip) / _head_to_screen_distance
    _bl_near_plane_scale_factor = (_bl_pos_in_head_space.length() * _near_clip) / _head_to_screen_distance
    _br_near_plane_scale_factor = (_br_pos_in_head_space.length() * _near_clip) / _head_to_screen_distance
    
    _tl_far_plane_scale_factor = (_tl_pos_in_head_space.length() * _far_clip) / _head_to_screen_distance
    _tr_far_plane_scale_factor = (_tr_pos_in_head_space.length() * _far_clip) / _head_to_screen_distance
    _bl_far_plane_scale_factor = (_bl_pos_in_head_space.length() * _far_clip) / _head_to_screen_distance
    _br_far_plane_scale_factor = (_br_pos_in_head_space.length() * _far_clip) / _head_to_screen_distance 
    
    _tl_pos_in_head_space.normalize()
    _tr_pos_in_head_space.normalize()
    _bl_pos_in_head_space.normalize()
    _br_pos_in_head_space.normalize()

    # compute near clip points
    _tl_near_pos_in_head_space = _tl_pos_in_head_space * _tl_near_plane_scale_factor
    _tr_near_pos_in_head_space = _tr_pos_in_head_space * _tr_near_plane_scale_factor
    _bl_near_pos_in_head_space = _bl_pos_in_head_space * _bl_near_plane_scale_factor
    _br_near_pos_in_head_space = _br_pos_in_head_space * _br_near_plane_scale_factor

    _tl_near_world_pos = _head_abs_mat * _tl_near_pos_in_head_space
    _tr_near_world_pos = _head_abs_mat * _tr_near_pos_in_head_space
    _bl_near_world_pos = _head_abs_mat * _bl_near_pos_in_head_space
    _br_near_world_pos = _head_abs_mat * _br_near_pos_in_head_space

    _tl_near_world_pos = avango.gua.Vec3(_tl_near_world_pos.x, _tl_near_world_pos.y, _tl_near_world_pos.z)
    _tr_near_world_pos = avango.gua.Vec3(_tr_near_world_pos.x, _tr_near_world_pos.y, _tr_near_world_pos.z)
    _bl_near_world_pos = avango.gua.Vec3(_bl_near_world_pos.x, _bl_near_world_pos.y, _bl_near_world_pos.z)
    _br_near_world_pos = avango.gua.Vec3(_br_near_world_pos.x, _br_near_world_pos.y, _br_near_world_pos.z)

    # compute far clip points
    _tl_far_pos_in_head_space = _tl_pos_in_head_space * _tl_far_plane_scale_factor
    _tr_far_pos_in_head_space = _tr_pos_in_head_space * _tr_far_plane_scale_factor
    _bl_far_pos_in_head_space = _bl_pos_in_head_space * _bl_far_plane_scale_factor
    _br_far_pos_in_head_space = _br_pos_in_head_space * _br_far_plane_scale_factor

    _tl_far_world_pos = _head_abs_mat * _tl_far_pos_in_head_space
    _tr_far_world_pos = _head_abs_mat * _tr_far_pos_in_head_space
    _bl_far_world_pos = _head_abs_mat * _bl_far_pos_in_head_space
    _br_far_world_pos = _head_abs_mat * _br_far_pos_in_head_space

    _tl_far_world_pos = avango.gua.Vec3(_tl_far_world_pos.x, _tl_far_world_pos.y, _tl_far_world_pos.z)
    _tr_far_world_pos = avango.gua.Vec3(_tr_far_world_pos.x, _tr_far_world_pos.y, _tr_far_world_pos.z)
    _bl_far_world_pos = avango.gua.Vec3(_bl_far_world_pos.x, _bl_far_world_pos.y, _bl_far_world_pos.z)
    _br_far_world_pos = avango.gua.Vec3(_br_far_world_pos.x, _br_far_world_pos.y, _br_far_world_pos.z)

    ## compute planes ##
    _frustum_planes = []

    # near plane
    _v1 = _bl_near_world_pos - _br_near_world_pos
    _v2 = _tl_near_world_pos - _bl_near_world_pos
    _n = _v1.cross(_v2)
    _n.normalize()
    _d = - _n.dot(_br_near_world_pos)
    _near_plane = (_n, _d)
    _frustum_planes.append(_near_plane)

    # far plane
    _v1 = _br_far_world_pos - _bl_far_world_pos
    _v2 = _tr_far_world_pos - _br_far_world_pos
    _n = _v1.cross(_v2)
    _n.normalize()
    _d = - _n.dot(_bl_far_world_pos)
    _far_plane = (_n, _d)
    _frustum_planes.append(_far_plane)

    # left plane
    _v1 = _bl_far_world_pos - _bl_near_world_pos
    _v2 = _tl_far_world_pos - _bl_far_world_pos
    _n = _v1.cross(_v2)
    _n.normalize()
    _d = - _n.dot(_bl_near_world_pos)
    _left_plane = (_n, _d)
    _frustum_planes.append(_left_plane)

    # right plane
    _v1 = _br_near_world_pos - _br_far_world_pos
    _v2 = _tr_near_world_pos - _br_near_world_pos
    _n = _v1.cross(_v2)
    _n.normalize()
    _d = - _n.dot(_br_far_world_pos)
    _right_plane = (_n, _d)
    _frustum_planes.append(_right_plane)

    # top plane
    _v1 = _tr_near_world_pos - _tr_far_world_pos
    _v2 = _tl_near_world_pos - _tr_near_world_pos
    _n = _v1.cross(_v2)
    _n.normalize()
    _d = - _n.dot(_tr_far_world_pos)
    _top_plane = (_n, _d)
    _frustum_planes.append(_top_plane)

    # bottom plane
    _v1 = _bl_near_world_pos - _bl_far_world_pos
    _v2 = _br_near_world_pos - _bl_near_world_pos
    _n = _v1.cross(_v2)
    _n.normalize()
    _d = - _n.dot(_bl_far_world_pos)
    _bottom_plane = (_n, _d)
    _frustum_planes.append(_bottom_plane)

    # determine realtion to planes (in front, behind)
    for _plane in _frustum_planes:

      _n = _plane[0]
      _d = _plane[1]

      if (_n.x * POINT.x + _n.y * POINT.y + _n.z * POINT.z + _d) < 0:
        return False

    return True
