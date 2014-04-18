#!/usr/bin/python

## @file
# Contains class HUDManager.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

# import framework libraries
from   Navigation import *

## Class to toggle the correct UI notifications for all users.
class HUDManager(avango.script.Script):

  ## @var timer
  # A timer instance to get the current time in seconds.
  timer = avango.nodes.TimeSensor()

  ## Default constructor.
  def __init__(self):
    self.super(HUDManager).__init__()

    ## @var users_waiting_for_time_update
    # Dict of User subclass instances (key) that require an update after a certain amount of time.
    # The value is the event's start time.
    self.users_waiting_for_time_update = dict()

  ## Custom constructor.
  # @param NET_TRANS_NODE Reference to the net transformation node for distribution.
  # @param USER_LIST Reference to the list containing all users in the setup.
  def my_constructor(self, NET_TRANS_NODE, USER_LIST):

    ## @var NET_TRANS_NODE
    # Reference to the net transformation node for distribution.
    self.NET_TRANS_NODE = NET_TRANS_NODE

    ## @var USER_LIST
    # Reference to the list containing all users in the setup.
    self.USER_LIST = USER_LIST

    # set evaluation policy
    self.always_evaluate(True)

  ## Updates the stored nettrans node.
  # @param NET_TRANS_NODE The new nettrans node to be stored.
  def update_nettrans_node(self, NET_TRANS_NODE):

    self.NET_TRANS_NODE = NET_TRANS_NODE

  ## Checks which users are on a specific platform and switches their coupling plane to visible
  # @param PLATFORM_ID The platform's id on which the users should be notified.
  def show_coupling_plane(self, PLATFORM_ID):
    
    for _user in self.USER_LIST:
      if _user.platform_id == PLATFORM_ID:
        
        # if user is in watchlist, remove it as a new plane is displayed
        if _user in self.users_waiting_for_time_update:
          del self.users_waiting_for_time_update[_user]

        # display coupling plane
        _user.coupling_plane_node.Material.value = "data/materials/CouplingPlane.gmd"
        _user.coupling_plane_node.GroupNames.value[0] = "display_group"

        # hide decoupling notifier if it isn't already
        _user.decoupling_notifier.GroupNames.value[0] = "do_not_display_group"

  ## Checks which users are on a specific platform and switches their coupling plane to invisible
  # @param PLATFORM_ID The platform's id on which the user's coupling plane should be disabled.
  def hide_coupling_plane(self, PLATFORM_ID):

    for _user in self.USER_LIST:
      if _user.platform_id == PLATFORM_ID:
        _user.coupling_plane_node.GroupNames.value[0] = "do_not_display_group"

  ## Tells the HUDManager that a list of navigations is now coupled. The HUDManager will 
  # then check for all users on the platforms and update their coupling status notifiers.
  # @param COUPLED_NAVIGATION_LIST List of Navigation instances that are now coupled.
  def display_coupling(self, COUPLED_NAVIGATION_LIST):

    _loader = avango.gua.nodes.GeometryLoader()

    # check for every user that could be updated
    for _user in self.USER_LIST:

      # if the user is on a platform
      for _nav_1 in COUPLED_NAVIGATION_LIST:
        if _user.platform_id == _nav_1.platform.platform_id:
 
          # add every other platform to his notifiers
          for _nav_2 in COUPLED_NAVIGATION_LIST:
            if _nav_1 != _nav_2:
              
              # check if desired plane is not already present
              _new_node_needed = True

              for _node in _user.coupling_status_node.Children.value:
                if (_node.Name.value == ('user_' + str(_user.id) +'_coupl_notifier_' + str(_nav_2.platform.platform_id))):
                  _new_node_needed = False
                  break

              # if the desired plane is not yet present, create and draw it
              if _new_node_needed:
                _plane = _loader.create_geometry_from_file('user_' + str(_user.id) +'_coupl_notifier_' + str(_nav_2.platform.platform_id),
                                                           'data/objects/plane.obj',
                                                           'data/materials/' +_nav_2.trace_material + 'Shadeless.gmd',
                                                           avango.gua.LoaderFlags.LOAD_MATERIALS)
                self.NET_TRANS_NODE.distribute_object(_plane)
                _user.coupling_status_node.Children.value.append(_plane)
      
      # update the offsets of the notifiers to have a proper display
      _user.update_coupling_status_overview()

  ## Tells the HUDManager that a Navigation instance is now out of every coupling. The HUDManager will
  # then check for all users on the platforms and update their coupling status notifiers. Apart from that,
  # a message is shown to all users in the group that NAVIGATION has decoupled from the group.
  # @param NAVIGATION The Navigation instance to be removed from all couplings.
  def remove_from_coupling_display(self, NAVIGATION):

    _loader = avango.gua.nodes.GeometryLoader()

    # check for every user that could be updated
    for _user in self.USER_LIST:

      # if the user is on NAVIGATION's platform, simply remove all notifiers but the own color notifier
      if _user.platform_id == NAVIGATION.platform.platform_id:
        _user.coupling_status_node.Children.value = [_user.coupling_status_node.Children.value[0]]
        continue

      # if the user has a notifier for being coupled with NAVIGATION, remove this node from the scenegraph
      for _node in _user.coupling_status_node.Children.value:
        if (_node.Name.value == ('user_' + str(_user.id) + "_coupl_notifier_" + str(NAVIGATION.platform.platform_id))):
          _user.coupling_status_node.Children.value.remove(_node)
          _user.update_coupling_status_overview()
          
          # display notification that a user was decoupled
          _user.coupling_plane_node.GroupNames.value[0] = "display_group"
          _user.coupling_plane_node.Material.value = "data/materials/DecouplingPlane.gmd"

          # display color of decoupled navigation
          _user.decoupling_notifier.GroupNames.value[0] = "display_group"
          _user.decoupling_notifier.Material.value = 'data/materials/' + NAVIGATION.trace_material + 'Shadeless.gmd'

          # add user to watchlist such that the notifications are removed again after a certain
          # amount of time
          self.users_waiting_for_time_update[_user] = self.timer.Time.value

          break

  ## Evaluated every frame.
  def evaluate(self):

    # hide decoupling notifiers again after a certain amount of time
    for _key_user in self.users_waiting_for_time_update:

      if self.timer.Time.value - self.users_waiting_for_time_update[_key_user] > 3.0:

        # hide message plane and reset its material
        _key_user.coupling_plane_node.GroupNames.value[0] = "do_not_display_group"

        # hide decoupling notifier
        _key_user.decoupling_notifier.GroupNames.value[0] = "do_not_display_group"

        # remove user from watchlist
        del self.users_waiting_for_time_update[_key_user]
        break