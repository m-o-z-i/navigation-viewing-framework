#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

# import python libraries
# ...

# import framework libraries
from Intersection import *


class ManipulationManager:

  # constructor
  def __init__(self, NET_TRANS_NODE, SCENEGRAPH, SCENE_MANAGER):
  
    # references
    self.SCENE_MANAGER = SCENE_MANAGER
  
    # init first ray
    _parent_node = SCENEGRAPH["/net/platform_0"]
    _transmitter_offset = avango.gua.make_trans_mat(0.0,0.043,1.6)
  
    self.ray_pointer1 = RayPointer()
    self.ray_pointer1.my_constructor(self, 1, SCENEGRAPH, NET_TRANS_NODE, _parent_node, _transmitter_offset, "tracking-dlp-pointer1", "device-pointer1")


  # functions
  def get_hierarchy_material(self, INDEX):
  
    return self.SCENE_MANAGER.get_hierarchy_material(INDEX)



class RayPointer(avango.script.Script):

  # internal fields
  sf_pointer_button0 = avango.SFBool()
  sf_pointer_button1 = avango.SFBool()
  sf_pointer_button2 = avango.SFBool()  

  mf_pointer_pick_result = avango.gua.MFPickResult()

  # constructor
  def __init__(self):
    self.super(RayPointer).__init__()


  def my_constructor(self, MANIPULATION_MANAGER, ID, SCENEGRAPH, NET_TRANS_NODE, PARENT_NODE, TRACKING_TRANSMITTER_OFFSET, POINTER_TRACKING_STATION, POINTER_DEVICE_STATION):
    
    # references
    self.MANIPULATION_MANAGER = MANIPULATION_MANAGER
    
    # parameters
    self.ray_length = 10.0 # in meter
    self.ray_thickness = 0.0075 # in meter
    self.intersection_sphere_size = 0.025 # in meter
    self.hierarchy_selection_level = 0

    # variables
    self.id = ID
    self.highlighted_object = None
    self.dragged_object = None
    self.dragging_offset = None

    # init sensors
    self.pointer_tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.pointer_tracking_sensor.Station.value = POINTER_TRACKING_STATION
    self.pointer_tracking_sensor.ReceiverOffset.value = avango.gua.make_identity_mat()
    self.pointer_tracking_sensor.TransmitterOffset.value = TRACKING_TRANSMITTER_OFFSET
        
    self.pointer_device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.pointer_device_sensor.Station.value = POINTER_DEVICE_STATION

    # init scenegraph node
    self.ray_transform = avango.gua.nodes.TransformNode(Name = "ray_transform")
    PARENT_NODE.Children.value.append(self.ray_transform)

    _loader = avango.gua.nodes.GeometryLoader()
    
    self.ray_geometry = _loader.create_geometry_from_file("ray_geometry", "data/objects/cylinder.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
    self.ray_transform.Children.value.append(self.ray_geometry)
    self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                                            avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                            avango.gua.make_scale_mat(0.005,self.ray_length,0.005)
  
    self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry", "data/objects/sphere.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
    NET_TRANS_NODE.Children.value.append(self.intersection_point_geometry)
    self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible

    self.dragging_trigger = avango.script.nodes.Update(Callback = self.dragging_callback, Active = False)
      
    # init sub classes
    self.pointer_intersection = Intersection() # ray intersection for target identification
    self.pointer_intersection.my_constructor(SCENEGRAPH, self.ray_transform.WorldTransform, self.ray_length) # parameters: SCENEGRAPH, SF_PICK_MATRIX, PICK_LENGTH
    
    # init field connections
    self.ray_transform.Transform.connect_from(self.pointer_tracking_sensor.Matrix)
    self.mf_pointer_pick_result.connect_from(self.pointer_intersection.mf_pick_result)
    self.sf_pointer_button0.connect_from(self.pointer_device_sensor.Button0)
    self.sf_pointer_button1.connect_from(self.pointer_device_sensor.Button1)
    self.sf_pointer_button2.connect_from(self.pointer_device_sensor.Button2)

    self.set_hierarchy_selection_level(-1)
    
    
  # callbacks
  @field_has_changed(mf_pointer_pick_result)
  def mf_pointer_pick_result_mat_changed(self):

    self.update_ray()
    self.update_object_highlight()
    

  @field_has_changed(sf_pointer_button0)
  def sf_pointer_button0_changed(self):

    if self.sf_pointer_button0.value == True and self.highlighted_object != None: # dragging started

      self.dragged_object = self.highlighted_object
      
      self.dragging_offset = avango.gua.make_inverse_mat(self.ray_transform.WorldTransform.value) * self.dragged_object.get_world_transform()

      self.dragging_trigger.Active.value = True # activate dragging callback

    elif self.sf_pointer_button0.value == False and self.dragged_object != None: # dragging stopped

      self.dragged_object = None
      
      self.dragging_trigger.Active.value = False # deactivate dragging callback



  @field_has_changed(sf_pointer_button1)
  def sf_pointer_button1_changed(self):

    if self.sf_pointer_button1.value == True:
      self.set_hierarchy_selection_level(min(self.hierarchy_selection_level + 1, 3))
      

  @field_has_changed(sf_pointer_button2)
  def sf_pointer_button2_changed(self):

    if self.sf_pointer_button2.value == True:
      self.set_hierarchy_selection_level(max(self.hierarchy_selection_level - 1, -1))
        

  # functions
  def dragging_callback(self):

    _mat = self.ray_transform.WorldTransform.value * self.dragging_offset
    
    self.dragged_object.set_world_transform(_mat)


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
  
  
  def update_ray(self):
  
    if len(self.mf_pointer_pick_result.value) > 0: # intersection found    
      _pick_result = self.mf_pointer_pick_result.value[0] # get first intersection target

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
      self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible
  
      # set to default ray length
      self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                                          avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                          avango.gua.make_scale_mat(self.ray_thickness, self.ray_length, self.ray_thickness)



  def update_object_highlight(self):
  
    if len(self.mf_pointer_pick_result.value) > 0: # intersection found    
      _pick_result = self.mf_pointer_pick_result.value[0] # get first intersection target
      
      _node = _pick_result.Object.value
      
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

  
  
