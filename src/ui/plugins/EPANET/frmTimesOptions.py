# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\SWMM-EPANET_User_Interface\src\ui\plugins\EPANET\frmTimesOptions.ui'
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

class Ui_frmHydraulicsOptions(object):
    def setupUi(self, frmHydraulicsOptions):
        frmHydraulicsOptions.setObjectName(_fromUtf8("frmHydraulicsOptions"))
        frmHydraulicsOptions.resize(304, 390)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmHydraulicsOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmHydraulicsOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.lblTotalDuration = QtGui.QLabel(self.centralWidget)
        self.lblTotalDuration.setGeometry(QtCore.QRect(30, 20, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTotalDuration.setFont(font)
        self.lblTotalDuration.setObjectName(_fromUtf8("lblTotalDuration"))
        self.lblHydraulic = QtGui.QLabel(self.centralWidget)
        self.lblHydraulic.setGeometry(QtCore.QRect(30, 50, 121, 16))
        self.lblHydraulic.setObjectName(_fromUtf8("lblHydraulic"))
        self.lblQuality = QtGui.QLabel(self.centralWidget)
        self.lblQuality.setGeometry(QtCore.QRect(30, 80, 111, 16))
        self.lblQuality.setObjectName(_fromUtf8("lblQuality"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(60, 330, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(160, 330, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.txtQuality = QtGui.QLineEdit(self.centralWidget)
        self.txtQuality.setGeometry(QtCore.QRect(160, 80, 113, 20))
        self.txtQuality.setObjectName(_fromUtf8("txtQuality"))
        self.lblRule = QtGui.QLabel(self.centralWidget)
        self.lblRule.setGeometry(QtCore.QRect(30, 110, 111, 16))
        self.lblRule.setObjectName(_fromUtf8("lblRule"))
        self.txtRule = QtGui.QLineEdit(self.centralWidget)
        self.txtRule.setGeometry(QtCore.QRect(160, 110, 113, 20))
        self.txtRule.setObjectName(_fromUtf8("txtRule"))
        self.lblPattern = QtGui.QLabel(self.centralWidget)
        self.lblPattern.setGeometry(QtCore.QRect(30, 140, 111, 16))
        self.lblPattern.setObjectName(_fromUtf8("lblPattern"))
        self.txtPattern = QtGui.QLineEdit(self.centralWidget)
        self.txtPattern.setGeometry(QtCore.QRect(160, 140, 113, 20))
        self.txtPattern.setObjectName(_fromUtf8("txtPattern"))
        self.lblPatternTime = QtGui.QLabel(self.centralWidget)
        self.lblPatternTime.setGeometry(QtCore.QRect(30, 170, 121, 16))
        self.lblPatternTime.setObjectName(_fromUtf8("lblPatternTime"))
        self.lblReporting = QtGui.QLabel(self.centralWidget)
        self.lblReporting.setGeometry(QtCore.QRect(30, 200, 121, 16))
        self.lblReporting.setObjectName(_fromUtf8("lblReporting"))
        self.cboStatistic = QtGui.QComboBox(self.centralWidget)
        self.cboStatistic.setGeometry(QtCore.QRect(160, 290, 111, 22))
        self.cboStatistic.setObjectName(_fromUtf8("cboStatistic"))
        self.txtPatternTime = QtGui.QLineEdit(self.centralWidget)
        self.txtPatternTime.setGeometry(QtCore.QRect(160, 170, 113, 20))
        self.txtPatternTime.setObjectName(_fromUtf8("txtPatternTime"))
        self.lblReportingTime = QtGui.QLabel(self.centralWidget)
        self.lblReportingTime.setGeometry(QtCore.QRect(30, 230, 111, 16))
        self.lblReportingTime.setObjectName(_fromUtf8("lblReportingTime"))
        self.lblClockStart = QtGui.QLabel(self.centralWidget)
        self.lblClockStart.setGeometry(QtCore.QRect(30, 260, 111, 16))
        self.lblClockStart.setObjectName(_fromUtf8("lblClockStart"))
        self.lblStatistic = QtGui.QLabel(self.centralWidget)
        self.lblStatistic.setGeometry(QtCore.QRect(30, 290, 111, 16))
        self.lblStatistic.setObjectName(_fromUtf8("lblStatistic"))
        self.txtReportingTime = QtGui.QLineEdit(self.centralWidget)
        self.txtReportingTime.setGeometry(QtCore.QRect(160, 230, 113, 20))
        self.txtReportingTime.setObjectName(_fromUtf8("txtReportingTime"))
        self.txtClockStart = QtGui.QLineEdit(self.centralWidget)
        self.txtClockStart.setGeometry(QtCore.QRect(160, 260, 113, 20))
        self.txtClockStart.setObjectName(_fromUtf8("txtClockStart"))
        self.txtReporting = QtGui.QLineEdit(self.centralWidget)
        self.txtReporting.setGeometry(QtCore.QRect(160, 200, 113, 20))
        self.txtReporting.setObjectName(_fromUtf8("txtReporting"))
        self.txtTotalDuration = QtGui.QLineEdit(self.centralWidget)
        self.txtTotalDuration.setGeometry(QtCore.QRect(160, 20, 113, 20))
        self.txtTotalDuration.setObjectName(_fromUtf8("txtTotalDuration"))
        self.txtHydraulic = QtGui.QLineEdit(self.centralWidget)
        self.txtHydraulic.setGeometry(QtCore.QRect(160, 50, 113, 20))
        self.txtHydraulic.setObjectName(_fromUtf8("txtHydraulic"))
        frmHydraulicsOptions.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtGui.QToolBar(frmHydraulicsOptions)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        frmHydraulicsOptions.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(frmHydraulicsOptions)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        frmHydraulicsOptions.setStatusBar(self.statusBar)

        self.retranslateUi(frmHydraulicsOptions)
        QtCore.QMetaObject.connectSlotsByName(frmHydraulicsOptions)

    def retranslateUi(self, frmHydraulicsOptions):
        frmHydraulicsOptions.setWindowTitle(_translate("frmHydraulicsOptions", "EPANET Hydraulics Options", None))
        self.lblTotalDuration.setText(_translate("frmHydraulicsOptions", "Total Duration", None))
        self.lblHydraulic.setText(_translate("frmHydraulicsOptions", "<html><head/><body><p>Hydraulic Time Step</p></body></html>", None))
        self.lblQuality.setText(_translate("frmHydraulicsOptions", "Quality Time Step", None))
        self.cmdOK.setText(_translate("frmHydraulicsOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmHydraulicsOptions", "Cancel", None))
        self.lblRule.setText(_translate("frmHydraulicsOptions", "Rule Time Step", None))
        self.lblPattern.setText(_translate("frmHydraulicsOptions", "Pattern Time Step", None))
        self.lblPatternTime.setText(_translate("frmHydraulicsOptions", "Pattern Start Time", None))
        self.lblReporting.setText(_translate("frmHydraulicsOptions", "Reporting Time Step", None))
        self.lblReportingTime.setText(_translate("frmHydraulicsOptions", "Report Start Time", None))
        self.lblClockStart.setText(_translate("frmHydraulicsOptions", "Clock Start Time", None))
        self.lblStatistic.setText(_translate("frmHydraulicsOptions", "Statistic", None))

