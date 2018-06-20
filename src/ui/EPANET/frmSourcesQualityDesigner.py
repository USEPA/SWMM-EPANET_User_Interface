# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmSourcesQualityDesigner.ui'
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

class Ui_frmSourcesQuality(object):
    def setupUi(self, frmSourcesQuality):
        frmSourcesQuality.setObjectName(_fromUtf8("frmSourcesQuality"))
        frmSourcesQuality.resize(295, 265)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmSourcesQuality.setFont(font)
        self.centralWidget = QWidget(frmSourcesQuality)
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
        self.lblQuality = QLabel(self.fraTop)
        self.lblQuality.setObjectName(_fromUtf8("lblQuality"))
        self.gridLayout.addWidget(self.lblQuality, 0, 0, 1, 1)
        self.txtQuality = QLineEdit(self.fraTop)
        self.txtQuality.setObjectName(_fromUtf8("txtQuality"))
        self.gridLayout.addWidget(self.txtQuality, 0, 1, 1, 1)
        self.lblPattern = QLabel(self.fraTop)
        self.lblPattern.setObjectName(_fromUtf8("lblPattern"))
        self.gridLayout.addWidget(self.lblPattern, 1, 0, 1, 1)
        self.txtPattern = QLineEdit(self.fraTop)
        self.txtPattern.setObjectName(_fromUtf8("txtPattern"))
        self.gridLayout.addWidget(self.txtPattern, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
        self.gbxType = QGroupBox(self.centralWidget)
        self.gbxType.setObjectName(_fromUtf8("gbxType"))
        self.gridLayout_2 = QGridLayout(self.gbxType)
        # self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.rbnConcentration = QRadioButton(self.gbxType)
        self.rbnConcentration.setObjectName(_fromUtf8("rbnConcentration"))
        self.gridLayout_2.addWidget(self.rbnConcentration, 0, 0, 1, 1)
        self.rbnSetPoint = QRadioButton(self.gbxType)
        self.rbnSetPoint.setObjectName(_fromUtf8("rbnSetPoint"))
        self.gridLayout_2.addWidget(self.rbnSetPoint, 0, 1, 1, 1)
        self.rbnMass = QRadioButton(self.gbxType)
        self.rbnMass.setObjectName(_fromUtf8("rbnMass"))
        self.gridLayout_2.addWidget(self.rbnMass, 1, 0, 1, 1)
        self.rbnFlow = QRadioButton(self.gbxType)
        self.rbnFlow.setObjectName(_fromUtf8("rbnFlow"))
        self.gridLayout_2.addWidget(self.rbnFlow, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.gbxType)
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
        frmSourcesQuality.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmSourcesQuality)
        QtCore.QMetaObject.connectSlotsByName(frmSourcesQuality)

    def retranslateUi(self, frmSourcesQuality):
        frmSourcesQuality.setWindowTitle(_translate("frmSourcesQuality", "EPANET Source Editor", None))
        self.lblQuality.setText(_translate("frmSourcesQuality", "Source Quality", None))
        self.lblPattern.setText(_translate("frmSourcesQuality", "Time Pattern", None))
        self.gbxType.setTitle(_translate("frmSourcesQuality", "Source Type", None))
        self.rbnConcentration.setText(_translate("frmSourcesQuality", "Concentration", None))
        self.rbnSetPoint.setText(_translate("frmSourcesQuality", "Setpoint Booster", None))
        self.rbnMass.setText(_translate("frmSourcesQuality", "MassBooster", None))
        self.rbnFlow.setText(_translate("frmSourcesQuality", "Flow Paced Booster", None))
        self.cmdOK.setText(_translate("frmSourcesQuality", "OK", None))
        self.cmdCancel.setText(_translate("frmSourcesQuality", "Cancel", None))

