# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPANET\frmTitleDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmTitle(object):
    def setupUi(self, frmTitle):
        frmTitle.setObjectName("frmTitle")
        frmTitle.resize(541, 194)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmTitle.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmTitle)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.formLayout = QtWidgets.QFormLayout(self.frame)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.lblTitle = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblTitle)
        self.txtTitle = QtWidgets.QPlainTextEdit(self.frame)
        self.txtTitle.setObjectName("txtTitle")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtTitle)
        self.verticalLayout.addWidget(self.frame)
        self.fraOKCancel = QtWidgets.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraOKCancel.setObjectName("fraOKCancel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmTitle.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTitle)
        QtCore.QMetaObject.connectSlotsByName(frmTitle)

    def retranslateUi(self, frmTitle):
        _translate = QtCore.QCoreApplication.translate
        frmTitle.setWindowTitle(_translate("frmTitle", "EPANET Title"))
        self.lblTitle.setText(_translate("frmTitle", "Title:"))
        self.cmdOK.setText(_translate("frmTitle", "OK"))
        self.cmdCancel.setText(_translate("frmTitle", "Cancel"))

