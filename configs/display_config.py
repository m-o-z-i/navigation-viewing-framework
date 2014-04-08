#!/usr/bin/python

display_config = [
  {
  ##################################################
      "name":             "large_powerwall"
  ##################################################
    , "hostname":         "kerberos"
    , "displaystrings":   [":0.0", ":0.1", ":0.2", ":0.3"]
    , "resolution":       (1920, 1200)
    , "size":             (4.16, 2.6)
    , "transform":        (0.0, 1.57, 0.0)
    , "warpmatrices":     [
      (
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      )
      , (
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      )
      , (
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      )
      , (
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      )
    ]
  }

  , {
  ##################################################
      "name":             "small_powerwall"
  ##################################################
    , "hostname":         "tba"
    , "displaystrings":   [":0.0", ":0.1"]
    , "resolution":       (1920, 1200)
    , "size":             (3.0, 1.98)
    , "transform":        (0.0, 1.42, 0.0)
    , "warpmatrices":     [
      (
          "/opt/lcd-warpmatrices/lcd_4_warp_P2.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P2.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P2.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P1.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P1.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P1.warp"
      )
      , (
          "/opt/lcd-warpmatrices/lcd_4_warp_P4.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P4.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P4.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P3.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P3.warp"
        , "/opt/lcd-warpmatrices/lcd_4_warp_P3.warp"
      )
    ]
  }

  , {
  ##################################################
      "name":             "atalante_display"
  ##################################################
    , "hostname":         "atalante"
    , "resolution":       (1920, 1080)
    , "size":             (0.40, 0.20)
    , "transform":        (0.0, 1.0, 0.0)
  }
]
