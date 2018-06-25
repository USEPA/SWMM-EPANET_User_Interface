import os
from enum import Enum
from qgis.core import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QMessageBox
from core.coordinate import Coordinate
from core.epanet.hydraulics.node import Junction as EpanetJunction
from core.epanet.hydraulics.node import Tank as EpanetTank
from core.epanet.hydraulics.node import Reservoir, Source, Demand
from core.epanet.hydraulics.node import SourceType, MixingModel
from core.epanet.hydraulics.link import Pipe, Pump, Valve, FixedStatus, ValveType
from core.epanet.labels import Label, MeterType
from core.swmm.hydraulics.node import Junction as SwmmJunction
from core.swmm.hydraulics.node import Outfall, OutfallType, StorageUnit, StorageCurveType, Divider, FlowDividerType
from core.swmm.hydraulics.node import SubCentroid
from core.swmm.hydraulics.link import Pump as SwmmPump
from core.swmm.hydraulics.link import Conduit, SubLink, Weir, WeirType, Orifice, OrificeType, RoadSurfaceType
from core.swmm.hydraulics.link import Outlet, OutletCurveType
from core.swmm.hydrology.raingage import RainGage, RainFormat, RainFileUnits, RainDataSource
from core.swmm.hydrology.subcatchment import Subcatchment, Routing
from ui.model_utility import ParseData
from core.indexed_list import IndexedList

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
pipe_import_attributes = [
    "id", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness",
    "loss_coefficient", "bulk_reaction_coefficient", "wall_reaction_coefficient", "initial_status"]

pumps_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
pumps_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "power", "head_curve_name", "speed", "pattern"]
pump_import_attributes = [ "id", "description", "inlet_node", "outlet_node",
                            "power", "head_curve_name", "speed", "pattern", "initial_status",
                            "efficiency_curve_name", "energy_price", "price_pattern"]
pump_import_attributes_swmm = [
    "id",
    "description",
    "inlet_node",
    "outlet_node",
    "initial_status",
    "startup_depth",
    "shutoff_depth"
]

valves_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
valves_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "setting", "minor_loss_coefficient"]
valve_import_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "type", "diameter", "setting",
    "minor_loss_coefficient", "status"]

junctions_model_attributes = [
    "element_type", "name", "elevation", "base_demand_flow", "demand_pattern_name"]
junctions_gis_attributes = [
    "element_type", "id", "elevation", "base_demand_flow", "demand_pattern"]
junction_import_attributes = [ "id", "elevation", "emitter_coefficient",
                               "initial_quality",
                               "source_quality_amount", "source_quality_type", "source_quality_pattern",
                               "base_demand_flow", "demand_pattern_name"]

labels_model_attributes = [
    "element_type", "name", "anchor_name", "font", "size", "bold", "italic"]
labels_gis_attributes = [
    "element_type", "id", "anchor_name", "font", "size", "bold", "italic"]
label_import_attributes = [
    "id", "description", "meter_type", "meter_name",
    "anchor_name", "font", "size", "bold", "italic"
]

reservoir_import_attributes = ["id", "tag", "total_head", "head_pattern_name",
                               "initial_quality",
                               "source_quality_amount", "source_quality_type", "source_quality_pattern"]
tank_import_attributes = [
 "id",
 "description",
 "inlet_node",
 "outlet_node",
 "elevation",
 "diameter",
 "initial_level",
 "minimum_level",
 "maximum_level",
 "minimum_volume",
 "volume_curve",
 "mixing_model",
 "mixing_fraction",
 "reaction_coeff",
 "initial_quality",
 "source_quality_amount",
 "source_quality_type",
 "source_quality_pattern"
]

conduit_model_attributes = [
    "element_type", "name", "description", "inlet_node", "outlet_node", "length", "roughness",
    "inlet_offset", "outlet_offset", "maximum_flow", "loss_coefficient", "flap_gate", "seepage"]
conduit_gis_attributes = [
    "element_type", "id", "description", "inlet_node", "outlet_node", "length", "roughness",
    "inlet_offset", "outlet_offset", "maximum_flow", "loss_coefficient", "flap_gate", "seepage"]
conduit_import_attributes = [
    "id",
    "description",
    "inlet_node",
    "outlet_node",
    "length",
    "roughness",
    "inlet_offset",
    "outlet_offset",
    "maximum_flow",
    "loss_coefficient",
    "entry_loss_coefficient",
    "exit_loss_coefficient",
    "flap_gate",
    "seepage",
    "max_depth"]

junctions_model_attributes_swmm = [
    "element_type", "name", "elevation", "max_depth", "surcharge_depth", "ponded_area"]
junctions_gis_attributes_swmm = [
    "element_type", "id", "elevation", "max_depth", "surcharge_depth", "ponded_area"]
junction_import_attributes_swmm = [
    "id",
    "description",
    "elevation",
    "max_depth",
    "initial_depth",
    "surcharge_depth",
    "ponded_area"
]

generic_model_attributes = [
    "element_type", "name"]
generic_gis_attributes = [
    "element_type", "id"]

subcatchment_model_attributes = [
    "element_type",
    "name",
    "description",
    "rain_gage",
    "outlet",
    "area",
    "width",
    "percent_slope",
    "percent_impervious",
    "n_imperv",
    "n_perv",
    "storage_depth_imperv",
    "storage_depth_perv",
    "percent_zero_impervious",
    "subarea_routing",
    "initial_loadings",
    "curb_length"]

