#!/usr/bin/python

## @file
# Contains classes ManipulationManager and RayPointer.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import framework libraries
from Intersection import *

from TUIO import *

## Class to handle manipulations with a set of RayPointer instances.
class ManipulationManager:

  ## Default constructor.
  # @param NET_TRANS_NODE Reference to the nettrans node to which the scene is appended to.
  # @param SCENEGRAPH Reference to the scenegraph in which the manipulation is taking place.
  # @param SCENE_MANAGER Reference to the SceneManager instance which is used.
  def __init__(self, NET_TRANS_NODE, SCENEGRAPH, SCENE_MANAGER):
  
    # references
    ## @var SCENE_MANAGER
    # Reference to the SceneManager instance which is used.
    self.SCENE_MANAGER = SCENE_MANAGER
  
    # init first ray
    _parent_node = SCENEGRAPH["/net/platform_0/scale"]
    #_transmitter_offset = avango.gua.make_trans_mat(0.0, 0.043, 1.6)
    _transmitter_offset = avango.gua.make_trans_mat(0.0, 1.2, 0.0)
  
    ## @var ray_pointer1
    # First instance of RayPointer to create manipulations.
    self.ray_pointer1 = RayPointer()
    self.ray_pointer1.my_constructor(self, 1, SCENEGRAPH, NET_TRANS_NODE, _parent_node, _transmitter_offset, "tracking-dlp-pointer1", "device-pointer1")
    self.ray_pointer1.pointer_tracking_sensor.TransmitterOffset.value = avango.gua.make_trans_mat(0.1,1.2,1.6)

    self.tuio_cursor = TUIOManager()


  ## Returns the material string belonging to this object's hierarchy level.
  # @param INDEX The index for which the hierarchy material is to be retrieved.
  def get_hierarchy_material(self, INDEX):
  
    return self.SCENE_MANAGER.get_hierarchy_material(INDEX)


