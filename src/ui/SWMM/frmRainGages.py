import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.raingage import RainGage
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton


class frmRainGages(frmGenericPropertyEditor):

    SECTION_NAME = "[RAINGAGES]"
    SECTION_TYPE = RainGage

    def __init__(self, main_form):
        self.help_topic = "swmm/src/src/raingageproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        project_section = self.project.find_section(self.SECTION_NAME)
        if project_section and\
                isinstance(project_section.value, list) and\
                len(project_section.value) > 0 and\
                isinstance(project_section.value[0], self.SECTION_TYPE):
                    edit_these.extend(project_section.value)
        if len(edit_these) == 0:
            self.new_item = self.SECTION_TYPE()
            # self.new_item.name = "1"
            edit_these.append(self.new_item)

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # for timeseries, show available timeseries
            timeseries_section = self.project.find_section("TIMESERIES")
            timeseries_list = timeseries_section.value[0:]
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
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            project_section = self.project.find_section(self.SECTION_NAME)
            if project_section and isinstance(project_section.value, list):
                project_section.value.append(self.new_item)
            else:
                print("Unable to add new item to project: section is not a list: " + self.SECTION_NAME)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
