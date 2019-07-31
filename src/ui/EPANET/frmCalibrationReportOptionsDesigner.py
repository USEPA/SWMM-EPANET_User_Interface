# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPANET\frmCalibrationReportOptionsDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmCalibrationReportOptions(object):
    def setupUi(self, frmCalibrationReportOptions):
        frmCalibrationReportOptions.setObjectName("frmCalibrationReportOptions")
        frmCalibrationReportOptions.resize(411, 333)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCalibrationReportOptions.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmCalibrationReportOptions)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gbxCalibrate = QtWidgets.QGroupBox(self.frame)
        self.gbxCalibrate.setObjectName("gbxCalibrate")
        self.gridLayout = QtWidgets.QGridLayout(self.gbxCalibrate)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox = QtWidgets.QComboBox(self.gbxCalibrate)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.gbxCalibrate)
        self.gbxMeasured = QtWidgets.QGroupBox(self.frame)
        self.gbxMeasured.setObjectName("gbxMeasured")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.gbxMeasured)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listWidget = QtWidgets.QListWidget(self.gbxMeasured)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_3.addWidget(self.listWidget)
        self.horizontalLayout_2.addWidget(self.gbxMeasured)
        self.verticalLayout_2.addWidget(self.frame)
        self.fraOKCancel = QtWidgets.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraOKCancel.setObjectName("fraOKCancel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdOK = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmCalibrationReportOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCalibrationReportOptions)
        QtCore.QMetaObject.connectSlotsByName(frmCalibrationReportOptions)

    def retranslateUi(self, frmCalibrationReportOptions):
        _translate = QtCore.QCoreApplication.translate
        frmCalibrationReportOptions.setWindowTitle(_translate("frmCalibrationReportOptions", "EPANET Calibration Report Options"))
        self.gbxCalibrate.setTitle(_translate("frmCalibrationReportOptions", "Calibrate Against"))
        self.gbxMeasured.setTitle(_translate("frmCalibrationReportOptions", "Measured at Nodes:"))
        self.cmdOK.setText(_translate("frmCalibrationReportOptions", "OK"))
        self.cmdCancel.setText(_translate("frmCalibrationReportOptions", "Cancel"))

