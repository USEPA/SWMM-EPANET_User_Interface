# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmTimeStepsDesigner.ui'
#
# Created: Tue Mar 08 16:51:05 2016
#      by: PyQt4 UI code generator 4.11.3
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
        frmTimeSteps.resize(366, 358)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTimeSteps.setFont(font)
        self.centralWidget = QtGui.QWidget(frmTimeSteps)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_2 = QtGui.QFrame(self.centralWidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblDays = QtGui.QLabel(self.frame_2)
        self.lblDays.setObjectName(_fromUtf8("lblDays"))
        self.gridLayout.addWidget(self.lblDays, 0, 1, 1, 1)
        self.lblHr = QtGui.QLabel(self.frame_2)
        self.lblHr.setObjectName(_fromUtf8("lblHr"))
        self.gridLayout.addWidget(self.lblHr, 0, 2, 1, 1)
        self.lblReporting = QtGui.QLabel(self.frame_2)
        self.lblReporting.setObjectName(_fromUtf8("lblReporting"))
        self.gridLayout.addWidget(self.lblReporting, 1, 0, 1, 1)
        self.sbxReportDay = QtGui.QSpinBox(self.frame_2)
        self.sbxReportDay.setMaximumSize(QtCore.QSize(150, 16777215))
        self.sbxReportDay.setObjectName(_fromUtf8("sbxReportDay"))
        self.gridLayout.addWidget(self.sbxReportDay, 1, 1, 1, 1)
        self.tmeReport = QtGui.QTimeEdit(self.frame_2)
        self.tmeReport.setMinimumSize(QtCore.QSize(70, 0))
        self.tmeReport.setProperty("showGroupSeparator", False)
        self.tmeReport.setObjectName(_fromUtf8("tmeReport"))
        self.gridLayout.addWidget(self.tmeReport, 1, 2, 1, 1)
        self.lblRunoffDry = QtGui.QLabel(self.frame_2)
        self.lblRunoffDry.setTextFormat(QtCore.Qt.AutoText)
        self.lblRunoffDry.setObjectName(_fromUtf8("lblRunoffDry"))
        self.gridLayout.addWidget(self.lblRunoffDry, 2, 0, 1, 1)
        self.sbxDry = QtGui.QSpinBox(self.frame_2)
        self.sbxDry.setMaximumSize(QtCore.QSize(150, 16777215))
        self.sbxDry.setObjectName(_fromUtf8("sbxDry"))
        self.gridLayout.addWidget(self.sbxDry, 2, 1, 1, 1)
        self.tmeDry = QtGui.QTimeEdit(self.frame_2)
        self.tmeDry.setMinimumSize(QtCore.QSize(70, 0))
        self.tmeDry.setProperty("showGroupSeparator", False)
        self.tmeDry.setObjectName(_fromUtf8("tmeDry"))
        self.gridLayout.addWidget(self.tmeDry, 2, 2, 1, 1)
        self.lblRunoffWet = QtGui.QLabel(self.frame_2)
        self.lblRunoffWet.setObjectName(_fromUtf8("lblRunoffWet"))
        self.gridLayout.addWidget(self.lblRunoffWet, 3, 0, 1, 1)
        self.sbxWet = QtGui.QSpinBox(self.frame_2)
        self.sbxWet.setMaximumSize(QtCore.QSize(150, 16777215))
        self.sbxWet.setObjectName(_fromUtf8("sbxWet"))
        self.gridLayout.addWidget(self.sbxWet, 3, 1, 1, 1)
        self.tmeWet = QtGui.QTimeEdit(self.frame_2)
        self.tmeWet.setMinimumSize(QtCore.QSize(70, 0))
        self.tmeWet.setProperty("showGroupSeparator", False)
        self.tmeWet.setObjectName(_fromUtf8("tmeWet"))
        self.gridLayout.addWidget(self.tmeWet, 3, 2, 1, 1)
        self.lblRouting = QtGui.QLabel(self.frame_2)
        self.lblRouting.setObjectName(_fromUtf8("lblRouting"))
        self.gridLayout.addWidget(self.lblRouting, 4, 0, 1, 1)
        self.txtRouting = QtGui.QLineEdit(self.frame_2)
        self.txtRouting.setMaximumSize(QtCore.QSize(150, 16777215))
        self.txtRouting.setObjectName(_fromUtf8("txtRouting"))
        self.gridLayout.addWidget(self.txtRouting, 4, 1, 1, 1)
        self.lblSeconds = QtGui.QLabel(self.frame_2)
        self.lblSeconds.setObjectName(_fromUtf8("lblSeconds"))
        self.gridLayout.addWidget(self.lblSeconds, 4, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.gbxSteady = QtGui.QGroupBox(self.centralWidget)
        self.gbxSteady.setObjectName(_fromUtf8("gbxSteady"))
        self.formLayout = QtGui.QFormLayout(self.gbxSteady)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.cbxSkip = QtGui.QCheckBox(self.gbxSteady)
        self.cbxSkip.setObjectName(_fromUtf8("cbxSkip"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.cbxSkip)
        self.lblSystem = QtGui.QLabel(self.gbxSteady)
        self.lblSystem.setObjectName(_fromUtf8("lblSystem"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblSystem)
        self.sbxSystem = QtGui.QSpinBox(self.gbxSteady)
        self.sbxSystem.setMaximumSize(QtCore.QSize(150, 16777215))
        self.sbxSystem.setObjectName(_fromUtf8("sbxSystem"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sbxSystem)
        self.lblLateral = QtGui.QLabel(self.gbxSteady)
        self.lblLateral.setObjectName(_fromUtf8("lblLateral"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblLateral)
        self.sbxLateral = QtGui.QSpinBox(self.gbxSteady)
        self.sbxLateral.setMaximumSize(QtCore.QSize(150, 16777215))
        self.sbxLateral.setObjectName(_fromUtf8("sbxLateral"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.sbxLateral)
        self.verticalLayout.addWidget(self.gbxSteady)
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(163, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.frame)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.frame)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.frame)
        frmTimeSteps.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTimeSteps)
        QtCore.QMetaObject.connectSlotsByName(frmTimeSteps)
        frmTimeSteps.setTabOrder(self.sbxReportDay, self.tmeReport)
        frmTimeSteps.setTabOrder(self.tmeReport, self.sbxDry)
        frmTimeSteps.setTabOrder(self.sbxDry, self.tmeDry)
        frmTimeSteps.setTabOrder(self.tmeDry, self.sbxWet)
        frmTimeSteps.setTabOrder(self.sbxWet, self.tmeWet)
        frmTimeSteps.setTabOrder(self.tmeWet, self.txtRouting)
        frmTimeSteps.setTabOrder(self.txtRouting, self.cbxSkip)
        frmTimeSteps.setTabOrder(self.cbxSkip, self.sbxSystem)
        frmTimeSteps.setTabOrder(self.sbxSystem, self.sbxLateral)
        frmTimeSteps.setTabOrder(self.sbxLateral, self.cmdOK)
        frmTimeSteps.setTabOrder(self.cmdOK, self.cmdCancel)

    def retranslateUi(self, frmTimeSteps):
        frmTimeSteps.setWindowTitle(_translate("frmTimeSteps", "SWMM Time Steps Options", None))
        self.lblDays.setText(_translate("frmTimeSteps", "Days", None))
        self.lblHr.setText(_translate("frmTimeSteps", "Hr:Min:Sec", None))
        self.lblReporting.setText(_translate("frmTimeSteps", "Reporting", None))
        self.tmeReport.setDisplayFormat(_translate("frmTimeSteps", "h:mm:ss", None))
        self.lblRunoffDry.setText(_translate("frmTimeSteps", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Runoff:</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Dry weather</p></body></html>", None))
        self.tmeDry.setDisplayFormat(_translate("frmTimeSteps", "h:mm:ss", None))
        self.lblRunoffWet.setText(_translate("frmTimeSteps", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Runoff:</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Wet weather</p></body></html>", None))
        self.tmeWet.setDisplayFormat(_translate("frmTimeSteps", "h:mm:ss", None))
        self.lblRouting.setText(_translate("frmTimeSteps", "Routing", None))
        self.lblSeconds.setText(_translate("frmTimeSteps", "Seconds", None))
        self.gbxSteady.setTitle(_translate("frmTimeSteps", "Steady Flow Periods", None))
        self.cbxSkip.setText(_translate("frmTimeSteps", "Skip Steady Flow Periods", None))
        self.lblSystem.setText(_translate("frmTimeSteps", "System Flow Tolerance (%)", None))
        self.lblLateral.setText(_translate("frmTimeSteps", "Lateral Flow Tolerance (%)", None))
        self.cmdOK.setText(_translate("frmTimeSteps", "OK", None))
        self.cmdCancel.setText(_translate("frmTimeSteps", "Cancel", None))

