import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from core.epanet.reports import Reports
from ui.model_utility import transl8
from ui.EPANET.frmTableDesigner import Ui_frmTable
from ui.EPANET.frmGenericListOutput import frmGenericListOutput
from Externals.epanet.outputapi.ENOutputWrapper import *
from Externals.epanet.outputapi.outputapi import ENR_demand, ENR_head, ENR_pressure, ENR_quality


class frmTable(QtGui.QMainWindow, Ui_frmTable):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.cboFilter.addItems(('Below', 'Equal To', 'Above'))
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.rbnNodes.clicked.connect(self.rbnNodes_Clicked)
        self.rbnLinks.clicked.connect(self.rbnLinks_Clicked)
        self.rbnTimeseriesNode.clicked.connect(self.rbnTimeseriesNode_Clicked)
        self._parent = parent
        self.forms = []

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.report = Reports(project, output)
        self.cboTime.clear()
        if self.project and self.output:
            for time_index in range(0, self.output.numPeriods - 1):
                self.cboTime.addItem(self.report.get_time_string(time_index))
            self.rbnNodes.setChecked(True)
            self.rbnNodes_Clicked()

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.cbxSort.setEnabled(True)
            self.cbxSort.setText(transl8("frmTable", "Sort by Elevation", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_NodeAttributeNames)
            self.lstColumns.selectAll()
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_NodeAttributeNames)

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.cbxSort.setEnabled(True)
            self.cbxSort.setText(transl8("frmTable", "Sort by Length", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_LinkAttributeNames)
            self.lstColumns.selectAll()
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_LinkAttributeNames)

    def rbnTimeseriesNode_Clicked(self):
        if self.rbnTimeseriesNode.isChecked():
            self.cbxSort.setEnabled(False)
            self.cbxSort.setText(transl8("frmTable", "Sort by", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_NodeAttributeNames)
            self.lstColumns.selectAll()
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_NodeAttributeNames)

    def rbnTimeseriesLink_Clicked(self):
        if self.rbnLinks.isChecked():
            self.cbxSort.setEnabled(False)
            self.cbxSort.setText(transl8("frmTable", "Sort by", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_LinkAttributeNames)
            self.lstColumns.selectAll()
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_LinkAttributeNames)

    def cmdOK_Clicked(self):
        row_headers = []
        column_headers = []
        parameter_codes = []
        if self.rbnNodes.isChecked() or self.rbnTimeseriesNode.isChecked():
            get_index = self.output.get_NodeIndex
            get_value = self.output.get_NodeValue
            get_series = self.output.get_NodeSeries
            ids = self.report.all_node_ids()
            for node_type, node_id in zip(self.report.all_node_types(), ids):
                row_headers.append(node_type + ' ' + node_id)
            for column_item in self.lstColumns.selectedItems():
                attribute_name = str(column_item.text())
                attribute_index = ENR_NodeAttributeNames.index(attribute_name)
                parameter_codes.append(ENR_NodeAttributes[attribute_index])
                units = ENR_NodeAttributeUnits[attribute_index][self.report.unit_system]
                if units:
                    attribute_name += '\n(' + units + ')'
                column_headers.append(attribute_name)

        else:  # if self.rbnLinks.isChecked() or self.rbnTimeseriesLink.isChecked():
            get_index = self.output.get_LinkIndex
            get_value = self.output.get_LinkValue
            ids = self.report.all_link_ids()
            for link_type, link_id in zip(self.report.all_link_types(), ids):
                row_headers.append(link_type + ' ' + link_id)
            for column_item in self.lstColumns.selectedItems():
                attribute_name = str(column_item.text())
                attribute_index = ENR_LinkAttributeNames.index(attribute_name)
                parameter_codes.append(ENR_LinkAttributes[attribute_index])
                units = ENR_LinkAttributeUnits[attribute_index][self.report.unit_system]
                if units:
                    attribute_name += '\n(' + units + ')'
                column_headers.append(attribute_name)

        frm = frmGenericListOutput(self.parent(),"EPANET Table Output")
        if self.rbnNodes.isChecked() or self.rbnLinks.isChecked():
            self.make_table(frm, get_index, get_value, self.cboTime.currentIndex(),
                            ids, row_headers, parameter_codes, column_headers)
        else:
            id = self.txtNodeLink.text()  # TODO: turn this textbox into combo box?
            self.make_timeseries_table(frm, get_index, get_series, id, parameter_codes, column_headers)
            return
        frm.tblGeneric.resizeColumnsToContents()
        frm.show()
        self.forms.append(frm)
        # self.close()

    def make_table(self, frm, get_index, get_value, time_index, ids, row_headers, parameter_codes, column_headers):
        frm.setWindowTitle("Network Table at " + self.report.get_time_string(time_index))
        tbl = frm.tblGeneric

        tbl.setRowCount(len(row_headers))
        tbl.setColumnCount(len(column_headers))
        tbl.setHorizontalHeaderLabels(column_headers)
        tbl.setVerticalHeaderLabels(row_headers)

        row = 0
        for this_id in ids:
            col = 0
            for parameter_code in parameter_codes:
                output_index = get_index(this_id)
                if output_index >= 0:
                    val = get_value(output_index, time_index, parameter_code)
                    if parameter_code == ENR_status and val in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
                        val_str = ('Closed', 'Closed', 'Closed', 'Open', 'Active', 'Open', 'Open', 'Open')[int(val)]
                    else:
                        val_str = '{:7.2f}'.format(val)

                    # str(parameter_code) + ' (' + ENR_NodeAttributeNames[parameter_code] + '), ' + str(this_id))
                    item = QtGui.QTableWidgetItem(val_str)
                    item.setFlags(QtCore.Qt.ItemIsSelectable)  # | QtCore.Qt.ItemIsEnabled)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    tbl.setItem(row, col, item)
                col += 1
            row += 1

    def cmdCancel_Clicked(self):
        self.close()
