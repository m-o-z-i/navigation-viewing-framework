#!/usr/bin/python

## @file
# Contains class RecorderPlayer

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ConsoleIO import *
import Tools

# import python libraries
import time
import math
import copy
from os import listdir

## Class to record paths of scenegraph nodes over a specific timespan. Can record the whole
# path or just keyframes. An attached player can reproduce recorded paths for the scenegraph nodes.
# Either interpolated between the checkpoints, or by jumping directly to them.
class RecorderPlayer(avango.script.Script):

  # input fields
  ## @var sf_record_key
  # Boolean field to indicate if the record key was pressed.
  sf_record_key = avango.SFBool()

  ## @var sf_save_key
  # Boolean field to indicate if the save key was pressed.
  sf_save_key = avango.SFBool()

  ## @var sf_trigger_key
  # Boolean field to indicate if the keyframe triggering key was pressed.
  sf_trigger_key = avango.SFBool()

  ## @var sf_play_mode_key
  # Boolean field to indicate if the play mode changing key was pressed.
  sf_play_mode_key = avango.SFBool()

  ## @var sf_record_mode_key
  # Boolean field to indicate if the play mode changing key was pressed.
  sf_record_mode_key = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(RecorderPlayer).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH_NODE The scenegraph node to be recorded and played.
  # @param NAVIGATION If a Navigation instance to be updated belongs to the node, it can be specified here. None otherwise.
  # @param SF_RECORD_KEY Boolean field containing the record key values.
  # @param SF_SAVE_KEY Boolean field containing the save key values.
  # @param SF_TRIGGER_KEY Boolean field containing the keyframe trigger key values.
  # @param SF_PLAY_MODE_CHANGE Boolean field containing the play mode key values.
  # @param SF_RECORD_MODE_CHANGE Boolean field containing the record mode key values.
  def my_constructor(self
                   , SCENEGRAPH_NODE
                   , NAVIGATION
                   , SF_RECORD_KEY
                   , SF_SAVE_KEY
                   , SF_TRIGGER_KEY
                   , SF_PLAY_MODE_CHANGE
                   , SF_RECORD_MODE_CHANGE):

    # references
    ## @var SCENEGRAPH_NODE
    # The scenegraph node to be recorded and played.
    self.SCENEGRAPH_NODE = SCENEGRAPH_NODE

    ## @var NAVIGATION
    # If a Navigation instance to be updated belongs to the node, it can be specified here. None otherwise.
    self.NAVIGATION = NAVIGATION

    # variables
    ## @var recordings_list
    # List of all the recordings captured or loaded for this scenegraph node.
    self.recordings_list = []

    ## @var recording_list
    # Currently loaded recording to be played. List of waypoints and timestamps.
    self.recording_list = []

    ## @var recorder_start_time
    # Point in time when a recording was started.
    self.recorder_start_time = None

    ## @var in_keyframe_recording
    # Boolean indicating if a recording in keyframe mode is currently in progress.
    self.in_keyframe_recording = False

    ## @var player_start_time
    # Point in time when the player was started.
    self.player_start_time = None

    ## @var play_index
    # Index of the current waypoint in the recording currently played by the player.
    self.play_index = 0

    ## @var playing_time
    # Variable used to store the point in time when an animation was paused.
    self.playing_time = 0

    ## @var play_reset_flag
    # Boolean indicating if the end of the path to be played was reached.
    self.play_reset_flag = False

    ## @var recording_index
    # Index of the recording currently played by the player.
    self.recording_index = None

    ## @var record_mode
    # String specifying the record mode. ALL_FRAMES records the complete path of the scenegraph node.
    # KEYFRAMES requires the user to explicitly press the trigger key to capture keyframes.
    self.record_mode = "ALL_FRAMES"
    #self.record_mode = "KEYFRAMES"

    ## @var play_mode
    # String specifying the play mode. CONTINUOUS interpolates between the waypoints captured.
    # DISCRETE jumps to the waypoints after the correct amount of time recorded. EQUAL_SPEED uses
    # a fixed speed to interpolate between the frames.
    self.play_mode = "CONTINUOUS"
    #self.play_mode = "DISCRETE"
    #self.play_mode  = "EQUAL_SPEED"

    # init frame callbacks
    ## @var recorder_trigger
    # Callback when a recording is in progress.
    self.recorder_trigger = avango.script.nodes.Update(Callback = self.recorder_callback, Active = False)

    ## @var player_trigger
    # Callback when a playing progress is active.
    self.player_trigger = avango.script.nodes.Update(Callback = self.player_callback, Active = False)

    self.load_recorded_paths()

    # init field connections
    self.sf_record_key.connect_from(SF_RECORD_KEY)
    self.sf_save_key.connect_from(SF_SAVE_KEY)
    self.sf_trigger_key.connect_from(SF_TRIGGER_KEY)
    self.sf_play_mode_key.connect_from(SF_PLAY_MODE_CHANGE)
    self.sf_record_mode_key.connect_from(SF_RECORD_MODE_CHANGE)


  # callbacks
  ## Called whenever sf_record_key changes.
  @field_has_changed(sf_record_key)
  def sf_record_key_changed(self):

    if self.sf_record_key.value == True: # key pressed

      if self.recorder_trigger.Active.value == True:
        self.stop_recorder()

      else:
        self.start_recorder()

  ## Called whenever sf_save_key changes.
  @field_has_changed(sf_save_key)
  def sf_save_key_changed(self):

    if self.sf_save_key.value == True: # key pressed
      self.save_recording()

      print_message("Saving recording " + str(self.recording_index))

  ## Called whenever sf_trigger_key changes.
  @field_has_changed(sf_trigger_key)
  def sf_trigger_key_changed(self):

    if self.sf_trigger_key.value == True and \
       self.in_keyframe_recording:
      
      print "Capture keyframe"
      _time_step = time.time() - self.recorder_start_time
      self.record_parameters(_time_step)

  ## Called whenever sf_play_mode_key changes.
  @field_has_changed(sf_play_mode_key)
  def sf_play_mode_key_changed(self):
    
    self.stop_player()
    self.stop_recorder()

    if self.sf_play_mode_key.value == True:

      if self.play_mode == "CONTINUOUS":
        self.play_mode = "DISCRETE"
        print_message("Play mode switched to DISCRETE.")
      elif self.play_mode == "DISCRETE":
        self.play_mode = "EQUAL_SPEED"
        print_message("Play mode switched to EQUAL_SPEED.")
      else:
        self.play_mode = "CONTINUOUS"
        print_message("Play mode switched to CONTINUOUS.")


  ## Called whenever sf_record_mode_key changes.
  @field_has_changed(sf_record_mode_key)
  def sf_record_mode_key_changed(self):

    self.stop_player()
    self.stop_recorder()
    
    if self.sf_record_mode_key.value == True:

      if self.record_mode == "ALL_FRAMES":
        self.record_mode = "KEYFRAMES"
        print_message("Record mode switched to KEYFRAMES.")
      else:
        self.record_mode = "ALL_FRAMES"
        print_message("Record mode switched to ALL_FRAMES.")

  ## Evaluated every frame when a recording is in progress.
  def recorder_callback(self):

    if self.record_mode == "ALL_FRAMES":
      _time_step = time.time() - self.recorder_start_time
      self.record_parameters(_time_step)

  ## Evaluated every frame when a playing in in progress.
  def player_callback(self):

    _time_step = self.playing_time + (time.time() - self.player_start_time)

    self.play(_time_step)

    if self.play_reset_flag == True:
      self.stop_player()
      self.next_recording()
      self.start_player() # restart player

  # functions
  ## Called when the play key was pressed. Starts or stops the playing progress.
  def play_key(self):

    if len(self.recording_list) > 0:

      if self.player_trigger.Active.value == True:
        self.stop_player()

      else:
        self.start_player()

  ## Switches to the next recording to be played.
  def next_recording(self):

    if self.recording_index != None:

      self.stop_player()
      self.stop_recorder() # evtl. stop recording

      self.recording_index += 1

      if self.recording_index > len(self.recordings_list) - 1:
        self.recording_index = 0

      self.recording_list = self.recordings_list[self.recording_index]

      self.reset_player()

      # set node to new starting position without starting the playing progress
      self.interpolate_between_frames(self.recording_list, 0)

      if self.NAVIGATION != None:
        self.NAVIGATION.trace.clear(self.NAVIGATION.get_current_world_pos())

      print_message("Switch to recording " + str(self.recording_index))

  ## Switches to the next recording to be played.
  def prior_recording(self):

    if self.recording_index != None:

      self.stop_player()
      self.stop_recorder() # evtl. stop recording

      self.recording_index -= 1

      if self.recording_index < 0:
        self.recording_index = len(self.recordings_list) - 1

      self.recording_list = self.recordings_list[self.recording_index]

      self.reset_player()

      # set node to new starting position without starting the playing progress
      self.interpolate_between_frames(self.recording_list, 0)
      
      if self.NAVIGATION != None:
        self.NAVIGATION.trace.clear(self.NAVIGATION.get_current_world_pos())

      print_message("Switch to recording " + str(self.recording_index))

  ## Loads all the paths for the handled scenegraph node from the path_recordings directory.
  def load_recorded_paths(self):

    _entries = listdir("recordings/paths/")

    for _entry in _entries:

      if _entry.endswith("~"):
        continue

      _path = "recordings/paths/{0}".format(_entry)

      self.load_path_from_file(_path)


    if len(self.recordings_list) > 0:

      self.recording_list = self.recordings_list[0]
      self.recording_index = 0

  ## Loads a single path from a file.
  # @param PATH The path to the file to be loaded.
  def load_path_from_file(self, PATH):

    try:
      _file = open(PATH,"r")
      _lines = _file.readlines()
      _file.close()

    except IOError:
      print_error("Error while loading path description file.", True)

    else: # file succesfully loaded

      # check if the recording is for handled scenegraph node
      if _lines[0].replace("\n", "") != self.SCENEGRAPH_NODE.Path.value:
        #print_warning("Return at " + _lines[0].replace("\n", ""))
        return
      
      # remove scenegraph path from list to parse
      _lines.pop(0)

      _recording_list = []

      for _line in _lines:
        _line = _line.split()

        _time = float(_line[0])
        _pos = avango.gua.Vec3(float(_line[1]), float(_line[2]), float(_line[3]))

        _quat	= avango.gua.make_rot_mat(float(_line[4]), float(_line[5]), float(_line[6]), float(_line[7])).get_rotate()
        #_quat	= avango.gua.Quat(float(_line[4]), avango.gua.Vec3(float(_line[5]), float(_line[6]), float(_line[7]))) # sucks

        _scale = avango.gua.Vec3(float(_line[8]), float(_line[9]), float(_line[10]))

        _recording_list.append( [_time, _pos, _quat, _scale] )

      self.recordings_list.append(_recording_list)

  ## Starts the recording progress for the handled scenegraph node.
  def start_recorder(self):

    print_message("Start recording")

    self.stop_player()

    self.recording_list = [] # clear list

    self.recorder_start_time = time.time()

    if self.record_mode == "KEYFRAMES":
      _time_step = time.time() - self.recorder_start_time
      self.record_parameters(_time_step)
      self.in_keyframe_recording = True

    self.recorder_trigger.Active.value = True # activate recorder callback

  ## Stops the recording progress for the handled scenegraph node.
  def stop_recorder(self):

    if self.recorder_trigger.Active.value == True:

      if self.record_mode == "KEYFRAMES":
        _time_step = time.time() - self.recorder_start_time
        self.record_parameters(_time_step)
        self.in_keyframe_recording = True

      print_message("Stop recording of " + str(len(self.recording_list)) + " control points.")

      self.recorder_trigger.Active.value = False # deactivate recorder callback

      self.recorder_start_time = None
      self.in_keyframe_recording = False

  ## Saves the recording captured.
  def save_recording(self):

    self.recording_index = len(self.recordings_list)

    _path = self.SCENEGRAPH_NODE.Path.value
    _path = _path.replace("/", "-")

    _name = "recordings/paths/" + _path +"_path_" + str(self.recording_index)
    _file = open(_name,"w")

    _recording_list = []

    _file.write(self.SCENEGRAPH_NODE.Path.value + "\n")

    for _tupel in self.recording_list:
      _recording_list.append(_tupel)

      _time = _tupel[0]
      _pos = _tupel[1]
      _quat = _tupel[2]
      _scale = _tupel[3]

      _file.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n".format(
        _time, _pos.x, _pos.y, _pos.z, _quat.get_angle(), _quat.get_axis().x, _quat.get_axis().y, _quat.get_axis().z, _scale.x, _scale.y, _scale.z
      ))

    _file.close()

    self.recordings_list.append(_recording_list)

  ## Records the current parameters of the scenegraph node and stores it together with the current time step.
  # @param TIME_STEP The current point in time to be stored with the parameters.
  def record_parameters(self, TIME_STEP):

    _mat = self.SCENEGRAPH_NODE.Transform.value

    self.recording_list.append( [TIME_STEP, _mat.get_translate(), _mat.get_rotate(), _mat.get_scale()] )

  ## Starts the player.
  def start_player(self):

    print_message("Start playing")

    if self.play_mode == "EQUAL_SPEED":
      _velocity = 1 # in m/s

      ## @var mod_recording_list
      # Copied recording_list with adapted time stamps for equal speed playing.
      self.mod_recording_list = self.unshared_copy(self.recording_list)

      _current_time = 0.0
      self.mod_recording_list[0][0] = 0.0
      
      for _i in range(1, len(self.mod_recording_list)):
        _pos_last = self.mod_recording_list[_i-1][1]
        _pos_curr = self.mod_recording_list[_i][1]
        _distance = Tools.euclidean_distance(_pos_last, _pos_curr)
        self.mod_recording_list[_i][0] = _current_time + (_distance * 1/_velocity)
        _current_time += (_distance * 1/_velocity)
    

    self.play_reset_flag = False

    self.player_start_time = time.time()

    self.player_trigger.Active.value = True # activate player callback

  ## Returns a deep copy without references of a given list.
  # @param IN_LIST The list to be copied.
  def unshared_copy(self, IN_LIST):
    
    if isinstance(IN_LIST, list):
        return list( map(self.unshared_copy, IN_LIST) )
    return IN_LIST

  ## Stops the player.
  def stop_player(self):

    if self.player_trigger.Active.value == True:
      print_message("Stop playing")

      self.playing_time += time.time() - self.player_start_time

      self.player_trigger.Active.value = False # deactivate player callback

  ## Resets the player to the next recording when one animation is done.
  def reset_player(self):

    if len(self.recording_list) > 0:
      print_message("Reset player")

      self.play_index = 0
      self.playing_time = 0

      _values = self.recording_list[0]
      _pos		= _values[1]
      _quat		= _values[2]
      _scale  = _values[3]

      _mat =  avango.gua.make_trans_mat(_pos) * \
              avango.gua.make_rot_mat(_quat.get_angle(), _quat.get_axis().x, _quat.get_axis().y, _quat.get_axis().z) * \
              avango.gua.make_scale_mat(_scale)

      self.SCENEGRAPH_NODE.Transform.value = _mat


  ## Sets the matrix of the handled scenegraph node according to the current recording.
  # @param TIME_STEP The point in time to which the node is set.
  def play(self, TIME_STEP):

    _recording_to_play = []

    if self.play_mode == "EQUAL_SPEED":
      _recording_to_play = self.mod_recording_list
    else:
      _recording_to_play = self.recording_list


    if self.play_index != None:

      _last_recorded_time_step = _recording_to_play[-1][0]

      if TIME_STEP > _last_recorded_time_step:
        self.play_reset_flag = True # object has finished it's animation

      else:
        _time_step1 = _recording_to_play[self.play_index][0]

        if TIME_STEP >= _time_step1:

          for _index in range(self.play_index, len(_recording_to_play)):
            _time_step2 = _recording_to_play[_index+1][0]
            _time_step1 = _recording_to_play[_index][0]

            if TIME_STEP <= _time_step2:
              self.play_index = _index

              _factor = (TIME_STEP - _time_step1) / (_time_step2 - _time_step1)
              _factor = max(0.0,min(_factor,1.0))

              if self.play_mode == "DISCRETE":
                if _factor < 0.5:
                  _factor = 0.0
                else:
                  _factor = 1.0

              self.interpolate_between_frames(_recording_to_play, _factor) # interpolate position and orientation and scale

              if self.NAVIGATION != None and TIME_STEP < 0.1:
                self.NAVIGATION.trace.clear(self.NAVIGATION.get_current_world_pos())

              break

  ## Interpolates between the two frames at play_index and play_index + 1.
  # @param RECORDING_TO_PLAY The recording list to be played.
  # @param FACTOR The factor to interpolate to between frames. [0; 1]
  def interpolate_between_frames(self, RECORDING_TO_PLAY, FACTOR):

    _tupel1 = RECORDING_TO_PLAY[self.play_index]
    _pos1 = _tupel1[1]
    _quat1 = _tupel1[2]
    _scale1 = _tupel1[3]

    _tupel2 = RECORDING_TO_PLAY[self.play_index+1]
    _pos2	= _tupel2[1]
    _quat2 = _tupel2[2]
    _scale2 = _tupel2[3]

    _new_pos = _pos1.lerp_to(_pos2, FACTOR)
    _new_quat = _quat1.slerp_to(_quat2, FACTOR)
    _new_scale = _scale1.lerp_to(_scale2, FACTOR)

    _new_mat =  avango.gua.make_trans_mat(_new_pos) * \
                avango.gua.make_rot_mat(_new_quat.get_angle(), _new_quat.get_axis().x, _new_quat.get_axis().y, _new_quat.get_axis().z) * \
                avango.gua.make_scale_mat(_new_scale)

    self.SCENEGRAPH_NODE.Transform.value = _new_mat

    if self.NAVIGATION != None:
      self.NAVIGATION.inputmapping.set_abs_mat(_new_mat)

