import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import core.swmm.climatology
from ui.SWMM.frmClimatologyDesigner import Ui_frmClimatology
from core.swmm.climatology.climatology import TemperatureSource
from ui.SWMM.frmTimeseries import frmTimeseries
import ui.convenience
# from PyQt4.QtGui import *


class frmClimatology(QtGui.QMainWindow, Ui_frmClimatology):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cboEvap.clear()
        self.cboEvap.addItems(("Constant Value","Time Series","Climate File","Monthly Averages","Temperatures"))
        # ui.convenience.set_combo_items(core.swmm.curves.CurveType, self.cboCurveType)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.rbnNoData, QtCore.SIGNAL("clicked()"), self.rbnNoData_Clicked)
        QtCore.QObject.connect(self.rbnTimeseries, QtCore.SIGNAL("clicked()"), self.rbnTimeseries_Clicked)
        QtCore.QObject.connect(self.rbnExternal, QtCore.SIGNAL("clicked()"), self.rbnExternal_Clicked)
        QtCore.QObject.connect(self.btnTimeSeries, QtCore.SIGNAL("clicked()"), self.btnTimeSeries_Clicked)
        QtCore.QObject.connect(self.btnClimate, QtCore.SIGNAL("clicked()"), self.btnClimate_Clicked)
        # QtCore.QObject.connect(self.cboEvap, QtCore.SIGNAL("clicked()"), self.cboEvap_currentIndexChanged)
        self.cboEvap.currentIndexChanged.connect(self.cboEvap_currentIndexChanged)
        self.set_all(parent.project)
        self._parent = parent
        self.curve_type = ""

    def set_from(self, project, climate_type):
        if climate_type == "Temperature":
            self.tabClimate.setCurrentIndex(0)
        elif climate_type == "Evaporation":
            self.tabClimate.setCurrentIndex(1)
        elif climate_type == "Wind Speed":
            self.tabClimate.setCurrentIndex(2)
        elif climate_type == "Snow Melt":
            self.tabClimate.setCurrentIndex(3)
        elif climate_type == "Areal Depletion":
            self.tabClimate.setCurrentIndex(4)
        elif climate_type == "Adjustment":
            self.tabClimate.setCurrentIndex(5)

    def set_all(self, project):
        evap_section = core.swmm.climatology
        # evap_section = project.find_section("EVAPORATION")

        # temp_section = core.swmm.climatology.climatology
        temp_section = project.find_section("TEMPERATURE")
        if temp_section.source == TemperatureSource.TIMESERIES and temp_section.timeseries:
            self.rbnTimeseries.setChecked(True)
            self.rbnExternal.setChecked(False)
            self.rbnNoData.setChecked(False)
        elif temp_section.source == TemperatureSource.FILE:
            self.rbnTimeseries.setChecked(False)
            self.rbnExternal.setChecked(True)
            self.rbnNoData.setChecked(False)
        else:
            self.rbnTimeseries.setChecked(False)
            self.rbnExternal.setChecked(False)
            self.rbnNoData.setChecked(True)

        time_series_section = project.find_section("TIMESERIES")
        time_series_list = time_series_section.value[0:]
        self.cboTimeSeries.clear()
        selected_index = 0
        for value in time_series_list:
            self.cboTimeSeries.addItem(value.name)
            if value.name == temp_section.timeseries:
                selected_index = self.cboTimeSeries.count
        self.cboTimeSeries.setCurrentIndex(selected_index)
        self.txtClimate.setText(temp_section.filename)
        self.dedStart.setDate(QtCore.QDate.fromString(temp_section.start_date, "MM/dd/yyyy"))
        if temp_section.start_date:
            self.cbxStart.setChecked(True)

        self.cboEvap_currentIndexChanged(0)

    def cmdOK_Clicked(self):
        # TODO: Check for blank/duplicate curve ID
        # TODO: Check if X-values are in ascending order
        # section = self._parent.project.find_section("CURVES")
        # curve_list = section.value[0:]
        # # assume we are editing the first one
        # for curve in curve_list:
        #     if curve.curve_id and curve.curve_type.name[:4] == self.curve_type[:4]:
        #         curve.curve_id = self.txtCurveID.text()
        #         # curve.description = self.txtDescription.text()
        #         # curve.curve_type = core.swmm.curves.CurveType[self.cboCurveType.currentText()]
        #         if self.curve_type == "PUMP":
        #             if self.cboCurveType.currentIndex() == 0:
        #                 curve.curve_type = core.swmm.curves.CurveType["PUMP1"]
        #             if self.cboCurveType.currentIndex() == 1:
        #                 curve.curve_type = core.swmm.curves.CurveType["PUMP2"]
        #             if self.cboCurveType.currentIndex() == 2:
        #                 curve.curve_type = core.swmm.curves.CurveType["PUMP3"]
        #             if self.cboCurveType.currentIndex() == 3:
        #                 curve.curve_type = core.swmm.curves.CurveType["PUMP4"]
        #         curve.curve_xy = []
        #         for row in range(self.tblMult.rowCount()):
        #             if self.tblMult.item(row,0) and self.tblMult.item(row,1):
        #                 x = self.tblMult.item(row,0).text()
        #                 y = self.tblMult.item(row,1).text()
        #                 if len(x) > 0 and len(y) > 0:
        #                     curve.curve_xy.append((x, y))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboEvap_currentIndexChanged(self, newIndex):
        if newIndex == 0: # constant value
            self.lblDaily.setVisible(True)
            self.txtDaily.setVisible(True)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapDelete.setVisible(False)
            self.lblEvapMisc.setVisible(False)
            self.tblEvap.setVisible(False)
        elif newIndex == 1: # time series
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(True)
            self.cboEvapTs.setVisible(True)
            self.btnEvapDelete.setVisible(True)
            self.lblEvapMisc.setVisible(False)
            self.tblEvap.setVisible(False)
        elif newIndex == 2: # climate file
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapDelete.setVisible(False)
            self.lblEvapMisc.setText("Pan Coefficients")
            self.lblEvapMisc.setVisible(True)
            self.tblEvap.setVisible(True)
        elif newIndex == 3: # monthly averages
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapDelete.setVisible(False)
            self.lblEvapMisc.setText("Monthly Averages (in/day)")
            self.lblEvapMisc.setVisible(True)
            self.tblEvap.setVisible(True)
        elif newIndex == 4: # temperatures
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapDelete.setVisible(False)
            self.lblEvapMisc.setText("Evaporation rates will be computed using temperatures from the Climate File selected on the Temperature page.")
            self.lblEvapMisc.setVisible(True)
            self.tblEvap.setVisible(False)

    def rbnNoData_Clicked(self):
        if self.rbnNoData.isChecked():
            self.rbnTimeseries.setChecked(False)
            self.rbnExternal.setChecked(False)
        else:
            self.rbnNoData.setChecked(True)

    def rbnTimeseries_Clicked(self):
        if self.rbnTimeseries.isChecked():
            self.rbnNoData.setChecked(False)
            self.rbnExternal.setChecked(False)
        else:
            self.rbnTimeseries.setChecked(True)

    def rbnExternal_Clicked(self):
        if self.rbnExternal.isChecked():
            self.rbnNoData.setChecked(False)
            self.rbnTimeseries.setChecked(False)
        else:
            self.rbnExternal.setChecked(True)

    def btnTimeSeries_Clicked(self):
        # send in currently selected timeseries
        self._frmTimeseries = frmTimeseries(self.parent())
        self._frmTimeseries.show()

    def btnClimate_Clicked(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Select a Climatological File", '',
                                                      "Data files (*.DAT);;Text files (*.TXT);;All files (*.*)")
        if file_name:
            self.txtClimate.setText(file_name)