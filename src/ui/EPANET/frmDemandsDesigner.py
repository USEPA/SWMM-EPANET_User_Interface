# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPANET\frmDemandsDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmDemands(object):
    def setupUi(self, frmDemands):
        frmDemands.setObjectName("frmDemands")
        frmDemands.resize(484, 356)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmDemands.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmDemands)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fraTop = QtWidgets.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraTop.setObjectName("fraTop")
        self.gridLayout = QtWidgets.QGridLayout(self.fraTop)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tblDemands = QtWidgets.QTableWidget(self.fraTop)
        self.tblDemands.setRowCount(10)
        self.tblDemands.setObjectName("tblDemands")
        self.tblDemands.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblDemands.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tblDemands, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
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
        frmDemands.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmDemands)
        QtCore.QMetaObject.connectSlotsByName(frmDemands)

    def retranslateUi(self, frmDemands):
        _translate = QtCore.QCoreApplication.translate
        frmDemands.setWindowTitle(_translate("frmDemands", "EPANET Demands Editor"))
        item = self.tblDemands.horizontalHeaderItem(0)
        item.setText(_translate("frmDemands", "Base Demand"))
        item = self.tblDemands.horizontalHeaderItem(1)
        item.setText(_translate("frmDemands", "Time Pattern"))
        item = self.tblDemands.horizontalHeaderItem(2)
        item.setText(_translate("frmDemands", "Category"))
        self.cmdOK.setText(_translate("frmDemands", "OK"))
        self.cmdCancel.setText(_translate("frmDemands", "Cancel"))

