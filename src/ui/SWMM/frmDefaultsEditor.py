import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericDefaultsEditorDesigner import Ui_frmGenericDefaultsEditor
from ui.inifile import ini_setting
from ui.convenience import set_combo_items
from ui.convenience import set_combo
from core.swmm.hydrology.subcatchment import E_InfilModel
from core.swmm.options.general import FlowUnits
from core.swmm.options.general import LinkOffsets
from core.swmm.options.general import FlowRouting
from core.swmm.options.dynamic_wave import ForceMainEquation
from core.swmm.hydrology.subcatchment import HortonInfiltration
from core.swmm.hydrology.subcatchment import GreenAmptInfiltration
from core.swmm.hydrology.subcatchment import CurveNumberInfiltration
from core.swmm.hydraulics.link import CrossSection
from core.swmm.hydraulics.link import CrossSectionShape
from ui.text_plus_button import TextPlusButton
from ui.SWMM.frmInfiltration import frmInfiltration
from ui.SWMM.frmCrossSection import frmCrossSection
from ui.model_utility import ParseData
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
        self.label_changed = False
        self.property_sub_changed = False
        self.parameter_changed = False
        self.loaded = False
        self.refresh_column = None
        if self.session is not None:
            self.setWindowTitle(self.session.model + " Project Defaults")
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.tabDefaults, QtCore.SIGNAL("currentChanged(int)"), self.tab_changed)
        QtCore.QObject.connect(self.tblGeneric, QtCore.SIGNAL("cellChanged(int, int)"), self.tblGeneric_changed)

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
        QtCore.QObject.connect(self.tbl_2, QtCore.SIGNAL("cellChanged(int, int)"), self.tbl_2_changed)

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
        QtCore.QObject.connect(self.tbl_3, QtCore.SIGNAL("cellChanged(int, int)"), self.tbl_3_changed)

        self.corner_label_tab3 = QtGui.QLabel("Option", self.tbl_3)
        self.corner_label_tab3.setAlignment(QtCore.Qt.AlignCenter)
        self.corner_label_tab3.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        QtCore.QObject.connect(self.tbl_3.verticalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)
        QtCore.QObject.connect(self.tbl_3.horizontalHeader(),
                               QtCore.SIGNAL("geometriesChanged()"), self.resizeCorner)

        self.sm_hydraulics = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(self.sm_hydraulics, QtCore.SIGNAL("mapped(int)"),
                               self.tbl_3_combo_indexChanged)

        self.populate_defaults()
        self.installEventFilter(self)
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
        self.tabDefaults.setTabText(1, "Subcatchments")
        self.tabDefaults.setTabText(2, "Nodes/Links")

        self.set_tab_prefix()
        self.set_sub_properties()
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
        #self.model_object_keys = ["Rain Gage", "Subcatchment", "Junction", "Outfall", "Divider",
        #                           "Storage Unit", "Conduit", "Pump", "Regulator"]
        self.tblGeneric.setColumnCount(1)
        self.tblGeneric.setRowCount(len(self.defaults.model_object_keys))
        self.tblGeneric.setHorizontalHeaderLabels(["ID Prefix"])
        self.tblGeneric.setVerticalHeaderLabels(self.defaults.model_object_keys)
        for i in range(0, len(self.defaults.model_object_keys)):
            prefix = ""
            if self.defaults:
                #prefix = unicode(self.qsettings.value("Labels/" + self.model_object_keys[i], ""))
                prefix = self.defaults.model_object_prefix[self.defaults.model_object_keys[i]]
            #self.tblGeneric.insertRow(self.tblGeneric.rowCount())
            self.tblGeneric.setItem(i,0, QtGui.QTableWidgetItem(prefix))
        self.tblGeneric.insertRow(self.tblGeneric.rowCount())
        self.tblGeneric.setVerticalHeaderItem(self.tblGeneric.rowCount()- 1,
                                              QtGui.QTableWidgetItem(self.defaults.id_increment_key))
        if self.defaults:
            #self.increment = int(self.qsettings.value("Labels/Increment", 1))
            self.increment = self.defaults.id_increment
        self.tblGeneric.setItem(self.tblGeneric.rowCount()- 1,0,
                                QtGui.QTableWidgetItem(unicode(self.defaults.id_increment)))
        pass

    def set_sub_properties(self):
        """
        setup object property defaults tab entries
        Returns:
        """
        #self.properties = ["Area", "Width", "% Slope", "% Imperv", "N-Imperv", "N-Perv",
        #                   "Dstore-Imperv", "Dstore-Perv", "%Zero-Imperv", "Infiltration Model"]
        #self.properties_def_values = [5, 500, 0.5, 25, 0.01, 0.1, 0.05, 0.05, 25, "HORTON"]
        self.tbl_2.setColumnCount(1)
        self.tbl_2.setRowCount(len(self.defaults.properties_sub_keys))
        self.tbl_2.setHorizontalHeaderLabels(["Default Value"])
        self.tbl_2.setVerticalHeaderLabels(self.defaults.properties_sub_keys)
        for i in range(0, len(self.defaults.properties_sub_keys) - 1):
            #def_val = unicode(self.qsettings.value("Defaults/" + self.properties[i], def_val))
            def_val = self.defaults.properties_sub_values[self.defaults.properties_sub_keys[i]]
            self.tbl_2.setItem(i,0, QtGui.QTableWidgetItem(unicode(def_val)))
        self.set_infilmodel_cell(0)

        pass

    def set_tab_hydraulics(self):
        """
        setup the hydraulic parameter defaults tab entries
        Returns:
        """
        #self.parameters = ["Node Invert", "Node Max. Depth", "Node Ponded Area", "Conduit Length", "Conduit Geometry",
        #                   "Conduit Roughness", "Flow Units", "Link Offsets", "Routing Method", "Force Main Equation"]
        #self.parameters_def_values = [0, 0, 0, 400, "CIRCULAR", 0.01, "CFS", "DEPTH", "KINWAVE", "H_W"]
        self.tbl_3.setColumnCount(1)
        self.tbl_3.setRowCount(len(self.defaults.parameters_keys))
        self.tbl_3.setHorizontalHeaderLabels(["Default Value"])
        self.tbl_3.setVerticalHeaderLabels(self.defaults.parameters_keys)
        for i in range(0, len(self.defaults.parameters_keys)):
            combobox = None
            key = self.defaults.parameters_keys[i]
            def_val = self.defaults.parameters_values[key]
            if "flow units" in key.lower():
                combobox = QtGui.QComboBox()
                enum_val = FlowUnits[def_val]
            elif "link offsets" in key.lower():
                combobox = QtGui.QComboBox()
                enum_val = LinkOffsets[def_val]
            elif "routing method" in key.lower():
                combobox = QtGui.QComboBox()
                enum_val = FlowRouting[def_val.upper()]
            elif "force main" in key.lower():
                combobox = QtGui.QComboBox()
                enum_val = ForceMainEquation[def_val.upper()]

            if combobox is not None:
                combobox.setObjectName(key + "|" + str(i) + "|0")
                set_combo_items(type(enum_val), combobox)
                set_combo(combobox, enum_val)
                QtCore.QObject.connect(combobox, QtCore.SIGNAL("currentIndexChanged(int)"),
                                       self.sm_hydraulics, QtCore.SLOT("map()"))
                self.sm_hydraulics.setMapping(combobox, i)
                self.tbl_3.setCellWidget(i, 0, combobox)
            else:
                if "conduit geometry" in key.lower():
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
        self.infil_model = E_InfilModel.HORTON.name
        if self.defaults:
            self.infil_model = self.defaults.properties_sub_values[self.defaults.infil_model_key]
            # if self.qsettings.contains(self.default_key_infilmodel):
            #     model_obj = self.qsettings.value(self.default_key_infilmodel)
            #     # model_name = type(model_obj)
            #     if model_obj is not None:
            #         self.infil_model = unicode(model_obj.model_type().name)
            # else:
            #     self.infil_model = unicode(self.qsettings.value("Defaults/" + self.properties[len(self.properties) - 1],
            #                                                self.infil_model))
        tb.textbox.setText(self.infil_model)
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_infilmodel(column))
        self.tbl_2.setCellWidget(self.tbl_2.rowCount() - 1, 0, tb)
        self.property_sub_changed = True

    def make_show_infilmodel(self, column):
        def local_show():
            frm = frmInfiltration(self, [], None, "Default Infiltration Model",
                                  defaults=self.defaults)
            #frm.set_from(self.project, "")
            frm.setWindowModality(QtCore.Qt.ApplicationModal)
            frm.show()
            self.refresh_column = column
        return local_show

    def set_channel_cell(self, column):
        # text plus button for demand categories editor
        # xsection = CrossSection()
        tb = TextPlusButton(self)
        if self.defaults is not None and self.defaults.xsection is not None:
            self.channel_geom = self.defaults.xsection.shape.name
        tb.textbox.setText(self.channel_geom)
        tb.textbox.setEnabled(False)
        tb.column = column
        tb.button.clicked.connect(self.make_show_channel(column, self.defaults))
        self.tbl_3.setCellWidget(4, 0, tb)

    def make_show_channel(self, column, defaults):
        def local_show():
            frm = frmCrossSection(self, defaults=defaults)
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
        #    self.set_sub_properties()
        #elif index == 2:
        #    self.set_tab_hydraulics()
        pass

    def tblGeneric_changed(self, row, col):
        if not self.loaded: return
        if self.tblGeneric.verticalHeaderItem(row) is None: return
        item = self.tblGeneric.item(row, col)
        if item is None: return
        key = self.tblGeneric.verticalHeaderItem(row).text()
        if key == self.defaults.id_increment_key:
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
        if "infiltration model" in key.lower():
            self.defaults.properties_sub_values[key] = item.currentText()
        else:
            val, val_is_good = ParseData.floatTryParse(item.text())
            if val_is_good:
                self.defaults.properties_sub_values[key] = val
        self.property_changed = True
        pass

    def tbl_3_changed(self, row, col):
        if not self.loaded: return
        if self.tbl_3.verticalHeaderItem(row) is None: return
        item = self.tbl_3.item(row, col)
        if item is None: return
        key = self.tbl_3.verticalHeaderItem(row).text()
        if "flow units" in key.lower() or \
           "link offsets" in key.lower() or \
           "routing" in key.lower() or \
           "force main" in key.lower():
            # do nothing
            pass
        elif "conduit geometry" in key.lower():
            #self.defaults.xsection.shape = CrossSection[item.text()]
            pass
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

        if self.property_sub_changed:
            self.defaults.sync_defaults_sub_property()
            pass

        if self.parameter_changed:
            self.defaults.sync_defaults_parameter()
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
