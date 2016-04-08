import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydraulics.node import Junction
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmInflows import frmInflows


class frmJunction(frmGenericPropertyEditor):
    def __init__(self, parent):
        self.parent = parent
        self.project = parent.project
        edit_these = []
        if self.project.junctions and isinstance(self.project.junctions.value, list):
            edit_these.extend(self.project.junctions.value)
        if len(edit_these) == 0:
            self.new_item = Junction()
            self.new_item.name = "1"
            edit_these.append(self.new_item)

        frmGenericPropertyEditor.__init__(self, parent, edit_these, "SWMM Junction Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            tb = TextPlusButton(self)
            tb.textbox.setText("NO")
            tb.column = column
            # self.connect(tb.button, QtCore.SIGNAL("clicked()"), self.callingFunction)
            tb.button.clicked.connect(self.make_show_inflows(column))
            self.tblGeneric.setCellWidget(5, column, tb)

        for column in range(0, self.tblGeneric.columnCount()):
            tb = TextPlusButton(self)
            tb.textbox.setText("NO")
            tb.button.clicked.connect(self.make_show_treatments(column))
            self.tblGeneric.setCellWidget(6, column, tb)

    def make_show_inflows(self, column):
        def local_show_inflows():
            print("Show inflows for " + str(column))
            self.parent.show_edit_window(frmInflows(self.parent))
        return local_show_inflows

    def make_show_treatments(self, column):
        def local_show_treatments():
            print("Show treatments for " + str(column))
            edit_these = []
            if isinstance(self.project.treatment.value, list):
                if len(self.project.treatment.value) == 0:
                    new_item = Treatment()
                    new_item.name = "NewTreatment"
                    self.project.treatment.value.append(new_item)

            edit_these.extend(self.project.treatment.value)
            self.parent.show_edit_window(frmGenericPropertyEditor(self, edit_these, "SWMM Treatment Editor"))

        return local_show_treatments

    def cmdOK_Clicked(self):
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self.project.junctions.value.append(self.new_item)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
