# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\frmQueryDesigner.ui'
#
# Created: Tue Mar 21 14:33:16 2017
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_frmQuery(object):
    def setupUi(self, frmQuery):
        frmQuery.setObjectName(_fromUtf8("frmQuery"))
        frmQuery.setWindowModality(QtCore.Qt.ApplicationModal)
        frmQuery.resize(173, 174)
        frmQuery.setMaximumSize(QtCore.QSize(173, 174))
        font = QtGui.QFont()
        font.setPointSize(10)
        frmQuery.setFont(font)
        self.centralWidget = QtGui.QWidget(frmQuery)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cboFind = QtGui.QComboBox(self.centralWidget)
        self.cboFind.setObjectName(_fromUtf8("cboFind"))
        self.verticalLayout.addWidget(self.cboFind)
        self.cboProperty = QtGui.QComboBox(self.centralWidget)
        self.cboProperty.setObjectName(_fromUtf8("cboProperty"))
        self.verticalLayout.addWidget(self.cboProperty)
        self.cboAbove = QtGui.QComboBox(self.centralWidget)
        self.cboAbove.setObjectName(_fromUtf8("cboAbove"))
        self.verticalLayout.addWidget(self.cboAbove)
        self.fraNum = QtGui.QFrame(self.centralWidget)
        self.fraNum.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraNum.setFrameShadow(QtGui.QFrame.Raised)
        self.fraNum.setObjectName(_fromUtf8("fraNum"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraNum)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtNum = QtGui.QLineEdit(self.fraNum)
        self.txtNum.setObjectName(_fromUtf8("txtNum"))
        self.horizontalLayout.addWidget(self.txtNum)
        self.cmdSubmit = QtGui.QPushButton(self.fraNum)
        self.cmdSubmit.setObjectName(_fromUtf8("cmdSubmit"))
        self.horizontalLayout.addWidget(self.cmdSubmit)
        self.verticalLayout.addWidget(self.fraNum)
        self.txtSummary = QtGui.QLineEdit(self.centralWidget)
        self.txtSummary.setObjectName(_fromUtf8("txtSummary"))
        self.verticalLayout.addWidget(self.txtSummary)
        frmQuery.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmQuery)
        QtCore.QMetaObject.connectSlotsByName(frmQuery)

    def retranslateUi(self, frmQuery):
        frmQuery.setWindowTitle(_translate("frmQuery", "Query", None))
        self.cmdSubmit.setText(_translate("frmQuery", "Submit", None))

