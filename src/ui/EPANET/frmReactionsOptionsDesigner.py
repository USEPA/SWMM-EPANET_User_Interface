# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmReactionsOptionsDesigner.ui'
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

class Ui_frmReactionsOptions(object):
    def setupUi(self, frmReactionsOptions):
        frmReactionsOptions.setObjectName(_fromUtf8("frmReactionsOptions"))
        frmReactionsOptions.resize(339, 261)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmReactionsOptions.setFont(font)
        self.centralWidget = QWidget(frmReactionsOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.gridLayout = QGridLayout(self.fraTop)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBulkOrder = QLabel(self.fraTop)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblBulkOrder.setFont(font)
        self.lblBulkOrder.setObjectName(_fromUtf8("lblBulkOrder"))
        self.gridLayout.addWidget(self.lblBulkOrder, 0, 0, 1, 1)
        self.txtBulkOrder = QLineEdit(self.fraTop)
        self.txtBulkOrder.setObjectName(_fromUtf8("txtBulkOrder"))
        self.gridLayout.addWidget(self.txtBulkOrder, 0, 1, 1, 1)
        self.lblWallOrder = QLabel(self.fraTop)
        self.lblWallOrder.setObjectName(_fromUtf8("lblWallOrder"))
        self.gridLayout.addWidget(self.lblWallOrder, 1, 0, 1, 1)
        self.txtWallOrder = QLineEdit(self.fraTop)
        self.txtWallOrder.setObjectName(_fromUtf8("txtWallOrder"))
        self.gridLayout.addWidget(self.txtWallOrder, 1, 1, 1, 1)
        self.lblTankOrder = QLabel(self.fraTop)
        self.lblTankOrder.setObjectName(_fromUtf8("lblTankOrder"))
        self.gridLayout.addWidget(self.lblTankOrder, 2, 0, 1, 1)
        self.txtTankOrder = QLineEdit(self.fraTop)
        self.txtTankOrder.setObjectName(_fromUtf8("txtTankOrder"))
        self.gridLayout.addWidget(self.txtTankOrder, 2, 1, 1, 1)
        self.lblGlobalBulk = QLabel(self.fraTop)
        self.lblGlobalBulk.setObjectName(_fromUtf8("lblGlobalBulk"))
        self.gridLayout.addWidget(self.lblGlobalBulk, 3, 0, 1, 1)
        self.txtGlobalBulk = QLineEdit(self.fraTop)
        self.txtGlobalBulk.setObjectName(_fromUtf8("txtGlobalBulk"))
        self.gridLayout.addWidget(self.txtGlobalBulk, 3, 1, 1, 1)
        self.lblGlobalWall = QLabel(self.fraTop)
        self.lblGlobalWall.setObjectName(_fromUtf8("lblGlobalWall"))
        self.gridLayout.addWidget(self.lblGlobalWall, 4, 0, 1, 1)
        self.txtGlobalWall = QLineEdit(self.fraTop)
        self.txtGlobalWall.setObjectName(_fromUtf8("txtGlobalWall"))
        self.gridLayout.addWidget(self.txtGlobalWall, 4, 1, 1, 1)
        self.lblLimiting = QLabel(self.fraTop)
        self.lblLimiting.setObjectName(_fromUtf8("lblLimiting"))
        self.gridLayout.addWidget(self.lblLimiting, 5, 0, 1, 1)
        self.txtLimiting = QLineEdit(self.fraTop)
        self.txtLimiting.setObjectName(_fromUtf8("txtLimiting"))
        self.gridLayout.addWidget(self.txtLimiting, 5, 1, 1, 1)
        self.lblCorrelation = QLabel(self.fraTop)
        self.lblCorrelation.setObjectName(_fromUtf8("lblCorrelation"))
        self.gridLayout.addWidget(self.lblCorrelation, 6, 0, 1, 1)
        self.txtCorrelation = QLineEdit(self.fraTop)
        self.txtCorrelation.setObjectName(_fromUtf8("txtCorrelation"))
        self.gridLayout.addWidget(self.txtCorrelation, 6, 1, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(136, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmReactionsOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmReactionsOptions)
        QtCore.QMetaObject.connectSlotsByName(frmReactionsOptions)

    def retranslateUi(self, frmReactionsOptions):
        frmReactionsOptions.setWindowTitle(_translate("frmReactionsOptions", "EPANET Reactions Options", None))
        self.lblBulkOrder.setText(_translate("frmReactionsOptions", "Bulk Reaction Order", None))
        self.lblWallOrder.setText(_translate("frmReactionsOptions", "<html><head/><body><p>Wall Reaction Order</p></body></html>", None))
        self.lblTankOrder.setText(_translate("frmReactionsOptions", "Tank Reaction Order", None))
        self.lblGlobalBulk.setText(_translate("frmReactionsOptions", "Global Bulk Coefficient", None))
        self.lblGlobalWall.setText(_translate("frmReactionsOptions", "Global Wall Coefficient", None))
        self.lblLimiting.setText(_translate("frmReactionsOptions", "Limiting Concentration", None))
        self.lblCorrelation.setText(_translate("frmReactionsOptions", "Wall Roughness Correlation", None))
        self.cmdOK.setText(_translate("frmReactionsOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmReactionsOptions", "Cancel", None))

