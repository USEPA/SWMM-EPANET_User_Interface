# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmCalibrationReportOptionsDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
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

class Ui_frmCalibrationReportOptions(object):
    def setupUi(self, frmCalibrationReportOptions):
        frmCalibrationReportOptions.setObjectName(_fromUtf8("frmCalibrationReportOptions"))
        frmCalibrationReportOptions.resize(405, 325)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCalibrationReportOptions.setFont(font)
        self.centralWidget = QWidget(frmCalibrationReportOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QVBoxLayout(self.centralWidget)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QFrame(self.centralWidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gbxCalibrate = QGroupBox(self.frame)
        self.gbxCalibrate.setObjectName(_fromUtf8("gbxCalibrate"))
        self.gridLayout = QGridLayout(self.gbxCalibrate)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBox = QComboBox(self.gbxCalibrate)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.gbxCalibrate)
        self.gbxMeasured = QGroupBox(self.frame)
        self.gbxMeasured.setObjectName(_fromUtf8("gbxMeasured"))
        self.horizontalLayout_3 = QHBoxLayout(self.gbxMeasured)
        # self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.listWidget = QListWidget(self.gbxMeasured)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayout_3.addWidget(self.listWidget)
        self.horizontalLayout_2.addWidget(self.gbxMeasured)
        self.verticalLayout_2.addWidget(self.frame)
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
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmCalibrationReportOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCalibrationReportOptions)
        QtCore.QMetaObject.connectSlotsByName(frmCalibrationReportOptions)

    def retranslateUi(self, frmCalibrationReportOptions):
        frmCalibrationReportOptions.setWindowTitle(_translate("frmCalibrationReportOptions", "EPANET Calibration Report Options", None))
        self.gbxCalibrate.setTitle(_translate("frmCalibrationReportOptions", "Calibrate Against", None))
        self.gbxMeasured.setTitle(_translate("frmCalibrationReportOptions", "Measured at Nodes:", None))
        self.cmdOK.setText(_translate("frmCalibrationReportOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmCalibrationReportOptions", "Cancel", None))

