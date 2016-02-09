# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmReportOptions.ui'
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

class Ui_frmReportOptions(object):
    def setupUi(self, frmReportOptions):
        frmReportOptions.setObjectName(_fromUtf8("frmReportOptions"))
        frmReportOptions.resize(574, 359)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmReportOptions.setFont(font)
        self.centralWidget = QtGui.QWidget(frmReportOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(200, 320, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(300, 320, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.gbxNode = QtGui.QGroupBox(self.centralWidget)
        self.gbxNode.setGeometry(QtCore.QRect(20, 90, 171, 211))
        self.gbxNode.setObjectName(_fromUtf8("gbxNode"))
        self.listWidget = QtGui.QListWidget(self.gbxNode)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 131, 141))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.cmdNodeAll = QtGui.QPushButton(self.gbxNode)
        self.cmdNodeAll.setGeometry(QtCore.QRect(20, 170, 51, 23))
        self.cmdNodeAll.setObjectName(_fromUtf8("cmdNodeAll"))
        self.cmdNodeNone = QtGui.QPushButton(self.gbxNode)
        self.cmdNodeNone.setGeometry(QtCore.QRect(80, 170, 51, 23))
        self.cmdNodeNone.setObjectName(_fromUtf8("cmdNodeNone"))
        self.gbxReport = QtGui.QGroupBox(self.centralWidget)
        self.gbxReport.setGeometry(QtCore.QRect(20, 10, 531, 71))
        self.gbxReport.setObjectName(_fromUtf8("gbxReport"))
        self.cbxControls = QtGui.QCheckBox(self.gbxReport)
        self.cbxControls.setGeometry(QtCore.QRect(420, 30, 101, 17))
        self.cbxControls.setObjectName(_fromUtf8("cbxControls"))
        self.cbxInput = QtGui.QCheckBox(self.gbxReport)
        self.cbxInput.setGeometry(QtCore.QRect(30, 30, 121, 17))
        self.cbxInput.setObjectName(_fromUtf8("cbxInput"))
        self.cbxFlow = QtGui.QCheckBox(self.gbxReport)
        self.cbxFlow.setGeometry(QtCore.QRect(310, 30, 101, 17))
        self.cbxFlow.setObjectName(_fromUtf8("cbxFlow"))
        self.cbxContinuity = QtGui.QCheckBox(self.gbxReport)
        self.cbxContinuity.setGeometry(QtCore.QRect(160, 30, 141, 17))
        self.cbxContinuity.setObjectName(_fromUtf8("cbxContinuity"))
        self.gbxLinks = QtGui.QGroupBox(self.centralWidget)
        self.gbxLinks.setGeometry(QtCore.QRect(200, 90, 171, 211))
        self.gbxLinks.setObjectName(_fromUtf8("gbxLinks"))
        self.listWidget_2 = QtGui.QListWidget(self.gbxLinks)
        self.listWidget_2.setGeometry(QtCore.QRect(20, 20, 131, 141))
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.cmdLinksAll = QtGui.QPushButton(self.gbxLinks)
        self.cmdLinksAll.setGeometry(QtCore.QRect(20, 170, 51, 23))
        self.cmdLinksAll.setObjectName(_fromUtf8("cmdLinksAll"))
        self.cmdLinksNone = QtGui.QPushButton(self.gbxLinks)
        self.cmdLinksNone.setGeometry(QtCore.QRect(80, 170, 51, 23))
        self.cmdLinksNone.setObjectName(_fromUtf8("cmdLinksNone"))
        self.gbxSubcatchments = QtGui.QGroupBox(self.centralWidget)
        self.gbxSubcatchments.setGeometry(QtCore.QRect(380, 90, 171, 211))
        self.gbxSubcatchments.setObjectName(_fromUtf8("gbxSubcatchments"))
        self.listWidget_3 = QtGui.QListWidget(self.gbxSubcatchments)
        self.listWidget_3.setGeometry(QtCore.QRect(20, 20, 131, 141))
        self.listWidget_3.setObjectName(_fromUtf8("listWidget_3"))
        self.cmdSubcatchmentsAll = QtGui.QPushButton(self.gbxSubcatchments)
        self.cmdSubcatchmentsAll.setGeometry(QtCore.QRect(20, 170, 51, 23))
        self.cmdSubcatchmentsAll.setObjectName(_fromUtf8("cmdSubcatchmentsAll"))
        self.cmdSubcatchmentsNone = QtGui.QPushButton(self.gbxSubcatchments)
        self.cmdSubcatchmentsNone.setGeometry(QtCore.QRect(80, 170, 51, 23))
        self.cmdSubcatchmentsNone.setObjectName(_fromUtf8("cmdSubcatchmentsNone"))
        frmReportOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmReportOptions)
        QtCore.QMetaObject.connectSlotsByName(frmReportOptions)

    def retranslateUi(self, frmReportOptions):
        frmReportOptions.setWindowTitle(_translate("frmReportOptions", "SWMM Report Options", None))
        self.cmdOK.setText(_translate("frmReportOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmReportOptions", "Cancel", None))
        self.gbxNode.setTitle(_translate("frmReportOptions", "Nodes", None))
        self.cmdNodeAll.setText(_translate("frmReportOptions", "All", None))
        self.cmdNodeNone.setText(_translate("frmReportOptions", "None", None))
        self.gbxReport.setTitle(_translate("frmReportOptions", "Report Options", None))
        self.cbxControls.setText(_translate("frmReportOptions", "Controls", None))
        self.cbxInput.setText(_translate("frmReportOptions", "Input Summary", None))
        self.cbxFlow.setText(_translate("frmReportOptions", "Flow Stats", None))
        self.cbxContinuity.setText(_translate("frmReportOptions", "Continuity Checks", None))
        self.gbxLinks.setTitle(_translate("frmReportOptions", "Links", None))
        self.cmdLinksAll.setText(_translate("frmReportOptions", "All", None))
        self.cmdLinksNone.setText(_translate("frmReportOptions", "None", None))
        self.gbxSubcatchments.setTitle(_translate("frmReportOptions", "Subcatchments", None))
        self.cmdSubcatchmentsAll.setText(_translate("frmReportOptions", "All", None))
        self.cmdSubcatchmentsNone.setText(_translate("frmReportOptions", "None", None))

