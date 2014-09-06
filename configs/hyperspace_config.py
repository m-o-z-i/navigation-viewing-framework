

## hyperspace scenes
# a list of scenes or a single scene that is loaded;
# the first scene is activated by default
#
scenes = {
    0: "SceneVRHyperspace0(self, SCENEGRAPH, NET_TRANS_NODE)" # intro/outro
  , 1: "SceneVRHyperspace1(self, SCENEGRAPH, NET_TRANS_NODE)" # boarding & navigation
  , 2: "SceneVRHyperspace2(self, SCENEGRAPH, NET_TRANS_NODE)" # passenger seats, virtual air steward
  , 7: "SceneVRHyperspace2b(self, SCENEGRAPH, NET_TRANS_NODE)" # virtual air steward shows transparent window
  , 3: "SceneVRHyperspace3(self, SCENEGRAPH, NET_TRANS_NODE)" # ambient flightmode
  , 4: "SceneVRHyperspace4(self, SCENEGRAPH, NET_TRANS_NODE)" # in flight navigation, bar
  , 5: "SceneVRHyperspace5(self, SCENEGRAPH, NET_TRANS_NODE)" # bar, telepresence call, virtual passengers
  , 6: "SceneVRHyperspace6(self, SCENEGRAPH, NET_TRANS_NODE)" # virtual window, telepresence
}

active_scenes = [1]

stereo = True

animation_nodes = {
  1: [ "/net/SceneVRHyperspace1/nav_light_group" ],
  2: [],
  7: [ "/net/SceneVRHyperspace2b/terrain_group" ],
  3: [ "/net/SceneVRHyperspace3/terrain_group" ],
  4: [],
  5: [],
  6: [ "/net/SceneVRHyperspace6/terrain_group" ]
}

transparent_materials = ["Floor", "Roof", "SeatRow", "Seats", "Window"]

toggle_transparency = dict()
for mat in transparent_materials:
  toggle_transparency[mat] = {
      "toggle":     False
    , "start_time": 0.0
    , "start_val":  0.0
    , "end_val":    0.5
    , "end_time":   0.0
  }
transparency_toggle_duration = 5.0

textures = {
    1: ["data/textures/bwb/place-ticket-here-1.png", "data/textures/bwb/place-ticket-here-2.png", "data/textures/bwb/place-ticket-here-3.png"]
  , 2: ["data/textures/bwb/backrest-1.png", "data/textures/bwb/backrest-2.png", "data/textures/bwb/backrest-3.png"]
  , 5: ["data/textures/bwb/call-1.png", "data/textures/bwb/call-2.png", "data/textures/bwb/call-3.png"]
}
texture_idx = 0

# this flag is set automatically, nothing to do here
prepipes = len([i for i in [3, 6, 7] if i in active_scenes]) > 0
