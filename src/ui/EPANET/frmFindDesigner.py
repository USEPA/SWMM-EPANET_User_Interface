# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPANET\frmFindDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmFind(object):
    def setupUi(self, frmFind):
        frmFind.setObjectName("frmFind")
        frmFind.setWindowModality(QtCore.Qt.ApplicationModal)
        frmFind.resize(301, 207)
        frmFind.setMinimumSize(QtCore.QSize(301, 207))
        frmFind.setMaximumSize(QtCore.QSize(301, 207))
        font = QtGui.QFont()
        font.setPointSize(10)
        frmFind.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmFind)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.gbxID = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxID.setObjectName("gbxID")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.gbxID)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.txtID = QtWidgets.QLineEdit(self.gbxID)
        self.txtID.setObjectName("txtID")
        self.verticalLayout_3.addWidget(self.txtID)
        self.gridLayout.addWidget(self.gbxID, 0, 2, 1, 1)
        self.gbxAdjacent = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxAdjacent.setObjectName("gbxAdjacent")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gbxAdjacent)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lstAdjacent = QtWidgets.QListWidget(self.gbxAdjacent)
        self.lstAdjacent.setObjectName("lstAdjacent")
        self.verticalLayout_4.addWidget(self.lstAdjacent)
        self.gridLayout.addWidget(self.gbxAdjacent, 1, 2, 1, 1)
        self.gbxFind = QtWidgets.QGroupBox(self.centralWidget)
        self.gbxFind.setObjectName("gbxFind")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbxFind)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rbnNode = QtWidgets.QRadioButton(self.gbxFind)
        self.rbnNode.setObjectName("rbnNode")
        self.verticalLayout_2.addWidget(self.rbnNode)
        self.rbnLink = QtWidgets.QRadioButton(self.gbxFind)
        self.rbnLink.setObjectName("rbnLink")
        self.verticalLayout_2.addWidget(self.rbnLink)
        self.rbnSources = QtWidgets.QRadioButton(self.gbxFind)
        self.rbnSources.setObjectName("rbnSources")
        self.verticalLayout_2.addWidget(self.rbnSources)
        self.cmdFind = QtWidgets.QPushButton(self.gbxFind)
        self.cmdFind.setObjectName("cmdFind")
        self.verticalLayout_2.addWidget(self.cmdFind)
        self.gridLayout.addWidget(self.gbxFind, 0, 0, 2, 1)
        frmFind.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmFind)
        QtCore.QMetaObject.connectSlotsByName(frmFind)

    def retranslateUi(self, frmFind):
        _translate = QtCore.QCoreApplication.translate
        frmFind.setWindowTitle(_translate("frmFind", "Map Finder"))
        self.gbxID.setTitle(_translate("frmFind", "ID"))
        self.gbxAdjacent.setTitle(_translate("frmFind", "Adjacent"))
        self.gbxFind.setTitle(_translate("frmFind", "Find"))
        self.rbnNode.setText(_translate("frmFind", "Node"))
        self.rbnLink.setText(_translate("frmFind", "Link"))
        self.rbnSources.setText(_translate("frmFind", "Sources"))
        self.cmdFind.setText(_translate("frmFind", "Find"))