## Internal representation of a ray-based pointing device.
class RayPointer(avango.script.Script):

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
  # @param ID Identification number of the RayPointer, starting from 1.
  # @param SCENEGRAPH Reference to the scenegraph in which the manipulation is taking place.
  # @param NET_TRANS_NODE Reference to the nettrans node to which the scene is appended to.
  # @param PARENT_NODE Scenegraph node to which the ray is to be appended to.
  # @param TRACKING_TRANSMITTER_OFFSET Transmitter offset of the tracking system to be applied.
  # @param POINTER_TRACKING_STATION Tracking target name of the pointing device.
  # @param POINTER_DEVICE_STATION Input values name of the pointing device.
  def my_constructor(self, MANIPULATION_MANAGER, ID, SCENEGRAPH, NET_TRANS_NODE, PARENT_NODE, TRACKING_TRANSMITTER_OFFSET, POINTER_TRACKING_STATION, POINTER_DEVICE_STATION):
    #return
    print "in manipulation my_constructor"
    # references
    ## @var MANIPULATION_MANAGER
    # Reference to the ManipulationManager instance to which this RayPointer is associated.
    self.MANIPULATION_MANAGER = MANIPULATION_MANAGER
    
    # parameters
    ## @var ray_length
    # Length of the pointer's ray in meters.
    self.ray_length = 1000.0

    ## @var ray_thickness
    # Thickness of the pointer's ray in meters.
    self.ray_thickness = 0.0075

    ## @var intersection_sphere_size
    # Radius of the intersection sphere in meters.
    self.intersection_sphere_size = 0.025

    ## @var hierarchy_selection_level
    # Hierarchy level which is selected by this pointer.
    self.hierarchy_selection_level = 0

    # variables
    ## @var id
    # Identification number of the RayPointer, starting from 1.
    self.id = ID

    ## @var highlighted_object
    # Reference to the currently highlighted object.
    self.highlighted_object = None

    ## @var dragged_object
    # Reference to the currently dragged object.
    self.dragged_object = None

    ## @var dragging_offset
    # Offset to be applied during the dragging process.
    self.dragging_offset = None

    # init sensors
    ## @var pointer_tracking_sensor
    # Device sensor capturing the pointer's tracking position and rotation.
    self.pointer_tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.pointer_tracking_sensor.Station.value = POINTER_TRACKING_STATION
    self.pointer_tracking_sensor.ReceiverOffset.value = avango.gua.make_identity_mat()
    self.pointer_tracking_sensor.TransmitterOffset.value = TRACKING_TRANSMITTER_OFFSET
    
    ## @var pointer_device_sensor
    # Device sensor capturing the pointer's button input values.
    self.pointer_device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.pointer_device_sensor.Station.value = POINTER_DEVICE_STATION

    # init scenegraph node
    ## @var ray_transform
    # Transformation node of the pointer's ray.
    self.ray_transform = avango.gua.nodes.TransformNode(Name = "ray_transform")
    PARENT_NODE.Children.value.append(self.ray_transform)

    _loader = avango.gua.nodes.TriMeshLoader()
    
    ## @var ray_geometry
    # Geometry node representing the ray graphically.
    self.ray_geometry = _loader.create_geometry_from_file("ray_geometry", "data/objects/cylinder.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
    self.ray_transform.Children.value.append(self.ray_geometry)
    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                                            avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                            avango.gua.make_scale_mat(0.005,self.ray_length,0.005)
  
    ## @var intersection_point_geometry
    # Geometry node representing the intersection point of the ray with an object in the scene.
    self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry", "data/objects/sphere.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
    NET_TRANS_NODE.Children.value.append(self.intersection_point_geometry)
    self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible

    ## @var dragging_trigger
    # Trigger function which is called when a dragging process is in progress.
    self.dragging_trigger = avango.script.nodes.Update(Callback = self.dragging_callback, Active = False)
      
    # init sub classes
    ## @var pointer_intersection
    # Instance of Intersection to determine hit points of the ray with the scene.
    self.pointer_intersection = Intersection() # ray intersection for target identification
    self.pointer_intersection.my_constructor(SCENEGRAPH, self.ray_transform.WorldTransform, self.ray_length, "man_pick_group") # parameters: SCENEGRAPH, SF_PICK_MATRIX, PICK_LENGTH, PICKMASK
    
    # init field connections
    self.ray_transform.Transform.connect_from(self.pointer_tracking_sensor.Matrix)
    self.mf_pointer_pick_result.connect_from(self.pointer_intersection.mf_pick_result)
    self.sf_pointer_button0.connect_from(self.pointer_device_sensor.Button0)
    self.sf_pointer_button1.connect_from(self.pointer_device_sensor.Button1)
    self.sf_pointer_button2.connect_from(self.pointer_device_sensor.Button2)

    self.set_hierarchy_selection_level(-1)
    
    
  # callbacks
  ## Called whenever mf_pointer_pick_result changes.
  @field_has_changed(mf_pointer_pick_result)
  def mf_pointer_pick_result_mat_changed(self):
    print len(self.mf_pointer_pick_result.value)

    self.update_ray()
    self.update_object_highlight()
    
  ## Called whenever sf_pointer_button0 changes.
  @field_has_changed(sf_pointer_button0)
  def sf_pointer_button0_changed(self):

    if self.sf_pointer_button0.value == True and self.highlighted_object != None: # dragging started

      self.dragged_object = self.highlighted_object
      
      self.dragging_offset = avango.gua.make_inverse_mat(self.ray_transform.WorldTransform.value) * self.dragged_object.get_world_transform()

      self.dragging_trigger.Active.value = True # activate dragging callback

    elif self.sf_pointer_button0.value == False and self.dragged_object != None: # dragging stopped

      self.dragged_object = None
      
      self.dragging_trigger.Active.value = False # deactivate dragging callback

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
        

  # functions
  ## Called when in dragging. Updates the position of the dragged object.
  def dragging_callback(self):

    _mat = self.ray_transform.WorldTransform.value * self.dragging_offset
    
    self.dragged_object.set_world_transform(_mat)

  ## Change the hierarchy selection level to a given level.
  # @param HIERARCHY_LEVEL The new hierarchy selection level to be set.
  def set_hierarchy_selection_level(self, HIERARCHY_LEVEL):

    self.hierarchy_selection_level = HIERARCHY_LEVEL
    
    print "hierarchy selection level", self.hierarchy_selection_level
    
    if self.hierarchy_selection_level >= 0:
      _material = self.MANIPULATION_MANAGER.get_hierarchy_material(HIERARCHY_LEVEL)
     
      self.ray_geometry.Material.value = _material
      self.intersection_point_geometry.Material.value = _material

    else:
      self.ray_geometry.Material.value = "data/materials/White.gmd"
      self.intersection_point_geometry.Material.value = "data/materials/White.gmd"
  
  ## Updates the ray according to the intersections found.
  def update_ray(self):
  
    if len(self.mf_pointer_pick_result.value) > 0: # intersection found    
      _pick_result = self.mf_pointer_pick_result.value[0] # get first intersection target
    
      #print _pick_result.Object.value, _pick_result.Object.value.Name.value

      # update intersection point
      #_point = _pick_result.WorldPosition.value # intersection point in world coordinate system --> not working ???
    
      _point = _pick_result.Position.value # intersection point in object coordinate system

      _node = _pick_result.Object.value
      _point = _node.WorldTransform.value * _point # transform point into world coordinates
      _point = avango.gua.Vec3(_point.x,_point.y,_point.z) # make Vec3 from Vec4
      
      self.intersection_point_geometry.Transform.value = avango.gua.make_trans_mat(_point) * \
                                                          avango.gua.make_scale_mat(self.intersection_sphere_size, self.intersection_sphere_size, self.intersection_sphere_size)
                                                          
      self.intersection_point_geometry.GroupNames.value = [] # set geometry visible
  
      # update ray length
      _distance = (_point - self.ray_transform.WorldTransform.value.get_translate()).length()
  
      self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,_distance * -0.5) * \
                                          avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                          avango.gua.make_scale_mat(self.ray_thickness, _distance, self.ray_thickness)
  
    else: # no intersection found
      #print "None"
      self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible
  
      # set to default ray length
      self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                                          avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                          avango.gua.make_scale_mat(self.ray_thickness, self.ray_length, self.ray_thickness)


  ## Updates the object to be highlighted according to the intersections found.
  def update_object_highlight(self):
  
    if len(self.mf_pointer_pick_result.value) > 0: # intersection found    
      _pick_result = self.mf_pointer_pick_result.value[0] # get first intersection target
      
      _node = _pick_result.Object.value
      
      #print "hit", _node, _node.Name.value, _node.has_field
      
      if _node.has_field("InteractiveObject") == True:
        _object = _node.InteractiveObject.value
        
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

  
  
