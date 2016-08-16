try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore, Qt
    from PyQt4.QtGui import QMessageBox
    from core.coordinate import Coordinate
    from core.epanet.hydraulics.link import Pipe
    import plugins.EpanetGIS.exporter
    import plugins.EpanetGIS.importer
    import os

    plugin_name = "EpanetGIS"
    plugin_create_menu = True
    __all__ = {"Export to GIS": 1,
               "Import from GIS": 2}
    file_filter = "GeoJSON (*.json);;Shapefile (*.shp);;All files (*.*)"

    def run(session=None, choice=None):
        print("run " + str(choice))
        if not session or not session.project:
            result = "Project is not open"
        else:
            try:
                gui_settings = QtCore.QSettings("EPANET", "GUI")
                directory = gui_settings.value("GISPath", os.path.dirname(session.project.file_name))

                if choice == 1:
                    file_name = QtGui.QFileDialog.getSaveFileName(session, "Export to GIS",
                                                                  directory, file_filter)
                elif choice == 2:
                    file_name = QtGui.QFileDialog.getOpenFileName(session, "Select GIS file to import",
                                                                  directory, file_filter)
                else:
                    file_name = ''

                if file_name:
                    path_only, file_only = os.path.split(file_name)
                    if path_only != directory:  # Save path as default for next import/export operation
                        gui_settings.setValue("GISPath", path_only)
                        gui_settings.sync()

                    if choice == 1:
                        result = plugins.EpanetGIS.exporter.export_to_gis(session, file_name)
                    elif choice == 2:
                        result = plugins.EpanetGIS.importer.import_from_gis(session, file_name)
                else:
                    result = "Selected operation not yet implemented."
                del gui_settings
                QMessageBox.information(None, plugin_name, result, QMessageBox.Ok)
            except Exception as ex:
                print str(ex)


except Exception as ex:
    print "Skip loading plugin: " + str(ex)
