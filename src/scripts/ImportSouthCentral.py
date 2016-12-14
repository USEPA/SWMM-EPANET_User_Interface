import ui.import_export as ie
from PyQt4 import QtGui

"""
    Example script that imports a particular set of shapefiles into an EPANET project.
    This can be used on a blank project to start a new project or on an existing project to add objects.

    model_attributes is the list of model attributes for which there are values to be imported.
    When customizing this script, attributes for which there are no values in the GIS layer should be removed.
    gis_attributes is the list of field names in the GIS layer that will be imported into the model.
    The gis_attributes list must have the same order and number of attributes as the model_attributes for that layer.

    To make a more complicated import script, for example one that does a unit conversion on an attribute, see the
    source code at: https://github.com/USEPA/SWMM-EPANET_User_Interface/blob/dev-ui/src/ui/import_export.py
    and copy the import function called below and the import_nodes or import_links that it calls into your script and
    customize it as needed.

    All layers being imported must already be in the same projection or they will not line up on the map.
    If a shapefile being imported has a projection file (for example if Junction.shp has a corresponding Junction.prj)
    then that projection will be used by the project.
"""

# Customize this line to make the script start looking for files in a particular directory (optional)
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
