import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from core.swmm.hydraulics.node import Junction
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmInflows import frmInflows
from ui.SWMM.frmTreatment import frmTreatment


class frmJunction(frmGenericPropertyEditor):

    SECTION_NAME = "[JUNCTIONS]"
    SECTION_TYPE = Junction

    def __init__(self, session, edit_these, new_item):
        frmGenericPropertyEditor.__init__(self, session, session.project.junctions,
                                          edit_these, new_item, "SWMM Junction Editor")
        self.help_topic = "swmm/src/src/junctionproperties.htm"
        self.session = session
        self.refresh_column = -1
        for column in range(0, self.tblGeneric.columnCount()):
            # also set special text plus button cells
            self.set_inflow_cell(column)
            self.set_treatment_cell(column)
        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_inflow_cell(self.refresh_column)
                self.set_treatment_cell(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_inflow_cell(self, column):
        tb = TextPlusButton(self)
        tb.textbox.setText("NO")
        direct_list = self.project.inflows.value[0:]
        for value in direct_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        dry_list = self.project.dwf.value[0:]
        for value in dry_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        rdii_list = self.project.rdii.value[0:]
        for value in rdii_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_inflows(column))
        self.tblGeneric.setCellWidget(5, column, tb)

    def set_treatment_cell(self, column):
        # text plus button for treatments editor
        tb = TextPlusButton(self)
        tb.textbox.setText("NO")
        treatment_list = self.project.treatment.value[0:]
        for value in treatment_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_treatments(column))
        self.tblGeneric.setCellWidget(6, column, tb)

    def make_show_inflows(self, column):
        def local_show():
            editor = frmInflows(self.session, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_treatments(self, column):
        def local_show():
            editor = frmTreatment(self.session, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
