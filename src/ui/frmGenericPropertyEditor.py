import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from property_editor_backend import PropertyEditorBackend


class frmGenericPropertyEditor(QtGui.QMainWindow, Ui_frmGenericPropertyEditor):
    def __init__(self, parent, edit_these, title):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, parent, edit_these)

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

