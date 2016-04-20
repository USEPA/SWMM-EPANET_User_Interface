import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from core.swmm.hydraulics.node import DirectInflowType
from core.swmm.quality import ConcentrationUnitLabels
from ui.SWMM.frmInflowsDesigner import Ui_frmInflows
from ui.SWMM.frmTimeseries import frmTimeseries
from ui.SWMM.frmPatternEditor import frmPatternEditor
from ui.SWMM.frmUnitHydrograph import frmUnitHydrograph


class frmInflows(QtGui.QMainWindow, Ui_frmInflows):

    def __init__(self, parent, node_name):
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
        self.cboDryConstituent.currentIndexChanged.connect(self.cboDryConstituent_currentIndexChanged)
        QtCore.QObject.connect(self.btnAverage, QtCore.SIGNAL("clicked()"), self.btnAverage_Clicked)
        QtCore.QObject.connect(self.btnDryPattern1, QtCore.SIGNAL("clicked()"), self.btnDryPattern1_Clicked)
        QtCore.QObject.connect(self.btnDryPattern2, QtCore.SIGNAL("clicked()"), self.btnDryPattern2_Clicked)
        QtCore.QObject.connect(self.btnDryPattern3, QtCore.SIGNAL("clicked()"), self.btnDryPattern3_Clicked)
        QtCore.QObject.connect(self.btnDryPattern4, QtCore.SIGNAL("clicked()"), self.btnDryPattern4_Clicked)
        QtCore.QObject.connect(self.btnDryPattern5, QtCore.SIGNAL("clicked()"), self.btnDryPattern5_Clicked)
        QtCore.QObject.connect(self.btnDryPattern6, QtCore.SIGNAL("clicked()"), self.btnDryPattern6_Clicked)
        QtCore.QObject.connect(self.btnDryPattern7, QtCore.SIGNAL("clicked()"), self.btnDryPattern7_Clicked)
        QtCore.QObject.connect(self.btnDryPattern8, QtCore.SIGNAL("clicked()"), self.btnDryPattern8_Clicked)
        QtCore.QObject.connect(self.btnUnitHydro1, QtCore.SIGNAL("clicked()"), self.btnUnitHydro1_Clicked)
        QtCore.QObject.connect(self.btnUniHydro2, QtCore.SIGNAL("clicked()"), self.btnUniHydro2_Clicked)
        self.node_id = node_name
        self._parent = parent
        # local data structure to hold the inflow data as pollutant combos change
        self.done_loading = False
        self.previous_constituent_index = -1
        self.local_pollutant_list = []
        self.local_pollutant_list.append('FLOW')
        self.local_pollutant_units = []
        self.local_pollutant_units.append(parent.project.options.flow_units.name)
        pollutants_section = parent.project.find_section("POLLUTANTS")
        for value in pollutants_section.value:
            self.local_pollutant_list.append(value.name)
            self.local_pollutant_units.append(ConcentrationUnitLabels[value.units.value])
        self.local_timeseries_list = []
        self.local_format = []
        self.local_conversion_factor = []
        self.local_scale_factor = []
        self.local_baseline = []
        self.local_baseline_pattern = []
        # local data structure to hold the dry inflow data as pollutant combos change
        self.previous_dry_constituent_index = -1
        self.local_average_list = []
        self.local_dry_pattern_1_list = []
        self.local_dry_pattern_2_list = []
        self.local_dry_pattern_3_list = []
        self.local_dry_pattern_4_list = []
        # now set form
        self.set_from(parent.project)
        self.cboConstituent_currentIndexChanged(0)
        self.cboDryConstituent_currentIndexChanged(0)
        self.setWindowTitle('SWMM Inflows for Node ' + self.node_id)
        self.done_loading = True

    def set_from(self, project):
        # build a local data structure to hold the data at the present, will need to update as pollutants change
        for item in self.local_pollutant_list:
            self.local_timeseries_list.append('')
            self.local_format.append('')
            self.local_conversion_factor.append('')
            self.local_scale_factor.append('')
            self.local_baseline.append('')
            self.local_baseline_pattern.append('')
        for item in self.local_pollutant_list:
            self.local_average_list.append('')
            self.local_dry_pattern_1_list.append('')
            self.local_dry_pattern_2_list.append('')
            self.local_dry_pattern_3_list.append('')
            self.local_dry_pattern_4_list.append('')

        # direct_section = core.swmm.project.DirectInflow()
        # direct_section = project.find_section("INFLOWS")
        self.cboConstituent.clear()
        self.cboDryConstituent.clear()
        self.cboConstituent.addItem('FLOW')
        self.cboDryConstituent.addItem('FLOW')
        self.lblAverage.setText('Average Value (' + project.options.flow_units.name + ')')
        pollutants_section = project.find_section("POLLUTANTS")
        for value in pollutants_section.value:
            self.cboConstituent.addItem(value.name)
            self.cboDryConstituent.addItem(value.name)
        patterns_section = project.find_section("PATTERNS")
        self.cboPattern.clear()
        self.cboDryPattern1.clear()
        self.cboDryPattern2.clear()
        self.cboDryPattern3.clear()
        self.cboDryPattern4.clear()
        self.cboPattern.addItem('')
        self.cboDryPattern1.addItem('')
        self.cboDryPattern2.addItem('')
        self.cboDryPattern3.addItem('')
        self.cboDryPattern4.addItem('')
        for value in patterns_section.value:
            self.cboPattern.addItem(value.name)
            self.cboDryPattern1.addItem(value.name)
            self.cboDryPattern2.addItem(value.name)
            self.cboDryPattern3.addItem(value.name)
            self.cboDryPattern4.addItem(value.name)
        timeseries_section = project.find_section("TIMESERIES")
        self.cboTimeSeries.clear()
        self.cboTimeSeries.addItem('')
        for value in timeseries_section.value:
            self.cboTimeSeries.addItem(value.name)
        self.cboInflowType.clear()
        self.cboInflowType.addItem('CONCEN')
        self.cboInflowType.addItem('MASS')
        self.cboConstituent.setCurrentIndex(0)

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
        dry_section = self._parent.project.find_section("DWF")
        dry_list = dry_section.value[0:]
        for value in dry_list:
            if value.node == self.node_id:
                index = -1
                local_column = -1
                for item in self.local_pollutant_list:
                    index += 1
                    if item == value.constituent:
                        local_column = index
                if local_column > -1:
                    self.local_average_list[local_column] = value.average
                    if value.time_patterns.count(0) > 0:
                        self.local_dry_pattern_1_list[local_column] = value.time_patterns[0]
                    if value.time_patterns.count(0) > 1:
                        self.local_dry_pattern_2_list[local_column] = value.time_patterns[1]
                    if value.time_patterns.count(0) > 2:
                        self.local_dry_pattern_3_list[local_column] = value.time_patterns[2]
                    if value.time_patterns.count(0) > 3:
                        self.local_dry_pattern_4_list[local_column] = value.time_patterns[3]

        # rdii_section = core.swmm.project.RDIInflow()
        rdii_section = project.find_section("RDII")
        hydrograph_section = project.find_section('HYDROGRAPHS')
        self.cboUnitHydro.clear()
        self.cboUnitHydro.addItem('')
        for value in hydrograph_section.value:
            self.cboUnitHydro.addItem(value.group_name)
        rdii_list = rdii_section.value[0:]
        for value in rdii_list:
            if value.node == self.node_id:
                self.txtSewershed.setText(value.sewershed_area)
                selected_index = 0
                for index in range(0,self.cboUnitHydro.count()):
                    if self.cboUnitHydro.itemText(index) == value.hydrograph_group:
                        selected_index = index
                self.cboUnitHydro.setCurrentIndex(selected_index)

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
                if direct_section.value == '':
                    direct_section.value = []
                direct_section.value.append(new_inflow)

        # dry section
        if self.previous_dry_constituent_index > -1:
            index = -1
            local_column = -1
            for item in self.local_pollutant_list:
                index += 1
                if item == self.cboDryConstituent.itemText(self.previous_dry_constituent_index):
                    local_column = index
            if local_column > -1:
                self.local_average_list[local_column] = self.txtAverage.text()
                self.local_dry_pattern_1_list[local_column] = self.cboDryPattern1.currentText()
                self.local_dry_pattern_2_list[local_column] = self.cboDryPattern2.currentText()
                self.local_dry_pattern_3_list[local_column] = self.cboDryPattern3.currentText()
                self.local_dry_pattern_4_list[local_column] = self.cboDryPattern4.currentText()

        dry_section = self._parent.project.find_section("DWF")
        dry_list = dry_section.value[0:]
        index = -1
        for pollutant in self.local_pollutant_list:
            # is this pollutant in the dry inflow list?
            index += 1
            found = False
            for value in dry_list:
                if value.node == self.node_id and value.constituent == pollutant:
                    if index > -1:
                        found = True
                        value.average = self.local_average_list[index]
                        value.time_patterns = []
                        if len(str(self.local_dry_pattern_1_list[index])) > 0:
                            value.time_patterns.append(self.local_dry_pattern_1_list[index])
                        if len(str(self.local_dry_pattern_2_list[index])) > 0:
                            value.time_patterns.append(self.local_dry_pattern_2_list[index])
                        if len(str(self.local_dry_pattern_3_list[index])) > 0:
                            value.time_patterns.append(self.local_dry_pattern_3_list[index])
                        if len(str(self.local_dry_pattern_4_list[index])) > 0:
                            value.time_patterns.append(self.local_dry_pattern_4_list[index])
            if found == False:
                # have to add this dry inflow to the list
                new_inflow = core.swmm.project.DryWeatherInflow()
                new_inflow.node = self.node_id
                new_inflow.constituent = pollutant
                new_inflow.average = self.local_average_list[index]
                new_inflow.baseline_pattern = self.local_baseline_pattern[index]
                new_inflow.time_patterns = []
                if len(str(self.local_dry_pattern_1_list[index])) > 0:
                    new_inflow.time_patterns.append(self.local_dry_pattern_1_list[index])
                if len(str(self.local_dry_pattern_2_list[index])) > 0:
                    new_inflow.time_patterns.append(self.local_dry_pattern_2_list[index])
                if len(str(self.local_dry_pattern_3_list[index])) > 0:
                    new_inflow.time_patterns.append(self.local_dry_pattern_3_list[index])
                if len(str(self.local_dry_pattern_4_list[index])) > 0:
                    new_inflow.time_patterns.append(self.local_dry_pattern_4_list[index])
                if dry_section.value == '':
                    dry_section.value = []
                dry_section.value.append(new_inflow)

        # rainfall dependent infiltration/inflow
        rdii_section = self._parent.project.find_section("RDII")
        rdii_list = rdii_section.value[0:]
        found = False
        for value in rdii_list:
            if value.node == self.node_id:
                found = True
                value.sewershed_area = self.txtSewershed.text()
                value.hydrograph_group = self.cboUnitHydro.currentText()
        if found == False:
            # have to add this rdii to the list
            new_inflow = core.swmm.project.RDIInflow()
            new_inflow.node = self.node_id
            new_inflow.sewershed_area = self.txtSewershed.text()
            new_inflow.hydrograph_group = self.cboUnitHydro.currentText()
            if rdii_section.value == '':
                rdii_section.value = []
            rdii_section.value.append(new_inflow)
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

    def cboConstituent_currentIndexChanged(self, newIndex):
        # put data back to the local data structure
        if self.previous_constituent_index > -1 and self.done_loading:
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

    def cboDryConstituent_currentIndexChanged(self, newIndex):
        # put data back to the local data structure
        if self.previous_dry_constituent_index > -1 and self.done_loading:
            index = -1
            local_column = -1
            for item in self.local_pollutant_list:
                index += 1
                if item == self.cboDryConstituent.itemText(self.previous_dry_constituent_index):
                    local_column = index
            if local_column > -1:
                self.local_average_list[local_column] = self.txtAverage.text()
                self.local_dry_pattern_1_list[local_column] = self.cboDryPattern1.currentText()
                self.local_dry_pattern_2_list[local_column] = self.cboDryPattern2.currentText()
                self.local_dry_pattern_3_list[local_column] = self.cboDryPattern3.currentText()
                self.local_dry_pattern_4_list[local_column] = self.cboDryPattern4.currentText()

        # get data from the local data structure
        index = -1
        local_column = -1
        for item in self.local_pollutant_list:
            index += 1
            if item == self.cboDryConstituent.currentText():
                local_column = index
        if local_column > -1:
            self.txtAverage.setText(self.local_average_list[local_column])
            selected_index = 0
            for index in range(0,self.cboDryPattern1.count()):
                if self.cboDryPattern1.itemText(index) == self.local_dry_pattern_1_list[local_column]:
                    selected_index = index
            self.cboDryPattern1.setCurrentIndex(selected_index)
            selected_index = 0
            for index in range(0,self.cboDryPattern2.count()):
                if self.cboDryPattern2.itemText(index) == self.local_dry_pattern_2_list[local_column]:
                    selected_index = index
            self.cboDryPattern2.setCurrentIndex(selected_index)
            selected_index = 0
            for index in range(0,self.cboDryPattern3.count()):
                if self.cboDryPattern3.itemText(index) == self.local_dry_pattern_3_list[local_column]:
                    selected_index = index
            self.cboDryPattern3.setCurrentIndex(selected_index)
            selected_index = 0
            for index in range(0,self.cboDryPattern4.count()):
                if self.cboDryPattern4.itemText(index) == self.local_dry_pattern_4_list[local_column]:
                    selected_index = index
            self.cboDryPattern4.setCurrentIndex(selected_index)

            self.lblAverage.setText('Average Value (' + self.local_pollutant_units[local_column] + ')')

        self.previous_dry_constituent_index = newIndex

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

    def btnAverage_Clicked(self):
        self.txtAverage.setText('')

    def btnDryPattern1_Clicked(self):
        # edit pattern
        self._frmPatternEditor = frmPatternEditor(self.parent())
        self._frmPatternEditor.show()

    def btnDryPattern2_Clicked(self):
        # edit pattern
        self._frmPatternEditor = frmPatternEditor(self.parent())
        self._frmPatternEditor.show()

    def btnDryPattern3_Clicked(self):
        # edit pattern
        self._frmPatternEditor = frmPatternEditor(self.parent())
        self._frmPatternEditor.show()

    def btnDryPattern4_Clicked(self):
        # edit pattern
        self._frmPatternEditor = frmPatternEditor(self.parent())
        self._frmPatternEditor.show()

    def btnDryPattern5_Clicked(self):
        self.cboDryPattern1.setCurrentIndex(0)

    def btnDryPattern6_Clicked(self):
        self.cboDryPattern2.setCurrentIndex(0)

    def btnDryPattern7_Clicked(self):
        self.cboDryPattern3.setCurrentIndex(0)

    def btnDryPattern8_Clicked(self):
        self.cboDryPattern4.setCurrentIndex(0)

    def btnUnitHydro1_Clicked(self):
        # edit unit hydrograph
        self._frmUnitHydrograph = frmUnitHydrograph(self.parent())
        self._frmUnitHydrograph.show()

    def btnUniHydro2_Clicked(self):
        self.cboUnitHydro.setCurrentIndex(0)