## Class to build all the RecorderPlayer instances for all the scenegraph nodes to be handled.
class AnimationManager(avango.script.Script):

  # input fields
  ## @var sf_record
  # Boolean field to indicate if the record key was pressed.
  sf_record = avango.SFBool()

  ## @var sf_save
  # Boolean field to indicate if the save key was pressed.
  sf_save = avango.SFBool()

  ## @var sf_play
  # Boolean field to indicate if the play key was pressed.
  sf_play = avango.SFBool()

  ## @var sf_next
  # Boolean field to indicate if the next recording key was pressed.
  sf_next = avango.SFBool()

  ## @var sf_prior
  # Boolean field to indicate if the prior recording key was pressed.
  sf_prior = avango.SFBool()

  ## @var sf_trigger
  # Boolean field to indicate if the keyframe trigger key was pressed.
  sf_trigger = avango.SFBool()

  ## @var sf_play_mode_change
  # Boolean field to indicate if the play mode key was pressed.
  sf_play_mode_change = avango.SFBool()

  ## @var sf_record_mode_change
  # Boolean field to indicate if the record mode key was pressed.
  sf_record_mode_change = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(AnimationManager).__init__()

  ## Custom constructor.
  # @param SCENEGRAPH_NODE_LIST List of scenegraph nodes to be handled for animations.
  # @param NAVIGATION_LIST Navigation instances associated to the scenegraph nodes. If no instance is associated, 
  #                        None is given in the list.
  def my_constructor(self, SCENEGRAPH_NODE_LIST, NAVIGATION_LIST):
 
    ## @var keyboard_sensor
    # Daemon sensor representing the inputs from the keyboard.
    self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.keyboard_sensor.Station.value = "device-keyboard0"
        
    # init field connections
    self.sf_play.connect_from(self.keyboard_sensor.Button21) # F3
    
    self.sf_next.connect_from(self.keyboard_sensor.Button22) # F4
    self.sf_prior.connect_from(self.keyboard_sensor.Button23) # F5

    self.sf_record.connect_from(self.keyboard_sensor.Button24) # F6
    self.sf_save.connect_from(self.keyboard_sensor.Button25) # F7

    self.sf_trigger.connect_from(self.keyboard_sensor.Button20) # F2

    self.sf_play_mode_change.connect_from(self.keyboard_sensor.Button28) # F10
    self.sf_record_mode_change.connect_from(self.keyboard_sensor.Button29) # F11

    ## @var path_recorder_players
    # List of RecorderPlayer instances that were created.
    self.path_recorder_players = []

    for _i in range(len(SCENEGRAPH_NODE_LIST)):
      _path_recorder_player = RecorderPlayer()
      _path_recorder_player.my_constructor(SCENEGRAPH_NODE_LIST[_i]
                                             , NAVIGATION_LIST[_i]
                                             , self.sf_record
                                             , self.sf_save
                                             , self.sf_trigger
                                             , self.sf_play_mode_change
                                             , self.sf_record_mode_change)
      self.path_recorder_players.append(_path_recorder_player)


  ## Called whenever sf_play changes.
  @field_has_changed(sf_play)
  def sf_play_changed(self):

    if self.sf_play.value == True: # button pressed
      
      self.play_key()

  ## Called whenever sf_next changes.
  @field_has_changed(sf_next)
  def sf_next_changed(self):

    if self.sf_next.value == True: # button pressed

      for _path_recorder_player in self.path_recorder_players:
        _path_recorder_player.next_recording()


  ## Called whenever sf_prior changes.
  @field_has_changed(sf_prior)
  def sf_prior_changed(self):

    if self.sf_prior.value == True: # button pressed

      for _path_recorder_player in self.path_recorder_players:
        _path_recorder_player.prior_recording()


  ## Calls the play function in all RecorderPlayer instances created.
  def play_key(self):

    for _path_recorder_player in self.path_recorder_players:
      _path_recorder_player.play_key()
