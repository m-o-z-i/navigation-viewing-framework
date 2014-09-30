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
  
  _dtrack.stations[4] = avango.daemon.Station('tracking-lcd-glasses-1')        # glasses powerwall user one
  _dtrack.stations[3] = avango.daemon.Station('tracking-lcd-glasses-2')        # glasses powerwall user two


  device_list.append(_dtrack)
  print("ART Tracking started at LCD WALL")

## Initializes AR Track on DLP wall.
def init_dlp_wall_tracking():

  # create instance of DTrack
  _dtrack = avango.daemon.DTrack()
  _dtrack.port = "5002" # ART port at DLP wall
  
  _dtrack.stations[1] = avango.daemon.Station('tracking-dlp-glasses-1')
  _dtrack.stations[2] = avango.daemon.Station('tracking-dlp-glasses-2')
  _dtrack.stations[3] = avango.daemon.Station('tracking-dlp-glasses-3')
  _dtrack.stations[4] = avango.daemon.Station('tracking-dlp-glasses-4')
  _dtrack.stations[5] = avango.daemon.Station('tracking-dlp-glasses-5')
  _dtrack.stations[6] = avango.daemon.Station('tracking-dlp-glasses-6')    

  device_list.append(_dtrack)
  print("ART Tracking started at DLP WALL")


## Initializes PST Tracking.
def init_pst_tracking():

	# create instance of DTrack
	pst = avango.daemon.DTrack()
	pst.port = "5004" # PST port

	pst.stations[1] = avango.daemon.Station('tracking-pst-glasses-1')

	device_list.append(pst)

	print("PST Tracking started!")

## @var device_list
# List of devices to be handled by daemon.
device_list = []

# initialize trackings
init_lcd_wall_tracking()
init_dlp_wall_tracking()
init_pst_tracking()

avango.daemon.run(device_list)
