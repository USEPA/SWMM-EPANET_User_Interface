# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SWMM\frmCurveEditorDesigner.ui'
#
# Created: Tue Dec 20 18:06:02 2016
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

class Ui_frmCurveEditor(object):
    def setupUi(self, frmCurveEditor):
        frmCurveEditor.setObjectName(_fromUtf8("frmCurveEditor"))
        frmCurveEditor.resize(587, 448)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCurveEditor.setFont(font)
        self.centralWidget = QtGui.QWidget(frmCurveEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraParms = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fraParms.sizePolicy().hasHeightForWidth())
        self.fraParms.setSizePolicy(sizePolicy)
        self.fraParms.setMaximumSize(QtCore.QSize(16777215, 250))
        self.fraParms.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraParms.setFrameShadow(QtGui.QFrame.Raised)
        self.fraParms.setObjectName(_fromUtf8("fraParms"))
        self.gridLayout = QtGui.QGridLayout(self.fraParms)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCurveID = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCurveID.setFont(font)
        self.lblCurveID.setObjectName(_fromUtf8("lblCurveID"))
        self.gridLayout.addWidget(self.lblCurveID, 0, 0, 1, 1)
        self.lblCurveType = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCurveType.setFont(font)
        self.lblCurveType.setObjectName(_fromUtf8("lblCurveType"))
        self.gridLayout.addWidget(self.lblCurveType, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(231, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.txtCurveID = QtGui.QLineEdit(self.fraParms)
        self.txtCurveID.setObjectName(_fromUtf8("txtCurveID"))
        self.gridLayout.addWidget(self.txtCurveID, 1, 0, 1, 1)
        self.cboCurveType = QtGui.QComboBox(self.fraParms)
        self.cboCurveType.setObjectName(_fromUtf8("cboCurveType"))
        self.gridLayout.addWidget(self.cboCurveType, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(231, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.lblDescription = QtGui.QLabel(self.fraParms)
        self.lblDescription.setObjectName(_fromUtf8("lblDescription"))
        self.gridLayout.addWidget(self.lblDescription, 2, 0, 1, 1)
        self.txtDescription = QtGui.QLineEdit(self.fraParms)
        self.txtDescription.setObjectName(_fromUtf8("txtDescription"))
        self.gridLayout.addWidget(self.txtDescription, 3, 0, 1, 3)
        self.verticalLayout_2.addWidget(self.fraParms)
        self.fraBottom = QtGui.QFrame(self.centralWidget)
        self.fraBottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraBottom.setFrameShadow(QtGui.QFrame.Raised)
        self.fraBottom.setObjectName(_fromUtf8("fraBottom"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fraBottom)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btnSave = QtGui.QPushButton(self.fraBottom)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.gridLayout_2.addWidget(self.btnSave, 1, 1, 1, 1)
        self.btnHelp = QtGui.QPushButton(self.fraBottom)
        self.btnHelp.setObjectName(_fromUtf8("btnHelp"))
        self.gridLayout_2.addWidget(self.btnHelp, 1, 4, 1, 1)
        self.cmdOK = QtGui.QPushButton(self.fraBottom)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.gridLayout_2.addWidget(self.cmdOK, 1, 2, 1, 1)
        self.btnLoad = QtGui.QPushButton(self.fraBottom)
        self.btnLoad.setObjectName(_fromUtf8("btnLoad"))
        self.gridLayout_2.addWidget(self.btnLoad, 1, 0, 1, 1)
        self.cmdCancel = QtGui.QPushButton(self.fraBottom)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.gridLayout_2.addWidget(self.cmdCancel, 1, 3, 1, 1)
        self.tblMult = QtGui.QTableWidget(self.fraBottom)
        self.tblMult.setCornerButtonEnabled(False)
        self.tblMult.setRowCount(100)
        self.tblMult.setColumnCount(2)
        self.tblMult.setObjectName(_fromUtf8("tblMult"))
        item = QtGui.QTableWidgetItem()
        self.tblMult.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblMult.setHorizontalHeaderItem(1, item)
        self.tblMult.horizontalHeader().setVisible(True)
        self.tblMult.verticalHeader().setVisible(True)
        self.gridLayout_2.addWidget(self.tblMult, 0, 0, 1, 2)
        self.fraRight = QtGui.QFrame(self.fraBottom)
        self.fraRight.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraRight.setFrameShadow(QtGui.QFrame.Raised)
        self.fraRight.setObjectName(_fromUtf8("fraRight"))
        self.gridLayout_2.addWidget(self.fraRight, 0, 2, 1, 3)
        self.verticalLayout_2.addWidget(self.fraBottom)
        frmCurveEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCurveEditor)
        QtCore.QMetaObject.connectSlotsByName(frmCurveEditor)

    def retranslateUi(self, frmCurveEditor):
        frmCurveEditor.setWindowTitle(_translate("frmCurveEditor", "SWMM Curves", None))
        self.lblCurveID.setText(_translate("frmCurveEditor", "Curve Name", None))
        self.lblCurveType.setText(_translate("frmCurveEditor", "Pump Type", None))
        self.lblDescription.setText(_translate("frmCurveEditor", "<html><head/><body><p>Description</p></body></html>", None))
        self.btnSave.setText(_translate("frmCurveEditor", "Save...", None))
        self.btnHelp.setText(_translate("frmCurveEditor", "Help", None))
        self.cmdOK.setText(_translate("frmCurveEditor", "OK", None))
        self.btnLoad.setText(_translate("frmCurveEditor", "Load...", None))
        self.cmdCancel.setText(_translate("frmCurveEditor", "Cancel", None))
        item = self.tblMult.horizontalHeaderItem(0)
        item.setText(_translate("frmCurveEditor", "Flow", None))
        item = self.tblMult.horizontalHeaderItem(1)
        item.setText(_translate("frmCurveEditor", "Head", None))

