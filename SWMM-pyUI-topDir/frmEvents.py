import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView
from frmEventsDesigner import Ui_frmEvents
from core.swmm.options.events import Events
from core.indexed_list import IndexedList


class frmEvents(QMainWindow, Ui_frmEvents):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/events_editor.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.tableWidget.itemSelectionChanged.connect(self.tableSelectionChanged)
        self.btnAdd.clicked.connect(self.btnAdd_Clicked)
        self.btnReplace.clicked.connect(self.btnReplace_Clicked)
        self.btnDelete.clicked.connect(self.btnDelete_Clicked)
        self.btnDeleteAll.clicked.connect(self.btnDeleteAll_Clicked)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.project = main_form.project
        self.set_from(main_form.project)
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmEvents_geometry") and
                main_form.program_settings.value("Geometry/" + "frmEvents_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmEvents_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmEvents_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        section = project.events
        for event in section.value:
            numRows = self.tableWidget.rowCount()
            self.tableWidget.insertRow(numRows)
            # Add text to the row
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Checked)
            self.tableWidget.setItem(numRows, 0, chkBoxItem)

            txtItem1 = QTableWidgetItem(event.start_date)
            txtItem1.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(numRows, 1, txtItem1)

            txtItem2 = QTableWidgetItem(event.start_time)
            txtItem2.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(numRows, 2, txtItem2)

            txtItem3 = QTableWidgetItem(event.end_date)
            txtItem3.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(numRows, 3, txtItem3)

            txtItem4 = QTableWidgetItem(event.end_time)
            txtItem4.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(numRows, 4, txtItem4)

            self.tableWidget.setRowHeight(numRows,20)
            self.tableWidget.setCurrentCell(0,0)
        self.tableWidget.resizeColumnsToContents()
        pass

    def tableSelectionChanged(self):
        selectedRow = self.tableWidget.currentRow()
        self.dedStart.setDate(QtCore.QDate.fromString(self.tableWidget.item(selectedRow,1).text(), "MM/dd/yyyy"))
        self.tmeStart.setTime(QtCore.QTime.fromString(self.tableWidget.item(selectedRow,2).text(), "hh:mm"))
        self.dedEnd.setDate(QtCore.QDate.fromString(self.tableWidget.item(selectedRow,3).text(), "MM/dd/yyyy"))
        self.tmeEnd.setTime(QtCore.QTime.fromString(self.tableWidget.item(selectedRow,4).text(), "hh:mm"))
        pass

    def btnAdd_Clicked(self):
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)

        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Checked)
        self.tableWidget.setItem(numRows, 0, chkBoxItem)

        txtItem1 = QTableWidgetItem(self.dedStart.date().toString("MM/dd/yyyy"))
        txtItem1.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(numRows, 1, txtItem1)

        txtItem2 = QTableWidgetItem(self.tmeStart.time().toString("hh:mm"))
        txtItem2.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(numRows, 2, txtItem2)

        txtItem3 = QTableWidgetItem(self.dedEnd.date().toString("MM/dd/yyyy"))
        txtItem3.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(numRows, 3, txtItem3)

        txtItem4 = QTableWidgetItem(self.tmeEnd.time().toString("hh:mm"))
        txtItem4.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(numRows, 4, txtItem4)

        self.tableWidget.setRowHeight(numRows, 20)

    def btnReplace_Clicked(self):
        selectedRow = self.tableWidget.currentRow()

        txtItem1 = QTableWidgetItem(self.dedStart.date().toString("MM/dd/yyyy"))
        txtItem1.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(selectedRow, 1, txtItem1)

        txtItem2 = QTableWidgetItem(self.tmeStart.time().toString("hh:mm"))
        txtItem2.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(selectedRow, 2, txtItem2)

        txtItem3 = QTableWidgetItem(self.dedEnd.date().toString("MM/dd/yyyy"))
        txtItem3.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(selectedRow, 3, txtItem3)

        txtItem4 = QTableWidgetItem(self.tmeEnd.time().toString("hh:mm"))
        txtItem4.setFlags(QtCore.Qt.ItemIsEnabled)
        self.tableWidget.setItem(selectedRow, 4, txtItem4)
        pass

    def btnDelete_Clicked(self):
        selectedRow = self.tableWidget.currentRow()
        self.tableWidget.removeRow(selectedRow)
        pass

    def btnDeleteAll_Clicked(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        pass

    def cmdOK_Clicked(self):
        section = self.project.events
        section.value = IndexedList([], ['name'])

        numRows = self.tableWidget.rowCount()

        for row in range(0,numRows):
            chkBoxItem = self.tableWidget.item(row,0)
            checked = chkBoxItem.checkState()
            if checked == 2:
                event = Events()
                event.start_date = self.tableWidget.item(row,1).text()
                event.start_time = self.tableWidget.item(row,2).text()
                event.end_date = self.tableWidget.item(row,3).text()
                event.end_time = self.tableWidget.item(row,4).text()
                event.name = event.start_date + event.start_time + event.end_date + event.end_time
                section.value.append(event)

        self._main_form.program_settings.setValue("Geometry/" + "frmEvents_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmEvents_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
