# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\frmQueryDesigner.ui'
#
# Created: Tue Mar 21 14:33:16 2017
#      by: PyQt5 UI code generator 4.10.2
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

class Ui_frmQuery(object):
    def setupUi(self, frmQuery):
        frmQuery.setObjectName(_fromUtf8("frmQuery"))
        frmQuery.setWindowModality(QtCore.Qt.ApplicationModal)
        frmQuery.resize(173, 174)
        frmQuery.setMaximumSize(QtCore.QSize(173, 174))
        font = QtGui.QFont()
        font.setPointSize(10)
        frmQuery.setFont(font)
        self.centralWidget = QWidget(frmQuery)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cboFind = QComboBox(self.centralWidget)
        self.cboFind.setObjectName(_fromUtf8("cboFind"))
        self.verticalLayout.addWidget(self.cboFind)
        self.cboProperty = QComboBox(self.centralWidget)
        self.cboProperty.setObjectName(_fromUtf8("cboProperty"))
        self.verticalLayout.addWidget(self.cboProperty)
        self.cboAbove = QComboBox(self.centralWidget)
        self.cboAbove.setObjectName(_fromUtf8("cboAbove"))
        self.verticalLayout.addWidget(self.cboAbove)
        self.fraNum = QFrame(self.centralWidget)
        self.fraNum.setFrameShape(QFrame.StyledPanel)
        self.fraNum.setFrameShadow(QFrame.Raised)
        self.fraNum.setObjectName(_fromUtf8("fraNum"))
        self.horizontalLayout = QHBoxLayout(self.fraNum)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtNum = QLineEdit(self.fraNum)
        self.txtNum.setObjectName(_fromUtf8("txtNum"))
        self.horizontalLayout.addWidget(self.txtNum)
        self.cmdSubmit = QPushButton(self.fraNum)
        self.cmdSubmit.setObjectName(_fromUtf8("cmdSubmit"))
        self.horizontalLayout.addWidget(self.cmdSubmit)
        self.verticalLayout.addWidget(self.fraNum)
        self.txtSummary = QLineEdit(self.centralWidget)
        self.txtSummary.setObjectName(_fromUtf8("txtSummary"))
        self.verticalLayout.addWidget(self.txtSummary)
        frmQuery.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmQuery)
        QtCore.QMetaObject.connectSlotsByName(frmQuery)

    def retranslateUi(self, frmQuery):
        frmQuery.setWindowTitle(_translate("frmQuery", "Query", None))
        self.cmdSubmit.setText(_translate("frmQuery", "Submit", None))

