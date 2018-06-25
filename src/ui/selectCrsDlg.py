# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Transformation tools
Description          : Help to use grids and towgs84 to transform a vector/raster
Date                 : April 16, 2011
copyright            : (C) 2011 by Giuseppe Sucameli (Faunalia)
email                : brush.tyler@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from qgis.gui import QgsProjectionSelectionDialog


class SelectCrsDlg(QDialog):
    def __init__(self, title, parent=None):
        QDialog.__init__(self)
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        self.selector = QgsProjectionSelectionDialog(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)

        layout.addWidget(self.selector)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(buttonBox, SIGNAL("rejected()"), self.reject)

    def epsg(self):
        return str(self.selector.selectedAuthId())

    def proj4string(self):
        return str(self.selector.selectedProj4String())

    def getProjection(self):
        if self.selector.selectedAuthId():
            return self.epsg()

        if self.selector.selectedProj4String():
            return self.proj4string()

        return ""

