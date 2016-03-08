# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmCurveEditorDesigner.ui'
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

class Ui_frmCurveEditor(object):
    def setupUi(self, frmCurveEditor):
        frmCurveEditor.setObjectName(_fromUtf8("frmCurveEditor"))
        frmCurveEditor.resize(571, 383)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCurveEditor.setFont(font)
        self.centralWidget = QtGui.QWidget(frmCurveEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fraParms = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraParms.sizePolicy().hasHeightForWidth())
        self.fraParms.setSizePolicy(sizePolicy)
        self.fraParms.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraParms.setFrameShadow(QtGui.QFrame.Raised)
        self.fraParms.setObjectName(_fromUtf8("fraParms"))
        self.gridLayout = QtGui.QGridLayout(self.fraParms)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblEquation = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblEquation.setFont(font)
        self.lblEquation.setObjectName(_fromUtf8("lblEquation"))
        self.gridLayout.addWidget(self.lblEquation, 3, 0, 1, 6)
        self.lblDescription = QtGui.QLabel(self.fraParms)
        self.lblDescription.setObjectName(_fromUtf8("lblDescription"))
        self.gridLayout.addWidget(self.lblDescription, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(325, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.lblCurveType = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCurveType.setFont(font)
        self.lblCurveType.setObjectName(_fromUtf8("lblCurveType"))
        self.gridLayout.addWidget(self.lblCurveType, 2, 0, 1, 2)
        self.txtCurveID = QtGui.QLineEdit(self.fraParms)
        self.txtCurveID.setObjectName(_fromUtf8("txtCurveID"))
        self.gridLayout.addWidget(self.txtCurveID, 0, 1, 1, 4)
        self.lblCurveID = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCurveID.setFont(font)
        self.lblCurveID.setObjectName(_fromUtf8("lblCurveID"))
        self.gridLayout.addWidget(self.lblCurveID, 0, 0, 1, 1)
        self.txtDescription = QtGui.QLineEdit(self.fraParms)
        self.txtDescription.setObjectName(_fromUtf8("txtDescription"))
        self.gridLayout.addWidget(self.txtDescription, 1, 1, 1, 5)
        self.comboBox = QtGui.QComboBox(self.fraParms)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(364, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 3)
        self.verticalLayout.addWidget(self.fraParms)
        self.tblMult = QtGui.QTableWidget(self.centralWidget)
        self.tblMult.setCornerButtonEnabled(False)
        self.tblMult.setRowCount(50)
        self.tblMult.setColumnCount(2)
        self.tblMult.setObjectName(_fromUtf8("tblMult"))
        item = QtGui.QTableWidgetItem()
        self.tblMult.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblMult.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblMult.setHorizontalHeaderItem(1, item)
        self.tblMult.horizontalHeader().setVisible(True)
        self.tblMult.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tblMult)
        self.fraOKCancel = QtGui.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtGui.QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(99, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cmdOK = QtGui.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtGui.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmCurveEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCurveEditor)
        QtCore.QMetaObject.connectSlotsByName(frmCurveEditor)

    def retranslateUi(self, frmCurveEditor):
        frmCurveEditor.setWindowTitle(_translate("frmCurveEditor", "EPANET Curve Editor", None))
        self.lblEquation.setText(_translate("frmCurveEditor", "Equation:", None))
        self.lblDescription.setText(_translate("frmCurveEditor", "<html><head/><body><p>Description</p></body></html>", None))
        self.lblCurveType.setText(_translate("frmCurveEditor", "Curve Type", None))
        self.lblCurveID.setText(_translate("frmCurveEditor", "Curve ID", None))
        item = self.tblMult.verticalHeaderItem(0)
        item.setText(_translate("frmCurveEditor", "Flow", None))
        item = self.tblMult.horizontalHeaderItem(0)
        item.setText(_translate("frmCurveEditor", "Flow", None))
        item = self.tblMult.horizontalHeaderItem(1)
        item.setText(_translate("frmCurveEditor", "Head", None))
        self.cmdOK.setText(_translate("frmCurveEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmCurveEditor", "Cancel", None))

