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
        layout.addWidget(None)
        pass
