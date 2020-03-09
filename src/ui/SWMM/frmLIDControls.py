import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView
from ui.help import HelpHandler
from ui.SWMM.frmLIDControlsDesigner import Ui_frmLIDControls
from ui.SWMM.frmLIDUsage import frmLIDUsage
from core.swmm.hydrology.lidcontrol import LIDType
from core.swmm.hydrology.subcatchment import LIDUsage


class frmLIDControls(QMainWindow, Ui_frmLIDControls):

    def __init__(self, main_form, subcatchment_name):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/lidgroupeditor.htm"
        self.units = main_form.project.options.flow_units.value
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.btnAdd.clicked.connect(self.btnAdd_Clicked)
        self.btnEdit.clicked.connect(self.btnEdit_Clicked)
        self.btnDelete.clicked.connect(self.btnDelete_Clicked)
        self._main_form = main_form
        # set for first subcatchment for now
        self.subcatchment_name = subcatchment_name
        self.set_subcatchment(main_form.project, subcatchment_name)

        if (main_form.program_settings.value("Geometry/" + "frmLIDControls_geometry") and
                main_form.program_settings.value("Geometry/" + "frmLIDControls_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmLIDControls_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmLIDControls_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_subcatchment(self, project, subcatchment_name):
        # section = core.swmm.project.LIDUsage()
        section = project.lid_usage
        lid_list = section.value[0:]
        # assume we want to edit the first one
        self.subcatchment_name = subcatchment_name
        self.setWindowTitle("LID Controls for Subcatchment " + subcatchment_name)
        self.tblControls.setColumnCount(self.tblControls.columnCount()+6)  # add for hidden columns
        lid_count = -1
        for value in lid_list:
            if value.subcatchment_name == subcatchment_name:
                # this is the subcatchment we want to edit
                lid_count += 1
                self.tblControls.setRowCount(lid_count+1)
                self.tblControls.setItem(lid_count,0,QTableWidgetItem(str(value.control_name)))

                self.SetLongLIDName(value.control_name,lid_count)
                self.SetAreaTerm(subcatchment_name, lid_count, value.number_replicate_units, value.area_each_unit)

                self.tblControls.setItem(lid_count,3,QTableWidgetItem(str(value.percent_impervious_area_treated)))
                self.tblControls.setItem(lid_count,4, QTableWidgetItem(str(value.percent_pervious_area_treated)))

                self.tblControls.setItem(lid_count,5,QTableWidgetItem(str(value.detailed_report_file)))

                # store the other param values in hidden columns
                self.tblControls.setItem(lid_count,6,QTableWidgetItem(str(value.number_replicate_units)))
                self.tblControls.setItem(lid_count,7,QTableWidgetItem(str(value.area_each_unit)))
                self.tblControls.setItem(lid_count,8,QTableWidgetItem(str(value.top_width_overland_flow_surface)))
                self.tblControls.setItem(lid_count,9,QTableWidgetItem(str(value.percent_initially_saturated)))
                self.tblControls.setItem(lid_count,10,QTableWidgetItem(str(value.send_outflow_pervious_area)))
                self.tblControls.setItem(lid_count,11,QTableWidgetItem(str(value.subcatchment_drains_to)))

        self.tblControls.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblControls.setColumnHidden(6,True)
        self.tblControls.setColumnHidden(7,True)
        self.tblControls.setColumnHidden(8,True)
        self.tblControls.setColumnHidden(9,True)
        self.tblControls.setColumnHidden(10,True)
        self.tblControls.setColumnHidden(11,True)

    def cmdOK_Clicked(self):
        row_count = self.tblControls.rowCount()
        section = self._main_form.project.lid_usage
        lid_list = section.value[0:]
        lid_count = 0
        for value in lid_list:
            if value.subcatchment_name == self.subcatchment_name:
                lid_count += 1
                if lid_count <= row_count:
                    # put this lid back in this spot
                    if value.control_name != self.tblControls.item(lid_count-1,0).text() or \
                        value.percent_impervious_area_treated != self.tblControls.item(lid_count-1,3).text() or \
                        value.percent_pervious_area_treated != self.tblControls.item(lid_count - 1, 4).text() or \
                        value.detailed_report_file != self.tblControls.item(lid_count-1,5).text() or \
                        value.number_replicate_units != self.tblControls.item(lid_count-1,6).text() or \
                        value.area_each_unit != self.tblControls.item(lid_count-1,7).text() or \
                        value.top_width_overland_flow_surface != self.tblControls.item(lid_count-1,8).text() or \
                        value.percent_initially_saturated != self.tblControls.item(lid_count-1,9).text() or \
                        value.send_outflow_pervious_area != self.tblControls.item(lid_count-1,10).text() or \
                        value.subcatchment_drains_to != self.tblControls.item(lid_count-1,11).text():
                        self._main_form.mark_project_as_unsaved()

                    value.control_name = self.tblControls.item(lid_count - 1, 0).text()
                    value.percent_impervious_area_treated = self.tblControls.item(lid_count - 1, 3).text()
                    value.percent_pervious_area_treated = self.tblControls.item(lid_count - 1, 4).text()
                    value.detailed_report_file = self.tblControls.item(lid_count - 1, 5).text()
                    value.number_replicate_units = self.tblControls.item(lid_count - 1, 6).text()
                    value.area_each_unit = self.tblControls.item(lid_count - 1, 7).text()
                    value.top_width_overland_flow_surface = self.tblControls.item(lid_count - 1, 8).text()
                    value.percent_initially_saturated = self.tblControls.item(lid_count - 1, 9).text()
                    value.send_outflow_pervious_area = self.tblControls.item(lid_count - 1, 10).text()
                    value.subcatchment_drains_to = self.tblControls.item(lid_count - 1, 11).text()
                if lid_count > row_count:
                    # we removed some rows, remove from the lid list
                    section.value.remove(value)
                    self._main_form.mark_project_as_unsaved()
        if row_count > lid_count:
            # we added some rows, need to add to the lid list
            for row in range(self.tblControls.rowCount()):
                if row > lid_count-1:
                    new_lid = LIDUsage()
                    new_lid.subcatchment_name = self.subcatchment_name
                    new_lid.control_name = self.tblControls.item(row,0).text()
                    new_lid.percent_impervious_area_treated = self.tblControls.item(row,3).text()
                    new_lid.percent_pervious_area_treated = self.tblControls.item(row, 4).text()
                    new_lid.detailed_report_file = self.tblControls.item(row,5).text()
                    new_lid.number_replicate_units = self.tblControls.item(row,6).text()
                    new_lid.area_each_unit = self.tblControls.item(row,7).text()
                    new_lid.top_width_overland_flow_surface = self.tblControls.item(row,8).text()
                    new_lid.percent_initially_saturated = self.tblControls.item(row,9).text()
                    new_lid.send_outflow_pervious_area = self.tblControls.item(row,10).text()
                    new_lid.subcatchment_drains_to = self.tblControls.item(row,11).text()
                    section.value.append(new_lid)
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmLIDControls_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmLIDControls_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def btnAdd_Clicked(self):
        self._frmLIDUsage = frmLIDUsage(self._main_form)
        # add to this subcatchment
        self._frmLIDUsage.set_add(self._main_form.project, self, self.subcatchment_name)
        self._frmLIDUsage.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmLIDUsage.show()

    def btnEdit_Clicked(self):
        self._frmLIDUsage = frmLIDUsage(self._main_form)
        row = self.tblControls.currentRow()
        lid_selected = str(self.tblControls.item(row,0).text())
        # edit the lid for this subcatchment and this lid name
        self._frmLIDUsage.set_edit(self._main_form.project, self, row, lid_selected, self.subcatchment_name)
        self._frmLIDUsage.setWindowModality(QtCore.Qt.ApplicationModal)
        self._frmLIDUsage.show()

    def btnDelete_Clicked(self):
        row = self.tblControls.currentRow()
        self.tblControls.removeRow(row)

    def SetLongLIDName(self, short_name, row):
        lid_name = short_name
        lid_control_section = self._main_form.project.lid_controls
        lid_control_list = lid_control_section.value[0:]
        for lid in lid_control_list:
            if lid.name == short_name:
                # this is the lid
                if lid.lid_type == LIDType.BC:
                    lid_name = 'Bio-Retention'
                elif lid.lid_type == LIDType.RG:
                    lid_name = 'Rain Garden'
                elif lid.lid_type == LIDType.GR:
                    lid_name = 'Green Roof'
                elif lid.lid_type == LIDType.IT:
                    lid_name = 'Infiltration Trench'
                elif lid.lid_type == LIDType.PP:
                    lid_name = 'Permeable Pavement'
                elif lid.lid_type == LIDType.RB:
                    lid_name = 'Rain Barrel'
                elif lid.lid_type == LIDType.RD:
                    lid_name = 'Rooftop Disconnection'
                elif lid.lid_type == LIDType.VS:
                    lid_name = 'Vegetative Swale'
        self.tblControls.setItem(row, 1, QTableWidgetItem(str(lid_name)))

    def SetAreaTerm(self, subcatchment_name, row, number_replicate_units, area_each_unit):
        area = float(number_replicate_units) * float(area_each_unit)

        if self.units < 4:
            conversion_factor = 43560.0
        else:
            conversion_factor = 10000.0

        subcatchment_area = 0.0
        for value in self._main_form.project.subcatchments.value:
            if value.name == subcatchment_name:
                subcatchment_area = value.area

        if type(subcatchment_area) is str:
            if len(subcatchment_area) < 1:
                subcatchment_area = 10.0
        elif float(subcatchment_area) <= 0:
            subcatchment_area = 10.0

        subcatchment_area = float(subcatchment_area) * conversion_factor

        term = '{:5.3f}'.format(100.0 * area/subcatchment_area)
        self.tblControls.setItem(row, 2, QTableWidgetItem(term))
