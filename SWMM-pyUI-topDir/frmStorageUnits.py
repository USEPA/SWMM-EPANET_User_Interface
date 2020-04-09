import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.swmm.hydraulics.node import StorageUnit
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from frmInflows import frmInflows
from frmTreatment import frmTreatment
from frmSeepage import frmSeepage
from core.swmm.curves import CurveType


class frmStorageUnits(frmGenericPropertyEditor):

    # SECTION_NAME = "[STORAGE]"
    SECTION_TYPE = StorageUnit

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/storageunitproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.storage
        self.new_item = new_item

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

        frmGenericPropertyEditor.__init__(self, main_form, self.project.storage,
                                          edit_these, new_item, "SWMM Storage Units Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            combobox = QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in self.project.curves.value:
                if value.curve_type == CurveType.STORAGE:
                    combobox.addItem(value.name)
                    if edit_these[column].storage_curve == value.name:
                        selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(17, column, combobox)
            # also set special text plus button cells
            self.set_seepage_loss_cell(column)
            self.set_inflow_cell(column)
            self.set_treatment_cell(column)

        if (main_form.program_settings.value("Geometry/" + "frmStorageUnits_geometry") and
                main_form.program_settings.value("Geometry/" + "frmStorageUnits_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmStorageUnits_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmStorageUnits_state",
                                                               self.windowState(), type=QtCore.QByteArray))

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_seepage_loss_cell(self.refresh_column)
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
        self.tblGeneric.setCellWidget(5, column, tb)

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
        self.tblGeneric.setCellWidget(6, column, tb)

    def set_seepage_loss_cell(self, column):
        # text plus button for seepage loss editor
        tb = TextPlusButton(self)
        tb.textbox.setText("NO")
        storage_section = self.project.find_section("STORAGE")
        storage_list = storage_section.value[0:]
        for value in storage_list:
            if value.name == str(self.tblGeneric.item(0,column).text()):
                if value.seepage_hydraulic_conductivity > '0':
                    tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_seepage_loss(column))
        self.tblGeneric.setCellWidget(12, column, tb)

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

    def make_show_seepage_loss(self, column):
        def local_show():
            if self.new_item:
                self.backend.apply_edits() # create before editing
            editor = frmSeepage(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        # self._main_form.model_layers.create_layers_from_project(self.project)

        self._main_form.program_settings.setValue("Geometry/" + "frmStorageUnits_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmStorageUnits_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
