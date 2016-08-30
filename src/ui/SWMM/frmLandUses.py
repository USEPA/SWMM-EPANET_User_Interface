import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmLandUsesDesigner import Ui_frmLandUsesEditor
import ui.convenience
from core.swmm.quality import BuildupFunction
from core.swmm.quality import Normalizer
from core.swmm.quality import Buildup
from core.swmm.quality import Washoff
from core.swmm.quality import WashoffFunction


class frmLandUses(QtGui.QMainWindow, Ui_frmLandUsesEditor):
    def __init__(self, main_form=None, edit_these=[]):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/landuseeditorgeneralpage.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.tabLanduse.currentChanged.connect(self.tabLanduse_currentTabChanged)
        self.tblGeneral.currentCellChanged.connect(self.tblGeneral_currentCellChanged)
        self.tblBuildup.currentCellChanged.connect(self.tblBuildup_currentCellChanged)
        self.tblWashoff.currentCellChanged.connect(self.tblWashoff_currentCellChanged)
        self._main_form = main_form
        self.land_use_name = ''
        self.tblGeneral.setColumnCount(1)
        self.tblGeneral.setRowCount(6)
        header_labels = ["Value"]
        self.tblGeneral.setHorizontalHeaderLabels(header_labels)
        self.tblGeneral.setVerticalHeaderLabels(("Land Use Name","Description","STREET SWEEPING","    Interval","    Availability","    Last Swept"))
        self.local_pollutant_list = []
        pollutants_section = main_form.project.pollutants
        for value in pollutants_section.value:
            self.local_pollutant_list.append(value.name)
        self.tblBuildup.setColumnCount(self.local_pollutant_list.__len__())
        self.tblBuildup.setRowCount(7)
        self.tblBuildup.setHorizontalHeaderLabels(self.local_pollutant_list)
        self.tblBuildup.setVerticalHeaderLabels(("Function","Max. Buildup","Rate Constant","Power/Sat. Constant","Normalizer","Scaling Factor","Time Series"))
        self.tblWashoff.setColumnCount(self.local_pollutant_list.__len__())
        self.tblWashoff.setRowCount(5)
        self.tblWashoff.setHorizontalHeaderLabels(self.local_pollutant_list)
        self.tblWashoff.setVerticalHeaderLabels(("Function","Coefficient","Exponent","Cleaning Effic.","BMP Effic."))
        if edit_these:
            if isinstance(edit_these, list):
                self.set_from(main_form.project, edit_these[0])
            else:
                self.set_from(main_form.project, edit_these)
        self.resize(400,450)

    def set_from(self, project, land_use_name):
        self.land_use_name = land_use_name
        section = project.find_section("LANDUSES")
        land_use_list = section.value[0:]
        for land_use in land_use_list:
            if land_use.name == land_use_name:
                # this is the land_use we want to edit
                led = QtGui.QLineEdit(land_use.name)
                self.tblGeneral.setItem(0,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(land_use.comment)
                self.tblGeneral.setItem(1,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(land_use.last_swept)
                self.tblGeneral.setItem(3,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(land_use.street_sweeping_availability)
                self.tblGeneral.setItem(4,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(land_use.street_sweeping_interval)
                self.tblGeneral.setItem(5,0,QtGui.QTableWidgetItem(led.text()))
        self.tblGeneral.setCurrentCell(0,0)
        section = project.find_section("BUILDUP")
        buildup_list = section.value[0:]
        local_column = -1
        for pollutant in self.local_pollutant_list:
            local_column += 1
            for buildup in buildup_list:
                if buildup.land_use_name == land_use_name and pollutant == buildup.pollutant:
                    # this is the land_use we want to edit
                    combobox = QtGui.QComboBox()
                    ui.convenience.set_combo_items(type(buildup.function), combobox)
                    ui.convenience.set_combo(combobox, buildup.function)  # BuildupFunction.POW
                    self.tblBuildup.setCellWidget(0,local_column, combobox)
                    led = QtGui.QLineEdit(buildup.max_buildup)
                    self.tblBuildup.setItem(1,local_column,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(buildup.rate_constant)
                    self.tblBuildup.setItem(2,local_column,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(buildup.power_sat_constant)
                    self.tblBuildup.setItem(3,local_column,QtGui.QTableWidgetItem(led.text()))
                    combobox = QtGui.QComboBox()
                    ui.convenience.set_combo_items(type(buildup.normalizer), combobox)
                    ui.convenience.set_combo(combobox, buildup.normalizer)   # Normalizer.AREA
                    self.tblBuildup.setCellWidget(4,local_column, combobox)
                    led = QtGui.QLineEdit(buildup.scaling_factor)
                    self.tblBuildup.setItem(5,local_column,QtGui.QTableWidgetItem(led.text()))
                    timeseries_section = project.find_section("TIMESERIES")
                    timeseries_list = timeseries_section.value[0:]
                    combobox = QtGui.QComboBox()
                    combobox.addItem('')
                    selected_index = 0
                    for value in timeseries_list:
                        combobox.addItem(value.name)
                        if buildup.timeseries == value.name:
                            selected_index = int(combobox.count())-1
                    combobox.setCurrentIndex(selected_index)
                    self.tblBuildup.setCellWidget(6, local_column, combobox)
        self.tblBuildup.setCurrentCell(0,0)
        section = project.find_section("WASHOFF")
        washoff_list = section.value[0:]
        local_column = -1
        for pollutant in self.local_pollutant_list:
            local_column += 1
            for washoff in washoff_list:
                if washoff.land_use_name == land_use_name and pollutant == washoff.pollutant:
                    # this is the land_use we want to edit
                    combobox = QtGui.QComboBox()
                    ui.convenience.set_combo_items(type(washoff.function), combobox)
                    ui.convenience.set_combo(combobox, washoff.function)  # WashoffFunction.EXP
                    self.tblWashoff.setCellWidget(0,local_column, combobox)
                    led = QtGui.QLineEdit(washoff.coefficient)
                    self.tblWashoff.setItem(1,local_column,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(washoff.exponent)
                    self.tblWashoff.setItem(2,local_column,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(washoff.cleaning_efficiency)
                    self.tblWashoff.setItem(3,local_column,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(washoff.bmp_efficiency)
                    self.tblWashoff.setItem(4,local_column,QtGui.QTableWidgetItem(led.text()))
        self.tblWashoff.setCurrentCell(0,0)

    def cmdOK_Clicked(self):
        section = self._main_form.project.landuses
        land_uses_list = section.value[0:]
        for land_use in land_uses_list:
            if land_use.name == self.land_use_name:
                # put this back in place
                land_use.name = self.tblGeneral.item(0,0).text()
                land_use.comment = self.tblGeneral.item(1,0).text()
                land_use.last_swept = self.tblGeneral.item(3,0).text()
                land_use.street_sweeping_availability = self.tblGeneral.item(4,0).text()
                land_use.street_sweeping_interval = self.tblGeneral.item(5,0).text()
        section = self._main_form.project.buildup
        buildup_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            buildup_found = False
            for buildup in buildup_list:
                if buildup.land_use_name == self.land_use_name and pollutant == buildup.pollutant:
                    # put this back in place
                    buildup_found = True
                    combobox = self.tblBuildup.cellWidget(0,pollutant_count)
                    buildup.function = BuildupFunction[combobox.currentText()]
                    buildup.max_buildup = self.tblBuildup.item(1,pollutant_count).text()
                    buildup.rate_constant = self.tblBuildup.item(2,pollutant_count).text()
                    buildup.power_sat_constant = self.tblBuildup.item(3,pollutant_count).text()
                    combobox = self.tblBuildup.cellWidget(4,pollutant_count)
                    buildup.normalizer = Normalizer[combobox.currentText()]
                    buildup.scaling_factor = self.tblBuildup.item(5,pollutant_count).text()
                    combobox = self.tblBuildup.cellWidget(6,pollutant_count)
                    buildup.timeseries = combobox.currentText()
            if not buildup_found:
                # add new record
                new_buildup = Buildup()
                new_buildup.land_use_name = self.land_use_name
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
                if section.value == '':
                    section.value = []
                section.value.append(new_buildup)
        section = self._main_form.project.find_section("WASHOFF")
        washoff_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            washoff_found = False
            for washoff in washoff_list:
                if washoff.land_use_name == self.land_use_name and pollutant == washoff.pollutant:
                    # put this back in place
                    washoff_found = True
                    combobox = self.tblWashoff.cellWidget(0,pollutant_count)
                    washoff.function = WashoffFunction[combobox.currentText()]
                    washoff.coefficient = self.tblWashoff.item(1,pollutant_count).text()
                    washoff.exponent = self.tblWashoff.item(2,pollutant_count).text()
                    washoff.cleaning_efficiency = self.tblWashoff.item(3,pollutant_count).text()
                    washoff.bmp_efficiency = self.tblWashoff.item(4,pollutant_count).text()
            if not washoff_found:
                # add new record
                new_washoff = Washoff()
                new_washoff.land_use_name = self.land_use_name
                new_washoff.pollutant = pollutant
                combobox = self.tblWashoff.cellWidget(0,pollutant_count)
                new_washoff.function = WashoffFunction[combobox.currentText()]
                new_washoff.coefficient = self.tblWashoff.item(1,pollutant_count).text()
                new_washoff.exponent = self.tblWashoff.item(2,pollutant_count).text()
                new_washoff.cleaning_efficiency = self.tblWashoff.item(3,pollutant_count).text()
                new_washoff.bmp_efficiency = self.tblWashoff.item(4,pollutant_count).text()
                if section.value == '':
                    section.value = []
                section.value.append(new_washoff)
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
