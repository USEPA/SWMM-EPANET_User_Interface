# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmSummaryReportDesigner.ui'
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

class Ui_frmSummaryReport(object):
    def setupUi(self, frmSummaryReport):
        frmSummaryReport.setObjectName(_fromUtf8("frmSummaryReport"))
        frmSummaryReport.resize(541, 385)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmSummaryReport.setFont(font)
        self.centralWidget = QtGui.QWidget(frmSummaryReport)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QtGui.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.verticalLayout = QtGui.QVBoxLayout(self.fraTop)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTopic = QtGui.QFrame(self.fraTop)
        self.fraTopic.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTopic.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTopic.setObjectName(_fromUtf8("fraTopic"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.fraTopic)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblTopic = QtGui.QLabel(self.fraTopic)
        self.lblTopic.setObjectName(_fromUtf8("lblTopic"))
        self.horizontalLayout_2.addWidget(self.lblTopic)
        self.cboType = QtGui.QComboBox(self.fraTopic)
        self.cboType.setObjectName(_fromUtf8("cboType"))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.cboType.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cboType)
        self.label = QtGui.QLabel(self.fraTopic)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.fraTopic)
        self.tblSummary = QtGui.QTableWidget(self.fraTop)
        self.tblSummary.setObjectName(_fromUtf8("tblSummary"))
        self.tblSummary.setColumnCount(0)
        self.tblSummary.setRowCount(0)
        self.verticalLayout.addWidget(self.tblSummary)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(338, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmSummaryReport.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmSummaryReport)
        QtCore.QMetaObject.connectSlotsByName(frmSummaryReport)

    def retranslateUi(self, frmSummaryReport):
        frmSummaryReport.setWindowTitle(_translate("frmSummaryReport", "SWMM Summary Report", None))
        self.lblTopic.setText(_translate("frmSummaryReport", "Topic:", None))
        self.cboType.setItemText(0, _translate("frmSummaryReport", "Subcatchment Runoff", None))
        self.cboType.setItemText(1, _translate("frmSummaryReport", "Subcatchment Washoff", None))
        self.cboType.setItemText(2, _translate("frmSummaryReport", "Node Depth", None))
        self.cboType.setItemText(3, _translate("frmSummaryReport", "Node Inflow", None))
        self.cboType.setItemText(4, _translate("frmSummaryReport", "Node Surcharge", None))
        self.cboType.setItemText(5, _translate("frmSummaryReport", "Node Flooding", None))
        self.cboType.setItemText(6, _translate("frmSummaryReport", "Outfall Loading", None))
        self.cboType.setItemText(7, _translate("frmSummaryReport", "Link Flow", None))
        self.cboType.setItemText(8, _translate("frmSummaryReport", "Conduit Surcharge", None))
        self.cboType.setItemText(9, _translate("frmSummaryReport", "Link Pollutant Load", None))
        self.label.setText(_translate("frmSummaryReport", "Click a column header to sort the column.", None))
        self.cmdCancel.setText(_translate("frmSummaryReport", "Close", None))

