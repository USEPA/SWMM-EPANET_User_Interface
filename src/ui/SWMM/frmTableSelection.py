import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import Externals.swmm.outputapi.SMOutputWrapper as SMO
from ui.SWMM.frmTableSelectionDesigner import Ui_frmTableSelection
from ui.frmGenericListOutput import frmGenericListOutput


class frmTableSelection(QtGui.QMainWindow, Ui_frmTableSelection):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/tablebyobjectdialog.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        # self.set_from(parent.project)
        self._main_form = main_form
        self.cboTime.currentIndexChanged.connect(self.cboTime_currentIndexChanged)
        self.cboObject.currentIndexChanged.connect(self.cboObject_currentIndexChanged)
        self.cboObject.setCurrentIndex(0)
        self.lstNodes.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.lstVariables.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        self.cboEnd.clear()
        if project and self.output:
            self.cboTime.addItems(["Elapsed Time", "Date/Time"])
            self.cboTime.setCurrentIndex(0)
            self.cboObject.addItems(SMO.SMO_objectTypeLabels)
            self.cboObject.setCurrentIndex(0)

    def cmdOK_Clicked(self):
        selected_locations = [str(location.data()) for location in self.lstNodes.selectedIndexes()]
        if not selected_locations:
            QtGui.QMessageBox.information(None, "Table",
                                          "No locations are selected.",
                                          QtGui.QMessageBox.Ok)
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
        for selected_location in selected_locations:
            for variable in self.lstVariables.selectedIndexes():
                selected_variable = str(variable.data())
                # for each selected location, for each selected variable
                this_column_values, units = self.output.get_series_by_name(object_label,
                                                                           selected_location,
                                                                           selected_variable,
                                                                           start_index, num_steps)
                if units:
                    units = '\n(' + units + ')'
                if len(selected_locations) == 1:
                    column_headers.append(selected_variable + units)
                else:
                    column_headers.append(selected_variable + ' at ' + object_label + ' ' + selected_location + units)
                num_columns += 1
                this_column_formatted = ['{:7.2f}'.format(val) for val in this_column_values]
                column_data.append(this_column_formatted)

        self._frmOutputTable = frmGenericListOutput(self._main_form, "SWMM Table Output")
        self._frmOutputTable.set_data_by_columns(row_headers, column_headers, column_data)
        self._frmOutputTable.show()
        # self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboObject_currentIndexChanged(self, newIndex):
        object_type = SMO.SMO_objectTypes[newIndex]
        self.lblNodes.setText(object_type.TypeLabel)

        self.lstNodes.clear()
        for item in self.output.all_items[newIndex]:
            self.lstNodes.addItem(item.id)
        if object_type == SMO.SMO_system:
            self.lstNodes.item(0).setSelected(True)
            self.lstNodes.setVisible(False)
            self.lblNodes.setVisible(False)
        else:
            self.lstNodes.setVisible(True)
            self.lblNodes.setVisible(True)

        self.lstVariables.clear()
        for variable in object_type.AttributeNames:
            self.lstVariables.addItem(variable)

    def cboTime_currentIndexChanged(self, newIndex):
        self.cboStart.clear()
        self.cboEnd.clear()
        for time_index in range(0, self.output.numPeriods):
            if newIndex == 0:
                time_string = self.output.get_time_string(time_index)
            else:
                time_string = self.output.get_date_string(time_index)
            self.cboStart.addItem(time_string)
            self.cboEnd.addItem(time_string)
        self.cboStart.setCurrentIndex(0)
        self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)

