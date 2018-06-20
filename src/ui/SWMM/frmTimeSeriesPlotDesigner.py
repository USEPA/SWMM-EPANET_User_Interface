# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmTimeSeriesPlotDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
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

class Ui_frmTimeSeriesPlot(object):
    def setupUi(self, frmTimeSeriesPlot):
        frmTimeSeriesPlot.setObjectName(_fromUtf8("frmTimeSeriesPlot"))
        frmTimeSeriesPlot.resize(381, 478)
        font = QFont()
        font.setPointSize(10)
        frmTimeSeriesPlot.setFont(font)
        self.centralWidget = QWidget(frmTimeSeriesPlot)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxTimePeriods = QGroupBox(self.centralWidget)
        self.gbxTimePeriods.setObjectName(_fromUtf8("gbxTimePeriods"))
        self.gridLayout = QGridLayout(self.gbxTimePeriods)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblStart = QLabel(self.gbxTimePeriods)
        self.lblStart.setObjectName(_fromUtf8("lblStart"))
        self.gridLayout.addWidget(self.lblStart, 0, 0, 1, 1)
        self.cboStart = QComboBox(self.gbxTimePeriods)
        self.cboStart.setObjectName(_fromUtf8("cboStart"))
        self.gridLayout.addWidget(self.cboStart, 1, 0, 1, 1)
        self.lblEnd = QLabel(self.gbxTimePeriods)
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.gridLayout.addWidget(self.lblEnd, 0, 1, 1, 1)
        self.cboEnd = QComboBox(self.gbxTimePeriods)
        self.cboEnd.setObjectName(_fromUtf8("cboEnd"))
        self.gridLayout.addWidget(self.cboEnd, 1, 1, 1, 1)
        self.rbnElapsed = QRadioButton(self.gbxTimePeriods)
        self.rbnElapsed.setObjectName(_fromUtf8("rbnElapsed"))
        self.gridLayout.addWidget(self.rbnElapsed, 2, 0, 1, 1)
        self.rbnDate = QRadioButton(self.gbxTimePeriods)
        self.rbnDate.setObjectName(_fromUtf8("rbnDate"))
        self.gridLayout.addWidget(self.rbnDate, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.gbxTimePeriods)
        self.gbxData = QGroupBox(self.centralWidget)
        self.gbxData.setObjectName(_fromUtf8("gbxData"))
        self.verticalLayout_2 = QVBoxLayout(self.gbxData)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraButtons = QFrame(self.gbxData)
        self.fraButtons.setFrameShape(QFrame.StyledPanel)
        self.fraButtons.setFrameShadow(QFrame.Raised)
        self.fraButtons.setObjectName(_fromUtf8("fraButtons"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraButtons)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnAdd = QToolButton(self.fraButtons)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout_2.addWidget(self.btnAdd)
        self.btnRemove = QToolButton(self.fraButtons)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.horizontalLayout_2.addWidget(self.btnRemove)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnLoad = QToolButton(self.fraButtons)
        self.btnLoad.setObjectName(_fromUtf8("btnLoad"))
        self.horizontalLayout_2.addWidget(self.btnLoad)
        self.btnSave = QToolButton(self.fraButtons)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.btnScript = QToolButton(self.fraButtons)
        self.btnScript.setObjectName(_fromUtf8("btnScript"))
        self.horizontalLayout_2.addWidget(self.btnScript)
        self.verticalLayout_2.addWidget(self.fraButtons)
        self.lstData = QListWidget(self.gbxData)
        self.lstData.setObjectName(_fromUtf8("lstData"))
        self.verticalLayout_2.addWidget(self.lstData)
        self.verticalLayout.addWidget(self.gbxData)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmTimeSeriesPlot.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTimeSeriesPlot)
        QtCore.QMetaObject.connectSlotsByName(frmTimeSeriesPlot)

    def retranslateUi(self, frmTimeSeriesPlot):
        frmTimeSeriesPlot.setWindowTitle(_translate("frmTimeSeriesPlot", "SWMM Time Series Plot Selection", None))
        self.gbxTimePeriods.setTitle(_translate("frmTimeSeriesPlot", "Time Periods", None))
        self.lblStart.setText(_translate("frmTimeSeriesPlot", "Start Date", None))
        self.lblEnd.setText(_translate("frmTimeSeriesPlot", "End Date", None))
        self.rbnElapsed.setText(_translate("frmTimeSeriesPlot", "Elapsed Time", None))
        self.rbnDate.setText(_translate("frmTimeSeriesPlot", "Date/Time", None))
        self.gbxData.setTitle(_translate("frmTimeSeriesPlot", "Data Series", None))
        self.btnAdd.setText(_translate("frmTimeSeriesPlot", "+", None))
        self.btnRemove.setText(_translate("frmTimeSeriesPlot", "-", None))
        self.btnLoad.setText(_translate("frmTimeSeriesPlot", "Load", None))
        self.btnSave.setText(_translate("frmTimeSeriesPlot", "Save", None))
        self.btnScript.setText(_translate("frmTimeSeriesPlot", "To Script", None))
        self.cmdOK.setText(_translate("frmTimeSeriesPlot", "OK", None))
        self.cmdCancel.setText(_translate("frmTimeSeriesPlot", "Cancel", None))

