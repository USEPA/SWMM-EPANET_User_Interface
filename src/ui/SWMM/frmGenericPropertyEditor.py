from enum import Enum
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import ui.convenience
from core.swmm.patterns import PatternType
from ui.SWMM.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor


class cBox(QtGui.QComboBox):
    def __init__(self, *args, **kwargs):
        super(cBox, self).__init__(*args, **kwargs)


class frmGenericPropertyEditor(QtGui.QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, parent, edit_these):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.tblGeneric.currentCellChanged.connect(self.tblGeneric_currentCellChanged)
        if edit_these:
            self.meta = edit_these[0].metadata
        self.set_from(parent.project, edit_these)
        self._parent = parent

    def set_from(self, project, edit_these):
        if edit_these:
            self.meta = edit_these[0].metadata
            self.tblGeneric.horizontalHeader().hide()
            self.tblGeneric.setColumnCount(len(edit_these))
            self.tblGeneric.setRowCount(len(self.meta))
            self.tblGeneric.setVerticalHeaderLabels(self.meta.labels())
            column = 0
            for edit_this in edit_these:
                row = 0
                for meta_item in self.meta:
                    value = self.meta.value(meta_item, edit_this)
                    if isinstance(value, Enum):
                        combobox = QtGui.QComboBox()
                        ui.convenience.set_combo_items(type(value), combobox)
                        ui.convenience.set_combo(combobox, value)
                        self.tblGeneric.setCellWidget(row, column, combobox)
                    else:
                        print "row " + str(row) + " col " + str(column) + " = " + str(value)
                        self.tblGeneric.setItem(row, column, QtGui.QTableWidgetItem(value))
                    row += 1
                column += 1
        else:
            self.tblGeneric.setColumnCount(1)
            self.tblGeneric.setRowCount(1)
            self.tblGeneric.setVerticalHeaderLabels(("Error"))
            led = QtGui.QLineEdit("No items selected to edit")
            self.tblGeneric.setItem(-1,1,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def tblGeneric_currentCellChanged(self):
        row = self.tblGeneric.currentRow()
        col = self.tblGeneric.currentColumn()
        self.lblNotes.setText(self.meta[row].hint)
