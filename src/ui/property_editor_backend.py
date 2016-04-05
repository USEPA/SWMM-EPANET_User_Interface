import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from enum import Enum
import ui.convenience


class PropertyEditorBackend:
    def __init__(self, table, hint_label, parent, edit_these):
        self.table = table
        self.hint_label = hint_label
        self.parent = parent
        if self.hint_label:
            table.currentCellChanged.connect(self.table_currentCellChanged)
        if edit_these:
            self.edit_these = edit_these
            self.meta = edit_these[0].metadata
        self.set_from(parent.project, edit_these)

    def set_from(self, project, edit_these):
        self.edit_these = edit_these
        if edit_these:
            self.meta = edit_these[0].metadata
            self.table.horizontalHeader().hide()
            self.table.setColumnCount(len(edit_these))
            self.table.setRowCount(len(self.meta))
            self.table.setVerticalHeaderLabels(self.meta.labels())
            column = 0
            for edit_this in edit_these:
                row = 0
                for meta_item in self.meta:
                    value = self.meta.value(meta_item, edit_this)
                    if isinstance(value, bool):
                        checkbox = QtGui.QCheckBox()
                        checkbox.setChecked(value)
                        self.table.setCellWidget(row, column, checkbox)
                    if isinstance(value, Enum):
                        combobox = QtGui.QComboBox()
                        ui.convenience.set_combo_items(type(value), combobox)
                        ui.convenience.set_combo(combobox, value)
                        self.table.setCellWidget(row, column, combobox)
                    else:
                        # print "row " + str(row) + " col " + str(column) + " = " + str(value)
                        self.table.setItem(row, column, QtGui.QTableWidgetItem(value))
                    row += 1
                column += 1
        else:
            self.table.setColumnCount(1)
            self.table.setRowCount(1)
            self.table.setVerticalHeaderLabels(["Error"])
            led = QtGui.QLineEdit("No items selected to edit")
            self.table.setItem(-1, 1, QtGui.QTableWidgetItem(led.text()))

    def apply_edits(self):
        column = 1
        for edit_this in self.edit_these:
            row = 0
            label_item = self.table.verticalHeaderItem(row)
            if label_item:
                label = label_item.text()
                # if label:
                #     for meta_item in self.meta:
                #         if meta_item.label == label:
                #             old_value = self.meta.value(meta_item, edit_this)
                #             new_value = None
                #             if isinstance(old_value, bool):
                #                 checkbox = self.table.item(row, column)
                #                 if isinstance(checkbox, QtGui.QCheckBox):
                #                     new_value = checkbox.isChecked()
                #             if isinstance(old_value, Enum):
                #                 combobox = self.table.item(row, column)
                #                 if isinstance(checkbox, QtGui.QComboBox):
                #                     try:
                #                         new_value = type(old_value)[combobox.currentText()]
                #                     except Exception as ex:
                #                         print "Could not interpret " + str(combobox.currentText()) + " as Enum " + str(type(old_value))
                #             else:
                #                 widget = self.table.item(row, column)
                #                 if widget:
                #                     new_value = widget.text()
                #             if new_value is not None:
                #                 try:
                #                     setattr(edit_this, meta_item.attribute, new_value)
                #                 except Exception as ex:
                #                     print "Could not set " + str(meta_item.attribute) + " to " + str(widget.text())
                #             row += 1
            column += 1

    def table_currentCellChanged(self):
        row = self.table.currentRow()
        # col = self.table.currentColumn()
        if self.hint_label:
            self.hint_label.setText(self.meta[row].hint)