import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QCheckBox, QComboBox, QTableWidgetItem, QLineEdit, QFontComboBox, QSizePolicy
from enum import Enum
import ui.convenience


class PropertyEditorBackend:
    def __init__(self, table, hint_label, main_form, edit_these, new_item):
        self.table = table
        self.hint_label = hint_label
        self._main_form = main_form
        self.loaded = False
        self.col_to_item_dict = {}
        if self.hint_label:
            table.currentCellChanged.connect(self.table_currentCellChanged)
        self.set_from(edit_these, new_item)

    def set_from(self, edit_these, new_item):
        self.edit_these = edit_these
        self.new_item = new_item
        if edit_these:
            self.meta = edit_these[0].metadata
            # self.table.horizontalHeader().hide()
            self.table.setColumnCount(len(edit_these))
            listofblanks = [''] * len(edit_these)
            self.table.setHorizontalHeaderLabels(listofblanks)
            self.table.horizontalHeader().setFixedHeight(5)
            self.table.setRowCount(len(self.meta))
            self.table.setVerticalHeaderLabels(self.meta.labels())
            column = 0
            for edit_this in edit_these:
                row = 0
                for meta_item in self.meta:
                    value = self.meta.value(meta_item, edit_this)
                    if isinstance(value, bool):
                        checkbox = QCheckBox()
                        checkbox.setChecked(value)
                        self.table.setCellWidget(row, column, checkbox)
                    if isinstance(value, Enum):
                        combobox = QComboBox()
                        ui.convenience.set_combo_items(type(value), combobox)
                        ui.convenience.set_combo(combobox, value)
                        self.table.setCellWidget(row, column, combobox)
                    elif meta_item.attribute == 'font':
                        combobox = QFontComboBox()
                        combobox.setCurrentText(value)
                        size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
                        size_policy.setHorizontalStretch(0)
                        size_policy.setVerticalStretch(0)
                        combobox.setSizePolicy(size_policy)
                        combobox.setMinimumSize(QtCore.QSize(50, 22))
                        combobox.setMaximumSize(QtCore.QSize(16777215, 1010))
                        self.table.setCellWidget(row, column, combobox)
                    else:
                        # print "row " + str(row) + " col " + str(column) + " = " + str(value)
                        self.table.setItem(row, column, QTableWidgetItem(value))
                    row += 1
                self.col_to_item_dict[column] = edit_this
                column += 1
        else:
            self.table.setColumnCount(1)
            self.table.setRowCount(1)
            self.table.setVerticalHeaderLabels(["Error"])
            led = QLineEdit("No items selected to edit")
            self.table.setItem(-1, 1, QTableWidgetItem(led.text()))
        self.loaded = True

    def apply_edits(self):
        column = 0
        edited_names = []
        for edit_this in self.edit_these:
            for row in range(self.table.rowCount()):
                label_item = self.table.verticalHeaderItem(row)
                if label_item:
                    label = label_item.text()
                    if label:
                        for meta_item in self.meta:
                            if meta_item.label == label:
                                if not meta_item.attribute:
                                    print ("No attribute to set for " + label)
                                    break
                                new_value = None
                                widget = self.table.cellWidget(row, column)
                                if widget:
                                    if isinstance(widget, QCheckBox):
                                        new_value = widget.isChecked()
                                    elif isinstance(widget, QComboBox):
                                        default_value = self.meta.value(meta_item, edit_this)
                                        if isinstance(default_value, Enum):
                                            try:
                                                new_value = type(default_value)[widget.currentText()]
                                            except Exception as ex:
                                                print("Could not interpret " + str(widget.currentText()) +
                                                      " as Enum " + str(type(default_value)))
                                        else:
                                            new_value = widget.currentText()
                                else:
                                    widget = self.table.item(row, column)
                                    if widget:
                                        new_value = widget.text()
                                if new_value is not None and new_value != 'None':
                                    try:
                                        old_value = str(getattr(edit_this, meta_item.attribute))
                                        if new_value != old_value:
                                            # TODO: make undoable edit?
                                            setattr(edit_this, meta_item.attribute, new_value)
                                            self._main_form.mark_project_as_unsaved()
                                            if meta_item.attribute == "name":
                                                edited_names.append((old_value, edit_this))
                                    except Exception as ex:
                                        print("Could not set " + str(meta_item.label) + " to " + str(new_value))
            column += 1
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
        elif edited_names:
            self._main_form.edited_name(edited_names)
        else:
            pass
            # TODO: self._main_form.edited_?

    def table_currentCellChanged(self):
        row = self.table.currentRow()
        # col = self.table.currentColumn()
        if self.hint_label:
            if hasattr(self, "meta") and self.meta and self.meta[row]:
                units = ''
                if self._main_form.project.metric:
                    units = self.meta[row].units_metric
                else:
                    units = self.meta[row].units_english
                self.hint_label.setText(self.meta[row].hint + ' ' + units)
            else:
                self.hint_label.setText('')
