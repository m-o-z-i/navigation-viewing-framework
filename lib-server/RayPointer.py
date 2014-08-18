#!/usr/bin/python

## @file
# Contains class RayPointer.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
from Tool import *
import Tools
from TrackingReader import TrackingTargetReader
from scene_config import *
from SceneManager import *

##
class RayPointerRepresentation(ToolRepresentation):

  ##
  def __init__(self):
    self.super(RayPointerRepresentation).__init__()

  ##
  def my_constructor(self, RAY_POINTER_INSTANCE, DISPLAY_GROUP, VIEW_TRANSFORM_NODE):
    
    self.base_constructor(RAY_POINTER_INSTANCE
                                    , DISPLAY_GROUP
                                    , VIEW_TRANSFORM_NODE
                                    , "pick_ray_" + str(RAY_POINTER_INSTANCE.id)
                                    , "self.tool_transform_node.Transform.value = self.DISPLAY_GROUP.offset_to_workspace * self.TOOL_INSTANCE.tracking_reader.sf_abs_mat.value")

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var ray_geometry
    # Geometry node representing the ray graphically.
    self.ray_geometry = _loader.create_geometry_from_file( "ray_geometry"
                                                         , "data/objects/cylinder.obj"
                                                         , "data/materials/White.gmd"
                                                         , avango.gua.LoaderFlags.DEFAULTS)
    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, self.TOOL_INSTANCE.ray_length * -0.5) * \
                                        avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                        avango.gua.make_scale_mat(0.005, self.TOOL_INSTANCE.ray_length, 0.005)
    self.tool_transform_node.Children.value.append(self.ray_geometry)

    self.always_evaluate(True)


