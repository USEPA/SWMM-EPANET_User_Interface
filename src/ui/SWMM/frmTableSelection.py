import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QMessageBox

import Externals.swmm.outputapi.SMOutputWrapper as SMO
from ui.SWMM.frmTableSelectionDesigner import Ui_frmTableSelection
from ui.frmGenericListOutput import frmGenericListOutput


class frmTableSelection(QMainWindow, Ui_frmTableSelection):

    def __init__(self, main_form):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/tablebyobjectdialog.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._main_form = main_form
        self.cboTime.currentIndexChanged.connect(self.cboTime_currentIndexChanged)
        self.cboObject.currentIndexChanged.connect(self.cboObject_currentIndexChanged)
        self.cboObject.setCurrentIndex(0)
        self.lstNodes.setSelectionMode(QAbstractItemView.MultiSelection)
        self.lstVariables.setSelectionMode(QAbstractItemView.MultiSelection)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        self.cboEnd.clear()
        if project and self.output:
            self.cboTime.addItems(["Elapsed Time", "Date/Time"])
            self.cboTime.setCurrentIndex(0)
            self.cboObject.addItems(SMO.swmm_output_object_labels)
            self.cboObject.setCurrentIndex(0)

    def cmdOK_Clicked(self):
        selected_locations = [str(location.data()) for location in self.lstNodes.selectedIndexes()]
        if not selected_locations:
            QMessageBox.information(None, "Table",
                                          "No locations are selected.",
                                          QMessageBox.Ok)
            return
        object_label = self.cboObject.currentText()
        start_index = self.cboStart.currentIndex()
        end_index = self.cboEnd.currentIndex()
        num_steps = end_index - start_index + 1

        num_columns = 1
        column_headers = []
        row_headers = []
        # column_headers.append('Date')
        elapsed_flag = self.cboTime.currentIndex() == 0
        for time_index in range(start_index, end_index + 1):
            if elapsed_flag:
                time_string = self.output.get_time_string(time_index)
            else:
                time_string = self.output.get_date_string(time_index)
            row_headers.append(time_string)

        title = "Table - " + object_label + " Results"
        if len(selected_locations) == 1 and selected_locations[0] != "-1":
            title += " at " + selected_locations[0]
        self.setWindowTitle(title)
        column_data = []
        items = self.output.get_items(object_label)
        for selected_location in selected_locations:
            for variable in self.lstVariables.selectedIndexes():
                selected_variable = str(variable.data())
                # for each selected location, for each selected variable
                item = items[selected_location]
                if item:
                    attribute = item.get_attribute_by_name(selected_variable)
                    this_column_values = item.get_series(self.output, attribute, start_index, num_steps)
                    units = attribute.units(self.output.unit_system)
                    if units:
                        units = '\n(' + units + ')'
                    if len(selected_locations) == 1:
                        column_headers.append(selected_variable + units)
                    else:
                        column_headers.append(selected_variable + ' at ' + object_label + ' ' + selected_location + units)
                    num_columns += 1
                    this_column_formatted = [attribute.str(val) for val in this_column_values]
                    column_data.append(this_column_formatted)

        self._frmOutputTable = frmGenericListOutput(self._main_form, "SWMM Table Output")
        self._frmOutputTable.set_data_by_columns(row_headers, column_headers, column_data)
        self._frmOutputTable.show()
        # self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboObject_currentIndexChanged(self, newIndex):
        object_type = SMO.swmm_output_object_types[newIndex]
        self.lblNodes.setText(object_type.type_label)

        self.lstNodes.clear()
        for item in self.output.all_items[newIndex]:
            self.lstNodes.addItem(item)
        if object_type == SMO.SwmmOutputSystem:
            self.lstNodes.item(0).setSelected(True)
            self.lstNodes.setVisible(False)
            self.lblNodes.setVisible(False)
        else:
            self.lstNodes.setVisible(True)
            self.lblNodes.setVisible(True)

        self.lstVariables.clear()
        for attribute in object_type.attributes:
            self.lstVariables.addItem(attribute.name)

    def cboTime_currentIndexChanged(self, newIndex):
        self.cboStart.clear()
        self.cboEnd.clear()
        for time_index in range(0, self.output.num_periods):
            if newIndex == 0:
                time_string = self.output.get_time_string(time_index)
            else:
                time_string = self.output.get_date_string(time_index)
            self.cboStart.addItem(time_string)
            self.cboEnd.addItem(time_string)
        self.cboStart.setCurrentIndex(0)
        self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)