subcatchment_import_attributes = [
    "id",
    "description",
    "rain_gage",
    "outlet",
    "area",
    "width",
    "percent_slope",
    "percent_impervious",
    "n_imperv",
    "n_perv",
    "storage_depth_imperv",
    "storage_depth_perv",
    "percent_zero_impervious",
    "subarea_routing",
    "initial_loadings",
    "curb_length"
]

raingage_import_attributes = [
    "id",
    "description",
    "rain_format",
    "rain_interval",
    "snow_catch_factor",
    "data_source",
    "timeseries",
    "data_file_name",
    "data_file_station_id",
    "data_file_rain_units",
]

outfall_import_attributes = [
    "id",
    "description",
    "elevation",
    "tide_gate",
    "route_to",
    "outfall_type",
    "fixed_stage",
    "tidal_curve",
    "time_series_name"
]

storage_import_attributes = [
    "id",
    "description",
    "elevation",
    "max_depth",
    "initial_depth",
    "evaporation_factor",
    "storage_curve",
    "coefficient",
    "exponent",
    "constant"
]

divider_import_attributes = [
    "id",
    "Description",
    "tag",
    "elevation",
    "max_depth",
    "initial_depth",
    "surcharge_depth",
    "ponded_area",
    "diverted_link",
    "flow_divider_type",
    "min_diversion_flow",
    "weir_height",
    "weir_coefficient"
]

#"can_surcharge", '', "Can Surcharge", "False", '', '', "True if weir can surcharge"),
#"flap_gate", '', "Flap Gate", "False", '', '', "True if weir contains a flap gate to prevent backflow"),
#"road_surface", '', "Road Surface", "", '', '', "Type of road surface if roadway weir")
weir_import_attributes = [
    "id",
    "description",
    "inlet_node",
    "outlet_node",
    "tag",
    "type",
    "height",
    "length",
    "side_slope",
    "inlet_offset",
    "discharge_coefficient",
    "flap_gate",
    "end_contractions",
    "end_coefficient",
    "can_surcharge",
    "road_width",
    "road_surface"
]

#"type", '', "Type", "", '', '', "Type of orifice"),
#"cross_section", '', "Shape", "", '', '', "Orifice shape"),
orifice_import_attributes = [
    "id",
    "description",
    "inlet_node",
    "outlet_node",
    "tag",
    "height",
    "width",
    "inlet_offset",
    "discharge_coefficient",
    "flap_gate",
    "o_rate"
]

outlet_import_attributes = [
    "id",
    "inlet_node",
    "outlet_node",
    "description",
    "tag",
    "inlet_offset",
    "flap_gate",
    "curve_type",
    "coefficient",
    "exponent",
    "rating_curve"
]

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
    coordinates = session.project.all_nodes()
    if session.model == "EPANET":
        return export_epanet_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                                    coordinates)
    else:
        return export_swmm_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                                  coordinates)

def export_epanet_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                         coordinates):
    layer_count = 0
    layer = None

    all_gis_attributes = pipe_gis_attributes
    if one_file:  # if putting all types in one file, need all attributes to include ones from all layers
        for attributes in (pumps_gis_attributes, valves_gis_attributes, junctions_gis_attributes, labels_gis_attributes):
            for attribute in attributes:
                if attribute and attribute not in all_gis_attributes:
                    all_gis_attributes.append(attribute)

    # Export Pipes
    layer = export_links_layer(session.project.pipes.value, pipe_model_attributes, pipe_gis_attributes,
                               all_gis_attributes, layer, session.crs, one_file, path_file + "_pipes" + extension,
                               driver_name, layer_options, coordinates)
    if layer:
        layer_count += 1

    # Export Pumps
    layer = export_links_layer(session.project.pumps.value, pumps_model_attributes, pumps_gis_attributes,
                               all_gis_attributes, layer, session.crs, one_file, path_file + "_pumps" + extension,
                               driver_name, layer_options, coordinates)
    if layer:
        layer_count += 1

    # Export Valves
    layer = export_links_layer(session.project.valves.value, valves_model_attributes, valves_gis_attributes,
                               all_gis_attributes, layer, session.crs, one_file, path_file + "_valves" + extension,
                               driver_name, layer_options, coordinates)
    if layer:
        layer_count += 1

    # Export Junctions
    layer = export_points_layer(session.project.junctions.value, junctions_model_attributes, junctions_gis_attributes,
                                all_gis_attributes, layer, session.crs, one_file,
                                path_file + "_junctions" + extension, driver_name, layer_options)
    if layer:
        layer_count += 1

    # Export Labels
    layer = export_points_layer(session.project.labels.value, labels_model_attributes, labels_gis_attributes,
                                all_gis_attributes, layer, session.crs, one_file,
                                path_file + "_labels" + extension, driver_name, layer_options)
    if layer:
        layer_count += 1

    for section in [session.project.reservoirs, session.project.tanks, session.project.sources]:
        if len(section.value) > 0:
            layer = export_points_layer(section.value, generic_model_attributes, generic_gis_attributes,
                                        all_gis_attributes, layer, session.crs, one_file,
                                        path_file + "_" + session.project.format_as_attribute_name(section.SECTION_NAME)
                                        + extension, driver_name, layer_options)
            if layer:
                layer_count += 1

    if one_file:
        if session.crs:
            layer.setCrs(session.crs)
        QgsVectorFileWriter.writeAsVectorFormat(layer, file_name, "utf-8", session.crs, driver_name)
        print("saved " + file_name)

    return "Exported " + str(layer_count) + " layers to GIS"


