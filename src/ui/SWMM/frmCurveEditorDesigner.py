# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmCurveEditorDesigner.ui'
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
        frmCurveEditor.resize(588, 338)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCurveEditor.setFont(font)
        self.centralWidget = QtGui.QWidget(frmCurveEditor)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.fraParms = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
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
        self.cboCurveType = QtGui.QComboBox(self.fraParms)
        self.cboCurveType.setObjectName(_fromUtf8("cboCurveType"))
        self.gridLayout.addWidget(self.cboCurveType, 0, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.lblDescription = QtGui.QLabel(self.fraParms)
        self.lblDescription.setObjectName(_fromUtf8("lblDescription"))
        self.gridLayout.addWidget(self.lblDescription, 4, 0, 1, 1)
        self.txtCurveName = QtGui.QLineEdit(self.fraParms)
        self.txtCurveName.setObjectName(_fromUtf8("txtCurveName"))
        self.gridLayout.addWidget(self.txtCurveName, 0, 1, 1, 3)
        self.lblCurveType = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCurveType.setFont(font)
        self.lblCurveType.setObjectName(_fromUtf8("lblCurveType"))
        self.gridLayout.addWidget(self.lblCurveType, 0, 5, 1, 1)
        self.txtDescription = QtGui.QLineEdit(self.fraParms)
        self.txtDescription.setObjectName(_fromUtf8("txtDescription"))
        self.gridLayout.addWidget(self.txtDescription, 4, 1, 1, 6)
        self.lblCurveID = QtGui.QLabel(self.fraParms)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCurveID.setFont(font)
        self.lblCurveID.setObjectName(_fromUtf8("lblCurveID"))
        self.gridLayout.addWidget(self.lblCurveID, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.fraParms)
        self.fraBottom = QtGui.QFrame(self.centralWidget)
        self.fraBottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraBottom.setFrameShadow(QtGui.QFrame.Raised)
        self.fraBottom.setObjectName(_fromUtf8("fraBottom"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.fraBottom)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
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
        self.horizontalLayout_2.addWidget(self.tblMult)
        self.fraRight = QtGui.QFrame(self.fraBottom)
        self.fraRight.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fraRight.setFrameShadow(QtGui.QFrame.Raised)
        self.fraRight.setObjectName(_fromUtf8("fraRight"))
        self.verticalLayout = QtGui.QVBoxLayout(self.fraRight)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem1 = QtGui.QSpacerItem(20, 151, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.fraOKCancel = QtGui.QFrame(self.fraRight)
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
        self.horizontalLayout_2.addWidget(self.fraRight)
        self.verticalLayout_2.addWidget(self.fraBottom)
        frmCurveEditor.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCurveEditor)
        QtCore.QMetaObject.connectSlotsByName(frmCurveEditor)

    def retranslateUi(self, frmCurveEditor):
        frmCurveEditor.setWindowTitle(_translate("frmCurveEditor", "SWMM Curves", None))
        self.lblDescription.setText(_translate("frmCurveEditor", "<html><head/><body><p>Description</p></body></html>", None))
        self.lblCurveType.setText(_translate("frmCurveEditor", "Curve Type", None))
        self.lblCurveID.setText(_translate("frmCurveEditor", "Curve Name", None))
        item = self.tblMult.horizontalHeaderItem(0)
        item.setText(_translate("frmCurveEditor", "Flow", None))
        item = self.tblMult.horizontalHeaderItem(1)
        item.setText(_translate("frmCurveEditor", "Head", None))
        self.cmdOK.setText(_translate("frmCurveEditor", "OK", None))
        self.cmdCancel.setText(_translate("frmCurveEditor", "Cancel", None))

