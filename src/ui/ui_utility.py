import sys, os
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

class EmbedMap(QWidget):
    """ Main GUI Widget for map display inside vertical layout """
    def __init__(self, parent=None, **kwargs):
        super(EmbedMap, self).__init__(parent)
        layout = QVBoxLayout(self)
        #define QMapControl here
        #qmap = QMapControl()
        #layout.addWidget(qmap)
        canvas = QgsMapCanvas()
        canvas.useImageToRender(False)
        #canvas.setCanvasColor(QtGui.QColor.white)
        canvas.show()
        layers = []
        basemap = "C:/Data/gis/NE1_50M_SR_W.tif"
        layerbm = QgsRasterLayer(basemap, "basemap")
        QgsMapLayerRegistry.instance().addMapLayer(layerbm)


        shapefile = "C:/Data/gis/ne_50m_urban_areas.shp"
        layer=QgsVectorLayer(shapefile, "layer1","ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        canvas.setExtent(layer.extent())
        #canvas.setLayerSet([QgsMapCanvasLayer(layer)])

        shapefile2 = "C:/Data/gis/ne_50m_rivers_lake_centerlines.shp"
        layer2 = QgsVectorLayer(shapefile2, "layer2", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer2)
        #canvas.setLayerSet([QgsMapCanvasLayer(layer2)])
        layer2.rendererV2().symbols()[0].setColor(QColor("0000FF"))


        layers.append(QgsMapCanvasLayer(layer2))
        layers.append(QgsMapCanvasLayer(layer))
        layers.append(QgsMapCanvasLayer(layerbm))

        canvas.setLayerSet(layers)
        canvas.setExtent(QgsRectangle(-125, 31, -113, 38))

        layout.addWidget(canvas)

        #contents = QWidget()
        #contents.setLayout(layout)
        self.setLayout(layout)
        #self.setCentralWidget(self)

        #layout.addWidget(None)
        pass

class ObjectTreeView(QTreeWidget):
    ObjRoot = ['Title/Notes','Options','Climatology', 'Hydrology', \
               'Hydraulics','Quality','Curves', 'Time Series', 'Time Patterns', 'Map Labels']
    ObjOptions = ['General','Dates','Time Steps','Dynamic Wave','Interface Files','Reporting']
    ObjClimatology = ['Temperature','Evaporation','Wind Speed','Snow Melt','Areal Depletion',\
                      'Adjustment']
    ObjHydrology = ['Rain Gages','Subcatchments','Aquifers','Snow Packs','Unit Hydrographs', \
                    'LID Controls']
    ObjHydraulics = ['Nodes','Links','Transects','Controls']
    ObjNodes = ['Junctions','Outfalls','Dividers','Storage Units']
    ObjLinks = ['Conduits','Pumps','Orifices','Weirs','Outlets']
    ObjQuality = ['Pollutants','Land Uses']
    ObjCurves = ['Control Curves','Diversion Curves','Pump Curves','Rating Curves','Shape Curves',\
                 'Storage Curves','Tidal Curves']
    def __init__(self, parent=None, **kwargs):
        super(ObjectTreeView, self).__init__(parent)
