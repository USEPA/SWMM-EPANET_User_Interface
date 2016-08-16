from qgis.core import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox


def export_to_gis(session, file_name):
    if file_name.lower().endswith("shp"):
        driver_name = "ESRI Shapefile"
    else:
        driver_name = "GeoJson"
    coordinates = session.project.coordinates.value
    vertices =  session.project.vertices.value

    attributes = {"type": "type",
                  "name": "name",
                  "description": "description",
                  "inlet_node": "inlet_node",
                  "outlet_node": "outlet_node",
                  "length": "length",
                  "diameter": "diameter",
                  "roughness": "roughness",
                  "loss_coefficient": "loss_coefficient"}
    """ Dictionary of attribute names in vector layer: attribute names of EPANET object.
        Edit strings in the left column as needed to match layer being imported.
        To omit an attribute from the GIS layer, delete the line containing that field.
        EPANET object attribute "type" will be exported as, for example, "Pipe", "Pump" or "Valve".
    """
    layer = make_links_layer(coordinates, vertices, session.project.pipes.value, attributes)
    if layer:
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_name, "utf-8", layer.crs(), driver_name)

    result = "Saved " + file_name


def make_links_layer(coordinates, vertices, links, attributes):
    layer = QgsVectorLayer("LineString", "links", "memory")
    provider = layer.dataProvider()

    # add fields
    fields = []
    for layer_attribute, model_attribute in attributes.items():
        fields.append(QgsField(model_attribute, QtCore.QVariant.String))
    provider.addAttributes(fields)

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
                points = [QgsPoint(float(inlet_coord.x), float(inlet_coord.y))]
                for vertex_pair in vertices:
                    if vertex_pair.name == link.name:
                        points.append(QgsPoint(float(vertex_pair.x), float(vertex_pair.y)))
                points.append(QgsPoint(float(outlet_coord.x), float(outlet_coord.y)))
                feature.setGeometry(QgsGeometry.fromPolyline(points))

                values = []
                for layer_attribute, model_attribute in attributes.items():
                    if model_attribute == "type":
                        values.append(type(link).__name__)
                    else:
                        values.append(getattr(link, model_attribute, ''))
                feature.setAttributes(values)
                features.append(feature)
                break  # stop looking for more coordinates

    if features:
        layer.startEditing()  # changes are only possible when editing the layer
        provider.addFeatures(features)
        layer.commitChanges()
        layer.updateExtents()
        return layer
    else:
        return None

