# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPANET\frmControlsDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmControls(object):
    def setupUi(self, frmControls):
        frmControls.setObjectName("frmControls")
        frmControls.resize(541, 245)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmControls.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmControls)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtControls = QtWidgets.QPlainTextEdit(self.frame)
        self.txtControls.setObjectName("txtControls")
        self.verticalLayout.addWidget(self.txtControls)
        self.verticalLayout_2.addWidget(self.frame)
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
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmControls.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmControls)
        QtCore.QMetaObject.connectSlotsByName(frmControls)

    def retranslateUi(self, frmControls):
        _translate = QtCore.QCoreApplication.translate
        frmControls.setWindowTitle(_translate("frmControls", "EPANET Controls"))
        self.cmdOK.setText(_translate("frmControls", "OK"))
        self.cmdCancel.setText(_translate("frmControls", "Cancel"))

