import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from Externals.epanet.outputapi.ENOutputWrapper import ENR_node_type, ENR_link_type
from core.epanet.reports import Reports
from ui.EPANET.frmTableDesigner import Ui_frmTable
from ui.frmGenericListOutput import frmGenericListOutput
from ui.model_utility import transl8, process_events


class frmTable(QMainWindow, Ui_frmTable):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Table_Op.htm"
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.cboCompare.addItems(('Below', 'Equal To', 'Above'))
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cmdAdd.clicked.connect(self.cmdAdd_Clicked)
        self.cmdDelete.clicked.connect(self.cmdDelete_Clicked)
        self.rbnNodes.clicked.connect(self.rbnNodes_Clicked)
        self.rbnLinks.clicked.connect(self.rbnLinks_Clicked)
        self.rbnTimeseriesNode.clicked.connect(self.rbnTimeseriesNode_Clicked)
        self.rbnTimeseriesLink.clicked.connect(self.rbnTimeseriesLink_Clicked)
        self._main_form = main_form
        self.item_type = ENR_node_type
        self.forms = []

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.report = Reports(project, output)
        self.cboTime.clear()
        if self.project and self.output:
            for time_index in range(0, self.output.num_periods):
                #if self.???:  TODO: give choice between elapsed hours and date
                self.cboTime.addItem(self.output.get_time_string(time_index))
                #else:
                #    self.cboTime.addItem(self.output.get_date_string(time_index))

            self.rbnNodes.setChecked(True)
            self.rbnNodes_Clicked()

    def rbnNodes_Clicked(self):
        if self.rbnNodes.isChecked():
            self.item_type = ENR_node_type
            self.set_attributes()
            self.cbxSort.setEnabled(True)
            self.cbxSort.setText(transl8("frmTable", "Sort by Elevation", None))
            self.rbnLinks.setChecked(False)
            self.rbnTimeseriesNode.setChecked(False)
            self.rbnTimeseriesLink.setChecked(False)

    def rbnLinks_Clicked(self):
        if self.rbnLinks.isChecked():
            self.item_type = ENR_link_type
            self.set_attributes()
            self.cbxSort.setEnabled(True)
            self.cbxSort.setText(transl8("frmTable", "Sort by Length", None))
            self.rbnNodes.setChecked(False)
            self.rbnTimeseriesNode.setChecked(False)
            self.rbnTimeseriesLink.setChecked(False)

    def rbnTimeseriesNode_Clicked(self):
        if self.rbnTimeseriesNode.isChecked():
            self.item_type = ENR_node_type
            self.set_attributes()
            self.cbxSort.setEnabled(False)
            self.cbxSort.setText(transl8("frmTable", "Sort by", None))
            self.rbnNodes.setChecked(False)
            self.rbnLinks.setChecked(False)
            self.rbnTimeseriesLink.setChecked(False)

    def rbnTimeseriesLink_Clicked(self):
        if self.rbnTimeseriesLink.isChecked():
            self.item_type = ENR_link_type
            self.set_attributes()
            self.cbxSort.setEnabled(False)
            self.cbxSort.setText(transl8("frmTable", "Sort by", None))
            self.rbnNodes.setChecked(False)
            self.rbnLinks.setChecked(False)
            self.rbnTimeseriesNode.setChecked(False)

    def set_attributes(self):
        self.lstColumns.clear()
        attribute_names = [attribute.name for attribute in self.item_type.Attributes]
        self.lstColumns.addItems(attribute_names)
        self.lstColumns.selectAll()
        self.cboFilter.clear()
        self.cboFilter.addItems(attribute_names)

    def cmdOK_Clicked(self):
        row_headers = []
        column_headers = []
        attributes = []
        quality_name = ""
        if hasattr(self.item_type, "AttributeQuality"):
            quality_name = self.item_type.AttributeQuality.name

        for column_index in self.lstColumns.selectedIndexes():
            attribute_index = column_index.row()
            if attribute_index < len(self.item_type.Attributes):
                attribute = self.item_type.Attributes[attribute_index]
                attributes.append(attribute)
                column_header = attribute.name
                units = ""
                if attribute.name == quality_name:
                    if self.project.options.quality.quality.value == 2: # 'chemical'
                        column_header = "Chemical"
                        units = attribute.units(self.output.unit_system)
                    elif self.project.options.quality.quality.value == 3: # 'Age'
                        column_header = "Age"
                        units = "hours"
                    elif self.project.options.quality.quality.value == 4:  # 'Trace'
                        column_header = "Trace " + self.project.options.quality.trace_node
                        units = "percent"
                else:
                    units = attribute.units(self.output.unit_system)
                if units:
                    column_header += '\n(' + units + ')'
                column_headers.append(column_header)
            else:
                print ("Did not find attribute " + attribute_index)

        frm = frmGenericListOutput(self._main_form, "EPANET Table Output")
        if self.rbnNodes.isChecked() or self.rbnLinks.isChecked():
            items_in_order = list()
            if self.rbnNodes.isChecked():
                for item in self.report.all_nodes_set_category():
                    items_in_order.append(item)
                    row_headers.append(item.category + ' ' + item.name)
            else:
                for item in self.report.all_links_set_category():
                    items_in_order.append(item)
                    row_headers.append(item.category + ' ' + item.name)
            time_index = self.cboTime.currentIndex()
            title = "Network Table - " + self.item_type.TypeLabel + "s at "+ self.output.get_time_string(time_index)
            self.make_table(frm, title, time_index, items_in_order,
                            row_headers, attributes, column_headers)
        else:
            name = self.txtNodeLink.text()  # TODO: turn this textbox into combo box or list?
            if self.rbnTimeseriesNode.isChecked():
                item = self.output.nodes[name]
            else:
                item = self.output.links[name]
            title = "Time Series Table - " + self.item_type.TypeLabel + ' ' + name
            self.make_timeseries_table(frm, title, item, attributes, column_headers)
        frm.tblGeneric.resizeColumnsToContents()
        frm.show()
        frm.update()
        self.forms.append(frm)
        # self.close()

    def make_table(self, frm, title, time_index, items, row_headers, attributes, column_headers):
        frm.setWindowTitle(title)
        tbl = frm.tblGeneric

        tbl.setRowCount(len(row_headers))
        tbl.setColumnCount(len(column_headers))
        tbl.setHorizontalHeaderLabels(column_headers)
        tbl.setVerticalHeaderLabels(row_headers)

        row = 0
        for this_item in items:
            col = 0
            values = this_item.get_all_attributes_at_time(self.output, time_index)
            for attribute in attributes:
                val_str = attribute.str(values[attribute.index])
                table_cell_widget = QTableWidgetItem(val_str)
                table_cell_widget.setFlags(QtCore.Qt.ItemIsSelectable)  # | QtCore.Qt.ItemIsEnabled)
                table_cell_widget.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                tbl.setItem(row, col, table_cell_widget)
                col += 1
            row += 1
            if row == 20:
                tbl.resizeColumnsToContents()
                frm.show()
                frm.update()
                process_events()

    def make_timeseries_table(self, frm, title, item, attributes, column_headers):
        frm.setWindowTitle(title)
        row_headers = []
        for time_index in range(0, self.output.num_periods):
            row_headers.append(self.output.get_time_string(time_index))
        tbl = frm.tblGeneric
        tbl.setRowCount(len(row_headers))
        tbl.setColumnCount(len(column_headers))
        tbl.setHorizontalHeaderLabels(column_headers)
        tbl.setVerticalHeaderLabels(row_headers)

        if item:
            row = 0
            for time_index in range(0, self.output.num_periods):
                col = 0
                values = item.get_all_attributes_at_time(self.output, time_index)
                for attribute in attributes:
                    val_str = attribute.str(values[attribute.index])
                    table_cell_widget = QTableWidgetItem(val_str)
                    table_cell_widget.setFlags(QtCore.Qt.ItemIsSelectable)  # | QtCore.Qt.ItemIsEnabled)
                    table_cell_widget.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    tbl.setItem(row, col, table_cell_widget)
                    col += 1
                row += 1

    def cmdCancel_Clicked(self):
        self.close()

    def cmdAdd_Clicked(self):
        qty = self.cboFilter.currentText()
        comp = self.cboCompare.currentText()
        val = self.txtValue.text()
        entry = qty + " " + comp + " " + val
        if self.lstFilter.count() == 0:
            self.lstFilter.addItem(entry)
        else:
            if not self.lstFilter.findItems(entry, QtCore.Qt.MatchCaseSensitive):
                self.lstFilter.addItem(entry)
        pass

    def cmdDelete_Clicked(self):
        if not self.lstFilter.selectedItems(): return
        for wi in self.lstFilter.selectedItems():
            self.lstFilter.takeItem(self.lstFilter.row(wi))
        pass
