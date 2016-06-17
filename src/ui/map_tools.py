try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import *

    class EmbedMap(QWidget):
        """ Main GUI Widget for map display inside vertical layout """
        def __init__(self, mapCanvas, session, main_form=None, **kwargs):
            super(EmbedMap, self).__init__(main_form)
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
            pass

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

        def setAddFeatureMode(self):
            if self.session.actionAdd_Feature.isChecked():
                if self.qgisNewFeatureTool is None:
                    if self.layers and len(self.layers) > 0:
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
            provider.addAttributes([QgsField("ID", QtCore.QVariant.String)])

            features = []
            # Receivers = as in the above example 'Receivers' is a list of results
            for coordinate_pair in coordinates:
                # add a feature
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(coordinate_pair.X, coordinate_pair.Y)))
                feature.setAttributes([coordinate_pair.id])
                features.append(feature)

            layer.startEditing()
            layer.addFeatures(features)
            layer.commitChanges()
            layer.updateExtents()
            layerCtr = len(self.layers)
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            self.layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setLayerSet(self.layers)
            if layerCtr == 0:
                self.canvas.setExtent(layer.extent())
            else:
                self.canvas.setExtent(self.canvas.extent())
            self.canvas.refresh()

        def addVectorLayer(self, filename):
            if filename.lower().endswith('.shp'):
                layerCtr = len(self.layers)
                layer=QgsVectorLayer(filename, "layer_v_" + str(layerCtr), "ogr")
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                self.layers.append(QgsMapCanvasLayer(layer))
                self.canvas.setLayerSet(self.layers)
                if layerCtr ==0:
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

except:
    print "Skipping map_tools"
