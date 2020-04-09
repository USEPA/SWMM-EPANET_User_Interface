import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from PyQt5.Qt import QApplication, QClipboard


class frmGenericListOutput(QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, main_form, title):
        QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.fraNotes.setVisible(False)
        self.cmdOK.setVisible(False)
        self.cmdCancel.setText('Close')

    def set_data_by_rows(self, row_headers, column_headers, data_rows):
        """Populate the table.
            Args
            row_headers: list of row headers, or None to not have first column dedicated to headers
            column_headers: list of column headers, or None to not have first row dedicated to headers
            data_rows: list of rows. Each row is a list of values in that row.
        """
        self.tblGeneric.setRowCount(len(data_rows))
        self.tblGeneric.setColumnCount(len(data_rows[0]))

        if row_headers:
            self.tblGeneric.setVerticalHeaderLabels(row_headers)
        else:
            self.tblGeneric.verticalHeader().setVisible(False)
        if column_headers:
            self.tblGeneric.setHorizontalHeaderLabels(column_headers)
        else:
            self.tblGeneric.horizontalHeader().setVisible(False)

        row = 0
        for data_row in data_rows:
            col = 0
            for data_value in data_row:
                item = QTableWidgetItem(str(data_value))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tblGeneric.setItem(row, col, item)
                col += 1
            row += 1
        self.tblGeneric.resizeColumnsToContents()
        for row in range(self.tblGeneric.rowCount()):
            self.tblGeneric.setRowHeight(row, 10)

    def set_data_by_columns(self, row_headers, column_headers, data_columns):
        """Populate the table.
            Args
            row_headers: list of row headers, or None to not have first column dedicated to headers
            column_headers: list of column headers, or None to not have first row dedicated to headers
            data_columns: list of columns. Each column is a list of values in that column.
        """
        self.tblGeneric.setRowCount(len(data_columns[0]))
        self.tblGeneric.setColumnCount(len(data_columns))

        if row_headers:
            self.tblGeneric.setVerticalHeaderLabels(row_headers)
        else:
            self.tblGeneric.verticalHeader().setVisible(False)
        if column_headers:
            self.tblGeneric.setHorizontalHeaderLabels(column_headers)
        else:
            self.tblGeneric.horizontalHeader().setVisible(False)

        col = 0
        for data_column in data_columns:
            row = 0
            for data_value in data_column:
                item = QTableWidgetItem(str(data_value))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tblGeneric.setItem(row, col, item)
                row += 1
            col += 1
        self.tblGeneric.resizeColumnsToContents()
        for row in range(self.tblGeneric.rowCount()):
            self.tblGeneric.setRowHeight(row, 10)

    def set_data(self, nrows, ncols, headers, data):
        counter = -1
        self.tblGeneric.setRowCount(nrows)
        self.tblGeneric.setColumnCount(ncols)
        self.tblGeneric.setHorizontalHeaderLabels(headers)
        self.tblGeneric.verticalHeader().setVisible(False)
        for col in range(ncols):
            for row in range(nrows):
                counter += 1
                item = QTableWidgetItem(str(data[counter]))
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tblGeneric.setItem(row, col, item)
        self.tblGeneric.resizeColumnsToContents()
        for row in range(self.tblGeneric.rowCount()):
            self.tblGeneric.setRowHeight(row, 10)

    def cmdCancel_Clicked(self):
        self.close()

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