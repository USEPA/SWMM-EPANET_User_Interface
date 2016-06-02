import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.hydrology.subcatchment import HortonInfiltration
from core.swmm.hydrology.subcatchment import GreenAmptInfiltration
from core.swmm.hydrology.subcatchment import CurveNumberInfiltration
from core.swmm.hydrology.subcatchment import Groundwater
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmLIDControls import frmLIDControls
from ui.SWMM.frmInitialBuildup import frmInitialBuildup
from ui.SWMM.frmLandUseAssignment import frmLandUseAssignment
from ui.SWMM.frmInfiltration import frmInfiltration
from ui.SWMM.frmGroundwaterFlow import frmGroundwaterFlow


class frmSubcatchments(frmGenericPropertyEditor):

    SECTION_NAME = "[SUBCATCHMENTS]"
    SECTION_TYPE = Subcatchment

    def __init__(self, main_form):
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
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

        frmGenericPropertyEditor.__init__(self, main_form, edit_these, "SWMM " + self.SECTION_TYPE.__name__ + " Editor")

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

        self.installEventFilter(self)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_infiltration_cell(self.refresh_column)
                self.set_groundwater_cell(self.refresh_column)
                self.set_lid_control_cell(self.refresh_column)
                self.set_land_use_cell(self.refresh_column)
                self.set_initial_buildup_cell(self.refresh_column)
                self.refresh_column = -1
        return False

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
        groundwater_section = self.project.groundwater
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
            edit_these = []
            groundwater_section = self.project.groundwater
            if isinstance(groundwater_section.value, list):
                if len(groundwater_section.value) == 0:
                    new_item = Groundwater()
                    groundwater_section.value.append(new_item)
                edit_these.extend(groundwater_section.value)
            else:
                new_item = Groundwater()
                groundwater_section.value = []
                groundwater_section.value.append(new_item)
                edit_these.extend(groundwater_section.value)
            editor = frmGroundwaterFlow(self, edit_these, "SWMM Groundwater Flow Editor")
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_infilt(self, column):
        def local_show():
            edit_these = []
            infiltration_section = self.project.find_section('INFILTRATION')
            if isinstance(infiltration_section.value, list):
                if len(infiltration_section.value) == 0:
                    option_section = self.project.find_section('OPTIONS')
                    new_item = HortonInfiltration()
                    if option_section.infiltration == "HORTON":
                        new_item = HortonInfiltration()
                    elif option_section.infiltration == "MODIFIED_HORTON":
                        new_item = HortonInfiltration()
                    elif option_section.infiltration == "GREEN_AMPT":
                        new_item = GreenAmptInfiltration()
                    elif option_section.infiltration == "MODIFIED_GREEN_AMPT":
                        new_item = GreenAmptInfiltration()
                    elif option_section.infiltration == "CURVE_NUMBER":
                        new_item = CurveNumberInfiltration()
                    infiltration_section.value.append(new_item)
                edit_these.extend(infiltration_section.value)
            editor = frmInfiltration(self, edit_these, "SWMM Infiltration Editor")
            editor.show()
        return local_show

    def make_show_lid_controls(self, column):
        def local_show():
            editor = frmLIDControls(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_coverage_controls(self, column):
        def local_show():
            editor = frmLandUseAssignment(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_loadings_controls(self, column):
        def local_show():
            editor = frmInitialBuildup(self._main_form, str(self.tblGeneric.item(0, column).text()))
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
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
