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
from examples_common.GuaVE import GuaVE

# import python libraries
import sys

# Command line parameters:
# main.py SERVER_IP WORKSPACE_CONFIG_FILE WORKSPACE_ID DISPLAY_GROUP_ID SCREEN_ID DISPLAY_NAME

## Main method for the client application.
def start():

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

  # get the server ip
  server_ip = str(sys.argv[1])

  # get the workspace config file #
  workspace_config_file = str(sys.argv[2])
  exec('from ' + workspace_config_file.replace("/", ".").replace(".py", "") + ' import displays', globals())

  # get the workspace id
  workspace_id = int(sys.argv[3])

  # get the display group id
  display_group_id = int(sys.argv[4])

  # get the screen id
  screen_id = int(sys.argv[5])

  # get the display name
  display_name = str(sys.argv[6])

  # get own hostname
  hostname = open('/etc/hostname', 'r').readline()
  hostname = hostname.strip(" \n")

  print("This client is running on", hostname, "and listens to server", server_ip)
  print("It is responsible for workspace", workspace_id, ", display group", display_group_id, "and screen", screen_id)

  # preload materials and shading models
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")
  
  # create distribution node
  nettrans = avango.gua.nodes.NetTransform(
                Name = "net",
                # specify role, ip, and port
                Groupname = "AVCLIENT|{0}|7432".format(server_ip)
                )

  # create a dummy scenegraph to be extended by distribution
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  graph.Root.value.Children.value = [nettrans]

  # create material updaters as this cannot be distributed
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")
  
  timer = avango.nodes.TimeSensor()
  
  water_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  water_updater.MaterialName.value = "data/materials/Water.gmd"
  water_updater.UniformName.value = "time"
  water_updater.TimeIn.connect_from(timer.Time)

  '''
  # PLOD Stuff
  _loader = avango.gua.nodes.PLODLoader()
  _loader.UploadBudget.value = 256
  _loader.RenderBudget.value = 4*1024
  _loader.OutOfCoreBudget.value = 24*1024

  
  # Valcamonica
  _path = "/mnt/pitoti/KDN_LOD/PITOTI_KDN_LOD/01_SFM-Befliegung_Seradina_PointCloud/" # opt path
  #_path = "/media/SSD_500GB/CONVERTED_Seradina_Parts/" # ssd path 

  _node = _loader.create_geometry_from_file("seradina1_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina2_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina3_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina4_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_04.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    
  _node = _loader.create_geometry_from_file("seradina5_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_05.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina6_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_06.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina7_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_07.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina8_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_08.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina9_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_09.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina10_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_10.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina11_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_11.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina12_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_12.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina13_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_13.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina14_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_14.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina15_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_15.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina16_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_16.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  
  # seradina rock
  _path = "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/" # opt path
  #_path = "/media/SSD_500GB/Pitoti_Resampled/" # ssd path
  _node = _loader.create_geometry_from_file("rock", _path + "TLS_Seradina_Rock-12C.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  
  # seradina pitoti
  _node = _loader.create_geometry_from_file("pitoti1", _path + "Area-1_Warrior-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti2", _path + "Area-1_Warrior-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti3", _path + "Area-1_Warrior-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti4", _path + "Area-1_Warrior-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti5", _path + "Area-1_Warrior-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti6", _path + "Area-1_Warrior-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti7", _path + "Area-1_Warrior-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti8", _path + "Area-1_Warrior-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti9", _path + "Area-1_Warrior-scene_P03-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti10", _path + "Area-1_Warrior-scene_P03-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti11", _path + "Area-1_Warrior-scene_P03-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti12", _path + "Area-1_Warrior-scene_P03-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("pitoti13", _path + "Area-2_Plowing-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti14", _path + "Area-2_Plowing-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti15", _path + "Area-2_Plowing-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti16", _path + "Area-2_Plowing-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti17", _path + "Area-2_Plowing-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti18", _path + "Area-2_Plowing-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti19", _path + "Area-2_Plowing-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti20", _path + "Area-2_Plowing-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
    
  _node = _loader.create_geometry_from_file("pitoti21", _path + "Area-10_Hunting_Scene_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti22", _path + "Area-10_Hunting_Scene_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti23", _path + "Area-10_Hunting_Scene_P03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    

  _node = _loader.create_geometry_from_file("pitoti24", _path + "Area-6_house_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti25", _path + "Area-6_house_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  

  _node = _loader.create_geometry_from_file("pitoti26", _path + "Area-3_Archers_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti27", _path + "Area-3_Archers_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    
  
  _node = _loader.create_geometry_from_file("pitoti28", _path + "Area_4_hunter_with_bow.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("pitoti29", _path + "Area-5_hunter_with_speer_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)              
  _node = _loader.create_geometry_from_file("pitoti30", _path + "Area-5_hunter_with_speer_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)      
  # END PLOD stuff
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
                         handled_display_instance, 
                         workspace_id,
                         display_group_id,
                         screen_id,
                         _string_num)
    views.append(_view)
    _string_num += 1

  viewer.SceneGraphs.value = [graph]

  # create client portal manager
  portal_manager = ClientPortalManager()
  portal_manager.my_constructor(graph, views)

  shell_client = GuaVE()
  shell_client.start(locals(), globals())

  # start rendering process
  viewer.run()

if __name__ == '__main__':
  start()
