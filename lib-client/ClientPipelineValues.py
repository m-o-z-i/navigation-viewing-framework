#!/usr/bin/python

## @file
# Contains function for setting common pipeline values for users.

# import guacamole libraries
import avango
import avango.gua

## Sets all the pipeline values to obtain a nice appearance.
def set_pipeline_values(PIPELINE):
  avango.gua.create_texture("data/textures/sky.jpg")
  PIPELINE.BackgroundTexture.value = "data/textures/sky.jpg"

  PIPELINE.EnableBloom.value              = True
  PIPELINE.BloomIntensity.value           = 0.1
  PIPELINE.BloomThreshold.value           = 1.0
  PIPELINE.BloomRadius.value              = 10
  PIPELINE.EnableFXAA.value               = False
  PIPELINE.EnableFog.value                = True
  PIPELINE.FogStart.value                 = 300.0
  PIPELINE.FogEnd.value                   = 400.0
  PIPELINE.EnableFrustumCulling.value     = False
  PIPELINE.AmbientColor.value             = avango.gua.Color(0.2, 0.2, 0.2)
  PIPELINE.FarClip.value                  = 800.0
  PIPELINE.EnableBackfaceCulling.value    = False
  PIPELINE.EnableSsao.value               = True
  PIPELINE.SsaoRadius.value               = 2.0
  PIPELINE.SsaoIntensity.value            = 2.0
  PIPELINE.EnableFPSDisplay.value         = False
  PIPELINE.BackgroundMode.value           = avango.gua.BackgroundMode.SKYMAP_TEXTURE
  PIPELINE.FogTexture.value               = PIPELINE.BackgroundTexture.value