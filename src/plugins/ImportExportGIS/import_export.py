import os
from enum import Enum
from qgis.core import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.link import Pipe, Pump, Valve

"""Export (save) model elements as GIS data or Import (read) model elements from existing GIS data."""


""" *_model_attributes and *_gis_attributes map the attribute names of model objects to attribute names
    exported to or imported from a GIS vector layer.
    Edit *_gis_attributes as needed to specify attribute (column) names as they will appear when imported or exported.
    To omit an attribute from the GIS layer, change the attribute name to be blank in *_gis_attributes.
    model attribute "element_type" will be exported as, for example, "Pipe", "Pump" or "Valve".
"""
pipe_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness",
    "loss_coefficient"]
pipe_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness",
    "loss_coefficient"]

pumps_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
pumps_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]

valves_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
valves_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]

junctions_model_attributes = [
    "element_type", "name", "elevation", "base_demand_flow", "demand_pattern_name"]
junctions_gis_attributes = [
    "element_type", "id", "elevation", "base_demand_flow", "demand_pattern"]

labels_model_attributes = [
    "element_type", "name", "anchor_name", "font", "size", "bold", "italic"]
labels_gis_attributes = [
    "element_type", "id", "anchor_name", "font", "size", "bold", "italic"]

conduit_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "length", "roughness",
    "inlet_offset", "outlet_offset", "maximum_flow", "loss_coefficient", "flap_gate", "seepage"]
conduit_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "length", "roughness",
    "inlet_offset", "outlet_offset", "maximum_flow", "loss_coefficient", "flap_gate", "seepage"]

junctions_model_attributes_swmm = [
    "element_type", "name", "elevation", "max_depth", "surcharge_depth", "ponded_area"]
junctions_gis_attributes_swmm = [
    "element_type", "id", "elevation", "max_depth", "surcharge_depth", "ponded_area"]


def export_to_gis(session, file_name):
    path_file, extension = os.path.splitext(file_name)
    extension = extension.lower()
    layer_options = ''
    if extension == ".shp":
        driver_name = "ESRI Shapefile"
        one_file = False
    elif extension == ".csv":
        driver_name = "CSV"
        one_file = False
    elif extension == ".gdb":
        driver_name = "FileGDB"
        one_file = True
        layer_options = 'GEOMETRY=AS_XYZ'
    else:
        driver_name = "GeoJson"
        one_file = True
        extension = ".json"
    coordinates = session.project.all_coordinates()
    vertices = session.project.vertices.value
    if session.model == "EPANET":
        return export_epanet_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                                    coordinates, vertices)
    else:
        return export_swmm_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                                  coordinates, vertices)

