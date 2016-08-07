import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.link import Pipe
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmPipe(frmGenericPropertyEditor):

    SECTION_NAME = "[PIPES]"
    SECTION_TYPE = Pipe()

    def __init__(self, main_form):
        self.help_topic = "epanet/src/src/pipeproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.pipes and isinstance(self.project.pipes.value, list):
            edit_these.extend(self.project.pipes.value)
        if len(edit_these) == 0:
            self.new_item = Pipe()
            self.new_item.name = "1"
            edit_these.append(self.new_item)
        else:
            self.new_item = False

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "EPANET Pipe Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # Pipes can have a status of OPEN, CLOSED, or CV.
            combobox = QtGui.QComboBox()
            combobox.addItem('OPEN')
            combobox.addItem('CLOSED')
            combobox.addItem('CV')
            if edit_these[column].initial_status and (edit_these[column].initial_status.upper() == 'OPEN' or edit_these[column].initial_status == ''):
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
