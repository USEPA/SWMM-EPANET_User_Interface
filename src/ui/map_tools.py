try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore, Qt
    from PyQt4.QtGui import *
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
            self.addPointTool = None

            self.qgisNewFeatureTool = None

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
                if self.selectTool is None:
                    if self.canvas.layers():
                        self.selectTool = SelectMapTool(self.canvas, self.session)
                        self.selectTool.setAction(self.session.actionMapSelectObj)
                if self.selectTool:
                    self.canvas.setMapTool(self.selectTool)
            else:
                self.canvas.unsetMapTool(self.selectTool)

        def clearSelectableObjects(self):
            self.layer_spatial_indexes = []
            for layer in self.canvas.layers():
                if isinstance(layer, QgsVectorLayer):
                    layer.removeSelection()

        def find_feature(self, layer, feature_name):
            for feature in layer.getFeatures(QgsFeatureRequest(QgsExpression('"name"=' + "'" + feature_name + "'"))):
                return feature

        def setAddPointMode(self, action_obj, layer_name):
            """Start interactively adding points to point layer layer_name using tool button action_obj"""
            if action_obj.isChecked():
                # QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
                layer = getattr(self.session.model_layers, layer_name)
                self.session.select_named_items(layer, None)
                for obj_type, name in self.session.section_types.iteritems():
                    if name == layer_name:
                        if self.addPointTool:
                            QApplication.restoreOverrideCursor()
                            self.canvas.unsetMapTool(self.addPointTool)

                        self.addPointTool = AddPointTool(self.canvas, layer, layer_name, obj_type, self.session)
                        self.addPointTool.setAction(action_obj)
                        self.canvas.setMapTool(self.addPointTool)

            elif self.addPointTool and self.addPointTool.layer_name == layer_name:
                QApplication.restoreOverrideCursor()
                self.canvas.unsetMapTool(self.addPointTool)
                self.addPointTool = None

        def setAddFeatureMode(self):
            """This is an example method for interactively adding a polygon, need to make this add a subcatchment"""

            # Test of activating QGIS properties editor, does not belong in this method
            # layer = self.canvas.layers()[0]
            # self.layer_properties_widget = QgsLayerPropertiesWidget(
            #         layer.rendererV2().symbol().symbolLayers()[0],
            #         layer.rendererV2().symbol(),
            #         layer)
            # self.layer_properties_widget.setMapCanvas(self.canvas)
            # self.layer_properties_widget.show()
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
            self.session.btnCoord.setText('x,y: {:.4f}, {:.4f}'.format(pm.x(), pm.y()))
            pass

        @staticmethod
        def point_feature_from_item(item):
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(item.x),
                                                               float(item.y))))
            feature.setAttributes([item.name, 0.0])
            return feature

        @staticmethod
        def line_feature_from_item(item, inlet_coord, outlet_coord):
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPolyline([
                QgsPoint(float(inlet_coord.x), float(inlet_coord.y)),
                QgsPoint(float(outlet_coord.x), float(outlet_coord.y))]))
            feature.setAttributes([item.name, 0.0])
            return feature

        def addCoordinates(self, coordinates, layer_name):
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

        @staticmethod
        def set_default_point_renderer(layer):
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(130, 180, 255, 255))
            sym.setSize(8.0)
            layer.setRendererV2(QgsSingleSymbolRendererV2(sym))

        def addLinks(self, coordinates, links, layer_name, link_color=QColor('black'), link_width=1):
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
                        inlet_coord = coordinates[link.inlet_node]
                        outlet_coord = coordinates[link.outlet_node]
                        if inlet_coord and outlet_coord:
                            features.append(self.line_feature_from_item(link, inlet_coord, outlet_coord))
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

        def saveVectorLayers(self, folder):
            layer_index = 0
            if hasattr(self.session, "model_layers"):
                model_layers = self.session.model_layers.all_layers
            else:
                model_layers = self.canvas.layers()
            for map_layer in model_layers:
                try:
                    vector_layer = map_layer.layer()
                    layer_index += 1
                    file_name = os.path.join(folder, "layer" + str(layer_index) + ".json")

                    QgsVectorFileWriter.writeAsVectorFormat(vector_layer, file_name, "utf-8", vector_layer.crs(),
                                                            driverName="GeoJson")
                except Exception as e:
                    print str(e)

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

        def __init__(self, canvas, layer, onGeometryAdded, captureMode):
            QgsMapTool.__init__(self, canvas)
            self.canvas          = canvas
            self.layer           = layer
            self.onGeometryAdded = onGeometryAdded
            self.captureMode     = captureMode
            self.rubberBand      = None
            self.tempRubberBand  = None
            self.capturedPoints  = []
            self.capturing       = False
            self.setCursor(QtCore.Qt.CrossCursor)

        def canvasReleaseEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                if not self.capturing:
                    self.startCapturing()
                self.addVertex(event.pos())
            elif event.button() == QtCore.Qt.RightButton:
                points = self.getCapturedGeometry()
                self.stopCapturing()
                if points:
                    self.geometryCaptured(points)

        def canvasMoveEvent(self, event):
            if self.tempRubberBand and self.capturing:
                mapPt,layerPt = self.transformCoordinates(event.pos())
                self.tempRubberBand.movePoint(mapPt)

        def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Backspace or \
               event.key() == QtCore.Qt.Key_Delete:
                self.removeLastVertex()
                event.ignore()
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                points = self.getCapturedGeometry()
                self.stopCapturing()
                if points:
                    self.geometryCaptured(points)

        def transformCoordinates(self, canvasPt):
            return self.toMapCoordinates(canvasPt), self.toLayerCoordinates(self.layer, canvasPt)

        def startCapturing(self):
            color = QColor("red")
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
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                return QGis.Polygon
            else:
                return QGis.Line

        def stopCapturing(self):
            if self.rubberBand:
                self.canvas.scene().removeItem(self.rubberBand)
                self.rubberBand = None
            if self.tempRubberBand:
                self.canvas.scene().removeItem(self.tempRubberBand)
                self.tempRubberBand = None
            self.capturing = False
            self.capturedPoints = []
            self.canvas.refresh()

        def addVertex(self, canvasPoint):
            mapPt,layerPt = self.transformCoordinates(canvasPoint)

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

        def getCapturedGeometry(self):
            points = self.capturedPoints
            if self.captureMode == CaptureTool.CAPTURE_LINE:
                if len(points) < 2:
                    return None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                if len(points) < 3:
                    return None
            if self.captureMode == CaptureTool.CAPTURE_POLYGON:
                points.append(points[0]) # Close polygon.
            return points

        def geometryCaptured(self, layerCoords):
            if self.captureMode == CaptureTool.CAPTURE_LINE:
                geometry = QgsGeometry.fromPolyline(layerCoords)
            elif self.captureMode == CaptureTool.CAPTURE_POLYGON:
                geometry = QgsGeometry.fromPolygon([layerCoords])

            if geometry:
                feature = QgsFeature()
                feature.setGeometry(geometry)
                self.layer.startEditing()
                self.layer.addFeature(feature)
                self.layer.commitChanges()
                self.layer.updateExtents()
                self.onGeometryAdded()


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
        def __init__(self, canvas, session):
            self.canvas = canvas
            self.session = session
            self.start_drag_position = None
            self.tempRubberBand = None
            QgsMapToolEmitPoint.__init__(self, self.canvas)
            self.build_spatial_index()

        def build_spatial_index(self):
            self.layer_spatial_indexes = []
            if hasattr(self.session, "model_layers"):
                model_layers = self.session.model_layers.all_layers
            else:
                model_layers = self.canvas.layers()
            for lyr in model_layers:
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
                            self.layer_spatial_indexes.append((lyr, spatial_index, ids))
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

        def start_drag(self, mouse_event):
            self.start_drag_position = mouse_event.pos()
            color = QColor("red")
            color.setAlphaF(0.78)

            self.tempRubberBand = QgsRubberBand(self.canvas, QGis.Line)
            self.tempRubberBand.setWidth(2)
            self.tempRubberBand.setColor(color)
            self.tempRubberBand.setLineStyle(QtCore.Qt.DotLine)
            self.tempRubberBand.addPoint(self.toMapCoordinates(mouse_event.pos()))
            self.tempRubberBand.show()

        def end_drag(self):
            self.start_drag_position = None
            if self.tempRubberBand:
                self.canvas.scene().removeItem(self.tempRubberBand)
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
                extending = mouse_event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier)

                self.selected_names = []
                map_point = self.toMapCoordinates(mouse_event.pos())
                self.nearest_layer, nearest_feature = self.find_nearest_feature(map_point)
                if nearest_feature:
                    nearest_feature_name = nearest_feature.attributes()[0]
                else:
                    nearest_feature_name = None

                previously_selected = []
                for feat in self.nearest_layer.selectedFeatures():
                    previously_selected.append(feat.attributes()[0])

                if not extending and nearest_feature_name and nearest_feature_name in previously_selected:
                    # Clicking an already-selected item starts moving all selected items
                    self.start_drag(mouse_event)
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

        def find_nearest_feature(self, map_point):
            nearest_layer = None
            nearest_feature = None
            nearest_pt_id = -1
            nearest_distance = float("inf")
            for (lyr, points, ids) in self.layer_spatial_indexes:
                try:
                    pt_index = 0
                    for pt in points:
                        distance = map_point.sqrDist(pt)
                        if distance < nearest_distance:
                            nearest_layer = lyr
                            nearest_pt_id = ids[pt_index]
                            nearest_distance = distance
                        pt_index += 1

                except Exception as e1:
                    print str(e1)

            if nearest_layer:
                iterator = nearest_layer.getFeatures(QgsFeatureRequest().setFilterFid(nearest_pt_id))
                if iterator:
                    nearest_feature = next(iterator)

            return nearest_layer, nearest_feature

        def canvasDoubleClickEvent(self, e):
            self.session.edit_selected_objects()


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
