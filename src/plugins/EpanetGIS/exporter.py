from qgis.core import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
import os


def export_to_gis(session, file_name):
    if file_name.lower().endswith("shp"):
        driver_name = "ESRI Shapefile"
    else:
        driver_name = "GeoJson"
    coordinates = session.project.coordinates.value
    vertices = session.project.vertices.value

    path_file, extension = os.path.splitext(file_name)
    layer_count = 0

    # Export Pipes
    model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    """ Mapping of attribute names of model objects to attribute names exported to vector layer.
        Edit gis_attributes as needed to specify attribute names as they will appear when exported.
        To omit an attribute from the GIS layer, delete the attribute name from both lists.
        EPANET object attribute "element_type" will be exported as, for example, "Pipe", "Pump" or "Valve".
    """
    layer = make_links_layer(coordinates, vertices, session.project.pipes.value, model_attributes, gis_attributes)
    if layer:
        layer_file_name = path_file + "_pipes" + extension
        QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
        print("saved " + layer_file_name)
        layer_count += 1

    # Export Pumps
    model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
    gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
    layer = make_links_layer(coordinates, vertices, session.project.pumps.value, model_attributes, gis_attributes)
    if layer:
        layer_file_name = path_file + "_pumps" + extension
        QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
        print("saved " + layer_file_name)
        layer_count += 1

    # Export Valves
    model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
    gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
    layer = make_links_layer(coordinates, vertices, session.project.valves.value, model_attributes, gis_attributes)
    if layer:
        layer_file_name = path_file + "_valves" + extension
        QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
        print("saved " + layer_file_name)
        layer_count += 1

    result = "Exported " + str(layer_count) + " layers to GIS"


def make_links_layer(coordinates, vertices, links, model_attributes, gis_attributes):
    features = []
    for link in links:       # For each link, create a GIS feature
        inlet_coord = None
        outlet_coord = None
        for coordinate_pair in coordinates:  # Find the locations of both ends of this link
            if coordinate_pair.name == link.inlet_node:
                inlet_coord = coordinate_pair
            if coordinate_pair.name == link.outlet_node:
                outlet_coord = coordinate_pair
            if inlet_coord and outlet_coord:
                # Found both inlet and outlet coordinates, ready to create a GIS feature
                feature = QgsFeature()
                points = [QgsPoint(float(inlet_coord.x), float(inlet_coord.y))]
                for vertex_pair in vertices:  # Add any intermediate points between inlet and outlet
                    if vertex_pair.name == link.name:
                        points.append(QgsPoint(float(vertex_pair.x), float(vertex_pair.y)))
                points.append(QgsPoint(float(outlet_coord.x), float(outlet_coord.y)))
                feature.setGeometry(QgsGeometry.fromPolyline(points))

                values = []
                for model_attribute in model_attributes:
                    if model_attribute == "element_type":
                        values.append(type(link).__name__)
                    else:
                        values.append(getattr(link, model_attribute, ''))
                feature.setAttributes(values)
                features.append(feature)
                break  # stop looking for more coordinates
    if features:  # If features were created, build and return a GIS layer containing these features
        layer = QgsVectorLayer("LineString", "links", "memory")
        provider = layer.dataProvider()

        # create GIS fields
        fields = []
        for gis_attribute in gis_attributes:
            fields.append(QgsField(gis_attribute, QtCore.QVariant.String))
        provider.addAttributes(fields)

        layer.startEditing()  # changes are only possible when editing the layer
        provider.addFeatures(features)
        layer.commitChanges()
        layer.updateExtents()
        return layer
    else:  # No features were created, so do not create a GIS layer. Probably this model does not have any of these.
        return None

