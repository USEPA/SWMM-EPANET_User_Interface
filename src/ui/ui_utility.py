# import os, sys
# #oldpath = os.environ['PATH']
# #g4w_path = 'C:\\OSGeo4W64\\'
# #os.environ['PATH'] = g4w_path + 'apps\\qgis\\bin;' + g4w_path + 'bin;'
# #sys.path.extend([g4w_path + 'apps\\qgis\\python', g4w_path + 'apps\\qgis\\python\\plugins',
# #                 g4w_path + 'apps\\Python27\\DLLs', g4w_path + 'apps\\Python27',
# #                 g4w_path + 'apps\\Python27\\lib', g4w_path + 'apps\\Python27\\lib\\site-packages'])
# os.environ['QT_API'] = 'pyqt'
# import sip
# sip.setapi("QString", 2)
# sip.setapi("QVariant", 2)
# import traceback
# from PyQt4 import QtGui, QtCore
# from PyQt4.QtGui import *
#
# try:
#     from qgis.core import *
#     from qgis.gui import *
#     from map_tools import CaptureTool
#
#     class EmbedMap(QWidget):
#         """ Main GUI Widget for map display inside vertical layout """
#         def __init__(self, mapCanvas, session, parent=None, **kwargs):
#             super(EmbedMap, self).__init__(parent)
#             #define QMapControl here
#             #qmap = QMapControl()
#             #layout.addWidget(qmap)
#             #self.layers = [] #kwargs['layers']
#             self.canvas = mapCanvas  #QgsMapCanvas()
#             self.layers = mapCanvas.layers()
#             self.canvas.setMouseTracking(True)
#             self.canvas.useImageToRender(False)
#             #canvas.setCanvasColor(QtGui.QColor.white)
#             self.canvas.show()
#
#             self.session = session
#
#             self.canvas.setLayerSet(self.layers)
#             #self.canvas.setExtent(layerbm.extent())
#
#             #self.panTool = PanTool(self.canvas)
#             #self.panTool.setAction(self.session.actionPan)
#
#             self.panTool = QgsMapToolPan(self.canvas)
#             self.panTool.setAction(self.session.actionPan)
#
#             self.zoomInTool = QgsMapToolZoom(self.canvas, False)
#             self.zoomInTool.setAction(self.session.actionZoom_in)
#
#             self.zoomOutTool = QgsMapToolZoom(self.canvas, True)
#             self.zoomOutTool.setAction(self.session.actionZoom_out)
#
#             self.qgisNewFeatureTool = None
#
#             QtCore.QObject.connect(self.canvas, QtCore.SIGNAL("xyCoordinates(QgsPoint)"), \
#                                    self.canvasMoveEvent)
#
#             layout = QVBoxLayout(self)
#             layout.setContentsMargins(0, 0, 0, 0)
#             layout.addWidget(self.canvas)
#
#             #contents = QWidget()
#             #contents.setLayout(layout)
#
#             self.setLayout(layout)
#             #self.setCentralWidget(self)
#
#             #layout.addWidget(None)
#             self.setMouseTracking(True)
#             pass
#
#         def setZoomInMode(self):
#             if self.session.actionZoom_in.isChecked():
#                 self.canvas.setMapTool(self.zoomInTool)
#                 #self.zoomInTool.setCursor(QtCore.Qt.CrossCursor)
#                 #QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
#             else:
#                 self.canvas.unsetMapTool(self.zoomInTool)
#                 #self.zoomInTool.setCursor(QtCore.Qt.ArrowCursor)
#                 #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
#             pass
#
#         def setZoomOutMode(self):
#             if self.session.actionZoom_out.isChecked():
#                 self.canvas.setMapTool(self.zoomOutTool)
#                 #self.zoomOutTool.setCursor(QtCore.Qt.SplitHCursor)
#                 #QApplication.setOverrideCursor(QtCore.Qt.SplitHCursor)
#             else:
#                 self.canvas.unsetMapTool(self.zoomOutTool)
#                 #self.zoomOutTool.setCursor(QtCore.Qt.ArrowCursor)
#                 #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
#             pass
#
#         def setPanMode(self):
#             if self.session.actionPan.isChecked():
#                 self.canvas.setMapTool(self.panTool)
#                 #self.panTool.setCursor(QtCore.Qt.OpenHandCursor)
#                 #QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
#             else:
#                 self.canvas.unsetMapTool(self.panTool)
#                 #self.panTool.setCursor(QtCore.Qt.ArrowCursor)
#                 #QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
#
#         def setAddFeatureMode(self):
#             if self.session.actionAdd_Feature.isChecked():
#                 if self.qgisNewFeatureTool == None:
#                     if self.layers != None and len(self.layers) > 0:
#                         self.qgisNewFeatureTool = CaptureTool(self.canvas, self.canvas.layer(0), \
#                                                   self.session.onGeometryAdded, \
#                                                   CaptureTool.CAPTURE_POLYGON)
#                         self.qgisNewFeatureTool.setAction(self.session.actionAdd_Feature)
#                 if self.qgisNewFeatureTool != None:
#                     self.canvas.setMapTool(self.qgisNewFeatureTool)
#             else:
#                 self.canvas.unsetMapTool(self.qgisNewFeatureTool)
#
#         def zoomfull(self):
#             self.canvas.zoomToFullExtent()
#
#         def setMouseTracking(self, flag):
#             def recursive_set(parent):
#                 for child in parent.findChildren(QtCore.QObject):
#                     try:
#                         child.setMouseTracking(flag)
#                     except:
#                         pass
#                     recursive_set(child)
#             QtGui.QWidget.setMouseTracking(self, flag)
#             recursive_set(self)
#
#         def canvasMoveEvent(self, p):
#             x = p.x()
#             y = p.y()
#             pm = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
#             self.session.btnCoord.setText('x,y: {:.4f}, {:.4f}'.format(pm.x(), pm.y()))
#             pass
#
#         def addVectorLayer(self, filename):
#             if filename.lower().endswith('.shp'):
#                     layerCtr = len(self.layers)
#                     layer=QgsVectorLayer(filename, "layer_v_" + str(layerCtr), "ogr")
#                     QgsMapLayerRegistry.instance().addMapLayer(layer)
#                     self.layers.append(QgsMapCanvasLayer(layer))
#                     self.canvas.setLayerSet(self.layers)
#                     if layerCtr ==0:
#                         self.canvas.setExtent(layer.extent())
#                     else:
#                         self.canvas.setExtent(self.canvas.extent())
#                     self.canvas.refresh()
#                     #self.canvas.refreshAllLayers()
#
#         def addRasterLayer(self, filename):
#             if len(filename.strip()) > 0:
#                     layerCtr = len(self.layers)
#                     layer=QgsRasterLayer(filename, "layer_r_" + str(layerCtr))
#                     QgsMapLayerRegistry.instance().addMapLayer(layer)
#                     self.layers.append(QgsMapCanvasLayer(layer))
#                     self.canvas.setLayerSet(self.layers)
#                     if layerCtr ==0:
#                         self.canvas.setExtent(layer.extent())
#                     else:
#                         self.canvas.setExtent(self.canvas.extent())
#
#     class PanTool(QgsMapTool):
#         def __init__(self, mapCanvas):
#             QgsMapTool.__init__(self, mapCanvas)
#             self.setCursor(QtCore.Qt.OpenHandCursor)
#             self.dragging = False
#
#         def canvasPressEvent(self, event):
#             if event.button() == QtCore.Qt.LeftButton:
#                 self.dragging = True
#                 self.canvas().panAction(event)
#
#         def canvasReleaseEvent(self, event):
#             if event.button() == QtCore.Qt.LeftButton and self.dragging:
#                 self.canvas().panActionEnd(event.pos())
#                 self.dragging = False
#
# except:
#     print "skipping qgis in ui_utility"