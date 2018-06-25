# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmStatisticsReportSelectionDesigner.ui'
#
# Created: Fri Jul 29 15:37:04 2016
#      by: PyQt5 UI code generator 4.10.2
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

class Ui_frmStatisticsReportSelection(object):
    def setupUi(self, frmStatisticsReportSelection):
        frmStatisticsReportSelection.setObjectName(_fromUtf8("frmStatisticsReportSelection"))
        frmStatisticsReportSelection.resize(329, 395)
        font = QFont()
        font.setPointSize(10)
        frmStatisticsReportSelection.setFont(font)
        self.centralWidget = QWidget(frmStatisticsReportSelection)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.gridLayout_2 = QGridLayout(self.fraTop)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cboCategory = QComboBox(self.fraTop)
        self.cboCategory.setObjectName(_fromUtf8("cboCategory"))
        self.gridLayout_2.addWidget(self.cboCategory, 0, 2, 1, 1)
        self.lblCategory = QLabel(self.fraTop)
        self.lblCategory.setObjectName(_fromUtf8("lblCategory"))
        self.gridLayout_2.addWidget(self.lblCategory, 0, 1, 1, 1)
        self.lblName = QLabel(self.fraTop)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_2.addWidget(self.lblName, 1, 1, 1, 1)
        self.cboVariable = QComboBox(self.fraTop)
        self.cboVariable.setObjectName(_fromUtf8("cboVariable"))
        self.gridLayout_2.addWidget(self.cboVariable, 2, 2, 1, 1)
        self.lstName = QListWidget(self.fraTop)
        self.lstName.setObjectName(_fromUtf8("lstName"))
        self.gridLayout_2.addWidget(self.lstName, 1, 2, 1, 1)
        self.lblVariable = QLabel(self.fraTop)
        self.lblVariable.setObjectName(_fromUtf8("lblVariable"))
        self.gridLayout_2.addWidget(self.lblVariable, 2, 1, 1, 1)
        self.lblEvent = QLabel(self.fraTop)
        self.lblEvent.setObjectName(_fromUtf8("lblEvent"))
        self.gridLayout_2.addWidget(self.lblEvent, 3, 1, 1, 1)
        self.cboEvent = QComboBox(self.fraTop)
        self.cboEvent.setObjectName(_fromUtf8("cboEvent"))
        self.gridLayout_2.addWidget(self.cboEvent, 3, 2, 1, 1)
        self.lblStatistic = QLabel(self.fraTop)
        self.lblStatistic.setObjectName(_fromUtf8("lblStatistic"))
        self.gridLayout_2.addWidget(self.lblStatistic, 4, 1, 1, 1)
        self.cboStatistic = QComboBox(self.fraTop)
        self.cboStatistic.setObjectName(_fromUtf8("cboStatistic"))
        self.gridLayout_2.addWidget(self.cboStatistic, 4, 2, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
        self.gbxThresholds = QGroupBox(self.centralWidget)
        self.gbxThresholds.setObjectName(_fromUtf8("gbxThresholds"))
        self.gridLayout = QGridLayout(self.gbxThresholds)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPrecip = QLabel(self.gbxThresholds)
        self.lblPrecip.setObjectName(_fromUtf8("lblPrecip"))
        self.gridLayout.addWidget(self.lblPrecip, 0, 0, 1, 1)
        self.lblVolume = QLabel(self.gbxThresholds)
        self.lblVolume.setObjectName(_fromUtf8("lblVolume"))
        self.gridLayout.addWidget(self.lblVolume, 3, 0, 1, 1)
        self.txtMinEventValue = QLineEdit(self.gbxThresholds)
        self.txtMinEventValue.setObjectName(_fromUtf8("txtMinEventValue"))
        self.gridLayout.addWidget(self.txtMinEventValue, 0, 1, 1, 1)
        self.txtMinEventVolume = QLineEdit(self.gbxThresholds)
        self.txtMinEventVolume.setObjectName(_fromUtf8("txtMinEventVolume"))
        self.gridLayout.addWidget(self.txtMinEventVolume, 3, 1, 1, 1)
        self.txtMinEventDelta = QLineEdit(self.gbxThresholds)
        self.txtMinEventDelta.setObjectName(_fromUtf8("txtMinEventDelta"))
        self.gridLayout.addWidget(self.txtMinEventDelta, 4, 1, 1, 1)
        self.lblSeparation = QLabel(self.gbxThresholds)
        self.lblSeparation.setObjectName(_fromUtf8("lblSeparation"))
        self.gridLayout.addWidget(self.lblSeparation, 4, 0, 1, 1)
        self.verticalLayout.addWidget(self.gbxThresholds)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fraMid = QFrame(self.fraOKCancel)
        self.fraMid.setFrameShape(QFrame.StyledPanel)
        self.fraMid.setFrameShadow(QFrame.Raised)
        self.fraMid.setObjectName(_fromUtf8("fraMid"))
        self.horizontalLayout_3 = QHBoxLayout(self.fraMid)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout.addWidget(self.fraMid)
        spacerItem = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmStatisticsReportSelection.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmStatisticsReportSelection)
        QtCore.QMetaObject.connectSlotsByName(frmStatisticsReportSelection)

    def retranslateUi(self, frmStatisticsReportSelection):
        frmStatisticsReportSelection.setWindowTitle(_translate("frmStatisticsReportSelection", "SWMM Statistics Report Selection", None))
        self.lblCategory.setText(_translate("frmStatisticsReportSelection", "Object Category", None))
        self.lblName.setText(_translate("frmStatisticsReportSelection", "Object Name", None))
        self.lblVariable.setText(_translate("frmStatisticsReportSelection", "Variable Analyzed", None))
        self.lblEvent.setText(_translate("frmStatisticsReportSelection", "Event Time Period", None))
        self.lblStatistic.setText(_translate("frmStatisticsReportSelection", "Statistic", None))
        self.gbxThresholds.setTitle(_translate("frmStatisticsReportSelection", "Event Thresholds", None))
        self.lblPrecip.setText(_translate("frmStatisticsReportSelection", "Precipitation", None))
        self.lblVolume.setText(_translate("frmStatisticsReportSelection", "Event Volume", None))
        self.lblSeparation.setText(_translate("frmStatisticsReportSelection", "Separation Time", None))
        self.cmdOK.setText(_translate("frmStatisticsReportSelection", "OK", None))
        self.cmdCancel.setText(_translate("frmStatisticsReportSelection", "Cancel", None))

