#!/usr/bin/python

## @file
# Contains classes ManipulationManager and RayPointer.

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed
import avango.daemon

class State:

  ### default constructor
  def __init__(self, name = None, operation = None, inTransition = None, outTransition = None):

   # print "init new state:", name
    self.name = name

    ### init state functions
    self.operation = None
    self.inTransition = None
    self.outTransition = None


    if operation != None:
      self.operation = operation

    if inTransition != None:
      self.inTransition = inTransition
        
    if outTransition != None:
      self.outTransition = outTransition


  ### functions
  def getName(self):
  
    return self.name



class StateHandler:

  ### default constructor
  def __init__(self):

    self.states = {} # dictonary of state classes
    self.currentState = None


  ### functions
  def addState(self, name = None , operation = None, inTransition = None, outTransition = None):

    if name == None:
      #print "error: no state name defined"
      return

    _state = State(name, operation, inTransition, outTransition)
    
    self.states[name] = _state # store new state in dictonary

     
  def setState(self, name):
  
    _key_list = self.states.keys()

    if _key_list.count(name) > 0: # valid state 
      _state = self.states[name]
      
      if _state != self.currentState: # state has changed

        if self.currentState != None: # check for valid state

          if self.currentState.outTransition != None: # check if OUT transition function is defined
            self.currentState.outTransition() # call OUT transition function of current state

        self.currentState = _state # set new state
        #print "new state:", self.currentState.getName()

        if self.currentState.inTransition != None: # check if IN transition function is defined
          self.currentState.inTransition() # call IN transition function of new state
          
  
  def previousState(self):

    if self.currentState != None:
      _key_list = self.states.keys()
      _index = _key_list.index(self.currentState.getName())
  
      self.setState(_key_list[_index+1]) # set state machine to next state

  
  def nextState(self):

    if self.currentState != None:
      _key_list = self.states.keys()
      _index = _key_list.index(self.currentState.getName())
  
      self.setState(_key_list[_index-1]) # set state machine to previous state
  
  
  def run(self):

    if self.currentState != None: # check for valid state
   
      if self.currentState.operation != None: # check if operation function is defined
        self.currentState.operation() # call operation function of current state

