# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\EPANET\frmCalibrationDataDesigner.ui'
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

class Ui_frmCalibrationData(object):
    def setupUi(self, frmCalibrationData):
        frmCalibrationData.setObjectName(_fromUtf8("frmCalibrationData"))
        frmCalibrationData.resize(541, 303)
        font = QtGui.QFont()
        font.setPointSize(10)
        frmCalibrationData.setFont(font)
        self.centralWidget = QtGui.QWidget(frmCalibrationData)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame = QtGui.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tableWidget = QtGui.QTableWidget(self.frame)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(6)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.tableWidget.verticalHeader().setMinimumSectionSize(50)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.toolButton = QtGui.QToolButton(self.frame)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout_2.addWidget(self.frame)
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
        self.verticalLayout_2.addWidget(self.fraOKCancel)
        frmCalibrationData.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmCalibrationData)
        QtCore.QMetaObject.connectSlotsByName(frmCalibrationData)

    def retranslateUi(self, frmCalibrationData):
        frmCalibrationData.setWindowTitle(_translate("frmCalibrationData", "EPANET Calibration Data", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("frmCalibrationData", "Demand", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("frmCalibrationData", "Head", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("frmCalibrationData", "Pressure", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("frmCalibrationData", "Quality", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("frmCalibrationData", "Flow", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("frmCalibrationData", "Velocity", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("frmCalibrationData", "Name of Calibration File", None))
        self.toolButton.setText(_translate("frmCalibrationData", "...", None))
        self.cmdOK.setText(_translate("frmCalibrationData", "OK", None))
        self.cmdCancel.setText(_translate("frmCalibrationData", "Cancel", None))

