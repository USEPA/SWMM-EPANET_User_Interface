import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.link import Pump
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmPump(frmGenericPropertyEditor):

    SECTION_NAME = "[PUMPS]"
    SECTION_TYPE = Pump()

    def __init__(self, main_form):
        self.help_topic = "epanet/src/src/pumpproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.pumps and isinstance(self.project.pumps.value, list):
            edit_these.extend(self.project.pumps.value)
        if len(edit_these) == 0:
            self.new_item = Pump()
            self.new_item.name = "1"
            edit_these.append(self.new_item)
        else:
            self.new_item = False

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "EPANET Pump Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # pump curve
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in self.project.curves:
                combobox.addItem(value.name)
                if edit_these[column].head_curve_name == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(5, column, combobox)
            # for pattern, show available patterns
            pattern_section = self.project.find_section("PATTERNS")
            pattern_list = pattern_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.pattern_name)
                if edit_these[column].pattern == value.pattern_name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(8, column, combobox)
            # Pumps can have a status of OPEN, CLOSED
            combobox = QtGui.QComboBox()
            combobox.addItem('OPEN')
            combobox.addItem('CLOSED')
            if edit_these[column].initial_status and (edit_these[column].initial_status.upper() == 'OPEN' or edit_these[column].initial_status == ''):
                combobox.setCurrentIndex(0)
            else:
                combobox.setCurrentIndex(1)
            self.tblGeneric.setCellWidget(9, column, combobox)
            # efficiency curve
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in self.project.curves:
                combobox.addItem(value.name)
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(10, column, combobox)
            # for price pattern, show available patterns
            pattern_section = self.project.find_section("PATTERNS")
            pattern_list = pattern_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.pattern_name)
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(12, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
