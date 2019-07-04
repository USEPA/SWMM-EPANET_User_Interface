try:
    from qgis.core import *
    from qgis.gui import *

    # from qgis.core import QgsProject, QgsFeatureRequest
    # from qgis.gui import QgsMapToolZoom, QgsMapToolPan
    # from qgis.core import QgsVectorLayer, QgsExpression, QgsFeature, QgsGeometry, QgsPoint, QgsField
    # from qgis.core import QgsMarkerSymbol, QgsSimpleMarkerSymbolLayer, QgsSvgMarkerSymbolLayer, QgsPalLayerSettings
    # from qgis.core import QgsSingleSymbolRenderer, QgsSimpleLineSymbolLayer
    # from qgis.core import QgsMapLayer
    from PyQt5 import QtGui, QtCore, Qt
    from PyQt5.QtCore import QSettings
    from PyQt5.QtGui import *
    from PyQt5.Qt import *
    from PyQt5.QtWidgets import *
    from core.coordinate import Coordinate, Polygon
    from .svgs_rc import *
    from .qgis_icons_rc import *
    import traceback
    import math
    import os
    import sys
    from enum import Enum
    from .map_edit import EditTool
    from ui.model_utility import ParseData


    class EmbedMap(QWidget):
        """ Main GUI Widget for map display inside vertical layout """

        QGis_UnitType = ["Meters", "Feet", "Degrees", "Unknown", "DecimalDegree", "DegreesMinutesSeconds",
                         "DegreesDecimalMinutes"]
        map_unit_names       = ["Meters", "Kilometers", "Feet", "NauticalMiles", "Yards", "Miles", "Degrees", "Unknown"]
        map_unit_abbrev      = ["m",      "km",         "ft",   "nmi",           "yd",    "mi",    "deg",     ""]
        map_unit_to_meters   = [1.0,         1000.0,    0.3048,   1852,          0.9144,  1609.34, 0,         0]
        map_unit_to_feet     = [3.28084,     3280.84,   1.0,      6076.12,       3.0,     5280.0,  0,         0]
        map_unit_to_hectares = [0.0001,      100,       9.2903e-6, 342.99,    8.36127e-5, 259,     0,         0]
        map_unit_to_acres    = [0.000247105, 247.105,   2.2957e-5, 847.548,  0.000206612, 640,     0,         0]

        def __init__(self, canvas, session, main_form=None, qgs_project=None, **kwargs):
            super(EmbedMap, self).__init__(main_form)
            self.canvas = canvas  # QgsMapCanvas()
            self.canvas.setMouseTracking(True)
            # self.canvas.useImageToRender(False)
            # self.canvas.setCanvasColor(QtGui.QColor.white)
            self.qgs_project = qgs_project
            QSettings().setValue("/Qgis/digitizing/marker_only_for_selected", False)

            # root = QgsProject.instance().layerTreeRoot()
            root = self.qgs_project.layerTreeRoot()
            self.project_group = root.addGroup("Project Objects")
            self.nodes_group = self.project_group.addGroup("Nodes")
            self.links_group = self.project_group.addGroup("Links")
            self.other_group = root.addGroup("Others")
            self.base_group = root.addGroup("Base Maps")
            self.layer_styles = {}
            # self.flowdir_symlayer = QgsSvgMarkerSymbolLayerV2(':/icons/svg/flow_dir.svg')

            # first thoughts about adding a legend - may be barking up wrong tree...
            # self.root = QgsProject.instance().layerTreeRoot()
            # self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
            #
            # self.model = QgsLayerTreeModel(self.root)
            # self.model.setFlag(QgsLayerTreeModel.ShowLegend)
            # self.view = QgsLayerTreeView()
            # self.view.setModel(self.model)
            #
            # self.LegendDock = QDockWidget("Layers", self)
            # self.LegendDock.setObjectName("layers")
            # self.LegendDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
            # self.LegendDock.setWidget(self.view)
            # self.LegendDock.setContentsMargins(9, 9, 9, 9)
            # self.canvas.addDockWidget(Qt.LeftDockWidgetArea, self.LegendDock)

            self.canvas.show()

            self.session = session

            self.panTool = QgsMapToolPan(self.canvas)
            self.panTool.setAction(self.session.actionPan)

            self.zoomInTool = QgsMapToolZoom(self.canvas, False)
            self.zoomInTool.setAction(self.session.actionZoom_in)

            self.zoomOutTool = QgsMapToolZoom(self.canvas, True)
            self.zoomOutTool.setAction(self.session.actionZoom_out)

            self.selectTool = None
            self.selectVertexTool = None
            self.addObjectTool = None
            self.addPolygonTool = None

            self.qgisNewFeatureTool = None
            self.measureTool = None
            self.selectRegionTool = None
            self.translateCoordTool = None
            self.map_linear_unit = self.map_unit_names[7]  # Unknown
            self.coord_origin = Coordinate()
            self.coord_fext = Coordinate()
            self.coord_fext.x = 100000.0
            self.coord_fext.y = 100000.0

            self.canvas.xyCoordinates.connect(self.canvasMoveEvent)

            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.canvas)

            #contents = QWidget()
            #contents.setLayout(layout)

            self.setLayout(layout)
            #self.setCentralWidget(self)

            #layout.addWidget(None)
            self.setMouseTracking(True)

            self.refresh_extent_needed = True
            self.feature_request = QgsFeatureRequest()

        def do_label(self, layer):
            if not layer or not layer.isValid():
                return False
            lyr_name = layer.name()
            try:
                lyr_name = lyr_name[0:lyr_name.index(' [')]
            except ValueError as e:
                lyr_name = layer.name()
            if self.session.project_settings.config.value(lyr_name + '-label') == 'Off':
                return False
            return True

        def process_name_change(self, section, old_name, item):
            # Note: old_named element is already replaced with the new_named item
            obj_type = type(section.value[0]).__name__
            edit_lyr = self.session.model_layers.find_layer_by_name(obj_type)
            # lyr = QgsVectorLayer()
            edit_provider = edit_lyr.dataProvider()
            for f_edit in edit_provider.getFeatures(QgsFeatureRequest(QgsExpression('"name"=' + "'" + old_name + "'"))):
                # update GIS layer item name
                vfi = f_edit.fieldNameIndex('name')
                edit_provider.changeAttributeValues({f_edit.id(): {vfi: str(item.name)}})

                if edit_lyr in self.session.model_layers.nodes_layers:
                    # need to find all subcatch and all links to it
                    all_links = self.session.model_layers.links_layers
                    if self.session.model == 'SWMM':
                        all_links.extend([self.session.model_layers.sublinks])
                    for lyr in all_links:
                        provider = lyr.dataProvider()
                        neighbors = provider.getFeatures(QgsFeatureRequest().setFilterRect(f_edit.geometry().boundingBox()))
                        for line_feature in neighbors:
                            if f_edit.geometry().intersects(line_feature.geometry()):
                                inlet_updated = False
                                outlet_updated = False
                                vfi = -1
                                if line_feature['inlet'] == old_name:
                                    vfi = line_feature.fieldNameIndex('inlet')
                                    inlet_updated = True
                                elif line_feature['outlet'] == old_name:
                                    vfi = line_feature.fieldNameIndex('outlet')
                                    outlet_updated = True
                                if vfi >= 0:
                                    provider.changeAttributeValues({line_feature.id(): {vfi: str(item.name)}})
                                # update the corresponding model link object
                                link_name = line_feature['name']
                                link_section = self.session.project.find_section(lyr.name())
                                link_to_update = link_section.find_item(link_name)
                                if link_to_update:
                                    if link_to_update.inlet_node == old_name:
                                        link_to_update.inlet_node = item.name
                                    elif link_to_update.outlet_node == old_name:
                                        link_to_update.outlet_node = item.name
                                if lyr.name() == 'sublinks': # find its sub source
                                    sub_name = link_name[len('sublink-'):]
                                    sub = self.session.project.subcatchments.find_item(sub_name)
                                    if sub and sub.outlet == old_name:
                                        sub.outlet = item.name
                                    pass
                        pass
                    pass
                elif edit_lyr in self.session.model_layers.links_layers:
                    # no additional processing
                    pass
                elif self.session.model == 'SWMM' and edit_lyr.geometryType() == QgsWkbTypes.PolygonGeometry:
                    ind_c_mapid = f_edit.fieldNameIndex('c_mapid')
                    ind_c_modelid = f_edit.fieldNameIndex('c_modelid')
                    edit_provider.changeAttributeValues({f_edit.id(): {ind_c_modelid: 'subcentroid-' + item.name}})
                    cent_lyr = self.session.model_layers.subcentroids
                    sublink_lyr = self.session.model_layers.sublinks
                    cent_provider = cent_lyr.dataProvider()
                    sublink_provider = sublink_lyr.dataProvider()
                    ms_cent = self.session.project.subcentroids
                    ms_sublink = self.session.project.sublinks
                    for c_edit in cent_provider.getFeatures(QgsFeatureRequest(QgsExpression('"name"=' + "'subcentroid-" + old_name + "'"))):
                        vfi = c_edit.fieldNameIndex('name')
                        cent_provider.changeAttributeValues({c_edit.id(): {vfi: 'subcentroid-' + item.name}})
                        vfi = c_edit.fieldNameIndex('sub_modelid')
                        cent_provider.changeAttributeValues({c_edit.id(): {vfi: item.name}})
                        m_cent = ms_cent.find_item('subcentroid-' + old_name)
                        m_cent.name = 'subcentroid-' + item.name
                    for sl_edit in sublink_provider.getFeatures(QgsFeatureRequest(QgsExpression('"name"=' + "'sublink-" + old_name + "'"))):
                        vfi = sl_edit.fieldNameIndex('name')
                        sublink_provider.changeAttributeValues({sl_edit.id(): {vfi: 'sublink-' + item.name}})
                        vfi = sl_edit.fieldNameIndex('inlet')
                        sublink_provider.changeAttributeValues({sl_edit.id(): {vfi: 'subcentroid-' + item.name}})
                        m_sublink = ms_sublink.find_item('sublink-' + old_name)
                        m_sublink.name = 'sublink-' + item.name
                        m_sublink.inlet_node = 'subcentroid-' + item.name
                    pass
                pass

        def save_gis_settings(self):
            if self.session.project_settings is None:
                return
            if self.session.project_settings:
                if self.session.project.file_name:
                    pre, ext = os.path.splitext(self.session.project.file_name)
                    self.session.project_settings.config.setPath(QSettings.IniFormat, QSettings.UserScope, pre + ".ini")
                layers = self.other_group.findLayers()
                if len(layers) > 0:
                    self.session.project_settings.config.setValue("OtherMaps/" + r"layer_count", str(len(layers)))
                    layer_paths = ""
                    for nd in self.other_group.findLayers():
                        data_path = nd.layer().dataProvider().dataSourceUri()
                        if '|' in data_path:
                            data_path = data_path[0: data_path.rfind('|')]
                        layer_paths += data_path + "|"
                    self.session.project_settings.config.setValue("OtherMaps/" + r"layer_paths", layer_paths)
                else:
                    self.session.project_settings.config.setValue("OtherMaps/" + r"layer_count", "0")
                    self.session.project_settings.config.setValue("OtherMaps/" + r"layer_paths", "")

                layers = self.base_group.findLayers()
                if len(layers) > 0:
                    self.session.project_settings.config.setValue("BaseMaps/" + "layer_count", str(len(layers)))
                    layer_paths = ""
                    for nd in self.base_group.findLayers():
                        layer_paths += nd.layer().dataProvider().dataSourceUri() + "|"
                    self.session.project_settings.config.setValue("BaseMaps/" + r"layer_paths", layer_paths)
                else:
                    self.session.project_settings.config.setValue("BaseMaps/" + r"layer_count", "0")
                    self.session.project_settings.config.setValue("BaseMaps/" + r"layer_paths", "")

        def load_extra_layers(self):
            try:
                if 'OtherMaps/layer_paths' in self.session.project_settings.config.allKeys():
                    extra_layers = self.session.project_settings.config.value("OtherMaps/layer_paths").split("|")
                    for lyr_path in extra_layers:
                        self.addVectorLayer(lyr_path)
                if 'BaseMaps/layer_paths' in self.session.project_settings.config.allKeys():
                    extra_layers = self.session.project_settings.config.value("BaseMaps/layer_paths").split("|")
                    for lyr_path in extra_layers:
                        self.addRasterLayer(lyr_path)
            except:
                print("Adding extra layers failed.")

        def is_model_layer(self, alayer):
            if isinstance(alayer, QgsVectorLayer):
                if alayer in self.session.model_layers.all_layers:
                    return True
                else:
                    return False
            else:
                return False

        def setZoomInMode(self):
            if self.session.actionZoom_in.isChecked():
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                self.canvas.setMapTool(self.zoomInTool)
                #self.zoomInTool.setCursor(QtCore.Qt.CrossCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
            else:
                self.canvas.unsetMapTool(self.zoomInTool)
                #self.zoomInTool.setCursor(QtCore.Qt.ArrowCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
            pass

        def setZoomOutMode(self):
            if self.session.actionZoom_out.isChecked():
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                self.canvas.setMapTool(self.zoomOutTool)
                #self.zoomOutTool.setCursor(QtCore.Qt.SplitHCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.SplitHCursor)
            else:
                self.canvas.unsetMapTool(self.zoomOutTool)
                #self.zoomOutTool.setCursor(QtCore.Qt.ArrowCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
            pass

        def setPanMode(self):
            if self.session.actionPan.isChecked():
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                self.canvas.setMapTool(self.panTool)
                #self.panTool.setCursor(QtCore.Qt.OpenHandCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
            else:
                self.canvas.unsetMapTool(self.panTool)
                #self.panTool.setCursor(QtCore.Qt.ArrowCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

        def setSelectMode(self):
            QApplication.restoreOverrideCursor()
            if self.session.actionMapSelectObj.isChecked():
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                if self.canvas.layers():
                    self.selectTool = SelectMapTool(self.canvas, self.session)
                    if self.session.gis_layer_tree.currentLayer():
                        self.selectTool.auto_detect = False
                        self.selectTool.nearest_layer = self.session.gis_layer_tree.currentLayer()
                    self.selectTool.setAction(self.session.actionMapSelectObj)
                else:
                    self.selectTool = None
                if self.selectTool:
                    self.canvas.setMapTool(self.selectTool)
            else:
                self.canvas.unsetMapTool(self.selectTool)
                self.selectTool = None

        def setSelectVertexMode(self):
            if self.session.actionMapSelectVertices.isChecked():
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                if self.canvas.layers():
                    self.selectVertexTool = MoveVerticesTool(self.canvas, self.session)
                    self.selectVertexTool.setAction(self.session.actionMapSelectVertices)
                else:
                    self.selectVertexTool = None
                if self.selectVertexTool:
                    self.canvas.setMapTool(self.selectVertexTool)
            else:
                self.canvas.unsetMapTool(self.selectVertexTool)
                self.selectVertexTool = None

        def setEditVertexMode(self):
            layer = None
            if self.canvas.layers():
                layer = self.session.gis_layer_tree.currentLayer()
                if layer and layer.geometryType() == QgsWkbTypes.PointGeometry:
                    layer = None
                # for lyr in self.canvas.layers():
                #     if "subcatchment" in lyr.name().lower() or \
                #             "conduit" in lyr.name().lower():
                #         layer = lyr
                #         break
            if layer is None:
                if self.session.actionMapSelectVertices.isChecked():
                    self.session.actionMapMeasure.setChecked(False)
                    self.setMeasureMode()
                    self.session.actionMapSelectRegion.setChecked(False)
                    self.setSelectByRegionMode()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Need to select a GIS layer first")
                    msg.setWindowTitle("Edit Vertex")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    self.session.actionMapSelectVertices.setChecked(False)
                return
            if self.session.actionMapSelectVertices.isChecked():
                if self.canvas.layers():
                    layer.startEditing()
                    self.canvas.refresh()
                    self.selectVertexTool = EditTool(self.canvas, layer, self.session, self.session.onGeometryChanged)
                    self.selectVertexTool.setAction(self.session.actionMapSelectVertices)
                else:
                    self.selectVertexTool = None
                if self.selectVertexTool:
                    self.canvas.setMapTool(self.selectVertexTool)
            else:
                self.canvas.unsetMapTool(self.selectVertexTool)
                self.selectVertexTool = None
                #layer.commitChanges()
                if layer.isEditable():
                    buf = layer.editBuffer()
                    if len(buf.changedGeometries()) > 0:
                        reply = QMessageBox.question(None, "Confirm",
                                                 "Save changes to " + layer.name() + "?",
                                                 QMessageBox.Yes | QMessageBox.No,
                                                 QMessageBox.Yes)
                        if reply == QMessageBox.Yes:
                            for fid in buf.changedGeometries():
                                iterator = layer.getFeatures(QgsFeatureRequest().setFilterFid(fid))
                                ftarget = None
                                if iterator:
                                    ftarget = next(iterator)
                                if ftarget is not None:
                                    if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                                        self.session.update_model_object_vertices(layer.name(),
                                                                              ftarget.attributes()[0],
                                                                              ftarget.geometry().asMultiPolygon()[0][0])
                                    elif layer.geometryType() == QgsWkbTypes.LineGeometry:
                                        self.session.update_model_object_vertices(layer.name(),
                                                                                  ftarget.attributes()[0],
                                                                                  ftarget.geometry().asPolyline())
                                    pass
                            layer.commitChanges()
                        else:
                            layer.rollBack()
                    else:
                        layer.rollBack()
                        self.canvas.refresh()

        def setMeasureMode(self):
            if self.session.actionMapMeasure.isChecked():
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                if self.measureTool is None:
                    self.measureTool = CaptureTool(self.canvas, None, None, None, self.session)
                    self.measureTool.setMeasureMode(True)
                self.canvas.setMapTool(self.measureTool)
            else:
                if self.measureTool:
                    self.measureTool.stopCapturing()
                self.canvas.unsetMapTool(self.measureTool)

        def setSelectByRegionMode(self):
            if self.session.actionMapSelectRegion.isChecked():
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                if self.selectRegionTool is None:
                    self.selectRegionTool = CaptureRegionTool(self.canvas, None, None, None, self.session)
                self.canvas.setMapTool(self.selectRegionTool)
            else:
                if self.selectRegionTool:
                    self.selectRegionTool.stopCapturing()
                self.canvas.unsetMapTool(self.selectRegionTool)

        def setTranslateCoordinatesMode(self):
            if self.session.translating_coordinates:
                self.session.actionMapMeasure.setChecked(False)
                self.setMeasureMode()
                self.session.actionMapSelectRegion.setChecked(False)
                self.setSelectByRegionMode()
                if self.translateCoordTool is None:
                    self.translateCoordTool = ModelCoordinatesTranslationTool(self.canvas, self.session)
                self.canvas.setMapTool(self.translateCoordTool)
            else:
                self.canvas.unsetMapTool(self.translateCoordTool)

        def clearSelectableObjects(self):
            self.layer_spatial_indexes = []
            for layer in self.canvas.layers():
                if isinstance(layer, QgsVectorLayer):
                    layer.removeSelection()

        def find_feature(self, layer, feature_name):
            for feature in layer.getFeatures(QgsFeatureRequest(QgsExpression('"name"=' + "'" + feature_name + "'"))):
                return feature

        def setAddObjectMode(self, action_obj, layer_name, tool_type):
            """Start interactively adding points to point layer layer_name using tool button action_obj"""
            if self.addObjectTool:
                if not isinstance(self.addObjectTool,AddPointTool):
                    self.addObjectTool.stopCapturing()

            if action_obj.isChecked():
                # QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
                layer = getattr(self.session.model_layers, layer_name)
                self.session.select_named_items(layer, None)
                for obj_type, name in self.session.section_types.items():
                    if name == layer_name:
                        if self.addObjectTool:
                            QApplication.restoreOverrideCursor()
                            self.canvas.unsetMapTool(self.addObjectTool)

                        self.addObjectTool = tool_type(self.canvas, layer, layer_name, obj_type, self.session)
                        self.addObjectTool.setAction(action_obj)
                        self.canvas.setMapTool(self.addObjectTool)

            elif self.addObjectTool and self.addObjectTool.layer_name == layer_name:
                QApplication.restoreOverrideCursor()
                self.canvas.unsetMapTool(self.addObjectTool)
                self.addObjectTool = None

        def setAddFeatureMode(self):
            layer = self.session.current_map_layer()
            if layer:
                """This is an example method for interactively adding a polygon, need to make this add a subcatchment"""
                if self.session.actionAdd_Feature.isChecked():
                    if self.qgisNewFeatureTool is None:
                        if self.canvas.layers():
                            self.qgisNewFeatureTool = CaptureTool(self.canvas, self.canvas.layer(0),
                                                                  self.session.onGeometryAdded,
                                                                  CaptureTool.CAPTURE_POLYGON)
                            self.qgisNewFeatureTool.setAction(self.session.actionAdd_Feature)
                    if self.qgisNewFeatureTool:
                        self.canvas.setMapTool(self.qgisNewFeatureTool)
                else:
                    self.canvas.unsetMapTool(self.qgisNewFeatureTool)


            #from qgis.core import QgsStyleV2
            #from qgis.gui import QgsRendererV2PropertiesDialog
            #from qgis.utils import iface
            #renderer_v2_properties = QgsRendererV2PropertiesDialog(layer, QgsStyleV2.defaultStyle(), True)
            #renderer_v2_properties.show()
            #self.session._forms.append(renderer_v2_properties)

            # Test of activating QGIS properties editor, does not belong in this method
            # layer = self.canvas.layers()[0]
            # self.layer_properties_widget = QgsLayerPropertiesWidget(
            #         layer.rendererV2().symbol().symbolLayers()[0],
            #         layer.rendererV2().symbol(),
            #         layer)
            # self.layer_properties_widget.setMapCanvas(self.canvas)
            # self.layer_properties_widget.show()

        def move_labels_to_anchor_nodes(self, project, labels_layer):
            # if anchor nodes in use, move labels accordingly to anchor nodes
            # if not self.map_widget.canvas.extent().contains(self.map_widget.canvas.fullExtent()):
            for label in project.labels.value:
                if len(label.anchor_name) > 0:
                    # have an anchor node name, make sure it is real
                    found_node = False
                    found_x = 0.0
                    found_y = 0.0
                    if hasattr(project,'junctions'):
                        for point in project.junctions.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'outfalls'):
                        for point in project.outfalls.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'dividers'):
                        for point in project.dividers.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'storage'):
                        for point in project.storage.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'raingages'):
                        for point in project.raingages.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'subcentroids'):
                        for point in project.subcentroids.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'reservoirs'):
                        for point in project.reservoirs.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'tanks'):
                        for point in project.tanks.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y
                    if hasattr(project, 'sources'):
                        for point in project.sources.value:
                            if point.name == label.anchor_name:
                                found_node = True
                                found_x = point.x
                                found_y = point.y

                    if found_node:
                        # now move the label point
                        index = 0
                        for feature in labels_layer.dataProvider().getFeatures():
                            index += 1
                            if feature[0] == label.name:
                                labels_layer.startEditing()
                                labels_layer.changeGeometry(index, QgsGeometry.fromPointXY(QgsPointXY(float(found_x), float(found_y))), True)
                                labels_layer.commitChanges()

        def zoomfull(self):
            self.canvas.zoomToFullExtent()
            #self.set_extent(self.canvas.extent())

        def zoom_to_one_feature(self):
            for lyr in self.canvas.layers():
                if isinstance(lyr, QgsVectorLayer):
                    try:
                        for f in lyr.getFeatures():
                            lyr.selectByIds([f.id()])
                            box = lyr.boundingBoxOfSelected()
                            self.canvas.setExtent(box)
                            lyr.triggerRepaint()
                            return
                    except:
                        pass

        def setMouseTracking(self, flag):
            def recursive_set(parent):
                for child in parent.findChildren(QtCore.QObject):
                    try:
                        child.setMouseTracking(flag)
                    except:
                        pass
                    recursive_set(child)
            QWidget.setMouseTracking(self, flag)
            recursive_set(self)

        def canvasMoveEvent(self, p):
            try:
                unit_index = self.map_unit_names.index(self.map_linear_unit)
                u = self.map_unit_abbrev[unit_index]
            except:
                u = ''
            # x = '%g' % self.round_to_n(p.x(), 5)
            # y = '%g' % self.round_to_n(p.y(), 5)
            x = '%.3f' % p.x()
            y = '%.3f' % p.y()
            # pm = self.canvas.getCoordinateTransform().toMapCoordinates(p.x(), p.y())
            # x = ('%.5f' % pm.x()).rstrip('0').rstrip('.')
            # y = ('%.5f' % pm.y()).rstrip('0').rstrip('.')
            # coord_str = '{:s}, {:s} {:s}'.format(x, y, u)
            coord_btn = self.session.btnCoord
            coord_btn.setText('{:s}, {:s} {:s}'.format(x, y, u))
            btn_width = coord_btn.fontMetrics().boundingRect(coord_btn.text()).width() + 10.0
            coord_btn.setFixedWidth(btn_width)

        def get_features_by_attribute(self, layer, attribute, value,
                                      no_geometry=True,
                                      subset_attribute=True,
                                      get_ids_only=False):
            resultList = []
            try:
                ind = layer.dataProvider().fieldNameIndex(attribute)
                expr_text = "\"" + attribute + "\"='" + value + "'"
                expr = QgsExpression(expr_text)
                self.feature_request.setFilterExpression(expr_text)
                if no_geometry:
                    self.feature_request.setFlags(QgsFeatureRequest.NoGeometry)
                else:
                    self.feature_request.setFlags(QgsFeatureRequest.NoFlags)

                if subset_attribute:
                    self.feature_request.setSubsetOfAttributes([ind])
                else:
                    self.feature_request.setSubsetOfAttributes(QgsFeatureRequest.AllAttributes)

                for feat in layer.getFeatures(self.feature_request):
                    # name = feat.attribute("some_other_field")
                    # resultList.append(name)
                    if get_ids_only:
                        resultList.append(feat.id())
                    else:
                        resultList.append(feat)
            except:
                pass
            return resultList

        @staticmethod
        def round_to_n(x, n):
            if not x: return 0
            power = -int(math.floor(math.log10(abs(x)))) + (n - 1)
            factor = (10 ** power)
            return round(x * factor) / factor

        @staticmethod
        def point_feature_from_item(item):
            feature = QgsFeature()
            feature.initAttributes(6)
            feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(item.x), float(item.y))))
            feature.setAttributes([item.name, '0, 0, 0', 0.0, False, False, 10.0, ''])
            if hasattr(item, 'bold') and hasattr(item, 'italic') and hasattr(item, 'size') and hasattr(item, 'font'):
                feature.setAttributes([item.name, '0, 0, 0', 0.0, item.bold, item.italic, item.size, item.font])
            return feature

        @staticmethod
        def line_feature_from_item(item, project_coordinates, subinlet=None, suboutlet=None):
            link_coordinates = []
            if subinlet is not None:
                link_coordinates.append(subinlet)
            else:
                link_coordinates.append(project_coordinates[item.inlet_node])

            link_coordinates.extend(item.vertices)
            if suboutlet is not None:
                link_coordinates.append(suboutlet)
            else:
                link_coordinates.append(project_coordinates[item.outlet_node])

            points = [QgsPoint(float(coord.x), float(coord.y)) for coord in link_coordinates]
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolyline(points))
            feature.setAttributes([item.name, '0, 0, 0', "", "", 0, 0.0, 0.0])
            return feature

        @staticmethod
        def polygon_feature_from_item(item):
            points = [QgsPointXY(float(coord.x), float(coord.y)) for coord in item.vertices]
            # geometry = QgsGeometry.fromPolygon([points])
            geometry = QgsGeometry()
            geometry.addPointsXY(points, QgsWkbTypes.PolygonGeometry)
            feature = QgsFeature()
            feature.setGeometry(geometry)
            feature.setAttributes([item.name, 0.0, 0, ""])
            return feature

        def addCoordinates(self, coordinates, layer_name):
            try:
                if self.session.crs and self.session.crs.isValid():
                    layer = QgsVectorLayer("Point?crs=" + self.session.crs.toWkt(), layer_name, "memory")
                else:
                    layer = QgsVectorLayer("Point", layer_name, "memory")
                provider = layer.dataProvider()
                is_centroid = "CENTROID" in layer.name().upper()

                # add fields
                if is_centroid:
                    provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                            QgsField("color", QtCore.QVariant.String),
                                            QgsField("sub_mapid", QtCore.QVariant.Int),
                                            QgsField("sub_modelid", QtCore.QVariant.String)])
                    pass
                else:
                    provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                            QgsField("color", QtCore.QVariant.String),
                                            QgsField("value", QtCore.QVariant.Double),
                                            QgsField("bold", QtCore.QVariant.Bool),
                                            QgsField("italic", QtCore.QVariant.Bool),
                                            QgsField("size", QtCore.QVariant.Double),
                                            QgsField("font", QtCore.QVariant.String)])
                layer.updateFields()

                features = []
                if coordinates:
                    for coordinate_pair in coordinates:
                        # add a feature
                        try:
                            features.append(self.point_feature_from_item(coordinate_pair))
                        except Exception as ex:
                            if len(str(coordinate_pair.x)) > 0 and len(str(coordinate_pair.y)) > 0:
                                print ("Did not add coordinate '" + coordinate_pair.name + "' (" +
                                      str(coordinate_pair.x) + ", " +
                                      str(coordinate_pair.y) + ") to map: " + str(ex))

                if features:
                    # changes are only possible when editing the layer
                    layer.startEditing()
                    provider.addFeatures(features)
                    layer.commitChanges()
                    layer.updateExtents()
                    layer.dataProvider().createSpatialIndex()

                # create a new symbol layer with default properties
                self.set_default_point_renderer(layer, coordinates)
                if is_centroid:
                    self.add_layer(layer, self.project_group)
                else:
                    self.add_layer(layer, self.nodes_group)
                return layer
            except Exception as exBig:
                print("Error making layer: " + str(exBig))
                return None

        @staticmethod
        def set_default_point_renderer(layer, coordinates=None, size=3.5, do_labels=True):
            """ Create and set the default appearance of layer.
                If specified, coordinates will be used to check for whether there are too many to label. """
            if layer is None:
                return
            symbol = QgsMarkerSymbol()
            symbol = symbol.createSimple({})
            # symbol = QgsMarkerSymbolV2.defaultSymbol(layer.geometryType())
            symbol.deleteSymbolLayer(0)
            symbol_layer = QgsSimpleMarkerSymbolLayer()
            symbol_layer.setColor(QColor(130, 180, 255, 255))

            # Label the coordinates if there are not too many of them
            # do_labels = True
            if coordinates and len(coordinates) > 500:
                size = 1.5
                do_labels = False

            layer_name_upper = layer.name().upper()

            if "JUNCTION" in layer_name_upper:
                size = 1.5
                symbol_layer.setShape(QgsSimpleMarkerSymbolLayerBase.Circle)
            elif "OUT" in layer_name_upper:
                size = 2.5
                symbol_layer.setShape(QgsSimpleMarkerSymbolLayerBase.Triangle)
                symbol_layer.setAngle(180.0)
            elif "DIVIDER" in layer_name_upper:
                symbol_layer.setShape(QgsSimpleMarkerSymbolLayerBase.Diamond)
            elif "STORAGE" in layer_name_upper or "RESERVOIR" in layer_name_upper:
                #symbol_layer.setName(MapSymbol.rectangle.name)
                symbol_layer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_storage.svg')
            elif "LABEL" in layer_name_upper:
                symbol_layer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_label.svg')
            elif "MAP" in layer_name_upper:
                symbol_layer.setShape(QgsSimpleMarkerSymbolLayerBase.Hexagon)
            elif "CENTROID" in layer_name_upper:
                symbol_layer.setShape(QgsSimpleMarkerSymbolLayerBase.Square)
                symbol_layer.setColor(QColor('black'))
                size = 1.0
            elif "RAIN" in layer_name_upper:
                symbol_layer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_raingage.svg')
            elif "TANK" in layer_name_upper:
                symbol_layer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_tank.svg')

            if size < 1.0:
                size = 4.0
            if do_labels:
                pal_layer = QgsPalLayerSettings()
                pal_layer.enabled = True
                pal_layer.fontSizeInMapUnits = False
                pal_layer.labelOffsetInMapUnits = False
                pal_layer.fieldName = 'name'
                pal_layer.placement = QgsPalLayerSettings.OverPoint
                # expr = "case when size < 3 then size * 2 else size end case"
                # pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, expr, '')
                if "LABELS" in layer_name_upper:
                    # size = coordinates[0].size
                    # size = 10.0
                    # symbol_layer.setOutlineColor(QColor('transparent'))
                    # symbol_layer.setColor(QColor('transparent'))
                    symbol_layer.setEnabled(False)

                    # new code to implement bold, italics, font
                    provider = layer.dataProvider()
                    for feature in provider.getFeatures():
                        font_name = QFont().family()
                        format = pal_layer.format()
                        font = format.font()
                        isBold = feature[3]
                        isItalic = feature[4]
                        font_size = 10
                        if float(feature[5]):
                            font_size = float(feature[5])
                        if len(str(feature[6])) > 0:
                            font_name = str(feature[6])
                        font.setFamily(font_name)
                        font.setBold(isBold)
                        font.setItalic(isItalic)
                        format.setFont(font)
                        format.setSize(font_size)
                        pal_layer.setFormat(format)

                    pc = QgsPropertyCollection('ddp')

                    qgs_prop_bold = QgsProperty()
                    qgs_prop_bold.setField("bold")
                    pc.setProperty(1, qgs_prop_bold)

                    qgs_prop_italic = QgsProperty()
                    qgs_prop_italic.setField("italic")
                    pc.setProperty(2, qgs_prop_italic)

                    qgs_prop_size = QgsProperty()
                    qgs_prop_size.setField("size")
                    pc.setProperty(0, qgs_prop_size)

                    qgs_prop_font = QgsProperty()
                    qgs_prop_font.setField("family")
                    pc.setProperty(6, qgs_prop_font)

                    pal_layer.setDataDefinedProperties(pc)

                else:
                    pal_layer.xOffset = size
                    pal_layer.yOffset = -size
                # pal_layer.textColor = None
                # pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Color, True, False, "", "color")
                labeler = QgsVectorLayerSimpleLabeling(pal_layer)
                layer.setLabeling(labeler)
                layer.setLabelsEnabled(True)

            symbol_layer.setSize(size)
            symbol.appendSymbolLayer(symbol_layer)
            renderer = QgsSingleSymbolRenderer(symbol)
            layer.setRenderer(renderer)
            # layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)

        def addLinks(self, coordinates, links, layer_name, link_color=QColor('black'), link_width=1):
            try:
                if self.session.crs and self.session.crs.isValid():
                    layer = QgsVectorLayer("LineString?crs=" + self.session.crs.toWkt(), layer_name, "memory")
                else:
                    layer = QgsVectorLayer("LineString", layer_name, "memory")
                provider = layer.dataProvider()

                symbol_layer = QgsSimpleLineSymbolLayer()
                symbol_layer.setColor(link_color)
                if link_width > 1 and (coordinates is None or len(coordinates) <= 100):
                    symbol_layer.setWidth(link_width)

                # markerLayer = markerMeta.createSymbolLayer({'width': '0.26',
                #                                             'color': '255,0,0',
                #                                             'rotate': '1',
                #                                             'placement': 'centralpoint',
                #                                             'offset': '0'})
                # subSymbol = markerLayer.subSymbol()
                self.set_default_line_renderer(layer)
                # add fields
                provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                        QgsField("color", QtCore.QVariant.String),
                                        QgsField("inlet", QtCore.QVariant.String),
                                        QgsField("outlet", QtCore.QVariant.String),
                                        QgsField("sub2sub", QtCore.QVariant.Int),
                                        QgsField("angle", QtCore.QVariant.Double),
                                        QgsField("value", QtCore.QVariant.Double)])

                layer.updateFields()
                features = []
                if links:
                    for link in links:
                        try:
                            features.append(self.line_feature_from_item(link, coordinates))
                        except Exception as exLink:
                            print ("Skipping link " + link.name + ": " + str(exLink))

                if features:
                    # changes are only possible when editing the layer
                    layer.startEditing()
                    provider.addFeatures(features)
                    layer.commitChanges()
                    layer.updateExtents()
                    layer.dataProvider().createSpatialIndex()
                # sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("LineDecoration").createSymbolLayer(
                #     {'width': '0.26', 'color': '0,0,0'})
                # layer.rendererV2().symbols()[0].appendSymbolLayer(sl)
                if "sublink" in layer_name.lower():
                    self.add_layer(layer, self.project_group)
                else:
                    self.add_layer(layer, self.links_group)

                return layer
            except Exception as exBig:
                print("Error making layer: " + str(exBig))
                return None

        def add_layer(self, layer, group=None):
            if not self.session.crs:
                self.set_crs_from_layer(layer)
            if group:
                # QgsMapLayerRegistry.instance().addMapLayer(layer, False)
                self.qgs_project.addMapLayer(layer, False)
                group.addLayer(layer)
            else:
                # QgsMapLayerRegistry.instance().addMapLayer(layer)
                self.qgs_project.addMapLayer(layer)
            layers = self.canvas.layers()
            layers.append(layer)
            # self.canvas.setLayerSet([QgsMapCanvasLayer(lyr) for lyr in layers])
            layers_now = [] # [QgsVectorLayer(lyr) for lyr in layers]
            for lyr in layers:
                layers_now.append(lyr)
            self.canvas.setLayers(layers_now)
            self.set_extent(self.canvas.fullExtent())
            if "centroid" in layer.name().lower():
                mlyrkey = ""
                for mlyrkey in self.qgs_project.mapLayers().keys():
                    if "centroid" in mlyrkey:
                        break
                node = self.session.gis_layer_root.findLayer(mlyrkey)
                # node.setVisible(Qt.Unchecked)
                # node = QgsLayerTreeNode() # for DBG only
                node.setItemVisibilityChecked(False)

        def set_crs_from_layer(self, layer):
            """ If this layer has a valid coordinate reference system (projection),
                If the current session does not yet have a crs, use this one for this session.
                The crs for the session is later saved in filename.prj when the project is saved in filename.inp.
            """
            try:
                dp = layer.dataProvider()
                crs = dp.crs()
                if crs.isValid():
                    # if not self.session.crs:
                    self.session.set_crs(crs)
                    print("CRS = " + crs.toWkt())
                    # else:  # TODO: compare to existing CRS?
                    #     pass
            except Exception as ex:
                print (str(ex))

        def remove_all_layers(self):
            self.qgs_project.removeAllMapLayers()
            self.canvas.setLayers([])

        def remove_layers(self, remove_these_layers):
            layer_names = []
            canvas_layers = self.canvas.layers()
            for layer in remove_these_layers:
                layer_names.append(layer.name())
                canvas_layers.remove(layer)
            self.qgs_project.removeMapLayers(layer_names)
            self.canvas.setLayers([QgsMapLayer(lyr) for lyr in canvas_layers])
            self.set_extent(self.canvas.fullExtent())

        def select_all_map_features(self):
            if not self.session and not self.session.model_layers:
                return
            for mlyr in self.session.model_layers.all_layers:
                lyr_name = mlyr.name()
                if lyr_name and \
                   (lyr_name.lower().startswith("label") or
                   lyr_name.lower().startswith("subcentroid") or
                   lyr_name.lower().startswith("sublink")):
                    continue
                mlyr.selectAll()

        @staticmethod
        def set_default_line_renderer(layer, do_labels=True):
            if layer is None:
                return
            symbol = QgsLineSymbol()
            symbol = symbol.createSimple({})
            symbol.deleteSymbolLayer(0)
            slayer = QgsSimpleLineSymbolLayer()
            slayer.setWidth(1.0)
            slayer.setColor(QColor("dark gray"))
            symbol.appendSymbolLayer(slayer)
            layer_name_upper = layer.name().upper()
            if "CONDUIT" in layer_name_upper or \
               "PIPE" in layer_name_upper:
                slayer = QgsSimpleLineSymbolLayer()
                slayer.setWidth(0.5)
                slayer.setColor(QColor("light gray"))
                symbol.appendSymbolLayer(slayer)
                renderer = QgsSingleSymbolRenderer(symbol)
                layer.setRenderer(renderer)
            elif "SUBLINK" in layer_name_upper:
                symbol.deleteSymbolLayer(0)
                slayer = QgsSimpleLineSymbolLayer()
                slayer.setWidth(0.5)
                slayer.setColor(QColor("light blue"))
                slayer.setPenStyle(QtCore.Qt.DotLine)
                symbol.appendSymbolLayer(slayer)
                renderer = QgsSingleSymbolRenderer(symbol)
                layer.setRenderer(renderer)
            else:
                slayer.setWidth(1.0)
                slayer = QgsMarkerLineSymbolLayer(True, 1.5)
                mlayer = slayer.subSymbol()
                anewlayer = None
                if "PUMP" in layer_name_upper:
                    anewlayer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_pump.svg')
                elif "ORIFICE" in layer_name_upper:
                    anewlayer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_orifice.svg')
                elif "OUTLET" in layer_name_upper:
                    anewlayer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_outlet.svg')
                elif "WEIR" in layer_name_upper:
                    anewlayer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_weir.svg')
                elif "VALVE" in layer_name_upper:
                    anewlayer = QgsSvgMarkerSymbolLayer(':/icons/svg/obj_valve.svg')
                if anewlayer is not None:
                    mlayer.changeSymbolLayer(0, anewlayer)
                    slayer.setPlacement(QgsMarkerLineSymbolLayer.CentralPoint)
                    symbol.appendSymbolLayer(slayer)
                    renderer = QgsSingleSymbolRenderer(symbol)
                    layer.setRenderer(renderer)
                else:
                    sym = QgsSymbol.defaultSymbol(layer.geometryType())
                    sym.setColor(QColor('gray'))
                    sym.setWidth(0.5)
                    layer.setRenderer(QgsSingleSymbolRenderer(sym))

            # do_labels = True
            if not "SUBLINK" in layer_name_upper:
                pal_layer = QgsPalLayerSettings()
                # pal_layer.readFromLayer(layer) #pyqgis3 removed
                pal_layer.enabled = do_labels
                pal_layer.drawLabels = do_labels
                pal_layer.fontSizeInMapUnits = False
                pal_layer.labelOffsetInMapUnits = False
                pal_layer.fieldName = 'name'
                pal_layer.placement = QgsPalLayerSettings.Line
                # expr = "case when size < 3 then size * 2 else size end case"
                # pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, expr, '')
                if "LABELS" in layer_name_upper:
                    # size = coordinates[0].size
                    size = 10.0
                    # symbol_layer.setOutlineColor(QColor('transparent'))
                    # symbol_layer.setColor(QColor('transparent'))
                else:
                    pal_layer.xOffset = 0.5
                    pal_layer.yOffset = -0.5
                # pal_layer.textColor = QColor('blue')
                # pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Color, True, False, "", "color")
                labeler = QgsVectorLayerSimpleLabeling(pal_layer)
                layer.setLabeling(labeler)
                # pal_layer.writeToLayer(layer) #pyqgis3 removed

        def label_layer(self, layer, fieldname, color=QColor('black')):
            if "LABELS" in layer.name().upper():
                return
            pal_layer = QgsPalLayerSettings()
            # pal_layer.readFromLayer(layer) #pyqgis3 removed
            pal_layer.enabled = True
            pal_layer.fontSizeInMapUnits = False
            pal_layer.labelOffsetInMapUnits = False
            pal_layer.fieldName = fieldname
            pal_layer.placement = QgsPalLayerSettings.Line
            # expr = "case when size < 3 then size * 2 else size end case"
            # pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, expr, '')
            pal_layer.xOffset = 0.5
            pal_layer.yOffset = -0.5
            pal_layer.textColor = color
            labeler = QgsVectorLayerSimpleLabeling(pal_layer)
            layer.setLabeling(labeler)
            # pal_layer.writeToLayer(layer) #pyqgis3 removed

        def addPolygons(self, polygons, layer_name, poly_color='lightgreen'):
            try:
                if self.session.crs and self.session.crs.isValid():
                    layer = QgsVectorLayer("Polygon?crs=" + self.session.crs.toWkt(), layer_name, "memory")
                else:
                    layer = QgsVectorLayer("Polygon", layer_name, "memory")
                provider = layer.dataProvider()

                # add fields
                provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                        QgsField("color", QtCore.QVariant.Double),
                                        QgsField("c_mapid", QtCore.QVariant.Int),
                                        QgsField("c_modelid", QtCore.QVariant.String),
                                        QgsField("value", QtCore.QVariant.Double)])
                layer.updateFields()
                features = []
                if polygons:
                    for polygon in polygons:
                        poly_points = []
                        for coordinate_pair in polygon.vertices:
                            poly_points.append(QgsPointXY(float(coordinate_pair.x), float(coordinate_pair.y)))

                        if poly_points:
                            # check if they are closed
                            pt0 = poly_points[0]
                            pte = poly_points[len(poly_points) - 1]
                            if abs(pt0.x() - pte.x()) / pte.x() > 0.01 or abs(pt0.y() - pte.y()) / pte.y() > 0.01:
                                poly_points.append(poly_points[0])
                            # add a feature
                            feature = QgsFeature()
                            if len(poly_points) < 3:
                                new_points=[]
                                r = 4 * self.canvas.mapUnitsPerPixel()
                                ctr = poly_points[0]
                                new_points.append(QgsPointXY(ctr.x()-r, ctr.y()+r))
                                new_points.append(QgsPointXY(ctr.x()+r, ctr.y()+r))
                                new_points.append(QgsPointXY(ctr.x()+r, ctr.y()-r))
                                new_points.append(QgsPointXY(ctr.x()-r, ctr.y()-r))
                                new_points.append(QgsPointXY(ctr.x()-r, ctr.y()+r))
                                new_geom = QgsGeometry()
                                new_geom.addPointsXY(new_points, QgsWkbTypes.PolygonGeometry)
                                # feature.setGeometry(QgsGeometry.fromPolygonXY(new_geom))
                                feature.setGeometry(new_geom)
                            else:
                                new_geom = QgsGeometry()
                                new_geom.addPointsXY(poly_points, QgsWkbTypes.PolygonGeometry)
                                feature.setGeometry(new_geom)
                            feature.setAttributes([polygon.name, 0.0, 0, 0, 0.0])
                            features.append(feature)
                if features:
                    layer.startEditing()
                    provider.addFeatures(features)
                    layer.commitChanges()
                    layer.updateExtents()
                    layer.dataProvider().createSpatialIndex()

                self.set_default_polygon_renderer(layer, poly_color)
                self.add_layer(layer, self.project_group)
                return layer
            except Exception as exBig:
                print("Error making layer: " + str(exBig))
                return None

        @staticmethod
        def set_default_polygon_renderer(layer, poly_color='lightgreen', do_labels=False):
            sym = QgsSymbol.defaultSymbol(layer.geometryType())
            if "SUBCATCHMENT" in layer.name().upper():
                sym.deleteSymbolLayer(0)
                slayer = QgsSimpleFillSymbolLayer()
                slayer.setColor(QColor('dark gray'))
                sym.appendSymbolLayer(slayer)
                slayer = QgsLinePatternFillSymbolLayer()
                slayer.setColor(QColor("light gray"))
                slayer.setLineWidth(1)
                slayer.setDistance(2)
                slayer.setLineAngle(70)
                sym.appendSymbolLayer(slayer)
                slayer = QgsCentroidFillSymbolLayer()
                slayer.setColor(QColor("black"))
                sym.appendSymbolLayer(slayer)
            else:
                sym.setColor(QColor(poly_color))
            sym.setOpacity(0.2)
            layer.setRenderer(QgsSingleSymbolRenderer(sym))

            if do_labels and "SUBCATCHMENT" in layer.name().upper():
                pal_layer = QgsPalLayerSettings()
                # pal_layer.readFromLayer(layer) #pyqgis3 removed
                pal_layer.enabled = True
                pal_layer.fontSizeInMapUnits = False
                pal_layer.labelOffsetInMapUnits = False
                pal_layer.fieldName = 'name'
                pal_layer.placement = QgsPalLayerSettings.OverPoint
                labeler = QgsVectorLayerSimpleLabeling(pal_layer)
                layer.setLabeling(labeler)
                # pal_layer.writeToLayer(layer) #pyqgis3 removed

        @staticmethod
        def validatedGraduatedSymbol(layer, arenderer):
            if layer:
                return isinstance(layer.renderer(), QgsGraduatedSymbolRenderer)
            if arenderer:
                return isinstance(arenderer, QgsGraduatedSymbolRenderer)

        @staticmethod
        def validatedDefaultSymbol(geometryType):
            symbol = QgsSymbol.defaultSymbol(geometryType)
            if symbol is None:
                if geometryType == QgsWkbTypes.Point:
                    symbol = QgsMarkerSymbol()
                elif geometryType == QgsWkbTypes.LineString:
                    symbol = QgsLineSymbol()
                elif geometryType == QgsWkbTypes.MultiPolygon:
                    symbol = QgsFillSymbol()
            return symbol

        @staticmethod
        def applyGraduatedSymbologyStandardMode(layer, color_by, min=None, max=None,
                                                arenderer=None, aflow_dir=True, acolor_by_flow=None, do_label=True):
            provider = layer.dataProvider()
            calculate_min_max = False
            if min is None or max is None:
                calculate_min_max = True
            geom_type = layer.geometryType()
            # angle_idx = -1
            do_flowdir = False
            if aflow_dir and acolor_by_flow and geom_type == QgsWkbTypes.LineGeometry:
                if len(acolor_by_flow) == len(color_by):
                    do_flowdir = True

            for feature in provider.getFeatures():
                vfi = 1
                try:
                    feature_name = feature[0]
                    geom = feature.geometry()
                    val = color_by[feature_name]
                    vfi = feature.fieldNameIndex('value')
                    provider.changeAttributeValues({feature.id(): {vfi: round(val, 2)}})
                    # provider.changeAttributeValues({feature.id() : {1 : '100, 255, 50'}})
                    # feature[1] = val
                    if do_flowdir:
                        angle_idx = feature.fieldNameIndex('angle')
                        if angle_idx >= 0:
                            points = geom.asPolyline()
                            angle_0 = points[0].azimuth(points[len(points) - 1]) - 90.0
                            if acolor_by_flow[feature_name] < 0:
                                provider.changeAttributeValues({feature.id(): {angle_idx: angle_0 + 180.0}})
                            else:
                                provider.changeAttributeValues({feature.id(): {angle_idx: angle_0}})

                    if calculate_min_max:
                        if min is None or val < min:
                            min = val
                        if max is None or val > max:
                            max = val
                except Exception as ex:
                    print(str(ex))
                    provider.changeAttributeValues({feature.id(): {vfi: 0.0}})

            # colorRamp = QgsVectorGradientColorRampV2.create(
            #     {'color1': '155,155,0,255', 'color2': '0,0,255,255',
            #      'stops': '0.25;255,255,0,255:0.50;0,255,0,255:0.75;0,255,255,255'})
            # renderer = QgsGraduatedSymbolRendererV2.createRenderer(layer, "color", 5,
            #                                                          QgsGraduatedSymbolRendererV2.Quantile, symbol, colorRamp)
            # renderer.setSizeScaleField("LABELRANK")
            # layer.setRendererV2(QgsSingleSymbolRendererV2(symbol))

            slayer = None
            if do_flowdir:
                slayer = QgsMarkerLineSymbolLayer(True, 1.0)
                mlayer = slayer.subSymbol()
                anewlayer = QgsSvgMarkerSymbolLayer(':/icons/svg/flow_dir.svg')
                anewlayer.setSize(2.8)
                # lDataDefined = QgsDataDefined(True, True,
                #                               'CASE WHEN "color" < 0 THEN 180.0 ELSE 0.0 END',
                #                               'color')
                # lDataDefined = QgsDataDefined(True, False, '', 'angle')
                # lDataDefined = QgsExpressionContext(True, False, '', 'angle')
                lDataDefined = QgsProperty()
                lDataDefined.setField('angle')
                anewlayer.setDataDefinedProperty(QgsSymbolLayer.PropertyAngle, lDataDefined)

                # anewlayer.setDataDefinedProperty('angle', lDataDefined)
                # anewlayer.setAngle(180.0)
                if anewlayer:
                    mlayer.changeSymbolLayer(0, anewlayer)
                    slayer.setPlacement(QgsMarkerLineSymbolLayer.CentralPoint)
                    # symbol.appendSymbolLayer(slayer)
                    # symbol.setDataDefinedAngle(lDataDefined)
                    # renderer = QgsSingleSymbolRendererV2(symbol)
                    # layer.setRendererV2(renderer)

            if arenderer:
                if do_flowdir and slayer:
                    # arenderer = QgsGraduatedSymbolRendererV2()
                    ranges = []
                    for rng in arenderer.ranges():
                        # rng = QgsRendererRangeV2()
                        ns = rng.symbol().clone()
                        ns.appendSymbolLayer(slayer.clone())
                        ns.setColor(QtGui.QColor(rng.symbol().color().name()))
                        nrng = QgsRendererRange(rng.lowerValue(), rng.upperValue(), ns, rng.label())
                        ranges.append(nrng)

                    nr = QgsGraduatedSymbolRenderer("value", ranges)
                    layer.setRenderer(nr)
                else:
                    layer.setRenderer(arenderer.clone())
            else:
                if min is None or max is None:
                    min = 0
                    max = 5
                increment = (max - min) / 5
                ramp_val = [round(min + index*increment, 2) for index in [0, 1, 2, 3, 4]]
                colorRamp = ((str(ramp_val[0]) + ' to ' + str(ramp_val[1]), ramp_val[0], ramp_val[1], '#0000ff'),
                             (str(ramp_val[1]) + ' to ' + str(ramp_val[2]), ramp_val[1], ramp_val[2], '#00ffff'),
                             (str(ramp_val[2]) + ' to ' + str(ramp_val[3]), ramp_val[2], ramp_val[3], '#00ff00'),
                             (str(ramp_val[3]) + ' to ' + str(ramp_val[4]), ramp_val[3], ramp_val[4], '#ffff00'),
                             (str(ramp_val[4]) + ' to ' + str(round(max, 2)), ramp_val[4], max, '#ff0000'))
                ranges = []
                for label, lower, upper, color in colorRamp:
                    symbol = EmbedMap.validatedDefaultSymbol(layer.geometryType())
                    if layer.geometryType() == 0:
                        EmbedMap.set_default_point_renderer(layer, [], 3.5, False)
                        rc = QgsRenderContext()
                        symbol = layer.renderer().symbols(rc)[0].clone()
                        # symbol.setSize(1.5)
                    elif layer.geometryType() == 1:
                        EmbedMap.set_default_line_renderer(layer, False)
                        rc = QgsRenderContext()
                        symbol = layer.renderer().symbols(rc)[0].clone()
                        # symbol.setWidth(0.5)
                        if do_flowdir and slayer:
                            symbol.appendSymbolLayer(slayer.clone())

                    symbol.setColor(QtGui.QColor(color))
                    rng = QgsRendererRange(lower, upper, symbol, label)
                    ranges.append(rng)

                arenderer = QgsGraduatedSymbolRenderer("value", ranges)
                layer.setRenderer(arenderer)

            for feature in provider.getFeatures():
                val = feature['value']
                for rng in layer.renderer().ranges():
                    if val >= rng.lowerValue() and val <= rng.upperValue():
                        c = rng.symbol().color()
                        provider.changeAttributeValues({feature.id(): {1: str(c.red()) + "," + str(c.green()) + "," +
                                                                          str(c.blue())}})
                        break

            if do_label:
                # if layer.featureCount() <= 300:
                # pal_layer = QgsPalLayerSettings.fromLayer(layer) #pyqgis3 removed
                qgs_prop = QgsProperty()
                qgs_prop.setField("Color")
                pc = QgsPropertyCollection('ddp')
                pc.setProperty(4, qgs_prop)
                pal_layer = QgsPalLayerSettings()
                # pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Color, True, False, "", "color")
                pal_layer.setDataDefinedProperties(pc)
                pal_layer.fieldName = "value"
                pal_layer.placement = QgsPalLayerSettings.Line
                # pal_layer.writeToLayer(layer) #pyqgis3 removed
                pal_layer.scaleMin = 1/50000
                pal_layer.scaleMax = 1/1000
                pal_layer.enabled = True
                labeler = QgsVectorLayerSimpleLabeling(pal_layer)
                layer.setLabeling(labeler)
                layer.setLabelsEnabled(True)
            else:
                layer.setLabeling(None)
                layer.setLabelsEnabled(False)

        def applyLegend(self):
            self.root = QgsProject.instance().layerTreeRoot()
            # self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
            self.model = QgsLayerTreeModel(self.root)
            self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
            self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
            self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
            self.model.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
            self.model.setFlag(QgsLayerTreeModel.ShowLegend)
            self.view = QgsLayerTreeView()
            self.view.setModel(self.model)

            self.LegendDock = QDockWidget("Legend", self)
            self.LegendDock.setObjectName("legend")
            # self.LegendDock.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )
            self.LegendDock.setWidget(self.view)
            self.LegendDock.setContentsMargins(9, 9, 9, 9)
            # self.addDockWidget(Qt.LeftDockWidgetArea, self.LegendDock)

        def add_layer_from_file(self, file_name):
            """
            Add a GIS layer to the map from the file specified.
            Args:
                file_name: file to read as a GIS layer

            Returns:
                QGIS layer if added, None if not added
            """
            if not os.path.exists(file_name.strip()):
                return None
            layer_name = os.path.basename(file_name.strip())
            layer = QgsVectorLayer(file_name, layer_name, "ogr")
            if layer.isValid():
                self.add_layer(layer, self.other_group)
                return layer
            else:
                layer = QgsRasterLayer(file_name, layer_name)
                if layer.isValid():
                    self.add_layer(layer, self.base_group)
                    return layer
            return None

        def addVectorLayer(self, filename):
            if not os.path.isfile(filename):
                return
            layer_name, fext = os.path.splitext(os.path.basename(filename))
            layers = self.canvas.layers()
            layer_count = len(layers)
            #if filename.lower().endswith('.shp'):
            #layer = QgsVectorLayer(filename, "layer_v_" + str(layer_count), "ogr")
            layer = QgsVectorLayer(filename, layer_name, "ogr")
            if layer.featureCount() > 100:
                layer.dataProvider().createSpatialIndex()

            #elif filename.lower().endswith('.json'):
            #    layer=QgsVectorLayer(filename, "layer_v_" + str(layer_count), "GeoJson"o)
            sep_layers = []
            if fext.lower().endswith('.json') or fext.lower().endswith('.geojson'):
                sep_layers = self.parse_geojson(layer)
                for lyr_key in sep_layers:
                    lyr = sep_layers[lyr_key]
                    # pelem_type = lyr.name()[lyr.name().rindex("_") + 1:]
                    self.add_layer(lyr, self.other_group)
            else:
                if layer:
                    self.add_layer(layer, self.other_group)

        def replace_model_layer(self, alyr, group=None):
            alyr_name = alyr.name()
            for lyr in self.session.model_layers.all_layers:
                pelem_type = alyr_name[alyr_name().rindex("_") + 1:]
                if pelem_type == lyr.name() or lyr.name().startswith(pelem_type):
                    if lyr.featureCount() == 0:
                        orig_fields = []
                        #for fld in lyr.fields():
                        pass
            pass

        def parse_geojson(self, agjLayer):
            src_crs = agjLayer.crs()
            src_authid = ""
            src_Wkt = ""
            if src_crs.isValid():
                src_authid = src_crs.authid()
                src_Wkt = src_crs.toWkt()
            layers = {}
            geom_types = []
            elem_types = []
            elem_geom = {}
            ind = agjLayer.fieldNameIndex(u'element_type')
            if ind >= 0:
                elem_types = agjLayer.uniqueValues(ind, 20)
            for f in agjLayer.getFeatures():
                geom = f.geometry()
                if ind < 0 or \
                   (ind >= 0 and not elem_geom.__contains__(f.attributes()[ind])):
                    if not geom_types.__contains__(geom.wkbType()): geom_types.append(geom.wkbType())
                    if ind >=0:
                        if geom.wkbType() == QgsWkbTypes.Point:
                            elem_geom[f.attributes()[ind]] = "Point"
                        elif geom.wkbType() == QgsWkbTypes.LineString:
                            elem_geom[f.attributes()[ind]] = "LineString"
                        elif geom.wkbType() == QgsWkbTypes.MultiPolygon:
                            elem_geom[f.attributes()[ind]] = "Polygon"

            if len(elem_types) > 0:
                expr_text = "\"element_type\"='ZZZZ'"
                expr = None
                for et in elem_types:
                    attributes_added = False
                    try:
                        layer_type = elem_geom[et]
                        if src_authid:
                            layer_type = layer_type + "?crs=" + src_authid
                        new_layer = QgsVectorLayer(layer_type, agjLayer.name() + "_" + str(et), "memory")
                        expr = QgsExpression(expr_text.replace("ZZZZ", et))
                        it = agjLayer.getFeatures(QgsFeatureRequest(expr))
                        #ids = [sf.id() for sf in it]
                        #agjLayer.selectByIds(ids)
                        new_layer.startEditing()
                        for sf in it:
                            if not attributes_added:
                                for fld in sf.fields():
                                    new_layer.addAttribute(fld)
                                attributes_added = True
                            if not new_layer.addFeature(sf, False):
                                stderr = "problem adding feature"
                        new_layer.commitChanges()
                        new_layer.updateExtents()
                        layers[et] = new_layer
                    except:
                        pass
            elif len(geom_types) > 0:
                for gt in geom_types:
                    new_layer = None
                    geom_type = ""
                    layer_name_postfix = ""
                    field = QgsField("id", QtCore.QVariant.Int)
                    if gt == QgsWkbTypes.Point:
                        geom_type = "Point"
                        layer_name_postfix = "_point"
                    elif gt == QgsWkbTypes.LineString:
                        geom_type = "LineString"
                        layer_name_postfix = "_line"
                    elif gt == QgsWkbTypes.MultiPolygon:
                        geom_type = "Polygon"
                        layer_name_postfix = "_polygon"

                    layer_type = geom_type
                    if src_authid:
                        layer_type = geom_type + "?crs=" + src_authid
                    new_layer = QgsVectorLayer(layer_type, agjLayer.name() + layer_name_postfix, "memory")
                    # layer_type = layer_type + "&field=id:integer&index=yes"
                    # epsg_id = int(src_authid[5:])
                    # dst_crs = QgsCoordinateReferenceSystem(epsg_id, QgsCoordinateReferenceSystem.EpsgCrsId)
                    # new_layer.setCrs(dst_crs)
                    new_layer.dataProvider().addAttributes([field])
                    new_layer.startEditing()
                    new_id = 0
                    for f in agjLayer.getFeatures():
                        geom = f.geometry()
                        new_feature = QgsFeature()
                        new_feature.setGeometry(geom)
                        new_feature.setAttributes([new_id])
                        if geom.wkbType() == gt:
                            new_layer.addFeature(new_feature, True)
                            new_id = new_id + 1

                    if new_layer:
                        new_layer.commitChanges()
                        new_layer.updateExtents()

                    if len(geom_type) > 0:
                        layers[geom_type] = new_layer

            return layers
            pass

        def set_extent(self, extent):
            buffered_extent = extent.buffered(extent.height() / 20)
            self.canvas.setExtent(buffered_extent)
            self.canvas.refresh()

        def set_extent_by_corners(self, corners):
            r = QgsRectangle(QgsPointXY(corners[0], corners[1]), QgsPointXY(corners[2], corners[3]))
            self.set_extent(r)

        def set_extent_about_point(self, item):
            x_float = item.x
            y_float = item.y
            if not isinstance(x_float, float):
                x_float = float(item.x)
            if not isinstance(y_float, float):
                y_float = float(item.y)
            r = QgsRectangle(QgsPointXY(x_float - 1, y_float - 1), QgsPointXY(x_float + 1, y_float + 1))
            # self.set_extent(r)
            self.canvas.setExtent(r)
            # self.canvas.zoomWithCenter(x_float, y_float, False)
            self.canvas.refresh()

        def set_extent_empty(self):
            r = QgsRectangle(200.0, 200.0, 200.0, 200.0)
            self.canvas.mapSettings().setExtent(r)
            self.canvas.refresh()

        def addRasterLayer(self, filename, *args):
            if len(filename.strip()) > 0:
                layer_name = os.path.basename(filename.strip())
                #layer = QgsRasterLayer(filename, "layer_r_" + str(self.canvas.layerCount() + 1))
                layer = QgsRasterLayer(filename, layer_name)
                if args and len(args) > 0:
                    if args[0] == 'backdrop':
                        self.session.backdrop_name = layer.name()
                self.add_layer(layer, self.base_group)

        @staticmethod
        def get_extent(layers):
            '''
            Get the extent of layers by examing the coordinates of vertices
            Args:
                self: EmbedMap
                layers: [] of QgsVectorLayers
            Returns: QgsRectangle
            '''
            xmin = sys.float_info.max
            xmax = sys.float_info.min
            ymin = sys.float_info.max
            ymax = sys.float_info.min
            if not layers or len(layers) == 0:
                return None
            for lyr in layers:
                if not isinstance(lyr, QgsVectorLayer):
                    continue
                pt = None
                for f in lyr.getFeatures():
                    geom = f.geometry()
                    if geom.wkbType() == QgsWkbTypes.Point:
                        pt = geom.asPoint()
                        if pt.x() < xmin: xmin = pt.x()
                        if pt.x() > xmax: xmax = pt.x()
                        if pt.y() < ymin: ymin = pt.y()
                        if pt.y() > ymax: ymax = pt.y()
                    elif geom.wkbType() == QgsWkbTypes.MultiPolygon:
                        for pt in geom.asMultiPolygon()[0][0]:
                            if pt.x() < xmin: xmin = pt.x()
                            if pt.x() > xmax: xmax = pt.x()
                            if pt.y() < ymin: ymin = pt.y()
                            if pt.y() > ymax: ymax = pt.y()
                    elif geom.wkbType() == QgsWkbTypes.LineString:
                        for pt in geom.asPolyline():
                            if pt.x() < xmin: xmin = pt.x()
                            if pt.x() > xmax: xmax = pt.x()
                            if pt.y() < ymin: ymin = pt.y()
                            if pt.y() > ymax: ymax = pt.y()
            r = QgsRectangle(xmin, ymin, xmax, ymax)
            return r

        def calculate_units_ratio(self, src_pt_ll, src_pt_ur, dst_pt_ll, dst_pt_ur):
            self.x_unit_ratio = (dst_pt_ur.x - dst_pt_ll.x) / (src_pt_ur.x - src_pt_ll.x)
            self.y_unit_ratio = (dst_pt_ur.y - dst_pt_ll.y) / (src_pt_ur.y - src_pt_ll.y)

        def calculate_new_coordinates(self, src_pt_ll, dst_pt_ll, src_pt):
            src_x, xval_is_good = ParseData.floatTryParse(src_pt.x)
            src_y, yval_is_good = ParseData.floatTryParse(src_pt.y)
            if xval_is_good and yval_is_good:
                new_pt = Coordinate()
                new_pt.x = dst_pt_ll.x + (src_x - src_pt_ll.x) * abs(self.x_unit_ratio)
                new_pt.y = dst_pt_ll.y + (src_y - src_pt_ll.y) * abs(self.y_unit_ratio)
                return new_pt
            else:
                return None

        def translate_vertices_coordinates(self, src_pt_ll, dst_pt_ll, vertices):
            for vpt in vertices:
                new_coord = self.calculate_new_coordinates(src_pt_ll, dst_pt_ll, vpt)
                if new_coord:
                    vpt.x = str(new_coord.x)
                    vpt.y = str(new_coord.y)
                else:
                    # save a log of bad coords
                    pass

        def translate_layers_coordinates(self, src_pt_ll, src_pt_ur, dst_pt_ll, dst_pt_ur):
            if not self.session.project or not self.session.model_layers:
                return
            self.calculate_units_ratio(src_pt_ll, src_pt_ur, dst_pt_ll, dst_pt_ur)
            # update nodal coordinates
            sects = self.session.project.nodes_groups()
            sects.append(self.session.project.labels)
            if self.session.model == "SWMM":
                sects.append(self.session.project.raingages)
            for sect in sects:
                if sect.value and len(sect.value) > 0:
                    self.translate_vertices_coordinates(src_pt_ll, dst_pt_ll, sect.value)

            # update links vertices
            self.translate_vertices_coordinates(src_pt_ll, dst_pt_ll, self.session.project.all_vertices())

            # update SWMM polygons' vertices
            if self.session.model == "SWMM":
                for sub in self.session.project.subcatchments.value:
                    self.translate_vertices_coordinates(src_pt_ll, dst_pt_ll, sub.vertices)

        def update_links_length(self):
            if not self.session.project or not self.session.model_layers:
                return
            ruler = QgsDistanceArea()
            nodes = self.session.project.nodes_groups()
            for link_sect in self.session.project.links_groups():
                for lnk in link_sect.value:
                    for og in nodes:
                        node0 = og.find_item(lnk.inlet_node)
                        if node0: break
                    for og in nodes:
                        noden = og.find_item(lnk.outlet_node)
                        if noden: break
                    if node0 and noden:
                        node0x, val_is_good0x = ParseData.floatTryParse(node0.x)
                        node0y, val_is_good0y = ParseData.floatTryParse(node0.y)
                        nodenx, val_is_goodnx = ParseData.floatTryParse(noden.x)
                        nodeny, val_is_goodny = ParseData.floatTryParse(noden.y)
                        if val_is_good0x and val_is_good0y and \
                            val_is_goodnx and val_is_goodny:
                            pt0 = QgsPoint(node0x, node0y)
                            ptn = QgsPoint(nodenx, nodeny)
                            list_pts = [pt0]
                            if lnk.vertices and len(lnk.vertices) > 0:
                                for v in lnk.vertices:
                                    xval, xval_is_good = ParseData.floatTryParse(v.x)
                                    yval, yval_is_good = ParseData.floatTryParse(v.y)
                                    if xval_is_good and yval_is_good:
                                        list_pts.append(QgsPoint(xval, yval))
                            list_pts.append(ptn)
                            lnk.length = str(ruler.measureLine(list_pts))
                            del list_pts[:]
                            del list_pts

        def update_subcatchments_area(self, dst_unit):
            # update SWMM polygons' areas
            if self.session.model == "SWMM":
                ruler = QgsDistanceArea()
                list_pts = []
                for sub in self.session.project.subcatchments.value:
                    for v in sub.vertices:
                        valx, val_is_goodx = ParseData.floatTryParse(v.x)
                        valy, val_is_goody = ParseData.floatTryParse(v.y)
                        if val_is_goodx and val_is_goody:
                            list_pts.append(QgsPoint(valx, valy))
                    if len(list_pts) > 0:
                        try:
                            # geometry = QgsGeometry.fromPolygon([list_pts])
                            geometry = QgsGeometry()
                            geometry.addPointsXY(list_pts, QgsWkbTypes.PolygonGeometry)
                            a = ruler.measureArea(geometry)
                            if dst_unit.lower() == "feet":
                                sub.area = EmbedMap.round_to_n(a / 43560, 5)
                            elif dst_unit.lower() == "meters":
                                sub.area = EmbedMap.round_to_n(a / 10000, 5)
                        except:
                            # skip this sub
                            pass
                        del list_pts[:]

        def update_project_map_crs_info(self, crs_name):
            new_crs = None
            try:
                new_crs = QgsCoordinateReferenceSystem(crs_name)
            except:
                pass
            if new_crs:
                self.session.project.map.crs_name = crs_name
                self.session.project.map.crs_unit = self.QGis_UnitType[new_crs.mapUnits()]

        def drawVertexMarker(self, layer):
            """
            implement the drawVertexMarker routine to highlight the vertices of polygon
            for editing purpose
            Args:
                layer:

            Returns:

            """

        # def saveVectorLayers(self, folder):
        #     layer_index = 0
        #     for map_layer in self.session.model_layers.all_layers:
        #         try:
        #             vector_layer = map_layer.layer()
        #             layer_index += 1
        #             file_name = os.path.join(folder, "layer" + str(layer_index) + ".json")
        #
        #             QgsVectorFileWriter.writeAsVectorFormat(vector_layer, file_name, "utf-8", vector_layer.crs(),
        #                                                     driverName="GeoJson")
        #         except Exception as e:
        #             print str(e)

        def select_model_objects_by_ids(self, adict):
            """
            Args: adict: a dictionary in the form of:
                adict[junctions] = [3, 5, 25, 26 etc]
                adict[pipes] = [4, 10 etc]
                adict[tanks] = [1 etc]
            Returns:
            """
            total_selected = 0
            selected_ids = []
            if adict and len(adict) > 0:
                for obj_name in adict.keys():
                    lyr = self.session.model_layers.find_layer_by_name(obj_name)
                    if lyr:
                        del selected_ids[:]
                        for f in lyr.getFeatures():
                            if f['name'] in adict[obj_name]:
                                selected_ids.append(f.id())
                        if len(selected_ids) > 0:
                            lyr.selectByIds(selected_ids)
                            total_selected = total_selected + len(selected_ids)
                            lyr.triggerRepaint()
            return total_selected

        def create_composition(self, layer_list, extent):
            # New code for versions 2.4 and above
            ms = QgsMapSettings()
            ms.setLayers(layer_list)
            ms.setExtent(extent)
            comp = QObject.QgsComposition(ms)
            return comp, ms

        def print_map(self, alayerset):
            comp, ms = self.create_composition(alayerset, QgsRectangle(140, -28, 155, -15))
            comp.setPlotStyle(QObject.QgsComposition.Print)
            composerMap = QObject.QgsComposerMap(comp, 5, 5, 200, 200)

            # Uses mapsettings value
            composerMap.setNewExtent(ms.extent())

            comp.addItem(composerMap)
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName("out.pdf")
            # printer.setOutputFormat(QPrinter.SmallFormat)
            printer.setPaperSize(QSizeF(comp.paperWidth(), comp.paperHeight()), QPrinter.Millimeter)
            printer.setFullPage(True)
            printer.setColorMode(QPrinter.Color)
            printer.setResolution(comp.printResolution())

            pdfPainter = QPainter(printer)
            paperRectMM = printer.pageRect(QPrinter.Millimeter)
            paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
            comp.render(pdfPainter, paperRectPixel, paperRectMM)
            pdfPainter.end()

        def create_overview_0(self, alayerset):
            main_window = self.session
            new_dock_widget = QDockWidget(u"Overview")
            layout = QVBoxLayout()
            map_canvas_overview = QgsMapOverviewCanvas(
                new_dock_widget,
                self.canvas
            )
            map_canvas_overview.setLayers(alayerset)
            map_canvas_overview.setBackgroundColor(QColor(255, 127, 0))
            map_canvas_overview.enableAntiAliasing(True)
            map_canvas_overview.setMinimumWidth(380)
            map_canvas_overview.setMinimumHeight(280)
            new_dock_widget.resize(400, 300)
            layout.addWidget(map_canvas_overview)

            new_dock_widget.setLayout(layout)

            #main_window.addDockWidget(Qt.RightDockWidgetArea, new_dock_widget)
            main_window.addDockWidget(Qt.RightDockWidgetArea, new_dock_widget)
            new_dock_widget.show()

            map_canvas_overview.refresh()  # Make the background color disappear?

            # Layout optional playground
            layout.setContentsMargins(0, 0, 0, 0)

        def create_overview(self, alayers):
            ovw = MapOverview(alayers, self.canvas)
            ovw.exec_()


    class PanTool(QgsMapTool):
        def __init__(self, mapCanvas):
            QgsMapTool.__init__(self, mapCanvas)
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self.dragging = False

        def canvasPressEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                self.dragging = True
                self.canvas().panAction(event)

        def canvasReleaseEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton and self.dragging:
                self.canvas().panActionEnd(event.pos())
                self.dragging = False


    class CaptureTool(QgsMapTool):
        CAPTURE_LINE = 1
        CAPTURE_POLYGON = 2

        def __init__(self, canvas, layer, layer_name, object_type, session):
            QgsMapTool.__init__(self, canvas)
            self.canvas = canvas
            self.layer = layer
            self.layer_name = layer_name
            self.object_type = object_type
            self.session = session
            self.rubberBand = None
            self.tempRubberBand = None
            self.capturedPoints = []
            self.capturing = False
            self.ruler = None
            if object_type is not None and issubclass(object_type, Polygon):
                self.captureMode = CaptureTool.CAPTURE_POLYGON
            else:
                self.captureMode = CaptureTool.CAPTURE_LINE

            self.setCursor(QtCore.Qt.CrossCursor)
            self.inlet_node = None
            self.outlet_node = None
            self.measuring = False

        def setMeasureMode(self, measuring):
            self.measuring = measuring
            if self.measuring:
                if self.ruler is None:
                    self.ruler = QgsDistanceArea()

        def closedPolygon(self):
            if not self.measuring:
                return False
            points = self.capturedPoints
            if points is None or len(points) <= 2:
                return False
            if self.ruler is None:
                return False

            p_last = self.toCanvasCoordinates(points[len(points) - 1])
            p_0 = self.toCanvasCoordinates(points[0])
            close_d = self.ruler.measureLine(QgsPointXY(p_last), QgsPointXY(p_0))
            if abs(close_d) < 5:
                self.captureMode = CaptureTool.CAPTURE_POLYGON
                return True
            else:
                self.captureMode = CaptureTool.CAPTURE_LINE
                return False

        def canvasReleaseEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                if not self.capturing:
                    self.startCapturing()
                self.addVertex(event.pos())
                if self.measuring:
                    if self.closedPolygon():
                        self.measureCaptured(self.capturedPoints)
                        return
            elif event.button() == QtCore.Qt.RightButton:
                self.geometryCaptured()

        def canvasMoveEvent(self, event):
            if self.tempRubberBand and self.capturing:
                self.tempRubberBand.movePoint(self.toMapCoordinates(event.pos()))

        def keyPressEvent(self, event):
            key = event.key()
            if key in [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete]:
                self.removeLastVertex()
                event.ignore()
            elif key in [QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter]:
                self.geometryCaptured()
            elif key == QtCore.Qt.Key_Escape:
                self.stopCapturing()

        def startCapturing(self):
            self.stopCapturing()  # Clean up any leftover rubber bands
            self.inlet_node = None
            self.outlet_node = None
            color = QColor("red")
            if self.measuring:
                color = QColor("gray")
            color.setAlphaF(0.78)

            self.rubberBand = QgsRubberBand(self.canvas, self.bandType())
            self.rubberBand.setWidth(2)
            self.rubberBand.setColor(color)
            self.rubberBand.show()

            self.tempRubberBand = QgsRubberBand(self.canvas, self.bandType())
            self.tempRubberBand.setWidth(2)
            self.tempRubberBand.setColor(color)
            self.tempRubberBand.setLineStyle(QtCore.Qt.DotLine)
            self.tempRubberBand.show()
            self.capturing = True

        def bandType(self):
            if self.measuring:
                # return QgsWkbTypes.LineString
                return QgsWkbTypes.LineGeometry
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                # return QgsWkbTypes.Polygon
                return QgsWkbTypes.PolygonGeometry
            else:
                # return QgsWkbTypes.LineString
                return QgsWkbTypes.LineGeometry

        def stopCapturing(self):
            self.capturing = False
            self.capturedPoints = []
            if self.rubberBand:
                try:
                    self.canvas.scene().removeItem(self.rubberBand)
                except:
                    pass
                self.rubberBand = None
            if self.tempRubberBand:
                try:
                    self.canvas.scene().removeItem(self.tempRubberBand)
                except:
                    pass
                self.tempRubberBand = None
            self.canvas.refresh()

        def addVertex(self, canvasPoint):
            mapPt = self.toMapCoordinates(canvasPoint)
            layerPt = self.toLayerCoordinates(self.layer, canvasPoint)

            self.rubberBand.addPoint(mapPt)
            self.capturedPoints.append(layerPt)

            self.tempRubberBand.reset(self.bandType())
            if self.captureMode == CaptureTool.CAPTURE_LINE:
                self.tempRubberBand.addPoint(mapPt)

            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
                firstPoint = self.rubberBand.getPoint(0, 0)
                self.tempRubberBand.addPoint(firstPoint)
                self.tempRubberBand.movePoint(mapPt)
                self.tempRubberBand.addPoint(mapPt)

        def removeLastVertex(self):
            if not self.capturing: return

            bandSize = self.rubberBand.numberOfVertices()
            tempBandSize = self.tempRubberBand.numberOfVertices()
            numPoints = len(self.capturedPoints)

            if bandSize < 1 or numPoints < 1:
                return

            self.rubberBand.removePoint(-1)

            if bandSize > 1:
                if tempBandSize > 1:
                    point = self.rubberBand.getPoint(0, bandSize - 2)
                    self.tempRubberBand.movePoint(tempBandSize - 2, point)
            else:
                self.tempRubberBand.reset(self.bandType())

            del self.capturedPoints[-1]

        def geometryCaptured(self):
            points = self.capturedPoints
            if self.measuring:
                self.measureCaptured(points)
                return

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                if len(points) < 2:
                    points = None
                if self.inlet_node == None or self.outlet_node == None:
                    points = None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if len(points) < 3:
                    points = None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if points is not None:
                    points.append(points[0])  # Close polygon.

            self.stopCapturing()

            if points or (self.inlet_node and self.outlet_node):
                new_object = self.object_type()
                new_object.vertices = []
                if self.session.auto_length and self.session.crs and self.session.crs.isValid():
                    try:
                        map_widget = self.session.map_widget
                        unit_index = map_widget.map_unit_names.index(map_widget.map_linear_unit)
                        u = map_widget.map_unit_abbrev[unit_index]
                        if u:
                            if hasattr(new_object, "length"):
                                ruler = QgsDistanceArea()
                                if self.session.project.metric:
                                    unit_conversion = map_widget.map_unit_to_meters[unit_index]
                                else:
                                    unit_conversion = map_widget.map_unit_to_feet[unit_index]
                                new_object.length = map_widget.round_to_n(ruler.measureLine(points) * unit_conversion, 5)

                            if hasattr(new_object, "area"):
                                if not self.ruler:
                                    self.ruler = QgsDistanceArea()
                                if self.session.project.metric:
                                    unit_conversion = map_widget.map_unit_to_hectares[unit_index]
                                else:
                                    unit_conversion = map_widget.map_unit_to_acres[unit_index]
                                # geom = QgsGeometry.fromPolygon([points])
                                geom = QgsGeometry()
                                geom.addPointsXY(points, QgsWkbTypes.PolygonGeometry)
                                a = self.ruler.measureArea(geom)
                                new_object.area = map_widget.round_to_n(a * unit_conversion, 5)
                    except:
                        pass

                if self.inlet_node is not None and self.outlet_node is not None:
                    new_object.inlet_node = self.inlet_node
                    new_object.outlet_node = self.outlet_node
                    self.inlet_node = None
                    self.outlet_node = None
                    points = points[1:-1]

                for pt in points:
                    new_coord = Coordinate()
                    new_coord.x = pt.x()
                    new_coord.y = pt.y()
                    new_object.vertices.append(new_coord)

                self.session.add_item(new_object)

        def measureCaptured(self, layerCoords):
            if self.ruler is None:
                return
            msgBox = QMessageBox()
            self.captureMode = CaptureTool.CAPTURE_LINE
            if len(layerCoords) < 2:
                return
            elif len(layerCoords) >= 3:
                if self.closedPolygon():
                    self.captureMode = CaptureTool.CAPTURE_POLYGON

            distance_units = self.session.project.map.units.name.lower()
            area_units = "square " + distance_units
            if distance_units == 'none':
                distance_units = ''
                area_units = ''
            if self.captureMode == CaptureTool.CAPTURE_LINE:
                d = round(self.ruler.measureLine(layerCoords),2)

                msgBox.setText("Line Distance: " + str(d) + " " + distance_units)
            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
                # geometry = QgsGeometry.fromPolygon([layerCoords])
                geometry = QgsGeometry()
                layerCoords.append(layerCoords[0])
                geometry.addPointsXY(layerCoords, QgsWkbTypes.PolygonGeometry)
                a = round(self.ruler.measureArea(geometry),2)
                d = round(self.ruler.measurePerimeter(geometry),2)
                msgBox.setText("Perimeter Distance: " + str(d) + " " + distance_units + '\n' +
                               "Area: " + str(a) + " " + area_units)

            msgBox.setWindowTitle("Measure Dimension")
            msgBox.setWindowIcon(self.session.windowIcon())
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.exec_()
            del msgBox
            self.stopCapturing()
            pass


    class CaptureRegionTool(CaptureTool):
        CAPTURE_LINE = 1
        CAPTURE_POLYGON = 2

        def __init__(self, canvas, layer, layer_name, object_type, session, layers=None):
            CaptureTool.__init__(self, canvas, layer, layer_name, object_type, session)
            self.layers = layers
            self.captureMode = CaptureTool.CAPTURE_POLYGON
            self.measuring = True
            self.ruler = QgsDistanceArea()
            self.selected_model_objects = {}  # "Junction": [J1, j2, P3 etc]
            self.selected_map_objects = {}  # "Junction": [feature_id1, feature_id2, etc]
            self.region_layer = None
            self.region_geometry = None
            self.region_feature_id = None

        def update_region_layer(self, layerCoords):
            if not self.session and not self.session.model_layers:
                return
            # self.region_geometry = QgsGeometry.fromPolygon([layerCoords])
            self.region_geometry = QgsGeometry()
            layerCoords.append(layerCoords[0])
            self.region_geometry.addPointsXY(layerCoords, QgsWkbTypes.PolygonGeometry)

            if not self.region_layer:
                self.region_layer = QgsVectorLayer("Polygon", "select_region", "memory")
                self.region_layer.startEditing()
                self.region_layer.dataProvider().addAttributes([QgsField("name", QtCore.QVariant.String)])
                feature = QgsFeature()
                feature.setGeometry(self.region_geometry)
                feature.setAttributes(["select_region"])
                added = self.region_layer.dataProvider().addFeatures([feature])
                if added[0]:
                    self.region_feature_id = added[1][0].id()
            else:
                if self.region_feature_id:
                    self.region_layer.startEditing()
                    self.region_layer.changeGeometry(self.region_feature_id, self.region_geometry)
            self.region_layer.commitChanges()
            self.region_layer.updateExtents()
            self.region_layer.triggerRepaint()

        def select_by_region(self):
            total_selected = 0
            if self.region_layer and self.region_feature_id:
                # region_geom = self.region_layer.getFeature(self.region_feature_id).geometry()
                for rf in self.region_layer.getFeatures():
                    region_geom = rf.geometry()
                    break
                if not region_geom:
                    return total_selected
                for mlyr in self.session.model_layers.all_layers:
                    lyr_name = mlyr.name()
                    if lyr_name and \
                            (lyr_name.lower().startswith("label") or
                                 lyr_name.lower().startswith("subcentroid") or
                                 lyr_name.lower().startswith("sublink")):
                        continue
                    mlyr.removeSelection()
                    selected_ids = []
                    selected_model_ids = []
                    for f in mlyr.getFeatures():
                        geom = f.geometry()
                        if geom.wkbType() == QgsWkbTypes.Point:
                            if region_geom.contains(geom):
                                selected_ids.append(f.id())
                                selected_model_ids.append(f['name'])
                        elif geom.wkbType() == QgsWkbTypes.LineString:
                            if region_geom.intersects(geom):
                                selected_ids.append(f.id())
                                selected_model_ids.append(f['name'])
                        elif geom.wkbType() == QgsWkbTypes.MultiPolygon:
                            # region_geom = QgsGeometry()
                            if region_geom.intersects(geom):
                                selected_ids.append(f.id())
                                selected_model_ids.append(f['name'])
                    if len(selected_ids) > 0:
                        self.selected_map_objects[lyr_name] = selected_ids
                        mlyr.selectByIds(selected_ids)
                        total_selected = total_selected + len(selected_ids)
                        self.session.update_selected_listview(mlyr, selected_model_ids)

            return total_selected

        def geometryCaptured(self):
            points = self.capturedPoints
            if self.measuring:
                self.measureCaptured(points)
                return

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                if len(points) < 2:
                    points = None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if len(points) < 3:
                    points = None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if points is not None:
                    points.append(points[0])  # Close polygon.

            self.stopCapturing()

            if points:
                if self.session.auto_length and self.session.crs and self.session.crs.isValid():
                    try:
                        map_widget = self.session.map_widget
                        unit_index = map_widget.map_unit_names.index(map_widget.map_linear_unit)
                        u = map_widget.map_unit_abbrev[unit_index]
                    except:
                        pass
                self.update_region_layer(points)
                self.select_by_region()
                self.region_layer.updateExtents()
                self.canvas.refresh()
                self.session.setQgsMapToolSelectRegion()

        def measureCaptured(self, layerCoords):
            self.captureMode = CaptureTool.CAPTURE_LINE
            if len(layerCoords) < 2:
                return
            elif len(layerCoords) >= 3:
                if self.closedPolygon():
                    self.captureMode = CaptureTool.CAPTURE_POLYGON

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                d = self.ruler.measureLine(layerCoords)
                return
            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
                self.update_region_layer(layerCoords)
                self.select_by_region()
                self.region_layer.updateExtents()
                self.canvas.refresh()

            self.stopCapturing()
            self.session.setQgsMapToolSelectRegion()
            pass


    class AddLinkTool(CaptureTool):
        def __init__(self, canvas, layer, layer_name, object_type, session):
            CaptureTool.__init__(self, canvas, layer, layer_name, object_type, session)
            self.mp_geom = None
            self.build_spatial_index()

        def build_spatial_index(self):
            """ Build self.layer_spatial_indexes as cache of node locations eligible to be endpoints of a new link """
            self.layer_spatial_indexes = []
            index_layers = []
            index_layers.extend(self.session.model_layers.nodes_layers)
            for lyr in self.session.model_layers.all_layers:
                try:
                    if "centroid" in lyr.name().lower():
                        index_layers.extend([lyr])
                        break
                except:
                    pass
            # for lyr in self.session.model_layers.nodes_layers:
            for lyr in index_layers:
                try:
                    if isinstance(lyr, QgsVectorLayer):
                        provider = lyr.dataProvider()
                        map_points = []
                        canvas_points = []
                        ids = []
                        for feat in provider.getFeatures():
                            pt = feat.geometry().asPoint()
                            map_points.append(pt)
                            canvas_points.append(self.toCanvasCoordinates(pt))
                            ids.append(feat.id())
                        if map_points:
                            self.layer_spatial_indexes.append((lyr, map_points, canvas_points, ids))
                except Exception as e:
                    print(str(e))

        def find_nearest_feature(self, canvas_point):
            self.nearest_layer = None
            self.nearest_feature = None
            self.nearest_canvas_point = None
            self.nearest_map_point = None
            nearest_pt_id = -1
            self.nearest_distance = float("inf")
            for (lyr, map_points, canvas_points, ids) in self.layer_spatial_indexes:
                try:
                    pt_index = 0
                    for pt in canvas_points:
                        distance = (canvas_point.x() - pt.x()) ** 2 + (canvas_point.y() - pt.y()) ** 2
                        if distance < self.nearest_distance:
                            self.nearest_layer = lyr
                            self.nearest_canvas_point = canvas_point
                            self.nearest_map_point = map_points[pt_index]
                            nearest_pt_id = ids[pt_index]
                            self.nearest_distance = distance
                            # print(str(math.sqrt(nearest_distance)))
                        pt_index += 1

                except Exception as e1:
                    print(str(e1))

            if self.nearest_layer:
                iterator = self.nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(nearest_pt_id))
                if iterator:
                    self.nearest_feature = next(iterator)

                    # return nearest_layer, nearest_feature, nearest_canvas_point, nearest_map_point, math.sqrt(nearest_distance)

        def addVertex0(self, canvas_point):
            self.find_nearest_feature(canvas_point)
            # print("Found nearest distance " + str(nearest_distance))
            if self.nearest_feature:
                nearest_feature_name = self.nearest_feature.attributes()[0]
                if len(self.capturedPoints) == 0:
                    self.inlet_node = nearest_feature_name
                    canvas_point = self.nearest_canvas_point
                    map_point = self.nearest_map_point
                elif self.nearest_distance < 15:
                    if nearest_feature_name == self.inlet_node:
                        return
                    self.outlet_node = nearest_feature_name
                    canvas_point = self.nearest_canvas_point
                    map_point = self.nearest_map_point
                else:
                    map_point = self.toMapCoordinates(canvas_point)

            layer_point = self.toLayerCoordinates(self.layer, canvas_point)

            self.rubberBand.addPoint(map_point)
            self.capturedPoints.append(layer_point)
            self.tempRubberBand.reset(self.bandType())
            self.tempRubberBand.addPoint(map_point)

            if self.outlet_node:
                self.geometryCaptured()
                self.inlet_node = None
                self.outlet_node = None

        def find_nearest_feature_qgs(self, canvas_point):
            """
            Locates the closest point in self.layer_spatial_indexes and Sets:
                self.nearest_layer = QGIS layer object
                self.nearest_feature,
                self.nearest_vertex,
                self.nearest_spatial_index
            Args:
                map_point: user click point geometry object
                make_distance_labels:
            Returns:
            """

            self.nearest_layer = None
            self.nearest_feature = None
            self.nearest_point_index = -1
            self.nearest_distance = float("inf")
            self.nearest_spatial_index = 0
            nearest_feature_id = -1
            layer_index = 0
            index_layers = []
            index_layers.extend(self.session.model_layers.nodes_layers)
            for lyr in self.session.model_layers.all_layers:
                try:
                    if "centroid" in lyr.name().lower():
                        index_layers.extend([lyr])
                        break
                except:
                    pass
            for mlyr in index_layers:
                mlyr.removeSelection()
            for mlyr in index_layers:
                lyr_name = mlyr.name()
                # mlyr.removeSelection()
                selected_ids = []
                r = 4 * self.canvas.mapUnitsPerPixel()
                sel_rect = QgsRectangle(self.mp_geom.asPoint().x() - r,
                                        self.mp_geom.asPoint().y() - r,
                                        self.mp_geom.asPoint().x() + r,
                                        self.mp_geom.asPoint().y() + r)
                # mlyr.select(sel_rect, False)
                mlyr.selectByRect(sel_rect, QgsVectorLayer.SetSelection)
                ids = mlyr.selectedFeatureIds()
                """
                mlyr.select(self.mp_geom.boundingBox(), False)
                ids = mlyr.selectedFeatureIds()
                map_point = self.toMapCoordinates(canvas_point)
                self.mp_geom = QgsGeometry.fromPointXY(map_point)
                # featDict = {f.id(): f for (f) in mlyr.getFeatures()}
                featIdx = QgsSpatialIndex()
                for f in mlyr.getFeatures():
                    featIdx.insertFeature(f)
                ids = featIdx.intersects(self.mp_geom.boundingBox())
                """

                if len(ids):
                    selected_ids.append(ids[0])
                    self.nearest_layer = mlyr
                    iterator = self.nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(ids[0]))
                    if iterator:
                        self.nearest_feature = next(iterator)
                    return

        def addVertex(self, canvas_point):
            map_point = self.toMapCoordinates(canvas_point)
            self.mp_geom = QgsGeometry.fromPointXY(map_point)
            self.find_nearest_feature_qgs(canvas_point)
            # print("Found nearest distance " + str(nearest_distance))
            if self.nearest_feature:
                nearest_feature_name = self.nearest_feature.attributes()[0]
                if len(self.capturedPoints) == 0:
                    self.inlet_node = nearest_feature_name
                elif nearest_feature_name == self.inlet_node:
                    return
                else:
                    self.outlet_node = nearest_feature_name

            if self.inlet_node:
                layer_point = self.toLayerCoordinates(self.layer, canvas_point)

                self.rubberBand.addPoint(map_point)
                self.capturedPoints.append(layer_point)
                self.tempRubberBand.reset(self.bandType())
                self.tempRubberBand.addPoint(map_point)

            if self.outlet_node:
                self.geometryCaptured()
                self.inlet_node = None
                self.outlet_node = None


    class AddPointTool(QgsMapTool):
        def __init__(self, canvas, layer, layer_name, object_type, session):
            QgsMapTool.__init__(self, canvas)
            self.canvas = canvas
            self.layer = layer
            self.layer_name = layer_name
            self.object_type = object_type
            self.session = session
            # self.setCursor(Qt.CrossCursor)

        def canvasReleaseEvent(self, event):
            point = self.toLayerCoordinates(self.layer, event.pos())
            new_object = self.object_type()
            new_object.x = point.x()
            new_object.y = point.y()
            self.session.add_item(new_object)
            if self.object_type.__name__ == "Label":
                self.session.show_edit_window(
                    self.session.make_editor_from_tree(self.session.tree_section,
                                                       self.session.tree_top_items, [new_object.name]))


    class ModelCoordinatesTranslationTool(QgsMapTool):
        def __init__(self, canvas, session):
            QgsMapTool.__init__(self, canvas)
            self.canvas = canvas
            self.session = session
            self.pt_ll = None
            self.pt_ur = None
            self.layer = None
            if self.session and len(self.session.model_layers.nodes_layers) > 0:
                self.layer = self.session.model_layers.nodes_layers[0]
                # self.setCursor(Qt.CrossCursor)

        def canvasReleaseEvent(self, event):
            if not self.layer:
                self.layer = self.session.model_layers.nodes_layers[0]
            if not self.pt_ll:
                self.pt_ll = self.toLayerCoordinates(self.layer, event.pos())
            elif not self.pt_ur:
                self.pt_ur = self.toLayerCoordinates(self.layer, event.pos())
            if self.pt_ll and self.pt_ur:
                if self.pt_ll.x() > self.pt_ur.x() or self.pt_ll.y() > self.pt_ur.y():
                    tmp = self.pt_ll.x()
                    self.pt_ll.setX(self.pt_ur.x())
                    self.pt_ur.setX(tmp)
                    tmp = self.pt_ll.y()
                    self.pt_ll.setY(self.pt_ur.y())
                    self.pt_ur.setY(tmp)
                self.session.open_translate_coord_dialog(self.pt_ll, self.pt_ur)

        def clear(self):
            self.layer = None
            self.pt_ll = None
            self.pt_ur = None


    class SelectMapTool(QgsMapToolEmitPoint):
        """ Select an object by clicking it.
            Add another of the same type to the selection with ctrl-click.
            Move selected objects by dragging. Esc to cancel drag."""

        def __init__(self, canvas, session):
            self.canvas = canvas
            self.session = session
            self.start_drag_position = None
            self.tempRubberBand = None
            QgsMapToolEmitPoint.__init__(self, self.canvas)
            # self.build_spatial_index()
            self.mp_geom = None
            self.prev_nearest_layer = None
            self.extending_same_layer = False
            self.auto_detect = True

        def build_spatial_index(self):
            self.layer_spatial_indexes = []
            for lyr in self.session.model_layers.all_layers:
                lyr.removeSelection()
                try:
                    if isinstance(lyr, QgsVectorLayer):
                        provider = lyr.dataProvider()
                        # insert features to index
                        spatial_index = []  # QgsSpatialIndex()
                        ids = []
                        found = False
                        for feat in provider.getFeatures():
                            pt = self.make_center_point(feat.geometry())
                            if pt:
                                spatial_index.append(pt)
                                ids.append(feat.id())
                                found = True
                        if found:
                            self.layer_spatial_indexes.append((lyr, spatial_index, ids, None))
                except Exception as e:
                    print(str(e))

        def make_center_point(self, geometry):
            pt = None
            if geometry.wkbType() == QgsWkbTypes.LineString:
                line = geometry.asPolyline()
                pt = QgsPointXY((line[0].x() + line[-1].x()) / 2, (line[0].y() + line[-1].y()) / 2)
            elif geometry.wkbType() == QgsWkbTypes.MultiPolygon:
                # Select subbasin by clicking closest to center of its bounding box
                box = geometry.boundingBox()
                pt = QgsPointXY((box.xMinimum() + box.xMaximum()) / 2,
                              (box.yMinimum() + box.yMaximum()) / 2)
            elif geometry.wkbType() == QgsWkbTypes.Point:
                pt = geometry.asPoint()
            return pt

        def start_drag(self, event_pos):
            if self.tempRubberBand:  # Clean up old rubber band if we already have one
                self.end_drag()

            self.start_drag_position = event_pos
            color = QColor("red")
            color.setAlphaF(0.78)

            self.tempRubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
            self.tempRubberBand.setWidth(2)
            self.tempRubberBand.setColor(color)
            self.tempRubberBand.setLineStyle(QtCore.Qt.DotLine)
            self.tempRubberBand.addPoint(self.toMapCoordinates(event_pos))
            self.tempRubberBand.show()

        def end_drag(self):
            self.start_drag_position = None
            if self.tempRubberBand:
                try:
                    self.canvas.scene().removeItem(self.tempRubberBand)
                except:
                    pass
                self.tempRubberBand = None

        def canvasMoveEvent(self, mouse_event):
            if self.tempRubberBand:
                self.tempRubberBand.movePoint(self.toMapCoordinates(mouse_event.pos()))

        def canvasReleaseEvent(self, mouse_event):
            if self.tempRubberBand and mouse_event.pos() != self.start_drag_position:
                event_pt = self.toMapCoordinates(mouse_event.pos())
                start_pt = self.toMapCoordinates(self.start_drag_position)
                self.session.move_selected_items(self.nearest_layer,
                                                 event_pt.x() - start_pt.x(),
                                                 event_pt.y() - start_pt.y())
            self.end_drag()

        def keyPressEvent(self, event):
            if self.tempRubberBand and event.key() == QtCore.Qt.Key_Escape:
                self.end_drag()
                event.ignore()

        def canvasPressEvent0(self, mouse_event):
            try:
                event_pos = mouse_event.pos()
                extending = mouse_event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier)

                self.selected_names = []
                map_point = self.toMapCoordinates(event_pos)
                self.find_nearest_feature(map_point)
                if self.nearest_feature:
                    nearest_feature_name = self.nearest_feature.attributes()[0]
                else:
                    nearest_feature_name = None

                previously_selected = []
                for feat in self.nearest_layer.selectedFeatures():
                    previously_selected.append(feat.attributes()[0])

                if not extending and nearest_feature_name and nearest_feature_name in previously_selected:
                    # Clicking an already-selected item starts moving all selected items
                    self.start_drag(event_pos)
                else:
                    # Clear selection on other layers and on this layer if not extending the selection with Ctrl or Shift
                    for layer in self.canvas.layers():
                        if isinstance(layer, QgsVectorLayer):
                            if layer == self.nearest_layer and extending:
                                # add names of already-selected features to selected_names
                                self.selected_names.extend(previously_selected)
                            else:
                                layer.removeSelection()

                    if self.nearest_layer:
                        if nearest_feature_name not in self.selected_names:
                            self.selected_names.append(nearest_feature_name)
                        self.session.select_named_items(self.nearest_layer, self.selected_names)
            except Exception as e2:
                print(str(e2) + '\n' + str(traceback.print_exc()))

        def canvasPressEvent(self, mouse_event):
            try:
                event_pos = mouse_event.pos()
                extending = mouse_event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier)
                if extending:
                    self.extending_same_layer = True
                else:
                    self.extending_same_layer = False

                self.selected_names = []
                map_point = self.toMapCoordinates(event_pos)
                self.mp_geom = QgsGeometry.fromPointXY(map_point)
                # self.find_nearest_feature(map_point)
                self.find_nearest_feature_qgs()
                if self.nearest_feature:
                    nearest_feature_name = self.nearest_feature.attributes()[0]
                else:
                    nearest_feature_name = None

                previously_selected = []
                if self.nearest_layer:
                    for feat in self.nearest_layer.selectedFeatures():
                        previously_selected.append(feat.attributes()[0])

                if not extending and nearest_feature_name and nearest_feature_name in previously_selected:
                    # Clicking an already-selected item starts moving all selected items
                    self.start_drag(event_pos)
                else:
                    # Clear selection on other layers and on this layer if not extending the selection with Ctrl or Shift
                    for layer in self.canvas.layers():
                        if isinstance(layer, QgsVectorLayer):
                            if layer == self.nearest_layer and extending:
                                # add names of already-selected features to selected_names
                                self.selected_names.extend(previously_selected)
                            else:
                                layer.removeSelection()

                if self.nearest_layer:
                    if nearest_feature_name not in self.selected_names:
                        if nearest_feature_name is not None:
                            self.selected_names.append(nearest_feature_name)
                    self.session.select_named_items(self.nearest_layer, self.selected_names)
                else:
                    self.session.clear_section_selection()
                    self.session.clear_object_listing()

            except Exception as e2:
                print(str(e2) + '\n' + str(traceback.print_exc()))

        def find_nearest_feature(self, map_point, make_distance_labels=False):
            """ Locates the closest point in self.layer_spatial_indexes and Sets:
             self.nearest_layer = QGIS layer object self.nearest_feature, self.nearest_vertex, self.nearest_spatial_index"""
            if make_distance_labels:
                if hasattr(self, "distance_layer") and self.distance_layer:
                    self.session.map_widget.remove_layers([self.distance_layer])
                distances = []

            self.nearest_layer = None
            self.nearest_feature = None
            self.nearest_point_index = -1
            self.nearest_distance = float("inf")
            self.nearest_spatial_index = 0
            nearest_feature_id = -1
            layer_index = 0
            for (lyr, points, ids, pt_indexes) in self.layer_spatial_indexes:
                try:
                    sp_index = 0
                    for pt in points:
                        distance = map_point.sqrDist(pt)
                        if make_distance_labels:
                            dist_coord = Coordinate()
                            dist_coord.x = pt.x()
                            dist_coord.y = pt.y()
                            dist_coord.name = "{:,}".format(distance)
                            distances.append(dist_coord)
                        if distance < self.nearest_distance:
                            self.nearest_layer = lyr
                            nearest_feature_id = ids[sp_index]
                            if pt_indexes:
                                self.nearest_point_index = pt_indexes[sp_index]
                            self.nearest_distance = distance
                            self.nearest_spatial_index = layer_index
                            # print("Nearest: " + "{:,}".format(pt.x()) + ", " + "{:,}".format(pt.y()))
                        sp_index += 1

                except Exception as e1:
                    print(str(e1))
                layer_index += 1

            if nearest_feature_id > -1 and self.nearest_layer:
                iterator = self.nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(nearest_feature_id))
                if iterator:
                    self.nearest_feature = next(iterator)

            if make_distance_labels:
                self.distance_layer = self.session.map_widget.addCoordinates(distances, "Distances")
                self.canvas.refresh()

        def find_nearest_feature_qgs(self, make_distance_labels=False):
            """
            Locates the closest point in self.layer_spatial_indexes and Sets:
                self.nearest_layer = QGIS layer object
                self.nearest_feature,
                self.nearest_vertex,
                self.nearest_spatial_index
            Args:
                map_point: user click point geometry object
                make_distance_labels:
            Returns:
            """
            if make_distance_labels:
                if hasattr(self, "distance_layer") and self.distance_layer:
                    self.session.map_widget.remove_layers([self.distance_layer])
                distances = []

            if self.auto_detect:
                self.nearest_layer = None
            self.nearest_feature = None
            self.nearest_point_index = -1
            self.nearest_distance = float("inf")
            self.nearest_spatial_index = 0
            nearest_feature_id = -1
            layer_index = 0

            if self.extending_same_layer:
                if self.nearest_layer:
                    for mlyr in self.session.model_layers.all_layers:
                        if mlyr == self.nearest_layer:
                            pass
                        else:
                            mlyr.removeSelection()
            else:
                for mlyr in self.session.model_layers.all_layers:
                    mlyr.removeSelection()

            for mlyr in self.session.model_layers.all_layers:
                lyr_name = mlyr.name()
                if lyr_name and \
                        (lyr_name.lower().startswith("subcentroid") or
                        lyr_name.lower().startswith("sublink")):
                        #("label" in lyr_name.lower() or
                        #     lyr_name.lower().startswith("subcentroid") or
                        #     lyr_name.lower().startswith("sublink")):
                    continue
                # mlyr.removeSelection()
                if not self.auto_detect:
                    if self.nearest_layer:
                        if mlyr.name() != self.nearest_layer.name():
                            continue
                selected_ids = []
                r = 4 * self.canvas.mapUnitsPerPixel()
                lyr_pt = self.toLayerCoordinates(mlyr, self.mp_geom.asPoint())
                sel_rect = QgsRectangle(lyr_pt.x() - r,
                                        lyr_pt.y() - r,
                                        lyr_pt.x() + r,
                                        lyr_pt.y() + r)
                mlyr.selectByRect(sel_rect, False)
                ids = mlyr.selectedFeatureIds()
                if len(ids):
                    selected_ids.append(ids[0])
                    self.nearest_layer = mlyr
                    if self.nearest_layer == self.prev_nearest_layer:
                        self.extending_same_layer = True
                    else:
                        self.extending_same_layer = False
                        self.prev_nearest_layer = mlyr
                    iterator = self.nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(ids[0]))
                    if iterator:
                        self.nearest_feature = next(iterator)
                    # return

        def canvasDoubleClickEvent(self, e):
            self.session.edit_selected_objects()


    class MoveVerticesTool(SelectMapTool):
        """ Move the internal vertices of links or subcatchments. """

        def __init__(self, canvas, session):
            SelectMapTool.__init__(self, canvas, session)

        # def canvasPressEvent(self, mouse_event):
        #     try:
        #         map_point = self.toMapCoordinates(mouse_event.pos())
        #         self.nearest_layer, self.nearest_feature, self.nearest_vertex = self.find_nearest_feature(map_point)
        #         if self.nearest_feature:
        #             self.nearest_geometry = self.nearest_feature.geometry()
        #             self.start_drag(mouse_event)
        #     except Exception as e2:
        #         print str(e2) + '\n' + str(traceback.print_exc())

        def canvasPressEvent(self, mouse_event):
            try:
                event_pos = mouse_event.pos()
                map_point = self.toMapCoordinates(event_pos)
                self.find_nearest_feature(map_point)  # , True)
                if self.nearest_feature:
                    self.nearest_geometry = self.nearest_feature.geometry()
                    wkb_type = self.nearest_geometry.wkbType()
                    if wkb_type == QgsWkbTypes.LineString:
                        vertex = self.nearest_geometry.asPolyline()[self.nearest_point_index]
                    elif wkb_type == QgsWkbTypes.MultiPolygon:
                        vertex = self.nearest_geometry.asMultiPolygon()[0][0][self.nearest_point_index]
                    if vertex:
                        start_pos = self.toCanvasCoordinates(vertex)
                        # layer_point = self.toLayerCoordinates(self.nearest_layer, event_pos)
                        # vertex_coord, vertex, prev_vertex, next_vertex, dist_squared = self.nearest_geometry.closestVertex(layer_point)
                        # distance = math.sqrt(dist_squared)
                        # tolerance = self.calcTolerance(event_pos)
                        # if distance > tolerance: return
                        if mouse_event.button() == 1:  # LeftButton:
                            # Left click -> move vertex.
                            self.start_drag(start_pos)
                            # self.dragging = True
                            # self.feature = feature
                            # self.vertex = vertex
                            # self.moveVertexTo(event_pos)
                            self.canvas.refresh()
                        elif mouse_event.button() == 2:  # QtGui.Qt.RightButton:
                            # Right click -> delete vertex.
                            self.delete_vertex()
                            self.canvas.refresh()

            except Exception as e2:
                print(str(e2) + '\n' + str(traceback.print_exc()))

        # def canvasMoveEvent(self, event):
        #     if self.dragging:
        #         self.moveVertexTo(event.pos())
        #         self.canvas.refresh()

        def canvasReleaseEvent(self, mouse_event):
            if self.tempRubberBand and mouse_event.pos() != self.start_drag_position:
                self.moveVertexTo(mouse_event.pos())
                # self.session.move_selected_items(self.nearest_layer,
                #                                  event_pt.x() - start_pt.x(),
                #                                  event_pt.y() - start_pt.y())
            self.end_drag()

        # def canvasDoubleClickEvent(self, event):
        #     feature = self.findFeatureAt(event.pos())
        #     if feature == None:
        #         return
        #     mapPt, layerPt = self.transformCoordinates(event.pos())
        #     geometry = feature.geometry()
        #     distSquared, closestPt, beforeVertex = geometry.closestSegmentWithContext(layerPt)
        #     distance = math.sqrt(distSquared)
        #     tolerance = self.calcTolerance(event.pos())
        #     if distance > tolerance:
        #         return
        #     geometry.insertVertex(closestPt.x(), closestPt.y(), beforeVertex)
        #     self.layer.changeGeometry(feature.id(), geometry)
        #     self.canvas.refresh()

        # def calcTolerance(self, pos):
        #     pt1 = QPoint(pos.x(), pos.y())
        #     pt2 = QPoint(pos.x() + 10, pos.y())
        #     mapPt1, layerPt1 = self.transformCoordinates(pt1)
        #     mapPt2, layerPt2 = self.transformCoordinates(pt2)
        #     tolerance = layerPt2.x() - layerPt1.x()
        #     return tolerance

        def moveVertexTo(self, pos):
            geometry = self.nearest_geometry
            layer_pt = self.toLayerCoordinates(self.nearest_layer, pos)
            start_pt = self.toLayerCoordinates(self.nearest_layer, self.start_drag_position)

            self.session.move_vertex(self.nearest_layer,
                                     self.nearest_feature,
                                     self.nearest_point_index,
                                     start_pt.x(), start_pt.y(),
                                     layer_pt.x(), layer_pt.y())

            # This update is now handled within session.move_vertex via call to setQgsMapTool in class _MoveVertex
            # Update this moved point in layer_spatial_indexes
            # self.build_spatial_index()
            # pt_index = self.nearest_point_index
            # if self.nearest_geometry.wkbType() == QGis.WKBPolygon:
            #    pt_index += 1
            # self.layer_spatial_indexes[self.nearest_spatial_index][1][pt_index] = layer_pt

        def delete_vertex(self):
            geometry = self.nearest_geometry
            wkb_type = geometry.wkbType()
            if wkb_type == QgsWkbTypes.LineString:
                lineString = geometry.asPolyline()
                if len(lineString) <= 2:
                    return
            elif wkb_type == QgsWkbTypes.MultiPolygon:
                polygon = geometry.asMultiPolygon()
                exterior = polygon[0][0]
                if len(exterior) <= 4:
                    return
            if geometry.deleteVertex(self.nearest_point_index):
                self.nearest_layer.changeGeometry(self.nearest_feature.id(), geometry)
                del self.layer_spatial_indexes[self.nearest_spatial_index]
                self.nearest_feature = None
                self.nearest_layer = None
                self.nearest_feature = None
                self.nearest_canvas_point = None
                self.nearest_map_point = None

        def build_spatial_index(self):
            """ Build list of eligible vertices that could be moved by this tool.
                List is saved in self.layer_spatial_indexes. """
            self.layer_spatial_indexes = []
            model_layers = []
            model_layers.extend(self.session.model_layers.links_layers)
            try:
                model_layers.append(self.session.model_layers.subcatchments)
            except:
                pass  # Skip, don't have that layer
            for lyr in model_layers:
                try:
                    if isinstance(lyr, QgsVectorLayer):
                        # provider = lyr.dataProvider()
                        spatial_index = []
                        ids = []
                        pt_indexes = []
                        found = False
                        for feat in lyr.getFeatures():
                            geometry = feat.geometry()
                            points = None
                            try:
                                if geometry.wkbType() == QgsWkbTypes.LineString:
                                    points = geometry.asPolyline()[1:-1]  # skip first and last point which are nodes
                                    index = 1
                                elif geometry.wkbType() == QgsWkbTypes.MultiPolygon:
                                    points = geometry.asMultiPolygon()[0][0]
                                    index = 0
                                else:
                                    break  # if this one is not a type we can use, others in layer are not either
                            except:
                                pass
                            if points:
                                feat_id = feat.id()
                                for pt in points:
                                    spatial_index.append(pt)
                                    ids.append(feat_id)
                                    pt_indexes.append(index)
                                    index += 1
                                found = True
                        if found:
                            self.layer_spatial_indexes.append((lyr, spatial_index, ids, pt_indexes))
                except Exception as e:
                    print(str(e))


    class MapSymbol(Enum):
        circle = 1
        square = 2
        cross = 3
        rectangle = 4
        diamond = 5
        pentagon = 6
        triangle = 7
        equitri = 8
        star = 9
        regstar = 10
        arrow = 11
        fillarrowhead = 12
        x = 13


    class LegendMenuProvider(QgsLayerTreeViewMenuProvider):
        def __init__(self, view, map_control):
            QgsLayerTreeViewMenuProvider.__init__(self)
            self.view = view
            self.map_control = map_control
            self.label_by_name = None
            self.label_by_value = None

        def createContextMenu(self):
            clyr = self.view.currentLayer()
            if clyr is None or not clyr.isValid():
                return None
            m = QMenu()
            # m.addAction("Show Extent", self.showExtent)
            m.addAction("Zoom to layer", self.zoom_to_layer)
            m.addAction("Zoom to selected", self.zoom_to_layer_selected)
            m.addAction("Change Style...", self.edit_style)
            m.addAction("Default Style", self.default_style)
            if not self.map_control.is_model_layer(clyr):
                m.addAction("Remove Layer", self.remove_layer)
            lm = m.addMenu("Label")
            lm.addAction("By Name", lambda: self.label_layer("Name"))
            lm.addAction("By Value", lambda: self.label_layer("Value"))
            lm.addAction("Off", lambda: self.label_layer("Off"))
            return m

        def showExtent(self):
            r = self.view.currentLayer().extent()
            QMessageBox.information(None, "Extent", r.toString())

        def zoom_to_layer_selected(self):
            box = self.view.currentLayer().boundingBoxOfSelected()
            self.map_control.canvas.setExtent(box)
            self.map_control.canvas.refresh()

        def zoom_to_layer(self):
            # self.map_control.set_extent(self.view.currentLayer().extent())
            r = self.view.currentLayer().extent()
            xmin = sys.float_info.max
            xmax = sys.float_info.min
            ymin = sys.float_info.max
            ymax = sys.float_info.min
            if r.height() > 0:
                xmin = r.xMinimum()
                xmax = r.xMaximum()
                ymin = r.yMinimum()
                ymax = r.yMaximum()
            else:
                r_new = self.map_control.get_extent([self.view.currentLayer()])
                xmin = r_new.xMinimum()
                xmax = r_new.xMaximum()
                ymin = r_new.yMinimum()
                ymax = r_new.yMaximum()
            r_new = QgsRectangle(xmin, ymin, xmax, ymax)
            self.map_control.set_extent(r_new)
            pass

        def remove_layer(self):
            clyr = self.view.currentLayer()
            if clyr is None:
                return
            layer_names = []
            canvas_layers = self.map_control.canvas.layers()
            for layer in [clyr]:
                layer_names.append(layer.name())
                canvas_layers.remove(layer)
            self.map_control.qgs_project.removeMapLayers(layer_names)
            self.map_control.canvas.setLayers(canvas_layers)
            if isinstance(clyr, QgsVectorLayer):
                self.map_control.other_group.removeLayer(clyr)
            elif isinstance(clyr, QgsRasterLayer):
                self.map_control.base_group.removeLayer(clyr)
            self.map_control.set_extent(self.map_control.canvas.fullExtent())

        def edit_style(self):
            lyr = self.view.currentLayer()
            if isinstance(lyr, QgsRasterLayer):
                self.edit_style_raster()
                return
            ed = None
            new_renderer = None
            if isinstance(lyr.renderer(), QgsGraduatedSymbolRenderer):
                ed = GraduatedSymbolV2(lyr, None)
                if ed.exec_():
                    new_renderer = QgsGraduatedSymbolRenderer.convertFromRenderer(ed.get_renderer())
            else:
                old_renderer = self.view.currentLayer().renderer()
                ed = QgsSymbolSelectorDialog(old_renderer.symbol(),
                                               QgsStyle.defaultStyle(),
                                               lyr, None, False)

                if ed.exec_():
                    new_renderer = old_renderer.clone()

            if new_renderer:
                lyr.setRenderer(new_renderer)
                self.map_control.layer_styles[lyr.id()] = new_renderer.clone()
                lyr.triggerRepaint()
                self.map_control.session.update_thematic_map()
            self.view.setCurrentLayer(None)

        def edit_style_raster(self):
            lyr = self.view.currentLayer()
            ed = None
            new_renderer = None
            ed = RasterStyleEditor(lyr, None)
            if ed.exec_():
                new_renderer = ed.get_renderer()

            if new_renderer:
                lyr.setRenderer(new_renderer)
                self.map_control.layer_styles[lyr.id()] = new_renderer.clone()
                lyr.triggerRepaint()
                self.map_control.session.update_thematic_map()
            self.view.setCurrentLayer(None)

        def default_style(self):
            if not self.view.currentLayer() in self.map_control.session.model_layers.all_layers:
                return
            lyr = self.view.currentLayer()
            gtype = lyr.geometryType()
            if gtype == 0:
                EmbedMap.set_default_point_renderer(lyr)
            elif gtype == 1:
                EmbedMap.set_default_line_renderer(lyr)
            elif gtype == 2:
                EmbedMap.set_default_polygon_renderer(lyr)
            self.remove_layer_annotation()
            lyr.triggerRepaint()
            self.view.setCurrentLayer(None)
            pass

        def remove_layer_annotation(self):
            layer_name = self.view.currentLayer().name()
            if " [" in layer_name:
                layer_name = layer_name[0:layer_name.index(" [")]
                self.view.currentLayer().setLayerName(layer_name)

        def label_layer(self, attribute):
            # print "label layer by " + attribute
            lyr = self.view.currentLayer()
            lyr_name = lyr.name()
            try:
                lyr_name = lyr_name[0:lyr_name.index(' [')]
            except ValueError as e:
                lyr_name = lyr.name()

            if lyr and isinstance(lyr, QgsVectorLayer):
                pal_layer = QgsPalLayerSettings()
                if attribute.lower() in ('name', 'value'):
                    pal_layer.fieldName = attribute.lower()
                    pal_layer.placement = QgsPalLayerSettings.Line
                    pal_layer.enabled = True
                    labeler = QgsVectorLayerSimpleLabeling(pal_layer)
                    lyr.setLabeling(labeler)
                    lyr.setLabelsEnabled(True)
                    self.map_control.session.project_settings.config.setValue(lyr_name + '-label', attribute.lower())
                else:
                    pal_layer.enabled = False
                    lyr.setLabeling(None)
                    lyr.setLabelsEnabled(False)
                    self.map_control.session.project_settings.config.setValue(lyr_name + '-label', 'Off')
                lyr.triggerRepaint()
            self.view.setCurrentLayer(None)


    class GraduatedSymbolV2(QDialog):
        def __init__(self, layer, parent=None, **kwargs):
            QDialog.__init__(self)
            self.layer = layer
            self.keepGoing = True

            self.setWindowTitle('Graduated Symbol Editor')
            layout = QVBoxLayout()
            self.editor = QgsGraduatedSymbolRendererWidget(layer, QgsStyle.defaultStyle(),
                                                             layer.renderer())
            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)

            layout.addWidget(self.editor)
            layout.addWidget(buttonBox)

            buttonBox.accepted.connect(self.accept)
            buttonBox.rejected.connect(self.reject)

            layout.setContentsMargins(10, 10, 10, 10)
            self.setLayout(layout)

        def get_renderer(self):
            return self.editor.renderer()


    class RasterStyleEditor(QDialog):
        def __init__(self, layer, parent=None, **kwargs):
            QDialog.__init__(self)
            self.layer = layer
            self.keepGoing = True

            self.setWindowTitle('Raster Style Editor')
            layout = QVBoxLayout()
            # self.layer = QgsRasterLayer()
            # self.editor = QgsRasterRendererWidget(layer, self.layer.extent())
            renderer_type = ''
            if self.layer.renderer():
                renderer_type = self.layer.renderer().type()
            if renderer_type:
                if renderer_type.startswith('singlebandpseudocolor') or renderer_type.startswith('singlebandgray'):
                    self.editor = QgsSingleBandPseudoColorRendererWidget(self.layer, self.layer.extent())
                elif self.layer.renderer().type().startswith('multiband'):
                    self.editor = QgsMultiBandColorRendererWidget(self.layer, self.layer.extent())
            else:
                QMessageBox.information(None, "Raster Style Editor", 'Unrecognized Raster Renderer.', "")

            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)

            layout.addWidget(self.editor)
            layout.addWidget(buttonBox)

            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout.setContentsMargins(10, 10, 10, 10)
            self.setLayout(layout)

        def get_renderer(self):
            return self.editor.renderer()


    class MapOverview(QDialog):
        def __init__(self, layers, canvas, parent=None, **kwargs):
            QDialog.__init__(self)
            self.layers = layers
            self.canvas = canvas

            new_dock_widget = QDockWidget(u"Overview")
            layout = QVBoxLayout()
            map_canvas_overview = QgsMapOverviewCanvas(
                new_dock_widget,
                self.canvas
            )
            map_canvas_overview.setLayers(self.layers)
            # map_canvas_overview.setBackgroundColor(QColor(255, 127, 0))
            map_canvas_overview.setBackgroundColor(QColor(255, 255, 255))
            map_canvas_overview.enableAntiAliasing(True)
            map_canvas_overview.setMinimumWidth(380)
            map_canvas_overview.setMinimumHeight(280)
            new_dock_widget.resize(400, 300)
            layout.addWidget(map_canvas_overview)

            # new_dock_widget.setLayout(layout)

            # main_window.addDockWidget(Qt.RightDockWidgetArea, new_dock_widget)

            map_canvas_overview.refresh()  # Make the background color disappear?

            # Layout optional playground
            layout.setContentsMargins(0, 0, 0, 0)

            self.setWindowTitle('Map Overview')
            self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
            buttonBox = QDialogButtonBox(QDialogButtonBox.Close)

            layout.addWidget(new_dock_widget)
            layout.addWidget(buttonBox)

            buttonBox.accepted.connect(self.accept)
            buttonBox.rejected.connect(self.reject)

            layout.setContentsMargins(10, 10, 10, 10)
            self.setLayout(layout)

except:
    print("Skipping map_tools")
