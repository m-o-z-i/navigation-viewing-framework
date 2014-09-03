#!/usr/bin/python

## @file
# Client application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.script
import avango.gua
import avango.oculus
from   examples_common.GuaVE import GuaVE

# import framework libraries
import ClientMaterialUpdaters
from View import *
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


  ## @var shell
  # The GuaVE shell to be used when the application is running.
  shell = GuaVE()

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

  # get the server ip
  server_ip = str(sys.argv[1])
  #server_ip = "127.0.0.1"

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
                #Groupname = "AVCLIENT|{0}|7432".format(server_ip)
                Groupname = "AVCLIENT|{0}|5665".format(server_ip)
                )

  # create a dummy scenegraph to be extended by distribution
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")
  graph.Root.value.Children.value = [nettrans]

  # create material updaters as this cannot be distributed
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")

  
  #'''
  timer = avango.nodes.TimeSensor()
  
  water_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  water_updater.MaterialName.value = "data/materials/Water.gmd"
  water_updater.UniformName.value = "time"
  water_updater.TimeIn.connect_from(timer.Time)
  #'''



  '''
  avango.gua.load_shading_models_from("data/materials/bwb")
  avango.gua.load_materials_from("data/materials/bwb")

  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_l", "pre_scene2_texture")
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_r", "pre_scene2_texture")
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_depth_l", "pre_scene2_texture_depth")
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "background_depth_r", "pre_scene2_texture_depth")   
  avango.gua.set_material_uniform("data/materials/bwb/Fog.gmd", "sun_transform", avango.gua.make_rot_mat(-148, 0, 1, 0) * avango.gua.make_rot_mat(-15.0, 1.0, 0.0, 0.0))

  timer = avango.nodes.TimeSensor()

  fog_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  fog_updater.MaterialName.value = "data/materials/bwb/Fog.gmd"
  fog_updater.UniformName.value = "time"
  fog_updater.TimeIn.connect_from(timer.Time)
  '''

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
  
  #avango.gua.load_material("data/materials/bwb/Glass2.gmd")


  #avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_l", "pre_scene1_texture")
  #avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_r", "pre_scene1_texture")  
  #avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_l", "pre_scene1_texture_left")
  #avango.gua.set_material_uniform("data/materials/bwb/Glass2.gmd", "background_texture_r", "pre_scene1_texture_right")

  """
  _loader = avango.gua.nodes.PLODLoader()
  _loader.UploadBudget.value = 128
  _loader.RenderBudget.value = 1024
  _loader.OutOfCoreBudget.value = 4 * 1024

  #SpaceMonkey
  _SpaceMonkey = _loader.create_geometry_from_file("spacemonkey", "/mnt/SSD/PLOD_Models/Spacemonkey/Spacemonkey_new.kdn", avango.gua.LoaderFlags.DEFAULTS)

  #SeradinaRock
  _SeradinaRock1   = _loader.create_geometry_from_file("SeradinaRock",          "/mnt/SSD/PLOD_Models/Seradina_Rock/TLS_Seradina_Rock-12C.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock2   = _loader.create_geometry_from_file("SeradinaRock_pitoti1",  "/mnt/SSD/PLOD_Models/Pitoti/Area-9_Deer.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock3   = _loader.create_geometry_from_file("SeradinaRock_pitoti2",  "/mnt/SSD/PLOD_Models/Pitoti/Area-12_Horn.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock4   = _loader.create_geometry_from_file("SeradinaRock_pitoti3",  "/mnt/SSD/PLOD_Models/Pitoti/Area-A_Dagger.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock5   = _loader.create_geometry_from_file("SeradinaRock_pitoti4",  "/mnt/SSD/PLOD_Models/Pitoti/Area-B_Dagger.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock6   = _loader.create_geometry_from_file("SeradinaRock_pitoti5",  "/mnt/SSD/PLOD_Models/Pitoti/Area-7_Warrior.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock7   = _loader.create_geometry_from_file("SeradinaRock_pitoti6",  "/mnt/SSD/PLOD_Models/Pitoti/Area-6_house_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock8   = _loader.create_geometry_from_file("SeradinaRock_pitoti7",  "/mnt/SSD/PLOD_Models/Pitoti/Area-6_house_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock9   = _loader.create_geometry_from_file("SeradinaRock_pitoti8",  "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P01.kdn",avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock10  = _loader.create_geometry_from_file("SeradinaRock_pitoti9",  "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock11  = _loader.create_geometry_from_file("SeradinaRock_pitoti10", "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P03.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock12  = _loader.create_geometry_from_file("SeradinaRock_pitoti11", "/mnt/SSD/PLOD_Models/Pitoti/Area-11_Stele_P04.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock13  = _loader.create_geometry_from_file("SeradinaRock_pitoti12", "/mnt/SSD/PLOD_Models/Pitoti/Area-3_Archers_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock13  = _loader.create_geometry_from_file("SeradinaRock_pitoti13", "/mnt/SSD/PLOD_Models/Pitoti/Area-3_Archers_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock15  = _loader.create_geometry_from_file("SeradinaRock_pitoti14", "/mnt/SSD/PLOD_Models/Pitoti/Area-7_Rosa-Camuna.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock16  = _loader.create_geometry_from_file("SeradinaRock_pitoti15", "/mnt/SSD/PLOD_Models/Pitoti/Standing-Rider_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock17  = _loader.create_geometry_from_file("SeradinaRock_pitoti16", "/mnt/SSD/PLOD_Models/Pitoti/Standing-Rider_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock18  = _loader.create_geometry_from_file("SeradinaRock_pitoti17", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_Alphabet_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock19  = _loader.create_geometry_from_file("SeradinaRock_pitoti18", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_Alphabet_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock20  = _loader.create_geometry_from_file("SeradinaRock_pitoti19", "/mnt/SSD/PLOD_Models/Pitoti/TLS_Naquane-Ossimo-8.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock21  = _loader.create_geometry_from_file("SeradinaRock_pitoti20", "/mnt/SSD/PLOD_Models/Pitoti/Area_4_hunter_with_bow.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock22  = _loader.create_geometry_from_file("SeradinaRock_pitoti21", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_SFM_Alphabet_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock23  = _loader.create_geometry_from_file("SeradinaRock_pitoti22", "/mnt/SSD/PLOD_Models/Pitoti/Area-8_SFM_Alphabet_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock24  = _loader.create_geometry_from_file("SeradinaRock_pitoti23", "/mnt/SSD/PLOD_Models/Pitoti/Area-13_Superimposition.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock25  = _loader.create_geometry_from_file("SeradinaRock_pitoti23", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock26  = _loader.create_geometry_from_file("SeradinaRock_pitoti25", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock27  = _loader.create_geometry_from_file("SeradinaRock_pitoti26", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P03.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock28  = _loader.create_geometry_from_file("SeradinaRock_pitoti27", "/mnt/SSD/PLOD_Models/Pitoti/Sellero_Rosa_Camuna_P04.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock29  = _loader.create_geometry_from_file("SeradinaRock_pitoti28", "/mnt/SSD/PLOD_Models/Pitoti/Area-10_Hunting_Scene_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock30  = _loader.create_geometry_from_file("SeradinaRock_pitoti29", "/mnt/SSD/PLOD_Models/Pitoti/Area-10_Hunting_Scene_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock31  = _loader.create_geometry_from_file("SeradinaRock_pitoti30", "/mnt/SSD/PLOD_Models/Pitoti/Area-10_Hunting_Scene_P03.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock32  = _loader.create_geometry_from_file("SeradinaRock_pitoti31", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-1.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock33  = _loader.create_geometry_from_file("SeradinaRock_pitoti32", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-2.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock34  = _loader.create_geometry_from_file("SeradinaRock_pitoti33", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-3.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock35  = _loader.create_geometry_from_file("SeradinaRock_pitoti34", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P01-4.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock36  = _loader.create_geometry_from_file("SeradinaRock_pitoti35", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-1.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock37  = _loader.create_geometry_from_file("SeradinaRock_pitoti36", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-2.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock38  = _loader.create_geometry_from_file("SeradinaRock_pitoti37", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-3.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock39  = _loader.create_geometry_from_file("SeradinaRock_pitoti38", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P02-4.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock40  = _loader.create_geometry_from_file("SeradinaRock_pitoti39", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-1.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock41  = _loader.create_geometry_from_file("SeradinaRock_pitoti40", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-2.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock42  = _loader.create_geometry_from_file("SeradinaRock_pitoti41", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-3.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock43  = _loader.create_geometry_from_file("SeradinaRock_pitoti42", "/mnt/SSD/PLOD_Models/Pitoti/Area-1_Warrior-scene_P03-4.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock44  = _loader.create_geometry_from_file("SeradinaRock_pitoti43", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-1.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock45  = _loader.create_geometry_from_file("SeradinaRock_pitoti44", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-2.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock46  = _loader.create_geometry_from_file("SeradinaRock_pitoti45", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-3.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock47  = _loader.create_geometry_from_file("SeradinaRock_pitoti46", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P01-4.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock48  = _loader.create_geometry_from_file("SeradinaRock_pitoti47", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-1.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock49  = _loader.create_geometry_from_file("SeradinaRock_pitoti48", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-2.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock50  = _loader.create_geometry_from_file("SeradinaRock_pitoti49", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-3.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock51  = _loader.create_geometry_from_file("SeradinaRock_pitoti50", "/mnt/SSD/PLOD_Models/Pitoti/Area-2_Plowing-scene_P02-4.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock52  = _loader.create_geometry_from_file("SeradinaRock_pitoti51", "/mnt/SSD/PLOD_Models/Pitoti/TLS_Foppe-di-Nadro_Rock-24.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock53  = _loader.create_geometry_from_file("SeradinaRock_pitoti52", "/mnt/SSD/PLOD_Models/Pitoti/Area-5_hunter_with_speer_P01.kdn", avango.gua.LoaderFlags.DEFAULTS)
  _SeradinaRock54  = _loader.create_geometry_from_file("SeradinaRock_pitoti53", "/mnt/SSD/PLOD_Models/Pitoti/Area-5_hunter_with_speer_P02.kdn", avango.gua.LoaderFlags.DEFAULTS)
  #dont work:
  #_SeradinaRock55  = _loader.create_geometry_from_file("SeradinaRock_pitoti53", "/mnt/SSD/PLOD_Models/Pitoti/Area-Area-15_Sun-shape_Superimposition.kdn", avango.gua.LoaderFlags.DEFAULTS)

  #street:
  _Street = [0] *28
  for i in range(1, 28):
        _Street[i]  = _loader.create_geometry_from_file("Streets"+str(i), "/mnt/SSD/PLOD_Models/Streets/out_"+str(i)+".kdn", avango.gua.LoaderFlags.DEFAULTS)

  #valley:
  _Valley = [0] *15
  for i in range(1, 15):
        _Valley[i]  = _loader.create_geometry_from_file("SeradinaValley"+str(i), "/mnt/SSD/PLOD_Models/Seradina_Valley/CONVERTED_Seradina_Part_"+str(i)+".kdn", avango.gua.LoaderFlags.DEFAULTS)
  """

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

  shell.start(locals(), globals())

  # start rendering process
  viewer.run()

if __name__ == '__main__':
  start()
