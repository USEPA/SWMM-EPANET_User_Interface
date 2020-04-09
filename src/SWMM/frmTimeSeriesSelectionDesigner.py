# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmTimeSeriesSelectionDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
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

class Ui_frmTimeSeriesSelection(object):
    def setupUi(self, frmTimeSeriesSelection):
        frmTimeSeriesSelection.setObjectName(_fromUtf8("frmTimeSeriesSelection"))
        frmTimeSeriesSelection.resize(320, 264)
        font = QFont()
        font.setPointSize(10)
        frmTimeSeriesSelection.setFont(font)
        self.centralWidget = QWidget(frmTimeSeriesSelection)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblSpecify = QLabel(self.centralWidget)
        self.lblSpecify.setObjectName(_fromUtf8("lblSpecify"))
        self.verticalLayout.addWidget(self.lblSpecify)
        self.frame = QFrame(self.centralWidget)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QGridLayout(self.frame)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.txtObject = QLineEdit(self.frame)
        self.txtObject.setObjectName(_fromUtf8("txtObject"))
        self.gridLayout.addWidget(self.txtObject, 1, 1, 1, 1)
        self.lblObject = QLabel(self.frame)
        self.lblObject.setObjectName(_fromUtf8("lblObject"))
        self.gridLayout.addWidget(self.lblObject, 1, 0, 1, 1)
        self.lblAxis = QLabel(self.frame)
        self.lblAxis.setObjectName(_fromUtf8("lblAxis"))
        self.gridLayout.addWidget(self.lblAxis, 4, 0, 1, 1)
        self.lblType = QLabel(self.frame)
        self.lblType.setObjectName(_fromUtf8("lblType"))
        self.gridLayout.addWidget(self.lblType, 0, 0, 1, 1)
        self.cboObjectType = QComboBox(self.frame)
        self.cboObjectType.setObjectName(_fromUtf8("cboObjectType"))
        self.gridLayout.addWidget(self.cboObjectType, 0, 1, 1, 1)
        self.lblLegend = QLabel(self.frame)
        self.lblLegend.setObjectName(_fromUtf8("lblLegend"))
        self.gridLayout.addWidget(self.lblLegend, 3, 0, 1, 1)
        self.cboVariable = QComboBox(self.frame)
        self.cboVariable.setObjectName(_fromUtf8("cboVariable"))
        self.gridLayout.addWidget(self.cboVariable, 2, 1, 1, 1)
        self.lblVariable = QLabel(self.frame)
        self.lblVariable.setObjectName(_fromUtf8("lblVariable"))
        self.gridLayout.addWidget(self.lblVariable, 2, 0, 1, 1)
        self.txtLegend = QLineEdit(self.frame)
        self.txtLegend.setObjectName(_fromUtf8("txtLegend"))
        self.gridLayout.addWidget(self.txtLegend, 3, 1, 1, 1)
        self.fraLeftRight = QFrame(self.frame)
        self.fraLeftRight.setFrameShape(QFrame.StyledPanel)
        self.fraLeftRight.setFrameShadow(QFrame.Raised)
        self.fraLeftRight.setObjectName(_fromUtf8("fraLeftRight"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraLeftRight)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rbnLeft = QRadioButton(self.fraLeftRight)
        self.rbnLeft.setObjectName(_fromUtf8("rbnLeft"))
        self.horizontalLayout_2.addWidget(self.rbnLeft)
        self.rbnRight = QRadioButton(self.fraLeftRight)
        self.rbnRight.setObjectName(_fromUtf8("rbnRight"))
        self.horizontalLayout_2.addWidget(self.rbnRight)
        self.gridLayout.addWidget(self.fraLeftRight, 4, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmTimeSeriesSelection.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmTimeSeriesSelection)
        QtCore.QMetaObject.connectSlotsByName(frmTimeSeriesSelection)

    def retranslateUi(self, frmTimeSeriesSelection):
        frmTimeSeriesSelection.setWindowTitle(_translate("frmTimeSeriesSelection", "SWMM Data Series Plot Selection", None))
        self.lblSpecify.setText(_translate("frmTimeSeriesSelection", "Specify the object and variable to plot:", None))
        self.lblObject.setText(_translate("frmTimeSeriesSelection", "Object Name", None))
        self.lblAxis.setText(_translate("frmTimeSeriesSelection", "Axis", None))
        self.lblType.setText(_translate("frmTimeSeriesSelection", "Object Type", None))
        self.lblLegend.setText(_translate("frmTimeSeriesSelection", "Legend Label", None))
        self.lblVariable.setText(_translate("frmTimeSeriesSelection", "Variable", None))
        self.rbnLeft.setText(_translate("frmTimeSeriesSelection", "Left", None))
        self.rbnRight.setText(_translate("frmTimeSeriesSelection", "Right", None))
        self.cmdOK.setText(_translate("frmTimeSeriesSelection", "OK", None))
        self.cmdCancel.setText(_translate("frmTimeSeriesSelection", "Cancel", None))

