import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend
from PyQt5.Qt import QApplication, QClipboard
from PyQt5.QtCore import *


class frmGenericPropertyEditor(QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, session, project_section, edit_these, new_item, title):
        QMainWindow.__init__(self, session)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)

        self.session = session
        self.project = session.project
        self.project_section = project_section
        if new_item:
            edit_these = [new_item]
        elif self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                (not hasattr(self, "SECTION_TYPE") or isinstance(self.project_section.value[0], self.SECTION_TYPE)):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], str):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)
        self.edit_these = edit_these
        self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, session, edit_these, new_item)
        self.tblGeneric.cellChanged.connect(self.check_change)
        for row in range(self.tblGeneric.rowCount()):
            self.tblGeneric.setRowHeight(row, 20)

    def header_index(self, prop):
        """
        Look up the row header to match up with prop
        Args:
            prop: header text
        Returns:
            row number of matching header text
        """
        header = ""
        for row in range(self.tblGeneric.rowCount()):
            header = self.tblGeneric.verticalHeaderItem(row).text()
            if header and prop.upper() in header.upper():
                return row
        return -999

    def is_name_duplicate(self, irow, icol):
        new_name = self.tblGeneric.item(irow, icol).text()
        if self.project_section.find_item(new_name):
            return True
        else:
            return False
        pass

    def check_change(self, irow, icol):
        ori_value = getattr(self.backend.col_to_item_dict[icol], self.backend.meta[irow].attribute, '')
        new_value = self.tblGeneric.item(irow, icol).text()
        if not self.backend.loaded:
            return
        if irow == 0:
            if self.is_name_duplicate(irow, icol):
                QMessageBox.information(None, self.session.model,
                                        type(self.project_section.value[0]).__name__ + " '" + new_value + "' already exists.",
                                        QMessageBox.Ok)
                self.tblGeneric.cellChanged.disconnect(self.check_change)
                self.tblGeneric.item(irow, icol).setText(ori_value)
                self.tblGeneric.cellChanged.connect(self.check_change)
        pass

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        # self.session.model_layers.create_layers_from_project(self.project)
        self.close()

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

    def paste(self):
        str = QApplication.clipboard().text()
        selected_range = self.tblGeneric.selectedRanges()[0]
        rows = str.split('\n')
        numRows = len(rows) - 1
        numColumns = rows[0].count('\t') + 1
        for i in range(numRows):
            columns = rows[i].split('\t')
            for j in range(numColumns):
                if selected_range.topRow() + i < self.tblGeneric.rowCount() and selected_range.leftColumn() + j < self.tblGeneric.columnCount():
                    self.tblGeneric.item(selected_range.topRow() + i, selected_range.leftColumn() + j).setText(columns[j])
        if selected_range.rowCount() > numRows or selected_range.columnCount() > numColumns:
            # not enough data to fill selected area, don't continue unless theres a single cell on the clipboard
            if numRows == 1 and numColumns == 1:
                # fill selected range with single value
                value = rows[0]
                for i in range(selected_range.rowCount()):
                    for j in range(selected_range.columnCount()):
                        self.tblGeneric.item(selected_range.topRow() + i, selected_range.leftColumn() + j).setText(value)
        pass

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy):
            self.copy()
        if event.matches(QtGui.QKeySequence.Paste):
            self.paste()
