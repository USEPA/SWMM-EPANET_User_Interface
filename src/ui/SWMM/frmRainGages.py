import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QComboBox
from core.swmm.hydrology.raingage import RainGage
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton


class frmRainGages(frmGenericPropertyEditor):

    SECTION_NAME = "[RAINGAGES]"
    SECTION_TYPE = RainGage

    def __init__(self, session, edit_these, new_item):
        frmGenericPropertyEditor.__init__(self, session, session.project.raingages,
                                          edit_these, new_item, "SWMM " + self.SECTION_TYPE.__name__ + " Editor")
        self.help_topic = "swmm/src/src/raingageproperties.htm"
        self.refresh_column = -1

        for column in range(0, self.tblGeneric.columnCount()):
            # show current and available timeseries in combo box
            timeseries_list = self.project.timeseries.value
            combobox = QComboBox()
            combobox.addItem('*')
            selected_index = 0
            for value in timeseries_list:
                combobox.addItem(value.name)
                if self.edit_these[column].timeseries == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(9, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
