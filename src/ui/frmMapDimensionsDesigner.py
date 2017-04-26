# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmMapDimensionsDesigner.ui'
#
# Created: Tue Nov 15 16:02:58 2016
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

class Ui_frmMapDimensionsDesigner(object):
    def setupUi(self, frmMapDimensionsDesigner):
        frmMapDimensionsDesigner.setObjectName(_fromUtf8("frmMapDimensionsDesigner"))
        frmMapDimensionsDesigner.resize(439, 185)
        self.gridLayout = QtGui.QGridLayout(frmMapDimensionsDesigner)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gbUpleft = QtGui.QGroupBox(frmMapDimensionsDesigner)
        self.gbUpleft.setObjectName(_fromUtf8("gbUpleft"))
        self.formLayout = QtGui.QFormLayout(self.gbUpleft)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblLLx = QtGui.QLabel(self.gbUpleft)
        self.lblLLx.setObjectName(_fromUtf8("lblLLx"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblLLx)
        self.txtULx = QtGui.QLineEdit(self.gbUpleft)
        self.txtULx.setObjectName(_fromUtf8("txtULx"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtULx)
        self.lblLLy = QtGui.QLabel(self.gbUpleft)
        self.lblLLy.setObjectName(_fromUtf8("lblLLy"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblLLy)
        self.txtULy = QtGui.QLineEdit(self.gbUpleft)
        self.txtULy.setObjectName(_fromUtf8("txtULy"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtULy)
        self.gridLayout.addWidget(self.gbUpleft, 0, 0, 1, 2)
        self.gbLowRight = QtGui.QGroupBox(frmMapDimensionsDesigner)
        self.gbLowRight.setObjectName(_fromUtf8("gbLowRight"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbLowRight)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.lblURx = QtGui.QLabel(self.gbLowRight)
        self.lblURx.setObjectName(_fromUtf8("lblURx"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblURx)
        self.txtLRx = QtGui.QLineEdit(self.gbLowRight)
        self.txtLRx.setObjectName(_fromUtf8("txtLRx"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtLRx)
        self.lblURy = QtGui.QLabel(self.gbLowRight)
        self.lblURy.setObjectName(_fromUtf8("lblURy"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblURy)
        self.txtLRy = QtGui.QLineEdit(self.gbLowRight)
        self.txtLRy.setObjectName(_fromUtf8("txtLRy"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtLRy)
        self.gridLayout.addWidget(self.gbLowRight, 0, 2, 1, 2)
        self.gbMapUnits = QtGui.QGroupBox(frmMapDimensionsDesigner)
        self.gbMapUnits.setObjectName(_fromUtf8("gbMapUnits"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbMapUnits)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rdoUnitFeet = QtGui.QRadioButton(self.gbMapUnits)
        self.rdoUnitFeet.setObjectName(_fromUtf8("rdoUnitFeet"))
        self.horizontalLayout.addWidget(self.rdoUnitFeet)
        self.rdoUnitMeters = QtGui.QRadioButton(self.gbMapUnits)
        self.rdoUnitMeters.setObjectName(_fromUtf8("rdoUnitMeters"))
        self.horizontalLayout.addWidget(self.rdoUnitMeters)
        self.rdoUnitDegrees = QtGui.QRadioButton(self.gbMapUnits)
        self.rdoUnitDegrees.setObjectName(_fromUtf8("rdoUnitDegrees"))
        self.horizontalLayout.addWidget(self.rdoUnitDegrees)
        self.rdoUnitNone = QtGui.QRadioButton(self.gbMapUnits)
        self.rdoUnitNone.setObjectName(_fromUtf8("rdoUnitNone"))
        self.horizontalLayout.addWidget(self.rdoUnitNone)
        self.gridLayout.addWidget(self.gbMapUnits, 1, 0, 1, 4)
        self.btnAutoSize = QtGui.QPushButton(frmMapDimensionsDesigner)
        self.btnAutoSize.setObjectName(_fromUtf8("btnAutoSize"))
        self.gridLayout.addWidget(self.btnAutoSize, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(frmMapDimensionsDesigner)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 2)
        self.btnHelp = QtGui.QPushButton(frmMapDimensionsDesigner)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.gridLayout.addWidget(self.btnHelp, 2, 3, 1, 1)

        self.retranslateUi(frmMapDimensionsDesigner)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), frmMapDimensionsDesigner.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), frmMapDimensionsDesigner.reject)
        QtCore.QMetaObject.connectSlotsByName(frmMapDimensionsDesigner)
        frmMapDimensionsDesigner.setTabOrder(self.txtULx, self.txtULy)
        frmMapDimensionsDesigner.setTabOrder(self.txtULy, self.txtLRx)
        frmMapDimensionsDesigner.setTabOrder(self.txtLRx, self.txtLRy)
        frmMapDimensionsDesigner.setTabOrder(self.txtLRy, self.rdoUnitFeet)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitFeet, self.rdoUnitMeters)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitMeters, self.rdoUnitDegrees)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitDegrees, self.rdoUnitNone)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitNone, self.btnAutoSize)
        frmMapDimensionsDesigner.setTabOrder(self.btnAutoSize, self.btnHelp)

    def retranslateUi(self, frmMapDimensionsDesigner):
        frmMapDimensionsDesigner.setWindowTitle(_translate("frmMapDimensionsDesigner", "Map Dimensions", None))
        self.gbUpleft.setTitle(_translate("frmMapDimensionsDesigner", "Upper Left", None))
        self.lblLLx.setText(_translate("frmMapDimensionsDesigner", "X-coordinate:", None))
        self.lblLLy.setText(_translate("frmMapDimensionsDesigner", "Y-coordinate:", None))
        self.gbLowRight.setTitle(_translate("frmMapDimensionsDesigner", "Lower Right", None))
        self.lblURx.setText(_translate("frmMapDimensionsDesigner", "X-coordinate:", None))
        self.lblURy.setText(_translate("frmMapDimensionsDesigner", "Y-coordinate:", None))
        self.gbMapUnits.setTitle(_translate("frmMapDimensionsDesigner", "Map Units", None))
        self.rdoUnitFeet.setText(_translate("frmMapDimensionsDesigner", "Feet", None))
        self.rdoUnitMeters.setText(_translate("frmMapDimensionsDesigner", "Meters", None))
        self.rdoUnitDegrees.setText(_translate("frmMapDimensionsDesigner", "Degrees", None))
        self.rdoUnitNone.setText(_translate("frmMapDimensionsDesigner", "None", None))
        self.btnAutoSize.setText(_translate("frmMapDimensionsDesigner", "Auto-Size", None))
        self.btnHelp.setText(_translate("frmMapDimensionsDesigner", "Help", None))

