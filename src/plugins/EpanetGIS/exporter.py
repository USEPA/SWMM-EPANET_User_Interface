from qgis.core import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
import os


def export_to_gis(session, file_name):
    if file_name.lower().endswith("shp"):
        driver_name = "ESRI Shapefile"
        one_file = False
    else:
        driver_name = "GeoJson"
        one_file = True
    coordinates = session.project.coordinates.value
    vertices = session.project.vertices.value

    path_file, extension = os.path.splitext(file_name)
    layer_count = 0
    layer = None

    pipe_model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    pipe_gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    pumps_model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
    pumps_gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
    valves_model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
    valves_gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
    """ Mapping of attribute names of model objects to attribute names exported to vector layer.
        Edit gis_attributes as needed to specify attribute names as they will appear when exported.
        To omit an attribute from the GIS layer, delete the attribute name from both lists.
        EPANET object attribute "element_type" will be exported as, for example, "Pipe", "Pump" or "Valve".
    """

    if one_file:  # if putting all types in one file, need all attributes to include ones from all layers
        all_gis_attributes = pipe_gis_attributes | pumps_gis_attributes | valves_gis_attributes
    else:
        all_gis_attributes = pipe_gis_attributes

    # Export Pipes
    layer = make_links_layer(coordinates, vertices, session.project.pipes.value,
                             pipe_model_attributes, pipe_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_pipes" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
            print("saved " + layer_file_name)

    # Export Pumps
    if not one_file:
        layer = None
        all_gis_attributes = pumps_gis_attributes

    layer = make_links_layer(coordinates, vertices, session.project.pumps.value,
                             pumps_model_attributes, pumps_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_pumps" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
            print("saved " + layer_file_name)

    # Export Valves
    if not one_file:
        layer = None
        all_gis_attributes = valves_gis_attributes
    layer = make_links_layer(coordinates, vertices, session.project.valves.value,
                             valves_model_attributes, valves_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_valves" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
            print("saved " + layer_file_name)

    if one_file:
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_name, "utf-8", layer.crs(), driver_name)
        print("saved " + file_name)

    return "Exported " + str(layer_count) + " layers to GIS"


def make_gis_fields(gis_attributes):
    # create GIS fields
    fields = []
    for gis_attribute in gis_attributes:
        fields.append(QgsField(gis_attribute, QtCore.QVariant.String))


def make_links_layer(coordinates, vertices, links, model_attributes, gis_attributes, all_gis_attributes, layer):
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
                for gis_attribute in all_gis_attributes:
                    try:
                        index = gis_attributes.index(gis_attribute)
                        model_attribute = model_attributes[index]
                        if model_attribute == "element_type":
                            values.append(type(link).__name__)
                        else:
                            values.append(getattr(link, model_attribute, ''))
                    except:
                        values.append(None)
                feature.setAttributes(values)
                features.append(feature)
                break  # stop looking for more coordinates
    if features:  # If features were created, build and return a GIS layer containing these features
        creating_layer = (layer is None)
        if creating_layer:
            layer = QgsVectorLayer("LineString", "links", "memory")
            provider = layer.dataProvider()
            provider.addAttributes(make_gis_fields(all_gis_attributes))
        else:
            provider = layer.dataProvider()

        layer.startEditing()  # changes are only possible when editing the layer
        provider.addFeatures(features)
        layer.commitChanges()
        layer.updateExtents()
        return layer
    else:  # No features were created, so do not create a GIS layer. Probably this model does not have any of these.
        return None


def make_points_layer(coordinates, model_points, model_attributes, gis_attributes):
    features = []
    # Receivers = as in the above example 'Receivers' is a list of results
    for model_point in model_points:
        for coordinate_pair in coordinates:
            if coordinate_pair.name == model_point.name:
                # add a feature
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(coordinate_pair.x), float(coordinate_pair.y))))
                values = []
                for model_attribute in model_attributes:
                    if model_attribute == "element_type":
                        values.append(type(model_point).__name__)
                    else:
                        values.append(getattr(model_point, model_attribute, ''))
                feature.setAttributes(values)
                features.append(feature)

    if features:  # If features were created, build and return a GIS layer containing these features
        layer = QgsVectorLayer("Point", "Nodes", "memory")
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
