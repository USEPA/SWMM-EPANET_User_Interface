import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
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

        for column in range(0, self.tblGeneric.columnCount()):
            # for patterns, show available patterns
            pattern_section = main_form.project.patterns
            pattern_list = pattern_section.value[0:]
            combobox = QtGui.QComboBox()
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
