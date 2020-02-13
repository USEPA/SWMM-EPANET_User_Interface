import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QTableWidgetItem
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


class frmInfiltration(QMainWindow, Ui_frmInfiltrationEditor):
    def __init__(self, parent, edit_these, new_item, title, **kwargs):
        QMainWindow.__init__(self, parent)
        self.new_item = new_item
        self.helper = HelpHandler(self)
        option_section = parent.project.find_section('OPTIONS')
        self.project = parent.project
        if option_section.infiltration=="HORTON" or option_section.infiltration=="MODIFIED_HORTON":
            self.help_topic = "swmm/src/src/hortoninfiltrationparameters.htm"

        elif option_section.infiltration=="GREEN_AMPT" or option_section.infiltration=="MODIFIED_GREEN_AMPT":
            self.help_topic = "swmm/src/src/green_amptinfiltrationparame.htm"
        elif option_section.infiltration=="CURVE_NUMBER":
            self.help_topic = "swmm/src/src/curvenumberinfiltrationpara.htm"
        self.setupUi(self)
        self.setWindowTitle(title)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cboInfilModel.currentIndexChanged.connect(self.cboInfilModel_currentIndexChanged)

        self.defaults = None
        if "defaults" in kwargs:
            self.defaults = kwargs["defaults"]
        enum_val = E_InfilModel.HORTON
        if self.defaults is not None:
            enum_val = E_InfilModel[self.defaults.properties_sub_values[self.defaults.infil_model_key]]
            # self.infil_model = self.qsettings.value(self.default_key, None)
            # if self.infil_model is None:
            #     self.infil_model = HortonInfiltration()
            #     self.infil_model.set_defaults()
            # else:
            #     enum_val = self.infil_model.model_type()
            #     if enum_val == E_InfilModel.HORTON or \
            #        enum_val == E_InfilModel.MODIFIED_HORTON:
            #         self.infil_model_horton.__dict__.update(self.infil_model.__dict__)
            #     elif enum_val == E_InfilModel.GREEN_AMPT or \
            #          enum_val == E_InfilModel.MODIFIED_GREEN_AMPT:
            #         self.infil_model_ga.__dict__.update(self.infil_model.__dict__)
            #     elif enum_val == E_InfilModel.CURVE_NUMBER:
            #         self.infil_model_cn.__dict__.update(self.infil_model.__dict__)

            self.cboInfilModel.setEnabled(True)
            if self.lblNotes:
                self.tblGeneric.currentCellChanged.connect(self.table_currentCellChanged)
            self.tblGeneric.itemChanged.connect(self.table_itemChanged)
            pass
        else:
            self.backend = PropertyEditorBackend(self.tblGeneric, self.lblNotes, parent, edit_these, new_item)
            #self.lblTop.setText("Infiltration Method:  " + parent.project.find_section('OPTIONS').infiltration)
            proj_infilmodel = parent.project.find_section('OPTIONS').infiltration
            enum_val = E_InfilModel[proj_infilmodel.upper()]
            self.cboInfilModel.setEnabled(False)

        set_combo_items(type(enum_val), self.cboInfilModel)
        set_combo(self.cboInfilModel, enum_val)

        self.tblGeneric.setHorizontalHeaderLabels(['Value'])
        self.tblGeneric.horizontalHeader().setFixedHeight(30)
        self.corner_label = QLabel("Property", self.tblGeneric)
        self.corner_label.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.tblGeneric.verticalHeader().geometriesChanged.connect(self.resizeCorner)
        self.tblGeneric.horizontalHeader().geometriesChanged.connect(self.resizeCorner)

    def cboInfilModel_currentIndexChanged(self, currentIndex):
        #if self.infil_model is None: return
        if not self.defaults: return
        self.tblGeneric.clearContents()
        enum_val = E_InfilModel[self.cboInfilModel.currentText().upper()]
        if enum_val == E_InfilModel.HORTON or \
           enum_val == E_InfilModel.MODIFIED_HORTON:
            self.meta = self.defaults.infil_model_horton.metadata
            self.set_horton()
        elif enum_val == E_InfilModel.GREEN_AMPT or \
             enum_val == E_InfilModel.MODIFIED_GREEN_AMPT:
            self.meta = self.defaults.infil_model_ga.metadata
            self.set_greenampt()
        elif enum_val == E_InfilModel.CURVE_NUMBER:
            self.meta = self.defaults.infil_model_cn.metadata
            self.set_CN()

    def set_horton(self):
        self.lblNotes.setText("Maximum rate on the Horton infiltration curve (in/hr or mm/hr)")
        #mtype = self.defaults.infil_model_horton.model_type()
        mtype = E_InfilModel[self.cboInfilModel.currentText().upper()]
        props = []
        for i in range(0, len(HortonInfiltration.metadata)):
            if "subcatch" in HortonInfiltration.metadata[i].label.lower():
                continue
            else:
                props.append(HortonInfiltration.metadata[i].label)
        self.tblGeneric.setRowCount(len(props))
        self.tblGeneric.setVerticalHeaderLabels(props)
        for i in range(0, self.tblGeneric.rowCount()):
            vtitle = self.tblGeneric.verticalHeaderItem(i).text().lower()
            if "max" in vtitle and "infil" in vtitle:
                val = self.defaults.infil_model_horton.default_max_rate()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.defaults.infil_model_horton.max_rate
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
            elif "min" in vtitle and "infil" in vtitle:
                val = self.defaults.infil_model_horton.default_min_rate()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.defaults.infil_model_horton.min_rate
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
            elif "decay" in vtitle:
                val = self.defaults.infil_model_horton.default_decay()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.defaults.infil_model_horton.decay
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
            elif "dry" in vtitle:
                val = self.defaults.infil_model_horton.default_dry_time()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.defaults.infil_model_horton.dry_time
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
            elif "max" in vtitle and "volume" in vtitle:
                val = self.defaults.infil_model_horton.default_max_volume()
                if mtype == E_InfilModel.MODIFIED_HORTON:
                    val = self.defaults.infil_model_horton.max_volume
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))

    def set_greenampt(self):
        self.lblNotes.setText("Soil capillary suction head (inches or mm)")
        #mtype = self.defaults.infil_model_ga.model_type()
        mtype = E_InfilModel[self.cboInfilModel.currentText().upper()]
        props = []
        for i in range(0, len(GreenAmptInfiltration.metadata)):
            if "subcatch" in GreenAmptInfiltration.metadata[i].label.lower():
                continue
            else:
                props.append(GreenAmptInfiltration.metadata[i].label)
        self.tblGeneric.setRowCount(len(props))
        self.tblGeneric.setVerticalHeaderLabels(props)
        #self.infil_model = GreenAmptInfiltration()
        for i in range(0, self.tblGeneric.rowCount()):
            vtitle = self.tblGeneric.verticalHeaderItem(i).text().lower()
            if "suction" in vtitle:
                val = self.defaults.infil_model_ga.default_suction()
                if mtype == E_InfilModel.MODIFIED_GREEN_AMPT:
                    val = self.defaults.infil_model_ga.suction
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
            elif "conduct" in vtitle:
                val = self.defaults.infil_model_ga.default_conductivity()
                if mtype == E_InfilModel.MODIFIED_GREEN_AMPT:
                    val = self.defaults.infil_model_ga.hydraulic_conductivity
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
            elif "deficit" in vtitle:
                val = self.defaults.infil_model_ga.default_init_deficit()
                if mtype == E_InfilModel.MODIFIED_GREEN_AMPT:
                    val = self.defaults.infil_model_ga.initial_moisture_deficit
                self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))

    def set_CN(self):
        self.lblNotes.setText("SCS runoff curve number")
        props = []
        for i in range(0, len(CurveNumberInfiltration.metadata)):
            if "subcatch" in CurveNumberInfiltration.metadata[i].label.lower():
                continue
            elif "conduct" in CurveNumberInfiltration.metadata[i].label.lower():
                continue
            else:
                props.append(CurveNumberInfiltration.metadata[i].label)
        self.tblGeneric.setRowCount(len(props))
        self.tblGeneric.setVerticalHeaderLabels(props)
        #self.infil_model = CurveNumberInfiltration()
        for i in range(0, self.tblGeneric.rowCount()):
            vtitle = self.tblGeneric.verticalHeaderItem(i).text().lower()
            if "curve" in vtitle:
                val, val_is_good = ParseData.floatTryParse(self.defaults.infil_model_cn.curve_number)
                if val_is_good:
                    self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
                else:
                    self.tblGeneric.setItem(i,0, QTableWidgetItem(self.defaults.infil_model_cn.default_CN()))
            elif "dry" in vtitle:
                val, val_is_good = ParseData.floatTryParse(self.defaults.infil_model_cn.dry_days)
                if val_is_good:
                    self.tblGeneric.setItem(i,0, QTableWidgetItem(str(val)))
                else:
                    self.tblGeneric.setItem(i,0, QTableWidgetItem(self.defaults.infil_model_cn.default_dry_time()))

    def resizeCorner(self):
        self.corner_label.setGeometry(0, 0, self.tblGeneric.verticalHeader().width(),
                                           self.tblGeneric.horizontalHeader().height())

    def table_currentCellChanged(self):
        row = self.tblGeneric.currentRow()
        if self.lblNotes:
            if hasattr(self, "meta") and self.meta and self.meta[row]:
                self.lblNotes.setText(self.meta[row + 1].hint)
            else:
                self.lblNotes.setText('')

    def table_itemChanged(self, item):
        if self.tblGeneric.currentItem() is None: return
        new_val, new_val_is_good = ParseData.floatTryParse(self.tblGeneric.currentItem().text())
        if not new_val_is_good: return
        vtitle = self.tblGeneric.verticalHeaderItem(self.tblGeneric.currentRow()).text()

        attr_name = ""
        for i in range(0, len(self.meta)):
            if self.meta[i].label == vtitle:
                attr_name = self.meta[i].attribute
                break

        if len(attr_name) == 0: return

        enum_val = E_InfilModel[self.cboInfilModel.currentText().upper()]
        if enum_val == E_InfilModel.MODIFIED_HORTON:
            self.defaults.infil_model_horton.__dict__[attr_name] = new_val
        elif enum_val == E_InfilModel.MODIFIED_GREEN_AMPT:
            self.defaults.infil_model_ga.__dict__[attr_name] = new_val
        elif enum_val == E_InfilModel.CURVE_NUMBER:
            self.defaults.infil_model_cn.__dict__[attr_name] = new_val
        pass

    def cmdOK_Clicked(self):
        if hasattr(self, "backend") and self.backend is not None:
            if self.new_item:
                self.project.infiltration.value.append(self.new_item)
            self.backend.new_item = None
            self.backend.apply_edits()
        else:
            if self.defaults is not None:
                # self.qsettings.remove(self.default_key)
                enum_val = E_InfilModel[self.cboInfilModel.currentText().upper()]
                self.defaults.properties_sub_values[self.defaults.infil_model_key] = enum_val.name
                if enum_val == E_InfilModel.HORTON:
                    #self.qsettings.setValue(self.default_key, self.infil_model_horton)
                    self.defaults.infil_model_horton.set_defaults()
                elif enum_val == E_InfilModel.GREEN_AMPT:
                    #self.qsettings.setValue(self.default_key, self.infil_model_ga)
                    self.defaults.infil_model_ga.set_defaults()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

