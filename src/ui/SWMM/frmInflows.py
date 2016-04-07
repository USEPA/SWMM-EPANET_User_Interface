import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from core.swmm.hydraulics.node import DirectInflowType
from ui.SWMM.frmInflowsDesigner import Ui_frmInflows
from ui.SWMM.frmTimeseries import frmTimeseries
from ui.SWMM.frmPatternEditor import frmPatternEditor


class frmInflows(QtGui.QMainWindow, Ui_frmInflows):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.tabInflows.currentChanged.connect(self.tabInflows_currentTabChanged)
        self.cboConstituent.currentIndexChanged.connect(self.cboConstituent_currentIndexChanged)
        QtCore.QObject.connect(self.btnBaseline, QtCore.SIGNAL("clicked()"), self.btnBaseline_Clicked)
        QtCore.QObject.connect(self.btnTimeseriesDelete, QtCore.SIGNAL("clicked()"), self.btnTimeseriesDelete_Clicked)
        QtCore.QObject.connect(self.btnPatternDelete, QtCore.SIGNAL("clicked()"), self.btnPatternDelete_Clicked)
        QtCore.QObject.connect(self.btnTimeseries, QtCore.SIGNAL("clicked()"), self.btnTimeseries_Clicked)
        QtCore.QObject.connect(self.btnPattern, QtCore.SIGNAL("clicked()"), self.btnPattern_Clicked)
        self._parent = parent
        # local data structure to hold the data as tabs/pollutant combos change
        self.previous_constituent_index = -1
        self.local_pollutant_list = []
        self.local_timeseries_list = []
        self.local_format = []
        self.local_conversion_factor = []
        self.local_scale_factor = []
        self.local_baseline = []
        self.local_baseline_pattern = []
        self.set_from(parent.project)
        self.node_id = '10'  # will need to get this connected, hard code for now
        self.setWindowTitle('SWMM Inflows for Node ' + self.node_id)

    def set_from(self, project):
        # direct_section = core.swmm.project.DirectInflow()
        # direct_section = project.find_section("INFLOWS")
        self.cboConstituent.clear()
        self.local_pollutant_list = []
        self.cboConstituent.addItem('FLOW')
        self.local_pollutant_list.append('FLOW')
        pollutants_section = project.find_section("POLLUTANTS")
        for value in pollutants_section.value:
            self.cboConstituent.addItem(value.name)
            self.local_pollutant_list.append(value.name)
        patterns_section = project.find_section("PATTERNS")
        self.cboPattern.clear()
        self.cboPattern.addItem('')
        for value in patterns_section.value:
            self.cboPattern.addItem(value.name)
        timeseries_section = project.find_section("TIMESERIES")
        self.cboTimeSeries.clear()
        self.cboTimeSeries.addItem('')
        for value in timeseries_section.value:
            self.cboTimeSeries.addItem(value.name)
        self.cboInflowType.clear()
        self.cboInflowType.addItem('CONCEN')
        self.cboInflowType.addItem('MASS')
        self.cboConstituent.setCurrentIndex(0)

        # build a local data structure to hold the data at the present, will need to update as tab/pollutants change
        for item in self.local_pollutant_list:
            self.local_timeseries_list.append('')
            self.local_format.append('')
            self.local_conversion_factor.append('')
            self.local_scale_factor.append('')
            self.local_baseline.append('')
            self.local_baseline_pattern.append('')
        direct_section = self._parent.project.find_section("INFLOWS")
        direct_list = direct_section.value[0:]
        for value in direct_list:
            if value.node == self.node_id:
                index = -1
                local_column = -1
                for item in self.local_pollutant_list:
                    index += 1
                    if item == value.constituent:
                        local_column = index
                if local_column > -1:
                    self.local_timeseries_list[local_column] = value.timeseries
                    self.local_format[local_column] = value.format
                    self.local_conversion_factor[local_column] = value.conversion_factor
                    self.local_scale_factor[local_column] = value.scale_factor
                    self.local_baseline[local_column] = value.baseline
                    self.local_baseline_pattern[local_column] = value.baseline_pattern

        # dry_section = core.swmm.project.DryWeatherInflow()
        # dry_section = project.find_section("DWF")
        # rdii_section = core.swmm.project.RDIInflow()
        # rdii_section = project.find_section("RDII")

    def cmdOK_Clicked(self):
        # put data back to the local data structure
        if self.previous_constituent_index > -1:
            index = -1
            local_column = -1
            for item in self.local_pollutant_list:
                index += 1
                if item == self.cboConstituent.itemText(self.previous_constituent_index):
                    local_column = index
            if local_column > -1:
                self.local_conversion_factor[local_column] = self.txtUnitsFactor.text()
                self.local_baseline[local_column] = self.txtBaseline.text()
                self.local_scale_factor[local_column] = self.txtScaleFactor.text()
                self.local_timeseries_list[local_column] = self.cboTimeSeries.currentText()
                self.local_baseline_pattern[local_column] = self.cboPattern.currentText()
                if self.cboInflowType.currentIndex == 0:
                    self.local_format[local_column] = DirectInflowType.CONCENTRATION
                elif self.cboInflowType.currentIndex == 1:
                    self.local_format[local_column] = DirectInflowType.MASS

        direct_section = self._parent.project.find_section("INFLOWS")
        direct_list = direct_section.value[0:]
        index = -1
        for pollutant in self.local_pollutant_list:
            # is this pollutant in the inflow list?
            index += 1
            found = False
            for value in direct_list:
                if value.node == self.node_id and value.constituent == pollutant:
                    if index > -1:
                        found = True
                        value.timeseries = self.local_timeseries_list[index]
                        value.format = self.local_format[index]
                        value.conversion_factor = self.local_conversion_factor[index]
                        value.scale_factor = self.local_scale_factor[index]
                        value.baseline = self.local_baseline[index]
                        value.baseline_pattern = self.local_baseline_pattern[index]
            if found == False:
                # have to add this inflow to the list
                new_inflow = core.swmm.project.DirectInflow()
                new_inflow.node = self.node_id
                new_inflow.constituent = pollutant
                new_inflow.timeseries = self.local_timeseries_list[index]
                new_inflow.format = self.local_format[index]
                new_inflow.conversion_factor = self.local_conversion_factor[index]
                new_inflow.scale_factor = self.local_scale_factor[index]
                new_inflow.baseline = self.local_baseline[index]
                new_inflow.baseline_pattern = self.local_baseline_pattern[index]
                direct_section.value.append(new_inflow)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def tabInflows_currentTabChanged(self):

        tab_index = self.tabInflows.currentIndex()
        if tab_index == 0:
            self.lblNotes.setText("If Baseline or Time Series is left blank its value is 0. If Baseline Pattern is left blank its value is 1.0.")
        elif tab_index == 1:
            self.lblNotes.setText("If Average Value is left blank its value is 0. Any Time Pattern left blank defaults to a constant value of 1.0.")
        elif tab_index == 2:
            self.lblNotes.setText("Leave the Unit Hydrograph Group field blank to remove any RDII inflow at this node.")

        units = 1

        if units == 1:
            self.lblSewershed.setText('Sewershed Area (acres)')
        else:
            self.lblSewershed.setText('Sewershed Area (hectares)')

        # add flow units to average value lblAverage
        self.lblAverage.setText('Average Value ()')

    def cboConstituent_currentIndexChanged(self, newIndex):
        # put data back to the local data structure
        if self.previous_constituent_index > -1:
            index = -1
            local_column = -1
            for item in self.local_pollutant_list:
                index += 1
                if item == self.cboConstituent.itemText(self.previous_constituent_index):
                    local_column = index
            if local_column > -1:
                self.local_conversion_factor[local_column] = self.txtUnitsFactor.text()
                self.local_baseline[local_column] = self.txtBaseline.text()
                self.local_scale_factor[local_column] = self.txtScaleFactor.text()
                self.local_timeseries_list[local_column] = self.cboTimeSeries.currentText()
                self.local_baseline_pattern[local_column] = self.cboPattern.currentText()
                if self.cboInflowType.currentIndex == 0:
                    self.local_format[local_column] = DirectInflowType.CONCENTRATION
                elif self.cboInflowType.currentIndex == 1:
                    self.local_format[local_column] = DirectInflowType.MASS

        # set the form
        if newIndex == 0:
            self.cboInflowType.setVisible(False)
            self.txtUnitsFactor.setVisible(False)
            self.lblInflowType.setVisible(False)
            self.lblUnitsFactor.setVisible(False)
        else:
            self.cboInflowType.setVisible(True)
            self.txtUnitsFactor.setVisible(True)
            self.lblInflowType.setVisible(True)
            self.lblUnitsFactor.setVisible(True)

        # get data from the local data structure
        index = -1
        local_column = -1
        for item in self.local_pollutant_list:
            index += 1
            if item == self.cboConstituent.currentText():
                local_column = index
        if local_column > -1:
            self.txtUnitsFactor.setText(self.local_conversion_factor[local_column])
            self.txtBaseline.setText(self.local_baseline[local_column])
            self.txtScaleFactor.setText(self.local_scale_factor[local_column])
            selected_index = 0
            for index in range(0,self.cboTimeSeries.count()):
                if self.cboTimeSeries.itemText(index) == self.local_timeseries_list[local_column]:
                    selected_index = index
            self.cboTimeSeries.setCurrentIndex(selected_index)
            selected_index = 0
            for index in range(0,self.cboPattern.count()):
                if self.cboPattern.itemText(index) == self.local_baseline_pattern[local_column]:
                    selected_index = index
            self.cboPattern.setCurrentIndex(selected_index)
            if self.local_format[local_column] == DirectInflowType.CONCENTRATION:
                self.cboInflowType.setCurrentIndex(0)
            elif self.local_format[local_column] == DirectInflowType.MASS:
                self.cboInflowType.setCurrentIndex(1)

        self.previous_constituent_index = newIndex

    def btnBaseline_Clicked(self):
        self.txtBaseline.setText('')

    def btnTimeseriesDelete_Clicked(self):
        self.cboTimeSeries.setCurrentIndex(0)

    def btnPatternDelete_Clicked(self):
        self.cboPattern.setCurrentIndex(0)

    def btnTimeseries_Clicked(self):
        # send in currently selected timeseries
        self._frmTimeseries = frmTimeseries(self.parent())
        self._frmTimeseries.show()

    def btnPattern_Clicked(self):
        # edit pattern
        self._frmPatternEditor = frmPatternEditor(self.parent())
        self._frmPatternEditor.show()