def export_epanet_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                         coordinates, vertices):
    layer_count = 0
    layer = None

    all_gis_attributes = pipe_gis_attributes
    if one_file:  # if putting all types in one file, need all attributes to include ones from all layers
        for attributes in (pumps_gis_attributes, valves_gis_attributes, junctions_gis_attributes, labels_gis_attributes):
            for attribute in attributes:
                if attribute and attribute not in all_gis_attributes:
                    all_gis_attributes.append(attribute)

    # Export Pipes
    layer = make_links_layer(coordinates, vertices, session.project.pipes.value,
                             pipe_model_attributes, pipe_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_pipes" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(),
                                                    driver_name,
                                                    layerOptions=layer_options)
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

    # Export Junctions
    if not one_file:
        layer = None
        all_gis_attributes = junctions_gis_attributes

    layer = make_points_layer(session.project.junctions.value,
                              junctions_model_attributes, junctions_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_junctions" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
            print("saved " + layer_file_name)

    # Export Labels
    if not one_file:
        layer = None
        all_gis_attributes = labels_gis_attributes

    layer = make_points_layer(session.project.labels.value,
                              labels_model_attributes, labels_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_labels" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
            print("saved " + layer_file_name)

    if one_file:
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_name, "utf-8", layer.crs(), driver_name)
        print("saved " + file_name)

    return "Exported " + str(layer_count) + " layers to GIS"

def export_swmm_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                       coordinates, vertices):
    layer_count = 0
    layer = None

    all_gis_attributes = conduit_gis_attributes
    if one_file:  # if putting all types in one file, need all attributes to include ones from all layers
        for attributes in (pumps_gis_attributes, valves_gis_attributes, junctions_gis_attributes, labels_gis_attributes):
            for attribute in attributes:
                if attribute and attribute not in all_gis_attributes:
                    all_gis_attributes.append(attribute)

    # Export conduits
    layer = make_links_layer(coordinates, vertices, session.project.conduits.value,
                             conduit_model_attributes, conduit_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_conduits" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(),
                                                    driver_name,
                                                    layerOptions=layer_options)
            print("saved " + layer_file_name)

    # Export Junctions
    if not one_file:
        layer = None
        all_gis_attributes = junctions_gis_attributes_swmm

    layer = make_points_layer(session.project.junctions.value,
                              junctions_model_attributes_swmm, junctions_gis_attributes_swmm, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_junctions" + extension
            QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", layer.crs(), driver_name)
            print("saved " + layer_file_name)

    # Export Labels
    if not one_file:
        layer = None
        all_gis_attributes = labels_gis_attributes

    layer = make_points_layer(session.project.labels.value,
                              labels_model_attributes, labels_gis_attributes, all_gis_attributes, layer)
    if layer:
        layer_count += 1
        if not one_file:
            layer_file_name = path_file + "_labels" + extension
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
        if gis_attribute:
            fields.append(QgsField(gis_attribute, QtCore.QVariant.String))
    return fields


def make_links_layer(coordinates, vertices, links, model_attributes, gis_attributes, all_gis_attributes, layer):
    features = []
    for link in links:       # For each link, create a GIS feature
        try:
            inlet_coord = coordinates[link.inlet_node]
            outlet_coord = coordinates[link.outlet_node]
            feature = QgsFeature()
            points = [QgsPoint(float(inlet_coord.x), float(inlet_coord.y))]
            for vertex_pair in vertices:  # Add any intermediate points between inlet and outlet
                if vertex_pair.name == link.name:
                    points.append(QgsPoint(float(vertex_pair.x), float(vertex_pair.y)))
            points.append(QgsPoint(float(outlet_coord.x), float(outlet_coord.y)))
            feature.setGeometry(QgsGeometry.fromPolyline(points))

            values = gis_values_from_model(link, model_attributes, gis_attributes, all_gis_attributes)
            feature.setAttributes(values)
            features.append(feature)
        except Exception as exLink:
            print "Skipping link " + link.name + ": " + str(exLink)
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

def gis_values_from_model(model_object, model_attributes, gis_attributes, all_gis_attributes):
    values = []
    for gis_attribute in all_gis_attributes:
        if gis_attribute:
            try:
                index = gis_attributes.index(gis_attribute)
                model_attribute = model_attributes[index]
                if model_attribute == "element_type":
                    values.append(type(model_object).__name__)
                else:
                    attr_value = getattr(model_object, model_attribute, '')
                    if isinstance(attr_value, Enum):
                        attr_value = attr_value.name.replace('_', '-')
                    if isinstance(attr_value, bool):
                        if attr_value:
                            attr_value = "YES"
                        else:
                            attr_value = "NO"
                    if isinstance(attr_value, list):
                        attr_value = ' '.join(attr_value)
                    values.append(attr_value)
            except:
                values.append(None)
    return values


def make_points_layer(model_points, model_attributes, gis_attributes, all_gis_attributes, layer):
    features = []
    # Receivers = as in the above example 'Receivers' is a list of results
    for model_point in model_points:
        try:
            # add a feature
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(model_point.x), float(model_point.y))))
            values = gis_values_from_model(model_point, model_attributes, gis_attributes, all_gis_attributes)
            feature.setAttributes(values)
            features.append(feature)
        except Exception as exPoint:
            print "Skipping point " + model_point.name + ": " + str(exPoint)

    if features:  # If features were created, build and return a GIS layer containing these features
        creating_layer = (layer is None)
        if creating_layer:
            layer = QgsVectorLayer("Point", "Nodes", "memory")
            provider = layer.dataProvider()
            provider.addAttributes(make_gis_fields(all_gis_attributes))
        else:
            provider = layer.dataProvider()

        layer.startEditing()  # changes are only possible when editing the layer
        provider.addFeatures(features)
        layer.commitChanges()
        layer.updateExtents()
    return layer


