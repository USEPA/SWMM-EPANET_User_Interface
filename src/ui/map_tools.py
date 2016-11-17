try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore, Qt
    from PyQt4.QtGui import *
    from core.coordinate import Coordinate, Polygon
    import traceback
    import math
    import os

    class EmbedMap(QWidget):
        """ Main GUI Widget for map display inside vertical layout """
        def __init__(self, canvas, session, main_form=None, **kwargs):
            super(EmbedMap, self).__init__(main_form)
            self.canvas = canvas  # QgsMapCanvas()
            self.canvas.setMouseTracking(True)
            self.canvas.useImageToRender(False)
            # self.canvas.setCanvasColor(QtGui.QColor.white)

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
            self.mapLinearUnit = 'none'
            self.coord_origin = Coordinate()
            self.coord_fext = Coordinate()
            self.coord_fext.float_x = 100000.0
            self.coord_fext.float_y = 100000.0

            QtCore.QObject.connect(self.canvas, QtCore.SIGNAL("xyCoordinates(QgsPoint)"), self.canvasMoveEvent)

            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.canvas)

            #contents = QWidget()
            #contents.setLayout(layout)

            self.setLayout(layout)
            #self.setCentralWidget(self)

            #layout.addWidget(None)
            self.setMouseTracking(True)

        def setZoomInMode(self):
            if self.session.actionZoom_in.isChecked():
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
                self.canvas.setMapTool(self.panTool)
                #self.panTool.setCursor(QtCore.Qt.OpenHandCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
            else:
                self.canvas.unsetMapTool(self.panTool)
                #self.panTool.setCursor(QtCore.Qt.ArrowCursor)
                #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

        def setSelectMode(self):
            if self.session.actionMapSelectObj.isChecked():
                if self.canvas.layers():
                    self.selectTool = SelectMapTool(self.canvas, self.session)
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

        def setMeasureMode(self):
            if self.session.actionMapMeasure.isChecked():
                if self.measureTool is None:
                    self.measureTool = CaptureTool(self.canvas, None, None, None, self.session)
                    self.measureTool.setMeasureMode(True)
                self.canvas.setMapTool(self.measureTool)
            else:
                self.canvas.unsetMapTool(self.measureTool)

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
            if action_obj.isChecked():
                # QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
                layer = getattr(self.session.model_layers, layer_name)
                self.session.select_named_items(layer, None)
                for obj_type, name in self.session.section_types.iteritems():
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


        def zoomfull(self):
            self.canvas.zoomToFullExtent()
            self.set_extent(self.canvas.extent())


        def setMouseTracking(self, flag):
            def recursive_set(parent):
                for child in parent.findChildren(QtCore.QObject):
                    try:
                        child.setMouseTracking(flag)
                    except:
                        pass
                    recursive_set(child)
            QtGui.QWidget.setMouseTracking(self, flag)
            recursive_set(self)

        def canvasMoveEvent(self, p):
            x = p.x()
            y = p.y()
            pm = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            u = ""
            if self.mapLinearUnit == 'none':
                pass
            elif self.mapLinearUnit == 'meters':
                u = "m"
            elif self.mapLinearUnit == 'feet':
                u = "ft"
            elif self.mapLinearUnit == 'degrees':
                u = "deg"
            self.session.btnCoord.setText('x,y: {:.4f}, {:.4f} {:s}'.format(pm.x(), pm.y(), u))
            pass

        @staticmethod
        def point_feature_from_item(item):
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(item.x),
                                                               float(item.y))))
            feature.setAttributes([item.name, 0.0])
            return feature

        @staticmethod
        def line_feature_from_item(item, project_coordinates):
            link_coordinates = []
            link_coordinates.append(project_coordinates[item.inlet_node])
            link_coordinates.extend(item.vertices)
            link_coordinates.append(project_coordinates[item.outlet_node])

            link_points = [QgsPoint(float(coord.x), float(coord.y)) for coord in link_coordinates]
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolyline(link_points))
            feature.setAttributes([item.name, 0.0])
            return feature

        @staticmethod
        def polygon_feature_from_item(item):
            pts = [QgsPoint(float(coord.x), float(coord.y)) for coord in item.vertices]
            geometry = QgsGeometry.fromPolygon([pts])
            feature = QgsFeature()
            feature.setGeometry(geometry)
            feature.setAttributes([item.name, 0.0])
            return feature

        def addCoordinates(self, coordinates, layer_name):
            try:
                layer = QgsVectorLayer("Point", layer_name, "memory")
                provider = layer.dataProvider()

                # add fields
                provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                        QgsField("color", QtCore.QVariant.Double)])

                features = []
                if coordinates:
                    for coordinate_pair in coordinates:
                        # add a feature
                        try:
                            features.append(self.point_feature_from_item(coordinate_pair))
                        except Exception as ex:
                            if len(str(coordinate_pair.x)) > 0 and len(str(coordinate_pair.y)) > 0:
                                print "Did not add coordinate '" + coordinate_pair.name + "' (" +\
                                      str(coordinate_pair.x) + ", " +\
                                      str(coordinate_pair.y) + ") to map: " + str(ex)

                if features:
                    # changes are only possible when editing the layer
                    layer.startEditing()
                    provider.addFeatures(features)
                    layer.commitChanges()
                    layer.updateExtents()

                # create a new symbol layer with default properties
                symbol_layer = QgsSimpleMarkerSymbolLayerV2()
                symbol_layer.setColor(QColor(130, 180, 255, 255))

                # Label the coordinates if there are not too many of them
                if coordinates and len(coordinates) > 100:
                    symbol_layer.setSize(2.0)
                else:
                    if coordinates and hasattr(coordinates[0], "size"):
                        size = coordinates[0].size
                        symbol_layer.setSize(10.0)
                        symbol_layer.setOutlineColor(QColor('transparent'))
                        symbol_layer.setColor(QColor('transparent'))
                    else:
                        size = 8.0
                        symbol_layer.setSize(8.0)
                    pal_layer = QgsPalLayerSettings()
                    pal_layer.readFromLayer(layer)
                    pal_layer.enabled = True
                    pal_layer.fieldName = 'name'
                    pal_layer.placement= QgsPalLayerSettings.QuadrantAbove
                    pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, str(size), '')
                    pal_layer.writeToLayer(layer)

                # replace the default symbol layer with the new symbol layer
                layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)
                self.add_layer(layer)
                return layer
            except Exception as exBig:
                print("Error making layer: " + str(exBig))
                return None

        @staticmethod
        def set_default_point_renderer(layer):
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(130, 180, 255, 255))
            sym.setSize(8.0)
            layer.setRendererV2(QgsSingleSymbolRendererV2(sym))

        def addLinks(self, coordinates, links, layer_name, link_color=QColor('black'), link_width=1):
            try:
                layer = QgsVectorLayer("LineString", layer_name, "memory")
                provider = layer.dataProvider()

                symbol_layer = QgsSimpleLineSymbolLayerV2()
                symbol_layer.setColor(link_color)
                if link_width > 1 and (coordinates is None or len(coordinates) <= 100):
                    symbol_layer.setWidth(link_width)

                # markerLayer = markerMeta.createSymbolLayer({'width': '0.26',
                #                                             'color': '255,0,0',
                #                                             'rotate': '1',
                #                                             'placement': 'centralpoint',
                #                                             'offset': '0'})
                # subSymbol = markerLayer.subSymbol()

                layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)

                # add fields
                provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                        QgsField("color", QtCore.QVariant.Double)])

                features = []
                if links:
                    for link in links:
                        try:
                            features.append(self.line_feature_from_item(link, coordinates))
                        except Exception as exLink:
                            print "Skipping link " + link.name + ": " + str(exLink)

                if features:
                    # changes are only possible when editing the layer
                    layer.startEditing()
                    provider.addFeatures(features)
                    layer.commitChanges()
                    layer.updateExtents()
                # sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("LineDecoration").createSymbolLayer(
                #     {'width': '0.26', 'color': '0,0,0'})
                # layer.rendererV2().symbols()[0].appendSymbolLayer(sl)
                self.add_layer(layer)
                return layer
            except Exception as exBig:
                print("Error making layer: " + str(exBig))
                return None

        def add_layer(self, layer):
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            layers = self.canvas.layers()
            layers.append(layer)
            self.canvas.setLayerSet([QgsMapCanvasLayer(lyr) for lyr in layers])
            self.set_extent(self.canvas.fullExtent())

        def remove_layers(self, remove_layers):
            layer_names = []
            canvas_layers = self.canvas.layers()
            for layer in remove_layers:
                layer_names.append(layer.name())
                canvas_layers.remove(layer)
            QgsMapLayerRegistry.instance().removeMapLayers(layer_names)
            self.canvas.setLayerSet([QgsMapCanvasLayer(lyr) for lyr in canvas_layers])
            self.set_extent(self.canvas.fullExtent())

        @staticmethod
        def set_default_line_renderer(layer):
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor('gray'))
            sym.setWidth(3.5)
            layer.setRendererV2(QgsSingleSymbolRendererV2(sym))

        def addPolygons(self, polygons, layer_name, poly_color='lightgreen'):
            try:
                layer = QgsVectorLayer("Polygon", layer_name, "memory")
                provider = layer.dataProvider()

                # changes are only possible when editing the layer
                layer.startEditing()
                # add fields
                provider.addAttributes([QgsField("name", QtCore.QVariant.String),
                                        QgsField("color", QtCore.QVariant.Double)])

                features = []
                # Receivers = as in the above example 'Receivers' is a list of results
                poly_name = None
                poly_points = []
                if polygons:
                    for coordinate_pair in polygons:
                        if coordinate_pair.name != poly_name:
                            if poly_points:
                                # add a feature
                                feature = QgsFeature()
                                feature.setGeometry(QgsGeometry.fromPolygon([poly_points]))
                                feature.setAttributes([poly_name, 0.0])
                                features.append(feature)
                                poly_points = []
                            poly_name = coordinate_pair.name
                        poly_points.append(QgsPoint(float(coordinate_pair.x), float(coordinate_pair.y)))

                if poly_points:
                    # add a feature
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPolygon([poly_points]))
                    feature.setAttributes([poly_name, 0.0])
                    features.append(feature)

                if features:
                    layer.startEditing()
                    provider.addFeatures(features)
                    layer.commitChanges()
                    layer.updateExtents()

                self.set_default_polygon_renderer(layer, poly_color)
                self.add_layer(layer)
                return layer
            except Exception as exBig:
                print("Error making layer: " + str(exBig))
                return None

        @staticmethod
        def set_default_polygon_renderer(layer, poly_color='lightgreen'):
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(poly_color))
            layer.setRendererV2(QgsSingleSymbolRendererV2(sym))

        @staticmethod
        def validatedDefaultSymbol(geometryType):
            symbol = QgsSymbolV2.defaultSymbol(geometryType)
            if symbol is None:
                if geometryType == QGis.Point:
                    symbol = QgsMarkerSymbolV2()
                elif geometryType == QGis.Line:
                    symbol = QgsLineSymbolV2()
                elif geometryType == QGis.Polygon:
                    symbol = QgsFillSymbolV2()
            return symbol

        @staticmethod
        def applyGraduatedSymbologyStandardMode(layer, color_by, min=None, max=None):
            provider = layer.dataProvider()
            layer.startEditing()
            calculate_min_max = False
            if min is None or max is None:
                calculate_min_max = True
            for feature in provider.getFeatures():
                try:
                    feature_name = feature[0]
                    val = color_by[feature_name]
                    layer.changeAttributeValue(feature.id(), 1, val, True)
                    # feature[1] = val
                    if calculate_min_max:
                        if min is None or val < min:
                            min = val
                        if max is None or val > max:
                            max = val
                except Exception as ex:
                    print str(ex)
                    layer.changeAttributeValue(feature.id(), 1, 0.0, True)
            layer.commitChanges()

            # colorRamp = QgsVectorGradientColorRampV2.create(
            #     {'color1': '155,155,0,255', 'color2': '0,0,255,255',
            #      'stops': '0.25;255,255,0,255:0.50;0,255,0,255:0.75;0,255,255,255'})
            # renderer = QgsGraduatedSymbolRendererV2.createRenderer(layer, "color", 5,
            #                                                          QgsGraduatedSymbolRendererV2.Quantile, symbol, colorRamp)
            # renderer.setSizeScaleField("LABELRANK")
            # layer.setRendererV2(QgsSingleSymbolRendererV2(symbol))

            if min is None or max is None:
                min = 0
                max = 5
            increment = (max - min) / 5
            colorRamp = ((str(min) + ' to ' + str(round(min + 1*increment,2)), min, min + 1*increment, '#0000ff'), \
                         (str(round(min + 1*increment,2)) + ' to ' + str(round(min + 2*increment,2)), (min + 1*increment), (min + 2*increment), '#00ffff'), \
                         (str(round(min + 2*increment,2)) + ' to ' + str(round(min + 3*increment,2)), (min + 2*increment), (min + 3*increment), '#00ff00'), \
                         (str(round(min + 3*increment,2)) + ' to ' + str(round(min + 4*increment,2)), (min + 3*increment), (min + 4*increment), '#ffff00'), \
                         (str(round(min + 4*increment,2)) + ' to ' + str(round(max,2)), (min + 4*increment), max, '#ff0000'))
            ranges = []
            for label, lower, upper, color in colorRamp:
                symbol = EmbedMap.validatedDefaultSymbol(layer.geometryType())
                if layer.geometryType() == 0:
                    symbol.setSize(8.0)
                elif layer.geometryType() == 1:
                    symbol.setWidth(3.5)
                symbol.setColor(QtGui.QColor(color))
                rng = QgsRendererRangeV2(lower, upper, symbol, label)
                ranges.append(rng)
            renderer = QgsGraduatedSymbolRendererV2("color", ranges)

            layer.setRendererV2(renderer)

        def applyLegend(self):
            self.root = QgsProject.instance().layerTreeRoot()
            # self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
            self.model = QgsLayerTreeModel(self.root)
            self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
            self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
            self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
            self.model.setFlag(QgsLayerTreeModel.AllowSymbologyChangeState)
            self.model.setFlag(QgsLayerTreeModel.AllowLegendChangeState)
            self.model.setFlag(QgsLayerTreeModel.ShowLegend)
            self.view = QgsLayerTreeView()
            self.view.setModel(self.model)

            self.LegendDock = QDockWidget( "Legend", self )
            self.LegendDock.setObjectName( "legend" )
            # self.LegendDock.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )
            self.LegendDock.setWidget( self.view )
            self.LegendDock.setContentsMargins ( 9, 9, 9, 9 )
            # self.addDockWidget( Qt.LeftDockWidgetArea, self.LegendDock )

        def addVectorLayer(self, filename):
            layers = self.canvas.layers()
            layer_count = len(layers)
            #if filename.lower().endswith('.shp'):
            layer = QgsVectorLayer(filename, "layer_v_" + str(layer_count), "ogr")
            #elif filename.lower().endswith('.json'):
            #    layer=QgsVectorLayer(filename, "layer_v_" + str(layer_count), "GeoJson")
            if layer:
                self.add_layer(layer)

        def set_extent(self, extent):
            buffered_extent = extent.buffer(extent.height() / 20)
            self.canvas.setExtent(buffered_extent)
            self.canvas.refresh()

        def addRasterLayer(self, filename):
            if len(filename.strip()) > 0:
                layer = QgsRasterLayer(filename, "layer_r_" + str(self.canvas.layerCount() + 1))
                self.add_layer(layer)

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
        CAPTURE_LINE    = 1
        CAPTURE_POLYGON = 2

        def __init__(self, canvas, layer, layer_name, object_type, session):
            QgsMapTool.__init__(self, canvas)
            self.canvas          = canvas
            self.layer           = layer
            self.layer_name = layer_name
            self.object_type = object_type
            self.session = session
            self.rubberBand      = None
            self.tempRubberBand  = None
            self.capturedPoints  = []
            self.capturing       = False
            self.ruler           = None
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
            close_d = self.ruler.measureLine(QgsPoint(p_last), QgsPoint(p_0))
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
                return QGis.Line
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                return QGis.Polygon
            else:
                return QGis.Line

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

            bandSize     = self.rubberBand.numberOfVertices()
            tempBandSize = self.tempRubberBand.numberOfVertices()
            numPoints    = len(self.capturedPoints)

            if bandSize < 1 or numPoints < 1:
                return

            self.rubberBand.removePoint(-1)

            if bandSize > 1:
                if tempBandSize > 1:
                    point = self.rubberBand.getPoint(0, bandSize-2)
                    self.tempRubberBand.movePoint(tempBandSize-2, point)
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
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if len(points) < 3:
                    points = None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                points.append(points[0]) # Close polygon.

            self.stopCapturing()

            if points or self.inlet_node and self.outlet_node:
                new_object = self.object_type()
                new_object.vertices = []
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

            if self.captureMode == CaptureTool.CAPTURE_LINE:
                d = self.ruler.measureLine(layerCoords)
                msgBox.setText("Line Distance: " + str(d))
            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
                geometry = QgsGeometry.fromPolygon([layerCoords])
                a = self.ruler.measureArea(geometry)
                d = self.ruler.measurePerimeter(geometry)
                msgBox.setText("Perimeter Distance: " + str(d) + '\n' +
                               "Area: " + str(a))

            msgBox.setWindowTitle("Measure Dimension")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.exec_()
            del msgBox
            self.stopCapturing()
            pass

    class AddLinkTool(CaptureTool):
        def __init__(self, canvas, layer, layer_name, object_type, session):
            CaptureTool.__init__(self, canvas, layer, layer_name, object_type, session)
            self.build_spatial_index()

        def build_spatial_index(self):
            """ Build self.layer_spatial_indexes as cache of node locations eligible to be endpoints of a new link """
            self.layer_spatial_indexes = []
            for lyr in self.session.model_layers.nodes_layers:
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
                    print str(e)

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
                    print str(e1)

            if self.nearest_layer:
                iterator = self.nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(nearest_pt_id))
                if iterator:
                    self.nearest_feature = next(iterator)

            # return nearest_layer, nearest_feature, nearest_canvas_point, nearest_map_point, math.sqrt(nearest_distance)

        def addVertex(self, canvas_point):
            self.find_nearest_feature(canvas_point)
            # print("Found nearest distance " + str(nearest_distance))
            if self.nearest_feature:
                nearest_feature_name = self.nearest_feature.attributes()[0]
                if len(self.capturedPoints) == 0:
                    self.inlet_node = nearest_feature_name
                    canvas_point = self.nearest_canvas_point
                    map_point = self.nearest_map_point
                elif self.nearest_distance < 15:
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
            self.build_spatial_index()

        def build_spatial_index(self):
            self.layer_spatial_indexes = []
            for lyr in self.session.model_layers.all_layers:
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
                    print str(e)

        def make_center_point(self, geometry):
            pt = None
            if geometry.wkbType() == QGis.WKBLineString:
                line = geometry.asPolyline()
                pt = QgsPoint((line[0].x() + line[-1].x()) / 2, (line[0].y() + line[-1].y()) / 2)
            elif geometry.wkbType() == QGis.WKBPolygon:
                # Select subbasin by clicking closest to center of its bounding box
                box = geometry.boundingBox()
                pt = QgsPoint((box.xMinimum() + box.xMaximum()) / 2,
                              (box.yMinimum() + box.yMaximum()) / 2)
            elif geometry.wkbType() == QGis.WKBPoint:
                pt = geometry.asPoint()
            return pt

        def start_drag(self, event_pos):
            if self.tempRubberBand:  # Clean up old rubber band if we already have one
                self.end_drag()

            self.start_drag_position = event_pos
            color = QColor("red")
            color.setAlphaF(0.78)

            self.tempRubberBand = QgsRubberBand(self.canvas, QGis.Line)
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

        def canvasPressEvent(self, mouse_event):
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
                print str(e2) + '\n' + str(traceback.print_exc())

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
                            print("Nearest: " + "{:,}".format(pt.x()) + ", " + "{:,}".format(pt.y()))
                        sp_index += 1

                except Exception as e1:
                    print str(e1)
                layer_index += 1

            if nearest_feature_id > -1 and self.nearest_layer:
                iterator = self.nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(nearest_feature_id))
                if iterator:
                    self.nearest_feature = next(iterator)

            if make_distance_labels:
                self.distance_layer = self.session.map_widget.addCoordinates(distances, "Distances")
                self.canvas.refresh()

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
                self.find_nearest_feature(map_point)  #, True)
                if self.nearest_feature:
                    self.nearest_geometry = self.nearest_feature.geometry()
                    wkb_type = self.nearest_geometry.wkbType()
                    if wkb_type == QGis.WKBLineString:
                        vertex = self.nearest_geometry.asPolyline()[self.nearest_point_index]
                    elif wkb_type == QGis.WKBPolygon:
                        vertex = self.nearest_geometry.asPolygon()[0][self.nearest_point_index]
                    if vertex:
                        start_pos = self.toCanvasCoordinates(vertex)
                        #layer_point = self.toLayerCoordinates(self.nearest_layer, event_pos)
                        #vertex_coord, vertex, prev_vertex, next_vertex, dist_squared = self.nearest_geometry.closestVertex(layer_point)
                        #distance = math.sqrt(dist_squared)
                        #tolerance = self.calcTolerance(event_pos)
                        #if distance > tolerance: return
                        if mouse_event.button() == 1:  # LeftButton:
                            # Left click -> move vertex.
                            self.start_drag(start_pos)
                            #self.dragging = True
                            #self.feature = feature
                            #self.vertex = vertex
                            #self.moveVertexTo(event_pos)
                            self.canvas.refresh()
                        elif mouse_event.button() == 2:  # QtGui.Qt.RightButton:
                            # Right click -> delete vertex.
                            self.delete_vertex()
                            self.canvas.refresh()

            except Exception as e2:
                print str(e2) + '\n' + str(traceback.print_exc())


        # def canvasMoveEvent(self, event):
        #     if self.dragging:
        #         self.moveVertexTo(event.pos())
        #         self.canvas.refresh()

        def canvasReleaseEvent(self, mouse_event):
            if self.tempRubberBand and mouse_event.pos() != self.start_drag_position:
                self.nearest_layer.startEditing()
                self.moveVertexTo(mouse_event.pos())
                self.nearest_layer.commitChanges()
                self.canvas.refresh()
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
                                     self.nearest_feature.id(),
                                     self.nearest_geometry,
                                     self.nearest_point_index,
                                     start_pt.x(), start_pt.y(),
                                     layer_pt.x(), layer_pt.y())

            # Update this moved point in layer_spatial_indexes
            #self.build_spatial_index()
            #pt_index = self.nearest_point_index
            #if self.nearest_geometry.wkbType() == QGis.WKBPolygon:
            #    pt_index += 1
            #self.layer_spatial_indexes[self.nearest_spatial_index][1][pt_index] = layer_pt

        def delete_vertex(self):
            geometry = self.nearest_geometry
            wkb_type = geometry.wkbType()
            if wkb_type == QGis.WKBLineString:
                lineString = geometry.asPolyline()
                if len(lineString) <= 2:
                    return
            elif wkb_type == QGis.WKBPolygon:
                polygon = geometry.asPolygon()
                exterior = polygon[0]
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
                                if geometry.wkbType() == QGis.WKBLineString:
                                    points = geometry.asPolyline()[1:-1]  # skip first and last point which are nodes
                                    index = 1
                                elif geometry.wkbType() == QGis.WKBPolygon:
                                    points = geometry.asPolygon()[0]
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
                    print str(e)

    class SaveAsGis:
        @staticmethod
        def save_links(coordinates, links, link_attributes, file_name, driver_name="GeoJson"):
            layer = QgsVectorLayer("LineString", "links", "memory")
            provider = layer.dataProvider()

            # add fields
            provider.addAttributes([QgsField(link_attr, QtCore.QVariant.String) for link_attr in link_attributes])

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
                    feature.setAttributes([getattr(link, link_attr, '') for link_attr in link_attributes])
                    features.append(feature)

            # changes are only possible when editing the layer
            layer.startEditing()
            provider.addFeatures(features)
            layer.commitChanges()
            layer.updateExtents()

            QgsVectorFileWriter.writeAsVectorFormat(layer, file_name, "utf-8", layer.crs(), driver_name)

except:
    print "Skipping map_tools"
