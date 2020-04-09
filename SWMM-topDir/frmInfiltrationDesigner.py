# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SWMM\frmInfiltrationDesigner.ui'
#
# Created: Sun Jan 29 00:57:35 2017
#      by: PyQt5 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
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

class Ui_frmInfiltrationEditor(object):
    def setupUi(self, frmInfiltrationEditor):
        frmInfiltrationEditor.setObjectName(_fromUtf8("frmInfiltrationEditor"))
        frmInfiltrationEditor.resize(285, 338)
        font = QFont()
        font.setPointSize(10)
        frmInfiltrationEditor.setFont(font)
        self.centralWidget = QWidget(frmInfiltrationEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.formLayout = QFormLayout(self.fraTop)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblTop = QLabel(self.fraTop)
        self.lblTop.setObjectName(_fromUtf8("lblTop"))
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblTop)
        self.cboInfilModel = QComboBox(self.fraTop)
        self.cboInfilModel.setObjectName(_fromUtf8("cboInfilModel"))
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cboInfilModel)
        self.tblGeneric = QTableWidget(self.fraTop)
        self.tblGeneric.setObjectName(_fromUtf8("tblGeneric"))
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(0)
        item = QTableWidgetItem()
        self.tblGeneric.setHorizontalHeaderItem(0, item)
        self.tblGeneric.horizontalHeader().setStretchLastSection(True)
        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.tblGeneric)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraNotes = QFrame(self.centralWidget)
        self.fraNotes.setFrameShape(QFrame.StyledPanel)
        self.fraNotes.setFrameShadow(QFrame.Raised)
        self.fraNotes.setObjectName(_fromUtf8("fraNotes"))
        self.verticalLayout = QVBoxLayout(self.fraNotes)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblNotes = QLabel(self.fraNotes)
        self.lblNotes.setWordWrap(True)
        self.lblNotes.setObjectName(_fromUtf8("lblNotes"))
        self.verticalLayout.addWidget(self.lblNotes)
        self.verticalLayout_2.addWidget(self.fraNotes)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmInfiltrationEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmInfiltrationEditor)
        QtCore.QMetaObject.connectSlotsByName(frmInfiltrationEditor)

    def retranslateUi(self, frmInfiltrationEditor):
        frmInfiltrationEditor.setWindowTitle(_translate("frmInfiltrationEditor", "SWMM Infiltration Editor", None))
        self.lblTop.setText(_translate("frmInfiltrationEditor", "<html><head/><body><p>Infiltration Method:  </p></body></html>", None))
        item = self.tblGeneric.horizontalHeaderItem(0)
        item.setText(_translate("frmInfiltrationEditor", "Value", None))
        self.lblNotes.setText(_translate("frmInfiltrationEditor", "Explanatory notes", None))
        self.cmdOK.setText(_translate("frmInfiltrationEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmInfiltrationEditor", "Cancel", None))

