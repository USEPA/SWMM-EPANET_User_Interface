# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmTitleDesigner.ui'
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
        frmTitle.resize(541, 153)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTitle.setFont(font)
        self.centralWidget = QtGui.QWidget(frmTitle)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.formLayout = QtGui.QFormLayout(self.frame)
        self.formLayout.setMargin(11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblTitle = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName(_fromUtf8("lblTitle"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblTitle)
        self.txtTitle = QtGui.QPlainTextEdit(self.frame)
        self.txtTitle.setObjectName(_fromUtf8("txtTitle"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtTitle)
        self.verticalLayout.addWidget(self.frame)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(338, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
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

