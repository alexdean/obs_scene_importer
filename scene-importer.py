import obspython as obs
import glob
import os.path as path

template_scene_name = ""
image_directory = ""

def script_description():
  return """
    Create 1 new scene for each image file in a directory.
    Filenames like '01 - Scene Name.jpg'.
  """

# build the dialogs for user interaction
def script_properties():
  props = obs.obs_properties_create()

  scenes = obs.obs_frontend_get_scene_names()
  scene_select = obs.obs_properties_add_list(props, "template_scene_name", "Scene to use as a template", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  for scene in scenes:
    obs.obs_property_list_add_string(scene_select, scene, scene)

  obs.obs_properties_add_path(props, 'image_directory', 'Image directory', obs.OBS_PATH_DIRECTORY, '', '')

  obs.obs_properties_add_button(props, "button", "Import", run_import)
  return props

# called when properties are updated
def script_update(settings):
  global template_scene_name
  global image_directory
  template_scene_name = obs.obs_data_get_string(settings, "template_scene_name")
  image_directory = obs.obs_data_get_string(settings, "image_directory")

def run_import(props, prop):
  global template_scene_name
  global image_directory

  template_source = obs.obs_get_source_by_name(template_scene_name)
  template_scene = obs.obs_scene_from_source(template_source)

  # expecting filenames like '01 - test.jpg'
  files = glob.glob(image_directory + "/*")
  files.sort()
  for filename in files:
    obs.script_log(obs.LOG_WARNING, filename)
    parts = path.basename(filename).split('-')
    name_without_ordinal = parts[1].strip() # name = 'test.jpg'
    parts = name_without_ordinal.split('.')
    bare_name = parts[0].strip() # name = 'test'

    new_scene = obs.obs_scene_duplicate(template_scene, bare_name, obs.OBS_SCENE_DUP_REFS)

    source_data = obs.obs_data_create()
    obs.obs_data_set_string(source_data, 'file', filename)
    source = obs.obs_source_create('image_source', 'Image - ' + bare_name, source_data, None)
    scene_item = obs.obs_scene_add(new_scene, source)
    obs.obs_sceneitem_set_order(scene_item, obs.OBS_ORDER_MOVE_BOTTOM)

    obs.obs_source_release(source)
    obs.obs_scene_release(new_scene)

  obs.obs_source_release(template_source)