def export_swmm_to_gis(session, file_name, path_file, extension, driver_name, layer_options, one_file,
                       coordinates):
    layer_count = 0
    layer = None

    all_gis_attributes = conduit_gis_attributes
    if one_file:  # if putting all types in one file, need all attributes to include ones from all layers
        for attributes in (conduit_gis_attributes, junctions_gis_attributes_swmm, labels_gis_attributes):
            for attribute in attributes:
                if attribute and attribute not in all_gis_attributes:
                    all_gis_attributes.append(attribute)

    # Export conduits
    layer = export_links_layer(session.project.conduits.value, conduit_model_attributes, conduit_gis_attributes,
                               all_gis_attributes, layer, session.crs, one_file, path_file + "_conduits" + extension,
                               driver_name, layer_options, coordinates)
    if layer:
        layer_count += 1

    # Export Junctions
    layer = export_points_layer(session.project.junctions.value, junctions_model_attributes_swmm,
                                junctions_gis_attributes_swmm, all_gis_attributes, layer, session.crs, one_file,
                                path_file + "_junctions" + extension, driver_name, layer_options)
    if layer:
        layer_count += 1

    # Export Labels
    layer = export_points_layer(session.project.labels.value, labels_model_attributes, labels_gis_attributes,
                                all_gis_attributes, layer, session.crs, one_file,
                                path_file + "_labels" + extension, driver_name, layer_options)
    if layer:
        layer_count += 1

    for section in [session.project.raingages, session.project.outfalls,
                    session.project.dividers, session.project.storage]:
        if len(section.value) > 0:
            layer = export_points_layer(section.value, generic_model_attributes, generic_gis_attributes,
                                        all_gis_attributes, layer, session.crs, one_file,
                                        path_file + "_" + session.project.format_as_attribute_name(section.SECTION_NAME)
                                        + extension, driver_name, layer_options)
            if layer:
                layer_count += 1

    for section in [session.project.pumps, session.project.orifices, session.project.weirs, session.project.outlets]:
        if len(section.value) > 0:
            layer = export_links_layer(section.value, generic_model_attributes, generic_gis_attributes,
                                       all_gis_attributes, layer, session.crs, one_file,
                                       path_file + "_" + session.project.format_as_attribute_name(section.SECTION_NAME)
                                       + extension, driver_name, layer_options, coordinates)
            if layer:
                layer_count += 1

    if one_file:
        write_layer(layer, session.crs, file_name, driver_name, layer_options)

    layer_file_name = path_file + "_subcatchments" + extension
    one_file = False
    export_subcatchment_layer(session.project, session.model_layers.subcatchments, subcatchment_model_attributes,
                              session.crs, one_file, layer_file_name, driver_name, layer_options)
    return "Exported " + str(layer_count) + " layers to GIS"


def write_layer(layer, crs, layer_file_name, driver_name, layer_options):
    if layer:
        if crs:
            layer.setCrs(crs)
        QgsVectorFileWriter.writeAsVectorFormat(layer, layer_file_name, "utf-8", crs,
                                                driver_name, layerOptions=layer_options)
        if driver_name == "ESRI Shapefile":
            basename = os.path.splitext(layer_file_name)[0]
            os.remove(basename + ".cpg")
            os.remove(basename + ".qpj")
            if not crs or not crs.isValid():
                os.remove(basename + ".prj")

        print("saved " + layer_file_name)


def export_points_layer(model_points, model_attributes, gis_attributes, all_gis_attributes, layer, crs,
                        one_file, layer_file_name, driver_name, layer_options):
    if not one_file:
        layer = None
        all_gis_attributes = gis_attributes

    layer = make_points_layer(model_points, model_attributes, gis_attributes, all_gis_attributes, layer)

    if not one_file:
        write_layer(layer, crs, layer_file_name, driver_name, layer_options)
    return layer


def export_links_layer(model_links, model_attributes, gis_attributes, all_gis_attributes, layer, crs,
                        one_file, layer_file_name, driver_name, layer_options, coordinates):
    if not one_file:
        layer = None
        all_gis_attributes = gis_attributes

    layer = make_links_layer(coordinates, model_links,
                             model_attributes, gis_attributes, all_gis_attributes, layer)
    if not one_file:
        write_layer(layer, crs, layer_file_name, driver_name, layer_options)
    return layer

def export_subcatchment_layer(project, src_layer, model_attributes, crs, one_file, layer_file_name, driver_name,
                              layer_options):
    if not src_layer or src_layer.featureCount() == 0:
        return None
    ind = src_layer.fieldNameIndex(u'name')
    if ind < 0:
        return None
    layer = QgsVectorLayer("Polygon", "Subcatchment", "memory")
    provider = layer.dataProvider()
    provider.addAttributes(make_gis_fields(model_attributes))
    layer.startEditing()  # changes are only possible when editing the layer
    # src_layer = QgsVectorLayer()
    for f in src_layer.getFeatures():
        obj_sub = project.subcatchments.get_item(u'name', f.attributes()[ind])
        if obj_sub:
            new_f = QgsFeature()
            new_f.setGeometry(f.geometry())
            values = gis_values_from_model(obj_sub, model_attributes, model_attributes, model_attributes)
            new_f.setAttributes(values)
            layer.addFeature(new_f, False)
    layer.commitChanges()
    layer.updateExtents()

    if not one_file:
        write_layer(layer, crs, layer_file_name, driver_name, layer_options)
    return layer

