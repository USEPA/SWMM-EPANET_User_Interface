from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QFileInfo
from PyQt4.QtGui import *
#import qgis
import os
#print "PATH: ", os.environ['PATH']
#os.putenv("PATH", "c:\\OSGeo4W\\apps\\qgis\\bin;" + os.getenv("PATH", ""))
from qgis.core import QgsProject, QgsVectorLayer, QgsMapLayerRegistry
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer, QgsLayerTreeMapCanvasBridge

class EmbedMap(QWidget):
    """ Main GUI Widget for map display inside vertical layout """
    def __init__(self, parent=None, **kwargs):
        super(EmbedMap, self).__init__(parent)
        layout = QVBoxLayout(self)
        canvas = QgsMapCanvas(None)
        canvas.setCanvasColor(QColor(255,255,0))
        layer_filename = os.path.dirname(__file__) + os.path.sep + 'st.shp'
        if os.path.isfile(layer_filename):
            print "Opening: ", layer_filename
            layer = QgsVectorLayer(layer_filename, "States", "ogr")
            if not layer.isValid():
                # set extent to the extent of our layer
                canvas.setExtent(layer.extent())

                # set the map canvas layer set
                canvas.setLayerSet([QgsMapCanvasLayer(layer)])
            #  raise IOError, "Failed to open the layer"
            QgsMapLayerRegistry.instance().addMapLayer(layer)

        canvas.show()
        layout.addWidget(canvas)
        # project_path = os.path.dirname(__file__) + os.path.sep + 'test.qgs'
        # if os.exists(project_path):
        #     bridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), canvas)
        #     QgsProject.instance().read(QFileInfo(project_path))
        pass
