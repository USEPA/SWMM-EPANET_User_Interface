# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmPlotViewerDesigner.ui'
#
# Created: Thu Jan 05 13:30:33 2017
#      by: PyQt5 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_frmPlot(object):
    def setupUi(self, frmPlot):
        frmPlot.setObjectName(_fromUtf8("frmPlot"))
        frmPlot.resize(633, 412)
        self.centralwidget = QWidget(frmPlot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnHelp = QPushButton(self.centralwidget)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.gridLayout.addWidget(self.btnHelp, 1, 2, 1, 1)
        spacerItem = QSpacerItem(450, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnClose = QPushButton(self.centralwidget)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 1, 1, 1)
        self.fraPlot = QWidget(self.centralwidget)
        self.fraPlot.setObjectName(_fromUtf8("fraPlot"))
        self.gridLayout.addWidget(self.fraPlot, 0, 0, 1, 3)
        frmPlot.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frmPlot)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 633, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        frmPlot.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frmPlot)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmPlot.setStatusBar(self.statusbar)
        self.actionCopy = QAction(frmPlot)
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionSave = QAction(frmPlot)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionPrint = QAction(frmPlot)
        self.actionPrint.setObjectName(_fromUtf8("actionPrint"))
        self.actionOpen = QAction(frmPlot)
        self.actionOpen.setVisible(False)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionCopy)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionPrint)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(frmPlot)
        QtCore.QMetaObject.connectSlotsByName(frmPlot)

    def retranslateUi(self, frmPlot):
        frmPlot.setWindowTitle(_translate("frmPlot", "Time Series Viewer", None))
        self.btnHelp.setText(_translate("frmPlot", "Help", None))
        self.btnClose.setText(_translate("frmPlot", "Close", None))
        self.menuFile.setTitle(_translate("frmPlot", "File", None))
        self.actionCopy.setText(_translate("frmPlot", "Copy", None))
        self.actionSave.setText(_translate("frmPlot", "Save", None))
        self.actionPrint.setText(_translate("frmPlot", "Print", None))
        self.actionOpen.setText(_translate("frmPlot", "Open", None))

