import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import core.swmm.climatology
from ui.SWMM.frmClimatologyDesigner import Ui_frmClimatology
from core.swmm.climatology.climatology import TemperatureSource
from core.swmm.climatology.climatology import EvaporationFormat
from core.swmm.climatology.climatology import WindSource
from ui.SWMM.frmTimeseries import frmTimeseries
from ui.SWMM.frmPatternEditor import frmPatternEditor
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
        QtCore.QObject.connect(self.btnImpNo, QtCore.SIGNAL("clicked()"), self.btnImpNo_Clicked)
        QtCore.QObject.connect(self.btnImpNat, QtCore.SIGNAL("clicked()"), self.btnImpNat_Clicked)
        QtCore.QObject.connect(self.btnPerNo, QtCore.SIGNAL("clicked()"), self.btnPerNo_Clicked)
        QtCore.QObject.connect(self.btnPerNat, QtCore.SIGNAL("clicked()"), self.btnPerNat_Clicked)
        QtCore.QObject.connect(self.btnEvapTS, QtCore.SIGNAL("clicked()"), self.btnEvapTS_Clicked)
        QtCore.QObject.connect(self.btnPattern, QtCore.SIGNAL("clicked()"), self.btnPattern_Clicked)
        QtCore.QObject.connect(self.btnDelete, QtCore.SIGNAL("clicked()"), self.btnDelete_Clicked)
        QtCore.QObject.connect(self.btnClear, QtCore.SIGNAL("clicked()"), self.btnClear_Clicked)
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
        # evap_section = core.swmm.climatology
        evap_section = project.find_section("EVAPORATION")
        # "Constant Value","Time Series","Climate File","Monthly Averages","Temperatures"
        self.evap_pan_list = evap_section.monthly_pan_coefficients
        self.evap_monthly_list = evap_section.monthly

        if evap_section.format == EvaporationFormat.UNSET:
            self.cboEvap.setCurrentIndex(0)
            self.cboEvap_currentIndexChanged(0)
        elif evap_section.format == EvaporationFormat.CONSTANT:
            self.cboEvap.setCurrentIndex(0)
            self.cboEvap_currentIndexChanged(0)
        elif evap_section.format == EvaporationFormat.MONTHLY:
            self.cboEvap.setCurrentIndex(3)
            self.cboEvap_currentIndexChanged(3)
        elif evap_section.format == EvaporationFormat.TIMESERIES:
            self.cboEvap.setCurrentIndex(1)
            self.cboEvap_currentIndexChanged(1)
        elif evap_section.format == EvaporationFormat.TEMPERATURE:
            self.cboEvap.setCurrentIndex(4)
            self.cboEvap_currentIndexChanged(4)
        elif evap_section.format == EvaporationFormat.FILE:
            self.cboEvap.setCurrentIndex(2)
            self.cboEvap_currentIndexChanged(2)
        if evap_section.constant == '':
            evap_section.constant = 0.0
        self.txtDaily.setText(str(evap_section.constant))
        self.cbxDry.setChecked(evap_section.dry_only)

        time_series_section = project.find_section("TIMESERIES")
        time_series_list = time_series_section.value[0:]
        self.cboEvapTs.clear()
        selected_index = 0
        for value in time_series_list:
            self.cboEvapTs.addItem(value.name)
            if value.name == evap_section.timeseries:
                selected_index = int(self.cboEvapTs.count())-1
        self.cboEvapTs.setCurrentIndex(selected_index)

        pattern_section = project.find_section("PATTERNS")
        pattern_list = pattern_section.value[0:]
        self.cboMonthly.clear()
        self.cboMonthly.addItem("")
        selected_index = 0
        previous_pattern = ""
        for value in pattern_list:
             if value.name and value.name != previous_pattern:
                 self.cboMonthly.addItem(value.name)
                 previous_pattern = value.name
                 if value.name == evap_section.recovery_pattern:
                    selected_index = int(self.cboMonthly.count())-1
        self.cboMonthly.setCurrentIndex(selected_index)

        # temp_section = core.swmm.climatology.climatology
        temp_section = project.find_section("TEMPERATURE")
        if temp_section.source == TemperatureSource.UNSET:
            self.rbnTimeseries.setChecked(False)
            self.rbnExternal.setChecked(False)
            self.rbnNoData.setChecked(True)
        elif temp_section.source == TemperatureSource.TIMESERIES and temp_section.timeseries:
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
        self.cboTimeSeries.addItem('')
        selected_index = 0
        for value in time_series_list:
            self.cboTimeSeries.addItem(value.name)
            if value.name == temp_section.timeseries:
                selected_index = self.cboTimeSeries.count()
        self.cboTimeSeries.setCurrentIndex(selected_index)
        self.txtClimate.setText(temp_section.filename)
        self.dedStart.setDate(QtCore.QDate.fromString(temp_section.start_date, "MM/dd/yyyy"))
        if temp_section.start_date:
            self.cbxStart.setChecked(True)

        # wind speed tab
        if temp_section.wind_speed.source == WindSource.MONTHLY:
            self.rbnMonthly.setChecked(True)
            monthly_list = temp_section.wind_speed.wind_speed_monthly
            point_count = -1
            for value in monthly_list:
                point_count += 1
                led = QtGui.QLineEdit(str(value))
                self.tblWind.setItem(0,point_count,QtGui.QTableWidgetItem(led.text()))
        elif temp_section.wind_speed.source == WindSource.FILE:
            self.rbnUseClimate.setChecked(True)

        # snow melt tab
        self.txtSnowDivide.setText(str(temp_section.snow_melt.snow_temp))
        self.txtSnowATI.setText(str(temp_section.snow_melt.ati_weight))
        self.txtSnowMelt.setText(str(temp_section.snow_melt.negative_melt_ratio))
        self.txtSnowElevation.setText(str(temp_section.snow_melt.elevation))
        self.txtSnowLatitude.setText(str(temp_section.snow_melt.latitude))
        self.txtSnowLongitude.setText(str(temp_section.snow_melt.time_correction))

        # areal depletion
        areal_list = temp_section.areal_depletion.adc_impervious
        point_count = -1
        for value in areal_list:
            point_count += 1
            led = QtGui.QLineEdit(str(value))
            self.tblAreal.setItem(point_count,0,QtGui.QTableWidgetItem(led.text()))
        areal_list = temp_section.areal_depletion.adc_pervious
        point_count = -1
        for value in areal_list:
            point_count += 1
            led = QtGui.QLineEdit(str(value))
            self.tblAreal.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))
        # self.tblAreal.resizeColumnsToContents()

        # adjustments for temp, evap, rain, cond
        adjustments_section = project.find_section("ADJUSTMENTS")
        temp_list = adjustments_section.temperature
        point_count = -1
        for value in temp_list:
            point_count += 1
            led = QtGui.QLineEdit(str(value))
            self.tblAdjustments.setItem(point_count,0,QtGui.QTableWidgetItem(led.text()))
        evap_list = adjustments_section.evaporation
        point_count = -1
        for value in evap_list:
            point_count += 1
            led = QtGui.QLineEdit(str(value))
            self.tblAdjustments.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))
        rain_list = adjustments_section.rainfall
        point_count = -1
        for value in rain_list:
            point_count += 1
            led = QtGui.QLineEdit(str(value))
            self.tblAdjustments.setItem(point_count,2,QtGui.QTableWidgetItem(led.text()))
        cond_list = adjustments_section.soil_conductivity
        point_count = -1
        for value in cond_list:
            point_count += 1
            led = QtGui.QLineEdit(str(value))
            self.tblAdjustments.setItem(point_count,3,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):

        # save evap tab
        evap_section = self._parent.project.find_section("EVAPORATION")
        # "Constant Value","Time Series","Climate File","Monthly Averages","Temperatures"
        if self.cboEvap.currentIndex() == 0:
            evap_section.format = EvaporationFormat.CONSTANT
        elif self.cboEvap.currentIndex() == 1:
            evap_section.format = EvaporationFormat.TIMESERIES
        elif self.cboEvap.currentIndex() == 2:
            evap_section.format = EvaporationFormat.FILE
            evap_section.monthly_pan_coefficients = []
            for column in range(0,12):
                if self.tblEvap.item(0,column):
                    x = str(self.tblEvap.item(0,column).text())
                else:
                    x = ''
                evap_section.monthly_pan_coefficients.append(x)
        elif self.cboEvap.currentIndex() == 3:
            evap_section.format = EvaporationFormat.MONTHLY
            evap_section.monthly = []
            for column in range(0,12):
                if self.tblEvap.item(0,column):
                    x = str(self.tblEvap.item(0,column).text())
                else:
                    x = ''
                evap_section.monthly.append(x)
        elif self.cboEvap.currentIndex() == 4:
            evap_section.format = EvaporationFormat.TEMPERATURE
        evap_section.constant = float(self.txtDaily.text())
        if self.cbxDry.isChecked():
            evap_section.dry_only = True
        else:
            evap_section.dry_only = False
        evap_section.timeseries = str(self.cboEvapTs.currentText())
        evap_section.recovery_pattern = str(self.cboMonthly.currentText())

        # save temperature tab
        temp_section = self._parent.project.find_section("TEMPERATURE")
        if self.rbnTimeseries.isChecked():
            temp_section.source = TemperatureSource.TIMESERIES
        elif self.rbnExternal.isChecked():
            temp_section.source = TemperatureSource.FILE
        else:
            temp_section.source = TemperatureSource.UNSET
        temp_section.timeseries = str(self.cboTimeSeries.currentText())
        temp_section.filename = self.txtClimate.text()
        if self.cbxStart.isChecked():
            temp_section.start_date = self.dedStart.date().toString("MM/dd/yyyy")

        # save wind speed tab
        if self.rbnMonthly.isChecked():
            temp_section.wind_speed.source = WindSource.MONTHLY
        elif self.rbnUseClimate.isChecked():
            temp_section.wind_speed.source = WindSource.FILE
        temp_section.wind_speed.wind_speed_monthly = []
        for column in range(0,12):
            if self.tblWind.item(0,column):
                x = self.tblWind.item(0,column).text()
                if len(x) > 0:
                    temp_section.wind_speed.wind_speed_monthly.append(x)

        # save snow melt tab
        temp_section.snow_melt.snow_temp = self.txtSnowDivide.text()
        temp_section.snow_melt.ati_weight = self.txtSnowATI.text()
        temp_section.snow_melt.negative_melt_ratio = self.txtSnowMelt.text()
        temp_section.snow_melt.elevation = self.txtSnowElevation.text()
        temp_section.snow_melt.latitude = self.txtSnowLatitude.text()
        temp_section.snow_melt.time_correction = self.txtSnowLongitude.text()

        # save areal depletion
        temp_section.areal_depletion.adc_impervious = []
        for row in range(0,10):
            if self.tblAreal.item(row,0):
                x = self.tblAreal.item(row,0).text()
                if len(x) > 0:
                    temp_section.areal_depletion.adc_impervious.append(x)
        temp_section.areal_depletion.adc_pervious = []
        for row in range(0,10):
            if self.tblAreal.item(row,1):
                x = self.tblAreal.item(row,1).text()
                if len(x) > 0:
                    temp_section.areal_depletion.adc_pervious.append(x)

        # save adjustments for temp, evap, rain, cond
        adjustments_section = self._parent.project.find_section("ADJUSTMENTS")
        adjustments_section.temperature = []
        for row in range(0,12):
            if self.tblAdjustments.item(row,0):
                x = str(self.tblAdjustments.item(row,0).text())
            else:
                x = ''
            adjustments_section.temperature.append(x)
        adjustments_section.evaporation = []
        for row in range(0,12):
            if self.tblAdjustments.item(row,1):
                x = str(self.tblAdjustments.item(row,1).text())
            else:
                x = ''
            adjustments_section.evaporation.append(x)
        adjustments_section.rainfall = []
        for row in range(0,12):
            if self.tblAdjustments.item(row,2):
                x = str(self.tblAdjustments.item(row,2).text())
            else:
                x = ''
            adjustments_section.rainfall.append(x)
        adjustments_section.soil_conductivity = []
        for row in range(0,12):
            if self.tblAdjustments.item(row,3):
                x = str(self.tblAdjustments.item(row,3).text())
            else:
                x = ''
            adjustments_section.soil_conductivity.append(x)

        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboEvap_currentIndexChanged(self, newIndex):
        if newIndex == 0: # constant value
            self.lblDaily.setVisible(True)
            self.txtDaily.setVisible(True)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapTS.setVisible(False)
            self.lblEvapMisc.setVisible(False)
            self.tblEvap.setVisible(False)
        elif newIndex == 1: # time series
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(True)
            self.cboEvapTs.setVisible(True)
            self.btnEvapTS.setVisible(True)
            self.lblEvapMisc.setVisible(False)
            self.tblEvap.setVisible(False)
        elif newIndex == 2: # climate file
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapTS.setVisible(False)
            self.lblEvapMisc.setText("Pan Coefficients")
            self.lblEvapMisc.setVisible(True)
            self.tblEvap.setVisible(True)
            point_count = -1
            for value in self.evap_pan_list:
                point_count += 1
                led = QtGui.QLineEdit(str(value))
                self.tblEvap.setItem(0,point_count,QtGui.QTableWidgetItem(led.text()))
        elif newIndex == 3: # monthly averages
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapTS.setVisible(False)
            self.lblEvapMisc.setText("Monthly Averages (in/day)")
            self.lblEvapMisc.setVisible(True)
            self.tblEvap.setVisible(True)
            point_count = -1
            for value in self.evap_monthly_list:
                point_count += 1
                led = QtGui.QLineEdit(str(value))
                self.tblEvap.setItem(0,point_count,QtGui.QTableWidgetItem(led.text()))
        elif newIndex == 4: # temperatures
            self.lblDaily.setVisible(False)
            self.txtDaily.setVisible(False)
            self.lblEvapTs.setVisible(False)
            self.cboEvapTs.setVisible(False)
            self.btnEvapTS.setVisible(False)
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

    def btnImpNo_Clicked(self):
        for row in range(0,10):
            led = QtGui.QLineEdit('1.0')
            self.tblAreal.setItem(row,0,QtGui.QTableWidgetItem(led.text()))

    def btnPerNo_Clicked(self):
        for row in range(0,10):
            led = QtGui.QLineEdit('1.0')
            self.tblAreal.setItem(row,1,QtGui.QTableWidgetItem(led.text()))

    def btnImpNat_Clicked(self):
        self.tblAreal.setItem(0,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.10').text()))
        self.tblAreal.setItem(1,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.35').text()))
        self.tblAreal.setItem(2,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.53').text()))
        self.tblAreal.setItem(3,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.66').text()))
        self.tblAreal.setItem(4,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.75').text()))
        self.tblAreal.setItem(5,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.82').text()))
        self.tblAreal.setItem(6,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.87').text()))
        self.tblAreal.setItem(7,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.92').text()))
        self.tblAreal.setItem(8,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.95').text()))
        self.tblAreal.setItem(9,0,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.98').text()))

    def btnPerNat_Clicked(self):
        self.tblAreal.setItem(0,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.10').text()))
        self.tblAreal.setItem(1,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.35').text()))
        self.tblAreal.setItem(2,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.53').text()))
        self.tblAreal.setItem(3,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.66').text()))
        self.tblAreal.setItem(4,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.75').text()))
        self.tblAreal.setItem(5,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.82').text()))
        self.tblAreal.setItem(6,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.87').text()))
        self.tblAreal.setItem(7,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.92').text()))
        self.tblAreal.setItem(8,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.95').text()))
        self.tblAreal.setItem(9,1,QtGui.QTableWidgetItem(QtGui.QLineEdit('0.98').text()))

    def btnEvapTS_Clicked(self):
        # edit timeseries
        # send in currently selected timeseries
        self._frmTimeseries = frmTimeseries(self.parent())
        self._frmTimeseries.show()

    def btnPattern_Clicked(self):
        # edit pattern
        self._frmPatternEditor = frmPatternEditor(self.parent())
        self._frmPatternEditor.show()

        pattern_section = self._parent.project.find_section("PATTERNS")
        pattern_list = pattern_section.value[0:]
        self.cboMonthly.clear()
        self.cboMonthly.addItem("")
        selected_index = 0
        previous_pattern = ""
        for value in pattern_list:
            if value.name and value.name != previous_pattern:
                self.cboMonthly.addItem(value.name)
                previous_pattern = value.name

    def btnDelete_Clicked(self):
        # remove pattern
        self.cboMonthly.setCurrentIndex(0)

    def btnClear_Clicked(self):
        # clear adjustments for temp, evap, rain, cond
        for row in range(0,12):
            led = QtGui.QLineEdit('')
            self.tblAdjustments.setItem(row,0,QtGui.QTableWidgetItem(led.text()))
            self.tblAdjustments.setItem(row,1,QtGui.QTableWidgetItem(led.text()))
            self.tblAdjustments.setItem(row,2,QtGui.QTableWidgetItem(led.text()))
            self.tblAdjustments.setItem(row,3,QtGui.QTableWidgetItem(led.text()))
