import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericDefaultsEditorDesigner import Ui_frmGenericDefaultsEditor
from ui.inifile import ini_setting
from ui.convenience import set_combo_items
from ui.convenience import set_combo
from core.swmm.hydrology.subcatchment import E_Infiltration
from core.swmm.options.general import FlowUnits
from core.swmm.options.general import LinkOffsets
from core.swmm.options.general import FlowRouting
from core.swmm.options.dynamic_wave import ForceMainEquation
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmInfiltration import frmInfiltration
from ui.SWMM.frmCrossSection import frmCrossSection
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
    def __init__(self, session, project, qsettings):
        QtGui.QMainWindow.__init__(self, session)
        self.setupUi(self)
        self.qsettings = qsettings
        self.session = session
        self.project = project
        self.default_key_channel = "def_xsection"
        self.default_key_infilmodel = "def_infilmodel"
        if self.session is not None:
            self.setWindowTitle(self.session.model + " Project Defaults")
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.tabDefaults, QtCore.SIGNAL("currentChanged(int)"), self.tab_changed)

        self.gridLayout_tab2 = QtGui.QGridLayout(self.tabDefaults.widget(1))
        self.gridLayout_tab2.setObjectName(_fromUtf8("gridLayout_tab2"))
        self.tbl_2 = QtGui.QTableWidget(self.tabDefaults.widget(1))
        self.tbl_2.setObjectName(_fromUtf8("tbl_2"))
        self.tbl_2.setColumnCount(1)
        self.tbl_2.setRowCount(1)
        self.tbl_2.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_tab2.addWidget(self.tbl_2, 0, 0, 0, 0)

        self.gridLayout_tab3 = QtGui.QGridLayout(self.tabDefaults.widget(2))
        self.gridLayout_tab3.setObjectName(_fromUtf8("gridLayout_tab3"))
        self.tbl_3 = QtGui.QTableWidget(self.tabDefaults.widget(2))
        self.tbl_3.setObjectName(_fromUtf8("tbl_3"))
        self.tbl_3.setColumnCount(1)
        self.tbl_3.setRowCount(1)
        self.tbl_3.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_tab3.addWidget(self.tbl_3, 0, 0, 0, 0)

        self.populate_defaults()
        self.installEventFilter(self)

    def populate_defaults(self):
        """
        set up the defaults from ini settings
        Returns:
        """
        self.set_tabs(3)
        self.tabDefaults.setTabText(0, "ID Labels")
        self.tabDefaults.setTabText(1, "Subcatchments")
        self.tabDefaults.setTabText(2, "Nodes/Links")

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
        self.model_object_types = ["Rain Gages", "Subcatchments", "Junctions", "Outfalls", "Dividers",
                                   "Storage Units", "Conduits", "Pumps", "Regulators"]
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(len(self.model_object_types))
        self.tblGeneric.setHorizontalHeaderLabels(["ID Prefix"])
        self.tblGeneric.setVerticalHeaderLabels(self.model_object_types)
        for i in range(0, len(self.model_object_types)):
            prefix = ""
            if self.qsettings:
                prefix = unicode(self.qsettings.value("Labels/" + self.model_object_types[i], ""))
            #self.tblGeneric.insertRow(self.tblGeneric.rowCount())
            self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(prefix))
        self.tblGeneric.insertRow(self.tblGeneric.rowCount())
        self.tblGeneric.setVerticalHeaderItem(self.tblGeneric.rowCount()- 1, QtGui.QTableWidgetItem("ID Increment"))
        self.increment = "1"
        if self.qsettings:
            self.increment = int(self.qsettings.value("Labels/Increment", 1))
        self.tblGeneric.setItem(self.tblGeneric.rowCount()- 1,0, QtGui.QTableWidgetItem(self.increment))

        pass

    def set_tab_properties(self):
        """
        setup object property defaults tab entries
        Returns:
        """
        #self.properties = {"Node Elevation" : 0, "Tank Diameter" : 50, "Tank Height" : 20, "Pipe Length" : 1000,
        #                   "Pipe Diameter" : 12, "Pipe Roughness" : 100, "Auto Length" : "Off"}
        self.properties = ["Area", "Width", "% Slope", "% Imperv", "N-Imperv", "N-Perv",
                           "Dstore-Imperv", "Dstore-Perv", "%Zero-Imperv", "Infiltration Model"]
        self.properties_def_values = [5, 500, 0.5, 25, 0.01, 0.1, 0.05, 0.05, 25, "HORTON"]
        self.tbl_2.setColumnCount(1)
        self.tbl_2.setRowCount(len(self.properties))
        self.tbl_2.setHorizontalHeaderLabels(["Default Value"])
        self.tbl_2.setVerticalHeaderLabels(self.properties)
        for i in range(0, len(self.properties) - 1):
            def_val = self.properties_def_values[self.properties.index(self.properties[i])]
            if self.qsettings:
                def_val = unicode(self.qsettings.value("Defaults/" + self.properties[i], def_val))
            self.tbl_2.setItem(i,0, QtGui.QTableWidgetItem(unicode(def_val)))
        self.set_infilmodel_cell(0)

        pass

    def set_tab_hydraulics(self):
        """
        setup the hydraulic parameter defaults tab entries
        Returns:
        """
        self.parameters = ["Node Invert", "Node Max. Depth", "Node Ponded Area", "Conduit Length", "Conduit Geometry",
                           "Conduit Roughness", "Flow Units", "Link Offsets", "Routing Method", "Force Main Equation"]
        self.parameters_def_values = [0, 0, 0, 400, "CIRCULAR", 0.01, "CFS", "DEPTH", "KINWAVE", "H_W"]
        self.tbl_3.setColumnCount(1)
        self.tbl_3.setRowCount(len(self.parameters))
        self.tbl_3.setHorizontalHeaderLabels(["Default Value"])
        self.tbl_3.setVerticalHeaderLabels(self.parameters)
        for i in range(0, len(self.parameters)):
            combobox = None
            def_val = self.parameters_def_values[self.parameters.index(self.parameters[i])]
            if self.qsettings:
                def_val = unicode(self.qsettings.value("Defaults/" + self.parameters[i], def_val))
            if "flow units" in self.parameters[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = FlowUnits[def_val]
            elif "link offsets" in self.parameters[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = LinkOffsets[def_val]
            elif "routing method" in self.parameters[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = FlowRouting[def_val.upper()]
            elif "force main" in self.parameters[i].lower():
                combobox = QtGui.QComboBox()
                enum_val = ForceMainEquation[def_val.upper()]

            if combobox is not None:
                set_combo_items(type(enum_val), combobox)
                set_combo(combobox, enum_val)
                self.tbl_3.setCellWidget(i, 0, combobox)
            else:
                if "conduit geometry" in self.parameters[i].lower():
                    self.set_channel_cell(0)
                else:
                    self.tbl_3.setItem(i,0, QtGui.QTableWidgetItem(unicode(def_val)))
        pass

    def eventFilter(self, ui_object, event):
        if event.type() == QtCore.QEvent.WindowUnblocked:
            if self.refresh_column > -1:
                self.set_infilmodel_cell(self.refresh_column)
                self.set_channel_cell(self.refresh_column)
                self.refresh_column = -1
        return False

    def set_infilmodel_cell(self, column):
        # text plus button for demand categories editor
        tb = TextPlusButton(self)
        self.infil_model = "HORTON"
        if self.qsettings:
            self.infil_model = unicode(self.qsettings.value("Defaults/" + self.properties[len(self.properties) - 1],
                                                           self.infil_model))
        tb.textbox.setText(self.infil_model)
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_infilmodel(column))
        self.tbl_2.setCellWidget(self.tbl_2.rowCount() - 1, 0, tb)

    def make_show_infilmodel(self, column):
        def local_show():
            frm = frmInfiltration(self, [], None, "Default Infiltration Model")
            #frm.set_from(self.project, "")
            frm.setWindowModality(QtCore.Qt.ApplicationModal)
            frm.show()
            self.refresh_column = column
        return local_show

    def set_channel_cell(self, column):
        # text plus button for demand categories editor
        tb = TextPlusButton(self)
        self.channel_geom = "CIRCULAR"
        if self.qsettings:
            if self.qsettings.contains(self.default_key_channel):
                xs = self.qsettings.value(self.default_key_channel)
                if xs is not None:
                    self.channel_geom = unicode(xs.shape.name)
            else:
                self.channel_geom = unicode(self.qsettings.value("Defaults/" + self.parameters[4], self.channel_geom))
        tb.textbox.setText(self.channel_geom)
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_channel(column, self.qsettings))
        self.tbl_3.setCellWidget(4, 0, tb)

    def make_show_channel(self, column, setting):
        def local_show():
            frm = frmCrossSection(self, qsettings=setting, default_key=self.default_key_channel)
            frm.setWindowTitle("Define Default Conduit Geometry")
            #frm.set_from(self.project, "")
            frm.setWindowModality(QtCore.Qt.ApplicationModal)
            frm.show()
            self.refresh_column = column
        return local_show

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
