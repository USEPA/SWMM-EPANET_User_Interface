# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmTitle.ui'
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

class Ui_frmTitle(object):
    def setupUi(self, frmTitle):
        frmTitle.setObjectName(_fromUtf8("frmTitle"))
        frmTitle.resize(538, 137)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTitle.setFont(font)
        self.centralWidget = QtGui.QWidget(frmTitle)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.lblTitle = QtGui.QLabel(self.centralWidget)
        self.lblTitle.setGeometry(QtCore.QRect(20, 20, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.cmdOK = QtGui.QPushButton(self.centralWidget)
        self.cmdOK.setGeometry(QtCore.QRect(180, 100, 75, 23))
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.cmdCancel = QtGui.QPushButton(self.centralWidget)
        self.cmdCancel.setGeometry(QtCore.QRect(280, 100, 75, 23))
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.txtTitle = QtGui.QPlainTextEdit(self.centralWidget)
        self.txtTitle.setGeometry(QtCore.QRect(70, 20, 451, 71))
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        frmTitle.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTitle)
        QtCore.QMetaObject.connectSlotsByName(frmTitle)

    def retranslateUi(self, frmTitle):
        frmTitle.setWindowTitle(_translate("frmTitle", "SWMM Title", None))
        self.lblTitle.setText(_translate("frmTitle", "Title:", None))
        self.cmdOK.setText(_translate("frmTitle", "OK", None))
        self.cmdCancel.setText(_translate("frmTitle", "Cancel", None))

