import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmLIDControls import frmLIDControls
# from ui.SWMM.frmInfiltration import frmInfiltration


class frmSubcatchments(frmGenericPropertyEditor):

    SECTION_NAME = "[SUBCATCHMENTS]"
    SECTION_TYPE = Subcatchment

    def __init__(self, parent):
        self.parent = parent
        self.project = parent.project
        edit_these = []
        project_section = self.project.find_section(self.SECTION_NAME)
        if project_section and\
                isinstance(project_section.value, list) and\
                len(project_section.value) > 0 and\
                isinstance(project_section.value[0], self.SECTION_TYPE):
                    edit_these.extend(project_section.value)
        if len(edit_these) == 0:
            self.new_item = self.SECTION_TYPE()
            # self.new_item.name = "1"
            edit_these.append(self.new_item)

        frmGenericPropertyEditor.__init__(self, parent, edit_these, "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

        for column in range(0, self.tblGeneric.columnCount()):
            # text plus button for infiltration editor
            option_section = self.project.find_section('OPTIONS')
            tb = TextPlusButton(self)
            tb.textbox.setText(option_section.infiltration)
            tb.textbox.setEnabled(False)
            tb.column = column
            tb.button.clicked.connect(self.make_show_infilt(column))
            self.tblGeneric.setCellWidget(18, column, tb)
            # text plus button for lid controls
            tb = TextPlusButton(self)
            tb.textbox.setText("NO")
            tb.column = column
            tb.button.clicked.connect(self.make_show_lid_controls(column))
            self.tblGeneric.setCellWidget(21, column, tb)

    def make_show_infilt(self, column):
        def local_show():
            print("Show for column " + str(column))
            # editor = frmInfiltration(self.parent)
            # self.parent.show_edit_window(editor)
        return local_show

    def make_show_lid_controls(self, column):
        def local_show():
            print("Show for column " + str(column))
            editor = frmLIDControls(self.parent)
            # TODO: Populate editor textbox
            # TODO: make button do something related to column
            self.parent.show_edit_window(editor)
        return local_show

    def cmdOK_Clicked(self):
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            project_section = self.project.find_section(self.SECTION_NAME)
            if project_section and isinstance(project_section.value, list):
                project_section.value.append(self.new_item)
            else:
                print("Unable to add new item to project: section is not a list: " + self.SECTION_NAME)
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
