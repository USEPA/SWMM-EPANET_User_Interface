import ui.import_export as ie

file_name = r"C:/devNotMW/SWMM-EPANET_User_Interface_dev_ui/test/core/epanet/Examples/SouthCentral/pipe.shp"

model_attributes = ["name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
gis_attributes   = ["ID",   "DESCRIPT",    "FROM",       "TO",          "LENGTH", "DIAMETER", "ROUGHNESS", "MINORLOSS"]

print(ie.import_epanet_pipes(session, file_name, model_attributes, gis_attributes))
