import ui.import_export as ie
from PyQt4 import QtGui

directory = r"C:/devNotMW/GitHub/SWMM-EPANET_User_Interface_dev_ui/test/core/epanet/Examples/SouthCentral/"

file_name = QtGui.QFileDialog.getOpenFileName(None, 'Open Pipe File...', directory,
                                             'Shapefiles (*.shp);;All files (*.*)')
if file_name:
    model_attributes = ["name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    gis_attributes   = ["ID",   "DESCRIPT",    "FROM",       "TO",          "LENGTH", "DIAMETER", "ROUGHNESS", "MINORLOSS"]

    print(ie.import_epanet_pipes(session, file_name, model_attributes, gis_attributes))
