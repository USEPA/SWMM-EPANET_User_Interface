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
from ui.model_utility import ParseData


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
        QtCore.QObject.connect(self.cboInfilModel, QtCore.SIGNAL("currentIndexChanged()"),
                               self.cboInfilModel_currentIndexChanged)

        self.qsettings = None
        if kwargs.has_key("qsettings"):
            self.qsettings = kwargs["qsettings"]
        self.default_key = "obj_def_infilmodel"
        if kwargs.has_key("default_key"):
            self.default_key = kwargs["default_key"]
        self.infil_model = None

        enum_val = E_InfilModel.HORTON
        if self.qsettings is not None:
            self.infil_model = self.qsettings.value(self.default_key, None)
            if self.infil_model is None:
                self.infil_model = HortonInfiltration()
                self.infil_model.set_defaults()
            else:
                enum_val = self.infil_model.model_type()
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

    def cboInfilModel_currentIndexChanged(self):
        if self.infil_model is None: return
        self.tblGeneric.clearContents()
        enum_val = E_InfilModel[self.cboInfilModel.currentText().upper()]
        if enum_val == E_InfilModel.HORTON or \
           enum_val == E_InfilModel.MODIFIED_HORTON:
            self.set_horton()
        elif enum_val == E_InfilModel.GREEN_AMPT or \
             enum_val == E_InfilModel.MODIFIED_GREEN_AMPT:
            self.set_greenampt()
        elif enum_val == E_InfilModel.CURVE_NUMBER:
            self.set_CN()

    def set_horton(self):
        mtype = self.infil_model.model_type()
        props = []
        for i in range(0, len(HortonInfiltration.metadata)):
            if "subcatch" in HortonInfiltration.metadata[i][2].lower():
                continue
            else:
                props.append(HortonInfiltration.metadata[i][2])
        self.tblGeneric.setRowCount(len(props))
        self.tblGeneric.setVerticalHeaderLabels(props)
        for i in range(0, self.tblGeneric.rowCount()):
            vtitle = str(self.tblGeneric.verticalHeaderItem(i)).lower()
            if "max" in vtitle and "infil" in vtitle:
                val = self.infil_model.default_max_rate()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.infil_model.max_rate
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
            elif "min" in vtitle and "infil" in vtitle:
                val = self.infil_model.default_min_rate()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.infil_model.min_rate
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
            elif "decay" in vtitle:
                val = self.infil_model.default_decay()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.infil_model.decay
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
            elif "dry" in vtitle:
                val = self.infil_model.default_dry_time()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.infil_model.dry_time
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
            elif "max" in vtitle and "volume" in vtitle:
                val = self.infil_model.default_max_volume()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.infil_model.max_volume
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))

    def set_greenampt(self):
        mtype = self.infil_model.model_type()
        props = []
        for i in range(0, len(GreenAmptInfiltration.metadata)):
            if "subcatch" in GreenAmptInfiltration.metadata[i][2].lower():
                continue
            else:
                props.append(GreenAmptInfiltration.metadata[i][2])
        self.tblGeneric.setRowCount(len(props))
        self.tblGeneric.setVerticalHeaderLabels(props)
        #self.infil_model = GreenAmptInfiltration()
        for i in range(0, self.tblGeneric.rowCount()):
            vtitle = str(self.tblGeneric.verticalHeaderItem(i)).lower()
            if "suction" in vtitle:
                val = self.infil_model.default_suction()
                if mtype == E_InfilModel.MODIFIED_GREENAMPT:
                    val = self.infil_model.suction
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
            elif "conduct" in vtitle:
                val = self.infil_model.default_conductivity()
                if mtype == E_InfilModel.MODIFIED_GREENAMPT:
                    val = self.infil_model.hydraulic_conductivity
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
            elif "deficit" in vtitle:
                val = self.infil_model.default_init_deficit()
                if mtype == E_InfilModel.MODIFIED_GREENAMPT:
                    val = self.infil_model.initial_moisture_deficit
                self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))

    def set_CN(self):
        props = []
        for i in range(0, len(GreenAmptInfiltration.metadata)):
            if "subcatch" in GreenAmptInfiltration.metadata[i][2].lower():
                continue
            else:
                props.append(GreenAmptInfiltration.metadata[i][2])
        self.tblGeneric.setRowCount(len(props))
        self.tblGeneric.setVerticalHeaderLabels(props)
        #self.infil_model = CurveNumberInfiltration()
        for i in range(0, self.tblGeneric.rowCount()):
            vtitle = str(self.tblGeneric.verticalHeaderItem(i)).lower()
            if "curve" in vtitle:
                val, val_is_good = ParseData.floatTryParse(self.infil_model.curve_number())
                if val_is_good:
                    self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
                else:
                    self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(self.infil_model.default_CN())))
            elif "dry" in vtitle:
                val, val_is_good = ParseData.floatTryParse(self.infil_model.dry_days())
                if val_is_good:
                    self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(val)))
                else:
                    self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(unicode(self.infil_model.default_dry_time())))

    def cmdOK_Clicked(self):
        if self.backend is not None:
            self.backend.apply_edits()
        else:
            infil_model = None
            if self.qsettings is not None:
                self.qsettings.setValue(self.default_key, infil_model)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

