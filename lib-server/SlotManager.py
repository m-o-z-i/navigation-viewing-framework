#!/usr/bin/python

## @file
# Contains class SlotManager.

# import avango-guacamole libraries
import avango
import avango.gua
import RadioMasterHID

# import python libraries
from copy import copy


## Class to handle shutter configurations and timings. Associates the users per display to
# the available slots and sets the glasses correctly.
class SlotManager:

  ## Custom constructor.
  # @param USER_LIST Reference to a list of all users in the setup.
  def __init__(self, USER_LIST):

    ## @var users
    # Reference to a list of all users to be handled in the setup.
    self.users = USER_LIST

    ## @var slots
    # Dictionary to map Display instances to a list of associated Slot instances.
    self.slots = dict()

    ## @var radio_master_hid
    # Instance of RadioMasterHID to handle shutter glass configurations.
    self.radio_master_hid = RadioMasterHID.RadioMaster()
    self.radio_master_hid.set_master_transmit(1)
    self.radio_master_hid.set_master_timing(16600,16500)
    self.radio_master_hid.send_master_config() 


  ## Tells the SlotManager that a new Slot instance is to be handled for a certain Display instance.
  # @param SLOT The Slot instance to register.
  # @param DISPLAY The Display instance to which the new slot belongs to.
  def register_slot(self, SLOT, DISPLAY):
    if DISPLAY in self.slots:
      _slot_list = self.slots[DISPLAY]
      _slot_list.append(SLOT)
      self.slots[DISPLAY] = _slot_list
    else:
      self.slots[DISPLAY] = [SLOT]


  ## Updates the shutter timings and scenegraph slot connections according to the
  # vip / active status, display and platform of users.
  def update_slot_configuration(self):
    
    # loop over all displays to be handled
    for _display in self.slots:

      # check if current display is a stereo one
      _stereo = True
      if _display.shutter_timings == []:
        _stereo = False

      _default_user_list = []
      _vip_user_list = []
      _disabled_user_list = []
      _concatenated_user_list = []
      _num_users_on_display = 0

      # fill user lists for this display
      for _user in self.users:

        if _user.current_display != _display:
          continue

        _num_users_on_display += 1

        # inactive user
        if _user.is_active == False:
          _disabled_user_list.append([_user, 0])

        # active user
        elif _user.is_vip == False:
          _default_user_list.append([_user, 1])

        # active user and vip
        else:
          _vip_user_list.append([_user, 1])

      # get free slots still to be distributed
      _number_free_slots = len(self.slots[_display]) - len(_default_user_list) - len(_vip_user_list)

      # if vip users are present, distribute the free slots among them
      if len(_vip_user_list) > 0:
        _i = 0
        
        while _number_free_slots > 0:
          # add slot to vip user _i
          _vip_user_list[_i][1] += 1
          _i += 1

          # start again when at end of list
          if _i == len(_vip_user_list):
            _i = 0

          _number_free_slots -= 1

        _concatenated_user_list = _default_user_list + _vip_user_list + _disabled_user_list
      
      # all users are disabled
      elif _num_users_on_display == len(_disabled_user_list):
        _concatenated_user_list = _disabled_user_list

      # all users are default users, distribute remaining slots among them
      else:
        _i = 0

        while _number_free_slots > 0:
          # add slot to default user _i
          _default_user_list[_i][1] += 1
          _i += 1

          # start again when at end of list
          if _i == len(_default_user_list):
            _i = 0

          _number_free_slots -= 1

        _concatenated_user_list = _default_user_list + _vip_user_list + _disabled_user_list

      # update shutter values according to slots assigned
      print "?????????", _concatenated_user_list

      _i = 0
      for _state in _concatenated_user_list:

        _user = _state[0]
        _number_of_slots = _state[1]
        _slot_instances = self.slots[_display]

        # clear all slot connections
        for _slot in _slot_instances:
          _slot.clear_user()

        # check if the user has slots assigned to him
        if _number_of_slots > 0:
          if _stereo:
            # stereo display - set proper shutter timings
            _open_timings = _slot_instances[_i].shutter_timing[0]
            _open_values = _slot_instances[_i].shutter_value[0]
            _start_i = copy(_i)
            
            _i += (_number_of_slots - 1)

            _close_timings = _slot_instances[_i].shutter_timing[1]
            _close_values = _slot_instances[_i].shutter_value[1]
            _end_i = copy(_i)

            _j = 0

            # set ids with shutter timings and values properly
            while _j < len(_open_timings):
              print "!!!!!!!!!! OPEN USER", _user.glasses_id, "TIMING", _open_timings[_j]
              self.radio_master_hid.set_timer_value(_user.glasses_id, _j, _open_timings[_j])
              print "!!!!!!!!!! OPEN USER", _user.glasses_id, "ORIGINAL", _open_values[_j], "VALUE", int(str(_open_values[_j]), 16)
              self.radio_master_hid.set_shutter_value(_user.glasses_id, _j, int(str(_open_values[_j]), 16))
              _j += 1

            while _j < 2 * len(_open_timings):
               print "!!!!!!!!!! CLOSE USER", _user.glasses_id, "TIMING", _close_timings[_j - len(_open_timings)]
               self.radio_master_hid.set_timer_value(_user.glasses_id, _j, _close_timings[_j - len(_open_timings)])
               print "!!!!!!!!!! CLOSE USER", _user.glasses_id, "ORIGINAL", _close_values[_j - len(_open_timings)], "VALUE", int(str(_close_values[_j - len(_open_timings)]), 16)
               self.radio_master_hid.set_shutter_value(_user.glasses_id, _j, int(str(_close_values[_j - len(_open_timings)]), 16))
               _j += 1

            # assign user to slot instances
            for _k in range(_start_i, _end_i + 1):
              _slot_instances[_k].assign_user(_user)

            _i += 1
          else:
            # mono display - open shutters
            _start_i = copy(_i)
            _i += (_number_of_slots - 1)
            _end_i = copy(_i)

            # assign user to slot instances
            for _k in range(_start_i, _end_i + 1):
              _slot_instances[_k].assign_user(_user)

            _i += 1
        else:
          # no slots assigned to user - open shutters
          break

      self.radio_master_hid.send_shutter_config()
      print "Shutter configuration successfully sent"