def make_gis_fields(gis_attributes):
    # create GIS fields
    fields = []
    for gis_attribute in gis_attributes:
        if gis_attribute:
            fields.append(QgsField(gis_attribute, QtCore.QVariant.String))
    return fields

def make_links_layer(coordinates, links, model_attributes, gis_attributes, all_gis_attributes, layer):
    features = []
    for link in links:       # For each link, create a GIS feature
        try:
            inlet_coord = coordinates[link.inlet_node]
            outlet_coord = coordinates[link.outlet_node]
            feature = QgsFeature()
            points = [QgsPoint(float(inlet_coord.x), float(inlet_coord.y))]
            for vertex_pair in link.vertices:  # Add any intermediate points between inlet and outlet
                points.append(QgsPoint(float(vertex_pair.x), float(vertex_pair.y)))
            points.append(QgsPoint(float(outlet_coord.x), float(outlet_coord.y)))
            feature.setGeometry(QgsGeometry.fromPolyline(points))

            values = gis_values_from_model(link, model_attributes, gis_attributes, all_gis_attributes)
            feature.setAttributes(values)
            features.append(feature)
        except Exception as exLink:
            print("Skipping link " + link.name + ": " + str(exLink))
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
            print ("Skipping point " + model_point.name + ": " + str(exPoint))

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

def import_from_gis_piecemeal(session, file_name):
    # importable_sections = [session.project.pipes, session.project.pumps, session.project.valves]
    # already_populated_sections = [section for section in importable_sections if len(section.value) > 0]
    project = session.project
    num_existing_junctions = len(project.junctions.value)

    if session.model == "EPANET":
        section = project.pipes
        link_type = Pipe
        model_attributes = pipe_model_attributes
        gis_attributes = pipe_gis_attributes
        junction_type = EpanetJunction
    else:
        section = project.conduits
        link_type = Conduit
        model_attributes = conduit_model_attributes
        gis_attributes = conduit_gis_attributes
        junction_type = SwmmJunction

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

    result = import_links(session, section.value, file_name, model_attributes, gis_attributes, link_type, junction_type)
    if len(project.junctions.value) > num_existing_junctions:
        session.model_layers.junctions = session.map_widget.addCoordinates(project.junctions.value, "Junctions")

    if session.model == "EPANET":
        session.model_layers.pipes = session.map_widget.addLinks(project.all_nodes(),
                                                                 section.value, "Pipes", QtGui.QColor('gray'), 3)
    else:
        session.model_layers.conduits = session.map_widget.addLinks(project.all_nodes(),
                                                                    section.value, "Conduits", QtGui.QColor('gray'), 3.5)
    session.model_layers.set_lists()
    session.map_widget.zoomfull()
    return result

def import_from_gis(session, file_name):
    try:
        directory = session.program_settings.value("GISPath", os.path.dirname(session.project.file_name))
        if file_name and str(file_name).lower().endswith("json"):
            path_only, file_only = os.path.split(file_name)
            if path_only != directory:  # Save path as default for next import/export operation
                session.program_settings.setValue("GISPath", path_only)
                session.program_settings.sync()

            if session.model == "EPANET":
                import_summary = import_epanet_from_geojson(session, file_name)
                result = "imported objects:" + os.linesep
                for et in import_summary:
                    result = result + et + ": " + str(import_summary[et]) + " objects" + os.linesep
            elif session.model == "SWMM":
                import_summary = import_swmm_from_geojson(session, file_name)
                result = "imported objects:" + os.linesep
                for et in import_summary:
                    result = result + et + ": " + str(import_summary[et]) + " objects" + os.linesep
        else:
            result = "Create Model from GIS data supports GeoJSON data only"
        QMessageBox.information(None, "Create Model from GIS data", result, QMessageBox.Ok)
    except Exception as ex:
        print (str(ex))

