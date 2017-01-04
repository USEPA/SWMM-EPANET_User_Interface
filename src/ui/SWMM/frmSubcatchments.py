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

    def __init__(self, main_form, edit_these, new_item):
        self.help_topic = "swmm/src/src/subcatchmentproperties.htm"
        self._main_form = main_form
        self.project = main_form.project
        self.refresh_column = -1
        self.project_section = self.project.subcatchments
        if self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], basestring):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)

        frmGenericPropertyEditor.__init__(self, main_form, self.project_section, edit_these, new_item,
                                          "SWMM " + self.SECTION_TYPE.__name__ + " Editor")
        self.row_named = {}

        for row in range(0, self.tblGeneric.rowCount()):
            self.row_named[str(self.tblGeneric.verticalHeaderItem(row).text())] = row

        for column in range(0, self.tblGeneric.columnCount()):

            # for snowpacks, show available snowpacks
            combobox = QtGui.QComboBox()
            combobox.addItem('')
            selected_index = 0
            for value in self.project.snowpacks.value:
                combobox.addItem(value.name)
                if edit_these[column].snow_pack == value.name:
                    selected_index = int(combobox.count())-1
            combobox.setCurrentIndex(selected_index)
            self.tblGeneric.setCellWidget(self.row_named["Snow Pack"], column, combobox)

            # also set special text plus button cells
            self.set_special_cells(column)

        self.installEventFilter(self)

    def set_special_cells(self, column):
        self.set_infiltration_cell(self.row_named["Infiltration"], column)
        self.set_groundwater_cell(self.row_named["Groundwater"], column)
        self.set_lid_control_cell(self.row_named["LID Controls"], column)
        self.set_land_use_cell(self.row_named["Land Uses"], column)
        self.set_initial_buildup_cell(self.row_named["Initial Buildup"], column)

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_special_cells(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_infiltration_cell(self, row, column):
        # text plus button for infiltration editor
        tb = TextPlusButton(self)
        tb.textbox.setText(self.project.options.infiltration)
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_infilt(column))
        self.tblGeneric.setItem(row, column, QtGui.QTableWidgetItem(''))
        self.tblGeneric.setCellWidget(row, column, tb)

    def set_groundwater_cell(self, row, column):
        # text plus button for groundwater editor
        tb = TextPlusButton(self)
        tb.textbox.setText('NO')
        for value in self.project.groundwater.value:
            if value.subcatchment == str(self.tblGeneric.item(0,column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_groundwater(column))
        self.tblGeneric.setCellWidget(row, column, tb)

    def set_lid_control_cell(self, row, column):
        # text plus button for lid controls
        tb = TextPlusButton(self)
        section = self.project.find_section("LID_USAGE")
        if section:
            lid_list = section.value
        else:
            lid_list = []
        lid_count = 0
        for value in lid_list:
            if value.subcatchment_name == str(self.tblGeneric.item(0,column).text()):
                lid_count += 1
        tb.textbox.setText(str(lid_count))
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_lid_controls(column))
        self.tblGeneric.setCellWidget(row, column, tb)

    def set_land_use_cell(self, row, column):
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
        self.tblGeneric.setCellWidget(row, column, tb)

    def set_initial_buildup_cell(self, row, column):
        # text plus button for initial buildup
        tb = TextPlusButton(self)
        tb.textbox.setText('NONE')
        for value in self.project.loadings.value:
            if value.subcatchment_name == str(self.tblGeneric.item(0, column).text()):
                tb.textbox.setText('YES')
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_loadings_controls(column))
        self.tblGeneric.setCellWidget(row, column, tb)

    def make_show_groundwater(self, column):
        def local_show():
            edit_these = []
            groundwater_section = self.project.groundwater
            if isinstance(groundwater_section.value, list):
                if len(groundwater_section.value) > 0:
                    for item in groundwater_section.value:
                        if item.subcatchment == str(self.tblGeneric.item(0,column).text()):
                            edit_these.append(item)
                if len(groundwater_section.value) == 0:
                    new_item = Groundwater()
                    groundwater_section.value.append(new_item)
                    edit_these.append(new_item)
            else:
                new_item = Groundwater()
                groundwater_section.value = []
                groundwater_section.value.append(new_item)
                edit_these.append(new_item)
            editor = frmGroundwaterFlow(self, edit_these, None, "SWMM Groundwater Flow Editor")
            editor.setWindowModality(QtCore.Qt.ApplicationModal)
            editor.show()
            self.refresh_column = column
        return local_show

    def make_show_infilt(self, column):
        def local_show():
            edit_these = []
            infiltration_section = self.project.infiltration
            if isinstance(infiltration_section.value, list):
                if len(infiltration_section.value) > 0:
                    for item in infiltration_section.value:
                        if item.subcatchment == str(self.tblGeneric.item(0, column).text()):
                            edit_these.append(item)
                if len(edit_these) == 0:
                    infiltration = self.project.options.infiltration.upper()
                    if infiltration == "HORTON":
                        new_item = HortonInfiltration()
                    elif infiltration == "MODIFIED_HORTON":
                        new_item = HortonInfiltration()
                    elif infiltration == "GREEN_AMPT":
                        new_item = GreenAmptInfiltration()
                    elif infiltration == "MODIFIED_GREEN_AMPT":
                        new_item = GreenAmptInfiltration()
                    elif infiltration == "CURVE_NUMBER":
                        new_item = CurveNumberInfiltration()
                    else:
                        new_item = HortonInfiltration()
                    infiltration_section.value.append(new_item)
                    edit_these.append(new_item)
            editor = frmInfiltration(self, edit_these, None, "SWMM Infiltration Editor")
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
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
