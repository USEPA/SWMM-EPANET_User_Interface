# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmGenericPropertyEditorDesigner.ui'
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

class Ui_frmGenericPropertyEditor(object):
    def setupUi(self, frmGenericPropertyEditor):
        frmGenericPropertyEditor.setObjectName(_fromUtf8("frmGenericPropertyEditor"))
        frmGenericPropertyEditor.resize(538, 461)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmGenericPropertyEditor.setFont(font)
        self.centralWidget = QWidget(frmGenericPropertyEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QVBoxLayout(self.centralWidget)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraTop)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tblGeneric = QTableWidget(self.fraTop)
        self.tblGeneric.setObjectName(_fromUtf8("tblGeneric"))
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(0)
        item = QTableWidgetItem()
        self.tblGeneric.setHorizontalHeaderItem(0, item)
        self.horizontalLayout_2.addWidget(self.tblGeneric)
        self.verticalLayout_2.addWidget(self.fraTop)
        self.fraNotes = QFrame(self.centralWidget)
        self.fraNotes.setFrameShape(QFrame.StyledPanel)
        self.fraNotes.setFrameShadow(QFrame.Raised)
        self.fraNotes.setObjectName(_fromUtf8("fraNotes"))
        self.verticalLayout = QVBoxLayout(self.fraNotes)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
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
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
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
        frmGenericPropertyEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmGenericPropertyEditor)
        QtCore.QMetaObject.connectSlotsByName(frmGenericPropertyEditor)

    def retranslateUi(self, frmGenericPropertyEditor):
        frmGenericPropertyEditor.setWindowTitle(_translate("frmGenericPropertyEditor", "SWMM Property Editor", None))
        item = self.tblGeneric.horizontalHeaderItem(0)
        item.setText(_translate("frmGenericPropertyEditor", "Value", None))
        self.lblNotes.setText(_translate("frmGenericPropertyEditor", "Explanatory notes", None))
        self.cmdOK.setText(_translate("frmGenericPropertyEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmGenericPropertyEditor", "Cancel", None))

