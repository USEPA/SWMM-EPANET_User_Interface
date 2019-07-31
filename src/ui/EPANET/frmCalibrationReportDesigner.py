# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\EPANET\frmCalibrationReportDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmCalibrationReport(object):
    def setupUi(self, frmCalibrationReport):
        frmCalibrationReport.setObjectName("frmCalibrationReport")
        frmCalibrationReport.resize(685, 396)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCalibrationReport.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmCalibrationReport)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.fraTop = QtWidgets.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraTop.setObjectName("fraTop")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.fraTop)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.fraTop)
        self.tabWidget.setObjectName("tabWidget")
        self.tabStatistics = QtWidgets.QWidget()
        self.tabStatistics.setObjectName("tabStatistics")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabStatistics)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.txtStatistics = QtWidgets.QTextEdit(self.tabStatistics)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.txtStatistics.setFont(font)
        self.txtStatistics.setObjectName("txtStatistics")
        self.verticalLayout_4.addWidget(self.txtStatistics)
        self.tabWidget.addTab(self.tabStatistics, "")
        self.tabCorrelation = QtWidgets.QWidget()
        self.tabCorrelation.setObjectName("tabCorrelation")
        self.tabWidget.addTab(self.tabCorrelation, "")
        self.tabMean = QtWidgets.QWidget()
        self.tabMean.setObjectName("tabMean")
        self.tabWidget.addTab(self.tabMean, "")
        self.horizontalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout_8.addWidget(self.fraTop)
        self.fraOKCancel = QtWidgets.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraOKCancel.setObjectName("fraOKCancel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdCancel = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_8.addWidget(self.fraOKCancel)
        frmCalibrationReport.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCalibrationReport)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmCalibrationReport)

    def retranslateUi(self, frmCalibrationReport):
        _translate = QtCore.QCoreApplication.translate
        frmCalibrationReport.setWindowTitle(_translate("frmCalibrationReport", "EPANET Calibration Report"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStatistics), _translate("frmCalibrationReport", "Statistics"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCorrelation), _translate("frmCalibrationReport", "Correlation Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMean), _translate("frmCalibrationReport", "Mean Comparisons"))
        self.cmdCancel.setText(_translate("frmCalibrationReport", "Close"))

