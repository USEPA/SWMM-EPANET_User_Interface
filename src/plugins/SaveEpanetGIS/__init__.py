try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore, Qt
    from PyQt4.QtGui import QMessageBox
    import os

    plugin_name = "SaveEpanetGIS"  # "Save EPANET to GIS"
    plugin_create_menu = True
    # __all__ = {"Save Pipes": "pipes", "Save Pumps": "pumps"}
    __all__ = {"Save Pipes": 1, "Save Pumps": 2}


    def run(session=None, choice=None):
        print("run " + str(choice))
        try:
            if choice == 1:
                if not session or not session.project:
                    result = "Project is not open"
                else:
                    file_name = os.path.join(os.path.dirname(session.project.file_name), "pipes.json")
                    print("save pipes to " + file_name)
                    links = session.project.pipes.value
                    attributes = ["name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness",
                                  "loss_coefficient"]
                    save_links(session.project, links, file_name, attributes)
                    result = "Saved " + file_name

            #elif choice == "pumps":
            #elif choice == 3:
            else:
                result = "Selected operation not yet implemented."
            QMessageBox.information(None, plugin_name, result, QMessageBox.Ok)
        except Exception as ex:
            print str(ex)

    def save_links(project, links, file_name, attributes):
        coordinates = project.coordinates.value
        layer = QgsVectorLayer("LineString", "links", "memory")
        provider = layer.dataProvider()

        # add fields
        provider.addAttributes([QgsField(link_attr, QtCore.QVariant.String) for link_attr in attributes])

        features = []
        # Receivers = as in the above example 'Receivers' is a list of results
        for link in links:
            inlet_coord = None
            outlet_coord = None
            for coordinate_pair in coordinates:
                if coordinate_pair.name == link.inlet_node:
                    inlet_coord = coordinate_pair
                if coordinate_pair.name == link.outlet_node:
                    outlet_coord = coordinate_pair
                if inlet_coord and outlet_coord:
                    # add a feature
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPolyline([
                        QgsPoint(float(inlet_coord.x), float(inlet_coord.y)),
                        QgsPoint(float(outlet_coord.x), float(outlet_coord.y))]))

                    feature.setAttributes([getattr(link, link_attr, '') for link_attr in attributes])
                    features.append(feature)
                    break  # stop looking for more coordinates

        # changes are only possible when editing the layer
        layer.startEditing()
        provider.addFeatures(features)
        layer.commitChanges()
        layer.updateExtents()

        if file_name.lower().endswith("shp"):
            driver_name = "GeoJson"
        else:
            driver_name = "GeoJson"
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_name, "utf-8", layer.crs(), driver_name)


except Exception as ex:
    print "Skip loading plugin: " + str(ex)