def import_epanet_from_geojson(session, file_name):
    project = session.project
    layer = QgsVectorLayer(file_name, "temp", "ogr")
    ind = layer.fieldNameIndex(u'element_type')
    if ind < 0:
        return
    elem_types = layer.uniqueValues(ind, 20)
    import_items_count = {}
    for et in elem_types:
        import_items_count[et.lower()] = 0
    model_item = None
    model_layer = None
    # layer.startEditing()
    for f in layer.getFeatures():
        geom = f.geometry()
        elem_type = f.attributes()[ind]
        if not elem_type:
            continue
        if elem_type.lower().startswith("junction"):
            model_layer = session.model_layers.junctions
            model_item = EpanetJunction()
            build_model_object_per_geojson_record(project, f, junction_import_attributes, model_item)
            project.junctions.value.append(model_item)
            import_items_count["junction"] += 1
        elif elem_type.lower().startswith("tank"):
            model_layer = session.model_layers.tanks
            model_item = EpanetTank()
            build_model_object_per_geojson_record(project, f, tank_import_attributes, model_item)
            project.tanks.value.append(model_item)
            import_items_count["tank"] += 1
        elif elem_type.lower().startswith("reservoir"):
            model_layer = session.model_layers.reservoirs
            model_item = Reservoir()
            build_model_object_per_geojson_record(project, f, reservoir_import_attributes, model_item)
            project.reservoirs.value.append(model_item)
            import_items_count["reservoir"] += 1
        elif elem_type.lower().startswith("label"):
            model_layer = session.model_layers.labels
            model_item = Label()
            build_model_object_per_geojson_record(project, f, label_import_attributes, model_item)
            project.labels.value.append(model_item)
            import_items_count["label"] += 1
        elif elem_type.lower().startswith("pipe"):
            model_layer = session.model_layers.pipes
            model_item = Pipe()
            build_model_object_per_geojson_record(project, f, pipe_import_attributes, model_item)
            project.pipes.value.append(model_item)
            import_items_count["pipe"] += 1
        elif elem_type.lower().startswith("pump"):
            model_layer = session.model_layers.pumps
            model_item = Pump()
            build_model_object_per_geojson_record(project, f, pump_import_attributes, model_item)
            project.pumps.value.append(model_item)
            import_items_count["pump"] += 1
        elif elem_type.lower().startswith("valve"):
            model_layer = session.model_layers.valves
            model_item = Valve()
            build_model_object_per_geojson_record(project, f, valve_import_attributes, model_item)
            project.valves.value.append(model_item)
            import_items_count["valve"] += 1

        # add gis feature
        new_feature = QgsFeature()
        new_feature.setGeometry(geom)
        if geom.type() == QGis.Point:
            new_feature.setAttributes([model_item.name, 0.0, 0.0])
            model_item.x = geom.asPoint().x()
            model_item.y = geom.asPoint().y()
        elif geom.type() == QGis.Line:
            new_feature.setAttributes([model_item.name, 0.0, model_item.inlet_node, model_item.outlet_node, 0, 0.0, 0.0])
            line = geom.asPolyline()
            if len(line) > 2:
                for i in xrange(1, len(line)):
                    coord = Coordinate()
                    coord.x = str(line[i].x())
                    coord.y = str(line[i].y())
                    model_item.vertices.append(coord)
                    pass
        elif geom.type() == QGis.Polygon:
            new_feature.setAttributes([model_item.name, 0.0, 0, "0", 0.0])
        #model_layer = QgsVectorLayer()
        model_layer.startEditing()
        model_layer.addFeature(new_feature)
        model_layer.commitChanges()
        model_layer.updateExtents()

    # layer.rollBack(True)
    session.model_layers.set_lists()
    session.map_widget.zoomfull()
    return import_items_count

