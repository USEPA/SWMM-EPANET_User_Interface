import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmLIDControls import frmLIDControls
from ui.SWMM.frmInitialBuildup import frmInitialBuildup
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
            # for snowpacks, show available snowpacks
            snowpack_section = self.project.find_section("SNOWPACKS")
            snowpack_list = snowpack_section.value[0:]
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in snowpack_list:
                combobox.addItem(value.name)
                if edit_these[column].snow_pack == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(20, column, combobox)
            # also set special text plus button cells
            self.set_infiltration_cell(column)
            self.set_groundwater_cell(column)
            self.set_lid_control_cell(column)
            self.set_land_use_cell(column)
            self.set_initial_buildup_cell(column)

    def set_infiltration_cell(self, column):
        # text plus button for infiltration editor
        option_section = self.project.find_section('OPTIONS')
        tb = TextPlusButton(self)
        tb.textbox.setText(option_section.infiltration)
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_infilt(column))
        self.tblGeneric.setCellWidget(18, column, tb)

    def set_groundwater_cell(self, column):
        # text plus button for groundwater editor
        tb = TextPlusButton(self)
        tb.textbox.setText('NO')
        groundwater_section = self.project.find_section('GROUNDWATER')
        groundwater_list = groundwater_section.value[0:]
        for value in groundwater_list:
            if value.subcatchment == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_groundwater(column))
        self.tblGeneric.setCellWidget(19, column, tb)

    def set_lid_control_cell(self, column):
        # text plus button for lid controls
        tb = TextPlusButton(self)
        section = self.project.find_section("LID_USAGE")
        lid_list = section.value[0:]
        lid_count = 0
        for value in lid_list:
            if value.subcatchment_name == str(self.tblGeneric.item(0,column).text()):
                lid_count += 1
        tb.textbox.setText(str(lid_count))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_lid_controls(column))
        self.tblGeneric.setCellWidget(21, column, tb)

    def set_land_use_cell(self, column):
        # text plus button for land use coverages
        tb = TextPlusButton(self)
        section = self.project.find_section("COVERAGES")
        coverage_list = section.value[0:]
        coverage_count = 0
        for value in coverage_list:
            if value.subcatchment_name == str(self.tblGeneric.item(0,column).text()):
                coverage_count += 1
        tb.textbox.setText(str(coverage_count))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_coverage_controls(column))
        self.tblGeneric.setCellWidget(22, column, tb)

    def set_initial_buildup_cell(self, column):
        # text plus button for initial buildup
        tb = TextPlusButton(self)
        tb.textbox.setText('NONE')
        loadings_section = self.project.find_section('LOADINGS')
        loadings_list = loadings_section.value[0:]
        for value in loadings_list:
            if value.subcatchment_name == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_loadings_controls(column))
        self.tblGeneric.setCellWidget(23, column, tb)

    def make_show_groundwater(self, column):
        def local_show():
            print("Show for column " + str(column))
            # editor = frmInfiltration(self.parent)
            # self.parent.show_edit_window(editor)
        return local_show

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

    def make_show_coverage_controls(self, column):
        def local_show():
            print("Show for column " + str(column))
        return local_show

    def make_show_loadings_controls(self, column):
        def local_show():
            editor = frmInitialBuildup(self.parent, str(self.tblGeneric.item(0,column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            # self.parent.show_edit_window(editor)
            self.set_initial_buildup_cell(column)
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
