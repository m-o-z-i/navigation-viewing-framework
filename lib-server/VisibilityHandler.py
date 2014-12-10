#!/usr/bin/python

## @file
# Contains interfaces VisibilityHandler1D and VisibilityHandler2D.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script

## Function interface to be implemented by all entities
# whose visibilities should be regulated in different display groups.
class VisibilityHandler1D(avango.script.Script):

  ## Base constructor.
  # @param VISIBILITY_LIST A list containing visibility rules according to the DisplayGroups' visibility tags. 
  def list_constructor(self, VISIBILITY_LIST):

    ## @var visibility_list
    # A list containing visibility rules according to the DisplayGroups' visibility tags. 
    self.visibility_list = VISIBILITY_LIST

  ## Triggers the correct GroupNames for the different DisplayGroups.
  def handle_correct_visibility_groups(self):

    raise NotImplementedError( "To be implemented by a subclass." )

## Function interface to be implemented by all entities
# whose representation visibilities should be regulated in different display groups.
class VisibilityHandler2D(avango.script.Script):

  ## Base constructor.
  # @param VISIBILITY_TABLE A matrix containing visibility rules according to the DisplayGroups' visibility tags. 
  def table_constructor(self, VISIBILITY_TABLE):

    ## @var visibility_table
    # A matrix containing visibility rules according to the DisplayGroups' visibility tags.
    self.visibility_table = VISIBILITY_TABLE

  ## Triggers the correct GroupNames of all instances at a display group.
  # @param DISPLAY_GROUP The display group to set new GroupNames for.
  def handle_correct_visibility_groups_for(self, DISPLAY_GROUP):

    raise NotImplementedError( "To be implemented by a subclass." )