def import_from_gis(session, file_name):
    # importable_sections = [session.project.pipes, session.project.pumps, session.project.valves]
    # already_populated_sections = [section for section in importable_sections if len(section.value) > 0]
    project = session.project
    num_existing_junctions = len(project.junctions.value)

    section = project.pipes
    if len(section.value) > 0:
        msg = QMessageBox()
        msg.setText("Discard " + str(len(section.value)) + " links already in model before import?")
        msg.setWindowTitle("Importing Links")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        choice = msg.exec_()
        if choice == QMessageBox.Yes:
            section.value = []
        elif choice == QMessageBox.No:
            pass
        elif choice == QMessageBox.Cancel:
            return

    result = import_links(project, section.value, file_name, pipe_model_attributes, pipe_gis_attributes, Pipe)
    if len(project.junctions.value) > num_existing_junctions:
        session.model_layers.junctions = session.map_widget.addCoordinates(project.junctions.value, "Junctions")
    session.model_layers.pipes = session.map_widget.addLinks(project.all_coordinates(),
                                                             section.value, "Pipes", QtGui.QColor('gray'), 3)
    session.map_widget.zoomfull()
    return result


def import_links(project, links, file_name, model_attributes, gis_attributes, model_type, type_field='', type_value=''):
    """ Read GIS vector layer in file_name into links list.
    Args:
        project: EPANET project to import into, used for access to its coordinates attribute
                 which is updated with the newly imported values.
        links: list of project objects which non-geographic properties are imported into.
        file_name: GIS file to read.
        model_attributes: attribute names of the model objects in "links" list.
        gis_attributes: name of attributes as they exist in file_name.


    Notes:
        model_attributes and gis_attributes must be aligned with each other.
        Each value found by gis_attribute is assigned to the model_attribute in the same position in its array.
        If model_attribute is "inlet_node" or "outlet_node" these are added to project.junctions.
    """
    count = 0
    try:
        layer = QgsVectorLayer(file_name, "import", "ogr")
        if layer:
            coordinates = project.all_coordinates()
            for feature in layer.getFeatures():
                geom = feature.geometry()
                if geom.type() == QGis.Line:
                    line = geom.asPolyline()
                    model_item = model_type()
                    for model_attribute, gis_attribute in zip(model_attributes, gis_attributes):
                        attr_value = feature[gis_attribute]
                        setattr(model_item, model_attribute, attr_value)

                        # If this attribute is the inlet or outlet node, make sure project has its coordinates
                        index = -1
                        if model_attribute == "inlet_node":
                            index = 0
                        elif model_attribute == "outlet_node":
                            index = len(line) - 1
                        if index >= 0:
                            try:     # Remove this coordinate if it already exists
                                this_coord = coordinates[attr_value]
                            except:  # do not already have this coordinate, create it
                                this_coord = Junction()
                                this_coord.name = attr_value
                                project.junctions.value.append(this_coord)
                                coordinates.append(this_coord)
                            this_coord.x = line[index].x()
                            this_coord.y = line[index].y()
                    links.append(model_item)
                    count += 1
    except Exception as ex:
        print(str(ex))
    return "Imported " + str(count) + " " + model_type.__name__ + "s"
