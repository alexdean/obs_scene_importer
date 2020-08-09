import obspython as obs

def fit_to_screen(scene_item):
  # see ~/Library/Application Support/obs-studio/basic/profiles/Untitled/basic.ini
  # which contains
  # BaseCX=1680
  # BaseCY=1050
  # OutputCX=1120
  # OutputCY=700
  # 1680 x 1050 appear to be the dimensions we want, to completely fill the scren.
  video_info = obs.obs_video_info()
  obs.obs_get_video_info(video_info)

  bounds = obs.vec2()
  bounds.x = video_info.base_width # output_width # 1680 # source_width
  bounds.y = video_info.base_height # output_height # 1050 # source_height
  obs.obs_sceneitem_set_bounds(scene_item, bounds)

  # fit video to screen
  # https://obsproject.com/docs/reference-scenes.html?highlight=bounds#c.obs_transform_info.bounds
  obs.obs_sceneitem_set_bounds_type(scene_item, obs.OBS_BOUNDS_SCALE_INNER)

  scale = obs.vec2()
  scale.x = 1
  scale.y = 1
  obs.obs_sceneitem_set_scale(scene_item, scale)
