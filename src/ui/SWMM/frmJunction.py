import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydraulics.node import Junction
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmInflows import frmInflows
from ui.SWMM.frmTreatment import frmTreatment


class frmJunction(frmGenericPropertyEditor):
    def __init__(self, main_form):
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        edit_these = []
        if self.project.junctions and isinstance(self.project.junctions.value, list):
            edit_these.extend(self.project.junctions.value)
        if len(edit_these) == 0:
            self.new_item = Junction()
            self.new_item.name = "1"
            edit_these.append(self.new_item)

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "SWMM Junction Editor")

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
        direct_section = self.project.find_section("INFLOWS")
        direct_list = direct_section.value[0:]
        for value in direct_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        dry_section = self.project.find_section("DWF")
        dry_list = dry_section.value[0:]
        for value in dry_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        rdii_section = self.project.find_section("RDII")
        rdii_list = rdii_section.value[0:]
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
        treatment_section = self.project.find_section("TREATMENT")
        treatment_list = treatment_section.value[0:]
        for value in treatment_list:
            if value.node == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_treatments(column))
        self.tblGeneric.setCellWidget(6, column, tb)

    def make_show_inflows(self, column):
        def local_show():
            editor = frmInflows(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_treatments(self, column):
        def local_show():
            editor = frmTreatment(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def cmdOK_Clicked(self):
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self.project.junctions.value.append(self.new_item)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
