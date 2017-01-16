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
            #self.onGeometryChanged = onGeometryChanged
            self.session = session
            self.start_geom = None
            self.end_geom = None
            self.dragging = False
            self.feature = None
            self.vertex = None
            self.edit_type = ""
            self.pt_index = 0
            self.start_pos = None
            self.end_pos = None
            self.start_event_x = None
            self.start_event_y = None
            self.end_event_x = None
            self.end_event_y = None
            self.coord_x = None
            self.coord_y = None

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
                if self.start_event_x is None:
                    self.start_pos = self.toMapCoordinates(event.pos())
                    self.start_event_x = event.pos().x()
                    self.start_event_y = event.pos().y()
                    self.edit_type = "move"
                else:
                    self.canvasReleaseEvent(event)
                    return
                #self.moveVertexTo(event.pos())
            elif event.button() == QtCore.Qt.RightButton:
                # Right click -> delete vertex
                self.feature = feature
                self.vertex = vertex
                self.coord_x = vertexCoord.x() #in map coord
                self.coord_y = vertexCoord.y() #in map coord
                self.deleteVertex(feature, vertex)
                return
            self.canvas().refresh()
            pass

        def canvasMoveEvent(self, event):
            if self.dragging:
                self.moveVertexTo(event.pos())
                self.canvas().refresh()

        def canvasReleaseEvent(self, event):
            if self.dragging:
                #self.moveVertexTo(event.pos())
                #self.end_geom = self.copy_geometry(self.feature.geometry())
                self.end_pos = self.toMapCoordinates(event.pos())
                self.end_event_x = event.pos().x()
                self.end_event_y = event.pos().y()
                #d = self.start_pos.sqrDist(self.end_pos)
                d = self.calcCanvasDistance()
                if d > 4.0:
                    #self.layer.updateExtents()
                    #self.canvas().refresh()
                    self.dragging = False
                    #self.feature = None
                    #self.vertex = None
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

        def calcCanvasDistance(self):
            d = math.sqrt((self.end_event_x - self.start_event_x)**2 +
                          (self.end_event_y - self.start_event_y)**2)
            return d

        def moveVertexTo(self, pos):
            geometry = self.feature.geometry()
            layerPt = self.toLayerCoordinates(self.layer, pos)
            geometry.moveVertex(layerPt.x(), layerPt.y(), self.vertex)
            self.layer.changeGeometry(self.feature.id(), geometry)

        def deleteVertex(self, feature, vertex):
            self.edit_type = "delete"
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
                self.canvas().refresh()
                self.onGeometryChanged()

        def copy_geometry(self, geometry):
            if isinstance(geometry.asPolygon(), list):
                lv = geometry.asPolygon()
                vs = []
                vs.extend(lv)
                return QgsGeometry.fromPolygon(vs)
            else:
                return None

        def onGeometryChanged(self):
            if "move" in self.edit_type:
                from_pt = QPoint(self.start_event_x, self.start_event_y)
                to_pt = QPoint(self.end_event_x, self.end_event_y)
                self.start_pos = self.toMapCoordinates(from_pt)
                self.end_pos = self.toMapCoordinates(to_pt)
                self.session.edit_vertex(self.layer, self.feature, self.edit_type, self.vertex,
                                        self.start_pos.x(), self.start_pos.y(),
                                        self.end_pos.x(), self.end_pos.y())
            elif "delete" in self.edit_type:
                self.session.edit_vertex(self.layer, self.feature, self.edit_type, self.vertex,
                                         True, self.coord_x, self.coord_y)

            self.feature = None
            self.edit_type = ""
            self.vertex = None


    class EditVertex(QtGui.QUndoCommand):
        """Private class that edit a sub or link vertices from the model and the map. Accessed via delete_item method."""
        def __init__(self, session, layer, feature):
            QtGui.QUndoCommand.__init__(self, "Change geometry")
            self.session = session
            self.layer = layer
            self.subcentroids = self.session.model_layers.layer_by_name("subcentroids")
            self.sublinks = self.session.model_layers.layer_by_name("sublinks")
            self.feature = feature

        def redo(self):
            self.edit(False)

        def undo(self):
            self.edit(True)

        def edit(self, undo):
            pass
            # from qgis.core import QgsGeometry, QGis, QgsPoint
            # try:
            #     #self.layer.startEditing()
            #     if undo:
            #         geom = self.from_geom
            #     else:
            #         geom = self.to_geom
            #     self.layer.changeGeometry(self.feature.id(), geom)
            #     #self.layer.commitChanges()
            #     self.layer.updateExtents()
            #     self.layer.triggerRepaint()
            #     self.session.map_widget.canvas.refresh()
            #     self.update_centroidlinks(geom)
            # except Exception as ex:
            #     print("_EditVertex: " + str(ex) + '\n' + str(traceback.print_exc()))
            # try:
            #     self.setQgsMapTool()
            # except:
            #     pass

        def update_centroidlinks(self, geom):
            from qgis.core import QgsGeometry, QGis, QgsPoint
            feature_name = self.feature.attributes()[0]
            for section_field_name in self.session.section_types.values():
                try:
                    object = None
                    if self.layer == self.session.model_layers.layer_by_name(section_field_name):
                        section = getattr(self.session.project, section_field_name)
                        object = section.value[feature_name]
                        if section_field_name != "subcatchments":
                            if hasattr(object, "vertices"):
                                del object.vertices[:]
                                for v in geom.asPolyline():
                                    coord = Coordinate()
                                    coord.x = v.x()
                                    coord.y = v.y()
                                    object.vertices.append(coord)
                    if object is not None and hasattr(object, "centroid"):
                        new_c_g = geom.centroid()
                        new_c = new_c_g.asPoint()
                        object.centroid.x = str(new_c.x)
                        object.centroid.y = str(new_c.y)
                        for fc in self.subcentroids.getFeatures():
                            if fc["sub_modelid"] == feature_name:
                                # from qgis.core import QgsMap
                                change_map = {fc.id(): new_c_g}
                                self.subcentroids.dataProvider().changeGeometryValues(change_map)
                                break
                        for fl in self.sublinks.dataProvider().getFeatures():
                            if fl["inlet"] == self.feature["c_modelid"]:
                                if fl.geometry().wkbType() == QGis.WKBLineString:
                                    line = fl.geometry().asPolyline()
                                    new_l_g = QgsGeometry.fromPolyline([new_c, line[-1]])
                                    change_map = {fl.id(): new_l_g}
                                    self.sublinks.dataProvider().changeGeometryValues(change_map)
                                break

                    break
                except Exception as ex1:
                    print("Searching for object to edit vertex of: " + str(ex1) + '\n' + str(traceback.print_exc()))

    class MoveVertexz(EditVertex):
        """Private class that removes an item from the model and the map. Accessed via delete_item method."""

        def __init__(self, session, layer, feature, point_index, from_x, from_y, to_x, to_y):
            EditVertex.__init__(self, session, layer, feature)
            #self.session = session
            #self.layer = layer
            #self.subcentroids = self.session.model_layers.layer_by_name("subcentroids")
            #self.sublinks = self.session.model_layers.layer_by_name("sublinks")
            #self.feature = feature
            self.point_index = point_index
            self.from_x = from_x
            self.from_y = from_y
            self.to_x = to_x
            self.to_y = to_y

        def redo(self):
            self.move(False)

        def undo(self):
            self.move(True)

        def move(self, undo):
            from qgis.core import QgsGeometry, QGis, QgsPoint
            try:
                if not self.layer.isEditable():
                    self.layer.startEditing()

                if undo:
                    x = self.from_x
                    y = self.from_y
                else:
                    x = self.to_x
                    y = self.to_y

                geometry = self.feature.geometry()
                geometry.moveVertex(x, y, self.point_index)
                self.layer.changeGeometry(self.feature.id(), geometry)
                #self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()
                self.update_centroidlinks(geometry)
            except Exception as ex:
                print("_MoveVertex: " + str(ex) + '\n' + str(traceback.print_exc()))
            try:
                self.session.setQgsMapTool()
            except:
                pass


    class DeleteVertexz(EditVertex):
        """Private class that deletes a vertex from a polygon feature."""

        def __init__(self, session, layer, feature, point_index, point_deleted, coord_x, coord_y):
            EditVertex.__init__(self, session, layer, feature)
            # self.session = session
            # self.layer = layer
            # self.subcentroids = self.session.model_layers.layer_by_name("subcentroids")
            # self.sublinks = self.session.model_layers.layer_by_name("sublinks")
            # self.feature = feature
            self.point_index = point_index
            self.coord_x = coord_x
            self.coord_y = coord_y
            self.point_deleted = point_deleted

        def redo(self):
            self.delete(False)

        def undo(self):
            self.delete(True)

        def delete(self, undo):
            from qgis.core import QgsGeometry, QGis, QgsPoint
            try:
                if not self.layer.isEditable():
                    self.layer.startEditing()

                geometry = self.feature.geometry()
                if undo:
                    geometry.insertVertex(self.coord_x, self.coord_y, self.point_index)
                    self.point_deleted = False
                else:
                    if not self.point_deleted:
                        geometry.deleteVertex(self.point_index)
                        self.point_deleted = True

                self.layer.changeGeometry(self.feature.id(), geometry)
                # self.layer.commitChanges()
                self.layer.updateExtents()
                self.layer.triggerRepaint()
                self.session.map_widget.canvas.refresh()
                self.update_centroidlinks(geometry)
            except Exception as ex:
                print("DeleteVertexz: " + str(ex) + '\n' + str(traceback.print_exc()))
            try:
                #self.session.setQgsMapTool()
                pass
            except:
                pass

except:
    print "Skipping map_edit"