##
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
  # @param MANIPULATION_MANAGER Reference to the ManipulationManager instance to which this RayPointer is associated.
  def my_constructor(self, WORKSPACE_INSTANCE, TOOL_ID, POINTER_TRACKING_STATION, POINTER_DEVICE_STATION):

    self.base_constructor(WORKSPACE_INSTANCE, TOOL_ID, POINTER_TRACKING_STATION)

    # parameters
    ## @var ray_length
    # Length of the pointer's ray in meters.
    self.ray_length = 10.0

    ## @var ray_thickness
    # Thickness of the pointer's ray in meters.
    self.ray_thickness = 0.0075

    ## @var intersection_sphere_size
    # Radius of the intersection sphere in meters.
    self.intersection_sphere_size = 0.5

    ## @var hierarchy_selection_level
    # Hierarchy level which is selected by this pointer.
    self.hierarchy_selection_level = 0

    # variables

    ## @var highlighted_object
    # Reference to the currently highlighted object.
    self.highlighted_object = None

    ## @var dragged_object
    # Reference to the currently dragged object.
    self.dragged_object = None

    ## @var dragging_offset
    # Offset to be applied during the dragging process.
    self.dragging_offset = None

    ##
    #'''
    _loader = avango.gua.nodes.TriMeshLoader()

    self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry"
                                                                       , "data/objects/sphere.obj"
                                                                       , "data/materials/White.gmd"
                                                                       , avango.gua.LoaderFlags.DEFAULTS)
    self.intersection_point_geometry.GroupNames.value.append("do_not_display_group")
    scenegraphs[0]["/net"].Children.value.append(self.intersection_point_geometry)
    '''

    ####
    self.tl_near_geometry = _loader.create_geometry_from_file("tl_near_geometry"
                                                                       , "data/objects/sphere.obj"
                                                                       , "data/materials/White.gmd"
                                                                       , avango.gua.LoaderFlags.DEFAULTS)
    scenegraphs[0]["/net"].Children.value.append(self.tl_near_geometry)

    self.tr_near_geometry = _loader.create_geometry_from_file("tr_near_geometry"
                                                                       , "data/objects/sphere.obj"
                                                                       , "data/materials/White.gmd"
                                                                       , avango.gua.LoaderFlags.DEFAULTS)
    scenegraphs[0]["/net"].Children.value.append(self.tr_near_geometry)

    self.bl_near_geometry = _loader.create_geometry_from_file("bl_near_geometry"
                                                                       , "data/objects/sphere.obj"
                                                                       , "data/materials/White.gmd"
                                                                       , avango.gua.LoaderFlags.DEFAULTS)
    scenegraphs[0]["/net"].Children.value.append(self.bl_near_geometry)

    self.br_near_geometry = _loader.create_geometry_from_file("br_near_geometry"
                                                                       , "data/objects/sphere.obj"
                                                                       , "data/materials/White.gmd"
                                                                       , avango.gua.LoaderFlags.DEFAULTS)
    scenegraphs[0]["/net"].Children.value.append(self.br_near_geometry)
    '''


    ####
    
    ## @var pointer_device_sensor
    # Device sensor capturing the pointer's button input values.
    self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.device_sensor.Station.value = POINTER_DEVICE_STATION
    
    # init field connections
    self.sf_pointer_button0.connect_from(self.device_sensor.Button0)
    self.sf_pointer_button1.connect_from(self.device_sensor.Button1)
    self.sf_pointer_button2.connect_from(self.device_sensor.Button2)

  ##
  #
  def create_ray_pointer_representation_for(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE):

    _ray_pointer_repr = RayPointerRepresentation()
    _ray_pointer_repr.my_constructor(self, DISPLAY_GROUP, VIEW_TRANSFORM_NODE)
    self.tool_representations.append(_ray_pointer_repr)
    return _ray_pointer_repr

  ##
  #
  def compute_pick_result(self, MATRIX):

    _ray = avango.gua.nodes.RayNode()
    _ray.Transform.value = MATRIX * avango.gua.make_scale_mat(1.0, 1.0, self.ray_length)

    _picking_options = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                     | avango.gua.PickingOptions.GET_POSITIONS \
                     | avango.gua.PickingOptions.GET_WORLD_POSITIONS \
                     | avango.gua.PickingOptions.GET_WORLD_NORMALS

    _picking_mask = "man_pick_group"

    _pick_result = scenegraphs[0].ray_test(_ray, _picking_options, _picking_mask)
    return _pick_result

  ##
  #
  def create_candidate_list(self):
    
    _candidate_list = []

    if self.assigned_user != None:

      for _tool_repr in self.tool_representations:

        if _tool_repr.user_id == self.assigned_user.id:
        
          #print "At ToolRepresentation of display group", _tool_repr.DISPLAY_GROUP.id

          _world_transform = _tool_repr.get_world_transform()
          _pick_result = self.compute_pick_result(_world_transform)

          if len(_pick_result.value) > 0:
            
            # is pick in frustum of user?
            _user_repr = self.assigned_user.get_user_representation_at(_tool_repr.DISPLAY_GROUP.id)
            _pick_visible = False

            _user_head_mat = _user_repr.head.WorldTransform.value
            _user_nav_mat = _user_repr.view_transform_node.WorldTransform.value

            for _screen in _user_repr.screens:

              if self.is_inside_frustum(_pick_result.value[0].WorldPosition.value
                                      , _user_head_mat
                                      , _user_nav_mat
                                      , _tool_repr.DISPLAY_GROUP
                                      , _screen) == True:
                _pick_visible = True
                break


            if _pick_visible:
              _candidate_list.append(_pick_result.value[0])

    return _candidate_list

  ##
  #
  def is_inside_frustum(self, POINT, USER_HEAD_WORLD_MAT, USER_NAV_WORLD_MAT, DISPLAY_GROUP, SCREEN):
    
    _near_clip = 0.1
    _far_clip = 1000.0

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

    # sdfsd

    _head_abs_mat = avango.gua.make_trans_mat(USER_HEAD_WORLD_MAT.get_translate()) * \
                    avango.gua.make_rot_mat(USER_NAV_WORLD_MAT.get_rotate_scale_corrected()) * \
                    avango.gua.make_rot_mat(SCREEN.Transform.value.get_rotate())
    _inv_head_abs_mat = avango.gua.make_inverse_mat(_head_abs_mat)


    _tl_pos_in_head_space = _inv_head_abs_mat * _tl_pos    
    _tr_pos_in_head_space = _inv_head_abs_mat * _tr_pos
    _bl_pos_in_head_space = _inv_head_abs_mat * _bl_pos
    _br_pos_in_head_space = _inv_head_abs_mat * _br_pos

    #print "!!!", _head_abs_mat
    #print _tl_pos, _tl_pos_in_head_space

    _tl_pos_in_head_space = avango.gua.Vec3(_tl_pos_in_head_space.x, _tl_pos_in_head_space.y, _tl_pos_in_head_space.z)
    _tr_pos_in_head_space = avango.gua.Vec3(_tr_pos_in_head_space.x, _tr_pos_in_head_space.y, _tr_pos_in_head_space.z)
    _bl_pos_in_head_space = avango.gua.Vec3(_bl_pos_in_head_space.x, _bl_pos_in_head_space.y, _bl_pos_in_head_space.z)
    _br_pos_in_head_space = avango.gua.Vec3(_br_pos_in_head_space.x, _br_pos_in_head_space.y, _br_pos_in_head_space.z)

    _head_to_screen_distance = abs(_tl_pos_in_head_space.z)

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

    # determine realtion to planes
    for _plane in _frustum_planes:

      _n = _plane[0]
      _d = _plane[1]

      if (_n.x * POINT.x + _n.y * POINT.y + _n.z * POINT.z + _d) < 0:
        return False

    return True


  ##
  #
  def choose_from_candidate_list(self, CANDIDATE_LIST):
    
    _closest_index = -1
    _closest_distance = 1000

    for _i in range(len(CANDIDATE_LIST)):
      
      _pick_result = CANDIDATE_LIST[_i]

      if _pick_result.Distance.value < _closest_distance:
        _closest_distance = _pick_result.Distance.value
        _closest_index = _i 

    if _closest_index != -1:
      return CANDIDATE_LIST[_closest_index]
    else:
      return None

  ##
  #
  def get_pick_result(self):

    _candidate_representations = self.create_candidate_list()
    _chosen_pick_result = self.choose_from_candidate_list(_candidate_representations)
    return _chosen_pick_result


  ##
  #
  def evaluate(self):

    self.check_for_user_assignment()

    _pick_result = self.get_pick_result()

    if _pick_result != None:
      
      _point = _pick_result.Position.value # intersection point in object coordinate system
      _node = _pick_result.Object.value
      _point = _node.WorldTransform.value * _point # transform point into world coordinates
      _point = avango.gua.Vec3(_point.x,_point.y,_point.z) # make Vec3 from Vec4
      self.intersection_point_geometry.Transform.value = avango.gua.make_trans_mat(_point) * \
                                                         avango.gua.make_scale_mat(self.intersection_sphere_size, self.intersection_sphere_size, self.intersection_sphere_size)
      self.intersection_point_geometry.GroupNames.value.remove("do_not_display_group")

    else:

      self.intersection_point_geometry.GroupNames.value.append("do_not_display_group")

    #self.update_object_highlight(_pick_result)

  ## Change the hierarchy selection level to a given level.
  # @param HIERARCHY_LEVEL The new hierarchy selection level to be set.
  def set_hierarchy_selection_level(self, HIERARCHY_LEVEL):

    self.hierarchy_selection_level = HIERARCHY_LEVEL
    
    print "hierarchy selection level", self.hierarchy_selection_level
    
    if self.hierarchy_selection_level >= 0:
      _material = SceneManager.hierarchy_materials[HIERARCHY_LEVEL]
     
      for _ray_pointer_repr in self.tool_representations:
        _ray_pointer_repr.ray_geometry.Material.value = _material
      
      self.intersection_point_geometry.Material.value = _material

    else:

      for _ray_pointer_repr in self.tool_representations:
        _ray_pointer_repr.ray_geometry.Material.value = "data/materials/White.gmd"
      
      self.intersection_point_geometry.Material.value = "data/materials/White.gmd"

  ##
  #
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

    if self.sf_pointer_button0.value == True:
      
      _pick_result = self.get_pick_result()

      if _pick_result != None:
        pass

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