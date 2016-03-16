# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmSourcesQualityDesigner.ui'
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

class Ui_frmSourcesQuality(object):
    def setupUi(self, frmSourcesQuality):
        frmSourcesQuality.setObjectName(_fromUtf8("frmSourcesQuality"))
        frmSourcesQuality.resize(295, 265)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmSourcesQuality.setFont(font)
        self.centralWidget = QtGui.QWidget(frmSourcesQuality)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraTop = QtGui.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtGui.QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.gridLayout = QtGui.QGridLayout(self.fraTop)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblQuality = QtGui.QLabel(self.fraTop)
        self.lblQuality.setObjectName(_fromUtf8("lblQuality"))
        self.gridLayout.addWidget(self.lblQuality, 0, 0, 1, 1)
        self.txtQuality = QtGui.QLineEdit(self.fraTop)
        self.txtQuality.setObjectName(_fromUtf8("txtQuality"))
        self.gridLayout.addWidget(self.txtQuality, 0, 1, 1, 1)
        self.lblPattern = QtGui.QLabel(self.fraTop)
        self.lblPattern.setObjectName(_fromUtf8("lblPattern"))
        self.gridLayout.addWidget(self.lblPattern, 1, 0, 1, 1)
        self.txtPattern = QtGui.QLineEdit(self.fraTop)
        self.txtPattern.setObjectName(_fromUtf8("txtPattern"))
        self.gridLayout.addWidget(self.txtPattern, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.fraTop)
        self.gbxType = QtGui.QGroupBox(self.centralWidget)
        self.gbxType.setObjectName(_fromUtf8("gbxType"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbxType)
        self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.rbnConcentration = QtGui.QRadioButton(self.gbxType)
        self.rbnConcentration.setObjectName(_fromUtf8("rbnConcentration"))
        self.gridLayout_2.addWidget(self.rbnConcentration, 0, 0, 1, 1)
        self.rbnSetPoint = QtGui.QRadioButton(self.gbxType)
        self.rbnSetPoint.setObjectName(_fromUtf8("rbnSetPoint"))
        self.gridLayout_2.addWidget(self.rbnSetPoint, 0, 1, 1, 1)
        self.rbnMass = QtGui.QRadioButton(self.gbxType)
        self.rbnMass.setObjectName(_fromUtf8("rbnMass"))
        self.gridLayout_2.addWidget(self.rbnMass, 1, 0, 1, 1)
        self.rbnFlow = QtGui.QRadioButton(self.gbxType)
        self.rbnFlow.setObjectName(_fromUtf8("rbnFlow"))
        self.gridLayout_2.addWidget(self.rbnFlow, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.gbxType)
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

