import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from ui.SWMM.frmLIDControlsDesigner import Ui_frmLIDControls
from ui.SWMM.frmLIDUsage import frmLIDUsage
from core.swmm.hydrology.lidcontrol import LIDType
from core.swmm.hydrology.subcatchment import LIDUsage


class frmLIDControls(QtGui.QMainWindow, Ui_frmLIDControls):

    def __init__(self, main_form, subcatchment_name):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/lidgroupeditor.htm"
        self.units = main_form.project.options.flow_units.value
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.btnAdd_Clicked)
        QtCore.QObject.connect(self.btnEdit, QtCore.SIGNAL("clicked()"), self.btnEdit_Clicked)
        QtCore.QObject.connect(self.btnDelete, QtCore.SIGNAL("clicked()"), self.btnDelete_Clicked)
        self._main_form = main_form
        # set for first subcatchment for now
        self.subcatchment_name = subcatchment_name
        self.set_subcatchment(main_form.project, subcatchment_name)

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
                self.tblControls.setItem(lid_count,0,QtGui.QTableWidgetItem(str(value.control_name)))

                self.SetLongLIDName(value.control_name,lid_count)
                self.SetAreaTerm(subcatchment_name, lid_count, value.number_replicate_units, value.area_each_unit)

                self.tblControls.setItem(lid_count,3,QtGui.QTableWidgetItem(str(value.percent_impervious_area_treated)))

                self.tblControls.setItem(lid_count,4,QtGui.QTableWidgetItem(str(value.detailed_report_file)))

                # store the other param values in hidden columns
                self.tblControls.setItem(lid_count,5,QtGui.QTableWidgetItem(str(value.number_replicate_units)))
                self.tblControls.setItem(lid_count,6,QtGui.QTableWidgetItem(str(value.area_each_unit)))
                self.tblControls.setItem(lid_count,7,QtGui.QTableWidgetItem(str(value.top_width_overland_flow_surface)))
                self.tblControls.setItem(lid_count,8,QtGui.QTableWidgetItem(str(value.percent_initially_saturated)))
                self.tblControls.setItem(lid_count,9,QtGui.QTableWidgetItem(str(value.send_outflow_pervious_area)))
                self.tblControls.setItem(lid_count,10,QtGui.QTableWidgetItem(str(value.subcatchment_drains_to)))

        self.tblControls.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblControls.setColumnHidden(5,True)
        self.tblControls.setColumnHidden(6,True)
        self.tblControls.setColumnHidden(7,True)
        self.tblControls.setColumnHidden(8,True)
        self.tblControls.setColumnHidden(9,True)
        self.tblControls.setColumnHidden(10,True)

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
                    value.control_name = self.tblControls.item(lid_count-1,0).text()
                    value.percent_impervious_area_treated = self.tblControls.item(lid_count-1,3).text()
                    value.detailed_report_file = self.tblControls.item(lid_count-1,4).text()
                    value.number_replicate_units = self.tblControls.item(lid_count-1,5).text()
                    value.area_each_unit = self.tblControls.item(lid_count-1,6).text()
                    value.top_width_overland_flow_surface = self.tblControls.item(lid_count-1,7).text()
                    value.percent_initially_saturated = self.tblControls.item(lid_count-1,8).text()
                    value.send_outflow_pervious_area = self.tblControls.item(lid_count-1,9).text()
                    value.subcatchment_drains_to = self.tblControls.item(lid_count-1,10).text()
                if lid_count > row_count:
                    # we removed some rows, remove from the lid list
                    section.value.remove(value)
        if row_count > lid_count:
            # we added some rows, need to add to the lid list
            for row in range(self.tblControls.rowCount()):
                if row > lid_count-1:
                    new_lid = LIDUsage()
                    new_lid.subcatchment_name = self.subcatchment_name
                    new_lid.control_name = self.tblControls.item(row,0).text()
                    new_lid.percent_impervious_area_treated = self.tblControls.item(row,3).text()
                    new_lid.detailed_report_file = self.tblControls.item(row,4).text()
                    new_lid.number_replicate_units = self.tblControls.item(row,5).text()
                    new_lid.area_each_unit = self.tblControls.item(row,6).text()
                    new_lid.top_width_overland_flow_surface = self.tblControls.item(row,7).text()
                    new_lid.percent_initially_saturated = self.tblControls.item(row,8).text()
                    new_lid.send_outflow_pervious_area = self.tblControls.item(row,9).text()
                    new_lid.subcatchment_drains_to = self.tblControls.item(row,10).text()
                    section.value.append(new_lid)
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
        self.tblControls.setItem(row, 1, QtGui.QTableWidgetItem(str(lid_name)))

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

        if len(subcatchment_area) < 1:
            subcatchment_area = 10.0
        elif subcatchment_area <= 0:
            subcatchment_area = 10.0

        subcatchment_area = float(subcatchment_area) * conversion_factor

        term = '{:5.3f}'.format(100.0 * area/subcatchment_area)
        self.tblControls.setItem(row, 2, QtGui.QTableWidgetItem(term))
