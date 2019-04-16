import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.swmm.hydraulics.link import Outlet
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from core.swmm.curves import CurveType


class frmOutlets(frmGenericPropertyEditor):

    SECTION_NAME = "[OUTLETS]"
    SECTION_TYPE = Outlet

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/outletproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.outlets
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

        frmGenericPropertyEditor.__init__(self, main_form, self.project_section, edit_these, new_item,
                                          "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for flapgate, show true/false
            combobox = QComboBox()
            combobox.addItem('True')
            combobox.addItem('False')
            combobox.setCurrentIndex(1)
            if len(edit_these) > 0:
                if edit_these[column].flap_gate == 'True' or edit_these[column].flap_gate == True:
                    combobox.setCurrentIndex(0)
            self.tblGeneric.setCellWidget(6, column, combobox)
            # tabular curve name
            curves_section = self.project.find_section("CURVES")
            curves_list = curves_section.value[0:]
            combobox = QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for value in curves_list:
                if value.curve_type == CurveType.RATING:
                    combobox.addItem(value.name)
                    if len(edit_these) > 0:
                        if edit_these[column].rating_curve == value.name:
                            selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(10, column, combobox)

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.refresh_column = -1
        return False

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self._main_form.model_layers.create_layers_from_project(self.project)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
