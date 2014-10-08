#!/usr/bin/python


# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
from Intersection import *
from UIGeoFeature import *

class Ray(avango.script.Script):

  mf_pointer_pick_result = avango.gua.MFPickResult()
  sf_ray_transform = avango.gua.SFMatrix4()
  

  def __init__(self):
    self.super(Ray).__init__()

    
  def my_constructor(self, ID, SCENEGRAPH, NET_TRANS_NODE, PARENT_NODE, SF_MATRIX, LENGTH, RAY_THICKNESS):
    self.id = ID
    self.scenegraph = SCENEGRAPH
    self.net_trans_node = NET_TRANS_NODE
    self.parent_node = PARENT_NODE  
    self.default_length = LENGTH
    self.ray_thickness = 0.005
    self.intersection_sphere_size = 0.025

    self.active = True

    self.ray_transform = avango.gua.nodes.TransformNode(Name = "ray_transform")
    PARENT_NODE.Children.value.append(self.ray_transform)

    _mat = avango.gua.make_trans_mat(0.0,0.0,self.default_length * -0.5) * \
                                            avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                            avango.gua.make_scale_mat(self.ray_thickness,self.default_length,self.ray_thickness)

    self.edge = UIEdge("data/objects/cylinder.obj", _mat, "data/materials/White.gmd", NET_TRANS_NODE, self.ray_transform, True, 0.1, avango.gua.Vec3(), avango.gua.Vec3())
    self.ray_geometry = self.edge.get_geometry()

    _loader = avango.gua.nodes.TriMeshLoader()
    self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry", "data/objects/sphere.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
    NET_TRANS_NODE.Children.value.append(self.intersection_point_geometry)
    self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible

    

    #self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.default_length * -0.5) * \
    #                                        avango.gua.make_rot_mat(-90.0,1,0,0) * \
    #                                        avango.gua.make_scale_mat(0.005,self.default_length,0.005)

    # init sub classes
    ## @var pointer_intersection
    # Instance of Intersection to determine hit points of the ray with the scene.
    self.pointer_intersection = Intersection() # ray intersection for target identification
    self.pointer_intersection.my_constructor(SCENEGRAPH, self.ray_transform.WorldTransform, self.default_length, "man_pick_group") # parameters: SCENEGRAPH, SF_PICK_MATRIX, PICK_LENGTH, PICKMASK
    
    # init field connections
    self.ray_transform.Transform.connect_from(SF_MATRIX)
    self.sf_ray_transform.connect_from(SF_MATRIX)
    self.mf_pointer_pick_result.connect_from(self.pointer_intersection.mf_pick_result)

  def set_default_length(self, LENGTH):
    self.default_length = LENGTH

  def set_length(self, LENGTH):
    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,LENGTH * -0.5) * \
                                          avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                          avango.gua.make_scale_mat(self.ray_thickness, LENGTH, self.ray_thickness)

  def adjust_length(self, POINT, OBJECT):
    # intersection point in object coordinate system
    _point = OBJECT.WorldTransform.value * POINT # transform point into world coordinates
    _point = avango.gua.Vec3(_point.x,_point.y,_point.z) # make Vec3 from Vec4

    _distance = (_point - self.ray_transform.WorldTransform.value.get_translate()).length()
    
    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,_distance * -0.5) * \
                                          avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                          avango.gua.make_scale_mat(self.ray_thickness, _distance, self.ray_thickness)

    self.intersection_point_geometry.Transform.value = avango.gua.make_trans_mat(_point) * \
                                                          avango.gua.make_scale_mat(self.intersection_sphere_size, self.intersection_sphere_size, self.intersection_sphere_size)
    self.intersection_point_geometry.GroupNames.value = []

  # callbacks
  ## Called whenever mf_pointer_pick_result changes.
  @field_has_changed(mf_pointer_pick_result)
  def mf_pointer_pick_result_changed(self):
    if len(self.mf_pointer_pick_result.value) > 0: # intersection found    
      _pick_result = self.mf_pointer_pick_result.value[0] # get first intersection target
      _point = _pick_result.Position.value # intersection point in object coordinate system
      _node = _pick_result.Object.value
      
      self.adjust_length(_point, _node)

    else:
      self.set_length(self.default_length)
      self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"]

  @field_has_changed(sf_ray_transform)
  def sf_ray_transform_changed(self):
    self.point1 = self.sf_ray_transform.value.get_translate()
    self.intersection_point_geometry.GroupNames.value = []
    #self.point2 = self.point1 * avango.gua.make_trans_mat(0.0,0.0,self.default_length * -0.5) * \
    #                                        avango.gua.make_rot_mat(-90.0,1,0,0) * self.sf_ray_transform.value.get_rotate()

    
    
