# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmCalibrationReportDesigner.ui'
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

class Ui_frmCalibrationReport(object):
    def setupUi(self, frmCalibrationReport):
        frmCalibrationReport.setObjectName(_fromUtf8("frmCalibrationReport"))
        frmCalibrationReport.resize(685, 396)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCalibrationReport.setFont(font)
        self.centralWidget = QtGui.QWidget(frmCalibrationReport)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_8.setMargin(11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.fraTop = QtGui.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.fraTop)
        self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(self.fraTop)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabStatistics = QtGui.QWidget()
        self.tabStatistics.setObjectName(_fromUtf8("tabStatistics"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabStatistics)
        self.verticalLayout_4.setMargin(11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.txtStatistics = QtGui.QTextEdit(self.tabStatistics)
        self.txtStatistics.setObjectName(_fromUtf8("txtStatistics"))
        self.verticalLayout_4.addWidget(self.txtStatistics)
        self.tabWidget.addTab(self.tabStatistics, _fromUtf8(""))
        self.tabCorrelation = QtGui.QWidget()
        self.tabCorrelation.setObjectName(_fromUtf8("tabCorrelation"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tabCorrelation)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.widgetPlot = QtGui.QWidget(self.tabCorrelation)
        self.widgetPlot.setObjectName(_fromUtf8("widgetPlot"))
        self.horizontalLayout_2.addWidget(self.widgetPlot)
        self.tabWidget.addTab(self.tabCorrelation, _fromUtf8(""))
        self.tabMean = QtGui.QWidget()
        self.tabMean.setObjectName(_fromUtf8("tabMean"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tabMean)
        self.horizontalLayout_4.setMargin(11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.widgetMean = QtGui.QWidget(self.tabMean)
        self.widgetMean.setObjectName(_fromUtf8("widgetMean"))
        self.horizontalLayout_4.addWidget(self.widgetMean)
        self.tabWidget.addTab(self.tabMean, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout_8.addWidget(self.fraTop)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(338, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_8.addWidget(self.fraOKCancel)
        frmCalibrationReport.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCalibrationReport)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmCalibrationReport)

    def retranslateUi(self, frmCalibrationReport):
        frmCalibrationReport.setWindowTitle(_translate("frmCalibrationReport", "EPANET Calibration Report", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStatistics), _translate("frmCalibrationReport", "Statistics", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCorrelation), _translate("frmCalibrationReport", "Correlation Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMean), _translate("frmCalibrationReport", "Mean Comparisons", None))
        self.cmdCancel.setText(_translate("frmCalibrationReport", "Close", None))