def import_swmm_from_geojson(session, file_name):
    project = session.project
    layer = QgsVectorLayer(file_name, "temp", "ogr")
    ind = layer.fieldNameIndex(u'element_type')
    if ind < 0:
        return
    elem_types = layer.uniqueValues(ind, 20)
    import_items_count = {}
    for et in elem_types:
        import_items_count[et.lower()] = 0
    model_item = None
    model_layer = None
    p_section = None
    # layer.startEditing()
    adding_subcatchment = False
    sub_outlet = ""
    for f in layer.getFeatures():
        adding_subcatchment = False
        sub_outlet = None
        geom = f.geometry()
        elem_type = f.attributes()[ind]
        if not elem_type:
            continue
        p_section = None
        if elem_type.lower().startswith("junction"):
            model_layer = session.model_layers.junctions
            model_item = SwmmJunction()
            build_model_object_per_geojson_record(project, f, junction_import_attributes_swmm, model_item)
            p_section = project.junctions
        elif elem_type.lower().startswith("conduit"):
            model_layer = session.model_layers.conduits
            model_item = Conduit()
            build_model_object_per_geojson_record(project, f, conduit_import_attributes, model_item)
            p_section = project.conduits
        elif elem_type.lower().startswith("raingage"):
            model_layer = session.model_layers.raingages
            model_item = RainGage()
            build_model_object_per_geojson_record(project, f, raingage_import_attributes, model_item)
            p_section = project.raingages
        elif elem_type.lower().startswith("label"):
            model_layer = session.model_layers.labels
            model_item = Label()
            build_model_object_per_geojson_record(project, f, label_import_attributes, model_item)
            p_section = project.labels
        elif elem_type.lower().startswith("outfall"):
            model_layer = session.model_layers.outfalls
            model_item = Outfall()
            build_model_object_per_geojson_record(project, f, outfall_import_attributes, model_item)
            p_section = project.outfalls
        elif elem_type.lower().startswith("divider"):
            model_layer = session.model_layers.dividers
            model_item = Divider()
            build_model_object_per_geojson_record(project, f, divider_import_attributes, model_item)
            p_section = project.dividers
        elif elem_type.lower().startswith("subcatchment"):
            adding_subcatchment = True
            # sub_outlet = session.project.all_nodes()[f["outlet"]]
            sub_outlet = f["outlet"]
            model_layer = session.model_layers.subcatchments
            model_item = Subcatchment()
            build_model_object_per_geojson_record(project, f, subcatchment_import_attributes, model_item)
            pt = f.geometry().centroid().asPoint()
            model_item.centroid.x = str(pt.x())
            model_item.centroid.y = str(pt.y())
            p_section = project.subcatchments
        elif elem_type.lower().startswith("storageunit"):
            model_layer = session.model_layers.storage
            model_item = StorageUnit()
            build_model_object_per_geojson_record(project, f, storage_import_attributes, model_item)
            if model_item.storage_curve and model_item.storage_curve.lower() <> 'none':
                model_item.storage_curve_type = StorageCurveType.TABULAR
            #if model_item.coefficient or model_item.constant or model_item.exponent:
            #    model_item.storage_curve_type = StorageCurveType.FUNCTIONAL
            p_section = project.storage
        elif elem_type.lower().startswith("pump"):
            model_layer = session.model_layers.pumps
            model_item = SwmmPump()
            build_model_object_per_geojson_record(project, f, pump_import_attributes_swmm, model_item)
            p_section = project.pumps
        elif elem_type.lower().startswith("orifice"):
            model_layer = session.model_layers.orifices
            model_item = Orifice()
            build_model_object_per_geojson_record(project, f, orifice_import_attributes, model_item)
            p_section = project.orifices
        elif elem_type.lower().startswith("weir"):
            model_layer = session.model_layers.weirs
            model_item = Weir()
            build_model_object_per_geojson_record(project, f, weir_import_attributes, model_item)
            p_section = project.weirs
        elif elem_type.lower().startswith("outlet"):
            model_layer = session.model_layers.outlets
            model_item = Outlet()
            build_model_object_per_geojson_record(project, f, outlet_import_attributes, model_item)
            p_section = project.outlets

        if len(p_section.value) == 0 and not isinstance(p_section, list):
            p_section.value = IndexedList([], ['name'])
        p_section.value.append(model_item)
        import_items_count[elem_type.lower()] += 1

        # add gis feature
        new_feature = QgsFeature()
        new_feature.setGeometry(geom)
        if geom.type() == QGis.Point:
            new_feature.setAttributes([model_item.name, 0.0, 0.0])
            model_item.x = geom.asPoint().x()
            model_item.y = geom.asPoint().y()
        elif geom.type() == QGis.Line:
            new_feature.setAttributes([model_item.name, 0.0, model_item.inlet_node, model_item.outlet_node, 0, 0.0, 0.0])
            line = geom.asPolyline()
            if len(line) > 2:
                for i in xrange(1, len(line)):
                    coord = Coordinate()
                    coord.x = str(line[i].x())
                    coord.y = str(line[i].y())
                    model_item.vertices.append(coord)
                    pass
        elif geom.type() == QGis.Polygon:
            new_feature.setAttributes([model_item.name, 0.0, 0, "0", 0.0])
            for pt in geom.asPolygon()[0]:
                coord = Coordinate()
                coord.x = str(pt.x())
                coord.y = str(pt.y())
                model_item.vertices.append(coord)

        #model_layer = QgsVectorLayer()
        model_layer.startEditing()
        added_sub = model_layer.dataProvider().addFeatures([new_feature])

        if adding_subcatchment and added_sub[0]:
            centroid_layer = session.model_layers.subcentroids
            sublink_layer = session.model_layers.sublinks
            if centroid_layer and sublink_layer:
                c_item = SubCentroid()
                c_item.name = u'subcentroid-' + model_item.name
                c_item.subname = model_item.name
                p_section = session.project.subcentroids
                if len(p_section.value) == 0 and not isinstance(p_section, list):
                    p_section.value = IndexedList([], ['name'])
                p_section.value.append(c_item)
                fc = QgsFeature()
                centroid_layer.startEditing()
                pf = session.map_widget.point_feature_from_item(model_item.centroid)
                pf.setAttributes([c_item.name, 0.0, added_sub[1][0].id(), model_item.name])
                added_centroid = centroid_layer.dataProvider().addFeatures([pf])
                if added_centroid[0]:
                    added_centroid_id = added_centroid[1][0].id()
                    model_layer.changeAttributeValue(added_sub[1][0].id(), 2, added_centroid[1][0].id())
                    model_layer.changeAttributeValue(added_sub[1][0].id(), 3, c_item.name)
                    centroid_layer.updateExtents()
                    centroid_layer.commitChanges()
                    centroid_layer.triggerRepaint()

                l_item = SubLink()
                l_item.name = u'sublink-' + c_item.name
                l_item.inlet_node = c_item.name
                l_item.outlet_node = sub_outlet
                p_section = session.project.sublinks
                if len(p_section.value) == 0 and not isinstance(p_section, list):
                    p_section.value = IndexedList([], ['name'])
                p_section.value.append(l_item)
                inlet_sub = model_item.centroid
                lf = session.map_widget.line_feature_from_item(l_item,
                                                               session.project.all_nodes(),
                                                               inlet_sub, None)
                sublink_layer.startEditing()
                added_lf = sublink_layer.dataProvider().addFeatures([lf])
                if added_lf[0]:
                    # set subcatchment's outlet nodal/subcatch id
                    # if inlet_sub and model_item.name:
                    #    for s in session.project.subcatchments.value:
                    #        if s.name == model_item.name:
                    #            s.outlet = model_item.outlet_node
                    #            break
                    sublink_layer.changeAttributeValue(added_lf[1][0].id(), 2, l_item.inlet_node)
                    sublink_layer.changeAttributeValue(added_lf[1][0].id(), 3, l_item.outlet_node)
                    sublink_layer.changeAttributeValue(added_lf[1][0].id(), 4, 0)
                    sublink_layer.updateExtents()
                    sublink_layer.commitChanges()
                    sublink_layer.triggerRepaint()
                    session.map_widget.canvas.refresh()

                pass
        model_layer.commitChanges()

    # layer.rollBack(True)
    session.model_layers.junctions.updateExtents()
    session.model_layers.junctions.triggerRepaint()
    session.map_widget.canvas.refresh()
    session.model_layers.set_lists()
    session.map_widget.zoomfull()
    return import_items_count

