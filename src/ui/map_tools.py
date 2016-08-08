try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import *
    import os

    class EmbedMap(QWidget):
        """ Main GUI Widget for map display inside vertical layout """
        def __init__(self, mapCanvas, session, main_form=None, **kwargs):
            super(EmbedMap, self).__init__(main_form)
            self.main_form = main_form
            #define QMapControl here
            #qmap = QMapControl()
            #layout.addWidget(qmap)
            #self.layers = [] #kwargs['layers']
            self.canvas = mapCanvas  #QgsMapCanvas()
            self.layers = mapCanvas.layers()
            self.canvas.setMouseTracking(True)
            self.canvas.useImageToRender(False)
            #canvas.setCanvasColor(QtGui.QColor.white)
            self.canvas.show()

            self.session = session

            self.canvas.setLayerSet(self.layers)
            #self.canvas.setExtent(layerbm.extent())

            #self.panTool = PanTool(self.canvas)
            #self.panTool.setAction(self.session.actionPan)

            self.panTool = QgsMapToolPan(self.canvas)
            self.panTool.setAction(self.session.actionPan)

            self.zoomInTool = QgsMapToolZoom(self.canvas, False)
            self.zoomInTool.setAction(self.session.actionZoom_in)

            self.zoomOutTool = QgsMapToolZoom(self.canvas, True)
            self.zoomOutTool.setAction(self.session.actionZoom_out)

            self.selectTool = None

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
                    if self.layers and len(self.layers) > 0:
                        self.selectTool = SelectMapTool(self.canvas, self.main_form)
                        self.selectTool.setAction(self.session.actionMapSelectObj)
                if self.selectTool:
                    self.canvas.setMapTool(self.selectTool)
            else:
                self.canvas.unsetMapTool(self.selectTool)

        def setAddFeatureMode(self):
            # Temporarily hijacked to test properties editor
            layer = self.canvas.layers()[0]
            self.layer_properties_widget = QgsLayerPropertiesWidget(
                    layer.rendererV2().symbol().symbolLayers()[0],
                    layer.rendererV2().symbol(),
                    layer)
            self.layer_properties_widget.setMapCanvas(self.canvas)
            self.layer_properties_widget.show()
            # if self.session.actionAdd_Feature.isChecked():
            #     if self.qgisNewFeatureTool is None:
            #         if self.layers and len(self.layers) > 0:
            #             self.qgisNewFeatureTool = CaptureTool(self.canvas, self.canvas.layer(0),
            #                                                   self.session.onGeometryAdded,
            #                                                   CaptureTool.CAPTURE_POLYGON)
            #             self.qgisNewFeatureTool.setAction(self.session.actionAdd_Feature)
            #     if self.qgisNewFeatureTool:
            #         self.canvas.setMapTool(self.qgisNewFeatureTool)
            # else:
            #     self.canvas.unsetMapTool(self.qgisNewFeatureTool)

        def zoomfull(self):
            self.canvas.zoomToFullExtent()

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

        def addCoordinates(self, coordinates):
            layer = QgsVectorLayer("Point", "Nodes", "memory")
            provider = layer.dataProvider()

            # changes are only possible when editing the layer
            layer.startEditing()
            # add fields
            provider.addAttributes([QgsField("name", QtCore.QVariant.String)])

            features = []
            # Receivers = as in the above example 'Receivers' is a list of results
            for coordinate_pair in coordinates:
                # add a feature
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(coordinate_pair.x), float(coordinate_pair.y))))
                feature.setAttributes([coordinate_pair.name])
                features.append(feature)

            layer.startEditing()
            provider.addFeatures(features)
            layer.commitChanges()
            layer.updateExtents()

            # create a new symbol layer with default properties
            symbol_layer = QgsSimpleMarkerSymbolLayerV2()
            symbol_layer.setColor(QColor(130, 180, 255, 220))

            # Label the coordinates if there are not too many of them
            if len(coordinates) > 100:
                symbol_layer.setSize(2.0)
            else:
                symbol_layer.setSize(8.0)
                pal_layer = QgsPalLayerSettings()
                pal_layer.readFromLayer(layer)
                pal_layer.enabled = True
                pal_layer.fieldName = 'ID'
                pal_layer.placement= QgsPalLayerSettings.QuadrantAbove
                pal_layer.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', '')
                pal_layer.writeToLayer(layer)

            # replace the default symbol layer with the new symbol layer
            layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)

            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setLayerSet(self.layers)
            return layer

        def addLinks(self, coordinates, links, layer_name, link_attr, link_color=QColor('black')):
            layer = QgsVectorLayer("LineString", layer_name, "memory")
            provider = layer.dataProvider()

            symbol_layer = QgsSimpleLineSymbolLayerV2()
            symbol_layer.setColor(link_color)
            if len(coordinates) <= 100:
                symbol_layer.setWidth(2.5)

            # markerLayer = markerMeta.createSymbolLayer({'width': '0.26',
            #                                             'color': '255,0,0',
            #                                             'rotate': '1',
            #                                             'placement': 'centralpoint',
            #                                             'offset': '0'})
            # subSymbol = markerLayer.subSymbol()

            layer.rendererV2().symbols()[0].changeSymbolLayer(0, symbol_layer)

            # changes are only possible when editing the layer
            layer.startEditing()
            # add fields
            provider.addAttributes([QgsField("name", QtCore.QVariant.String)])

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
                    feature.setAttributes([getattr(link, link_attr, '')])
                    features.append(feature)

            layer.startEditing()
            provider.addFeatures(features)
            layer.commitChanges()
            layer.updateExtents()
            # sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("LineDecoration").createSymbolLayer(
            #     {'width': '0.26', 'color': '0,0,0'})
            # layer.rendererV2().symbols()[0].appendSymbolLayer(sl)
            # layerCtr = len(self.layers)
            # layerCtr = len(self.layers)
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setLayerSet(self.layers)

        def addPolygons(self, polygons, layer_name):
            layer = QgsVectorLayer("Polygon", layer_name, "memory")
            provider = layer.dataProvider()

            # changes are only possible when editing the layer
            layer.startEditing()
            # add fields
            provider.addAttributes([QgsField("name", QtCore.QVariant.String)])

            features = []
            # Receivers = as in the above example 'Receivers' is a list of results
            poly_name = None
            poly_points = []
            for coordinate_pair in polygons:
                if coordinate_pair.name != poly_name:
                    if poly_points:
                        # add a feature
                        feature = QgsFeature()
                        feature.setGeometry(QgsGeometry.fromPolygon([poly_points]))
                        feature.setAttributes([poly_name])
                        features.append(feature)
                        poly_points = []
                    poly_name = coordinate_pair.name
                poly_points.append(QgsPoint(float(coordinate_pair.x), float(coordinate_pair.y)))

            if poly_points:
                # add a feature
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolygon([poly_points]))
                feature.setAttributes([poly_name])
                features.append(feature)

            layer.startEditing()
            provider.addFeatures(features)
            layer.commitChanges()
            layer.updateExtents()
            # layerCtr = len(self.layers)
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setLayerSet(self.layers)

        def addVectorLayer(self, filename):
            if filename.lower().endswith('.shp'):
                layerCtr = len(self.layers)
                layer=QgsVectorLayer(filename, "layer_v_" + str(layerCtr), "ogr")
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                self.layers.append(QgsMapCanvasLayer(layer))
                self.canvas.setLayerSet(self.layers)
                if layerCtr == 0:
                    self.canvas.setExtent(layer.extent())
                else:
                    self.canvas.setExtent(self.canvas.extent())
                self.canvas.refresh()
                #self.canvas.refreshAllLayers()

        def addRasterLayer(self, filename):
            if len(filename.strip()) > 0:
                    layerCtr = len(self.layers)
                    layer=QgsRasterLayer(filename, "layer_r_" + str(layerCtr))
                    QgsMapLayerRegistry.instance().addMapLayer(layer)
                    self.layers.append(QgsMapCanvasLayer(layer))
                    self.canvas.setLayerSet(self.layers)
                    if layerCtr ==0:
                        self.canvas.setExtent(layer.extent())
                    else:
                        self.canvas.setExtent(self.canvas.extent())

        def saveVectorLayers(self, folder):
            layer_index = 0
            for map_layer in self.layers:
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

    class SelectMapTool(QgsMapToolEmitPoint):
        def __init__(self, canvas, main_form):
            self.canvas = canvas
            self.main_form = main_form
            QgsMapToolEmitPoint.__init__(self, self.canvas)
            self.spatial_index = QgsSpatialIndex()
            self.layer = self.canvas.layers()[0]
            # for lyr in self.canvas.layers():
            try:
                provider = self.layer.dataProvider()
                # TODO: check whether provider is vector and has ID field
                feat = QgsFeature()
                feats = provider.getFeatures()  # get all features in layer
                # insert features to index
                while feats.nextFeature(feat):
                    self.spatial_index.insertFeature(feat)
            except Exception as e:
                print str(e)

        def canvasPressEvent(self, e):
            try:
                clicked_point = self.toMapCoordinates(e.pos())
                nearest_feature = self.spatial_index.nearestNeighbor(clicked_point, 1)[0]
                if not (e.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier)):
                    self.layer.removeSelection()
                    self.main_form.select_id(None)
                # self.layer.setSelectedFeatures([nearest_feature])
                self.layer.select(nearest_feature)
                iterator = self.layer.getFeatures(QgsFeatureRequest().setFilterFid(nearest_feature))
                feature = next(iterator)
                self.main_form.select_id(feature.attributes()[0])
            except Exception as e:
                print str(e)


    class SaveAsGis:
        @staticmethod
        def save_links(coordinates, links, layer_name, link_attributes):
            layer = QgsVectorLayer("LineString", layer_name, "memory")
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



except:
    print "Skipping map_tools"
