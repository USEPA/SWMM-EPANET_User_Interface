import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.link import Pump
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmPump(frmGenericPropertyEditor):

    SECTION_NAME = "[PUMPS]"
    SECTION_TYPE = Pump

    def __init__(self, session, edit_these, new_item):
        self.help_topic = "epanet/src/src/Pump_Pro.htm"
        self._main_form = session
        self.project = session.project
        self.refresh_column = -1
        self.project_section = self.project.pumps
        if self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], basestring):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

        frmGenericPropertyEditor.__init__(self, session, session.project.pumps,
                                          edit_these, new_item, "EPANET Pump Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # pump curve
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in self.project.curves.value:
                combobox.addItem(value.name)
                if edit_these[column].head_curve_name == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(5, column, combobox)
            # for pattern, show available patterns
            pattern_list = self.project.patterns.value
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.name)
                if edit_these[column].pattern == value.name:
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
            for value in self.project.curves.value:
                combobox.addItem(value.name)
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(10, column, combobox)
            # for price pattern, show available patterns
            pattern_list = self.project.patterns.value
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in pattern_list:
                combobox.addItem(value.name)
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(12, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
