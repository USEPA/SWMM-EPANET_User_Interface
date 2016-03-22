import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from enum import Enum

import ui.convenience
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor


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
        self.edit_these = edit_these
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
                    if isinstance(value, bool):
                        checkbox = QtGui.QCheckBox()
                        checkbox.setChecked(value)
                        self.tblGeneric.setCellWidget(row, column, checkbox)
                    if isinstance(value, Enum):
                        combobox = QtGui.QComboBox()
                        ui.convenience.set_combo_items(type(value), combobox)
                        ui.convenience.set_combo(combobox, value)
                        self.tblGeneric.setCellWidget(row, column, combobox)
                    else:
                        # print "row " + str(row) + " col " + str(column) + " = " + str(value)
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
        # column = 1
        # for edit_this in self.edit_these:
        #     row = 0
        #     label_item = self.tblGeneric.verticalHeaderItem(row)
        #     if label_item:
        #         label = label_item.text()
        #         if label:
        #             for meta_item in self.meta:
        #                 if meta_item.label == label:
        #                     old_value = self.meta.value(meta_item, edit_this)
        #                     new_value = None
        #                     if isinstance(old_value, bool):
        #                         checkbox = self.tblGeneric.item(row, column)
        #                         if isinstance(checkbox, QtGui.QCheckBox):
        #                             new_value = checkbox.isChecked()
        #                     if isinstance(old_value, Enum):
        #                         combobox = self.tblGeneric.item(row, column)
        #                         if isinstance(checkbox, QtGui.QComboBox):
        #                             try:
        #                                 new_value = type(old_value)[combobox.currentText()]
        #                             except Exception as ex:
        #                                 print "Could not interpret " + str(combobox.currentText()) + " as Enum " + str(type(old_value))
        #                     else:
        #                         widget = self.tblGeneric.item(row, column)
        #                         if widget:
        #                             new_value = widget.text()
        #                     if new_value is not None:
        #                         try:
        #                             setattr(edit_this, meta_item.attribute, new_value)
        #                         except Exception as ex:
        #                             print "Could not set " + str(meta_item.attribute) + " to " + str(widget.text())
        #                     row += 1
        #     column += 1
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def tblGeneric_currentCellChanged(self):
        row = self.tblGeneric.currentRow()
        col = self.tblGeneric.currentColumn()
        self.lblNotes.setText(self.meta[row].hint)
