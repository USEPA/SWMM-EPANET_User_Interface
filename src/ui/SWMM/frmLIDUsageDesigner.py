# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui-py3qt5\src\ui\SWMM\frmLIDUsageDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmLIDUsage(object):
    def setupUi(self, frmLIDUsage):
        frmLIDUsage.setObjectName("frmLIDUsage")
        frmLIDUsage.resize(691, 410)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmLIDUsage.setFont(font)
        self.centralWidget = QtWidgets.QWidget(frmLIDUsage)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fraTop = QtWidgets.QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraTop.setObjectName("fraTop")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.fraTop)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fraLeft = QtWidgets.QFrame(self.fraTop)
        self.fraLeft.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraLeft.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraLeft.setObjectName("fraLeft")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fraLeft)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.fraTopLeft = QtWidgets.QFrame(self.fraLeft)
        self.fraTopLeft.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraTopLeft.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraTopLeft.setObjectName("fraTopLeft")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.fraTopLeft)
        self.gridLayout_12.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.lblLIDControlName = QtWidgets.QLabel(self.fraTopLeft)
        self.lblLIDControlName.setObjectName("lblLIDControlName")
        self.gridLayout_12.addWidget(self.lblLIDControlName, 0, 0, 1, 1)
        self.cboLIDControl = QtWidgets.QComboBox(self.fraTopLeft)
        self.cboLIDControl.setObjectName("cboLIDControl")
        self.gridLayout_12.addWidget(self.cboLIDControl, 0, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.fraTopLeft)
        self.lblImage = QtWidgets.QLabel(self.fraLeft)
        self.lblImage.setText("")
        self.lblImage.setObjectName("lblImage")
        self.verticalLayout_2.addWidget(self.lblImage)
        self.fraBotLeft = QtWidgets.QFrame(self.fraLeft)
        self.fraBotLeft.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraBotLeft.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraBotLeft.setObjectName("fraBotLeft")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.fraBotLeft)
        self.gridLayout_13.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_13.setSpacing(6)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.lblFile = QtWidgets.QLabel(self.fraBotLeft)
        self.lblFile.setObjectName("lblFile")
        self.gridLayout_13.addWidget(self.lblFile, 0, 0, 1, 1)
        self.btnFile = QtWidgets.QToolButton(self.fraBotLeft)
        self.btnFile.setObjectName("btnFile")
        self.gridLayout_13.addWidget(self.btnFile, 0, 1, 1, 1)
        self.btnClear = QtWidgets.QToolButton(self.fraBotLeft)
        self.btnClear.setObjectName("btnClear")
        self.gridLayout_13.addWidget(self.btnClear, 0, 2, 1, 1)
        self.txtFile = QtWidgets.QLineEdit(self.fraBotLeft)
        self.txtFile.setObjectName("txtFile")
        self.gridLayout_13.addWidget(self.txtFile, 1, 0, 1, 3)
        self.verticalLayout_2.addWidget(self.fraBotLeft)
        self.horizontalLayout_2.addWidget(self.fraLeft)
        self.line = QtWidgets.QFrame(self.fraTop)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.fraRight = QtWidgets.QFrame(self.fraTop)
        self.fraRight.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraRight.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraRight.setObjectName("fraRight")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.fraRight)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cbxFull = QtWidgets.QCheckBox(self.fraRight)
        self.cbxFull.setObjectName("cbxFull")
        self.gridLayout_2.addWidget(self.cbxFull, 0, 0, 1, 2)
        self.lblArea = QtWidgets.QLabel(self.fraRight)
        self.lblArea.setObjectName("lblArea")
        self.gridLayout_2.addWidget(self.lblArea, 1, 0, 1, 1)
        self.txtArea = QtWidgets.QLineEdit(self.fraRight)
        self.txtArea.setObjectName("txtArea")
        self.gridLayout_2.addWidget(self.txtArea, 1, 1, 1, 1)
        self.lblUnits = QtWidgets.QLabel(self.fraRight)
        self.lblUnits.setObjectName("lblUnits")
        self.gridLayout_2.addWidget(self.lblUnits, 2, 0, 1, 1)
        self.spxUnits = QtWidgets.QSpinBox(self.fraRight)
        self.spxUnits.setObjectName("spxUnits")
        self.gridLayout_2.addWidget(self.spxUnits, 2, 1, 1, 1)
        self.lblOccupied = QtWidgets.QLabel(self.fraRight)
        self.lblOccupied.setObjectName("lblOccupied")
        self.gridLayout_2.addWidget(self.lblOccupied, 3, 0, 1, 1)
        self.lblPercent = QtWidgets.QLabel(self.fraRight)
        self.lblPercent.setObjectName("lblPercent")
        self.gridLayout_2.addWidget(self.lblPercent, 3, 1, 1, 1)
        self.lblWidth = QtWidgets.QLabel(self.fraRight)
        self.lblWidth.setObjectName("lblWidth")
        self.gridLayout_2.addWidget(self.lblWidth, 4, 0, 1, 1)
        self.txtWidth = QtWidgets.QLineEdit(self.fraRight)
        self.txtWidth.setObjectName("txtWidth")
        self.gridLayout_2.addWidget(self.txtWidth, 4, 1, 1, 1)
        self.lblSat = QtWidgets.QLabel(self.fraRight)
        self.lblSat.setObjectName("lblSat")
        self.gridLayout_2.addWidget(self.lblSat, 5, 0, 1, 1)
        self.txtSat = QtWidgets.QLineEdit(self.fraRight)
        self.txtSat.setObjectName("txtSat")
        self.gridLayout_2.addWidget(self.txtSat, 5, 1, 1, 1)
        self.lblTreated = QtWidgets.QLabel(self.fraRight)
        self.lblTreated.setObjectName("lblTreated")
        self.gridLayout_2.addWidget(self.lblTreated, 6, 0, 1, 1)
        self.txtTreated = QtWidgets.QLineEdit(self.fraRight)
        self.txtTreated.setObjectName("txtTreated")
        self.gridLayout_2.addWidget(self.txtTreated, 6, 1, 1, 1)
        self.lblDrain = QtWidgets.QLabel(self.fraRight)
        self.lblDrain.setWordWrap(True)
        self.lblDrain.setObjectName("lblDrain")
        self.gridLayout_2.addWidget(self.lblDrain, 8, 0, 1, 2)
        self.txtDrain = QtWidgets.QLineEdit(self.fraRight)
        self.txtDrain.setObjectName("txtDrain")
        self.gridLayout_2.addWidget(self.txtDrain, 9, 0, 1, 1)
        self.cbkReturn = QtWidgets.QCheckBox(self.fraRight)
        self.cbkReturn.setObjectName("cbkReturn")
        self.gridLayout_2.addWidget(self.cbkReturn, 10, 0, 1, 2)
        self.lblPervious = QtWidgets.QLabel(self.fraRight)
        self.lblPervious.setObjectName("lblPervious")
        self.gridLayout_2.addWidget(self.lblPervious, 7, 0, 1, 1)
        self.txtPervTreated = QtWidgets.QLineEdit(self.fraRight)
        self.txtPervTreated.setObjectName("txtPervTreated")
        self.gridLayout_2.addWidget(self.txtPervTreated, 7, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.fraRight)
        self.verticalLayout.addWidget(self.fraTop)
        self.fraOKCancel = QtWidgets.QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fraOKCancel.setObjectName("fraOKCancel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fraOKCancel)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cmdOK = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName("cmdOK")
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QtWidgets.QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName("cmdCancel")
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout.addWidget(self.fraOKCancel)
        frmLIDUsage.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmLIDUsage)
        QtCore.QMetaObject.connectSlotsByName(frmLIDUsage)

    def retranslateUi(self, frmLIDUsage):
        _translate = QtCore.QCoreApplication.translate
        frmLIDUsage.setWindowTitle(_translate("frmLIDUsage", "SWMM LID Usage Editor"))
        self.lblLIDControlName.setText(_translate("frmLIDUsage", "LID Control Name"))
        self.lblFile.setText(_translate("frmLIDUsage", "Detailed Report File (Optional)"))
        self.btnFile.setText(_translate("frmLIDUsage", "..."))
        self.btnClear.setText(_translate("frmLIDUsage", "X"))
        self.cbxFull.setText(_translate("frmLIDUsage", "LID Occupies Full Subcatchment"))
        self.lblArea.setText(_translate("frmLIDUsage", "Area of Each Unit (sq ft or sq m)"))
        self.lblUnits.setText(_translate("frmLIDUsage", "Number of Units"))
        self.lblOccupied.setText(_translate("frmLIDUsage", "% of Subcatchment Occupied"))
        self.lblPercent.setText(_translate("frmLIDUsage", "100.0"))
        self.lblWidth.setText(_translate("frmLIDUsage", "Surface Width per Unit (ft or m)"))
        self.lblSat.setText(_translate("frmLIDUsage", "% Initially Saturated"))
        self.lblTreated.setText(_translate("frmLIDUsage", "% of Impervious Area Treated"))
        self.lblDrain.setText(_translate("frmLIDUsage", "Set Drain Flow To: \n"
"Leave Blank to use outlet of current subcatchment"))
        self.cbkReturn.setText(_translate("frmLIDUsage", "Return all Outflow to Pervious Area"))
        self.lblPervious.setText(_translate("frmLIDUsage", "% of Pervious Area Treated"))
        self.cmdOK.setText(_translate("frmLIDUsage", "OK"))
        self.cmdCancel.setText(_translate("frmLIDUsage", "Cancel"))

