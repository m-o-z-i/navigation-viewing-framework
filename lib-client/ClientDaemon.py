#!/usr/bin/python

## @file
# avango daemon to initialize tracking and device stations.

# import avango-guacamole libraries
import avango.daemon

# import python libraries
import os
import sys

## Initializes AR Track on LCD wall.
def init_lcd_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5000" # ART port at LCD wall
  
  _dtrack.stations[18] = avango.daemon.Station('tracking-oculus-stripe')   # oculus rift tracking
  _dtrack.stations[17] = avango.daemon.Station('tracking-oculus-front')    # oculus rift tracking
  _dtrack.stations[16] = avango.daemon.Station('tracking-oculus-stag')     # oculus rift tracking

  _dtrack.stations[4] = avango.daemon.Station('tracking-glasses-1')        # glasses powerwall user one
  _dtrack.stations[3] = avango.daemon.Station('tracking-glasses-2')        # glasses powerwall user two

  _dtrack.stations[7] = avango.daemon.Station('tracking-old-spheron')      # old spheron device

  device_list.append(_dtrack)
  print "ART Tracking started at LCD WALL"

## Initializes AR Track on DLP wall.
def init_dlp_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5002" # ART port at LED wall
  
  _dtrack.stations[19] = avango.daemon.Station('tracking-dlp-new-spheron')     # new spheron device

  _dtrack.stations[1] = avango.daemon.Station('tracking-dlp-glasses-1')

  device_list.append(_dtrack)
  print "ART Tracking started at DLP WALL"

## @var device_list
# List of devices to be handled by daemon.
device_list = []

# initialize trackings
init_lcd_wall_tracking()
init_dlp_wall_tracking()

avango.daemon.run(device_list)