def build_model_object_per_geojson_record(project, f, import_attributes, model_item):
    new_source_quality = None
    new_demand = None
    for attr_name in import_attributes:
        if f.fieldNameIndex(attr_name) >=0:
            attr_value = f.attributes()[f.fieldNameIndex(attr_name)]
            if attr_name == "id":
                model_item.name = attr_value
            elif attr_name == "description" and attr_value:
                if isinstance(model_item, Label):
                    model_item.name = attr_value
                else:
                    if hasattr(model_item, attr_name):
                        setattr(model_item, attr_name, attr_value)
            elif attr_name.startswith("source_quality_amount"):
                val, val_is_good = ParseData.floatTryParse(attr_value)
                if val_is_good:
                    new_source_quality = Source()
                    new_source_quality.name = model_item.name
                    new_source_quality.baseline_strength = attr_value
                    project.sources.value.append(new_source_quality)
            elif attr_name.startswith("source_quality_pattern"):
                if new_source_quality:
                    new_source_quality.pattern_name = attr_value
            elif attr_name.startswith("source_quality_type"):
                if new_source_quality:
                    for et in SourceType:
                        if et.name == attr_value:
                            new_source_quality.pattern_name = attr_value
                            break
            elif attr_name.startswith("base_demand"):
                new_demand = Demand()
                new_demand.junction_name = model_item.name
                val, val_is_good = ParseData.floatTryParse(attr_value)
                if val_is_good:
                    new_demand.base_demand = attr_value
                ctr = attr_name[attr_name.rindex("_") + 1:]
                val, val_is_good = ParseData.intTryParse(ctr)
                if val_is_good:
                    project.demands.value.append(new_demand)
            elif attr_name.startswith("demand_pattern"):
                if new_demand:
                    ctr = attr_name[attr_name.rindex("_") + 1:]
                    val, val_is_good = ParseData.intTryParse(ctr)
                    if val_is_good:
                        new_demand = project.demands.value[val - 1]
                        new_demand.demand_pattern = attr_value
            elif attr_name.startswith("demand_category"):
                if new_demand:
                    ctr = attr_name[attr_name.rindex("_") + 1:]
                    val, val_is_good = ParseData.intTryParse(ctr)
                    if val_is_good:
                        new_demand = project.demands.value[val - 1]
                        new_demand.category = attr_value
            elif attr_name.startswith("initial_status") or attr_name.startswith("status"):
                if attr_value and not attr_value == NULL:
                    if hasattr(model_item, attr_name):
                        if attr_value.lower() == "open":
                            model_item.initial_status = FixedStatus.OPEN
                        elif attr_value.lower() == "closed":
                            model_item.initial_status = FixedStatus.CLOSED
                        else:
                            model_item.initial_status = attr_value
            elif attr_name.startswith("meter_type"):
                for mt in MeterType:
                    if mt.name == attr_value:
                        model_item.meter_type = mt
                        break
            elif attr_name.startswith("mixing_"):
                if attr_value:
                    for mm in MixingModel:
                        if mm.name == attr_value.upper():
                            model_item.mixing_model = mm
                            break
            elif attr_name.startswith("subarea_routing"):
                if attr_value:
                    for r in Routing:
                        if r.name == attr_value.upper():
                            model_item.subarea_routing = r
                            break
            elif attr_name.startswith("outfall_type"):
                if attr_value:
                    for ot in OutfallType:
                        if ot.name == attr_value.upper():
                            model_item.outfall_type = ot
                            break
            elif attr_name.startswith("rain_format"):
                if attr_value:
                    for rf in RainFormat:
                        if rf.name == attr_value.upper():
                            model_item.rain_format = rf
                            break
            elif attr_name.startswith("rain_file_units"):
                if attr_value:
                    for rf in RainFileUnits:
                        if rf.name == attr_value.upper():
                            model_item.data_file_rain_units = rf
                            break
            elif attr_name.startswith("rain_data_source"):
                if attr_value:
                    for rf in RainDataSource:
                        if rf.name == attr_value.upper():
                            model_item.data_source = rf
                            break
            elif attr_name == "type":
                if attr_value and isinstance(model_item, Weir):
                    for wf in WeirType:
                        if wf.name == attr_value.upper():
                            model_item.type = wf
                            break
            elif attr_name == "road_surface":
                if attr_value:
                    for rsf in RoadSurfaceType:
                        if rsf.name == attr_value.upper():
                            model_item.road_surface = rsf
                            break
            elif attr_name == "curve_type":
                if attr_value and isinstance(model_item, Outlet):
                    for oct in OutletCurveType:
                        if oct.name == attr_value.upper():
                            model_item.curve_type = oct
                            break
            elif attr_name == "flow_divider_type":
                if attr_value and isinstance(model_item, Divider):
                    for fdt in FlowDividerType:
                        if fdt.name == attr_value.upper():
                            model_item.flow_divider_type = fdt
                            break
            else:
                if attr_value and not attr_value == NULL:
                    if hasattr(model_item, attr_name):
                        setattr(model_item, attr_name, attr_value)

