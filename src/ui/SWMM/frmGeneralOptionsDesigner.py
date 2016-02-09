# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmGeneralOptions.ui'
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

class Ui_frmGeneralOptions(object):
    def setupUi(self, frmGeneralOptions):
        frmGeneralOptions.setObjectName(_fromUtf8("frmGeneralOptions"))
        frmGeneralOptions.resize(443, 430)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmGeneralOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmGeneralOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(140, 390, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(230, 390, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.gbxProcess = QtGui.QGroupBox(self.centralWidget)
        self.gbxProcess.setGeometry(QtCore.QRect(20, 20, 191, 221))
        self.gbxProcess.setObjectName(_fromUtf8("gbxProcess"))
        self.cbxRainfallRunoff = QtGui.QCheckBox(self.gbxProcess)
        self.cbxRainfallRunoff.setGeometry(QtCore.QRect(20, 30, 151, 17))
        self.cbxRainfallRunoff.setObjectName(_fromUtf8("cbxRainfallRunoff"))
        self.cbxRainfallII = QtGui.QCheckBox(self.gbxProcess)
        self.cbxRainfallII.setGeometry(QtCore.QRect(20, 60, 171, 17))
        self.cbxRainfallII.setObjectName(_fromUtf8("cbxRainfallII"))
        self.cbxSnowmelt = QtGui.QCheckBox(self.gbxProcess)
        self.cbxSnowmelt.setGeometry(QtCore.QRect(20, 90, 91, 17))
        self.cbxSnowmelt.setObjectName(_fromUtf8("cbxSnowmelt"))
        self.cbxGroundwater = QtGui.QCheckBox(self.gbxProcess)
        self.cbxGroundwater.setGeometry(QtCore.QRect(20, 120, 161, 17))
        self.cbxGroundwater.setObjectName(_fromUtf8("cbxGroundwater"))
        self.cbxFlowRouting = QtGui.QCheckBox(self.gbxProcess)
        self.cbxFlowRouting.setGeometry(QtCore.QRect(20, 150, 161, 17))
        self.cbxFlowRouting.setObjectName(_fromUtf8("cbxFlowRouting"))
        self.cbxWaterQuality = QtGui.QCheckBox(self.gbxProcess)
        self.cbxWaterQuality.setGeometry(QtCore.QRect(20, 180, 161, 17))
        self.cbxWaterQuality.setObjectName(_fromUtf8("cbxWaterQuality"))
        self.gbxMiscellaneous = QtGui.QGroupBox(self.centralWidget)
        self.gbxMiscellaneous.setGeometry(QtCore.QRect(230, 210, 191, 171))
        self.gbxMiscellaneous.setObjectName(_fromUtf8("gbxMiscellaneous"))
        self.cbxAllowPonding = QtGui.QCheckBox(self.gbxMiscellaneous)
        self.cbxAllowPonding.setGeometry(QtCore.QRect(20, 30, 121, 17))
        self.cbxAllowPonding.setObjectName(_fromUtf8("cbxAllowPonding"))
        self.cbxReportControl = QtGui.QCheckBox(self.gbxMiscellaneous)
        self.cbxReportControl.setGeometry(QtCore.QRect(20, 60, 161, 17))
        self.cbxReportControl.setObjectName(_fromUtf8("cbxReportControl"))
        self.txtMinimum = QtGui.QLineEdit(self.gbxMiscellaneous)
        self.txtMinimum.setGeometry(QtCore.QRect(20, 140, 81, 20))
        self.txtMinimum.setObjectName(_fromUtf8("txtMinimum"))
        self.cbxReportInput = QtGui.QCheckBox(self.gbxMiscellaneous)
        self.cbxReportInput.setGeometry(QtCore.QRect(20, 90, 161, 17))
        self.cbxReportInput.setObjectName(_fromUtf8("cbxReportInput"))
        self.lblMinimum = QtGui.QLabel(self.gbxMiscellaneous)
        self.lblMinimum.setGeometry(QtCore.QRect(20, 120, 151, 16))
        self.lblMinimum.setObjectName(_fromUtf8("lblMinimum"))
        self.lblPercent = QtGui.QLabel(self.gbxMiscellaneous)
        self.lblPercent.setGeometry(QtCore.QRect(110, 140, 47, 13))
        self.lblPercent.setObjectName(_fromUtf8("lblPercent"))
        self.gbxRouting = QtGui.QGroupBox(self.centralWidget)
        self.gbxRouting.setGeometry(QtCore.QRect(20, 250, 191, 131))
        self.gbxRouting.setObjectName(_fromUtf8("gbxRouting"))
        self.rbnSteady = QtGui.QRadioButton(self.gbxRouting)
        self.rbnSteady.setGeometry(QtCore.QRect(20, 30, 131, 17))
        self.rbnSteady.setObjectName(_fromUtf8("rbnSteady"))
        self.rbnKinematic = QtGui.QRadioButton(self.gbxRouting)
        self.rbnKinematic.setGeometry(QtCore.QRect(20, 60, 131, 17))
        self.rbnKinematic.setObjectName(_fromUtf8("rbnKinematic"))
        self.rbnDynamic = QtGui.QRadioButton(self.gbxRouting)
        self.rbnDynamic.setGeometry(QtCore.QRect(20, 90, 131, 17))
        self.rbnDynamic.setObjectName(_fromUtf8("rbnDynamic"))
        self.gbxInfiltration = QtGui.QGroupBox(self.centralWidget)
        self.gbxInfiltration.setGeometry(QtCore.QRect(230, 20, 191, 181))
        self.gbxInfiltration.setObjectName(_fromUtf8("gbxInfiltration"))
        self.rbnHorton = QtGui.QRadioButton(self.gbxInfiltration)
        self.rbnHorton.setGeometry(QtCore.QRect(20, 30, 131, 17))
        self.rbnHorton.setObjectName(_fromUtf8("rbnHorton"))
        self.rbnModifiedHorton = QtGui.QRadioButton(self.gbxInfiltration)
        self.rbnModifiedHorton.setGeometry(QtCore.QRect(20, 60, 131, 17))
        self.rbnModifiedHorton.setObjectName(_fromUtf8("rbnModifiedHorton"))
        self.rbnGreenAmpt = QtGui.QRadioButton(self.gbxInfiltration)
        self.rbnGreenAmpt.setGeometry(QtCore.QRect(20, 90, 131, 17))
        self.rbnGreenAmpt.setObjectName(_fromUtf8("rbnGreenAmpt"))
        self.rbnModifiedGreenAmpt = QtGui.QRadioButton(self.gbxInfiltration)
        self.rbnModifiedGreenAmpt.setGeometry(QtCore.QRect(20, 120, 161, 17))
        self.rbnModifiedGreenAmpt.setObjectName(_fromUtf8("rbnModifiedGreenAmpt"))
        self.rbnCurveNumber = QtGui.QRadioButton(self.gbxInfiltration)
        self.rbnCurveNumber.setGeometry(QtCore.QRect(20, 150, 131, 17))
        self.rbnCurveNumber.setObjectName(_fromUtf8("rbnCurveNumber"))
        frmGeneralOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmGeneralOptions)
        QtCore.QMetaObject.connectSlotsByName(frmGeneralOptions)

    def retranslateUi(self, frmGeneralOptions):
        frmGeneralOptions.setWindowTitle(_translate("frmGeneralOptions", "SWMM General Options", None))
        self.cmdOK.setText(_translate("frmGeneralOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmGeneralOptions", "Cancel", None))
        self.gbxProcess.setTitle(_translate("frmGeneralOptions", "Process Models", None))
        self.cbxRainfallRunoff.setText(_translate("frmGeneralOptions", "Rainfall/Runoff", None))
        self.cbxRainfallII.setText(_translate("frmGeneralOptions", "Rainfall Dependent I/I", None))
        self.cbxSnowmelt.setText(_translate("frmGeneralOptions", "Snow Melt", None))
        self.cbxGroundwater.setText(_translate("frmGeneralOptions", "Groundwater", None))
        self.cbxFlowRouting.setText(_translate("frmGeneralOptions", "Flow Routing", None))
        self.cbxWaterQuality.setText(_translate("frmGeneralOptions", "Water Quality", None))
        self.gbxMiscellaneous.setTitle(_translate("frmGeneralOptions", "Miscellaneous", None))
        self.cbxAllowPonding.setText(_translate("frmGeneralOptions", "Allow Ponding", None))
        self.cbxReportControl.setText(_translate("frmGeneralOptions", "Report Control Actions", None))
        self.cbxReportInput.setText(_translate("frmGeneralOptions", "Report Input Summary", None))
        self.lblMinimum.setText(_translate("frmGeneralOptions", "Minimum Conduit Slope", None))
        self.lblPercent.setText(_translate("frmGeneralOptions", "(%)", None))
        self.gbxRouting.setTitle(_translate("frmGeneralOptions", "Routing Model", None))
        self.rbnSteady.setText(_translate("frmGeneralOptions", "Steady Flow", None))
        self.rbnKinematic.setText(_translate("frmGeneralOptions", "Kinematic Wave", None))
        self.rbnDynamic.setText(_translate("frmGeneralOptions", "Dynamic Wave", None))
        self.gbxInfiltration.setTitle(_translate("frmGeneralOptions", "Infiltration Model", None))
        self.rbnHorton.setText(_translate("frmGeneralOptions", "Horton", None))
        self.rbnModifiedHorton.setText(_translate("frmGeneralOptions", "Modified Horton", None))
        self.rbnGreenAmpt.setText(_translate("frmGeneralOptions", "Green-Ampt", None))
        self.rbnModifiedGreenAmpt.setText(_translate("frmGeneralOptions", "Modified Green-Ampt", None))
        self.rbnCurveNumber.setText(_translate("frmGeneralOptions", "Curve Number", None))

