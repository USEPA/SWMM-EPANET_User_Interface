# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\frmFindDesigner.ui'
#
# Created: Tue Mar 21 16:00:04 2017
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

class Ui_frmFind(object):
    def setupUi(self, frmFind):
        frmFind.setObjectName(_fromUtf8("frmFind"))
        frmFind.setWindowModality(QtCore.Qt.ApplicationModal)
        frmFind.resize(301, 207)
        frmFind.setMinimumSize(QtCore.QSize(301, 207))
        frmFind.setMaximumSize(QtCore.QSize(301, 207))
        font = QtGui.QFont()
        font.setPointSize(10)
        frmFind.setFont(font)
        self.centralWidget = QtGui.QWidget(frmFind)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gbxID = QtGui.QGroupBox(self.centralWidget)
        self.gbxID.setObjectName(_fromUtf8("gbxID"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbxID)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.txtID = QtGui.QLineEdit(self.gbxID)
        self.txtID.setObjectName(_fromUtf8("txtID"))
        self.verticalLayout_3.addWidget(self.txtID)
        self.gridLayout.addWidget(self.gbxID, 0, 2, 1, 1)
        self.gbxAdjacent = QtGui.QGroupBox(self.centralWidget)
        self.gbxAdjacent.setObjectName(_fromUtf8("gbxAdjacent"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbxAdjacent)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.lstAdjacent = QtGui.QListWidget(self.gbxAdjacent)
        self.lstAdjacent.setObjectName(_fromUtf8("lstAdjacent"))
        self.verticalLayout_4.addWidget(self.lstAdjacent)
        self.gridLayout.addWidget(self.gbxAdjacent, 1, 2, 1, 1)
        self.gbxFind = QtGui.QGroupBox(self.centralWidget)
        self.gbxFind.setObjectName(_fromUtf8("gbxFind"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbxFind)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.rbnNode = QtGui.QRadioButton(self.gbxFind)
        self.rbnNode.setObjectName(_fromUtf8("rbnNode"))
        self.verticalLayout_2.addWidget(self.rbnNode)
        self.rbnLink = QtGui.QRadioButton(self.gbxFind)
        self.rbnLink.setObjectName(_fromUtf8("rbnLink"))
        self.verticalLayout_2.addWidget(self.rbnLink)
        self.rbnSources = QtGui.QRadioButton(self.gbxFind)
        self.rbnSources.setObjectName(_fromUtf8("rbnSources"))
        self.verticalLayout_2.addWidget(self.rbnSources)
        self.cmdFind = QtGui.QPushButton(self.gbxFind)
        self.cmdFind.setObjectName(_fromUtf8("cmdFind"))
        self.verticalLayout_2.addWidget(self.cmdFind)
        self.gridLayout.addWidget(self.gbxFind, 0, 0, 2, 1)
        frmFind.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmFind)
        QtCore.QMetaObject.connectSlotsByName(frmFind)

    def retranslateUi(self, frmFind):
        frmFind.setWindowTitle(_translate("frmFind", "Map Finder", None))
        self.gbxID.setTitle(_translate("frmFind", "ID", None))
        self.gbxAdjacent.setTitle(_translate("frmFind", "Adjacent", None))
        self.gbxFind.setTitle(_translate("frmFind", "Find", None))
        self.rbnNode.setText(_translate("frmFind", "Node", None))
        self.rbnLink.setText(_translate("frmFind", "Link", None))
        self.rbnSources.setText(_translate("frmFind", "Sources", None))
        self.cmdFind.setText(_translate("frmFind", "Find", None))

