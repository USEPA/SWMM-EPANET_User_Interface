import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmLIDControls import frmLIDControls


class frmSubcatchments(frmGenericPropertyEditor):
    def __init__(self, parent):
        self.parent = parent
        self.project = parent.project
        edit_these = []
        project_subcatchments_section = self.project.find_section("[SUBCATCHMENTS]")
        if project_subcatchments_section and\
                isinstance(project_subcatchments_section.value, list) and\
                len(project_subcatchments_section.value) > 0 and\
                isinstance(project_subcatchments_section.value[0], Subcatchment):
                    edit_these.extend(self.project.subcatchments.value)
        if len(edit_these) == 0:
            self.new_item = Subcatchment()
            self.new_item.name = "1"
            edit_these.append(self.new_item)

        frmGenericPropertyEditor.__init__(self, parent, edit_these, "SWMM Subcatchment Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            tb = TextPlusButton(self)
            tb.textbox.setText("NO")
            tb.column = column
            tb.button.clicked.connect(self.make_show_lid_controls(column))
            self.tblGeneric.setCellWidget(21, column, tb)

        # for column in range(0, self.tblGeneric.columnCount()):
        #     tb = TextPlusButton(self)
        #     tb.textbox.setText("NO")
        #     tb.button.clicked.connect(self.make_show_treatments(column))
        #     self.tblGeneric.setCellWidget(6, column, tb)

    def make_show_lid_controls(self, column):
        def local_show():
            print("Show inflows for " + str(column))
            self.parent.show_edit_window(frmLIDControls(self.parent))
        return local_show

    # def make_show_treatments(self, column):
    #     def local_show():
    #         print("Show treatments for " + str(column))
    #         edit_these = []
    #         if isinstance(self.project.treatment.value, list):
    #             if len(self.project.treatment.value) == 0:
    #                 new_item = Treatment()
    #                 new_item.name = "NewTreatment"
    #                 self.project.treatment.value.append(new_item)
    #
    #         edit_these.extend(self.project.treatment.value)
    #         self.parent.show_edit_window(frmGenericPropertyEditor(self, edit_these, "SWMM Treatment Editor"))
    #     return local_show

    def cmdOK_Clicked(self):
        if self.new_item:
            self.project.junctions.value.append(self.new_item)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
