import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem, QComboBox
from ui.SWMM.frmLandUsesDesigner import Ui_frmLandUsesEditor
import ui.convenience
from core.swmm.quality import Buildup
from core.swmm.quality import Landuse
from core.swmm.quality import BuildupFunction
from core.swmm.quality import Normalizer
from core.swmm.quality import Buildup
from core.swmm.quality import Washoff
from core.swmm.quality import WashoffFunction


class frmLandUses(QMainWindow, Ui_frmLandUsesEditor):
    def __init__(self, main_form, edit_these, new_item):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/landuseeditorgeneralpage.htm"
        self.setupUi(self)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.landuses

        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.tabLanduse.currentChanged.connect(self.tabLanduse_currentTabChanged)
        self.tblGeneral.currentCellChanged.connect(self.tblGeneral_currentCellChanged)
        self.tblBuildup.currentCellChanged.connect(self.tblBuildup_currentCellChanged)
        self.tblWashoff.currentCellChanged.connect(self.tblWashoff_currentCellChanged)
        self.tblGeneral.setColumnCount(1)
        self.tblGeneral.setRowCount(6)
        header_labels = ["Value"]
        self.tblGeneral.setHorizontalHeaderLabels(header_labels)
        self.tblGeneral.setVerticalHeaderLabels(("Land Use Name","Description","STREET SWEEPING","    Interval","    Availability","    Last Swept"))
        self.local_pollutant_list = []
        for value in self.project.pollutants.value:
            self.local_pollutant_list.append(value.name)
        self.tblBuildup.setColumnCount(self.local_pollutant_list.__len__())
        self.tblBuildup.setRowCount(7)
        self.tblBuildup.setHorizontalHeaderLabels(self.local_pollutant_list)
        self.tblBuildup.setVerticalHeaderLabels(("Function","Max. Buildup","Rate Constant","Power/Sat. Constant","Normalizer","Scaling Factor","Time Series"))
        self.tblWashoff.setColumnCount(self.local_pollutant_list.__len__())
        self.tblWashoff.setRowCount(5)
        self.tblWashoff.setHorizontalHeaderLabels(self.local_pollutant_list)
        self.tblWashoff.setVerticalHeaderLabels(("Function","Coefficient","Exponent","Cleaning Effic.","BMP Effic."))
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)
        self.resize(400,450)

    def set_from(self, land_use):
        if not isinstance(land_use, Landuse):
            land_use = self.section.value[land_use]
        if isinstance(land_use, Landuse):
            # this is the land_use we want to edit
            self.editing_item = land_use
            led = QLineEdit(land_use.name)
            self.tblGeneral.setItem(0,0,QTableWidgetItem(led.text()))
            led = QLineEdit(land_use.comment)
            self.tblGeneral.setItem(1,0,QTableWidgetItem(led.text()))
            led = QLineEdit(land_use.last_swept)
            self.tblGeneral.setItem(3,0,QTableWidgetItem(led.text()))
            led = QLineEdit(land_use.street_sweeping_availability)
            self.tblGeneral.setItem(4,0,QTableWidgetItem(led.text()))
            led = QLineEdit(land_use.street_sweeping_interval)
            self.tblGeneral.setItem(5,0,QTableWidgetItem(led.text()))
            self.tblGeneral.setCurrentCell(0,0)
            local_column = -1
            for pollutant in self.local_pollutant_list:
                local_column += 1
                pollutant_found = False
                for buildup in self.project.buildup.value:
                    if buildup.land_use_name == land_use.name and  buildup.pollutant == pollutant:
                        # this is the land_use we want to edit
                        pollutant_found = True
                        break
                if not pollutant_found:
                    buildup = Buildup()
                    buildup.land_use_name = land_use.name
                    buildup.pollutant = pollutant
                    self.project.buildup.value.append(buildup)

                combobox = QComboBox()
                ui.convenience.set_combo_items(type(buildup.function), combobox)
                ui.convenience.set_combo(combobox, buildup.function)  # BuildupFunction.POW
                self.tblBuildup.setCellWidget(0, local_column, combobox)
                led = QLineEdit(buildup.max_buildup)
                self.tblBuildup.setItem(1, local_column,QTableWidgetItem(led.text()))
                led = QLineEdit(buildup.rate_constant)
                self.tblBuildup.setItem(2, local_column,QTableWidgetItem(led.text()))
                led = QLineEdit(buildup.power_sat_constant)
                self.tblBuildup.setItem(3, local_column,QTableWidgetItem(led.text()))
                combobox = QComboBox()
                ui.convenience.set_combo_items(type(buildup.normalizer), combobox)
                ui.convenience.set_combo(combobox, buildup.normalizer)   # Normalizer.AREA
                self.tblBuildup.setCellWidget(4, local_column, combobox)
                led = QLineEdit(buildup.scaling_factor)
                self.tblBuildup.setItem(5, local_column, QTableWidgetItem(led.text()))
                combobox = QComboBox()
                combobox.addItem('')
                selected_index = 0
                for value in self.project.timeseries.value:
                    combobox.addItem(value.name)
                    if buildup.timeseries == value.name:
                        selected_index = int(combobox.count())-1
                combobox.setCurrentIndex(selected_index)
                self.tblBuildup.setCellWidget(6, local_column, combobox)
            self.tblBuildup.setCurrentCell(0,0)
            local_column = -1
            for pollutant in self.local_pollutant_list:
                local_column += 1
                pollutant_found = False
                for washoff in self.project.washoff.value:
                    if washoff.land_use_name == land_use.name and washoff.pollutant == pollutant:
                        # this is the land_use we want to edit
                        pollutant_found = True
                        break
                if not pollutant_found:
                    washoff = Washoff()
                    washoff.land_use_name = land_use.name
                    washoff.pollutant = pollutant
                    self.project.washoff.value.append(washoff)

                combobox = QComboBox()
                ui.convenience.set_combo_items(type(washoff.function), combobox)
                ui.convenience.set_combo(combobox, washoff.function)  # WashoffFunction.EXP
                self.tblWashoff.setCellWidget(0,local_column, combobox)
                led = QLineEdit(washoff.coefficient)
                self.tblWashoff.setItem(1,local_column,QTableWidgetItem(led.text()))
                led = QLineEdit(washoff.exponent)
                self.tblWashoff.setItem(2,local_column,QTableWidgetItem(led.text()))
                led = QLineEdit(washoff.cleaning_efficiency)
                self.tblWashoff.setItem(3,local_column,QTableWidgetItem(led.text()))
                led = QLineEdit(washoff.bmp_efficiency)
                self.tblWashoff.setItem(4,local_column,QTableWidgetItem(led.text()))
            self.tblWashoff.setCurrentCell(0,0)

    def cmdOK_Clicked(self):
        new_name = self.tblGeneral.item(0,0).text()
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            buildup_found = False
            for buildup in self.project.buildup.value:
                if buildup.land_use_name == self.editing_item.name and pollutant == buildup.pollutant:
                    # put this back in place
                    buildup_found = True

                    orig_land_use_name = buildup.land_use_name
                    orig_function = buildup.function
                    orig_max_buildup = buildup.max_buildup
                    orig_rate_constant = buildup.rate_constant
                    orig_power_sat_constant = buildup.power_sat_constant
                    orig_normalizer = buildup.normalizer
                    orig_scaling_factor = buildup.scaling_factor
                    orig_timeseries = buildup.timeseries

                    combobox = self.tblBuildup.cellWidget(0,pollutant_count)
                    buildup.land_use_name = new_name
                    buildup.function = BuildupFunction[combobox.currentText()]
                    buildup.max_buildup = self.tblBuildup.item(1,pollutant_count).text()
                    buildup.rate_constant = self.tblBuildup.item(2,pollutant_count).text()
                    buildup.power_sat_constant = self.tblBuildup.item(3,pollutant_count).text()
                    combobox = self.tblBuildup.cellWidget(4,pollutant_count)
                    buildup.normalizer = Normalizer[combobox.currentText()]
                    buildup.scaling_factor = self.tblBuildup.item(5,pollutant_count).text()
                    combobox = self.tblBuildup.cellWidget(6,pollutant_count)
                    buildup.timeseries = combobox.currentText()

                    if orig_land_use_name != buildup.land_use_name or \
                        orig_function != buildup.function or \
                        orig_max_buildup != buildup.max_buildup or \
                        orig_rate_constant != buildup.rate_constant or \
                        orig_power_sat_constant != buildup.power_sat_constant or \
                        orig_normalizer != buildup.normalizer or \
                        orig_scaling_factor != buildup.scaling_factor or \
                        orig_timeseries != buildup.timeseries and buildup.function == BuildupFunction.EXP:
                        self._main_form.mark_project_as_unsaved()

            if not buildup_found:
                # add new record
                new_buildup = Buildup()
                new_buildup.land_use_name = new_name
                new_buildup.pollutant = pollutant
                combobox = self.tblBuildup.cellWidget(0,pollutant_count)
                new_buildup.function = BuildupFunction[combobox.currentText()]
                new_buildup.max_buildup = self.tblBuildup.item(1,pollutant_count).text()
                new_buildup.rate_constant = self.tblBuildup.item(2,pollutant_count).text()
                new_buildup.power_sat_constant = self.tblBuildup.item(3,pollutant_count).text()
                combobox = self.tblBuildup.cellWidget(4,pollutant_count)
                new_buildup.normalizer = Normalizer[combobox.currentText()]
                new_buildup.scaling_factor = self.tblBuildup.item(5,pollutant_count).text()
                combobox = self.tblBuildup.cellWidget(6,pollutant_count)
                new_buildup.timeseries = combobox.currentText()
                if self.project.buildup.value == '':
                    self.project.buildup.value = []
                self.project.buildup.value.append(new_buildup)
                self._main_form.mark_project_as_unsaved()

        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            washoff_found = False
            for washoff in self.project.washoff.value:
                if washoff.land_use_name == self.editing_item.name and pollutant == washoff.pollutant:
                    # put this back in place
                    washoff_found = True

                    orig_land_use_name = washoff.land_use_name
                    orig_function = washoff.function
                    orig_coefficient = washoff.coefficient
                    orig_exponent = washoff.exponent
                    orig_cleaning_efficiency = washoff.cleaning_efficiency
                    orig_bmp_efficiency = washoff.bmp_efficiency

                    combobox = self.tblWashoff.cellWidget(0,pollutant_count)
                    washoff.land_use_name = new_name
                    washoff.function = WashoffFunction[combobox.currentText()]
                    washoff.coefficient = self.tblWashoff.item(1,pollutant_count).text()
                    washoff.exponent = self.tblWashoff.item(2,pollutant_count).text()
                    washoff.cleaning_efficiency = self.tblWashoff.item(3,pollutant_count).text()
                    washoff.bmp_efficiency = self.tblWashoff.item(4,pollutant_count).text()

                    if orig_land_use_name != washoff.land_use_name or \
                        orig_function != washoff.function or \
                        orig_coefficient != washoff.coefficient or \
                        orig_exponent != washoff.exponent or \
                        orig_cleaning_efficiency != washoff.cleaning_efficiency or \
                        orig_bmp_efficiency != washoff.bmp_efficiency:
                        self._main_form.mark_project_as_unsaved()

            if not washoff_found:
                # add new record
                new_washoff = Washoff()
                new_washoff.land_use_name = new_name
                new_washoff.pollutant = pollutant
                combobox = self.tblWashoff.cellWidget(0,pollutant_count)
                new_washoff.function = WashoffFunction[combobox.currentText()]
                new_washoff.coefficient = self.tblWashoff.item(1,pollutant_count).text()
                new_washoff.exponent = self.tblWashoff.item(2,pollutant_count).text()
                new_washoff.cleaning_efficiency = self.tblWashoff.item(3,pollutant_count).text()
                new_washoff.bmp_efficiency = self.tblWashoff.item(4,pollutant_count).text()
                if self.project.washoff.value == '':
                    self.project.washoff.value = []
                self.project.washoff.value.append(new_washoff)
                self._main_form.mark_project_as_unsaved()

        # put this back in place
        orig_name = self.editing_item.name
        orig_comment = self.editing_item.comment
        orig_last_swept = self.editing_item.last_swept
        orig_street_sweeping_availability = self.editing_item.street_sweeping_availability
        orig_street_sweeping_interval = self.editing_item.street_sweeping_interval

        self.editing_item.name = new_name
        self.editing_item.comment = self.tblGeneral.item(1,0).text()
        self.editing_item.last_swept = self.tblGeneral.item(3,0).text()
        self.editing_item.street_sweeping_availability = self.tblGeneral.item(4,0).text()
        self.editing_item.street_sweeping_interval = self.tblGeneral.item(5,0).text()

        if orig_name != self.editing_item.name or \
            orig_comment != self.editing_item.comment or \
            orig_last_swept != self.editing_item.last_swept or \
            orig_street_sweeping_availability != self.editing_item.street_sweeping_availability or \
            orig_street_sweeping_interval != self.editing_item.street_sweeping_interval:
            self._main_form.mark_project_as_unsaved()

        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
            self._main_form.mark_project_as_unsaved()
        else:
            pass
            # TODO: self._main_form.edited_?

        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def tblGeneral_currentCellChanged(self):
        row = self.tblGeneral.currentRow()
        if row == 0:
            self.lblNotesGeneral.setText("User assigned name of land use")
        elif row == 1:
            self.lblNotesGeneral.setText("Optional comment or description of the land use")
        elif row == 2:
            self.lblNotesGeneral.setText("")
        elif row == 3:
            self.lblNotesGeneral.setText("Days between street sweeping within the land use (0 for no sweeping)")
        elif row == 4:
            self.lblNotesGeneral.setText("Fraction of pollutant buildup that is available for removal by sweeping")
        elif row == 5:
            self.lblNotesGeneral.setText("Number of days since land use was last swept at the start of the simulation")

    def tblBuildup_currentCellChanged(self):
        row = self.tblBuildup.currentRow()
        if row == 0:
            self.lblNotesBuildup.setText("Buildup function: POW = power, EXP = exponential, SAT = saturation, EXT = external time series")
        elif row == 1:
            self.lblNotesBuildup.setText("Maximum possible buildup (lbs(kg) per unit of normalizer variable)")
        elif row == 2:
            self.lblNotesBuildup.setText("Rate constant of buildup function (lbs(kg) per normalizer per day for power buildup or 1/days for exponential buildup")
        elif row == 3:
            self.lblNotesBuildup.setText("Time exponent for power buildup or half saturation constant (days) for saturation buildup")
        elif row == 4:
            self.lblNotesBuildup.setText("Subcatchment variable to which buildup is normalized: area (acres or hectares) or curb length (any units)")
        elif row == 5:
            self.lblNotesBuildup.setText("Scaling factor used to modify loading rates by a fixed ratio for EXT Function")
        elif row == 6:
            self.lblNotesBuildup.setText("Name of time series containing loading rates (lbs(kg) per normailzer per day) for EXT Function")

    def tblWashoff_currentCellChanged(self):
        row = self.tblWashoff.currentRow()
        if row == 0:
            self.lblNotesWashoff.setText("Washoff function: EXP = exponential, RC = rating curve, EMC = event mean concentration")
        elif row == 1:
            self.lblNotesWashoff.setText("Washoff coefficient or Event Mean Concentration (EMC)")
        elif row == 2:
            self.lblNotesWashoff.setText("Runoff exponent in washoff function")
        elif row == 3:
            self.lblNotesWashoff.setText("Street cleaning removal efficiency (percent) for the pollutant")
        elif row == 4:
            self.lblNotesWashoff.setText("Removal efficiency (percent) associated with any Best Management Practice utilized")

    def tabLanduse_currentTabChanged(self):

        tab_index = self.tabLanduse.currentIndex()
        if tab_index == 0:
            self.help_topic = "swmm/src/src/landuseeditorgeneralpage.htm"
        elif tab_index == 1:
            self.help_topic = "swmm/src/src/landuseeditorbuilduppage.htm"
        elif tab_index == 2:
            self.help_topic = "swmm/src/src/landuseeditorwashoffpage.htm"
