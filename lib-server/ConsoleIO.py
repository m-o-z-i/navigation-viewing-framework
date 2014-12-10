#!/usr/bin/python

## @file
# Contains functions for console inputs and outputs.

# import python libraries
import inspect
import sys

# color definitions
color_reset = '\033[0m'
color_warning = '\033[1;93m'
color_error = '\033[1;91m'
color_message = '\033[1;92m'
color_headline = '\033[1;94m'

## Prints a colored warning message on the console.
# @param MESSAGE The message to be printed.
def print_warning(MESSAGE):
  _calling_filename = get_calling_filename()
  print((color_warning + "[" + _calling_filename + ".py] " + MESSAGE + color_reset))
  print("")

## Prints a colored error message on the console and ends the application optionally.
# @param MESSAGE The message to be printed.
# @param TERMINATE Boolean saying if the application is to be terminated.
def print_error(MESSAGE, TERMINATE):
  _calling_filename = get_calling_filename()
  print((color_error + "[" + _calling_filename + ".py] " + MESSAGE + color_reset))
  print("")
  
  if TERMINATE:
    sys.exit()


## Prints a colored information message on the console.
# @param MESSAGE The message to be printed.
def print_message(MESSAGE):
  _calling_filename = get_calling_filename()
  print((color_message + "[" + _calling_filename + ".py] " + MESSAGE + color_reset))
  print("")

## Prints a colored headline on the console.
# @param MESSAGE The message to be printed.
def print_headline(MESSAGE):
  _calling_filename = get_calling_filename()
  print((color_headline + "\n==================================================================================="))
  print(("[" + _calling_filename + ".py] " + MESSAGE))
  print(("===================================================================================\n" + color_reset))

## Prints a subheadline on the console.
# @param MESSAGE The message to be printed.
def print_subheadline(MESSAGE):
  _line_string = ""

  for i in range(len(MESSAGE)):
    _line_string += "-"

  print((MESSAGE + "\n" + _line_string))

## Gets the filename from which one of the print functions was called.
def get_calling_filename():
  frm = inspect.stack()[2]
  mod = inspect.getmodule(frm[0])
  return mod.__name__