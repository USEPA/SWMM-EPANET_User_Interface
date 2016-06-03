import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from ui.SWMM.frmInfiltrationDesigner import Ui_frmInfiltrationEditor
from ui.property_editor_backend import PropertyEditorBackend


class frmInfiltration(QtGui.QMainWindow, Ui_frmInfiltrationEditor):
    def __init__(self, parent, edit_these, title):
        QtGui.QMainWindow.__init__(self, parent)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        self.setWindowTitle(title)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, parent, edit_these)
        self.lblTop.setText("Infiltration Method:  " + parent.project.find_section('OPTIONS').infiltration)
        # self.tblGeneric.horizontalHeader().show()
        # self.tblGeneric.setHorizontalHeaderLabels(('1','2','3','4','5','6','7','8'))

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

