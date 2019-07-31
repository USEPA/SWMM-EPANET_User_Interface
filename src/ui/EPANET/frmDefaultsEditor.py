import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QTableWidget, QWidget, QTableWidgetItem, QComboBox
from ui.help import HelpHandler
from ui.frmGenericDefaultsEditorDesigner import Ui_frmGenericDefaultsEditor
from ui.inifile import ini_setting
from ui.convenience import set_combo_items
from ui.convenience import set_combo
from core.epanet.options.hydraulics import FlowUnits
from core.epanet.options.hydraulics import HeadLoss
from core.epanet.options.hydraulics import Unbalanced
from core.epanet.options.report import StatusWrite
from ui.model_utility import ParseData
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class frmDefaultsEditor(QMainWindow, Ui_frmGenericDefaultsEditor):
    """
    Project defaults editor for setting and editing
    object id prefix (tab1)
    properties (tab2)
    hydraulic defaults (tab3)
    """
    def __init__(self, session, project, defaults):
        QMainWindow.__init__(self, session)
        self.helper = HelpHandler(self)
        self.help_topic = "epanet/src/src/Sett0005.htm"
        self.setupUi(self)
        self.defaults = defaults
        self.session = session
        self.project = project
        self.label_changed = False
        self.property_changed = False
        self.parameter_changed = False
        self.loaded = False
        if self.session is not None:
            self.setWindowTitle(self.session.model + " Project Defaults")
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        # self.tabDefaults.currentChanged(int).connect(self.tab_changed)
        # self.tblGeneric.cellChanged(int, int).connect(self.tblGeneric_changed)
        self.tabDefaults.currentChanged.connect(self.tab_changed)
        self.tblGeneric.cellChanged.connect(self.tblGeneric_changed)
        self.tblGeneric.verticalHeader().geometriesChanged.connect(self.resizeCorner)
        self.tblGeneric.horizontalHeader().geometriesChanged.connect(self.resizeCorner)

        self.corner_label_tab1 = QLabel("Object", self.tblGeneric)
        self.corner_label_tab1.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab1.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.gridLayout_tab2 = QGridLayout(self.tabDefaults.widget(1))
        self.gridLayout_tab2.setObjectName(_fromUtf8("gridLayout_tab2"))
        self.tbl_2 = QTableWidget(self.tabDefaults.widget(1))
        self.tbl_2.setObjectName(_fromUtf8("tbl_2"))
        self.tbl_2.setColumnCount(1)
        self.tbl_2.setRowCount(1)
        self.tbl_2.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_tab2.addWidget(self.tbl_2, 0, 0, 0, 0)
        self.tbl_2.cellChanged.connect(self.tbl_2_changed)

        self.corner_label_tab2 = QLabel("Property", self.tbl_2)
        self.corner_label_tab2.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab2.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.gridLayout_tab3 = QGridLayout(self.tabDefaults.widget(2))
        self.gridLayout_tab3.setObjectName(_fromUtf8("gridLayout_tab3"))
        self.tbl_3 = QTableWidget(self.tabDefaults.widget(2))
        self.tbl_3.setObjectName(_fromUtf8("tbl_3"))
        self.tbl_3.setColumnCount(1)
        self.tbl_3.setRowCount(1)
        self.tbl_3.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_tab3.addWidget(self.tbl_3, 0, 0, 0, 0)
        self.tbl_3.cellChanged.connect(self.tbl_3_changed)

        self.corner_label_tab3 = QLabel("Option", self.tbl_3)
        self.corner_label_tab3.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab3.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.tbl_3.verticalHeader().geometriesChanged.connect(self.resizeCorner)
        self.tbl_3.horizontalHeader().geometriesChanged.connect(self.resizeCorner)

        self.sm_property = QtCore.QSignalMapper(self)
        # self.sm_property.mapped(int).connect(self.tbl_2_combo_indexChanged)
        self.sm_property.mapped.connect(self.tbl_2_combo_indexChanged)
        self.sm_hydraulics = QtCore.QSignalMapper(self)
        # self.sm_hydraulics.mapped(int).connect(self.tbl_3_combo_indexChanged)
        self.sm_hydraulics.mapped.connect(self.tbl_3_combo_indexChanged)
        self.populate_defaults()
        self.loaded = True

    def resizeCorner(self):
        tab_ind = self.tabDefaults.currentIndex()
        if tab_ind == 0:
            self.corner_label_tab1.setGeometry(0, 0, self.tblGeneric.verticalHeader().width(),
                          self.tblGeneric.horizontalHeader().height())
        elif tab_ind == 1:
            self.corner_label_tab2.setGeometry(0, 0, self.tbl_2.verticalHeader().width(),
                                               self.tbl_2.horizontalHeader().height())
        elif tab_ind == 2:
            self.corner_label_tab3.setGeometry(0, 0, self.tbl_3.verticalHeader().width(),
                                               self.tbl_3.horizontalHeader().height())

    def populate_defaults(self):
        """
        set up the defaults from ini settings
        Returns:
        """
        self.set_tabs(3)
        self.tabDefaults.setTabText(0, "ID Labels")
        self.tabDefaults.setTabText(1, "Properties")
        self.tabDefaults.setTabText(2, "Hydraulics")

        self.set_tab_prefix()
        self.set_tab_properties()
        self.set_tab_hydraulics()
        #self.tab_changed(0)

    def set_tabs(self, num_tab):
        """
        ensure desired number of tabs are created
        Args:
            num_tab: the desired number of tabs
        Returns:
        """
        while self.tabDefaults.count() < num_tab:
            c = self.tabDefaults.count()
            new_tab = QWidget(self.tabDefaults)
            self.tabDefaults.addTab(new_tab, "tab_" + str(c + 1))
        while self.tabDefaults.count() > num_tab:
            c = self.tabDefaults.count()
            w = self.tabDefaults.widget(c - 1)
            self.tabDefaults.removeTab(c - 1)
            if w:
                del w

    def set_tab_prefix(self):
        """
        setup the object id tab entries
        Returns:
        """
        #self.model_object_types = ["Junctions", "Reservoirs", "Tanks", "Pumps", "Valves", "Patterns", "Curves"]
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(len(self.defaults.model_object_keys))
        self.tblGeneric.setHorizontalHeaderLabels(["ID Prefix"])
        self.tblGeneric.setVerticalHeaderLabels(self.defaults.model_object_keys)
        for i in range(0, len(self.defaults.model_object_keys)):
            prefix = self.defaults.model_object_prefix[self.defaults.model_object_keys[i]]
            #if self.qsettings:
            #    prefix = unicode(self.qsettings.value("Labels/" + self.model_object_types[i], ""))
            #self.tblGeneric.insertRow(self.tblGeneric.rowCount())
            self.tblGeneric.setItem(i,0, QTableWidgetItem(prefix))
        self.tblGeneric.insertRow(self.tblGeneric.rowCount())
        self.tblGeneric.setVerticalHeaderItem(self.tblGeneric.rowCount()- 1,
                                              QTableWidgetItem(self.defaults.id_increment_key))
        # self.increment = unicode(self.defaults.id_increment)
        self.increment = self.defaults.id_increment
        #if self.qsettings:
        #    self.increment = int(self.qsettings.value("Labels/Increment", 1))
        self.tblGeneric.setItem(self.tblGeneric.rowCount() - 1, 0, QTableWidgetItem(str(self.increment)))

        pass

    def set_tab_properties(self):
        """
        setup object property defaults tab entries
        Returns:
        """
        #self.properties = {"Node Elevation" : 0, "Tank Diameter" : 50, "Tank Height" : 20, "Pipe Length" : 1000,
        #                   "Pipe Diameter" : 12, "Pipe Roughness" : 100, "Auto Length" : "Off"}
        #self.properties = ["Node Elevation", "Tank Diameter", "Tank Height", "Pipe Length",
        #                   "Pipe Diameter", "Pipe Roughness", "Auto Length"]
        #self.properties_def_values = [0, 50, 20, 1000, 12, 100, "Off"]
        self.tbl_2.setColumnCount(1)
        self.tbl_2.setRowCount(len(self.defaults.properties_keys))
        self.tbl_2.setHorizontalHeaderLabels(["Default Value"])
        self.tbl_2.setVerticalHeaderLabels(self.defaults.properties_keys)
        for i in range(0, len(self.defaults.properties_keys)):
            def_val = self.defaults.properties_values[self.defaults.properties_keys[i]]
            #if self.qsettings:
            #    def_val = unicode(self.qsettings.value("Defaults/" + self.properties[i], def_val))
            key = self.defaults.properties_keys[i].lower()
            if "auto" in key:
                self.autolen_on = "Off"
                if def_val is not None:
                    self.autolen_on = def_val
                #if self.qsettings:
                #    self.autolen_on = unicode(
                #        self.qsettings.value("Defaults/" + self.properties[len(self.properties) - 1], "Off"))
                #self.tbl_2.setItem(self.tbl_2.rowCount() - 1, 0, QTableWidgetItem(self.autolen_on))
                combobox = QComboBox()
                combobox.addItem("On")
                combobox.addItem("Off")
                set_combo(combobox, self.autolen_on)
                combobox.setObjectName(key + "|" + str(i) + "|0")
                combobox.currentIndexChanged.connect(self.sm_property.map)
                self.sm_property.setMapping(combobox, i)
                self.tbl_2.setCellWidget(i, 0, combobox)
            else:
                self.tbl_2.setItem(i,0, QTableWidgetItem(str(def_val)))
        pass

    def set_tab_hydraulics(self):
        """
        setup the hydraulic parameter defaults tab entries
        Returns:
        """
        #self.parameters = ["Flow Units", "Headloss Formula", "Specific Gravity", "Relative Viscosity",
        #                   "Maximum Trials", "Accuracy", "If Unbalanced", "Default Pattern", "Demand Multiplier",
        #                   "Emitter Exponent", "Status Report", "Check Frequency", "Max Check", "Damp Limit"]
        #self.parameters_def_values = ["GPM", "H_W", 1.0, 1.0, 40, 0.001, "Continue", 1, 1.0, 0.5, "Yes",
        #                              "", "", ""]
        self.tbl_3.setColumnCount(1)
        self.tbl_3.setRowCount(len(self.defaults.parameters_keys))
        self.tbl_3.setHorizontalHeaderLabels(["Default Value"])
        self.tbl_3.setVerticalHeaderLabels(self.defaults.parameters_keys)
        for i in range(0, len(self.defaults.parameters_keys) - 1):
            combobox = None
            #def_val = self.parameters_def_values[self.parameters.index(self.parameters[i])]
            def_val = self.defaults.parameters_values[self.defaults.parameters_keys[i]]
            #if self.qsettings:
            #    def_val = unicode(self.qsettings.value("Defaults/" + self.parameters[i], def_val))
            key = self.defaults.parameters_keys[i].lower()
            if "flow units" in key:
                combobox = QComboBox()
                enum_val = FlowUnits[def_val]
            elif "headloss" in key:
                combobox = QComboBox()
                enum_val = HeadLoss[def_val.replace("-", "_")]
            elif "unbalanced" in key:
                combobox = QComboBox()
                enum_val = Unbalanced[def_val.upper()]
            elif "status report" in key:
                combobox = QComboBox()
                enum_val = StatusWrite[def_val.upper()]

            if combobox is not None:
                combobox.setObjectName(key + "|" + str(i) + "|0")
                set_combo_items(type(enum_val), combobox)
                set_combo(combobox, enum_val)
                combobox.currentIndexChanged.connect(self.sm_hydraulics.map)
                self.sm_hydraulics.setMapping(combobox, i)
                self.tbl_3.setCellWidget(i, 0, combobox)
            else:
                self.tbl_3.setItem(i,0, QTableWidgetItem(str(def_val)))
        pass

    def move_table(self, index):
        """
        dynamically move table control to the currently active tab
        this is when only one table control is shared among multiple tabs
        Args:
            index: the active tab's index
        Returns:
        """
        for i in range(0, self.tabDefaults.count()):
            controls = self.tabDefaults.widget(i).findChildren(QTableWidget, self.tblGeneric.objectName())
            if len(controls) > 0 and i != index:
                layout_src = self.tabDefaults.widget(i).layout()
                if layout_src is not None:
                    layout_src.removeWidget(self.tblGeneric)
                layout_dest = self.tabDefaults.widget(index).layout()
                if layout_dest is None:
                    layout_dest = QGridLayout(self.tabDefaults.widget(index))
                    self.tabDefaults.widget(index).setLayout(layout_dest)
                layout_dest.addChildWidget(self.tblGeneric)
                break

        pass

    def tab_changed(self, index):
        #self.move_table(index)
        if index == 0:
            self.help_topic = "epanet/src/src/Proj0043.htm"
        #    self.set_tab_prefix()
        elif index == 1:
            self.help_topic = "epanet/src/src/Proj0045.htm"
        #    self.set_tab_properties()
        elif index == 2:
            self.help_topic = "epanet/src/src/Proj0044.htm"
        #    self.set_tab_hydraulics()
        pass

    def tblGeneric_changed(self, row, col):
        if not self.loaded: return
        if self.tblGeneric.verticalHeaderItem(row) is None: return
        item = self.tblGeneric.item(row, col)
        if item is None: return
        key = self.tblGeneric.verticalHeaderItem(row).text()
        if row == self.tblGeneric.rowCount() - 1:
            val, val_is_good = ParseData.intTryParse(item.text())
            if val_is_good:
                self.defaults.id_increment = val
        else:
            self.defaults.model_object_prefix[key] = item.text()
        self.label_changed = True
        pass

    def tbl_2_changed(self, row, col):
        if not self.loaded: return
        if self.tbl_2.verticalHeaderItem(row) is None: return
        item = self.tbl_2.item(row, col)
        if item is None: return
        key = self.tbl_2.verticalHeaderItem(row).text()
        if "auto length" in key.lower():
            self.defaults.properties_values[key] = item.currentText()
        else:
            val, val_is_good = ParseData.floatTryParse(item.text())
            if val_is_good:
                self.defaults.properties_values[key] = val
        self.property_changed = True
        pass

    def tbl_2_combo_indexChanged(self, index):
        if not self.loaded: return
        cb = self.tbl_2.cellWidget(index, 0)
        key = self.tbl_2.verticalHeaderItem(index).text()
        val = cb.currentText()
        self.defaults.properties_values[key] = val
        self.property_changed = True
        pass

    def tbl_3_changed(self, row, col):
        if not self.loaded: return
        if self.tbl_3.verticalHeaderItem(row) is None: return
        item = self.tbl_3.item(row, col)
        if item is None: return
        key = self.tbl_3.verticalHeaderItem(row).text()
        if "flow units" in key.lower() or \
           "headloss" in key.lower() or \
           "unbalanced" in key.lower() or \
           "status report" in key.lower():
            # do nothing
            pass
        elif "maximum trials" in key.lower() or \
             "default pattern" in key.lower() or \
             "check freq" in key.lower() or \
             "max check" in key.lower():
            val, val_is_good = ParseData.intTryParse(item.text())
            if val_is_good:
                self.defaults.parameters_values[key] = val
        else:
            val, val_is_good = ParseData.floatTryParse(item.text())
            if val_is_good:
                self.defaults.parameters_values[key] = val
        self.parameter_changed = True
        pass

    def tbl_3_combo_indexChanged(self, index):
        if not self.loaded: return
        cb = self.tbl_3.cellWidget(index, 0)
        key = self.tbl_3.verticalHeaderItem(index).text()
        val = cb.currentText()
        self.defaults.parameters_values[key] = val
        self.parameter_changed = True
        pass

    def cmdOK_Clicked(self):
        """
        save/sync user changes to the defaults
        Returns:
        """
        if self.label_changed:
            self.defaults.sync_defaults_label()
            pass

        if self.property_changed:
            self.defaults.sync_defaults_property()
            pass

        if self.parameter_changed:
            self.defaults.sync_defaults_parameter()
            pass

        if self.chk4all.isChecked():
            # take default labels and defaults from project ini file and apply to global EPANET.ini file
            self.session.program_settings.sync()
            pass

        self.close()
        pass

    def cmdCancel_Clicked(self):
        """
        discard user changes to the defaults
        Returns:
        """
        self.close()
        pass
