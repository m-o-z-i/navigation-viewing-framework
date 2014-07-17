#!/usr/bin/python


# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import python libraries
import math

class FrameUpdate:

  # constructor
  def __init__(self):

    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = False)


  # callbacks
  def frame_callback(self):
    pass

  # functions  
  def enable(self, FLAG):
    
    self.frame_trigger.Active.value = FLAG



class FrameRotationUpdate(FrameUpdate):

  def __init__(self, SF_MAT, ROTATION_VELOCITY, ROTATION_AXIS):
    FrameUpdate.__init__(self)

    self.SF_MAT = SF_MAT

    self.rotation_velocity = ROTATION_VELOCITY / 60.0
    self.rotation_axis = ROTATION_AXIS

    self.enable(True)


  # callbacks
  def frame_callback(self):

    self.SF_MAT.value = self.SF_MAT.value * avango.gua.make_rot_mat(self.rotation_velocity, self.rotation_axis)



class FrameSineTranslationUpdate(FrameUpdate):

  def __init__(self, SF_MAT, TRANSLATION_VELOCITY, TRANSLATION_AXIS):
    FrameUpdate.__init__(self)

    self.SF_MAT = SF_MAT

    self.translation_velocity = TRANSLATION_VELOCITY / 60.0
    self.translation_axis = TRANSLATION_AXIS

    self.counter = 0.0
    self.start_pos = self.SF_MAT.value.get_translate()

    self.enable(True)


  # callbacks
  def frame_callback(self):

    self.counter += self.translation_velocity
    
    _new_pos = self.start_pos + self.translation_axis * math.sin(self.counter)

    _mat = self.SF_MAT.value
    _mat.set_translate(_new_pos)
    
    self.SF_MAT.value = _mat


class FrameSineScaleUpdate(FrameUpdate):

  def __init__(self, SF_MAT, SCALE_VELOCITY, SCALE_AXIS):
    FrameUpdate.__init__(self)

    self.SF_MAT = SF_MAT

    self.scale_velocity = SCALE_VELOCITY / 60.0
    self.scale_axis = SCALE_AXIS

    self.counter = 0.0
    self.start_scale = self.SF_MAT.value.get_scale()

    self.enable(True)


  # callbacks
  def frame_callback(self):

    self.counter += self.scale_velocity

    #_new_scale = self.start_scale + self.scale_axis * math.sin(self.counter)
    _new_scale = self.start_scale * (avango.gua.Vec3(1.0,1.0,1.0) + self.scale_axis * math.sin(self.counter))
       
    _mat = self.SF_MAT.value
    _mat = avango.gua.make_trans_mat(_mat.get_translate()) * \
            avango.gua.make_rot_mat(_mat.get_rotate_scale_corrected()) * \
            avango.gua.make_scale_mat(_new_scale)

    self.SF_MAT.value = _mat
    


'''
## Helper class to update material values with respect to the current time.
class TimedMaterialUniformUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in milliseconds.
  TimeIn = avango.SFFloat()

  ## @var MaterialName
  # Field containing the name of the material to be updated
  MaterialName = avango.SFString()

  ## @var UniformName
  # Field containing the name of the uniform value to be updated
  UniformName = avango.SFString()

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    avango.gua.set_material_uniform(self.MaterialName.value,
                                    self.UniformName.value,
                                    self.TimeIn.value)


## Helper class to get a rotation that alternates with respect to the current time.
class TimedSwayingUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in seconds.
  TimeIn = avango.SFFloat()

  ## @var SFRotMat
  # Field containing the rotation being calculated by this class.
  SFRotMat = avango.gua.SFMatrix4()

  # parameters
  ## @var max_rot_offset
  # Maximum rotation in degrees
  max_rot_offset = 1.0 

  ## @var frequency
  # Frequency to be applied.
  frequency      = 0.1

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    #calculate rotation of the ship
    self.SFRotMat.value = avango.gua.make_rot_mat( self.max_rot_offset * math.sin( (20 * self.frequency * self.TimeIn.value) / math.pi ),
                          0, 0, 1)


## Helper class to create a rotation matrix with resepect to the current time.
class DayAnimationUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containting the current time in seconds.
  TimeIn = avango.SFFloat()

  ## @var sf_sun_mat
  # Field containing the calculated rotation matrix for the sun.
  sf_sun_mat = avango.gua.SFMatrix4()

  ## @var day_time
  # The length of one day in seconds.
  day_time = 5 * 30.0

  ## @var morning_sun_color
  # The color of the sun at sunrise.
  morning_sun_color = avango.gua.Color(0.9, 0.65, 0.65)

  ## @var noon_sun_color
  # The color of the sun at noon.
  noon_sun_color = avango.gua.Color(1.0, 0.8, 0.8)

  ## @var evening_sun_color
  # The color of the sun at sunset.
  evening_sun_color = morning_sun_color

  ## @var sf_sun_color
  # The color of the sun.
  sf_sun_color = avango.gua.SFColor()
  sf_sun_color.value = morning_sun_color

  ## Linearly interpolates between two colors according to a given ratio.
  # @param START_COLOR The starting value for a ratio of 0.
  # @param TARGET_COLOR The final value for a ratio of 1.
  # @param RATIO A value between 0 and 1 that determines the interpolated result.
  def lerp_color(self, START_COLOR, TARGET_COLOR, RATIO):
    _start_vec  = avango.gua.Vec3(START_COLOR.r, START_COLOR.g, START_COLOR.b)
    _end_vec    = avango.gua.Vec3(TARGET_COLOR.r, TARGET_COLOR.g, TARGET_COLOR.b)
    _lerp_vec   = _start_vec.lerp_to(_end_vec, RATIO)
    return avango.gua.Color(_lerp_vec.x, _lerp_vec.y, _lerp_vec.z)

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):

    # set position of the sun
    _sun_angle = ((self.TimeIn.value % self.day_time) / self.day_time) * 360.0

    self.sf_sun_mat.value =  avango.gua.make_rot_mat(-_sun_angle, 1, 0, 0) * \
                             avango.gua.make_rot_mat(-30.0, 0, 1, 0)

    # update the sun color
    # between morning and noon
    if _sun_angle < 45:  
      self.sf_sun_color.value = self.lerp_color(self.morning_sun_color, self.noon_sun_color, _sun_angle / 45.0)
    # between noon and evening
    elif (_sun_angle > 135) and (_sun_angle < 180): 
      self.sf_sun_color.value = self.lerp_color(self.noon_sun_color, self.evening_sun_color, (_sun_angle - 135.0) / 45.0)

'''      
    
