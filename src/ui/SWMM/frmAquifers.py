import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend


class frmAquifers(frmGenericPropertyEditor):

    SECTION_NAME = "[AQUIFERS]"
    SECTION_TYPE = Aquifer

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/aquifereditordialog.htm"

        frmGenericPropertyEditor.__init__(self, main_form, main_form.project.aquifers, edit_these, new_item,
                                          "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        self.project_section = main_form.project.aquifers
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

        self.pattern_section = main_form.project.patterns
        pattern_list = self.pattern_section.value[0:]
        for column in range(0, self.tblGeneric.columnCount()):
            # for patterns, show available patterns
            combobox = QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.name)
                if edit_these[column].upper_evaporation_pattern == value.name:
                    selected_index = int(combobox.count()) - 1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(13, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
