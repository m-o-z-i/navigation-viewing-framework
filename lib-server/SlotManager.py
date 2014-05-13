#!/usr/bin/python

## @file
# Contains class SlotManager.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
import RadioMasterHID

# import framework libraries
from ConsoleIO   import *

# import python libraries
from copy import copy
import atexit

# @var total_number_of_shutter_glasses
total_number_of_shutter_glasses = 6

## Class to handle shutter configurations and timings. Associates the users per display to
# the available slots and sets the glasses correctly.
class SlotManager(avango.script.Script):

  ## Default constructor
  def __init__(self):
    self.super(SlotManager).__init__()
    self.always_evaluate(True)

    ##
    #
    self.glasses_slot_status = []
    for i in range(total_number_of_shutter_glasses):
      self.glasses_slot_status.append(0)

  ## Custom constructor.
  # @param USER_LIST Reference to a list of all users in the setup.
  def my_constructor(self, USER_LIST):

    ## @var users
    # Reference to a list of all users to be handled in the setup.
    self.users = USER_LIST

    ## @var slots
    # Dictionary to map Display instances to a list of associated Slot instances.
    self.slots = dict()

    ## @var queued_commands
    # Format: [string list, frames] A list of commands in string form that are executed in x frames in the future.
    self.queued_commands = []

    ## @var radio_master_hid
    # Instance of RadioMasterHID to handle shutter glass configurations.
    self.radio_master_hid = RadioMasterHID.RadioMaster()

    print_headline("Initializing RadioMasterHID")

    # Open HID shutter communication device
    _open_hid_output = self.radio_master_hid.openHID()

    if _open_hid_output.startswith("error"):
      print_error("openHID() - " + _open_hid_output, False)
    else:
      print_message("openHID() - " + _open_hid_output)

    # reset to default shutter configuration and register reset function on close
    self.reset_shutter_config("/opt/shutterConfig/DLP_1vip456_2tv3tv.xml")
    atexit.register(self.reset_shutter_config, INITIAL_CONFIGURATION = "/opt/shutterConfig/DLP_1vip456_2tv3tv.xml")
    self.print_uploaded_shutter_config()

  ## Loads an XML shutter configuration and uploads it.
  def reset_shutter_config(self, INITIAL_CONFIGURATION):

    # load initial shutter configuration
    _load_config_output = self.radio_master_hid.load_config(INITIAL_CONFIGURATION)

    if _load_config_output != 0:
      print_error("load_config() - Failed to load shutter configuration " + INITIAL_CONFIGURATION, False)
    else:
      print_message("load_config() - Loaded shutter configuration " + INITIAL_CONFIGURATION)

    # send initial shutter configuration
    self.send_shutter_config()

    # set and send master configuration settings
    self.radio_master_hid.set_master_transmit(1)
    self.radio_master_hid.set_master_clock(1) # 0 = use internal sync signal; 1 = use external sync signal
    self.radio_master_hid.set_master_timing(16600,16500)
    self.radio_master_hid.send_master_config() 

    #self.print_uploaded_shutter_config()

  ## Tells the RadioMasterHID to send the shutter configuration. Formats feedback nicely.
  def send_shutter_config(self):
    _send_output = self.radio_master_hid.send_shutter_config()

    if _send_output.startswith("error"):
      print_error("send_shutter_config() - " + _send_output, False)
    else:
      print_message("send_shutter_config() - " + _send_output)

    self.print_uploaded_shutter_config()

  ## Prints the currently uploaded shutter configuration including timings and values.
  def print_uploaded_shutter_config(self):

    print_headline("Currently uploaded shutter configuration")

    print "Ext clock:", self.radio_master_hid.get_master_clock(), "Transmit:", self.radio_master_hid.get_master_transmit()
    print "Timings:", self.radio_master_hid.get_master_period(), self.radio_master_hid.get_master_offset(), "\n"

    ids = list(self.radio_master_hid.get_ids())
    for _id in ids:
      print_subheadline("Shutter " + str(_id) + " " + str(self.radio_master_hid.get_description(_id)) + " " + str(hex(self.radio_master_hid.get_init_value(_id)) + ":"))
      ec = self.radio_master_hid.get_event_count(_id)
      for e in range(ec):
        print self.radio_master_hid.get_timer_value(_id, e), hex(self.radio_master_hid.get_shutter_value(_id, e))
      print " "

    print self.glasses_slot_status


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


  ## Evaluated every frame.
  def evaluate(self):
    for _entry in self.queued_commands:
      _entry[1] -= 1

      if _entry[1] == 0:
        
        for _command in _entry[0]:
          try:
            eval(_command)
          except:
            print_error("Could not execute command " + _entry[0], False)

        self.send_shutter_config()
        self.queued_commands.remove(_entry)

  ## Registers a list of string commands to be executed in some frames in the future.
  # @param COMMAND_LIST A list of strings containing the commands.
  # @param FRAMES Number of frames in which the commands are to be executed.
  def queue_commands(self, COMMAND_LIST, FRAMES):
    self.queued_commands.append([COMMAND_LIST, FRAMES])


  ## Updates the shutter timings and scenegraph slot connections according to the
  # vip / active status, display and platform of users.
  def update_slot_configuration(self):
 
    # List to save for which glasses a configuration was set
    _glasses_updated = []
    for _i in range(total_number_of_shutter_glasses):
      _glasses_updated.append(False)
      self.radio_master_hid.set_shutter_const(_i + 1, int("22", 16), 1)  # activate all shutter glasses

    
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
      print_headline("User - Slot Assignment on " + str(_display.name))

      # clear all slot connections
      _slot_instances = self.slots[_display]
      for _slot in _slot_instances:
        _slot.clear_user()

      _old_glasses_slot_status = list(self.glasses_slot_status)
      for _state in _concatenated_user_list:
        print "User", _state[0].id, "(VIP:", str(_state[0].is_vip) + ") was assigned " + str(_state[1]) + " slots."
        self.glasses_slot_status[_state[0].glasses_id - 1] = _state[1]

      _i = 0
      for _state in _concatenated_user_list:

        _user = _state[0]
        _number_of_slots = _state[1]

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

            if _user.glasses_id == None:
              print_warning("Warning: User " + _user.id + " has no glasses id specified.")

            if _user.glasses_id > total_number_of_shutter_glasses:
              print_error("Error at user " + str(_user.id) + ": Glasses ID (" + str(_user.glasses_id) + ") exceeds the maximum of available glasses (" + str(total_number_of_shutter_glasses) + ")." , True)
            else:
              _glasses_updated[_user.glasses_id - 1] = True

            # set event count properly
            self.radio_master_hid.set_event_count(_user.glasses_id, 2 * len(_open_timings))
            
            # if user glasses are closing, do it immediately
            if self.glasses_slot_status[_user.glasses_id - 1] <= _old_glasses_slot_status[_user.glasses_id - 1]:
              # set ids with shutter timings and values properly
              while _j < len(_open_timings):
                self.radio_master_hid.set_timer_value(_user.glasses_id, _j, _open_timings[_j])
                self.radio_master_hid.set_shutter_value(_user.glasses_id, _j, int(str(_open_values[_j]), 16))
                _j += 1

              while _j < 2 * len(_open_timings):
                 self.radio_master_hid.set_timer_value(_user.glasses_id, _j, _close_timings[_j - len(_open_timings)])
                 self.radio_master_hid.set_shutter_value(_user.glasses_id, _j, int(str(_close_values[_j - len(_open_timings)]), 16))
                 _j += 1
            # if the user glasses are opening, wait for some frames
            else:
              # set ids with shutter timings and values properly
              _command_list = []
              while _j < len(_open_timings):
                _command_list.append("self.radio_master_hid.set_timer_value(" + str(_user.glasses_id) + "," + str(_j) + "," + str(_open_timings[_j]) + ")")
                #_command_list.append("self.radio_master_hid.set_shutter_value(" + str(_user.glasses_id) + "," + str(_j) + "," + str(int(str(_open_values[_j]), 16)) + ")")
                self.radio_master_hid.set_shutter_value(_user.glasses_id, _j, int(str(_open_values[_j]), 16))
                _j += 1

              while _j < 2 * len(_open_timings):
                 _command_list.append("self.radio_master_hid.set_timer_value(" + str(_user.glasses_id) + "," + str(_j) + "," + str(_close_timings[_j - len(_open_timings)]) + ")")
                 #_command_list.append("self.radio_master_hid.set_shutter_value(" + str(_user.glasses_id) + "," + str(_j) + "," + str(int(str(_close_values[_j - len(_open_timings)]), 16)) + ")")
                 self.radio_master_hid.set_shutter_value(_user.glasses_id, _j, int(str(_close_values[_j - len(_open_timings)]), 16))
                 _j += 1

              self.queue_commands(_command_list, 10)

            # assign user to slot instances
            for _k in range(_start_i, _end_i + 1):
              _slot_instances[_k].assign_user(_user)

            _i += 1
          else:
            # mono display
            _start_i = copy(_i)
            _i += (_number_of_slots - 1)
            _end_i = copy(_i)

            # assign user to slot instances
            for _k in range(_start_i, _end_i + 1):
              _slot_instances[_k].assign_user(_user)

            _i += 1
 
    # open glasses for which no timings were assigned
    print_headline("Send updated shutter configuration")

    for _i in range(total_number_of_shutter_glasses):
      if _glasses_updated[_i] == False:
        print_warning("Opening shutter glasses " + str(_i + 1))
        self.radio_master_hid.set_shutter_const(_i + 1, int("88", 16), 1)

    self.send_shutter_config()