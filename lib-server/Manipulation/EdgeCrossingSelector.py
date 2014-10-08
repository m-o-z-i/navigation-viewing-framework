#!/usr/bin/python

## @file
# Contains EdgeCrossingSelector and Crossing Result


# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

from UIGeoFeature import*

###############################################################################################

class EdgeCrossingSelector:


  def __init__(self,DEFAULT_TYPE):
    self.default_type = DEFAULT_TYPE

    self.candidates = []
   
  def add_candidate(self, CANDIDATE):
    self.candidates.append(CANDIDATE)

  def remove_candidate(self, CANDIDATE):
    self.candidates.remove(CANDIDATE) 

  def check_crossing(self, P1, P2, P3):
  
    _point = P1
    _normal = (P2 - P1).cross(P3 - P1)

    for _candidate in self.candidates:
      

    _crossing_result = CrossingResult(_edge, _point)
    return _crossing_result

###############################################################################################
class CrossingResult:
  def __init__(self, EDGE, POINT)
    self.edge = EDGE
    self.crossing_point = POINT
