#!/usr/bin/python

## @file
# Contains class BoundingBoxVisualization.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import python libraries
import time

## Initializes a bounding box visualization of an object in the scene.
class BoundingBoxVisualization(avango.script.Script):

  # internal fields
  ## @var sf_node_mat
  # Matrix to represent the WorldTransform of the object to be handled.
  sf_node_mat = avango.gua.SFMatrix4()

  ## @var sf_enable_flag
  # Boolean field indicating if this bounding box visualization is activated.
  sf_enable_flag = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(BoundingBoxVisualization).__init__()

  ## Custom constructor.
  # @param OBJECT Reference to an InteractiveObject instance to be handled.
  # @param SCENEGRAPH Reference to the scenegraph in which the object is located.
  # @param NET_TRANS_NODE Active nettrans node to be used for distribution.
  # @param MATERIAL Material string to be used for the visualization.
  def my_constructor(self, OBJECT, SCENEGRAPH, NET_TRANS_NODE, MATERIAL):

    # references
    ## @var OBJECT
    # Reference to the InteractiveObject instance to be handled.
    self.OBJECT = OBJECT

    ## @var SCENEGRAPH
    # Reference to the scenegraph in which the handled object is located.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var bb_thickness
    # Thickness of the bounding box lines in meters.
    self.bb_thickness	= 0.01

    # variables
    ## @var lf_node_mat
    # Last frame matrix of the handled object to detect changes.
    self.lf_node_mat = avango.gua.make_identity_mat()

    ## @var bb
    # The bounding box to be visualized.
    self.bb = None

    # init nodes    
    _loader = avango.gua.nodes.TriMeshLoader()
            
    ## @var edge_group
    # Scenegraph transformation node to group all the bounding box edges.
    self.edge_group = avango.gua.nodes.TransformNode()
    NET_TRANS_NODE.Children.value.append(self.edge_group)
    
    ## @var edge1
    # Geometry node representing the first edge of the visualized bounding box.
    self.edge1 = _loader.create_geometry_from_file("edge1", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge1.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge1)

    ## @var edge2
    # Geometry node representing the second edge of the visualized bounding box.
    self.edge2 = _loader.create_geometry_from_file("edge2", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge2.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge2)

    ## @var edge3
    # Geometry node representing the third edge of the visualized bounding box.
    self.edge3 = _loader.create_geometry_from_file("edge3", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge3.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge3)

    ## @var edge4
    # Geometry node representing the fourth edge of the visualized bounding box.
    self.edge4 = _loader.create_geometry_from_file("edge4", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge4.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge4)

    ## @var edge5
    # Geometry node representing the fifth edge of the visualized bounding box.
    self.edge5 = _loader.create_geometry_from_file("edge5", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge5.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge5)

    ## @var edge6
    # Geometry node representing the sixth edge of the visualized bounding box.
    self.edge6 = _loader.create_geometry_from_file("edge6", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge6.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge6)
 
    ## @var edge7
    # Geometry node representing the seventh edge of the visualized bounding box.
    self.edge7 = _loader.create_geometry_from_file("edge7", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge7.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge7)

    ## @var edge8
    # Geometry node representing the eighth edge of the visualized bounding box.
    self.edge8 = _loader.create_geometry_from_file("edge8", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge8.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge8)

    ## @var edge9
    # Geometry node representing the nineth edge of the visualized bounding box.
    self.edge9 = _loader.create_geometry_from_file("edge9", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge9.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge9)

    ## @var edge10
    # Geometry node representing the tenth edge of the visualized bounding box.
    self.edge10 = _loader.create_geometry_from_file("edge10", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge10.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge10)

    ## @var edge11
    # Geometry node representing the eleventh edge of the visualized bounding box.
    self.edge11 = _loader.create_geometry_from_file("edge11", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge11.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge11)

    ## @var edge12
    # Geometry node representing the twelveth edge of the visualized bounding box.
    self.edge12 = _loader.create_geometry_from_file("edge12", "data/objects/cube.obj", MATERIAL, avango.gua.LoaderFlags.DEFAULTS)
    self.edge12.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.edge_group.Children.value.append(self.edge12)
    
    # init field connection
    self.sf_node_mat.connect_from(OBJECT.get_node().WorldTransform)
    self.sf_enable_flag.connect_from(OBJECT.sf_highlight_flag)
  
    self.edge_group.Transform.connect_from(self.sf_node_mat)
  
  

  # callbacks
  ## Called whenever sf_enable_flag changes.
  @field_has_changed(sf_enable_flag)
  def sf_enable_flag_changed(self):
    
    if self.sf_enable_flag.value == True: # set geometry visible
      self.edge1.GroupNames.value = []
      self.edge2.GroupNames.value = []      
      self.edge3.GroupNames.value = []
      self.edge4.GroupNames.value = []
      self.edge5.GroupNames.value = []
      self.edge6.GroupNames.value = []
      self.edge7.GroupNames.value = []
      self.edge8.GroupNames.value = []
      self.edge9.GroupNames.value = []
      self.edge10.GroupNames.value = []
      self.edge11.GroupNames.value = []
      self.edge12.GroupNames.value = []

    else: # set geometry invisible
      self.edge1.GroupNames.value = ["do_not_display_group"]
      self.edge2.GroupNames.value = ["do_not_display_group"]
      self.edge3.GroupNames.value = ["do_not_display_group"]
      self.edge4.GroupNames.value = ["do_not_display_group"]
      self.edge5.GroupNames.value = ["do_not_display_group"]
      self.edge6.GroupNames.value = ["do_not_display_group"]
      self.edge7.GroupNames.value = ["do_not_display_group"]  
      self.edge8.GroupNames.value = ["do_not_display_group"]
      self.edge9.GroupNames.value = ["do_not_display_group"]
      self.edge10.GroupNames.value = ["do_not_display_group"]
      self.edge11.GroupNames.value = ["do_not_display_group"]
      self.edge12.GroupNames.value = ["do_not_display_group"]
  
  
  ## Called whenever sf_node_mat changes.
  @field_has_changed(sf_node_mat)
  def sf_node_mat_changed(self):

    #print "object moved"
    _lf_scale = self.lf_node_mat.get_scale()
    _scale = self.sf_node_mat.value.get_scale()

    #if _lf_scale != _scale: # scale has changed
    #  self.update_bb_scale()
      
    self.lf_node_mat = self.sf_node_mat.value


  # functions
  ## Changes the material of the visualized bounding box.
  # @param MATERIAL The material string to be set and used.
  def set_material(self, MATERIAL):

    self.edge1.Material.value = MATERIAL
    self.edge2.Material.value = MATERIAL
    self.edge3.Material.value = MATERIAL
    self.edge4.Material.value = MATERIAL
    self.edge5.Material.value = MATERIAL
    self.edge6.Material.value = MATERIAL
    self.edge7.Material.value = MATERIAL
    self.edge8.Material.value = MATERIAL
    self.edge9.Material.value = MATERIAL
    self.edge10.Material.value = MATERIAL
    self.edge11.Material.value = MATERIAL
    self.edge12.Material.value = MATERIAL
      
  ## Calculates the bounding box of the current object.
  def calc_bb(self):

    self.SCENEGRAPH.update_cache()
  
    _node = self.OBJECT.get_node()

    self.bb = _node.BoundingBox.value
    #print _node.Name.value, len(_node.Children.value), self.bb.Min.value, self.bb.Max.value

    self.update_bb_scale()

  ## Computes and sets the correct transformations for the edges of the visualized bounding box.
  def update_bb_scale(self):
    
    if self.bb != None:

      _bb_min = avango.gua.make_inverse_mat(self.sf_node_mat.value) * self.bb.Min.value
      _bb_max = avango.gua.make_inverse_mat(self.sf_node_mat.value) * self.bb.Max.value

      _x_min	= _bb_min.x    
      _x_max	= _bb_max.x
      _dist_x	= _x_max - _x_min
      _center_x	= _x_min + _dist_x * 0.5

      _y_min	= _bb_min.y
      _y_max	= _bb_max.y
      _dist_y	= _y_max - _y_min
      _center_y	= _y_min + _dist_y * 0.5

      _z_min	= _bb_min.z
      _z_max	= _bb_max.z
      _dist_z	= _z_max - _z_min
      _center_z	= _z_min + _dist_z * 0.5


      _world_mat = self.OBJECT.get_world_transform()
      _scale = _world_mat.get_scale()

      # depth edges
      _scale_mat = avango.gua.make_scale_mat(self.bb_thickness/_scale.x, _dist_y + self.bb_thickness/_scale.y, self.bb_thickness/_scale.z)

      self.edge1.Transform.value = avango.gua.make_trans_mat(_x_min, _center_y, _z_min) * _scale_mat

      self.edge2.Transform.value = avango.gua.make_trans_mat(_x_max, _center_y, _z_min) * _scale_mat

      self.edge3.Transform.value = avango.gua.make_trans_mat(_x_min, _center_y, _z_max) * _scale_mat

      self.edge4.Transform.value = avango.gua.make_trans_mat(_x_max, _center_y, _z_max) * _scale_mat

      # width edges
      _scale_mat = avango.gua.make_scale_mat(_dist_x + self.bb_thickness/_scale.x, self.bb_thickness/_scale.y, self.bb_thickness/_scale.z)

      self.edge5.Transform.value = avango.gua.make_trans_mat(_center_x, _y_min, _z_min) * _scale_mat

      self.edge6.Transform.value = avango.gua.make_trans_mat(_center_x, _y_max, _z_min) * _scale_mat

      self.edge7.Transform.value = avango.gua.make_trans_mat(_center_x, _y_min, _z_max) * _scale_mat
      
      self.edge8.Transform.value = avango.gua.make_trans_mat(_center_x, _y_max, _z_max) * _scale_mat

      # height edges
      _scale_mat = avango.gua.make_scale_mat(self.bb_thickness/_scale.x, self.bb_thickness/_scale.y, _dist_z + self.bb_thickness/_scale.z)

      self.edge9.Transform.value = avango.gua.make_trans_mat(_x_min, _y_min, _center_z) * _scale_mat

      self.edge10.Transform.value = avango.gua.make_trans_mat(_x_min, _y_max, _center_z) * _scale_mat

      self.edge11.Transform.value = avango.gua.make_trans_mat(_x_max, _y_min, _center_z) * _scale_mat

      self.edge12.Transform.value = avango.gua.make_trans_mat(_x_max, _y_max, _center_z) * _scale_mat
