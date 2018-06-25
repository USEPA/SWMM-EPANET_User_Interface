import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from ui.property_editor_backend import PropertyEditorBackend


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

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

