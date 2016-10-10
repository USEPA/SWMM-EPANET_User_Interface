import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.raingage import RainGage
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton


class frmRainGages(frmGenericPropertyEditor):

    SECTION_NAME = "[RAINGAGES]"
    SECTION_TYPE = RainGage

    def __init__(self, main_form, edit_these=[]):
        self.help_topic = "swmm/src/src/raingageproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.find_section(self.SECTION_NAME)
        if self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], basestring):  # Translate list from names to objects
                    edit_these = [item for item in self.project_section.value if item.name in edit_these]

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # show current and available timeseries in combo box
            timeseries_list = self.project.timeseries.value
            combobox = QtGui.QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for value in timeseries_list:
                combobox.addItem(value.name)
                if edit_these[column].timeseries == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(9, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
