#!/usr/bin/python

## @file
# Client application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.script
import avango.gua
import avango.oculus

# import framework libraries
import ClientMaterialUpdaters
from View import *
from ClientPortal import * 
from display_config import displays

# import python libraries
import sys

# Command line parameters:
# client.py SERVER_IP PLATFORM_ID DISPLAY_NAME SCREEN_NUM
# @param SERVER_IP The IP address on which the server process is running.
# @param PLATFORM_ID The platform id for which this client is responsible for.
# @param DISPLAY_NAME The name associated to the display for which this client is responsible for.
# @param SCREEN_NUM The number of the screen on the platform.

## Main method for the client application.
def start():

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

  # get the server ip
  server_ip = str(sys.argv[1])

  # get the platform id
  platform_id = int(sys.argv[2])

  # get the display name
  display_name = str(sys.argv[3])

  # get the screen number on platform
  screen_num = int(sys.argv[4])

  # get own hostname
  hostname = open('/etc/hostname', 'r').readline()
  hostname = hostname.strip(" \n")

  print "This client is running on", hostname, "and listens to server", server_ip
  print "It is responsible for platform", platform_id, "and display", display_name

  # create distribution node
  nettrans = avango.gua.nodes.NetTransform(
                Name = "net",
                # specify role, ip, and port
                Groupname = "AVCLIENT|{0}|7432".format(server_ip)
                )

  # create a dummy scenegraph to be extended by distribution
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  # create node for local portal updates
  local_portal_node = avango.gua.nodes.TransformNode(Name = "local_portal_group")

  graph.Root.value.Children.value = [nettrans, local_portal_node]

  # create material updaters as this cannot be distributed
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")

  _loader = avango.gua.nodes.PLODLoader()
  _loader.UploadBudget.value = 32
  _loader.RenderBudget.value = 8*1024
  _loader.OutOfCoreBudget.value = 24*1024

  #_node = _loader.create_geometry_from_file("pig", "/opt/3d_models/point_based/plod/pig.kdn", avango.gua.PLODLoaderFlags.DEFAULTS | avango.gua.PLODLoaderFlags.NORMALIZE_POSITION | avango.gua.PLODLoaderFlags.NORMALIZE_SCALE | avango.gua.PLODLoaderFlags.MAKE_PICKABLE)
  #_node = _loader.create_geometry_from_file("spacemonkey", "/mnt/pitoti/KDN_LOD/PITOTI_KDN_LOD/Spacemonkey_new.kdn", avango.gua.PLODLoaderFlags.DEFAULTS | avango.gua.PLODLoaderFlags.NORMALIZE_POSITION | avango.gua.PLODLoaderFlags.NORMALIZE_SCALE | avango.gua.PLODLoaderFlags.MAKE_PICKABLE)

  # Pitoti
  _node = _loader.create_geometry_from_file("rock", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/TLS_Seradina_Rock-12C.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
    
  _node = _loader.create_geometry_from_file("pitoti1", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti2", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti3", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti4", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti5", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti6", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti7", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti8", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti9", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P03-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti10", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P03-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti11", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P03-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti12", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-1_Warrior-scene_P03-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("pitoti13", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti14", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti15", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti16", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti17", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti18", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti19", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti20", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-2_Plowing-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
    
  _node = _loader.create_geometry_from_file("pitoti21", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-10_Hunting_Scene_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti22", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-10_Hunting_Scene_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti23", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-10_Hunting_Scene_P03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    

  _node = _loader.create_geometry_from_file("pitoti24", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-6_house_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti25", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-6_house_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  

  _node = _loader.create_geometry_from_file("pitoti26", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-3_Archers_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti27", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-3_Archers_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    
  
  _node = _loader.create_geometry_from_file("pitoti28", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area_4_hunter_with_bow.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("pitoti29", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-5_hunter_with_speer_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)              
  _node = _loader.create_geometry_from_file("pitoti30", "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/Area-5_hunter_with_speer_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)      
      
  
  #'''
  timer = avango.nodes.TimeSensor()
  
  water_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  water_updater.MaterialName.value = "data/materials/Water.gmd"
  water_updater.UniformName.value = "time"
  water_updater.TimeIn.connect_from(timer.Time)
  #'''

  '''  
  avango.gua.load_material("data/materials/bwb/Fog.gmd")

  #avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_l", "pre_scene2_texture")
  #avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_r", "pre_scene2_texture")
  #avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_depth_l", "pre_scene2_texture_depth")
  #avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_depth_r", "pre_scene2_texture_depth")     
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_l", "pre_scene2_texture_left")
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_r", "pre_scene2_texture_right")
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_depth_l", "pre_scene2_texture_depth_left")
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_depth_r", "pre_scene2_texture_depth_right")   
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "sun_transform", avango.gua.make_rot_mat(-148, 0, 1, 0) * avango.gua.make_rot_mat(-15.0, 1.0, 0.0, 0.0))

  timer = avango.nodes.TimeSensor()

  fog_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  fog_updater.MaterialName.value = "data/materials/bwb/Fog.gmd"
  fog_updater.UniformName.value = "time"
  fog_updater.TimeIn.connect_from(timer.Time)
  '''
  
  '''
  avango.gua.load_material("data/materials/bwb/Glass2.gmd")

  #avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_l", "pre_scene1_texture")
  #avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_r", "pre_scene1_texture")  
  avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_l", "pre_scene1_texture_left")
  avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_r", "pre_scene1_texture_right")
  '''

  # get the display instance
  for _display in displays:
    if _display.name == display_name:
      handled_display_instance = _display

  # create a viewer
  viewer = avango.gua.nodes.Viewer()

  # Create a view for each displaystring (= slot)
  _string_num = 0
  views = []

  for _displaystring in handled_display_instance.displaystrings:
    _view = View()
    _view.my_constructor(graph, 
                         viewer,
                         platform_id, 
                         _string_num,
                         handled_display_instance, 
                         screen_num, 
                         handled_display_instance.stereo)
    views.append(_view)
    _string_num += 1

  viewer.SceneGraphs.value = [graph]

  # create client portal manager
  portal_manager = ClientPortalManager()
  portal_manager.my_constructor(graph, views)

  # start rendering process
  viewer.run()

if __name__ == '__main__':
  start()
