# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\dev-ui\src\ui\SWMM\frmClimatologyDesigner.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
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

class Ui_frmClimatology(object):
    def setupUi(self, frmClimatology):
        frmClimatology.setObjectName(_fromUtf8("frmClimatology"))
        frmClimatology.resize(618, 417)
        font = QFont()
        font.setPointSize(10)
        frmClimatology.setFont(font)
        self.centralWidget = QWidget(frmClimatology)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_3 = QVBoxLayout(self.centralWidget)
        # self.verticalLayout_3.setMargin(11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.fraTop = QFrame(self.centralWidget)
        self.fraTop.setFrameShape(QFrame.StyledPanel)
        self.fraTop.setFrameShadow(QFrame.Raised)
        self.fraTop.setObjectName(_fromUtf8("fraTop"))
        self.verticalLayout = QVBoxLayout(self.fraTop)
        # self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabClimate = QTabWidget(self.fraTop)
        self.tabClimate.setObjectName(_fromUtf8("tabClimate"))
        self.Temperature = QWidget()
        self.Temperature.setObjectName(_fromUtf8("Temperature"))
        self.gridLayout_5 = QGridLayout(self.Temperature)
        # self.gridLayout_5.setMargin(11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.fraNoData = QFrame(self.Temperature)
        self.fraNoData.setFrameShape(QFrame.StyledPanel)
        self.fraNoData.setFrameShadow(QFrame.Raised)
        self.fraNoData.setObjectName(_fromUtf8("fraNoData"))
        self.verticalLayout_2 = QVBoxLayout(self.fraNoData)
        # self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lblSource = QLabel(self.fraNoData)
        self.lblSource.setObjectName(_fromUtf8("lblSource"))
        self.verticalLayout_2.addWidget(self.lblSource)
        self.rbnNoData = QRadioButton(self.fraNoData)
        self.rbnNoData.setObjectName(_fromUtf8("rbnNoData"))
        self.verticalLayout_2.addWidget(self.rbnNoData)
        self.gridLayout_5.addWidget(self.fraNoData, 1, 0, 1, 1)
        self.fraTimeseries = QFrame(self.Temperature)
        self.fraTimeseries.setFrameShape(QFrame.StyledPanel)
        self.fraTimeseries.setFrameShadow(QFrame.Raised)
        self.fraTimeseries.setObjectName(_fromUtf8("fraTimeseries"))
        self.horizontalLayout_2 = QHBoxLayout(self.fraTimeseries)
        # self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rbnTimeseries = QRadioButton(self.fraTimeseries)
        self.rbnTimeseries.setObjectName(_fromUtf8("rbnTimeseries"))
        self.horizontalLayout_2.addWidget(self.rbnTimeseries)
        self.cboTimeSeries = QComboBox(self.fraTimeseries)
        self.cboTimeSeries.setObjectName(_fromUtf8("cboTimeSeries"))
        self.horizontalLayout_2.addWidget(self.cboTimeSeries)
        self.btnTimeSeries = QToolButton(self.fraTimeseries)
        self.btnTimeSeries.setObjectName(_fromUtf8("btnTimeSeries"))
        self.horizontalLayout_2.addWidget(self.btnTimeSeries)
        self.gridLayout_5.addWidget(self.fraTimeseries, 2, 0, 1, 1)
        self.fraExternal = QFrame(self.Temperature)
        self.fraExternal.setFrameShape(QFrame.StyledPanel)
        self.fraExternal.setFrameShadow(QFrame.Raised)
        self.fraExternal.setObjectName(_fromUtf8("fraExternal"))
        self.gridLayout_2 = QGridLayout(self.fraExternal)
        # self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.txtClimate = QLineEdit(self.fraExternal)
        self.txtClimate.setObjectName(_fromUtf8("txtClimate"))
        self.gridLayout_2.addWidget(self.txtClimate, 2, 0, 1, 2)
        self.btnClimate = QToolButton(self.fraExternal)
        self.btnClimate.setObjectName(_fromUtf8("btnClimate"))
        self.gridLayout_2.addWidget(self.btnClimate, 2, 2, 1, 1)
        self.dedStart = QDateEdit(self.fraExternal)
        self.dedStart.setObjectName(_fromUtf8("dedStart"))
        self.gridLayout_2.addWidget(self.dedStart, 3, 1, 1, 2)
        self.cbxStart = QCheckBox(self.fraExternal)
        self.cbxStart.setObjectName(_fromUtf8("cbxStart"))
        self.gridLayout_2.addWidget(self.cbxStart, 3, 0, 1, 1)
        self.rbnExternal = QRadioButton(self.fraExternal)
        self.rbnExternal.setObjectName(_fromUtf8("rbnExternal"))
        self.gridLayout_2.addWidget(self.rbnExternal, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.fraExternal, 3, 0, 1, 1)
        self.tabClimate.addTab(self.Temperature, _fromUtf8(""))
        self.Evaporation = QWidget()
        self.Evaporation.setObjectName(_fromUtf8("Evaporation"))
        self.gridLayout_3 = QGridLayout(self.Evaporation)
        # self.gridLayout_3.setMargin(11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.fraEvapTop = QFrame(self.Evaporation)
        self.fraEvapTop.setFrameShape(QFrame.StyledPanel)
        self.fraEvapTop.setFrameShadow(QFrame.Raised)
        self.fraEvapTop.setObjectName(_fromUtf8("fraEvapTop"))
        self.gridLayout_10 = QGridLayout(self.fraEvapTop)
        # self.gridLayout_10.setMargin(11)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.lblEvap = QLabel(self.fraEvapTop)
        self.lblEvap.setObjectName(_fromUtf8("lblEvap"))
        self.gridLayout_10.addWidget(self.lblEvap, 0, 0, 1, 1)
        self.cboEvap = QComboBox(self.fraEvapTop)
        self.cboEvap.setObjectName(_fromUtf8("cboEvap"))
        self.gridLayout_10.addWidget(self.cboEvap, 0, 1, 1, 1)
        self.lblDaily = QLabel(self.fraEvapTop)
        self.lblDaily.setObjectName(_fromUtf8("lblDaily"))
        self.gridLayout_10.addWidget(self.lblDaily, 1, 0, 1, 1)
        self.txtDaily = QLineEdit(self.fraEvapTop)
        self.txtDaily.setObjectName(_fromUtf8("txtDaily"))
        self.gridLayout_10.addWidget(self.txtDaily, 1, 1, 1, 1)
        spacerItem = QSpacerItem(188, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem, 1, 2, 1, 1)
        self.lblEvapTs = QLabel(self.fraEvapTop)
        self.lblEvapTs.setObjectName(_fromUtf8("lblEvapTs"))
        self.gridLayout_10.addWidget(self.lblEvapTs, 2, 0, 1, 1)
        self.cboEvapTs = QComboBox(self.fraEvapTop)
        self.cboEvapTs.setObjectName(_fromUtf8("cboEvapTs"))
        self.gridLayout_10.addWidget(self.cboEvapTs, 2, 1, 1, 1)
        self.btnEvapTS = QToolButton(self.fraEvapTop)
        self.btnEvapTS.setObjectName(_fromUtf8("btnEvapTS"))
        self.gridLayout_10.addWidget(self.btnEvapTS, 2, 2, 1, 1)
        self.lblEvapMisc = QLabel(self.fraEvapTop)
        self.lblEvapMisc.setWordWrap(True)
        self.lblEvapMisc.setObjectName(_fromUtf8("lblEvapMisc"))
        self.gridLayout_10.addWidget(self.lblEvapMisc, 3, 0, 1, 3)
        self.tblEvap = QTableWidget(self.fraEvapTop)
        self.tblEvap.setObjectName(_fromUtf8("tblEvap"))
        self.tblEvap.setColumnCount(12)
        self.tblEvap.setRowCount(1)
        item = QTableWidgetItem()
        self.tblEvap.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(9, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(10, item)
        item = QTableWidgetItem()
        self.tblEvap.setHorizontalHeaderItem(11, item)
        self.tblEvap.verticalHeader().setVisible(False)
        self.gridLayout_10.addWidget(self.tblEvap, 4, 0, 1, 3)
        self.gridLayout_3.addWidget(self.fraEvapTop, 0, 0, 1, 1)
        self.lineEvap = QFrame(self.Evaporation)
        self.lineEvap.setFrameShape(QFrame.HLine)
        self.lineEvap.setFrameShadow(QFrame.Sunken)
        self.lineEvap.setObjectName(_fromUtf8("lineEvap"))
        self.gridLayout_3.addWidget(self.lineEvap, 1, 0, 1, 1)
        self.fraEvapBottom = QFrame(self.Evaporation)
        self.fraEvapBottom.setFrameShape(QFrame.StyledPanel)
        self.fraEvapBottom.setFrameShadow(QFrame.Raised)
        self.fraEvapBottom.setObjectName(_fromUtf8("fraEvapBottom"))
        self.gridLayout_4 = QGridLayout(self.fraEvapBottom)
        # self.gridLayout_4.setMargin(11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblMonthly = QLabel(self.fraEvapBottom)
        self.lblMonthly.setObjectName(_fromUtf8("lblMonthly"))
        self.gridLayout_4.addWidget(self.lblMonthly, 0, 0, 1, 1)
        self.cboMonthly = QComboBox(self.fraEvapBottom)
        self.cboMonthly.setObjectName(_fromUtf8("cboMonthly"))
        self.gridLayout_4.addWidget(self.cboMonthly, 0, 1, 1, 1)
        self.btnPattern = QToolButton(self.fraEvapBottom)
        self.btnPattern.setObjectName(_fromUtf8("btnPattern"))
        self.gridLayout_4.addWidget(self.btnPattern, 0, 2, 1, 1)
        self.btnDelete = QToolButton(self.fraEvapBottom)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.gridLayout_4.addWidget(self.btnDelete, 0, 3, 1, 1)
        self.cbxDry = QCheckBox(self.fraEvapBottom)
        self.cbxDry.setObjectName(_fromUtf8("cbxDry"))
        self.gridLayout_4.addWidget(self.cbxDry, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.fraEvapBottom, 2, 0, 1, 1)
        self.tabClimate.addTab(self.Evaporation, _fromUtf8(""))
        self.WindSpeed = QWidget()
        self.WindSpeed.setObjectName(_fromUtf8("WindSpeed"))
        self.gridLayout_6 = QGridLayout(self.WindSpeed)
        # self.gridLayout_6.setMargin(11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.rbnUseClimate = QRadioButton(self.WindSpeed)
        self.rbnUseClimate.setObjectName(_fromUtf8("rbnUseClimate"))
        self.gridLayout_6.addWidget(self.rbnUseClimate, 0, 0, 1, 1)
        self.rbnMonthly = QRadioButton(self.WindSpeed)
        self.rbnMonthly.setObjectName(_fromUtf8("rbnMonthly"))
        self.gridLayout_6.addWidget(self.rbnMonthly, 1, 0, 1, 1)
        self.lblMonthlyWind = QLabel(self.WindSpeed)
        self.lblMonthlyWind.setObjectName(_fromUtf8("lblMonthlyWind"))
        self.gridLayout_6.addWidget(self.lblMonthlyWind, 2, 0, 1, 1)
        self.tblWind = QTableWidget(self.WindSpeed)
        self.tblWind.setRowCount(1)
        self.tblWind.setColumnCount(12)
        self.tblWind.setObjectName(_fromUtf8("tblWind"))
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(9, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(10, item)
        item = QTableWidgetItem()
        self.tblWind.setHorizontalHeaderItem(11, item)
        self.tblWind.verticalHeader().setVisible(False)
        self.gridLayout_6.addWidget(self.tblWind, 3, 0, 1, 1)
        self.fraWindBot = QFrame(self.WindSpeed)
        self.fraWindBot.setFrameShape(QFrame.StyledPanel)
        self.fraWindBot.setFrameShadow(QFrame.Raised)
        self.fraWindBot.setObjectName(_fromUtf8("fraWindBot"))
        self.gridLayout_6.addWidget(self.fraWindBot, 4, 0, 1, 1)
        self.tabClimate.addTab(self.WindSpeed, _fromUtf8(""))
        self.SnowMelt = QWidget()
        self.SnowMelt.setObjectName(_fromUtf8("SnowMelt"))
        self.gridLayout_7 = QGridLayout(self.SnowMelt)
        # self.gridLayout_7.setMargin(11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.lblSnowDivide = QLabel(self.SnowMelt)
        self.lblSnowDivide.setWordWrap(True)
        self.lblSnowDivide.setObjectName(_fromUtf8("lblSnowDivide"))
        self.gridLayout_7.addWidget(self.lblSnowDivide, 0, 0, 1, 1)
        self.txtSnowDivide = QLineEdit(self.SnowMelt)
        self.txtSnowDivide.setObjectName(_fromUtf8("txtSnowDivide"))
        self.gridLayout_7.addWidget(self.txtSnowDivide, 0, 1, 1, 1)
        self.lblSnowATI = QLabel(self.SnowMelt)
        self.lblSnowATI.setWordWrap(True)
        self.lblSnowATI.setObjectName(_fromUtf8("lblSnowATI"))
        self.gridLayout_7.addWidget(self.lblSnowATI, 1, 0, 1, 1)
        self.txtSnowATI = QLineEdit(self.SnowMelt)
        self.txtSnowATI.setObjectName(_fromUtf8("txtSnowATI"))
        self.gridLayout_7.addWidget(self.txtSnowATI, 1, 1, 1, 1)
        self.lblSnowMelt = QLabel(self.SnowMelt)
        self.lblSnowMelt.setWordWrap(True)
        self.lblSnowMelt.setObjectName(_fromUtf8("lblSnowMelt"))
        self.gridLayout_7.addWidget(self.lblSnowMelt, 2, 0, 1, 1)
        self.txtSnowMelt = QLineEdit(self.SnowMelt)
        self.txtSnowMelt.setObjectName(_fromUtf8("txtSnowMelt"))
        self.gridLayout_7.addWidget(self.txtSnowMelt, 2, 1, 1, 1)
        self.lblSnowElevation = QLabel(self.SnowMelt)
        self.lblSnowElevation.setWordWrap(True)
        self.lblSnowElevation.setObjectName(_fromUtf8("lblSnowElevation"))
        self.gridLayout_7.addWidget(self.lblSnowElevation, 3, 0, 1, 1)
        self.txtSnowElevation = QLineEdit(self.SnowMelt)
        self.txtSnowElevation.setObjectName(_fromUtf8("txtSnowElevation"))
        self.gridLayout_7.addWidget(self.txtSnowElevation, 3, 1, 1, 1)
        self.lblSnowLatitude = QLabel(self.SnowMelt)
        self.lblSnowLatitude.setWordWrap(True)
        self.lblSnowLatitude.setObjectName(_fromUtf8("lblSnowLatitude"))
        self.gridLayout_7.addWidget(self.lblSnowLatitude, 4, 0, 1, 1)
        self.txtSnowLatitude = QLineEdit(self.SnowMelt)
        self.txtSnowLatitude.setObjectName(_fromUtf8("txtSnowLatitude"))
        self.gridLayout_7.addWidget(self.txtSnowLatitude, 4, 1, 1, 1)
        self.lblSnowLongitude = QLabel(self.SnowMelt)
        self.lblSnowLongitude.setWordWrap(True)
        self.lblSnowLongitude.setObjectName(_fromUtf8("lblSnowLongitude"))
        self.gridLayout_7.addWidget(self.lblSnowLongitude, 5, 0, 1, 1)
        self.txtSnowLongitude = QLineEdit(self.SnowMelt)
        self.txtSnowLongitude.setObjectName(_fromUtf8("txtSnowLongitude"))
        self.gridLayout_7.addWidget(self.txtSnowLongitude, 5, 1, 1, 1)
        self.tabClimate.addTab(self.SnowMelt, _fromUtf8(""))
        self.ArealDepletion = QWidget()
        self.ArealDepletion.setObjectName(_fromUtf8("ArealDepletion"))
        self.verticalLayout_6 = QVBoxLayout(self.ArealDepletion)
        # self.verticalLayout_6.setMargin(11)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.lblFraction = QLabel(self.ArealDepletion)
        self.lblFraction.setObjectName(_fromUtf8("lblFraction"))
        self.verticalLayout_6.addWidget(self.lblFraction)
        self.tblAreal = QTableWidget(self.ArealDepletion)
        self.tblAreal.setRowCount(10)
        self.tblAreal.setColumnCount(2)
        self.tblAreal.setObjectName(_fromUtf8("tblAreal"))
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tblAreal.setVerticalHeaderItem(9, item)
        item = QTableWidgetItem()
        self.tblAreal.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblAreal.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblAreal.setItem(0, 0, item)
        self.tblAreal.verticalHeader().setHighlightSections(True)
        self.verticalLayout_6.addWidget(self.tblAreal)
        self.frame = QFrame(self.ArealDepletion)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_8 = QGridLayout(self.frame)
        # self.gridLayout_8.setMargin(11)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.btnPerNat = QPushButton(self.frame)
        self.btnPerNat.setObjectName(_fromUtf8("btnPerNat"))
        self.gridLayout_8.addWidget(self.btnPerNat, 1, 1, 1, 1)
        self.btnPerNo = QPushButton(self.frame)
        self.btnPerNo.setObjectName(_fromUtf8("btnPerNo"))
        self.gridLayout_8.addWidget(self.btnPerNo, 0, 1, 1, 1)
        self.btnImpNat = QPushButton(self.frame)
        self.btnImpNat.setObjectName(_fromUtf8("btnImpNat"))
        self.gridLayout_8.addWidget(self.btnImpNat, 1, 0, 1, 1)
        self.btnImpNo = QPushButton(self.frame)
        self.btnImpNo.setObjectName(_fromUtf8("btnImpNo"))
        self.gridLayout_8.addWidget(self.btnImpNo, 0, 0, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout_6.addWidget(self.frame)
        self.tabClimate.addTab(self.ArealDepletion, _fromUtf8(""))
        self.Adjustments = QWidget()
        self.Adjustments.setObjectName(_fromUtf8("Adjustments"))
        self.verticalLayout_4 = QVBoxLayout(self.Adjustments)
        # self.verticalLayout_4.setMargin(11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tblAdjustments = QTableWidget(self.Adjustments)
        self.tblAdjustments.setObjectName(_fromUtf8("tblAdjustments"))
        self.tblAdjustments.setColumnCount(4)
        self.tblAdjustments.setRowCount(12)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(9, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(10, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setVerticalHeaderItem(11, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tblAdjustments.setHorizontalHeaderItem(3, item)
        self.verticalLayout_4.addWidget(self.tblAdjustments)
        self.frame_2 = QFrame(self.Adjustments)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_4.addWidget(self.frame_2)
        self.fraAdjBottom = QFrame(self.Adjustments)
        self.fraAdjBottom.setFrameShape(QFrame.StyledPanel)
        self.fraAdjBottom.setFrameShadow(QFrame.Raised)
        self.fraAdjBottom.setObjectName(_fromUtf8("fraAdjBottom"))
        self.gridLayout_9 = QGridLayout(self.fraAdjBottom)
        # self.gridLayout_9.setMargin(11)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.lblAdjustments = QLabel(self.fraAdjBottom)
        self.lblAdjustments.setObjectName(_fromUtf8("lblAdjustments"))
        self.gridLayout_9.addWidget(self.lblAdjustments, 0, 0, 1, 1)
        self.btnClear = QPushButton(self.fraAdjBottom)
        self.btnClear.setObjectName(_fromUtf8("btnClear"))
        self.gridLayout_9.addWidget(self.btnClear, 0, 2, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem2, 0, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.fraAdjBottom)
        self.tabClimate.addTab(self.Adjustments, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabClimate)
        self.verticalLayout_3.addWidget(self.fraTop)
        self.fraOKCancel = QFrame(self.centralWidget)
        self.fraOKCancel.setFrameShape(QFrame.StyledPanel)
        self.fraOKCancel.setFrameShadow(QFrame.Raised)
        self.fraOKCancel.setObjectName(_fromUtf8("fraOKCancel"))
        self.horizontalLayout = QHBoxLayout(self.fraOKCancel)
        # self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QSpacerItem(338, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.cmdOK = QPushButton(self.fraOKCancel)
        self.cmdOK.setObjectName(_fromUtf8("cmdOK"))
        self.horizontalLayout.addWidget(self.cmdOK)
        self.cmdCancel = QPushButton(self.fraOKCancel)
        self.cmdCancel.setObjectName(_fromUtf8("cmdCancel"))
        self.horizontalLayout.addWidget(self.cmdCancel)
        self.verticalLayout_3.addWidget(self.fraOKCancel)
        frmClimatology.setCentralWidget(self.centralWidget)

        self.retranslateUi(frmClimatology)
        self.tabClimate.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmClimatology)

    def retranslateUi(self, frmClimatology):
        frmClimatology.setWindowTitle(_translate("frmClimatology", "SWMM Climatology", None))
        self.lblSource.setText(_translate("frmClimatology", "Source of Temperature Data:", None))
        self.rbnNoData.setText(_translate("frmClimatology", "No Data", None))
        self.rbnTimeseries.setText(_translate("frmClimatology", "Time Series", None))
        self.btnTimeSeries.setText(_translate("frmClimatology", "...", None))
        self.btnClimate.setText(_translate("frmClimatology", "...", None))
        self.cbxStart.setText(_translate("frmClimatology", "Start Reading File At", None))
        self.rbnExternal.setText(_translate("frmClimatology", "Exteral Climate File", None))
        self.tabClimate.setTabText(self.tabClimate.indexOf(self.Temperature), _translate("frmClimatology", "Temperature", None))
        self.lblEvap.setText(_translate("frmClimatology", "Source of Evaporation Rates", None))
        self.lblDaily.setText(_translate("frmClimatology", "Daily Evaporation (in/day)", None))
        self.lblEvapTs.setText(_translate("frmClimatology", "Name of Time Series", None))
        self.btnEvapTS.setText(_translate("frmClimatology", "...", None))
        self.lblEvapMisc.setText(_translate("frmClimatology", "Pan Coefficients", None))
        item = self.tblEvap.verticalHeaderItem(0)
        item.setText(_translate("frmClimatology", "Value", None))
        item = self.tblEvap.horizontalHeaderItem(0)
        item.setText(_translate("frmClimatology", "Jan", None))
        item = self.tblEvap.horizontalHeaderItem(1)
        item.setText(_translate("frmClimatology", "Feb", None))
        item = self.tblEvap.horizontalHeaderItem(2)
        item.setText(_translate("frmClimatology", "Mar", None))
        item = self.tblEvap.horizontalHeaderItem(3)
        item.setText(_translate("frmClimatology", "Apr", None))
        item = self.tblEvap.horizontalHeaderItem(4)
        item.setText(_translate("frmClimatology", "May", None))
        item = self.tblEvap.horizontalHeaderItem(5)
        item.setText(_translate("frmClimatology", "Jun", None))
        item = self.tblEvap.horizontalHeaderItem(6)
        item.setText(_translate("frmClimatology", "Jul", None))
        item = self.tblEvap.horizontalHeaderItem(7)
        item.setText(_translate("frmClimatology", "Aug", None))
        item = self.tblEvap.horizontalHeaderItem(8)
        item.setText(_translate("frmClimatology", "Sep", None))
        item = self.tblEvap.horizontalHeaderItem(9)
        item.setText(_translate("frmClimatology", "Oct", None))
        item = self.tblEvap.horizontalHeaderItem(10)
        item.setText(_translate("frmClimatology", "Nov", None))
        item = self.tblEvap.horizontalHeaderItem(11)
        item.setText(_translate("frmClimatology", "Dec", None))
        self.lblMonthly.setText(_translate("frmClimatology", "Monthly Soil Recovery Pattern (Optional)", None))
        self.btnPattern.setText(_translate("frmClimatology", "...", None))
        self.btnDelete.setText(_translate("frmClimatology", "X", None))
        self.cbxDry.setText(_translate("frmClimatology", "Evaporate Only During Dry Periods", None))
        self.tabClimate.setTabText(self.tabClimate.indexOf(self.Evaporation), _translate("frmClimatology", "Evaporation", None))
        self.rbnUseClimate.setText(_translate("frmClimatology", "Use Climate File Data (see Temperature page)", None))
        self.rbnMonthly.setText(_translate("frmClimatology", "Use Monthly Averages", None))
        self.lblMonthlyWind.setText(_translate("frmClimatology", "Monthly Wind Speed (mph)", None))
        item = self.tblWind.horizontalHeaderItem(0)
        item.setText(_translate("frmClimatology", "Jan", None))
        item = self.tblWind.horizontalHeaderItem(1)
        item.setText(_translate("frmClimatology", "Feb", None))
        item = self.tblWind.horizontalHeaderItem(2)
        item.setText(_translate("frmClimatology", "Mar", None))
        item = self.tblWind.horizontalHeaderItem(3)
        item.setText(_translate("frmClimatology", "Apr", None))
        item = self.tblWind.horizontalHeaderItem(4)
        item.setText(_translate("frmClimatology", "May", None))
        item = self.tblWind.horizontalHeaderItem(5)
        item.setText(_translate("frmClimatology", "Jun", None))
        item = self.tblWind.horizontalHeaderItem(6)
        item.setText(_translate("frmClimatology", "Jul", None))
        item = self.tblWind.horizontalHeaderItem(7)
        item.setText(_translate("frmClimatology", "Aug", None))
        item = self.tblWind.horizontalHeaderItem(8)
        item.setText(_translate("frmClimatology", "Sep", None))
        item = self.tblWind.horizontalHeaderItem(9)
        item.setText(_translate("frmClimatology", "Oct", None))
        item = self.tblWind.horizontalHeaderItem(10)
        item.setText(_translate("frmClimatology", "Nov", None))
        item = self.tblWind.horizontalHeaderItem(11)
        item.setText(_translate("frmClimatology", "Dec", None))
        self.tabClimate.setTabText(self.tabClimate.indexOf(self.WindSpeed), _translate("frmClimatology", "Wind Speed", None))
        self.lblSnowDivide.setText(_translate("frmClimatology", "Dividing Temperature Between Snow and Rain (degrees F)", None))
        self.lblSnowATI.setText(_translate("frmClimatology", "ATI Weight (fraction)", None))
        self.lblSnowMelt.setText(_translate("frmClimatology", "Negative Melt Ratio (fraction)", None))
        self.lblSnowElevation.setText(_translate("frmClimatology", "Elevation Above MLS (feet)", None))
        self.lblSnowLatitude.setText(_translate("frmClimatology", "Latitude (degrees)", None))
        self.lblSnowLongitude.setText(_translate("frmClimatology", "Longitude Correciton (+/- minutes)", None))
        self.tabClimate.setTabText(self.tabClimate.indexOf(self.SnowMelt), _translate("frmClimatology", "Snow Melt", None))
        self.lblFraction.setText(_translate("frmClimatology", "Fraction of Area Covered by Snow, by Depth Ratio", None))
        item = self.tblAreal.verticalHeaderItem(0)
        item.setText(_translate("frmClimatology", "0.0", None))
        item = self.tblAreal.verticalHeaderItem(1)
        item.setText(_translate("frmClimatology", "0.1", None))
        item = self.tblAreal.verticalHeaderItem(2)
        item.setText(_translate("frmClimatology", "0.2", None))
        item = self.tblAreal.verticalHeaderItem(3)
        item.setText(_translate("frmClimatology", "0.3", None))
        item = self.tblAreal.verticalHeaderItem(4)
        item.setText(_translate("frmClimatology", "0.4", None))
        item = self.tblAreal.verticalHeaderItem(5)
        item.setText(_translate("frmClimatology", "0.5", None))
        item = self.tblAreal.verticalHeaderItem(6)
        item.setText(_translate("frmClimatology", "0.6", None))
        item = self.tblAreal.verticalHeaderItem(7)
        item.setText(_translate("frmClimatology", "0.7", None))
        item = self.tblAreal.verticalHeaderItem(8)
        item.setText(_translate("frmClimatology", "0.8", None))
        item = self.tblAreal.verticalHeaderItem(9)
        item.setText(_translate("frmClimatology", "0.9", None))
        item = self.tblAreal.horizontalHeaderItem(0)
        item.setText(_translate("frmClimatology", "Impervious", None))
        item = self.tblAreal.horizontalHeaderItem(1)
        item.setText(_translate("frmClimatology", "Pervious", None))
        __sortingEnabled = self.tblAreal.isSortingEnabled()
        self.tblAreal.setSortingEnabled(False)
        self.tblAreal.setSortingEnabled(__sortingEnabled)
        self.btnPerNat.setText(_translate("frmClimatology", "Natural Area", None))
        self.btnPerNo.setText(_translate("frmClimatology", "No Per. Depletion", None))
        self.btnImpNat.setText(_translate("frmClimatology", "Natural Area", None))
        self.btnImpNo.setText(_translate("frmClimatology", "No Imp. Depletion", None))
        self.tabClimate.setTabText(self.tabClimate.indexOf(self.ArealDepletion), _translate("frmClimatology", "Areal Depletion", None))
        item = self.tblAdjustments.verticalHeaderItem(0)
        item.setText(_translate("frmClimatology", "Jan", None))
        item = self.tblAdjustments.verticalHeaderItem(1)
        item.setText(_translate("frmClimatology", "Feb", None))
        item = self.tblAdjustments.verticalHeaderItem(2)
        item.setText(_translate("frmClimatology", "Mar", None))
        item = self.tblAdjustments.verticalHeaderItem(3)
        item.setText(_translate("frmClimatology", "Apr", None))
        item = self.tblAdjustments.verticalHeaderItem(4)
        item.setText(_translate("frmClimatology", "May", None))
        item = self.tblAdjustments.verticalHeaderItem(5)
        item.setText(_translate("frmClimatology", "Jun", None))
        item = self.tblAdjustments.verticalHeaderItem(6)
        item.setText(_translate("frmClimatology", "Jul", None))
        item = self.tblAdjustments.verticalHeaderItem(7)
        item.setText(_translate("frmClimatology", "Aug", None))
        item = self.tblAdjustments.verticalHeaderItem(8)
        item.setText(_translate("frmClimatology", "Sep", None))
        item = self.tblAdjustments.verticalHeaderItem(9)
        item.setText(_translate("frmClimatology", "Oct", None))
        item = self.tblAdjustments.verticalHeaderItem(10)
        item.setText(_translate("frmClimatology", "Nov", None))
        item = self.tblAdjustments.verticalHeaderItem(11)
        item.setText(_translate("frmClimatology", "Dec", None))
        item = self.tblAdjustments.horizontalHeaderItem(0)
        item.setText(_translate("frmClimatology", "Temp", None))
        item = self.tblAdjustments.horizontalHeaderItem(1)
        item.setText(_translate("frmClimatology", "Evap", None))
        item = self.tblAdjustments.horizontalHeaderItem(2)
        item.setText(_translate("frmClimatology", "Rain", None))
        item = self.tblAdjustments.horizontalHeaderItem(3)
        item.setText(_translate("frmClimatology", "Cond", None))
        self.lblAdjustments.setText(_translate("frmClimatology", "Temp -- Temperature Adjustment (+- deg F or deg C)\n"
"Evap -- evaporation adjustment (+- in/day or mm/day)\n"
"Rain -- rainfall multiplier\n"
"Cond -- soil conductivity multiplier", None))
        self.btnClear.setText(_translate("frmClimatology", "Clear All", None))
        self.tabClimate.setTabText(self.tabClimate.indexOf(self.Adjustments), _translate("frmClimatology", "Adjustments", None))
        self.cmdOK.setText(_translate("frmClimatology", "OK", None))
        self.cmdCancel.setText(_translate("frmClimatology", "Cancel", None))

