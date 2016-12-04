import ui.import_export as ie

file_name = r"C:/devNotMW/SWMM-EPANET_User_Interface_dev_ui/test/core/epanet/Examples/SouthCentral/tank.shp"

model_attributes = ["name", "description", "elevation", "minimum_level", "maximum_level", "initial_level", "diameter", "minimum_volume", "volume_curve"]
gis_attributes   = ["ID",   "DESCRIPT",    "ELEVATION", "MIN_LEVEL",     "MAX_LEVEL",     "INIT_LEVEL",    "DIAMETER", "MIN_VOLUME",     "CURVE"]

print(ie.import_epanet_tanks(session, file_name, model_attributes, gis_attributes))