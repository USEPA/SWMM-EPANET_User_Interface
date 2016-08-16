from qgis.core import *
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from core.coordinate import Coordinate
from core.epanet.hydraulics.link import Pipe, Pump, Valve


def import_from_gis(session, file_name):
    importable_sections = [session.project.pipes, session.project.pumps, session.project.valves]
    already_populated_sections = [section for section in importable_sections if len(section.value) > 0]

    if already_populated_sections:
        msg = QMessageBox()
        msg.setText("Discard " + str(len(section.value)) + " pipes already in model before import?")
        msg.setWindowTitle("Importing Pipes")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        choice = msg.exec_()
        if choice == QMessageBox.Yes:
            section.value = []
        elif choice == QMessageBox.No:
            pass
        elif choice == QMessageBox.Cancel:
            return

    section = session.project.pipes
    model_attributes = [
        "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    gis_attributes = [
        "name", "description", "inlet_node", "outlet_node", "length", "diameter", "roughness", "loss_coefficient"]
    """ Mapping of attribute names in vector layer to attribute names of model objects.
        Edit gis_attributes as needed to match layer being imported.
        If a field is not available in the GIS layer, remove the field from both lists.
    """
    result = import_links(session.project, section.value, file_name, model_attributes, gis_attributes, Pipe)
    session.map_widget.addLinks(session.project.coordinates.value,
                                section.value, "Pipes", "name", QtGui.QColor('gray'))

    session.map_widget.zoomfull()
    return result


def import_links(project, links, file_name, model_attributes, gis_attributes, model_type):
    count = 0
    try:
        layer = QgsVectorLayer(file_name, "import", "ogr")
        if layer:
            coordinates = project.coordinates.value
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
                            for existing_coord in coordinates:
                                if existing_coord.name == attr_value:
                                    project.coordinates.value.remove(existing_coord)
                            new_coord = Coordinate()
                            new_coord.name = attr_value
                            new_coord.x = line[index].x()
                            new_coord.y = line[index].y()
                            coordinates.append(new_coord)
                    links.append(model_item)
                    count += 1
    except Exception as ex:
        print(str(ex))
    return "Imported " + str(count) + " features"

