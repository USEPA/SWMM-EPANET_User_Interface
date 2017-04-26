# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmMapDimensionsDesigner.ui'
#
# Created: Fri Apr 14 18:46:22 2017
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
        self.gbLowerLeft = QtGui.QGroupBox(frmMapDimensionsDesigner)
        self.gbLowerLeft.setObjectName(_fromUtf8("gbLowerLeft"))
        self.formLayout = QtGui.QFormLayout(self.gbLowerLeft)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblLLx = QtGui.QLabel(self.gbLowerLeft)
        self.lblLLx.setObjectName(_fromUtf8("lblLLx"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblLLx)
        self.txtLLx = QtGui.QLineEdit(self.gbLowerLeft)
        self.txtLLx.setObjectName(_fromUtf8("txtLLx"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtLLx)
        self.lblLLy = QtGui.QLabel(self.gbLowerLeft)
        self.lblLLy.setObjectName(_fromUtf8("lblLLy"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblLLy)
        self.txtLLy = QtGui.QLineEdit(self.gbLowerLeft)
        self.txtLLy.setObjectName(_fromUtf8("txtLLy"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtLLy)
        self.gridLayout.addWidget(self.gbLowerLeft, 0, 0, 1, 2)
        self.gbUpperRight = QtGui.QGroupBox(frmMapDimensionsDesigner)
        self.gbUpperRight.setObjectName(_fromUtf8("gbUpperRight"))
        self.formLayout_2 = QtGui.QFormLayout(self.gbUpperRight)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.lblURx = QtGui.QLabel(self.gbUpperRight)
        self.lblURx.setObjectName(_fromUtf8("lblURx"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblURx)
        self.txtURx = QtGui.QLineEdit(self.gbUpperRight)
        self.txtURx.setObjectName(_fromUtf8("txtURx"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.txtURx)
        self.lblURy = QtGui.QLabel(self.gbUpperRight)
        self.lblURy.setObjectName(_fromUtf8("lblURy"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblURy)
        self.txtURy = QtGui.QLineEdit(self.gbUpperRight)
        self.txtURy.setObjectName(_fromUtf8("txtURy"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.txtURy)
        self.gridLayout.addWidget(self.gbUpperRight, 0, 2, 1, 2)
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
        frmMapDimensionsDesigner.setTabOrder(self.txtLLx, self.txtLLy)
        frmMapDimensionsDesigner.setTabOrder(self.txtLLy, self.txtURx)
        frmMapDimensionsDesigner.setTabOrder(self.txtURx, self.txtURy)
        frmMapDimensionsDesigner.setTabOrder(self.txtURy, self.rdoUnitFeet)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitFeet, self.rdoUnitMeters)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitMeters, self.rdoUnitDegrees)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitDegrees, self.rdoUnitNone)
        frmMapDimensionsDesigner.setTabOrder(self.rdoUnitNone, self.btnAutoSize)
        frmMapDimensionsDesigner.setTabOrder(self.btnAutoSize, self.btnHelp)

    def retranslateUi(self, frmMapDimensionsDesigner):
        frmMapDimensionsDesigner.setWindowTitle(_translate("frmMapDimensionsDesigner", "Map Dimensions", None))
        self.gbLowerLeft.setTitle(_translate("frmMapDimensionsDesigner", "Lower Left", None))
        self.lblLLx.setText(_translate("frmMapDimensionsDesigner", "X-coordinate:", None))
        self.lblLLy.setText(_translate("frmMapDimensionsDesigner", "Y-coordinate:", None))
        self.gbUpperRight.setTitle(_translate("frmMapDimensionsDesigner", "Upper Right", None))
        self.lblURx.setText(_translate("frmMapDimensionsDesigner", "X-coordinate:", None))
        self.lblURy.setText(_translate("frmMapDimensionsDesigner", "Y-coordinate:", None))
        self.gbMapUnits.setTitle(_translate("frmMapDimensionsDesigner", "Map Units", None))
        self.rdoUnitFeet.setText(_translate("frmMapDimensionsDesigner", "Feet", None))
        self.rdoUnitMeters.setText(_translate("frmMapDimensionsDesigner", "Meters", None))
        self.rdoUnitDegrees.setText(_translate("frmMapDimensionsDesigner", "Degrees", None))
        self.rdoUnitNone.setText(_translate("frmMapDimensionsDesigner", "None", None))
        self.btnAutoSize.setText(_translate("frmMapDimensionsDesigner", "Auto-Size", None))
        self.btnHelp.setText(_translate("frmMapDimensionsDesigner", "Help", None))

