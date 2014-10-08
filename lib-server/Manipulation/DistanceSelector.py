#!/usr/bin/python

## @file
# Contains Miau


# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

from UIGeoFeature import*
from ObjectContact import *
from ObjectRelation import *

class DistanceSelector(avango.script.Script):
  def __init__(self):
    self.super(DistanceSelector).__init__()
    self.candidates = []
    self.distance_trigger = avango.script.nodes.Update(Callback = self.distance_callback, Active = False)

  def my_constructor(self, NET_TRANS_NODE):
    self.net_trans_node = NET_TRANS_NODE

  def add_candidate(self, CANDIDATE):
    self.candidates.append(CANDIDATE)
    print len(self.candidates)
    if len(self.candidates) >= 2:
      self.distance_trigger.Active.value = True
      

  def remove_candidate(self, CANDIDATE):
    self.candidates.remove(CANDIDATE)

  def check_distance(self, P1, P2):
    print (P1 - P2).length()
    if (P1 - P2).length() < 0.3:
      #print "WIR SIND UNS SO NAH"
      return True 
      
    else:
      return False

  def make_object_relation(self, CANDIDATE_1, CANDIDATE_2):
    _mat = avango.gua.make_identity_mat()
    _edge = UIEdge("data/objects/cylinder.obj", _mat, "data/materials/White.gmd", self.net_trans_node, self.net_trans_node, True, 0.1, avango.gua.Vec3(), avango.gua.Vec3())
    _object_relation = ObjectRelation()
    _object_relation.my_constructor(_edge, CANDIDATE_1, CANDIDATE_2, self)
    #print "..........."    

    self.candidates.remove(CANDIDATE_1)
    self.candidates.remove(CANDIDATE_2)
    
    
  # callbacks
  def distance_callback(self):
    
    for _candidate1 in self.candidates:
      for _candidate2 in self.candidates:
        if _candidate1.object != _candidate2.object:
          _distance = self.check_distance(_candidate1.intersection_point.value, _candidate2.intersection_point.value)
  
          if _distance == True:
            self.make_object_relation(_candidate1, _candidate2)
              
          




