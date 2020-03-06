import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem
from ui.help import HelpHandler
from core.swmm.hydrology.subcatchment import InitialLoading
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmInitialBuildup(frmGenericPropertyEditor):

    SECTION_NAME = "[LOADINGS]"

    def __init__(self, main_form, subcatchment_name):
        # purposely not calling frmGenericPropertyEditor.__init__
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/initialbuildupeditor.htm"
        self.units = main_form.project.options.flow_units.value
        self.setupUi(self)
        self.subcatchment_name = subcatchment_name
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.setWindowTitle('SWMM Initial Buildup Editor for Subcatchment ' + subcatchment_name)
        self.lblNotes.setText("Enter initial buildup of pollutants on Subcatchment " + subcatchment_name)
        self.tblGeneric.setColumnCount(1)
        local_column_list = []
        if self.units < 4:
            local_column_list.append('Initial Buildup (lbs/ac)')
        else:
            local_column_list.append('Initial Buildup (kg/ha)')
        self.tblGeneric.setHorizontalHeaderLabels(local_column_list)
        self.tblGeneric.setColumnWidth(0,200)
        self.local_pollutant_list = []
        pollutants_section = main_form.project.find_section("POLLUTANTS")
        row_count = 0
        for value in pollutants_section.value:
            row_count += 1
            self.local_pollutant_list.append(value.name)
        self.tblGeneric.setRowCount(row_count)
        self.tblGeneric.setVerticalHeaderLabels(self.local_pollutant_list)
        self.resize(300,300)
        section = main_form.project.find_section("LOADINGS")
        loadings_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            for loading in loadings_list:
                if loading.subcatchment_name == subcatchment_name and loading.pollutant_name == pollutant:
                    led = QLineEdit(str(loading.initial_buildup))
                    self.tblGeneric.setItem(pollutant_count,0,QTableWidgetItem(led.text()))
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmInitialBuildup_geometry") and
                main_form.program_settings.value("Geometry/" + "frmInitialBuildup_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmInitialBuildup_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmInitialBuildup_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section("LOADINGS")
        loadings_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            loading_found = False
            for loading in loadings_list:
                if loading.subcatchment_name == self.subcatchment_name and loading.pollutant_name == pollutant:
                    # put this back in place
                    loading_found = True
                    if self.tblGeneric.item(pollutant_count,0) and len(self.tblGeneric.item(pollutant_count,0).text()) > 0:
                        if loading.initial_buildup != self.tblGeneric.item(pollutant_count, 0).text():
                            self._main_form.mark_project_as_unsaved()
                        loading.initial_buildup = self.tblGeneric.item(pollutant_count,0).text()
                    else:
                        section.value.remove(loading)
                        self._main_form.mark_project_as_unsaved()
            if not loading_found:
                # add new record
                if self.tblGeneric.item(pollutant_count,0):
                    value1 = InitialLoading()
                    value1.subcatchment_name = self.subcatchment_name
                    value1.pollutant_name = pollutant
                    value1.initial_buildup = str(self.tblGeneric.item(pollutant_count,0).text())
                    if section.value == '':
                        section.value = []
                    section.value.append(value1)
                    self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmInitialBuildup_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmInitialBuildup_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmInitialBuildup_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmInitialBuildup_state", self.saveState())
        self.close()
