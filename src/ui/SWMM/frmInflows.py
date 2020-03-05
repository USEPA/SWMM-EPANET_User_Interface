import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from core.swmm.hydraulics.node import DirectInflow, DirectInflowType, RDIInflow, DryWeatherInflow
from core.swmm.quality import ConcentrationUnitLabels
from ui.SWMM.frmInflowsDesigner import Ui_frmInflows
from ui.SWMM.frmTimeseries import frmTimeseries
from ui.SWMM.frmPatternEditor import frmPatternEditor
from ui.SWMM.frmUnitHydrograph import frmUnitHydrograph


class frmInflows(QMainWindow, Ui_frmInflows):

    def __init__(self, main_form, node_name):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/directinfloweditor.htm"
        self.units = main_form.project.options.flow_units.value
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.tabInflows.currentChanged.connect(self.tabInflows_currentTabChanged)
        self.cboConstituent.currentIndexChanged.connect(self.cboConstituent_currentIndexChanged)
        self.btnBaseline.clicked.connect(self.btnBaseline_Clicked)
        self.btnTimeseriesDelete.clicked.connect(self.btnTimeseriesDelete_Clicked)
        self.btnPatternDelete.clicked.connect(self.btnPatternDelete_Clicked)
        self.btnTimeseries.clicked.connect(self.btnTimeseries_Clicked)
        self.btnPattern.clicked.connect(self.btnPattern_Clicked)
        self.cboDryConstituent.currentIndexChanged.connect(self.cboDryConstituent_currentIndexChanged)
        self.btnAverage.clicked.connect(self.btnAverage_Clicked)
        self.btnDryPattern1.clicked.connect(self.btnDryPattern1_Clicked)
        self.btnDryPattern2.clicked.connect(self.btnDryPattern2_Clicked)
        self.btnDryPattern3.clicked.connect(self.btnDryPattern3_Clicked)
        self.btnDryPattern4.clicked.connect(self.btnDryPattern4_Clicked)
        self.btnDryPattern5.clicked.connect(self.btnDryPattern5_Clicked)
        self.btnDryPattern6.clicked.connect(self.btnDryPattern6_Clicked)
        self.btnDryPattern7.clicked.connect(self.btnDryPattern7_Clicked)
        self.btnDryPattern8.clicked.connect(self.btnDryPattern8_Clicked)
        self.btnUnitHydro1.clicked.connect(self.btnUnitHydro1_Clicked)
        self.btnUniHydro2.clicked.connect(self.btnUniHydro2_Clicked)
        self.node_name = node_name
        self._main_form = main_form
        self.project = main_form.project

        # local data structure to hold the inflow data as pollutant combos change
        self.done_loading = False
        self.previous_constituent_index = -1
        self.local_pollutant_list = []
        self.local_pollutant_list.append('FLOW')
        self.local_pollutant_units = []
        self.local_pollutant_units.append(self.project.options.flow_units.name)
        for value in self.project.pollutants.value:
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
        self.set_from(self.project)
        self.cboConstituent_currentIndexChanged(0)
        self.cboDryConstituent_currentIndexChanged(0)
        self.setWindowTitle('SWMM Inflows for Node ' + self.node_name)
        self.done_loading = True

        if (main_form.program_settings.value("Geometry/" + "frmInflows_geometry") and
                main_form.program_settings.value("Geometry/" + "frmInflows_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmInflows_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmInflows_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        self.project = project
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

        for value in self.project.inflows.value:
            if value.node == self.node_name:
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
        pat_id = ''
        for value in self.project.dwf.value:
            if value.node == self.node_name:
                index = -1
                local_column = -1
                for item in self.local_pollutant_list:
                    index += 1
                    if item == value.constituent:
                        local_column = index
                if local_column > -1:
                    self.local_average_list[local_column] = value.average
                    if len(value.time_patterns) > 0:
                        if value.time_patterns[0]:
                            pat_id = value.time_patterns[0].strip("\"")
                        else:
                            pat_id = u''
                        self.local_dry_pattern_1_list[local_column] = pat_id
                        self.cboDryPattern1.setCurrentIndex(self.cboDryPattern1.findText(pat_id))
                    if len(value.time_patterns) > 1:
                        if value.time_patterns[1]:
                            pat_id = value.time_patterns[1].strip("\"")
                        else:
                            pat_id = u''
                        self.local_dry_pattern_2_list[local_column] = pat_id
                        self.cboDryPattern2.setCurrentIndex(self.cboDryPattern2.findText(pat_id))
                    if len(value.time_patterns) > 2:
                        if value.time_patterns[2]:
                            pat_id = value.time_patterns[2].strip("\"")
                        else:
                            pat_id = u''
                        self.local_dry_pattern_3_list[local_column] = pat_id
                        self.cboDryPattern3.setCurrentIndex(self.cboDryPattern3.findText(pat_id))
                    if len(value.time_patterns) > 3:
                        if value.time_patterns[3]:
                            pat_id = value.time_patterns[3].strip("\"")
                        else:
                            pat_id = u''
                        self.local_dry_pattern_4_list[local_column] = pat_id
                        self.cboDryPattern4.setCurrentIndex(self.cboDryPattern4.findText(pat_id))

        # rdii_section = core.swmm.project.RDIInflow()
        rdii_section = project.find_section("RDII")
        hydrograph_section = project.find_section('HYDROGRAPHS')
        self.cboUnitHydro.clear()
        self.cboUnitHydro.addItem('')
        for value in hydrograph_section.value:
            self.cboUnitHydro.addItem(value.name)
        rdii_list = rdii_section.value[0:]
        for value in rdii_list:
            if value.node == self.node_name:
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
                orig_conv_factor = self.local_conversion_factor[local_column]
                orig_baseline = self.local_baseline[local_column]
                orig_scale_factor = self.local_scale_factor[local_column]
                orig_timeseries_list = self.local_timeseries_list[local_column]
                orig_baseline_pattern = self.local_baseline_pattern[local_column]
                orig_format = self.local_format[local_column]
                if orig_format == '':
                    orig_format = DirectInflowType.CONCEN

                self.local_conversion_factor[local_column] = self.txtUnitsFactor.text()
                self.local_baseline[local_column] = self.txtBaseline.text()
                self.local_scale_factor[local_column] = self.txtScaleFactor.text()
                self.local_timeseries_list[local_column] = self.cboTimeSeries.currentText()
                self.local_baseline_pattern[local_column] = self.cboPattern.currentText()
                if self.cboInflowType.currentIndex() == 0:
                    self.local_format[local_column] = DirectInflowType.CONCEN
                elif self.cboInflowType.currentIndex() == 1:
                    self.local_format[local_column] = DirectInflowType.MASS

                if orig_conv_factor != self.local_conversion_factor[local_column] or \
                    orig_baseline != self.local_baseline[local_column] or \
                    orig_scale_factor != self.local_scale_factor[local_column] or \
                    orig_timeseries_list != self.local_timeseries_list[local_column] or \
                    orig_baseline_pattern != self.local_baseline_pattern[local_column] or \
                    orig_format != self.local_format[local_column]:
                    self._main_form.mark_project_as_unsaved()

        direct_section = self.project.find_section("INFLOWS")
        direct_list = direct_section.value[0:]
        index = -1
        for pollutant in self.local_pollutant_list:
            # is this pollutant in the inflow list?
            index += 1
            found = False
            for value in direct_list:
                if value.node == self.node_name and value.constituent == pollutant:
                    if index > -1:
                        found = True
                        orig_timeseries = value.timeseries
                        orig_format = value.format
                        orig_conv_factor = value.conversion_factor
                        orig_scale_factor = value.scale_factor
                        orig_baseline = value.baseline
                        orig_baseline_pattern = value.baseline_pattern

                        value.timeseries = self.local_timeseries_list[index]
                        value.format = self.local_format[index]
                        value.conversion_factor = self.local_conversion_factor[index]
                        value.scale_factor = self.local_scale_factor[index]
                        value.baseline = self.local_baseline[index]
                        value.baseline_pattern = self.local_baseline_pattern[index]

                        if orig_timeseries != value.timeseries or \
                            orig_format != value.format or \
                            orig_conv_factor != value.conversion_factor or \
                            orig_scale_factor != value.scale_factor or \
                            orig_baseline != value.baseline or \
                            orig_baseline_pattern != value.baseline_pattern:
                            self._main_form.mark_project_as_unsaved()

            if not found:
                # have to add this inflow to the list
                new_inflow = DirectInflow()
                new_inflow.node = self.node_name
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
                self._main_form.mark_project_as_unsaved()

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

        dry_section = self._main_form.project.find_section("DWF")
        dry_list = dry_section.value[0:]
        index = -1
        for pollutant in self.local_pollutant_list:
            # is this pollutant in the dry inflow list?
            index += 1
            found = False
            for value in dry_list:
                if value.node == self.node_name and value.constituent == pollutant:
                    if index > -1:
                        found = True

                        orig_average = value.average
                        orig_time_patterns = value.time_patterns

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

                        if orig_average != value.average or \
                            orig_time_patterns != value.time_patterns:
                            self._main_form.mark_project_as_unsaved()

            if not found:
                # have to add this dry inflow to the list
                new_inflow = DryWeatherInflow()
                new_inflow.node = self.node_name
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
                self._main_form.mark_project_as_unsaved()

        # rainfall dependent infiltration/inflow
        rdii_section = self._main_form.project.find_section("RDII")
        rdii_list = rdii_section.value[0:]
        found = False
        for value in rdii_list:
            if value.node == self.node_name:
                found = True
                if value.sewershed_area != self.txtSewershed.text() or \
                    value.hydrograph_group != self.cboUnitHydro.currentText():
                    self._main_form.mark_project_as_unsaved()
                value.sewershed_area = self.txtSewershed.text()
                value.hydrograph_group = self.cboUnitHydro.currentText()
        if not found:
            # have to add this rdii to the list
            new_inflow = RDIInflow()
            new_inflow.node = self.node_name
            new_inflow.sewershed_area = self.txtSewershed.text()
            new_inflow.hydrograph_group = self.cboUnitHydro.currentText()
            if rdii_section.value == '':
                rdii_section.value = []
            rdii_section.value.append(new_inflow)
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmInflows_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmInflows_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmInflows_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmInflows_state", self.saveState())
        self.close()

    def tabInflows_currentTabChanged(self):

        tab_index = self.tabInflows.currentIndex()
        if tab_index == 0:
            self.lblNotes.setText("If Baseline or Time Series is left blank its value is 0. If Baseline Pattern is left blank its value is 1.0.")
            self.help_topic = "swmm/src/src/directinfloweditor.htm"
        elif tab_index == 1:
            self.lblNotes.setText("If Average Value is left blank its value is 0. Any Time Pattern left blank defaults to a constant value of 1.0.")
            self.help_topic = "swmm/src/src/dryweatherinfloweditor.htm"
        elif tab_index == 2:
            self.lblNotes.setText("Leave the Unit Hydrograph Group field blank to remove any RDII inflow at this node.")
            self.help_topic = "swmm/src/src/rdiiinfloweditor.htm"

        if self.units < 4:
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
                if self.cboInflowType.currentIndex() == 0:
                    self.local_format[local_column] = DirectInflowType.CONCEN
                elif self.cboInflowType.currentIndex() == 1:
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
            if self.local_format[local_column] == DirectInflowType.CONCEN:
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
        new_name = ''
        if self.cboTimeSeries.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Time Series"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmTimeseries = frmTimeseries(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboTimeSeries.currentText())
            self._frmTimeseries = frmTimeseries(self._main_form, edit_these)
        # edit timeseries
        self._frmTimeseries.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmTimeseries.show()
        if self.cboTimeSeries.currentIndex() == 0:
            self.cboTimeSeries.addItem(new_name)
            self.cboTimeSeries.setCurrentIndex(self.cboTimeSeries.count()-1)

    def btnPattern_Clicked(self):
        new_name = ''
        if self.cboPattern.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Time Patterns"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmPatternEditor = frmPatternEditor(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboPattern.currentText())
            self._frmPatternEditor = frmPatternEditor(self._main_form, edit_these)
        # edit pattern
        self._frmPatternEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmPatternEditor.show()
        if self.cboPattern.currentIndex() == 0:
            self.cboPattern.addItem(new_name)
            self.cboPattern.setCurrentIndex(self.cboPattern.count()-1)

    def btnAverage_Clicked(self):
        self.txtAverage.setText('')

    def btnDryPattern1_Clicked(self):
        new_name = ''
        if self.cboDryPattern1.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Time Patterns"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmPatternEditor = frmPatternEditor(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboDryPattern1.currentText())
            self._frmPatternEditor = frmPatternEditor(self._main_form, edit_these)
        # edit pattern
        self._frmPatternEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmPatternEditor.show()
        if self.cboDryPattern1.currentIndex() == 0:
            self.cboDryPattern1.addItem(new_name)
            self.cboDryPattern1.setCurrentIndex(self.cboDryPattern1.count()-1)

    def btnDryPattern2_Clicked(self):
        new_name = ''
        if self.cboDryPattern2.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Time Patterns"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmPatternEditor = frmPatternEditor(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboDryPattern2.currentText())
            self._frmPatternEditor = frmPatternEditor(self._main_form, edit_these)
        # edit pattern
        self._frmPatternEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmPatternEditor.show()
        if self.cboDryPattern2.currentIndex() == 0:
            self.cboDryPattern2.addItem(new_name)
            self.cboDryPattern2.setCurrentIndex(self.cboDryPattern2.count()-1)

    def btnDryPattern3_Clicked(self):
        new_name = ''
        if self.cboDryPattern3.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Time Patterns"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmPatternEditor = frmPatternEditor(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboDryPattern3.currentText())
            self._frmPatternEditor = frmPatternEditor(self._main_form, edit_these)
        # edit pattern
        self._frmPatternEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmPatternEditor.show()
        if self.cboDryPattern3.currentIndex() == 0:
            self.cboDryPattern3.addItem(new_name)
            self.cboDryPattern3.setCurrentIndex(self.cboDryPattern3.count()-1)

    def btnDryPattern4_Clicked(self):
        new_name = ''
        if self.cboDryPattern4.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Time Patterns"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmPatternEditor = frmPatternEditor(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboDryPattern4.currentText())
            self._frmPatternEditor = frmPatternEditor(self._main_form, edit_these)
        # edit pattern
        self._frmPatternEditor.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmPatternEditor.show()
        if self.cboDryPattern4.currentIndex() == 0:
            self.cboDryPattern4.addItem(new_name)
            self.cboDryPattern4.setCurrentIndex(self.cboDryPattern4.count()-1)

    def btnDryPattern5_Clicked(self):
        self.cboDryPattern1.setCurrentIndex(0)

    def btnDryPattern6_Clicked(self):
        self.cboDryPattern2.setCurrentIndex(0)

    def btnDryPattern7_Clicked(self):
        self.cboDryPattern3.setCurrentIndex(0)

    def btnDryPattern8_Clicked(self):
        self.cboDryPattern4.setCurrentIndex(0)

    def btnUnitHydro1_Clicked(self):
        # send in currently selected UnitHydrograph
        new_name = ''
        if self.cboUnitHydro.currentIndex() == 0:
            # create a new one
            item_type = self._main_form.tree_types["Unit Hydrographs"]
            new_item = item_type()
            new_item.name = self._main_form.new_item_name(item_type)
            new_name = new_item.name
            self._frmUnitHydrograph = frmUnitHydrograph(self._main_form,[],new_item)
        else:
            edit_these = []
            edit_these.append(self.cboUnitHydro.currentText())
            self._frmUnitHydrograph = frmUnitHydrograph(self._main_form, edit_these)
        # edit UnitHydrograph
        self._frmUnitHydrograph.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmUnitHydrograph.show()
        if self.cboUnitHydro.currentIndex() == 0:
            self.cboUnitHydro.addItem(new_name)
            self.cboUnitHydro.setCurrentIndex(self.cboUnitHydro.count()-1)

    def btnUniHydro2_Clicked(self):
        self.cboUnitHydro.setCurrentIndex(0)

