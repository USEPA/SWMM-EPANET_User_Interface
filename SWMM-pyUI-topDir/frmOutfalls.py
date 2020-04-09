import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.swmm.hydraulics.node import Outfall
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from frmInflows import frmInflows
from frmTreatment import frmTreatment
from core.swmm.curves import CurveType


class frmOutfalls(frmGenericPropertyEditor):

    SECTION_NAME = "[OUTFALLS]"
    SECTION_TYPE = Outfall

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/outfallproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.outfalls
        if self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], str):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

        frmGenericPropertyEditor.__init__(self, main_form, self.project_section, edit_these, new_item, "SWMM Outfalls Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for tide gate, show true/false
            combobox = QComboBox()
            combobox.addItem('YES')
            combobox.addItem('NO')
            combobox.setCurrentIndex(1)
            if len(edit_these) > 0:
                if edit_these[column].tide_gate:
                    combobox.setCurrentIndex(0)
            row = self.header_index("tide")
            if row >= 0:
                self.tblGeneric.setCellWidget(row, column, combobox)
            # for curves, show available curves
            curves_section = self.project.find_section("CURVES")
            curves_list = curves_section.value[0:]
            combobox = QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for value in curves_list:
                if value.curve_type == CurveType.TIDAL:
                    combobox.addItem(value.name)
                    if edit_these[column].tidal_curve == value.name:
                        selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            row = self.header_index("curve")
            if row >= 0:
                self.tblGeneric.setCellWidget(row, column, combobox)
            # for time series, show available timeseries
            timeseries_section = self.project.find_section("TIMESERIES")
            timeseries_list = timeseries_section.value[0:]
            combobox = QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for value in timeseries_list:
                combobox.addItem(value.name)
                if edit_these[column].time_series_name == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            row = self.header_index("series")
            if row >= 0:
                self.tblGeneric.setCellWidget(row, column, combobox)
            # also set special text plus button cells
            self.set_inflow_cell(column)
            self.set_treatment_cell(column)

        if (main_form.program_settings.value("Geometry/" + "frmOutfalls_geometry") and
                main_form.program_settings.value("Geometry/" + "frmOutfalls_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmOutfalls_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmOutfalls_state",
                                                               self.windowState(), type=QtCore.QByteArray))

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_inflow_cell(self.refresh_column)
                self.set_treatment_cell(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_inflow_cell(self, column):
        tb = TextPlusButton(self)
        tb.textbox.setText("NO")
        direct_section = self.project.find_section("INFLOWS")
        direct_list = direct_section.value[0:]
        for value in direct_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        dry_section = self.project.find_section("DWF")
        dry_list = dry_section.value[0:]
        for value in dry_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        rdii_section = self.project.find_section("RDII")
        rdii_list = rdii_section.value[0:]
        for value in rdii_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_inflows(column))
        row = self.header_index("inflow")
        if row >=0:
            self.tblGeneric.setCellWidget(row, column, tb)

    def set_treatment_cell(self, column):
        # text plus button for treatments editor
        tb = TextPlusButton(self)
        tb.textbox.setText("NO")
        treatment_section = self.project.find_section("TREATMENT")
        treatment_list = treatment_section.value[0:]
        for value in treatment_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_treatments(column))
        row = self.header_index("treatment")
        if row >=0:
            self.tblGeneric.setCellWidget(row, column, tb)

    def make_show_inflows(self, column):
        def local_show():
            editor = frmInflows(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_treatments(self, column):
        def local_show():
            editor = frmTreatment(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        # self._main_form.model_layers.create_layers_from_project(self.project)

        self._main_form.program_settings.setValue("Geometry/" + "frmOutfalls_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmOutfalls_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
