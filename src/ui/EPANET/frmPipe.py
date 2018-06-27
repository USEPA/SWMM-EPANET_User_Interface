import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
from core.epanet.hydraulics.link import Pipe
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmPipe(frmGenericPropertyEditor):

    SECTION_NAME = "[PIPES]"
    SECTION_TYPE = Pipe

    def __init__(self, session, edit_these, new_item):
        self.help_topic = "epanet/src/src/Pipe_Pro.htm"
        self._main_form = session
        self.project = session.project
        self.refresh_column = -1
        self.project_section = self.project.pipes
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

        frmGenericPropertyEditor.__init__(self, session, session.project.pipes,
                                          edit_these, new_item, "EPANET Pipe Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # Pipes can have a status of OPEN, CLOSED, or CV.
            combobox = QComboBox()
            combobox.addItem('OPEN')
            combobox.addItem('CLOSED')
            combobox.addItem('CV')
            combobox.setCurrentIndex(0)
            if len(edit_these) > 0:
                if edit_these[column].initial_status.upper() == 'OPEN':
                    combobox.setCurrentIndex(0)
                elif edit_these[column].initial_status.upper() == 'CLOSED':
                    combobox.setCurrentIndex(1)
                else:
                    combobox.setCurrentIndex(2)
            self.tblGeneric.setCellWidget(9, column, combobox)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
