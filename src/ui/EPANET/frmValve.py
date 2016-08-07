import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.epanet.hydraulics.link import Valve
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmValve(frmGenericPropertyEditor):

    SECTION_NAME = "[VALVES]"
    SECTION_TYPE = Valve()

    def __init__(self, main_form):
        self.help_topic = "epanet/src/src/valveproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.valves and isinstance(self.project.valves.value, list):
            edit_these.extend(self.project.valves.value)
        if len(edit_these) == 0:
            self.new_item = Valve()
            self.new_item.name = "1"
            edit_these.append(self.new_item)
        else:
            self.new_item = False

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "EPANET Valve Editor")

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
