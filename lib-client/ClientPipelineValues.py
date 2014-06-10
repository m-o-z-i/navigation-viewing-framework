#!/usr/bin/python

## @file
# Contains function for setting common pipeline values for users.

# import avango-guacamole libraries
import avango
import avango.gua

## Sets all the pipeline values to obtain a nice appearance.
def set_default_pipeline_values(PIPELINE):

  avango.gua.create_texture("data/textures/sky.jpg")
  PIPELINE.BackgroundTexture.value = "data/textures/sky.jpg"

  PIPELINE.EnableBloom.value              = False
  PIPELINE.BloomIntensity.value           = 0.1
  PIPELINE.BloomThreshold.value           = 1.0
  PIPELINE.BloomRadius.value              = 10
  PIPELINE.EnableFXAA.value               = False
  PIPELINE.EnableFog.value                = True
  PIPELINE.FogStart.value                 = 300.0
  PIPELINE.FogEnd.value                   = 500.0
  PIPELINE.EnableFrustumCulling.value     = False
  PIPELINE.AmbientColor.value             = avango.gua.Color(0.25, 0.25, 0.25)
  PIPELINE.FarClip.value                  = 1000.0
  PIPELINE.EnableBackfaceCulling.value    = Falsey^
  PIPELINE.EnableSsao.value               = False
  PIPELINE.SsaoRadius.value               = 2.0
  PIPELINE.SsaoIntensity.value            = 2.0
  PIPELINE.EnableFPSDisplay.value         = True
  PIPELINE.BackgroundMode.value           = avango.gua.BackgroundMode.SKYMAP_TEXTURE
  PIPELINE.FogTexture.value               = PIPELINE.BackgroundTexture.value