def import_links(session, links, file_name, model_attributes, gis_attributes, model_type, junction_type):
    """ Read GIS vector layer in file_name into links list.
    Args:
        project: SWMM or EPANET project to import into, used for access to its all_coordinates method and junctions
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
            field_len = 20
            if layer.storageType() == u'ESRI Shapefile':
                field_len = 10
            session.map_widget.set_crs_from_layer(layer)
            project = session.project
            attributes = zip(model_attributes, gis_attributes)
            coordinates = project.all_nodes()
            for feature in layer.getFeatures():
                geom = feature.geometry()
                if geom.type() == QGis.Line:
                    line = geom.asPolyline()
                    item_name = ''
                    for model_attribute, gis_attribute in attributes:
                        if model_attribute == "name":
                            item_name = feature[gis_attribute[:field_len]]
                            break
                    try:
                        model_item = links[item_name]
                    except:
                        model_item = model_type()
                        links.append(model_item)
                    for model_attribute, gis_attribute in attributes:
                        try:
                            attr_value = feature[gis_attribute[:field_len]]
                            setattr(model_item, model_attribute, attr_value)

                            # If this attribute is the inlet or outlet node, make sure project has its coordinates
                            index = -1
                            if model_attribute == "inlet_node":
                                index = 0
                            elif model_attribute == "outlet_node":
                                index = len(line) - 1
                            if index >= 0:
                                try:     # Keep node if it already exists in model, but update its coordinates
                                    this_coord = coordinates[attr_value]
                                except:  # Create new node since model does not already have this one
                                    this_coord = junction_type()
                                    this_coord.name = attr_value
                                    project.junctions.value.append(this_coord)
                                    coordinates.append(this_coord)
                                this_coord.x = line[index].x()
                                this_coord.y = line[index].y()
                        except Exception as ex_attr:
                            print("Could not read GIS attribute '" + gis_attribute + "' into '" + model_attribute + "'")
                    count += 1
    except Exception as ex:
        print(str(ex))
    return "Imported " + str(count) + " " + model_type.__name__ + "s"


def import_epanet_pipes(session, file_name, model_attributes, gis_attributes):
    project = session.project
    section = project.pipes

    result = import_links(session, section.value, file_name, model_attributes, gis_attributes, Pipe, EpanetJunction)
    session.model_layers.junctions = session.map_widget.addCoordinates(project.junctions.value, "Junctions")
    session.model_layers.pipes = session.map_widget.addLinks(project.all_nodes(),
                                                             section.value, "Pipes", QtGui.QColor('gray'), 3)
    session.model_layers.set_lists()
    session.map_widget.zoomfull()
    return result


def import_nodes(session, nodes, file_name, model_attributes, gis_attributes, model_type):
    """ Read GIS vector layer in file_name into nodes list.
    Args:
        session: current session containing SWMM or EPANET project to import into
        nodes: list of project objects to populate.
        file_name: GIS file to read.
        model_attributes: attribute names of the model objects in nodes list.
        gis_attributes: name of attributes as they exist in file_name.
        model_type: type of node to create

    Notes:
        model_attributes and gis_attributes must be aligned with each other.
        Each value found by gis_attribute is assigned to the model_attribute in the same position in its array.
        If model_attribute is "inlet_node" or "outlet_node" these are added to project.junctions.
    """
    count = 0
    try:
        layer = QgsVectorLayer(file_name, "import", "ogr")
        if layer:
            session.map_widget.set_crs_from_layer(layer)
            attributes = zip(model_attributes, gis_attributes)
            for feature in layer.getFeatures():
                geom = feature.geometry()
                if geom.type() == QGis.Point:
                    item_name = ''
                    for model_attribute, gis_attribute in attributes:
                        if model_attribute == "name":
                            item_name = feature[gis_attribute]
                            break
                    try:  # update item if it already exists in model
                        model_item = nodes[item_name]
                    except:  # add item if it does not already exist in model
                        model_item = model_type()
                        model_item.name = item_name
                        nodes.append(model_item)
                    geo_pt = geom.asPoint()
                    model_item.x = geo_pt.x()
                    model_item.y = geo_pt.y()

                    for model_attribute, gis_attribute in attributes:
                        attr_value = ''
                        try:
                            attr_value = feature[gis_attribute]
                            setattr(model_item, model_attribute, attr_value)
                        except Exception as ex_attr:
                            print("Could not read GIS attribute '" + gis_attribute + "'='" + attr_value +
                                  "' into '" + model_attribute + "'")
                    count += 1
    except Exception as ex:
        print(str(ex))
    return "Imported " + str(count) + " " + model_type.__name__ + "s"


def import_epanet_junctions(session, file_name, model_attributes, gis_attributes):
    project = session.project
    section = project.junctions

    result = import_nodes(session, section.value, file_name, model_attributes, gis_attributes, EpanetJunction)
    session.model_layers.junctions = session.map_widget.addCoordinates(section.value, "Junctions")
    session.model_layers.set_lists()
    session.map_widget.zoomfull()
    return result


def import_epanet_tanks(session, file_name, model_attributes, gis_attributes):
    project = session.project
    section = project.tanks

    result = import_nodes(session, section.value, file_name, model_attributes, gis_attributes, EpanetTank)
    session.model_layers.tanks = session.map_widget.addCoordinates(section.value, "Tanks")
    session.model_layers.set_lists()
    session.map_widget.zoomfull()
    return result
