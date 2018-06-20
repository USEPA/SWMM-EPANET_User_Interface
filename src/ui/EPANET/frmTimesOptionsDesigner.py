# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmTimesOptionsDesigner.ui'
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

class Ui_frmTimesOptions(object):
    def setupUi(self, frmTimesOptions):
        frmTimesOptions.setObjectName(_fromUtf8("frmTimesOptions"))
        frmTimesOptions.resize(302, 354)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTimesOptions.setFont(font)
        self.centralWidget = QWidget(frmTimesOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.gridLayout = QGridLayout(self.fraTop)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblTotalDuration = QLabel(self.fraTop)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTotalDuration.setFont(font)
        self.lblTotalDuration.setObjectName(_fromUtf8("lblTotalDuration"))
        self.gridLayout.addWidget(self.lblTotalDuration, 0, 0, 1, 1)
        self.txtTotalDuration = QLineEdit(self.fraTop)
        self.txtTotalDuration.setObjectName(_fromUtf8("txtTotalDuration"))
        self.gridLayout.addWidget(self.txtTotalDuration, 0, 1, 1, 1)
        self.lblHydraulic = QLabel(self.fraTop)
        self.lblHydraulic.setObjectName(_fromUtf8("lblHydraulic"))
        self.gridLayout.addWidget(self.lblHydraulic, 1, 0, 1, 1)
        self.txtHydraulic = QLineEdit(self.fraTop)
        self.txtHydraulic.setObjectName(_fromUtf8("txtHydraulic"))
        self.gridLayout.addWidget(self.txtHydraulic, 1, 1, 1, 1)
        self.lblQuality = QLabel(self.fraTop)
        self.lblQuality.setObjectName(_fromUtf8("lblQuality"))
        self.gridLayout.addWidget(self.lblQuality, 2, 0, 1, 1)
        self.txtQuality = QLineEdit(self.fraTop)
        self.txtQuality.setObjectName(_fromUtf8("txtQuality"))
        self.gridLayout.addWidget(self.txtQuality, 2, 1, 1, 1)
        self.lblRule = QLabel(self.fraTop)
        self.lblRule.setObjectName(_fromUtf8("lblRule"))
        self.gridLayout.addWidget(self.lblRule, 3, 0, 1, 1)
        self.txtRule = QLineEdit(self.fraTop)
        self.txtRule.setObjectName(_fromUtf8("txtRule"))
        self.gridLayout.addWidget(self.txtRule, 3, 1, 1, 1)
        self.lblPattern = QLabel(self.fraTop)
        self.lblPattern.setObjectName(_fromUtf8("lblPattern"))
        self.gridLayout.addWidget(self.lblPattern, 4, 0, 1, 1)
        self.txtPattern = QLineEdit(self.fraTop)
        self.txtPattern.setObjectName(_fromUtf8("txtPattern"))
        self.gridLayout.addWidget(self.txtPattern, 4, 1, 1, 1)
        self.lblPatternTime = QLabel(self.fraTop)
        self.lblPatternTime.setObjectName(_fromUtf8("lblPatternTime"))
        self.gridLayout.addWidget(self.lblPatternTime, 5, 0, 1, 1)
        self.txtPatternTime = QLineEdit(self.fraTop)
        self.txtPatternTime.setObjectName(_fromUtf8("txtPatternTime"))
        self.gridLayout.addWidget(self.txtPatternTime, 5, 1, 1, 1)
        self.lblReporting = QLabel(self.fraTop)
        self.lblReporting.setObjectName(_fromUtf8("lblReporting"))
        self.gridLayout.addWidget(self.lblReporting, 6, 0, 1, 1)
        self.txtReporting = QLineEdit(self.fraTop)
        self.txtReporting.setObjectName(_fromUtf8("txtReporting"))
        self.gridLayout.addWidget(self.txtReporting, 6, 1, 1, 1)
        self.lblReportingTime = QLabel(self.fraTop)
        self.lblReportingTime.setObjectName(_fromUtf8("lblReportingTime"))
        self.gridLayout.addWidget(self.lblReportingTime, 7, 0, 1, 1)
        self.txtReportingTime = QLineEdit(self.fraTop)
        self.txtReportingTime.setObjectName(_fromUtf8("txtReportingTime"))
        self.gridLayout.addWidget(self.txtReportingTime, 7, 1, 1, 1)
        self.lblClockStart = QLabel(self.fraTop)
        self.lblClockStart.setObjectName(_fromUtf8("lblClockStart"))
        self.gridLayout.addWidget(self.lblClockStart, 8, 0, 1, 1)
        self.txtClockStart = QLineEdit(self.fraTop)
        self.txtClockStart.setObjectName(_fromUtf8("txtClockStart"))
        self.gridLayout.addWidget(self.txtClockStart, 8, 1, 1, 1)
        self.lblStatistic = QLabel(self.fraTop)
        self.lblStatistic.setObjectName(_fromUtf8("lblStatistic"))
        self.gridLayout.addWidget(self.lblStatistic, 9, 0, 1, 1)
        self.cboStatistic = QComboBox(self.fraTop)
        self.cboStatistic.setObjectName(_fromUtf8("cboStatistic"))
        self.gridLayout.addWidget(self.cboStatistic, 9, 1, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(138, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmTimesOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTimesOptions)
        QtCore.QMetaObject.connectSlotsByName(frmTimesOptions)

    def retranslateUi(self, frmTimesOptions):
        frmTimesOptions.setWindowTitle(_translate("frmTimesOptions", "EPANET Times Options", None))
        self.lblTotalDuration.setText(_translate("frmTimesOptions", "Total Duration", None))
        self.lblHydraulic.setText(_translate("frmTimesOptions", "<html><head/><body><p>Hydraulic Time Step</p></body></html>", None))
        self.lblQuality.setText(_translate("frmTimesOptions", "Quality Time Step", None))
        self.lblRule.setText(_translate("frmTimesOptions", "Rule Time Step", None))
        self.lblPattern.setText(_translate("frmTimesOptions", "Pattern Time Step", None))
        self.lblPatternTime.setText(_translate("frmTimesOptions", "Pattern Start Time", None))
        self.lblReporting.setText(_translate("frmTimesOptions", "Reporting Time Step", None))
        self.lblReportingTime.setText(_translate("frmTimesOptions", "Report Start Time", None))
        self.lblClockStart.setText(_translate("frmTimesOptions", "Clock Start Time", None))
        self.lblStatistic.setText(_translate("frmTimesOptions", "Statistic", None))
        self.cmdOK.setText(_translate("frmTimesOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmTimesOptions", "Cancel", None))

