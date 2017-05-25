try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore, Qt
    from PyQt4.QtGui import QMessageBox
    from core.coordinate import Coordinate
    from core.epanet.hydraulics.link import Pipe
    from ui import import_export
    # import plugins.ImportExportGIS.import_export as import_export
    import os

    plugin_name = "ImportExportGIS"
    plugin_create_menu = True
    __all__ = {"Export to GIS": 1,
               "Import from GIS to create model": 2}
    file_filter = "GeoJSON (*.json *.geojson);;" \
                  "Shapefile (*.shp);;" \
                  "Comma-separated text (*.csv);;" \
                  "File Geodatabase (*.gdb);;" \
                  "All files (*.*)"

    def run(session=None, choice=None):
        print("run " + str(choice))
        if not session or not session.project:
            result = "Project is not open"
        else:
            try:
                directory = session.program_settings.value("GISPath", os.path.dirname(session.project.file_name))

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
                        session.program_settings.setValue("GISPath", path_only)
                        session.program_settings.sync()

                    if choice == 1:
                        result = import_export.export_to_gis(session, file_name)
                    elif choice == 2:
                        # result = import_export.import_from_gis(session, file_name)
                        if str(file_name).lower().endswith("json"):
                            if session.model == "EPANET":
                                import_summary = import_export.import_epanet_from_geojson(session, file_name)
                                result = "imported objects:" + os.linesep
                                for et in import_summary:
                                    result = result + et + ": " + str(import_summary[et]) + " objects" + os.linesep
                            elif session.model == "SWMM":
                                import_summary = import_export.import_swmm_from_geojson(session, file_name)
                                result = "imported objects:" + os.linesep
                                for et in import_summary:
                                    result = result + et + ": " + str(import_summary[et]) + " objects" + os.linesep
                        else:
                            result = "Create Model from GIS data supports GeoJSON data only"
                else:
                    result = "Selected operation not yet implemented."
                QMessageBox.information(None, plugin_name, result, QMessageBox.Ok)
            except Exception as ex:
                print str(ex)


except Exception as ex:
    print "Skip loading ImportExportGIS plugin: " + str(ex)
