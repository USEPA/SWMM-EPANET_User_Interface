import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericDefaultsEditorDesigner import Ui_frmGenericDefaultsEditor
from ui.inifile import ini_setting
from ui.convenience import set_combo_items
from ui.convenience import set_combo
from core.epanet.options.hydraulics import FlowUnits
from core.epanet.options.hydraulics import HeadLoss
from core.epanet.options.hydraulics import Unbalanced
from core.epanet.options.report import StatusWrite
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class frmDefaultsEditor(QtGui.QMainWindow, Ui_frmGenericDefaultsEditor):
    """
    Project defaults editor for setting and editing
    object id prefix (tab1)
    properties (tab2)
    hydraulic defaults (tab3)
    """
    def __init__(self, session, project, defaults):
        QtGui.QMainWindow.__init__(self, session)
        self.setupUi(self)
        self.defaults = defaults
        self.session = session
        self.project = project
        if self.session is not None:
            self.setWindowTitle(self.session.model + " Project Defaults")
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.tabDefaults, QtCore.SIGNAL("currentChanged(int)"), self.tab_changed)

        self.corner_label_tab1 = QtGui.QLabel("Object", self.tblGeneric)
        self.corner_label_tab1.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab1.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        QtCore.QObject.connect(self.tblGeneric.verticalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)
        QtCore.QObject.connect(self.tblGeneric.horizontalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)


        self.gridLayout_tab2 = QtGui.QGridLayout(self.tabDefaults.widget(1))
        self.gridLayout_tab2.setObjectName(_fromUtf8("gridLayout_tab2"))
        self.tbl_2 = QtGui.QTableWidget(self.tabDefaults.widget(1))
        self.tbl_2.setObjectName(_fromUtf8("tbl_2"))
        self.tbl_2.setColumnCount(1)
        self.tbl_2.setRowCount(1)
        self.tbl_2.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_tab2.addWidget(self.tbl_2, 0, 0, 0, 0)

        self.corner_label_tab2 = QtGui.QLabel("Property", self.tbl_2)
        self.corner_label_tab2.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab2.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        QtCore.QObject.connect(self.tblGeneric.verticalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)
        QtCore.QObject.connect(self.tblGeneric.horizontalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)

        self.gridLayout_tab3 = QtGui.QGridLayout(self.tabDefaults.widget(2))
        self.gridLayout_tab3.setObjectName(_fromUtf8("gridLayout_tab3"))
        self.tbl_3 = QtGui.QTableWidget(self.tabDefaults.widget(2))
        self.tbl_3.setObjectName(_fromUtf8("tbl_3"))
        self.tbl_3.setColumnCount(1)
        self.tbl_3.setRowCount(1)
        self.tbl_3.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_tab3.addWidget(self.tbl_3, 0, 0, 0, 0)

        self.corner_label_tab3 = QtGui.QLabel("Option", self.tbl_3)
        self.corner_label_tab3.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab3.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        QtCore.QObject.connect(self.tbl_3.verticalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)
        QtCore.QObject.connect(self.tbl_3.horizontalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)

        self.populate_defaults()

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
            new_tab = QtGui.QWidget(self.tabDefaults)
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
            self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(prefix))
        self.tblGeneric.insertRow(self.tblGeneric.rowCount())
        self.tblGeneric.setVerticalHeaderItem(self.tblGeneric.rowCount()- 1,
                                              QtGui.QTableWidgetItem(self.defaults.id_increment_key))
        self.increment = unicode(self.defaults.id_increment)
        #if self.qsettings:
        #    self.increment = int(self.qsettings.value("Labels/Increment", 1))
        self.tblGeneric.setItem(self.tblGeneric.rowCount()- 1,0, QtGui.QTableWidgetItem(self.increment))

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
            if "auto" in self.defaults.properties_keys[i].lower():
                self.autolen_on = "Off"
                if def_val is not None:
                    self.autolen_on = def_val
                #if self.qsettings:
                #    self.autolen_on = unicode(
                #        self.qsettings.value("Defaults/" + self.properties[len(self.properties) - 1], "Off"))
                #self.tbl_2.setItem(self.tbl_2.rowCount() - 1, 0, QtGui.QTableWidgetItem(self.autolen_on))
                combobox = QtGui.QComboBox()
                combobox.addItem("On")
                combobox.addItem("Off")
                set_combo(combobox, self.autolen_on)
                #self.tbl_2.setCellWidget(self.tbl_2.rowCount() - 1, 0, combobox)
                self.tbl_2.setCellWidget(i, 0, combobox)
            else:
                self.tbl_2.setItem(i,0, QtGui.QTableWidgetItem(unicode(def_val)))
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
            if "flow units" in self.defaults.parameters_keys[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = FlowUnits[def_val]
            elif "headloss" in self.defaults.parameters_keys[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = HeadLoss[def_val.replace("-", "_")]
            elif "unbalanced" in self.defaults.parameters_keys[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = Unbalanced[def_val.upper()]
            elif "status report" in self.defaults.parameters_keys[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = StatusWrite[def_val.upper()]

            if combobox is not None:
                set_combo_items(type(enum_val), combobox)
                set_combo(combobox, enum_val)
                self.tbl_3.setCellWidget(i, 0, combobox)
            else:
                self.tbl_3.setItem(i,0, QtGui.QTableWidgetItem(unicode(def_val)))
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
            controls = self.tabDefaults.widget(i).findChildren(QtGui.QTableWidget, self.tblGeneric.objectName())
            if len(controls) > 0 and i != index:
                layout_src = self.tabDefaults.widget(i).layout()
                if layout_src is not None:
                    layout_src.removeWidget(self.tblGeneric)
                layout_dest = self.tabDefaults.widget(index).layout()
                if layout_dest is None:
                    layout_dest = QtGui.QGridLayout(self.tabDefaults.widget(index))
                    self.tabDefaults.widget(index).setLayout(layout_dest)
                layout_dest.addChildWidget(self.tblGeneric)
                break

        pass

    def tab_changed(self, index):
        #self.move_table(index)
        #if index == 0:
        #    self.set_tab_prefix()
        #elif index == 1:
        #    self.set_tab_properties()
        #elif index == 2:
        #    self.set_tab_hydraulics()
        pass

    def cmdOK_Clicked(self):
        """
        save/sync user changes to the defaults
        Returns:
        """
        self.close()
        pass

    def cmdCancel_Clicked(self):
        """
        discard user changes to the defaults
        Returns:
        """
        self.close()
        pass
