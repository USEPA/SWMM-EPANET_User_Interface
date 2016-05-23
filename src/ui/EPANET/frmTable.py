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
        if project and self.output:
            for time_index in range(0, self.output.numPeriods - 1):
                self.cboTime.addItem(self.time_string(time_index))
            self.rbnNodes.setChecked(True)
            self.rbnNodes_Clicked()

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.cbxSort.setEnabled(True)
            self.cbxSort.setText(transl8("frmTable", "Sort by Elevation", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_NodeAttributeNames)
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_NodeAttributeNames)

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.cbxSort.setEnabled(True)
            self.cbxSort.setText(transl8("frmTable", "Sort by Length", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_LinkAttributeNames)
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_LinkAttributeNames)

    def rbnTimeseriesNode_Clicked(self):
        if self.rbnTimeseriesNode.isChecked():
            self.cbxSort.setEnabled(False)
            self.cbxSort.setText(transl8("frmTable", "Sort by", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_NodeAttributeNames)
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_NodeAttributeNames)

    def rbnTimeseriesLink_Clicked(self):
        if self.rbnLinks.isChecked():
            self.cbxSort.setEnabled(False)
            self.cbxSort.setText(transl8("frmTable", "Sort by", None))
            self.lstColumns.clear()
            self.lstColumns.addItems(ENR_LinkAttributeNames)
            self.cboFilter.clear()
            self.cboFilter.addItems(ENR_LinkAttributeNames)

    def cmdOK_Clicked(self):
        frm = frmGenericListOutput(self.parent(),"EPANET Table Output")
        if self.rbnNodes.isChecked():
            self.make_node_table(frm)


        frm.show()
        self.forms.append(frm)
        # self.close()

    def make_node_table(self, frm):
        column_headers = ["Node ID"]
        column_data = []
        for column_item in self.lstColumns.selectedItems():
            column_headers.append(str(column_item.text()))
            column_data.append([])

        all_node_ids = self.report.all_node_ids()
        for node_id in all_node_ids:
            column_data[0].append(node_id)
            for column_list in column_data:
                column_list.append(123.456)

        num_rows = len(column_data[0])
        local_data = []
        for column_list in column_data:
            local_data.extend(column_list)

        frm.set_data(num_rows,len(column_headers),column_headers,local_data)


    def cmdCancel_Clicked(self):
        self.close()
