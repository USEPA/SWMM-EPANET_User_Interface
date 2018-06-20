# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmQualityOptionsDesigner.ui'
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

class Ui_frmQualityOptions(object):
    def setupUi(self, frmQualityOptions):
        frmQualityOptions.setObjectName(_fromUtf8("frmQualityOptions"))
        frmQualityOptions.resize(287, 311)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmQualityOptions.setFont(font)
        self.centralWidget = QWidget(frmQualityOptions)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbxQuality = QGroupBox(self.centralWidget)
        self.gbxQuality.setObjectName(_fromUtf8("gbxQuality"))
        self.gridLayout_2 = QGridLayout(self.gbxQuality)
        # self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.rbnTrace = QRadioButton(self.gbxQuality)
        self.rbnTrace.setObjectName(_fromUtf8("rbnTrace"))
        self.gridLayout_2.addWidget(self.rbnTrace, 1, 1, 1, 1)
        self.rbnNone = QRadioButton(self.gbxQuality)
        self.rbnNone.setObjectName(_fromUtf8("rbnNone"))
        self.gridLayout_2.addWidget(self.rbnNone, 0, 0, 1, 1)
        self.rbnAge = QRadioButton(self.gbxQuality)
        self.rbnAge.setObjectName(_fromUtf8("rbnAge"))
        self.gridLayout_2.addWidget(self.rbnAge, 0, 1, 1, 1)
        self.rbnChemical = QRadioButton(self.gbxQuality)
        self.rbnChemical.setObjectName(_fromUtf8("rbnChemical"))
        self.gridLayout_2.addWidget(self.rbnChemical, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.gbxQuality)
        self.fraMiddle = QFrame(self.centralWidget)
        self.fraMiddle.setFrameShape(QFrame.StyledPanel)
        self.fraMiddle.setFrameShadow(QFrame.Raised)
        self.fraMiddle.setObjectName(_fromUtf8("fraMiddle"))
        self.gridLayout = QGridLayout(self.fraMiddle)
        # self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblTolerance = QLabel(self.fraMiddle)
        self.lblTolerance.setObjectName(_fromUtf8("lblTolerance"))
        self.gridLayout.addWidget(self.lblTolerance, 4, 0, 1, 1)
        self.txtTraceNode = QLineEdit(self.fraMiddle)
        self.txtTraceNode.setObjectName(_fromUtf8("txtTraceNode"))
        self.gridLayout.addWidget(self.txtTraceNode, 3, 1, 1, 1)
        self.txtTolerance = QLineEdit(self.fraMiddle)
        self.txtTolerance.setObjectName(_fromUtf8("txtTolerance"))
        self.gridLayout.addWidget(self.txtTolerance, 4, 1, 1, 1)
        self.lblTraceNode = QLabel(self.fraMiddle)
        self.lblTraceNode.setObjectName(_fromUtf8("lblTraceNode"))
        self.gridLayout.addWidget(self.lblTraceNode, 3, 0, 1, 1)
        self.txtChemicalName = QLineEdit(self.fraMiddle)
        self.txtChemicalName.setObjectName(_fromUtf8("txtChemicalName"))
        self.gridLayout.addWidget(self.txtChemicalName, 0, 1, 1, 1)
        self.lblChemicalName = QLabel(self.fraMiddle)
        self.lblChemicalName.setObjectName(_fromUtf8("lblChemicalName"))
        self.gridLayout.addWidget(self.lblChemicalName, 0, 0, 1, 1)
        self.lblDiffusivity = QLabel(self.fraMiddle)
        self.lblDiffusivity.setObjectName(_fromUtf8("lblDiffusivity"))
        self.gridLayout.addWidget(self.lblDiffusivity, 2, 0, 1, 1)
        self.lblMassUnits = QLabel(self.fraMiddle)
        self.lblMassUnits.setObjectName(_fromUtf8("lblMassUnits"))
        self.gridLayout.addWidget(self.lblMassUnits, 1, 0, 1, 1)
        self.txtMassUnits = QLineEdit(self.fraMiddle)
        self.txtMassUnits.setObjectName(_fromUtf8("txtMassUnits"))
        self.gridLayout.addWidget(self.txtMassUnits, 1, 1, 1, 1)
        self.txtDiffusivity = QLineEdit(self.fraMiddle)
        self.txtDiffusivity.setObjectName(_fromUtf8("txtDiffusivity"))
        self.gridLayout.addWidget(self.txtDiffusivity, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.fraMiddle)
        self.frame_2 = QFrame(self.centralWidget)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QSpacerItem(84, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QPushButton(self.frame_2)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.frame_2)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.frame_2)
        frmQualityOptions.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmQualityOptions)
        QtCore.QMetaObject.connectSlotsByName(frmQualityOptions)

    def retranslateUi(self, frmQualityOptions):
        frmQualityOptions.setWindowTitle(_translate("frmQualityOptions", "EPANET Quality Options", None))
        self.gbxQuality.setTitle(_translate("frmQualityOptions", "Analysis Type", None))
        self.rbnTrace.setText(_translate("frmQualityOptions", "Trace", None))
        self.rbnNone.setText(_translate("frmQualityOptions", "None", None))
        self.rbnAge.setText(_translate("frmQualityOptions", "Age", None))
        self.rbnChemical.setText(_translate("frmQualityOptions", "Chemical", None))
        self.lblTolerance.setText(_translate("frmQualityOptions", "Quality Tolerance", None))
        self.lblTraceNode.setText(_translate("frmQualityOptions", "Trace Node", None))
        self.lblChemicalName.setText(_translate("frmQualityOptions", "<html><head/><body><p>Chemical Name</p></body></html>", None))
        self.lblDiffusivity.setText(_translate("frmQualityOptions", "Relative Diffusivity", None))
        self.lblMassUnits.setText(_translate("frmQualityOptions", "Mass Units", None))
        self.cmdOK.setText(_translate("frmQualityOptions", "OK", None))
        self.cmdCancel.setText(_translate("frmQualityOptions", "Cancel", None))

