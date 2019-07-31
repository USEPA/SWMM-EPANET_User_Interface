import ui.import_export as ie
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog

directory = r"C:/devNotMW/GitHub/SWMM-EPANET_User_Interface_dev_ui/test/core/epanet/Examples/SouthCentral/"

file_name, ftype = QFileDialog.getOpenFileName(None, 'Open Junction File...', directory,
                                             'Shapefiles (*.shp);;All files (*.*)')
if file_name:
    model_attributes = ["name", "description", "elevation", "base_demand_flow", "demand_pattern_name"]
    gis_attributes   = ["ID",   "DESCRIPT",    "ELEVATION", "DEMAND1",          "PATTERN1"]

    print(ie.import_epanet_junctions(session, file_name, model_attributes, gis_attributes))
