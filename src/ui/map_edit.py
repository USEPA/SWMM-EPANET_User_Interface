try:
    from qgis.core import *
    from qgis.gui import *
    from PyQt4 import QtGui, QtCore, Qt
    from PyQt4.QtGui import *
    from PyQt4.Qt import *
    from core.coordinate import Coordinate, Polygon
    from svgs_rc import *
    import traceback
    import math
    import os
    from enum import Enum

    class EditTool(QgsMapTool):
        def __init__(self, mapCanvas, layer, session, onGeometryChanged):
            QgsMapTool.__init__(self, mapCanvas)
            self.setCursor(Qt.CrossCursor)
            self.layer = layer
            self.onGeometryChanged = onGeometryChanged
            self.session = session
            self.start_geom = None
            self.end_geom = None
            self.dragging = False
            self.feature = None
            self.vertex = None

        def canvasPressEvent(self, event):
            feature = self.findFeatureAt(event.pos())
            if feature == None:
                return
            #mapPt, layerPt = self.transformCoordinates(event.pos())
            layerPt = self.toLayerCoordinates(self.layer, event.pos())
            geometry = feature.geometry()
            vertexCoord, vertex, prevVertex, nextVertex, distSquared = \
                geometry.closestVertex(layerPt)
            distance = math.sqrt(distSquared)
            tolerance = self.calcTolerance(event.pos())
            if distance > tolerance:
                return
            if event.button() == QtCore.Qt.LeftButton:
                # Left click -> move vertex.
                self.dragging = True
                self.feature = feature
                self.vertex = vertex
                if self.start_geom is None:
                    self.start_geom = self.copy_geometry(geometry)
                else:
                    self.canvasReleaseEvent(event)
                    return
                self.moveVertexTo(event.pos())
            elif event.button() == QtCore.Qt.RightButton:
                # Right click -> delete vertex
                self.deleteVertex(feature, vertex)
            self.canvas().refresh()
            pass

        def canvasMoveEvent(self, event):
            if self.dragging:
                self.moveVertexTo(event.pos())
                self.canvas().refresh()

        def canvasReleaseEvent(self, event):
            if self.dragging:
                self.moveVertexTo(event.pos())
                self.end_geom = self.copy_geometry(self.feature.geometry())
                #self.layer.updateExtents()
                #self.canvas().refresh()
                self.dragging = False
                self.feature = None
                self.vertex = None
                self.onGeometryChanged()

        def canvasDoubleClickEvent(self, event):
            feature = self.findFeatureAt(event.pos())
            if feature == None:
                return
            #mapPt, layerPt = self.transformCoordinates(event.pos())
            layerPt = self.toLayerCoordinates(self.layer, event.pos())
            geometry = feature.geometry()
            self.start_geom = self.copy_geometry(geometry)
            distSquared, closestPt, beforeVertex = \
                geometry.closestSegmentWithContext(layerPt)
            distance = math.sqrt(distSquared)
            tolerance = self.calcTolerance(event.pos())
            if distance > tolerance: return
            geometry.insertVertex(closestPt.x(), closestPt.y(), beforeVertex)
            self.layer.changeGeometry(feature.id(), geometry)
            self.canvas().refresh()

        def findFeatureAt(self, pos):
            #mapPt, layerPt = self.transformCoordinates(pos)
            layerPt = self.toLayerCoordinates(self.layer, pos)
            tolerance = self.calcTolerance(pos)
            searchRect = QgsRectangle(layerPt.x() - tolerance,
                                      layerPt.y() - tolerance,
                                      layerPt.x() + tolerance,
                                      layerPt.y() + tolerance)
            request = QgsFeatureRequest()
            request.setFilterRect(searchRect)
            request.setFlags(QgsFeatureRequest.ExactIntersect)
            for feature in self.layer.getFeatures(request):
                return feature
            return None

        def calcTolerance(self, pos):
            pt1 = QPoint(pos.x(), pos.y())
            pt2 = QPoint(pos.x() + 10, pos.y())
            #mapPt1, layerPt1 = self.transformCoordinates(pt1)
            #mapPt2, layerPt2 = self.transformCoordinates(pt2)
            layerPt1 = self.toLayerCoordinates(self.layer, pt1)
            layerPt2 = self.toLayerCoordinates(self.layer, pt2)
            tolerance = layerPt2.x() - layerPt1.x()
            return tolerance

        def moveVertexTo(self, pos):
            geometry = self.feature.geometry()
            layerPt = self.toLayerCoordinates(self.layer, pos)
            geometry.moveVertex(layerPt.x(), layerPt.y(), self.vertex)
            self.layer.changeGeometry(self.feature.id(), geometry)

        def deleteVertex(self, feature, vertex):
            geometry = feature.geometry()
            if geometry.wkbType() == QGis.WKBLineString:
                lineString = geometry.asPolyline()
                if len(lineString) <= 2:
                    return
            elif geometry.wkbType() == QGis.WKBPolygon:
                polygon = geometry.asPolygon()
                exterior = polygon[0]
                if len(exterior) <= 4:
                    return
            if geometry.deleteVertex(vertex):
                self.layer.changeGeometry(feature.id(), geometry)
                #self.onGeometryChanged()

        def copy_geometry(self, geometry):
            if isinstance(geometry.asPolygon(), list):
                return QgsGeometry.fromPolygon(geometry.asPolygon())
            else:
                return None

        def onGeometryChanged(self):
            self.session.edit_vertex(self.nearest_layer,
                                     self.nearest_feature,
                                     self.start_geom, self.end_geom)
            self.start_geom = None

except:
    print "Skipping map_edit"
