# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmTitleDesigner.ui'
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

class Ui_frmTitle(object):
    def setupUi(self, frmTitle):
        frmTitle.setObjectName(_fromUtf8("frmTitle"))
        frmTitle.resize(541, 153)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTitle.setFont(font)
        self.centralWidget = QWidget(frmTitle)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QFrame(self.centralWidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.formLayout = QFormLayout(self.frame)
        # self.formLayout.setMargin(11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblTitle = QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblTitle)
        self.txtTitle = QPlainTextEdit(self.frame)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtTitle)
        self.verticalLayout.addWidget(self.frame)
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
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmTitle.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTitle)
        QtCore.QMetaObject.connectSlotsByName(frmTitle)

    def retranslateUi(self, frmTitle):
        frmTitle.setWindowTitle(_translate("frmTitle", "EPANET Title", None))
        self.lblTitle.setText(_translate("frmTitle", "Title:", None))
        self.cmdOK.setText(_translate("frmTitle", "OK", None))
        self.cmdCancel.setText(_translate("frmTitle", "Cancel", None))

