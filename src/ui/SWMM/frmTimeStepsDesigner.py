# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmTimeSteps.ui'
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

class Ui_frmTimeSteps(object):
    def setupUi(self, frmTimeSteps):
        frmTimeSteps.setObjectName(_fromUtf8("frmTimeSteps"))
        frmTimeSteps.resize(374, 430)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTimeSteps.setFont(font)
        self.centralWidget = QtGui.QWidget(frmTimeSteps)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(100, 390, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(200, 390, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.gbxSteady = QtGui.QGroupBox(self.centralWidget)
        self.gbxSteady.setGeometry(QtCore.QRect(20, 240, 331, 131))
        self.gbxSteady.setObjectName(_fromUtf8("gbxSteady"))
        self.cbxSkip = QtGui.QCheckBox(self.gbxSteady)
        self.cbxSkip.setGeometry(QtCore.QRect(20, 30, 181, 17))
        self.cbxSkip.setObjectName(_fromUtf8("cbxSkip"))
        self.lblSystem = QtGui.QLabel(self.gbxSteady)
        self.lblSystem.setGeometry(QtCore.QRect(20, 60, 171, 16))
        self.lblSystem.setObjectName(_fromUtf8("lblSystem"))
        self.lblLateral = QtGui.QLabel(self.gbxSteady)
        self.lblLateral.setGeometry(QtCore.QRect(20, 90, 171, 16))
        self.lblLateral.setObjectName(_fromUtf8("lblLateral"))
        self.sbxSystem = QtGui.QSpinBox(self.gbxSteady)
        self.sbxSystem.setGeometry(QtCore.QRect(230, 60, 81, 22))
        self.sbxSystem.setObjectName(_fromUtf8("sbxSystem"))
        self.sbxLateral = QtGui.QSpinBox(self.gbxSteady)
        self.sbxLateral.setGeometry(QtCore.QRect(230, 90, 81, 22))
        self.sbxLateral.setObjectName(_fromUtf8("sbxLateral"))
        self.lblReporting = QtGui.QLabel(self.centralWidget)
        self.lblReporting.setGeometry(QtCore.QRect(40, 50, 101, 16))
        self.lblReporting.setObjectName(_fromUtf8("lblReporting"))
        self.lblRunoff1 = QtGui.QLabel(self.centralWidget)
        self.lblRunoff1.setGeometry(QtCore.QRect(40, 80, 101, 16))
        self.lblRunoff1.setObjectName(_fromUtf8("lblRunoff1"))
        self.lblDry = QtGui.QLabel(self.centralWidget)
        self.lblDry.setGeometry(QtCore.QRect(40, 100, 101, 16))
        self.lblDry.setObjectName(_fromUtf8("lblDry"))
        self.lblWet = QtGui.QLabel(self.centralWidget)
        self.lblWet.setGeometry(QtCore.QRect(40, 150, 101, 16))
        self.lblWet.setObjectName(_fromUtf8("lblWet"))
        self.lblRunoff2 = QtGui.QLabel(self.centralWidget)
        self.lblRunoff2.setGeometry(QtCore.QRect(40, 130, 101, 16))
        self.lblRunoff2.setObjectName(_fromUtf8("lblRunoff2"))
        self.lblRouting = QtGui.QLabel(self.centralWidget)
        self.lblRouting.setGeometry(QtCore.QRect(40, 180, 101, 16))
        self.lblRouting.setObjectName(_fromUtf8("lblRouting"))
        self.txtRouting = QtGui.QLineEdit(self.centralWidget)
        self.txtRouting.setGeometry(QtCore.QRect(150, 180, 71, 20))
        self.txtRouting.setObjectName(_fromUtf8("txtRouting"))
        self.lblSeconds = QtGui.QLabel(self.centralWidget)
        self.lblSeconds.setGeometry(QtCore.QRect(250, 180, 101, 16))
        self.lblSeconds.setObjectName(_fromUtf8("lblSeconds"))
        self.sbxReportDay = QtGui.QSpinBox(self.centralWidget)
        self.sbxReportDay.setGeometry(QtCore.QRect(150, 50, 51, 22))
        self.sbxReportDay.setObjectName(_fromUtf8("sbxReportDay"))
        self.sbxDry = QtGui.QSpinBox(self.centralWidget)
        self.sbxDry.setGeometry(QtCore.QRect(150, 90, 51, 22))
        self.sbxDry.setObjectName(_fromUtf8("sbxDry"))
        self.sbxWet = QtGui.QSpinBox(self.centralWidget)
        self.sbxWet.setGeometry(QtCore.QRect(150, 130, 51, 22))
        self.sbxWet.setObjectName(_fromUtf8("sbxWet"))
        self.lblDays = QtGui.QLabel(self.centralWidget)
        self.lblDays.setGeometry(QtCore.QRect(150, 30, 101, 16))
        self.lblDays.setObjectName(_fromUtf8("lblDays"))
        self.lblHr = QtGui.QLabel(self.centralWidget)
        self.lblHr.setGeometry(QtCore.QRect(240, 30, 101, 16))
        self.lblHr.setObjectName(_fromUtf8("lblHr"))
        self.tmeReport = QtGui.QTimeEdit(self.centralWidget)
        self.tmeReport.setGeometry(QtCore.QRect(240, 50, 81, 22))
        self.tmeReport.setProperty("showGroupSeparator", False)
        self.tmeReport.setObjectName(_fromUtf8("tmeReport"))
        self.tmeDry = QtGui.QTimeEdit(self.centralWidget)
        self.tmeDry.setGeometry(QtCore.QRect(240, 90, 81, 22))
        self.tmeDry.setProperty("showGroupSeparator", False)
        self.tmeDry.setObjectName(_fromUtf8("tmeDry"))
        self.tmeWet = QtGui.QTimeEdit(self.centralWidget)
        self.tmeWet.setGeometry(QtCore.QRect(240, 130, 81, 22))
        self.tmeWet.setProperty("showGroupSeparator", False)
        self.tmeWet.setObjectName(_fromUtf8("tmeWet"))
        frmTimeSteps.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTimeSteps)
        QtCore.QMetaObject.connectSlotsByName(frmTimeSteps)

    def retranslateUi(self, frmTimeSteps):
        frmTimeSteps.setWindowTitle(_translate("frmTimeSteps", "SWMM Time Steps Options", None))
        self.cmdOK.setText(_translate("frmTimeSteps", "OK", None))
        self.cmdCancel.setText(_translate("frmTimeSteps", "Cancel", None))
        self.gbxSteady.setTitle(_translate("frmTimeSteps", "Steady Flow Periods", None))
        self.cbxSkip.setText(_translate("frmTimeSteps", "Skip Steady Flow Periods", None))
        self.lblSystem.setText(_translate("frmTimeSteps", "System Flow Tolerance (%)", None))
        self.lblLateral.setText(_translate("frmTimeSteps", "Lateral Flow Tolerance (%)", None))
        self.lblReporting.setText(_translate("frmTimeSteps", "Reporting", None))
        self.lblRunoff1.setText(_translate("frmTimeSteps", "<html><head/><body><p>Runoff:</p></body></html>", None))
        self.lblDry.setText(_translate("frmTimeSteps", "Dry Weather", None))
        self.lblWet.setText(_translate("frmTimeSteps", "Wet Weather", None))
        self.lblRunoff2.setText(_translate("frmTimeSteps", "Runoff:", None))
        self.lblRouting.setText(_translate("frmTimeSteps", "Routing", None))
        self.lblSeconds.setText(_translate("frmTimeSteps", "Seconds", None))
        self.lblDays.setText(_translate("frmTimeSteps", "Days", None))
        self.lblHr.setText(_translate("frmTimeSteps", "Hr:Min:Sec", None))
        self.tmeReport.setDisplayFormat(_translate("frmTimeSteps", "h:mm:ss", None))
        self.tmeDry.setDisplayFormat(_translate("frmTimeSteps", "h:mm:ss", None))
        self.tmeWet.setDisplayFormat(_translate("frmTimeSteps", "h:mm:ss", None))

