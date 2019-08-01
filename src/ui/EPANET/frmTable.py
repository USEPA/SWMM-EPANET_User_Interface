import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication, QClipboard

from Externals.epanet.outputapi.ENOutputWrapper import ENR_node_type, ENR_link_type
from core.epanet.reports import Reports
from ui.EPANET.frmTableDesigner import Ui_frmTable
from ui.frmGenericListOutput import frmGenericListOutput
from ui.model_utility import transl8, process_events
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.link import Pipe


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
        self.cbxSort.setVisible(False)

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
        if self.item_type == ENR_node_type:
            self.property_attributes = ['Elevation', 'Base Demand', 'Initial Quality']
        elif self.item_type == ENR_link_type:
            self.property_attributes = ['Length', 'Diameter', 'Roughness', 'Bulk Coeff.', 'Wall Coeff.']
        self.lstColumns.addItems(self.property_attributes)
        attribute_names = [attribute.name for attribute in self.item_type.Attributes]
        self.lstColumns.addItems(attribute_names)
        self.lstColumns.selectAll()
        self.lstColumns.item(0).setSelected(False)
        self.lstColumns.item(1).setSelected(False)
        self.lstColumns.item(2).setSelected(False)
        if self.item_type == ENR_link_type:
            self.lstColumns.item(3).setSelected(False)
            self.lstColumns.item(4).setSelected(False)

        self.cboFilter.clear()
        if self.item_type == ENR_node_type:
            self.cboFilter.addItems(['Elevation', 'Base Demand', 'Initial Quality'])
        elif self.item_type == ENR_link_type:
            self.cboFilter.addItems(['Length', 'Diameter', 'Roughness', 'Bulk Coeff.', 'Wall Coeff.'])
        self.cboFilter.addItems(attribute_names)


    def cmdOK_Clicked(self):
        row_headers = []
        column_headers = []
        requested_output_attributes = []
        requested_property_attributes = []
        quality_name = ""
        if hasattr(self.item_type, "AttributeQuality"):
            quality_name = self.item_type.AttributeQuality.name

        for column_index in self.lstColumns.selectedIndexes():
            attribute_index = column_index.row() - len(self.property_attributes)
            if attribute_index < 0:
                # these are properties of the class
                attribute_index = attribute_index + len(self.property_attributes)
                column_header = self.property_attributes[attribute_index]
                if self.rbnNodes.isChecked():
                    meta_item = Junction.metadata.meta_item_of_label(column_header)
                else:
                    meta_item = Pipe.metadata.meta_item_of_label(column_header)
                attribute = meta_item.attribute
                if attribute:
                    units = ""
                    if self.output.unit_system == 0:
                        units = meta_item.units_english
                    elif self.output.unit_system == 1:
                        units = meta_item.units_metric
                    if len(units) == 0:
                        if attribute == 'base_demand_flow':
                            units = '(' + self.project.options.hydraulics.flow_units.name + ')'
                    if units:
                        column_header += '\n' + units
                    column_headers.append(column_header)
                    requested_property_attributes.append(self.property_attributes[attribute_index])
            elif attribute_index < len(self.item_type.Attributes):
                # these are output variables
                attribute = self.item_type.Attributes[attribute_index]
                requested_output_attributes.append(attribute)
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
                print ("Did not find attribute " + str(attribute_index))

        frm = frmGenericListOutput(self._main_form, "EPANET Table Output")

        if self.rbnNodes.isChecked() or self.rbnLinks.isChecked():
            output_items = list()
            property_items = list()
            time_index = self.cboTime.currentIndex()

            # property items
            if self.rbnNodes.isChecked():
                for item in self.project.all_nodes():
                    property_items.append(item)
            else:
                for item in self.project.all_links():
                    property_items.append(item)

            # output items
            if self.rbnNodes.isChecked():
                for item in self.report.all_nodes_set_category():
                    output_items.append(item)
                    row_headers.append(item.category + ' ' + item.name)
            else:
                for item in self.report.all_links_set_category():
                    output_items.append(item)
                    row_headers.append(item.category + ' ' + item.name)

            title = "Network Table - " + self.item_type.TypeLabel + "s at "+ self.output.get_time_string(time_index)
            self.make_table(frm, title, time_index, row_headers, column_headers,
                            property_items, requested_property_attributes,
                            output_items, requested_output_attributes)

        else:
            name = self.txtNodeLink.text()  # TODO: turn this textbox into combo box or list?
            if self.rbnTimeseriesNode.isChecked():
                item = self.output.nodes[name]
            else:
                item = self.output.links[name]
            title = "Time Series Table - " + self.item_type.TypeLabel + ' ' + name
            self.make_timeseries_table(frm, title, item, requested_output_attributes, column_headers)
        frm.tblGeneric.resizeColumnsToContents()
        frm.show()
        frm.update()
        self.forms.append(frm)
        # self.close()

    def check_filters(self, values):
        ok_to_append = True
        for i in range(0, self.lstFilter.count()):
            word_list = self.lstFilter.item(i).text().split()
            qty = word_list[0]
            comp = word_list[1]
            val = word_list[2]
            pos = self.cboFilter.findText(qty) + 1
            if pos > 0:
                if comp == 'Below':
                    if values[pos] >= float(val):
                        ok_to_append = False
                elif comp == 'Equal To':
                    if values[pos] > float(val):
                        ok_to_append = False
                    if values[pos] < float(val):
                        ok_to_append = False
                elif comp == 'Above':
                    if values[pos] <= float(val):
                        ok_to_append = False
        return ok_to_append

    def make_table(self, frm, title, time_index, row_headers, column_headers,
                   property_items, requested_property_attributes,
                   output_items, requested_output_attributes):

        frm.setWindowTitle(title)
        tbl = frm.tblGeneric

        tbl.setRowCount(len(row_headers))
        tbl.setColumnCount(len(column_headers))
        tbl.setHorizontalHeaderLabels(column_headers)
        tbl.setVerticalHeaderLabels(row_headers)

        # first set from properties
        row = 0
        for this_item in property_items:
            col = 0
            for selected_property_attribute in requested_property_attributes:
                if self.rbnNodes.isChecked():
                    meta_item = Junction.metadata.meta_item_of_label(selected_property_attribute)
                else:
                    meta_item = Pipe.metadata.meta_item_of_label(selected_property_attribute)
                attribute = meta_item.attribute
                if attribute:  # Found an attribute
                    val_str = str(getattr(this_item, attribute, 0))
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

        # now set from output values
        row = 0
        for this_item in output_items:
            col = len(requested_property_attributes)
            values = this_item.get_all_attributes_at_time(self.output, time_index)
            for attribute in requested_output_attributes:
                val_str = attribute.str(values[attribute.index])
                table_cell_widget = QTableWidgetItem(val_str)
                table_cell_widget.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                table_cell_widget.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                tbl.setItem(row, col, table_cell_widget)
                col += 1
            row += 1
            if row == 20:
                tbl.resizeColumnsToContents()
                frm.show()
                frm.update()
                process_events()

        # now remove the rows that fail the filter check
        rows_to_remove = []
        for i in range(0, self.lstFilter.count()):
            word_list = self.lstFilter.item(i).text().split()
            val = word_list[len(word_list)-1]
            comp = word_list[len(word_list)-2]
            qty = ''
            for word_index in range(0, len(word_list)-2):
                qty += word_list[word_index]
                if word_index < len(word_list)-3:
                    qty += ' '
            pos = self.cboFilter.findText(qty)
            if pos > 0:
                # for each row of the grid
                for irow in range(0, tbl.rowCount()):
                    remove_me = False
                    value = float(tbl.item(irow, pos).text())
                    if comp == 'Below':
                        if value >= float(val):
                            remove_me = True
                    elif comp == 'Equal To':
                        if value != float(val):
                            remove_me = True
                    elif comp == 'Above':
                        if value <= float(val):
                            remove_me = True
                    if remove_me and not irow in rows_to_remove:
                        rows_to_remove.append(irow)
         # now go ahead and remove those rows
        removed_count = 0
        for row_number in rows_to_remove:
            tbl.removeRow(int(row_number)-removed_count)
            removed_count += 1
        for row in range(tbl.rowCount()):
            tbl.setRowHeight(row, 10)

        # do sort
        # tbl.sortByColumn(1, Qt.AscendingOrder)
        # sorting not yet enabled


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
                    table_cell_widget.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    table_cell_widget.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    tbl.setItem(row, col, table_cell_widget)
                    col += 1
                row += 1
        for row in range(tbl.rowCount()):
            tbl.setRowHeight(row, 10)

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

    def copy(self):
        selected_range = self.tblGeneric.selectedRanges()[0]
        str = ""
        for i in range(selected_range.rowCount()):
            if i > 0:
                str += "\n"
            for j in range(selected_range.columnCount()):
                if j > 0:
                    str += "\t"
                str += self.tblGeneric.item(selected_range.topRow() + i, selected_range.leftColumn() + j).text()
        str += "\n"
        QApplication.clipboard().setText(str)

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy):
            self.copy()