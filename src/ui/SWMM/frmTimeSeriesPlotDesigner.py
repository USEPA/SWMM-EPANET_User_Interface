# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmTimeSeriesPlotDesigner.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frmTimeSeriesPlot(object):
    def setupUi(self, frmTimeSeriesPlot):
        frmTimeSeriesPlot.setObjectName(_fromUtf8("frmTimeSeriesPlot"))
        frmTimeSeriesPlot.resize(381, 478)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTimeSeriesPlot.setFont(font)
        self.centralWidget = QtGui.QWidget(frmTimeSeriesPlot)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxTimePeriods = QtGui.QGroupBox(self.centralWidget)
        self.gbxTimePeriods.setObjectName(_fromUtf8("gbxTimePeriods"))
        self.gridLayout = QtGui.QGridLayout(self.gbxTimePeriods)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblStart = QtGui.QLabel(self.gbxTimePeriods)
        self.lblStart.setObjectName(_fromUtf8("lblStart"))
        self.gridLayout.addWidget(self.lblStart, 0, 0, 1, 1)
        self.cboStart = QtGui.QComboBox(self.gbxTimePeriods)
        self.cboStart.setObjectName(_fromUtf8("cboStart"))
        self.gridLayout.addWidget(self.cboStart, 1, 0, 1, 1)
        self.lblEnd = QtGui.QLabel(self.gbxTimePeriods)
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.gridLayout.addWidget(self.lblEnd, 0, 1, 1, 1)
        self.cboEnd = QtGui.QComboBox(self.gbxTimePeriods)
        self.cboEnd.setObjectName(_fromUtf8("cboEnd"))
        self.gridLayout.addWidget(self.cboEnd, 1, 1, 1, 1)
        self.rbnElapsed = QtGui.QRadioButton(self.gbxTimePeriods)
        self.rbnElapsed.setObjectName(_fromUtf8("rbnElapsed"))
        self.gridLayout.addWidget(self.rbnElapsed, 2, 0, 1, 1)
        self.rbnDate = QtGui.QRadioButton(self.gbxTimePeriods)
        self.rbnDate.setObjectName(_fromUtf8("rbnDate"))
        self.gridLayout.addWidget(self.rbnDate, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.gbxTimePeriods)
        self.gbxData = QtGui.QGroupBox(self.centralWidget)
        self.gbxData.setObjectName(_fromUtf8("gbxData"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbxData)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraButtons = QtGui.QFrame(self.gbxData)
        self.fraButtons.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraButtons.setFrameShadow(QtGui.QFrame.Raised)
        self.fraButtons.setObjectName(_fromUtf8("fraButtons"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.fraButtons)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnAdd = QtGui.QToolButton(self.fraButtons)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout_2.addWidget(self.btnAdd)
        self.btnRemove = QtGui.QToolButton(self.fraButtons)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.horizontalLayout_2.addWidget(self.btnRemove)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.fraButtons)
        self.lstData = QtGui.QListWidget(self.gbxData)
        self.lstData.setObjectName(_fromUtf8("lstData"))
        self.verticalLayout_2.addWidget(self.lstData)
        self.verticalLayout.addWidget(self.gbxData)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(338, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
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
        self.cmdOK.setText(_translate("frmTimeSeriesPlot", "OK", None))
        self.cmdCancel.setText(_translate("frmTimeSeriesPlot", "Cancel", None))

