import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.help import HelpHandler
from ui.frmGenericPropertyEditorDesigner import Ui_frmGenericPropertyEditor
from ui.SWMM.frmInfiltrationDesigner import Ui_frmInfiltrationEditor
from ui.property_editor_backend import PropertyEditorBackend
from ui.convenience import set_combo_items
from ui.convenience import set_combo
from core.swmm.hydrology.subcatchment import E_InfilModel
from core.swmm.hydrology.subcatchment import HortonInfiltration
from core.swmm.hydrology.subcatchment import GreenAmptInfiltration
from core.swmm.hydrology.subcatchment import CurveNumberInfiltration


class frmInfiltration(QtGui.QMainWindow, Ui_frmInfiltrationEditor):
    def __init__(self, parent, edit_these, new_item, title, **kwargs):
        QtGui.QMainWindow.__init__(self, parent)
        self.helper = HelpHandler(self)
        option_section = parent.project.find_section('OPTIONS')
        if option_section.infiltration=="HORTON" or option_section.infiltration=="MODIFIED_HORTON":
            self.help_topic = "swmm/src/src/hortoninfiltrationparameters.htm"
        elif option_section.infiltration=="GREEN_AMPT" or option_section.infiltration=="MODIFIED_GREEN_AMPT":
            self.help_topic = "swmm/src/src/green_amptinfiltrationparame.htm"
        elif option_section.infiltration=="CURVE_NUMBER":
            self.help_topic = "swmm/src/src/curvenumberinfiltrationpara.htm"
        self.setupUi(self)
        self.setWindowTitle(title)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        self.qsettings = None
        if kwargs.has_key("qsettings"):
            self.qsettings = kwargs["qsettings"]
        self.default_key = "def_infilmodel"
        if kwargs.has_key("default_key"):
            self.default_key = kwargs["default_key"]

        enum_val = E_InfilModel.HORTON
        if self.qsettings is not None:
            QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
            self.cboInfilModel.setEnabled(True)
            pass
        else:
            self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, parent, edit_these, new_item)
            #self.lblTop.setText("Infiltration Method:  " + parent.project.find_section('OPTIONS').infiltration)
            proj_infilmodel = parent.project.find_section('OPTIONS').infiltration
            enum_val = E_InfilModel[proj_infilmodel.upper()]
            self.cboInfilModel.setEnabled(False)

        set_combo_items(type(enum_val), self.cboInfilModel)
        set_combo(self.cboInfilModel, enum_val)
        # self.tblGeneric.horizontalHeader().show()
        # self.tblGeneric.setHorizontalHeaderLabels(('1','2','3','4','5','6','7','8'))

    def cmdOK_Clicked(self):
        self.backend.apply_edits()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

