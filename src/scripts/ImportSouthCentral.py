import ui.import_export as ie
from PyQt4 import QtGui

directory = r"C:/devNotMW/GitHub/SWMM-EPANET_User_Interface_dev_ui/test/core/epanet/Examples/SouthCentral/"


# Locate and import junctions
file_name = QtGui.QFileDialog.getOpenFileName(None, 'Open Junction File...', directory,
                                             'Shapefiles (*.shp);;All files (*.*)')
if file_name:
    model_attributes = ["name", "description", "elevation", "base_demand_flow", "demand_pattern_name"]
    gis_attributes   = ["ID",   "DESCRIPT",    "ELEVATION", "DEMAND1",          "PATTERN1"]

    print(ie.import_epanet_junctions(session, file_name, model_attributes, gis_attributes))
else:
    print("Skipped Junctions")


# Locate and import tanks
file_name = QtGui.QFileDialog.getOpenFileName(None, 'Open Tank File...', directory,
                                             'Shapefiles (*.shp);;All files (*.*)')
if file_name:
    model_attributes = ["name", "description", "elevation", "minimum_level", "maximum_level", "initial_level", "diameter", "minimum_volume", "volume_curve"]
    gis_attributes   = ["ID",   "DESCRIPT",    "ELEVATION", "MIN_LEVEL",     "MAX_LEVEL",     "INIT_LEVEL",    "DIAMETER", "MIN_VOLUME",     "CURVE"]

    print(ie.import_epanet_tanks(session, file_name, model_attributes, gis_attributes))
else:
    print("Skipped Tanks")


# Locate and import pipes
file_name = QtGui.QFileDialog.getOpenFileName(None, 'Open Pipe File...', directory,
                                             'Shapefiles (*.shp);;All files (*.*)')
if file_name:
    model_attributes = ["name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    gis_attributes   = ["ID",   "DESCRIPT",    "FROM",       "TO",          "LENGTH", "DIAMETER", "ROUGHNESS", "MINORLOSS"]

    print(ie.import_epanet_pipes(session, file_name, model_attributes, gis_attributes))
else:
    print("Skipped Pipes")
