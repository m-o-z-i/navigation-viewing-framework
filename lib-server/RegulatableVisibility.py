#!/usr/bin/python

## @file
# Contains interface RegulatableVisibility.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script


## Function interface to be implemented by all entities
# whose visibilities should be regulated in different display groups.
class RegulatableVisibility(avango.script.Script):

  ## Base constructor.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def table_constructor(self, VISIBILITY_TABLE):

    self.visibility_table = VISIBILITY_TABLE

  ## Triggers the correct GroupNames of all instances at a display group.
  # @param DISPLAY_GROUP_ID The ID of the display group to set new GroupNames for.
  def trigger_visibilities_at(self, DISPLAY_GROUP_ID):

    raise NotImplementedError( "To be implemented by a subclass." )