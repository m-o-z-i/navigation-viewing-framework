
import os
import subprocess
import sys

def start():

  _name = ""

  for i in range(1, len(sys.argv)):
    _name = _name + " " + sys.argv[i]

  _name = _name[1:]
  print get_event_string(_name)

def get_event_string(DEVICE_NAME):

  device_file = subprocess.Popen(["cat", "/proc/bus/input/devices"], stdout=subprocess.PIPE).communicate()[0]
  device_file = device_file.split("\n")

  indices = []

  for _line in device_file:
    
    if DEVICE_NAME in _line:
      index = device_file.index(_line)
      indices.append(index)

  if indices == []:
    return ""

  else:

    _output = ""

    for _index in indices:
      _event_string_start_index = device_file[_index+4].find('event')

      _output = _output + "/dev/input/" + device_file[_index+4][_event_string_start_index:].split(" ")[0]
      _output += "\n"

    _output = _output[:-1]
    return _output

if __name__ == '__main__':
  start()
