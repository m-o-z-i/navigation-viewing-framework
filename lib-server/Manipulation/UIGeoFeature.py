#!/usr/bin/python


import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import time


class UIGeoFeature:

  def __init__(self, GEOMETRY, MATRIX, MATERIAL, NET_TRANS_NODE, PARENT_NODE, VISIBILITY):

    self.visibility = VISIBILITY
    self.creation_time = time.time()
    self.parent_node = PARENT_NODE

    _loader = avango.gua.nodes.TriMeshLoader()
    self.geometry = _loader.create_geometry_from_file("geometry", GEOMETRY, MATERIAL, avango.gua.LoaderFlags.DEFAULTS)

    self.geometry.Transform.value = MATRIX


    PARENT_NODE.Children.value.append(self.geometry)
    NET_TRANS_NODE.distribute_object(self.geometry)

  def set_transform(self, MATRIX):
    self.geometry.Transform.value = MATRIX

  def set_material(self, MATERIAL):
    self.geometry.Material.value = MATERIAL

  def get_geometry(self):
    return self.geometry

  def delete(self):
    self.parent_node.Children.value.remove(self.geometry)
    
#############################################################################################################

class UIEdge(UIGeoFeature):

  def __init__(self, GEOMETRY, MATRIX, MATERIAL, NET_TRANS_NODE, PARENT_NODE, VISIBILITY, LINE_THICKNESS, START , END):
    UIGeoFeature.__init__(self, GEOMETRY, MATRIX, MATERIAL, NET_TRANS_NODE, PARENT_NODE, VISIBILITY)
    print "Egde erstellt!"
    #TODO MATRIX aus start und end und thickness
    #self.options = OPTIONS
  

  #def set_start(self, POINT):
   #TODO Matrix update

  #def set_end(self, POINT):
    #TODO Matrix update

  #def set_thickness(self,THICKNESS)
    #TODO Matrix update

#############################################################################################################

class UIPoint(UIGeoFeature):

  def __init__(self, GEOMETRY, MATRIX, MATERIAL, PARENT_NODE, VISIBILITY, DIAMETER):
    
    UIGeoFeature.__init__(self, GEOMETRY, MATRIX, MATERIAL, PARENT_NODE, VISIBILITY)
    self.diameter=DIAMETER

  def set_position(self, POINT):
    position = POINT

#############################################################################################################


class UIPlane(UIGeoFeature):

  def __init__(self, GEOMETRY, MATRIX, MATERIAL, PARENT_NODE, VISIBILITY, NORMAL):
    UIGeoFeature.__init__(self, GEOMETRY, MATRIX, MATERIAL, PARENT_NODE, VISIBILITY)
    self.normal = NORMAL





    


  







