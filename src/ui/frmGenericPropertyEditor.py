import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from property_editor_backend import PropertyEditorBackend


class frmGenericPropertyEditor(QtGui.QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, session, project_section, edit_these, new_item, title):
        QtGui.QMainWindow.__init__(self, session)
        self.setupUi(self)
        self.setWindowTitle(title)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        self.session = session
        self.project = session.project
        self.project_section = project_section
        if new_item:
            edit_these = [new_item]
        elif self.project_section and \
                isinstance(self.project_section.value, list) and \
                len(self.project_section.value) > 0 and \
                isinstance(self.project_section.value[0], self.SECTION_TYPE):

            if edit_these:  # Edit only specified item(s) in section
                if isinstance(edit_these[0], basestring):  # Translate list from names to objects
                    edit_names = edit_these
                    edit_objects = [item for item in self.project_section.value if item.name in edit_these]
                    edit_these = edit_objects

            else:  # Edit all items in section
                edit_these = []
                edit_these.extend(self.project_section.value)
        self.edit_these = edit_these
        self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, session, edit_these, new_item)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

