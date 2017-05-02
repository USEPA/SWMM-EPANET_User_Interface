import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.link import Valve
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmValve(frmGenericPropertyEditor):

    SECTION_NAME = "[VALVES]"
    SECTION_TYPE = Valve

    def __init__(self, session, edit_these, new_item):
        self.help_topic = "epanet/src/src/Valve_Pr.htm"
        self._main_form = session
        self.project = session.project
        self.refresh_column = -1

        self.project_section = self.project.valves
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

        frmGenericPropertyEditor.__init__(self, session, session.project.valves,
                                          edit_these, new_item, "EPANET Valve Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # Valves can have a status of NONE, OPEN, CLOSED
            combobox = QtGui.QComboBox()
            combobox.addItem('NONE')
            combobox.addItem('OPEN')
            combobox.addItem('CLOSED')
            combobox.setCurrentIndex(0)
            self.tblGeneric.setCellWidget(9, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
