#!/usr/bin/python

## @file
# Starting point of the application.

# import guacamole libraries
import avango
import avango.gua

# import framwork libraries
from lib.SceneManager import *
from lib.ViewingManager import *

# import python libraries
import sys


## Main method for the application
def start():

  # initialize materials
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")

  # create loader class for geometry loading
  loader = avango.gua.nodes.GeometryLoader()

  # create scenegraph
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

  # initialize viewing setup
  viewing_manager = ViewingManager(graph, sys.argv[1])

  # initialize scene
  scene_manager = SceneManager(loader, graph.Root.value)

  # run application loop
  viewing_manager.run(locals(), globals())

if __name__ == '__main__':
  start()
