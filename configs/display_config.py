#!/usr/bin/python

display_config = [
    {
      "name":             "large_powerwall"
    , "hostname":         "kerberos"
    , "displaystrings":   [":0.0", ":0.1", ":0.2", ":0.3"]
    , "resolution":       (1920, 1200)
    , "size":             (4.16, 2.6)
    , "transform":        (0.0, 1.57, 0.0)
    , "warpmatricespath": "/opt/dlp-warpmatrices/"
    }
  , {
      "name":             "atalante_display"
    , "hostname":         "atalante"
    , "resolution":       (1920, 1080)
    , "size":             (0.40, 0.20)
    , "transform":        (0.0, 1.0, 0.0)
    }
]
