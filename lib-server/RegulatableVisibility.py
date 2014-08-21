#!/usr/bin/python

## @file
# Contains interface RegulatableVisibility.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script


##
class RegulatableVisibility(avango.script.Script):

  ## Base constructor.
  # @param
  def table_constructor(self, VISIBILITY_TABLE):

    self.visibility_table = VISIBILITY_TABLE

  ## Triggers the correct GroupNames of all instances at a display group.
  def trigger_visibilities_at(self, DISPLAY_GROUP_ID):

    raise NotImplementedError( "To be implemented by a subclass." )