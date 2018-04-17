import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
for typ in ["QString","QVariant", "QDate", "QDateTime", "QTextStream", "QTime", "QUrl"]:
    sip.setapi(typ, 2)
import webbrowser
import traceback
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QFileDialog, QColor
from time import sleep

from ui.model_utility import QString, from_utf8, transl8, process_events, StatusMonitor0
from ui.help import HelpHandler
from ui.frmMain import frmMain, ModelLayers
from ui.SWMM.frmDates import frmDates
from ui.SWMM.frmDynamicWave import frmDynamicWave
from ui.SWMM.frmMapBackdropOptions import frmMapBackdropOptions
from ui.SWMM.frmGeneralOptions import frmGeneralOptions
from ui.SWMM.frmInterfaceFiles import frmInterfaceFiles
from ui.SWMM.frmReportOptions import frmReportOptions
from ui.SWMM.frmTimeSteps import frmTimeSteps
from ui.SWMM.frmTitle import frmTitle

from ui.SWMM.frmAbout import frmAbout
from ui.SWMM.frmAquifers import frmAquifers
from ui.SWMM.frmClimatology import frmClimatology
from ui.SWMM.frmConduits import frmConduits
from ui.SWMM.frmControls import frmControls
from ui.SWMM.frmCurveEditor import frmCurveEditor
from ui.SWMM.frmOrifices import frmOrifices
from ui.SWMM.frmOutlets import frmOutlets
from ui.SWMM.frmPatternEditor import frmPatternEditor
from ui.SWMM.frmPumps import frmPumps
from ui.SWMM.frmTimeseries import frmTimeseries
from ui.SWMM.frmJunction import frmJunction
from ui.SWMM.frmOutfalls import frmOutfalls
from ui.SWMM.frmDividers import frmDividers
from ui.SWMM.frmStorageUnits import frmStorageUnits
from ui.SWMM.frmRainGages import frmRainGages
from ui.SWMM.frmSubcatchments import frmSubcatchments
from ui.SWMM.frmLID import frmLID
from ui.SWMM.frmSnowPack import frmSnowPack
from ui.SWMM.frmUnitHydrograph import frmUnitHydrograph
from ui.SWMM.frmTransect import frmTransect
from ui.SWMM.frmWeirs import frmWeirs
from ui.SWMM.frmCrossSection import frmCrossSection
from ui.SWMM.frmInflows import frmInflows
from ui.SWMM.frmLandUses import frmLandUses
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.SWMM.frmCalibrationData import frmCalibrationData
from ui.SWMM.frmSummaryReport import frmSummaryReport
from ui.SWMM.frmTimeSeriesPlot import frmTimeSeriesPlot
from ui.SWMM.frmProfilePlot import frmProfilePlot
from ui.SWMM.frmScatterPlot import frmScatterPlot
from ui.SWMM.frmTableSelection import frmTableSelection
from ui.SWMM.frmStatisticsReportSelection import frmStatisticsReportSelection

from core.swmm.swmm_project import SwmmProject as Project
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.hydrology.raingage import RainGage
from core.swmm.quality import Pollutant
from core.swmm.hydraulics.node import Junction
from core.swmm.hydraulics.node import Outfall
from core.swmm.hydraulics.node import Divider
from core.swmm.hydraulics.node import StorageUnit
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.hydrology.unithydrograph import UnitHydrograph
from core.swmm.hydraulics.link import Conduit
from core.swmm.hydraulics.link import Pump
from core.swmm.hydraulics.link import Orifice
from core.swmm.hydraulics.link import Outlet
from core.swmm.hydraulics.link import Weir
from core.swmm.hydraulics.link import Transect
from core.swmm.hydraulics.link import CrossSection
from core.swmm.quality import Landuse
from core.swmm.curves import Curve
from core.swmm.curves import CurveType
from core.swmm.timeseries import TimeSeries
from core.swmm.patterns import Pattern
from core.swmm.labels import Label
from core.swmm.hydraulics.node import SubCentroid
from core.swmm.hydraulics.link import SubLink

from frmRunSWMM import frmRunSWMM

import Externals.swmm.outputapi.SMOutputWrapper as SMO
from core.indexed_list import IndexedList
import ui.convenience
from ui.SWMM.inifile import DefaultsSWMM
from datetime import timedelta


class frmMainSWMM(frmMain):
    """Main form for SWMM user interface, based on frmMain which is shared with EPANET."""

    # Variables used to populate the tree control
    # Each item is a list: label plus either editing form for this section or a child list of tree variables.
    # If an editing form takes additional arguments, they follow the editing form as a list.
    # Special cases may just have a label and no editing form or children.
    # *_items are a lists of items in a section
    tree_options_General        = ["General",         frmGeneralOptions]
    tree_options_Dates          = ["Dates",           frmDates]
    tree_options_TimeSteps      = ["Time Steps",      frmTimeSteps]
    tree_options_DynamicWave    = ["Dynamic Wave",    frmDynamicWave]
    tree_options_InterfaceFiles = ["Interface Files", frmInterfaceFiles]
    tree_options_Reporting      = ["Reporting",       frmReportOptions]
    tree_options_MapBackdrop    = ["Map/Backdrop",    frmMapBackdropOptions]
    tree_options_items = [
        tree_options_General,
        tree_options_Dates,
        tree_options_TimeSteps,
        tree_options_DynamicWave,
        tree_options_InterfaceFiles,
        tree_options_Reporting,
        tree_options_MapBackdrop]

    tree_climatology_Temperature    = ["Temperature",     frmClimatology, ["Temperature"]]
    tree_climatology_Evaporation    = ["Evaporation",     frmClimatology, ["Evaporation"]]
    tree_climatology_WindSpeed      = ["Wind Speed",      frmClimatology, ["Wind Speed"]]
    tree_climatology_SnowMelt       = ["Snow Melt",       frmClimatology, ["Snow Melt"]]
    tree_climatology_ArealDepletion = ["Areal Depletion", frmClimatology, ["Areal Depletion"]]
    tree_climatology_Adjustment     = ["Adjustment",      frmClimatology, ["Adjustment"]]
    tree_climatology_items = [
        tree_climatology_Temperature,
        tree_climatology_Evaporation,
        tree_climatology_WindSpeed,
        tree_climatology_SnowMelt,
        tree_climatology_ArealDepletion,
        tree_climatology_Adjustment]

    tree_hydrology_RainGages       = ["Rain Gages",       frmRainGages]
    tree_hydrology_Subcatchments   = ["Subcatchments",    frmSubcatchments]
    tree_hydrology_Aquifers        = ["Aquifers",         frmAquifers]
    tree_hydrology_SnowPacks       = ["Snow Packs",       frmSnowPack]
    tree_hydrology_UnitHydrographs = ["Unit Hydrographs", frmUnitHydrograph]
    tree_hydrology_LIDControls     = ["LID Controls",     frmLID]
    tree_hydrology_items = [
        tree_hydrology_RainGages,
        tree_hydrology_Subcatchments,
        tree_hydrology_Aquifers,
        tree_hydrology_SnowPacks,
        tree_hydrology_UnitHydrographs,
        tree_hydrology_LIDControls]

    tree_nodes_Junctions    = ["Junctions",     frmJunction]
    tree_nodes_Outfalls     = ["Outfalls",      frmOutfalls]
    tree_nodes_Dividers     = ["Dividers",      frmDividers]
    tree_nodes_StorageUnits = ["Storage Units", frmStorageUnits]
    tree_nodes_items = [
        tree_nodes_Junctions,
        tree_nodes_Outfalls,
        tree_nodes_Dividers,
        tree_nodes_StorageUnits]

    tree_links_Conduits = ["Conduits", frmConduits]
    tree_links_Pumps    = ["Pumps",    frmPumps]
    tree_links_Orifices = ["Orifices", frmOrifices]
    tree_links_Weirs    = ["Weirs",    frmWeirs]
    tree_links_Outlets  = ["Outlets",  frmOutlets]
    tree_links_items = [
        tree_links_Conduits,
        tree_links_Pumps,
        tree_links_Orifices,
        tree_links_Weirs,
        tree_links_Outlets]

    tree_hydraulics_Nodes     = ["Nodes",     tree_nodes_items]
    tree_hydraulics_Links     = ["Links",     tree_links_items]
    tree_hydraulics_Transects = ["Transects", frmTransect]
    tree_hydraulics_Controls  = ["Controls",  frmControls]
    tree_hydraulics_items = [
        tree_hydraulics_Nodes,
        tree_hydraulics_Links,
        tree_hydraulics_Transects,
        tree_hydraulics_Controls]

    tree_quality_Pollutants = ["Pollutants", None]
    tree_quality_LandUses   = ["Land Uses",  frmLandUses]
    tree_quality_items = [
        tree_quality_Pollutants,
        tree_quality_LandUses]

    tree_curves_ControlCurves   = ["Control Curves",   frmCurveEditor, ["SWMM Control Curves",   "CONTROL"]]
    tree_curves_DiversionCurves = ["Diversion Curves", frmCurveEditor, ["SWMM Diversion Curves", "DIVERSION"]]
    tree_curves_PumpCurves      = ["Pump Curves",      frmCurveEditor, ["SWMM Pump Curves",      "PUMP"]]
    tree_curves_RatingCurves    = ["Rating Curves",    frmCurveEditor, ["SWMM Rating Curves",    "RATING"]]
    tree_curves_ShapeCurves     = ["Shape Curves",     frmCurveEditor, ["SWMM Shape Curves",     "SHAPE"]]
    tree_curves_StorageCurves   = ["Storage Curves",   frmCurveEditor, ["SWMM Storage Curves",   "STORAGE"]]
    tree_curves_TidalCurves     = ["Tidal Curves",     frmCurveEditor, ["SWMM Tidal Curves",     "TIDAL"]]
    tree_curves_items = [
        tree_curves_ControlCurves,
        tree_curves_DiversionCurves,
        tree_curves_PumpCurves,
        tree_curves_RatingCurves,
        tree_curves_ShapeCurves,
        tree_curves_StorageCurves,
        tree_curves_TidalCurves]

    tree_TitleNotes   = ["Title/Notes",   frmTitle]
    tree_Options      = ["Options",       tree_options_items]
    tree_Climatology  = ["Climatology",   tree_climatology_items]
    tree_Hydrology    = ["Hydrology",     tree_hydrology_items]
    tree_Hydraulics   = ["Hydraulics",    tree_hydraulics_items]
    tree_Quality      = ["Quality",       tree_quality_items]
    tree_Curves       = ["Curves",        tree_curves_items]
    tree_TimeSeries   = ["Time Series",   frmTimeseries]
    tree_TimePatterns = ["Time Patterns", frmPatternEditor]
    tree_MapLabels    = ["Map Labels",    None]
    tree_top_items = [
        tree_TitleNotes,
        tree_Options,
        tree_Climatology,
        tree_Hydrology,
        tree_Hydraulics,
        tree_Quality,
        tree_Curves,
        tree_TimeSeries,
        tree_TimePatterns,
        tree_MapLabels]

    tree_items_using_name = (tree_hydrology_Aquifers,
                           tree_hydrology_LIDControls,
                           tree_hydrology_UnitHydrographs,
                           tree_hydrology_SnowPacks,
                           tree_hydraulics_Transects,
                           tree_quality_LandUses,
                           tree_TimeSeries,
                           tree_TimePatterns,
                           tree_curves_ControlCurves,
                           tree_curves_DiversionCurves,
                           tree_curves_PumpCurves,
                           tree_curves_RatingCurves,
                           tree_curves_ShapeCurves,
                           tree_curves_StorageCurves,
                           tree_curves_TidalCurves)

    def __init__(self, q_application):
        self.model = "SWMM"

        self.program_settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope,
                                                 "EPA", self.model)
        print("Read program settings from " + self.program_settings.fileName())
        # ConfigParser is an alternative class for managing ini files.
        # Neither QSettings nor ConfigParser is backward-compatible with existing epaswmm5.ini,
        # they both cannot read the MRU section because it contains unescaped backslashes, and they have trouble with
        # keys that contain spaces, so we use a different file name to avoid corrupting the existing settings.
        # import ConfigParser
        # import Externals.appdirs as appdirs
        # self.program_settings_file = appdirs.user_data_dir(appauthor="EPASWMM", appname="epaswmm5.ini", roaming=True)
        # self.program_settings = ConfigParser.RawConfigParser()
        # self.program_settings.read(self.program_settings_file)
        # for name, value in self.program_settings.items("MRU"):
        #     print(name + " = " + value)

        self.model_path = ''  # Set this only if needed later when running model
        self.output = None    # Set this when model output is available
        self.status_suffix = "_status.txt"
        self.status_file_name = ''  # Set this when model status is available
        self.output_filename = ''  # Set this when model output is available
        self.animation_dates = {}
        self.animation_time_of_day = {}
        self.project_type = Project  # Use the model-specific Project as defined in core.swmm.project
        self.project_reader_type = ProjectReader
        self.project_writer_type = ProjectWriter
        self.project = Project()
        self.assembly_path = os.path.dirname(os.path.abspath(__file__))
        frmMain.__init__(self, q_application)
        self.on_load(tree_top_item_list=self.tree_top_items)
        self.project_settings = DefaultsSWMM("", self.project)
        self.tree_types = {
            self.tree_hydrology_Subcatchments[0]: Subcatchment,
            self.tree_hydrology_RainGages[0]: RainGage,
            self.tree_hydrology_Aquifers[0]: Aquifer,
            self.tree_hydrology_SnowPacks[0]: SnowPack,
            self.tree_hydrology_UnitHydrographs[0]: UnitHydrograph,
            self.tree_hydrology_LIDControls[0]: LIDControl,
            self.tree_nodes_Junctions[0]: Junction,
            self.tree_nodes_Outfalls[0]: Outfall,
            self.tree_nodes_Dividers[0]: Divider,
            self.tree_nodes_StorageUnits[0]: StorageUnit,
            self.tree_links_Conduits[0]: Conduit,
            self.tree_links_Pumps[0]: Pump,
            self.tree_links_Orifices[0]: Orifice,
            self.tree_links_Weirs[0]: Weir,
            self.tree_links_Outlets[0]: Outlet,
            self.tree_hydraulics_Transects[0]: Transect,
            self.tree_quality_Pollutants[0]: Pollutant,
            self.tree_quality_LandUses[0]: Landuse,
            self.tree_curves_ControlCurves[0]: Curve,
            self.tree_curves_DiversionCurves[0]: Curve,
            self.tree_curves_PumpCurves[0]: Curve,
            self.tree_curves_RatingCurves[0]: Curve,
            self.tree_curves_ShapeCurves[0]: Curve,
            self.tree_curves_StorageCurves[0]: Curve,
            self.tree_curves_TidalCurves[0]: Curve,
            self.tree_TimeSeries[0]: TimeSeries,
            self.tree_TimePatterns[0]: Pattern,
            self.tree_MapLabels[0]: Label
        }

        self.section_types = {
            Subcatchment: "subcatchments",
            RainGage: "raingages",
            Aquifer: "aquifers",
            SnowPack: "snowpacks",
            UnitHydrograph: "hydrographs",
            LIDControl: "lid_controls",
            Junction: "junctions",
            Outfall: "outfalls",
            Divider: "dividers",
            StorageUnit: "storage",
            Conduit: "conduits",
            Pump: "pumps",
            Orifice: "orifices",
            Weir: "weirs",
            Outlet: "outlets",
            Transect: "transects",
            Pollutant: "pollutants",
            Landuse: "landuses",
            Curve: "curves",
            TimeSeries: "timeseries",
            Pattern: "patterns",
            Label: "labels",
            SubCentroid: "subcentroids",
            SubLink: "sublinks"
        }

        if self.map_widget:  # initialize empty model map layers, ready to have model elements added
            self.model_layers = ModelLayersSWMM(self.map_widget)

        HelpHandler.init_class(os.path.join(self.assembly_path, "swmm.qhc"))
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/swmmsmainwindow.htm"

        self.actionTranslate_Coordinates = QtGui.QAction(self)
        self.actionTranslate_Coordinates.setObjectName(from_utf8("actionTranslate_CoordinatesMenu"))
        self.actionTranslate_Coordinates.setText(transl8("frmMain", "Translate Coordinates", None))
        self.actionTranslate_Coordinates.setToolTip(transl8("frmMain", "Change model objects coordinates", None))
        self.menuView.addAction(self.actionTranslate_Coordinates)
        QtCore.QObject.connect(self.actionTranslate_Coordinates, QtCore.SIGNAL('triggered()'),
                               lambda: self.open_translate_coord_dialog(None, None))

        self.actionStatus_ReportMenu = QtGui.QAction(self)
        self.actionStatus_ReportMenu.setObjectName(from_utf8("actionStatus_ReportMenu"))
        self.actionStatus_ReportMenu.setText(transl8("frmMain", "Status", None))
        self.actionStatus_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Status", None))
        self.menuReport.addAction(self.actionStatus_ReportMenu)
        QtCore.QObject.connect(self.actionStatus_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_status)
        self.actionProjStatus.triggered.connect(self.report_status)

        self.actionSummary_ReportMenu = QtGui.QAction(self)
        self.actionSummary_ReportMenu.setObjectName(from_utf8("actionSummary_ReportMenu"))
        self.actionSummary_ReportMenu.setText(transl8("frmMain", "Summary", None))
        self.actionSummary_ReportMenu.setToolTip(transl8("frmMain", "Display Results Summary", None))
        self.menuReport.addAction(self.actionSummary_ReportMenu)
        QtCore.QObject.connect(self.actionSummary_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_summary)

        menu = QtGui.QMenu()
        submenuGraph = QtGui.QMenu(self.menuReport)
        submenuGraph.setTitle("Graph")
        self.menuReport.addMenu(submenuGraph)

        self.actionGraph_ProfileMenu = QtGui.QAction(self)
        self.actionGraph_ProfileMenu.setObjectName(from_utf8("actionGraph_ProfileMenu"))
        self.actionGraph_ProfileMenu.setText(transl8("frmMain", "Profile", None))
        self.actionGraph_ProfileMenu.setToolTip(transl8("frmMain", "Display Profile Plot", None))
        submenuGraph.addAction(self.actionGraph_ProfileMenu)
        QtCore.QObject.connect(self.actionGraph_ProfileMenu, QtCore.SIGNAL('triggered()'), self.report_profile)
        self.actionProjPlotProfile.triggered.connect(self.report_profile)


        self.actionGraph_TimeSeriesMenu = QtGui.QAction(self)
        self.actionGraph_TimeSeriesMenu.setObjectName(from_utf8("actionGraph_TimeSeriesMenu"))
        self.actionGraph_TimeSeriesMenu.setText(transl8("frmMain", "Time Series", None))
        self.actionGraph_TimeSeriesMenu.setToolTip(transl8("frmMain", "Display Time Series Plot", None))
        submenuGraph.addAction(self.actionGraph_TimeSeriesMenu)
        QtCore.QObject.connect(self.actionGraph_TimeSeriesMenu, QtCore.SIGNAL('triggered()'), self.report_timeseries)
        self.actionProjPlotTimeseries.triggered.connect(self.report_timeseries)

        self.actionGraph_ScatterMenu = QtGui.QAction(self)
        self.actionGraph_ScatterMenu.setObjectName(from_utf8("actionGraph_ScatterMenu"))
        self.actionGraph_ScatterMenu.setText(transl8("frmMain", "Scatter", None))
        self.actionGraph_ScatterMenu.setToolTip(transl8("frmMain", "Display Scatter Plot", None))
        submenuGraph.addAction(self.actionGraph_ScatterMenu)
        QtCore.QObject.connect(self.actionGraph_ScatterMenu, QtCore.SIGNAL('triggered()'), self.report_scatter)
        self.actionProjPlotScatter.triggered.connect(self.report_scatter)

        self.actionTable_VariableMenu = QtGui.QAction(self)
        self.actionTable_VariableMenu.setObjectName(from_utf8("actionTable_VariableMenu"))
        self.actionTable_VariableMenu.setText(transl8("frmMain", "Table", None))
        self.actionTable_VariableMenu.setToolTip(transl8("frmMain", "Display Table", None))
        self.menuReport.addAction(self.actionTable_VariableMenu)
        QtCore.QObject.connect(self.actionTable_VariableMenu, QtCore.SIGNAL('triggered()'), self.report_variable)
        self.actionProjTableTimeseries.triggered.connect(self.report_variable)

        self.actionStatistics_ReportMenu = QtGui.QAction(self)
        self.actionStatistics_ReportMenu.setObjectName(from_utf8("actionStatistics_ReportMenu"))
        self.actionStatistics_ReportMenu.setText(transl8("frmMain", "Statistics", None))
        self.actionStatistics_ReportMenu.setToolTip(transl8("frmMain", "Display Results Statistics", None))
        self.menuReport.addAction(self.actionStatistics_ReportMenu)
        QtCore.QObject.connect(self.actionStatistics_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_statistics)
        self.actionProjTableStatistics.triggered.connect(self.report_statistics)

        self.actionStdMapQuery.triggered.connect(self.map_query)

        self.Help_Topics_Menu = QtGui.QAction(self)
        self.Help_Topics_Menu.setObjectName(from_utf8("Help_Topics_Menu"))
        self.Help_Topics_Menu.setText(transl8("frmMain", "Help Topics", None))
        self.Help_Topics_Menu.setToolTip(transl8("frmMain", "Display Help Topics", None))
        self.menuHelp.addAction(self.Help_Topics_Menu)
        QtCore.QObject.connect(self.Help_Topics_Menu, QtCore.SIGNAL('triggered()'), self.help_topics)

        self.Help_About_Menu = QtGui.QAction(self)
        self.Help_About_Menu.setObjectName(from_utf8("Help_About_Menu"))
        self.Help_About_Menu.setText(transl8("frmMain", "About", None))
        self.Help_About_Menu.setToolTip(transl8("frmMain", "About SWMM", None))
        self.menuHelp.addAction(self.Help_About_Menu)
        QtCore.QObject.connect(self.Help_About_Menu, QtCore.SIGNAL('triggered()'), self.help_about)

        if self.map_widget:
            self.map_widget.applyLegend()
            self.map_widget.LegendDock.setVisible(False)
            self.set_thematic_controls()
            self.cboMapSubcatchments.currentIndexChanged.connect(self.update_thematic_map)
            self.cboMapNodes.currentIndexChanged.connect(self.update_thematic_map)
            self.cboMapLinks.currentIndexChanged.connect(self.update_thematic_map)
            self.signalTimeChanged.connect(self.update_thematic_map_time)

        self.cbFlowUnits.currentIndexChanged.connect(self.cbFlowUnits_currentIndexChanged)
        self.cbOffset.currentIndexChanged.connect(self.cbOffset_currentIndexChanged)
        self._animate_date = lambda: self.update_time_index("date")
        self._animate_time = lambda: self.update_time_index("time")
        self._animate_datetime = lambda: self.update_time_index("datetime")
        self.cboDate.currentIndexChanged.connect(self._animate_date)
        self.cboTime.currentIndexChanged.connect(self._animate_time)
        self.sbETime.valueChanged.connect(self._animate_datetime)
        self.txtETime.setReadOnly(True)
        self.lblETime.setText('Elapsed Time')
        self.lblAnimateTime.setText('Time of Day')
        self.sbETime.lineEdit().setVisible(False)
        self.cboDate.setFixedWidth(100)
        self.sbETime.setFixedWidth(15)
        self.txtETime.setFixedWidth(100)

    def cbFlowUnits_currentIndexChanged(self):
        import core.swmm.options
        self.project.options.flow_units = core.swmm.options.general.FlowUnits[self.cbFlowUnits.currentText()[12:]]
        self.project.metric = self.project.options.flow_units in core.swmm.options.general.flow_units_metric

    def cbOffset_currentIndexChanged(self):
        import core.swmm.options
        self.project.options.link_offsets = core.swmm.options.general.LinkOffsets[self.cbOffset.currentText()[9:].upper()]

    def set_thematic_controls(self):
        self.allow_thematic_update = False
        self.cboMapSubcatchments.clear()
        self.cboMapSubcatchments.addItems(['None', 'Area', 'Width', '% Slope', '% Imperv', 'LID Controls'])
        self.cboMapNodes.clear()
        self.cboMapNodes.addItems(['None', 'Invert El.'])
        self.cboMapLinks.clear()
        self.cboMapLinks.addItems(['None', 'Max. Depth', 'Roughness', 'Slope'])
        if self.get_output():
            # Add object type labels to map combos if there are any of each type in output
            for attribute in SMO.SwmmOutputSubcatchment.attributes:
                self.cboMapSubcatchments.addItem(attribute.name)
            for attribute in SMO.SwmmOutputNode.attributes:
                self.cboMapNodes.addItem(attribute.name)
            for attribute in SMO.SwmmOutputLink.attributes:
                self.cboMapLinks.addItem(attribute.name)
            self.horizontalTimeSlider.setMaximum(self.output.num_periods - 1)
        self.allow_thematic_update = True
        self.update_thematic_map()

    def get_model_attributes(self, an_obj_type):
        """
        Get model object's attributes or parameter values
        Args:
            an_obj_type: "Subcatchments", "Nodes", "Links"
        Returns:
            color_by, a dictionary of object name and its parameter/attribute value
        """
        selected_attribute = ""
        setting_index = -1
        attribute_index_m = -1
        model_sections = None
        if an_obj_type:
            color_by = {}
            if "subcatchment" in an_obj_type.lower():
                selected_attribute = self.cboMapSubcatchments.currentText()
                if selected_attribute == "None":
                    return None
                setting_index = self.cboMapSubcatchments.currentIndex()
                attribute_index_m = 5
                model_sections = [self.project.subcatchments]
                color_by[model_sections[0].SECTION_NAME] = {}
            elif "node" in an_obj_type.lower():
                selected_attribute = self.cboMapNodes.currentText()
                if selected_attribute == "None":
                    return None
                setting_index = self.cboMapNodes.currentIndex()
                attribute_index_m = 1
                model_sections = self.project.nodes_groups()
                for sect in self.project.nodes_groups():
                    color_by[sect.SECTION_NAME] = {}
            elif "link" in an_obj_type.lower():
                selected_attribute = self.cboMapLinks.currentText()
                if selected_attribute == "None":
                    return None
                setting_index = self.cboMapLinks.currentIndex()
                attribute_index_m = 3
                model_sections = self.project.links_groups()
                for sect in self.project.links_groups():
                    color_by[sect.SECTION_NAME] = {}
            else:
                return None

            # not a parameter or an attribute
            if setting_index > attribute_index_m:
                return None

            for sect in model_sections:
                if sect.value:
                    for mobj in sect.value:
                        for md in mobj.metadata:
                            if md.label == selected_attribute:
                                color_by[sect.SECTION_NAME][mobj.name] = float(mobj.__dict__[md.attribute])
                                break
            return color_by
        else:
            return None

    def update_time_index(self, aChange):
        if aChange == "date":
            dt = self.animation_dates[self.cboDate.currentIndex()]
            # time_lbl = '{:02d}:{:02d}:{:02d}'.format(dt.hour, dt.minute, dt.second)
            time_lbl = "00:00:00"

            in_range = False
            for i in range(1, self.output.num_periods):
                # hr_min_str = self.output.get_time_string(i)
                # time_labels.append(hr_min_str)
                dt_temp = self.output.get_time(i)
                if str(dt.date()) == str(dt_temp.date()) and \
                    '{:02d}:{:02d}:{:02d}'.format(dt_temp.hour,
                                                  dt_temp.minute,
                                                  dt_temp.second) == time_lbl:
                    self.time_index = i - 1
                    in_range = True
                    break

            if in_range:
                self.cboTime.currentIndexChanged.disconnect(self._animate_time)
                self.cboTime.setCurrentIndex(self.cboTime.findText(time_lbl))
                self.cboTime.currentIndexChanged.connect(self._animate_time)
                self.txtETime.setText(str(self.cboDate.currentIndex()) + "." + time_lbl)

                self.sbETime.valueChanged.disconnect(self._animate_datetime)
                self.sbETime.setValue(self.time_index)
                self.sbETime.valueChanged.connect(self._animate_datetime)

                self.horizontalTimeSlider.valueChanged.disconnect(self.currentTimeChanged)
                self.horizontalTimeSlider.setValue(self.time_index)
                self.horizontalTimeSlider.valueChanged.connect(self.currentTimeChanged)

                self.update_thematic_map()
            pass
        elif aChange == "time":
            dt = self.animation_dates[self.cboDate.currentIndex()]
            time_dt = self.animation_time_of_day[self.cboTime.currentIndex()]
            # dt_act = dt + time_dt
            hrs, rest = divmod(time_dt.seconds, 3600)
            mins, secs = divmod(rest, 60)
            time_lbl = '{:02d}:{:02d}:{:02d}'.format(hrs, mins, secs)

            in_range = False
            for i in range(1, self.output.num_periods):
                # hr_min_str = self.output.get_time_string(i)
                # time_labels.append(hr_min_str)
                dt_temp = self.output.get_time(i)
                if str(dt.date()) == str(dt_temp.date()) and \
                    '{:02d}:{:02d}:{:02d}'.format(dt_temp.hour,
                                                  dt_temp.minute,
                                                  dt_temp.second) == time_lbl:
                    self.time_index = i
                    in_range = True
                    break

            if in_range:
                self.sbETime.valueChanged.disconnect(self._animate_datetime)
                self.sbETime.setValue(self.time_index)
                self.sbETime.valueChanged.connect(self._animate_datetime)

                self.txtETime.setText(str(self.cboDate.currentIndex()) + "." + time_lbl)

                self.horizontalTimeSlider.valueChanged.disconnect(self.currentTimeChanged)
                self.horizontalTimeSlider.setValue(self.time_index)
                self.horizontalTimeSlider.valueChanged.connect(self.currentTimeChanged)

                self.update_thematic_map()
            pass
        elif aChange == "datetime":
            if self.sbETime.value() >= self.output.num_periods:
                self.sbETime.setValue(self.output.num_periods - 1)
            elif self.sbETime.value() < 1:
                self.sbETime.setValue(1)
            else:
                self.time_index = self.sbETime.value()
                self.horizontalTimeSlider.valueChanged.disconnect(self.currentTimeChanged)
                self.horizontalTimeSlider.setValue(self.time_index)
                self.horizontalTimeSlider.valueChanged.connect(self.currentTimeChanged)
                dt = self.output.get_time(self.time_index)
                day_ctr = self.cboDate.findText(str(dt.date()))
                self.cboDate.currentIndexChanged.disconnect(self._animate_date)
                self.cboDate.setCurrentIndex(self.cboDate.findText(str(dt.date())))
                self.cboDate.currentIndexChanged.connect(self._animate_date)
                time_lbl = '{:02d}:{:02d}:{:02d}'.format(dt.hour, dt.minute, dt.second)
                self.cboTime.currentIndexChanged.disconnect(self._animate_time)
                self.cboTime.setCurrentIndex(self.cboTime.findText(time_lbl))
                self.cboTime.currentIndexChanged.connect(self._animate_time)
                self.txtETime.setText(str(day_ctr) + "." + time_lbl)
                self.update_thematic_map()

    def update_thematic_map(self):
        if not self.allow_thematic_update or not self.map_widget:
            return

        enable_time_widget = False  # Flag to set if any selected attributes are time-based
        try:

            # color_by = self.get_model_attributes("Subcatchments")
            # color_by = self.get_model_attributes("Nodes")
            # color_by = self.get_model_attributes("Links")

            if self.model_layers.subcatchments and self.model_layers.subcatchments.isValid():
                selected_attribute = self.cboMapSubcatchments.currentText()
                attribute = None
                setting_index = self.cboMapSubcatchments.currentIndex()
                if setting_index < 6:
                    meta_item = Subcatchment.metadata.meta_item_of_label(selected_attribute)
                    attribute = meta_item.attribute
                    color_by = {}
                    self.thematic_subcatchment_min = None
                    self.thematic_subcatchment_max = None
                    if attribute:  # Found an attribute of the subcatchment class to color by
                        for subcatchment in self.project.subcatchments.value:
                            value = float(getattr(subcatchment, attribute, 0))
                            color_by[subcatchment.name] = value
                            if self.thematic_subcatchment_min is None or value < self.thematic_subcatchment_min:
                                self.thematic_subcatchment_min = value
                            if self.thematic_subcatchment_max is None or value > self.thematic_subcatchment_max:
                                self.thematic_subcatchment_max = value

                elif self.output:  # Look for attribute to color by in the output
                    attribute = SMO.SwmmOutputSubcatchment.get_attribute_by_name(selected_attribute)
                    if attribute:
                        enable_time_widget = True
                        # find min and max values over entire run
                        for time_increment in range(0, self.output.num_periods-1):
                            values = SMO.SwmmOutputSubcatchment.get_attribute_for_all_at_time(self.output, attribute, time_increment)
                            for value in values:
                                if self.thematic_subcatchment_min is None or value < self.thematic_subcatchment_min:
                                    self.thematic_subcatchment_min = value
                                if self.thematic_subcatchment_max is None or value > self.thematic_subcatchment_max:
                                    self.thematic_subcatchment_max = value
                # if color_by:
                #     self.map_widget.applyGraduatedSymbologyStandardMode(self.model_layers.subcatchments, color_by,
                #                                                         self.thematic_subcatchment_min,
                #                                                         self.thematic_subcatchment_max)
                # else:
                #     self.map_widget.set_default_polygon_renderer(self.model_layers.subcatchments)
                # self.model_layers.subcatchments.triggerRepaint()

            if self.model_layers.nodes_layers:
                selected_attribute = self.cboMapNodes.currentText()
                attribute = None
                setting_index = self.cboMapNodes.currentIndex()
                if setting_index < 2:
                    meta_item = Junction.metadata.meta_item_of_label(selected_attribute)
                    attribute = meta_item.attribute
                    color_by = {}
                    self.thematic_node_min = None
                    self.thematic_node_max = None
                    if attribute:  # Found an attribute of the node class to color by
                        for item in self.project.all_nodes():
                            value = float(getattr(item, attribute, 0))
                            color_by[item.name] = value
                            if self.thematic_node_min is None or value < self.thematic_node_min:
                                self.thematic_node_min = value
                            if self.thematic_node_max is None or value > self.thematic_node_max:
                                self.thematic_node_max = value

                elif self.output:  # Look for attribute to color by in the output
                    attribute = SMO.SwmmOutputNode.get_attribute_by_name(selected_attribute)
                    if attribute:
                        enable_time_widget = True
                        # find min and max values over entire run
                        for time_increment in range(0, self.output.num_periods-1):
                            values = SMO.SwmmOutputNode.get_attribute_for_all_at_time(self.output, attribute, time_increment)
                            for value in values:
                                if self.thematic_node_min is None or value < self.thematic_node_min:
                                    self.thematic_node_min = value
                                if self.thematic_node_max is None or value > self.thematic_node_max:
                                    self.thematic_node_max = value

                # for layer in self.model_layers.nodes_layers:
                #     if layer.isValid():
                #         if color_by:
                #             self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                #                                                                 self.thematic_node_min,
                #                                                                 self.thematic_node_max)
                #         else:
                #             self.map_widget.set_default_point_renderer(layer)
                #         layer.triggerRepaint()

            if self.model_layers.links_layers:
                selected_attribute = self.cboMapLinks.currentText()
                attribute = None
                setting_index = self.cboMapLinks.currentIndex()
                if setting_index < 3:
                    meta_item = Conduit.metadata.meta_item_of_label(selected_attribute)
                    attribute = meta_item.attribute
                if setting_index == 3:
                    # special case for slope
                    attribute = 'slope'
                color_by = {}
                self.thematic_link_min = None
                self.thematic_link_max = None
                if attribute:  # Found an attribute of the conduit class to color by
                    for link in self.project.all_links():
                        try:
                            if attribute == 'max_depth':
                                for value in self.project.xsections.value:
                                    if value.link == link.name:
                                        color_by[link.name] = float(value.geometry1)
                            elif attribute == 'slope':
                                # calculate slope
                                try:
                                    start_elev = float(self.project.all_nodes()[link.inlet_node].elevation)
                                except Exception as start_elev_ex:
                                    print("Exception finding conduit start elevation, using 0: " + str(start_elev_ex))
                                    start_elev = 0.0
                                try:
                                    end_elev = float(self.project.all_nodes()[link.outlet_node].elevation)
                                except Exception as end_elev_ex:
                                    print("Exception finding conduit end elevation, using 0: " + str(end_elev_ex))
                                    end_elev = 0.0
                                if link.length > 0.0:
                                    slope = abs((float(start_elev) - float(end_elev)) / float(link.length))
                                else:
                                    slope = 0.0
                                color_by[link.name] = float(slope)
                            else:
                                color_by[link.name] = float(getattr(link, attribute, 0))
                            if self.thematic_link_min is None or color_by[link.name] < self.thematic_link_min:
                                self.thematic_link_min = color_by[link.name]
                            if self.thematic_link_max is None or color_by[link.name] > self.thematic_link_max:
                                self.thematic_link_max = color_by[link.name]
                        except Exception as exLinkAtt:
                            print("update_thematic_map: link attribute: " + link.name + ': ' + str(exLinkAtt))

                elif self.output:  # Look for attribute to color by in the output
                    attribute = SMO.SwmmOutputLink.get_attribute_by_name(selected_attribute)
                    if attribute:
                        enable_time_widget = True
                        # find min and max values over entire run
                        for time_increment in range(0, self.output.num_periods-1):
                            values = SMO.SwmmOutputLink.get_attribute_for_all_at_time(self.output, attribute, time_increment)
                            for value in values:
                                if self.thematic_link_min is None or value < self.thematic_link_min:
                                    self.thematic_link_min = value
                                if self.thematic_link_max is None or value > self.thematic_link_max:
                                    self.thematic_link_max = value

                # for layer in self.model_layers.links_layers:
                #     if layer.isValid():
                #         if color_by:
                #             self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                #                                                                 self.thematic_link_min,
                #                                                                 self.thematic_link_max)
                #         else:
                #             self.map_widget.set_default_line_renderer(layer)
                #         layer.triggerRepaint()

        except Exception as exBig:
            print("Exception in update_thematic_map: " + str(exBig))

        self.time_widget.setVisible(enable_time_widget)
        if enable_time_widget:
            self.update_thematic_map_time()

    def update_thematic_map_time(self):
        """
            Update thematic map for the current self.time_index.
            Depends on update_thematic_map having been called since last change to thematic map options.
        """
        try:
            if not self.allow_thematic_update or not self.map_widget:
                return

            if self.model_layers.subcatchments and self.model_layers.subcatchments.isValid():
                layer = self.model_layers.subcatchments
                selected_attribute = self.cboMapSubcatchments.currentText()
                setting_index = self.cboMapSubcatchments.currentIndex()
                color_by = {}
                if setting_index >= 6 and self.output:  # Look for attribute to color by in the output
                    attribute = SMO.SwmmOutputSubcatchment.get_attribute_by_name(selected_attribute)
                    if attribute:
                        enable_time_widget = False
                        values = SMO.SwmmOutputSubcatchment.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                        index = 0
                        for subcatchment in self.output.subcatchments.values():
                            color_by[subcatchment.name] = values[index]
                            index += 1
                if color_by:
                    if self.map_widget.layer_styles.has_key(layer.id()) and \
                            self.map_widget.validatedGraduatedSymbol(None,
                                                                     self.map_widget.layer_styles[layer.id()]):
                        self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                            self.thematic_node_min,
                                                                            self.thematic_node_max,
                                                                            self.map_widget.layer_styles[
                                                                                layer.id()])
                    else:
                        self.map_widget.applyGraduatedSymbologyStandardMode(self.model_layers.subcatchments, color_by,
                                                                            self.thematic_subcatchment_min,
                                                                            self.thematic_subcatchment_max)
                    self.annotate_layername(selected_attribute, "subcatchment", layer)
                    #self.map_widget.LegendDock.setVisible(True)
                else:
                    do_label = True
                    self.map_widget.set_default_polygon_renderer(layer, "lightgreen" , do_label)

                self.model_layers.subcatchments.triggerRepaint()

            if self.model_layers.nodes_layers:
                selected_attribute = self.cboMapNodes.currentText()
                setting_index = self.cboMapNodes.currentIndex()
                color_by = {}
                if setting_index >= 2 and self.output:  # Look for attribute to color by in the output
                    attribute = SMO.SwmmOutputNode.get_attribute_by_name(selected_attribute)
                    if attribute:
                        # set values to color by at current time index
                        values = SMO.SwmmOutputNode.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                        index = 0
                        for node in self.output.nodes.values():
                            color_by[node.name] = values[index]
                            index += 1

                for layer in self.model_layers.nodes_layers:
                    if layer.isValid():
                        if color_by:
                            if self.map_widget.layer_styles.has_key(layer.id()) and \
                                    self.map_widget.validatedGraduatedSymbol(None,
                                                                             self.map_widget.layer_styles[layer.id()]):
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                    self.thematic_node_min,
                                                                                    self.thematic_node_max,
                                                                                    self.map_widget.layer_styles[
                                                                                        layer.id()])
                            else:
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                    self.thematic_node_min,
                                                                                    self.thematic_node_max)
                            self.annotate_layername(selected_attribute, "node", layer)
                        else:
                            do_label = True
                            if len(self.project.all_nodes()) > 300:
                                do_label = False
                            self.map_widget.set_default_point_renderer(layer, None, 3.5, do_label)

                        layer.triggerRepaint()

            if self.model_layers.links_layers:
                selected_attribute = self.cboMapLinks.currentText()
                setting_index = self.cboMapLinks.currentIndex()
                color_by = {}
                if setting_index > 3 and self.output:  # Look for attribute to color by in the output
                    attribute = SMO.SwmmOutputLink.get_attribute_by_name(selected_attribute)
                    if attribute:
                        values = SMO.SwmmOutputLink.get_attribute_for_all_at_time(self.output, attribute, self.time_index)
                        index = 0
                        for link in self.output.links.values():
                            color_by[link.name] = values[index]
                            index += 1

                color_by_flow = None
                if selected_attribute and selected_attribute.lower() == "flow":
                    color_by_flow = color_by
                elif self.chkDisplayFlowDir.isChecked():
                    color_by_flow = {}
                    selected_attribute = "Flow"
                    attribute = SMO.SwmmOutputLink.get_attribute_by_name(selected_attribute)
                    if attribute:
                        values = SMO.SwmmOutputLink.get_attribute_for_all_at_time(self.output, attribute,
                                                                                 self.time_index)
                        # index = 1
                        for link in self.output.links.values():
                            color_by_flow[link.name] = values[link.index]
                            # index += 1

                for layer in self.model_layers.links_layers:
                    if layer.isValid():
                        if color_by:
                            if self.map_widget.layer_styles.has_key(layer.id()) and \
                                self.map_widget.validatedGraduatedSymbol(None,self.map_widget.layer_styles[layer.id()]):
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                    self.thematic_link_min,
                                                                                    self.thematic_link_max,
                                                                             self.map_widget.layer_styles[layer.id()],
                                                                                    self.chkDisplayFlowDir.isChecked(),
                                                                                    color_by_flow)
                            else:
                                self.map_widget.applyGraduatedSymbologyStandardMode(layer, color_by,
                                                                                self.thematic_link_min,
                                                                                self.thematic_link_max,
                                                                                    None,
                                                                                    self.chkDisplayFlowDir.isChecked(),
                                                                                    color_by_flow)
                            self.annotate_layername(selected_attribute, "link", layer)
                        else:
                            do_label = True
                            if len(self.project.all_links()) > 300:
                                do_label = False
                            self.map_widget.set_default_line_renderer(layer, do_label)
                        layer.triggerRepaint()

            if self.update_time_controls and self.output and self.horizontalTimeSlider.maximum() > 0:
                if self.time_index >= 0 and self.time_index < self.horizontalTimeSlider.maximum():
                    dt = self.output.get_time(self.time_index)
                    dt_str = str(dt.date())
                    self.cboDate.currentIndexChanged.disconnect(self._animate_date)
                    self.cboTime.currentIndexChanged.disconnect(self._animate_time)
                    self.sbETime.valueChanged.disconnect(self._animate_datetime)
                    self.cboDate.setCurrentIndex(self.cboDate.findText(dt_str))
                    time_lbl = '{:02d}:{:02d}:{:02d}'.format(dt.hour, dt.minute, dt.second)
                    self.cboTime.setCurrentIndex(self.cboTime.findText(time_lbl))
                    self.sbETime.setValue(self.time_index)
                    self.txtETime.setText(str(self.cboDate.currentIndex()) + "." + time_lbl)
                    # self.cboTime.connect(self.cboTime, "currentIndexChanged()", self.update_thematic_map_time)
                    self.cboDate.currentIndexChanged.connect(self._animate_date)
                    self.cboTime.currentIndexChanged.connect(self._animate_time)
                    self.sbETime.valueChanged.connect(self._animate_datetime)
                    pass
                self.update_time_controls = False
        except Exception as exBig:
            print("Exception in update_thematic_map_time: " + str(exBig))

    def annotate_layername(self, selected_attribute, obj_type, layer):
        """
        Append attribute and its unit to layer name in legend
        Args:
            selected_attribute: node/link attribute name
            obj_type: either 'node' or 'link'
            layer: map layer to be applied with graduated symbols
        Returns: None
        """
        unit_text = ""
        if obj_type == "subcatchment":
            if self.output.subcatchments_units.has_key(selected_attribute):
                unit_text = self.output.subcatchments_units[selected_attribute]
            else:
                if selected_attribute == "Elevation":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "ft"
                elif selected_attribute == "Base Demand":
                    unit_text = self.output.links_units["Flow"]
                elif selected_attribute == "Initial Quality":
                    unit_text = self.output.links_units["Quality"]
        elif obj_type == "node":
            if self.output.nodes_units.has_key(selected_attribute):
                unit_text = self.output.nodes_units[selected_attribute]
            else:
                if selected_attribute == "Elevation":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "ft"
                elif selected_attribute == "Base Demand":
                    unit_text = self.output.links_units["Flow"]
                elif selected_attribute == "Initial Quality":
                    unit_text = self.output.links_units["Quality"]
        elif obj_type == "link":
            if self.output.links_units.has_key(selected_attribute):
                unit_text = self.output.links_units[selected_attribute]
            else:
                if selected_attribute == "Length":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "ft"
                elif selected_attribute == "Diameter":
                    if self.output.unit_system:
                        unit_text = "m"
                    else:
                        unit_text = "in"

        layer_name = layer.name()
        if " [" in layer_name:
            layer_name = layer_name[0:layer_name.index(" [")]
        if unit_text:
            layer.setLayerName(layer_name + " [" + selected_attribute + ", " + unit_text + "]")
        else:
            layer.setLayerName(layer_name + " [" + selected_attribute + "]")

    def animate_e(self):
        if self.output:
            for self.time_index in range(1, self.output.num_periods):
                self.horizontalTimeSlider.setSliderPosition(self.time_index)
                sleep(2)

    def animate_e_step(self, i):
        if self.output:
            if i >= 0 and i <= self.output.num_periods:
                self.horizontalTimeSlider.setSliderPosition(i)

    def get_output(self):
        if not self.output:
            if os.path.isfile(self.output_filename):
                self.output = SMO.SwmmOutputObject(self.output_filename)
                self.horizontalTimeSlider.setMaximum(self.output.num_periods - 1)
        return self.output

    def report_status(self):
        print "report_status"
        if not os.path.isfile(self.status_file_name):
            prefix, extension = os.path.splitext(self.project.file_name)
            if os.path.isfile(prefix + self.status_suffix):
                self.status_file_name = prefix + self.status_suffix
        if os.path.isfile(self.status_file_name):
            webbrowser.open_new_tab(self.status_file_name)
        else:
            QMessageBox.information(None, self.model,
                                    "Model status not found.\n"
                                    "Run the model to generate model status.",
                                    QMessageBox.Ok)

    def report_profile(self):
        if self.get_output():
            self._frmProfilePlot = frmProfilePlot(self)
            self._frmProfilePlot.set_from(self.project, self.output) #self.get_output())
            self._frmProfilePlot.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_timeseries(self):
        if self.get_output():
            self._frmTimeSeriesPlot = frmTimeSeriesPlot(self)
            self._frmTimeSeriesPlot.set_from(self.project, self.output) #self.get_output())
            self._frmTimeSeriesPlot.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_scatter(self):
        if self.get_output():
            self._frmScatterPlot = frmScatterPlot(self)
            self._frmScatterPlot.set_from(self.project, self.get_output())
            self._frmScatterPlot.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_variable(self):
        if self.get_output():
            self._frmTableSelection = frmTableSelection(self)
            self._frmTableSelection.set_from(self.project, self.get_output())
            self._frmTableSelection.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_statistics(self):
        if self.get_output():
            self._frmStatisticsReportSelection = frmStatisticsReportSelection(self)
            self._frmStatisticsReportSelection.set_from(self.project, self.output)
            self._frmStatisticsReportSelection.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model output not found.\n"
                                    "Run the model to generate output.",
                                    QMessageBox.Ok)

    def report_summary(self):
        if not os.path.isfile(self.status_file_name):
            prefix, extension = os.path.splitext(self.project.file_name)
            if os.path.isfile(prefix + self.status_suffix):
                self.status_file_name = prefix + self.status_suffix
        if os.path.isfile(self.status_file_name):
            self._frmSummaryReport = frmSummaryReport(self)
            self._frmSummaryReport.set_from(self.project, self.status_file_name)
            self._frmSummaryReport.show()
        else:
            QMessageBox.information(None, self.model,
                                    "Model status not found.\n"
                                    "Run the model to generate model status.",
                                    QMessageBox.Ok)

    def calibration_data(self):
        self._frmCalibrationData = frmCalibrationData(self)
        self._frmCalibrationData.show()
        pass

    def edit_defaults(self):
        directory = self.program_settings.value("ProjectDir", "")
        qsettings = self.project_settings
        if qsettings is None:
            qsettings = self.program_settings
        from frmDefaultsEditor import frmDefaultsEditor
        fd = frmDefaultsEditor(self, self.project, qsettings)
        fd.show()

    def map_query(self):
        from ui.SWMM.frmQuery import frmQuery
        frmQ = frmQuery(self, self.project)
        frmQ.show()

    def map_overview(self):
        layerset = []
        layerset.append(self.model_layers.subcatchments.id())
        layerset.append(self.model_layers.sublinks.id())
        layerset.append(self.model_layers.conduits.id())
        layerset.append(self.model_layers.pumps.id())
        layerset.append(self.model_layers.orifices.id())
        layerset.append(self.model_layers.weirs.id())
        layerset.append(self.model_layers.outlets.id())
        self.map_widget.create_overview(layerset)
        pass

    def get_editor(self, edit_name):
        frm = None
        # First handle special cases where forms need more than simply being created

        new_item = None
        if edit_name == self.tree_quality_Pollutants[0]:
            edit_these = []
            if self.project and self.project.pollutants:
                if not isinstance(self.project.pollutants.value, basestring):
                    if isinstance(self.project.pollutants.value, list):
                        edit_these.extend(self.project.pollutants.value)
                if len(edit_these) == 0:
                    new_item = Pollutant()
                    new_item.name = self.new_item_name(Pollutant)
                    edit_these.append(new_item)
            frm = frmGenericPropertyEditor(self, self.project.pollutants, edit_these, new_item, "SWMM Pollutant Editor")
            frm.helper = HelpHandler(frm)
            frm.help_topic = "swmm/src/src/pollutanteditordialog.htm"
        elif edit_name == self.tree_MapLabels[0]:
            edit_these = []
            if self.project and self.project.labels:
                if not isinstance(self.project.labels.value, basestring):
                    if isinstance(self.project.labels.value, list):
                        edit_these.extend(self.project.labels.value)
                if len(edit_these) == 0:
                    new_item = Label()
                    new_item.name = self.new_item_name(Label)
                    edit_these.append(new_item)
            frm = frmGenericPropertyEditor(self, self.project.labels, edit_these, new_item, "SWMM Map Label Editor")
            frm.helper = HelpHandler(frm)
            frm.help_topic = "swmm/src/src/maplabeleditordialog.htm"
        elif edit_name in [item[0] for item in self.tree_items_using_name]:
            # in these cases the click on the tree diagram populates the lower left list, not directly to an editor
            return None
        elif edit_name == self.tree_links_Orifices[0] and len(self.project.orifices.value) == 0:
            return None
        elif edit_name == self.tree_links_Outlets[0] and len(self.project.outlets.value) == 0:
            return None
        elif edit_name == self.tree_links_Weirs[0] and len(self.project.weirs.value) == 0:
            return None
        elif edit_name == self.tree_links_Pumps[0] and len(self.project.pumps.value) == 0:
            return None
        elif edit_name == self.tree_nodes_Outfalls[0] and len(self.project.outfalls.value) == 0:
            return None
        elif edit_name == self.tree_nodes_Dividers[0] and len(self.project.dividers.value) == 0:
            return None
        elif edit_name == self.tree_nodes_StorageUnits[0] and len(self.project.storage.value) == 0:
            return None
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)
        return frm

    def get_object_list(self, category):
        ids = []
        if category == self.tree_curves_ControlCurves[0]:
            for curve in self.project.curves.value:
                if curve.curve_type == CurveType.CONTROL:
                    ids.append(curve.name)
        elif category == self.tree_curves_DiversionCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.DIVERSION:
                    ids.append(self.project.curves.value[i].name)
        elif category == self.tree_curves_PumpCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                curve_type = self.project.curves.value[i].curve_type
                if curve_type == CurveType.PUMP1 or curve_type == CurveType.PUMP2 or \
                    curve_type == CurveType.PUMP3 or curve_type == CurveType.PUMP4:
                    ids.append(self.project.curves.value[i].name)
        elif category == self.tree_curves_RatingCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.RATING:
                    ids.append(self.project.curves.value[i].name)
        elif category == self.tree_curves_ShapeCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.SHAPE:
                    ids.append(self.project.curves.value[i].name)
        elif category == self.tree_curves_StorageCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.STORAGE:
                    ids.append(self.project.curves.value[i].name)
        elif category == self.tree_curves_TidalCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.TIDAL:
                    ids.append(self.project.curves.value[i].name)
        elif category == self.tree_MapLabels[0]:
            for i in range(0, len(self.project.labels.value)):
                ids.append(self.project.labels.value[i].name)
        elif category == self.tree_nodes_StorageUnits[0]:
            for i in range(0, len(self.project.storage.value)):
                ids.append(self.project.storage.value[i].name)
        else:
            section = self.project.find_section(category)
            if section and isinstance(section.value, list):
                ids = [item.name for item in section.value]
            else:
                ids = None
        return ids

    def add_object(self, tree_text):
        item_type = self.tree_types[tree_text]
        new_item = item_type()
        new_item.name = self.new_item_name(item_type)
        if tree_text == self.tree_links_Orifices[0]:
            # need to add corresponding cross section
            new_xsection = CrossSection()
            new_xsection.name = new_item.name
            if self.project_settings:
                self.project_settings.apply_default_attributes(new_xsection)
            if len(self.project.xsections.value) == 0:
                edit_these = [new_xsection]
                self.project.xsections.value = edit_these
            else:
                self.project.xsections.value.append(new_xsection)
        elif tree_text == self.tree_curves_ControlCurves[0]:
            new_item.curve_type = CurveType.CONTROL
        elif tree_text == self.tree_curves_DiversionCurves[0]:
            new_item.curve_type = CurveType.DIVERSION
        elif tree_text == self.tree_curves_PumpCurves[0]:
            new_item.curve_type = CurveType.PUMP1
        elif tree_text == self.tree_curves_RatingCurves[0]:
            new_item.curve_type = CurveType.RATING
        elif tree_text == self.tree_curves_ShapeCurves[0]:
            new_item.curve_type = CurveType.SHAPE
        elif tree_text == self.tree_curves_StorageCurves[0]:
            new_item.curve_type = CurveType.STORAGE
        elif tree_text == self.tree_curves_TidalCurves[0]:
            new_item.curve_type = CurveType.TIDAL

        if self.project_settings:
            self.project_settings.apply_default_attributes(new_item)
        self.show_edit_window(self.make_editor_from_tree(self.tree_section, self.tree_top_items, [], new_item))

    def delete_named_object(self, tree_text, item_name):
        item_type = self.tree_types[tree_text]
        section_field_name = self.section_types[item_type]

        if hasattr(self.project, section_field_name):
            section = getattr(self.project, section_field_name)
        else:
            raise Exception("Section not found in project: " + section_field_name)
        item = section.value[item_name]
        self.delete_item(item)

        # if section_name == self.tree_curves_ControlCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and value.curve_type == CurveType.CONTROL:
        #             self.project.curves.value.remove(value)
        # elif section_name == self.tree_curves_DiversionCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and value.curve_type == CurveType.DIVERSION:
        #             self.project.curves.value.remove(value)
        # elif section_name == self.tree_curves_PumpCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and \
        #                 (value.curve_type == CurveType.PUMP1 or value.curve_type == CurveType.PUMP2
        #                  or value.curve_type == CurveType.PUMP3 or value.curve_type == CurveType.PUMP4):
        #             self.project.curves.value.remove(value)
        # elif section_name == self.tree_curves_RatingCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and value.curve_type == CurveType.RATING:
        #             self.project.curves.value.remove(value)
        # elif section_name == self.tree_curves_ShapeCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and value.curve_type == CurveType.SHAPE:
        #             self.project.curves.value.remove(value)
        # elif section_name == self.tree_curves_StorageCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and value.curve_type == CurveType.STORAGE:
        #             self.project.curves.value.remove(value)
        # elif section_name == self.tree_curves_TidalCurves[0]:
        #     for value in self.project.curves.value:
        #         if value.name == item_name and value.curve_type == CurveType.TIDAL:
        #             self.project.curves.value.remove(value)

    def run_simulation(self):
        self.output = None
        # First find input file to run
        use_existing = self.project and self.project.file_name and os.path.exists(self.project.file_name)
        if use_existing:
            filename, file_extension = os.path.splitext(self.project.file_name)
            ts = QtCore.QTime.currentTime().toString().replace(":", "_")
            if not os.path.exists(self.project.file_name_temporary):
                self.project.file_name_temporary = filename + "_trial_" + ts + file_extension
            self.save_project(self.project.file_name_temporary)
            # TODO: decide whether to automatically save to temp location as previous version did.
        elif self.project.subcatchments.value or self.project.raingages.value or self.project.all_nodes():
            # unsaved changes to a new project have been made, prompt to save
            if self.save_project_as():
                use_existing = True
            else:
                return None
        else:
            self.open_project()

        file_name = ''
        if self.project:
            file_name = self.project.file_name_temporary

        if os.path.exists(file_name):
            prefix, extension = os.path.splitext(file_name)
            self.status_file_name = prefix + self.status_suffix
            self.output_filename = prefix + '.out'
            os.chdir(os.path.split(prefix)[0])
            if self.output:
                self.output.close()
                self.output = None
            if not os.path.exists(self.model_path):
                if 'darwin' in sys.platform:
                    lib_name = 'libswmm.dylib'
                elif 'win' in sys.platform:
                    lib_name = 'swmm5_x64.dll'
                else:  # Linux
                    lib_name = 'libswmm_amd64.so'
                self.model_path = self.find_external(lib_name)

            if os.path.exists(self.model_path):
                print('Model Path ' + self.model_path + '\n')
                try:
                    from Externals.swmm.model.swmm5 import pyswmm
                    model_api = pyswmm(file_name, self.status_file_name, self.output_filename, self.model_path)
                    frmRun = frmRunSWMM(model_api, self.project, self)
                    self._forms.append(frmRun)
                    if not use_existing:
                        # Read this project so we can refer to it while running
                        frmRun.progressBar.setVisible(False)
                        frmRun.lblTime.setVisible(False)
                        frmRun.fraTime.setVisible(False)
                        frmRun.fraBottom.setVisible(False)
                        frmRun.showNormal()
                        frmRun.set_status_text("Reading " + file_name)

                        self.project = Project()
                        self.project.read_file(file_name)
                        frmRun.project = self.project

                    frmRun.Execute()
                    # self.add_map_constituents()
                    try:
                        self.output = SMO.SwmmOutputObject(self.output_filename)
                        self.output.build_units_dictionary()
                        self.set_thematic_controls()
                        self.labelStartTime.setText('0:00')
                        if self.output:
                            # QtCore.QObject.disconnect(self.cboDate, QtCore.SIGNAL('currentIndexChanged()'), self._animate_date)
                            # QtCore.QObject.disconnect(self.cboTime, QtCore.SIGNAL('currentIndexChanged()'), self._animate_time)
                            # QtCore.QObject.disconnect(self.sbETime, QtCore.SIGNAL('valueChanged()'), self._animate_datetime)
                            self.cboDate.currentIndexChanged.disconnect(self._animate_date)
                            self.cboTime.currentIndexChanged.disconnect(self._animate_time)
                            self.sbETime.valueChanged.disconnect(self._animate_datetime)
                            self.cboDate.clear()
                            self.cboTime.clear()
                            time_labels = []
                            date_labels = []
                            self.animation_dates.clear()
                            self.animation_time_of_day.clear()
                            if timedelta(seconds=self.output.reportStep) > (self.output.EndDate - self.output.StartDate):
                                self.cboTime.addItems(["01:00:00"])
                            else:
                                td_rep_step = timedelta(seconds = self.output.reportStep)
                                if td_rep_step.days > 0:
                                    self.cboTime.addItems(["01:00:00"])
                                else:
                                    num_periods_in_day, rest = divmod(86400, self.output.reportStep)
                                    for tod_index in range(0, num_periods_in_day, 1):
                                        time_div = timedelta(seconds = self.output.reportStep * tod_index)
                                        hours, remainder = divmod(time_div.seconds, 3600)
                                        minutes, secs = divmod(remainder, 60)
                                        time_labels.append('{:02d}:{:02d}:{:02d}'.format(hours, minutes, secs))
                                        self.animation_time_of_day[tod_index] = time_div
                                    self.cboTime.addItems(time_labels)

                            hr_min_str = ""
                            dt_str = None
                            date_ctr = 0
                            for i in range(0, self.output.num_periods):
                                # hr_min_str = self.output.get_time_string(i)
                                # time_labels.append(hr_min_str)
                                dt = self.output.get_time(i)
                                if not str(dt.date()) in date_labels:
                                    date_labels.append(str(dt.date()))
                                    self.animation_dates[date_ctr] = dt
                                    date_ctr += 1

                            # qdt0 = QtCore.QDateTime.fromString(str(self.output.get_time(1)), 'yyyy-MM-dd hh:mm:ss')
                            # qdt1 = QtCore.QDateTime.fromString(str(self.output.get_time(self.output.num_periods)), 'yyyy-MM-dd hh:mm:ss')
                            # self.sbETime.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
                            # self.sbETime.setDateTimeRange(qd0, qd1)
                            # self.sbETime.setDateTime(qdt0)
                            # self.sbETime.setMinimumDateTime(qdt0)
                            # self.sbETime.setMaximumDateTime(qdt1)
                            t_str = str(self.output.get_time(0))
                            self.txtETime.setText("0." + t_str[t_str.index(" ") + 1:])
                            self.cboDate.addItems(date_labels)
                            self.sbETime.setMaximum(self.output.num_periods)
                            self.sbETime.setMinimum(0)
                            # self.labelEndTime.setText(self.project.times.duration)
                            self.cboDate.setEnabled(True)
                            self.cboTime.setEnabled(True)
                            self.sbETime.setEnabled(True)
                            self.cboDate.currentIndexChanged.connect(self._animate_date)
                            self.cboTime.currentIndexChanged.connect(self._animate_time)
                            self.sbETime.valueChanged.connect(self._animate_datetime)
                        else:
                            self.cboDate.setEnabled(False)
                            self.cboTime.setEnabled(False)
                            self.sbETime.setEnabled(False)

                        return
                    except Exception as e1:
                        print(str(e1) + '\n' + str(traceback.print_exc()))
                        QMessageBox.information(None, self.model,
                                                "Error opening model output:\n {0}\n{1}\n{2}".format(
                                                self.output_filename, str(e1), str(traceback.print_exc())),
                                                QMessageBox.Ok)
                        self.cboDate.currentIndexChanged.connect(lambda: self.update_time_index("date"))
                        self.cboTime.currentIndexChanged.connect(lambda: self.update_time_index("time"))
                        self.sbETime.valueChanged.connect(lambda: self.update_time_index("datetime"))
                    return
                except Exception as e1:
                    print(str(e1) + '\n' + str(traceback.print_exc()))
                    QMessageBox.information(None, self.model,
                                            "Error running model with library:\n {0}\n{1}\n{2}".format(
                                                self.model_path, str(e1), str(traceback.print_exc())),
                                            QMessageBox.Ok)
                finally:
                    try:
                        if model_api and model_api.isOpen():
                            model_api.ENclose()
                    except:
                        pass
                    return

            # Could not run with library, try running with executable
            args = []
            if 'darwin' in sys.platform:
                exe_name = "swmm5.app"
            elif sys.platform == "linux2":
                exe_name = "swmm5"
            else:
                exe_name = "swmm5.exe"
            exe_path = self.find_external(exe_name)
            if os.path.isfile(exe_path):
                args.append(file_name)
                args.append(self.status_file_name)
                args.append(self.output_filename)
                # running the Exe
                self.status_monitor = StatusMonitor0(exe_path, args, self, model='SWMM')
                self.status_monitor.butt.clicked.connect(self.set_thematic_controls)
                self.status_monitor.show()
            else:
                QMessageBox.information(None, self.model, self.model + " model executable not found", QMessageBox.Ok)
        else:
            QMessageBox.information(None, self.model, self.model + " input file not found", QMessageBox.Ok)

    def help_topics(self):
        self.helper.show_help()

    def help_about(self):
        self._frmAbout = frmAbout(self)
        self._frmAbout.show()
        pass

    def open_project_quiet(self, file_name):
        """ Set wait cursor during open to show operation is in progress.
            Open project from file_name using frmMain.open_project_quiet.
            Create model layers on map and set UI controls from opened project. """
        self.setWaitCursor()
        if file_name:
            self.setWindowTitle("Reading " + file_name)
        if self.map_widget:
            self.map_widget.setVisible(False)
        self.repaint()
        frmMain.open_project_quiet(self, file_name)
        ui.convenience.set_combo(self.cbFlowUnits, 'Flow Units: ' + self.project.options.flow_units.name)
        ui.convenience.set_combo(self.cbOffset, 'Offsets: ' + self.project.options.link_offsets.name)

        if self.time_widget:
            if self.project.options.dates.start_date == self.project.options.dates.end_date:
                self.labelStartTime.setText(self.project.options.dates.start_time)
                self.labelEndTime.setText(self.project.options.dates.end_time)
            else:
                self.labelStartTime.setText(self.project.options.dates.start_date)
                self.labelEndTime.setText(self.project.options.dates.end_date)
        if self.map_widget:
            try:
                self.model_layers.create_layers_from_project(self.project)
                self.map_widget.zoomfull()
                self.setQgsMapTool()  # Reset any active tool that still has state from old project
            except Exception as ex:
                print(str(ex) + '\n' + str(traceback.print_exc()))
            self.map_widget.setVisible(True)
        self.restoreCursor()

    def set_project_map_extent(self):
        """
        This routine is for backward compatibility to ensure
        [MAP] section dimension is valid, such that it can be
        displayed correctly in the original software.
        Returns:
        """
        if self.project.map and self.project.map.dimensions:
            if self.map_widget:
                rect = self.map_widget.get_extent(self.model_layers.all_layers)
                if rect:
                    x_setback = (rect.xMaximum() - rect.xMinimum()) * 5.0 / 100.0
                    y_setback = (rect.yMaximum() - rect.yMinimum()) * 5.0 / 100.0
                    self.project.map.dimensions = (rect.xMinimum() - x_setback,
                                                   rect.yMinimum() - y_setback,
                                                   rect.xMaximum() + x_setback,
                                                   rect.yMaximum() + y_setback)


class ModelLayersSWMM(ModelLayers):
    """
    Create and manage the map layers that are directly linked to SWMM model elements.
    """
    def __init__(self, map_widget):
        """Initialize empty map layers"""
        ModelLayers.__init__(self, map_widget)
        addCoordinates = self.map_widget.addCoordinates
        addLinks = self.map_widget.addLinks
        self.junctions = addCoordinates(None, "Junctions")
        self.outfalls = addCoordinates(None, "Outfalls")
        self.dividers = addCoordinates(None, "Dividers")
        self.storage = addCoordinates(None, "Storage Units")
        self.raingages = addCoordinates(None, "Rain Gages")
        self.labels = addCoordinates(None, "Map Labels")
        self.pumps = addLinks(None, None, "Pumps", QColor('red'), 1)
        self.orifices = addLinks(None, None, "Orifices", QColor('green'), 1.5)
        self.outlets = addLinks(None, None, "Outlets", QColor('pink'), 2)
        self.weirs = addLinks(None, None, "Weirs", QColor('orange'), 2.5)
        self.conduits = addLinks(None, None, "Conduits", QColor('gray'), 3.5)
        self.subcentroids = addCoordinates(None, "subcentroids")
        self.sublinks = addLinks(None, None, "sublinks", QColor('gray'), 1.0)
        self.subcatchments = self.map_widget.addPolygons(None, "Subcatchments")
        self.set_lists()

    def set_lists(self):
        """Set up lists of layers for convenient iteration"""
        self.nodes_layers = [self.junctions, self.outfalls, self.dividers, self.storage]
        self.links_layers = [self.pumps, self.orifices, self.outlets, self.weirs, self.conduits]
        self.all_layers = [self.raingages, self.labels, self.subcatchments, self.subcentroids, self.sublinks]
        self.all_layers.extend(self.nodes_layers)
        self.all_layers.extend(self.links_layers)

    def create_layers_from_project(self, project):
        """Create QGIS map layers and populate them with features representing model objects"""
        ModelLayers.create_layers_from_project(self, project)
        addCoordinates = self.map_widget.addCoordinates
        addLinks = self.map_widget.addLinks

        # Add new layers containing objects from this project
        self.junctions = addCoordinates(project.junctions.value, "Junctions")
        self.outfalls = addCoordinates(project.outfalls.value, "Outfalls")
        self.dividers = addCoordinates(project.dividers.value, "Dividers")
        self.storage = addCoordinates(project.storage.value, "Storage Units")
        self.raingages = addCoordinates(project.raingages.value, "Rain Gages")
        self.labels = addCoordinates(project.labels.value, "Map Labels")
        coordinates = project.all_nodes()
        self.pumps = addLinks(coordinates, project.pumps.value, "Pumps", QColor('red'), 1)
        self.orifices = addLinks(coordinates, project.orifices.value, "Orifices", QColor('green'), 1.5)
        self.outlets = addLinks(coordinates, project.outlets.value, "Outlets", QColor('pink'), 2)
        self.weirs = addLinks(coordinates, project.weirs.value, "Weirs", QColor('orange'), 2.5)
        self.conduits = addLinks(coordinates, project.conduits.value, "Conduits", QColor('gray'), 3.5)
        self.subcentroids = addCoordinates(None, "subcentroids")
        self.sublinks = addLinks(None, None, "sublinks", QColor('gray'), 1.0)
        self.subcatchments = self.map_widget.addPolygons(project.subcatchments.value, "Subcatchments")
        self.set_lists()
        self.create_subcatchment_links(project)
        self.create_spatial_index()

    def create_subcatchment_links(self, project):
        #create centroids
        for fs in self.subcatchments.getFeatures():
            try:
                self.create_subcatchment_centroid(fs)
            except:
                print ("Failed sub centroid: " + fs['name'])

        #create sub links
        for fs in self.subcatchments.getFeatures():
            self.create_subcatchment_link(fs)

        pass

    def create_subcatchment_centroid(self, fs):
        pt = fs.geometry().centroid().asPoint()
        #ms = self.map_widget.session.project.subcatchments.find_item(fs["name"])
        ms = None
        try:
            ms = self.map_widget.session.project.subcatchments.value[fs['name']]
        except:
            ms = None
        if ms:
            ms.centroid.x = str(pt.x())
            ms.centroid.y = str(pt.y())
        else:
            return

        # add centroid item
        c_item = None
        for obj_type, lyr_name in self.map_widget.session.section_types.iteritems():
            if lyr_name == "subcentroids":
                c_item = obj_type()
                c_item.x = str(pt.x())
                c_item.y = str(pt.y())
                break
        c_item.name = u'subcentroid-' + ms.name #self.map_widget.session.new_item_name(type(c_item))
        c_section_field_name = self.map_widget.session.section_types[type(c_item)]
        if not hasattr(self.map_widget.session.project, c_section_field_name):
            raise Exception("Section not found in project: " + c_section_field_name)
        c_section = getattr(self.map_widget.session.project, c_section_field_name)
        centroid_layer = self.map_widget.session.model_layers.layer_by_name(c_section_field_name)
        if len(c_section.value) == 0 and not isinstance(c_section, list):
            c_section.value = IndexedList([], ['name'])
        c_section.value.append(c_item)
        centroid_layer.startEditing()
        pf = self.map_widget.point_feature_from_item(ms.centroid)
        pf.setAttributes([c_item.name, 0.0, fs.id(), ms.name])
        added_centroid = centroid_layer.dataProvider().addFeatures([pf])
        if added_centroid[0]:
            self.subcatchments.startEditing()
            self.subcatchments.changeAttributeValue(fs.id(), 2, added_centroid[1][0].id())
            self.subcatchments.changeAttributeValue(fs.id(), 3, c_item.name)
            self.subcatchments.updateExtents()
            self.subcatchments.commitChanges()
            self.subcatchments.triggerRepaint()
            centroid_layer.updateExtents()
            centroid_layer.commitChanges()
            centroid_layer.triggerRepaint()

    def create_subcatchment_link(self, fs):
        sub_section = getattr(self.project, "subcatchments")
        ms = sub_section.find_item(fs["name"])
        if not ms.outlet:
            return
        fc = None
        fcs = self.map_widget.get_features_by_attribute(self.subcentroids, "sub_modelid", ms.name)
        if fcs and len(fcs) > 0:
            fc = fcs[0]
        else:
            return

        isSub2Sub = 0 #False
        # subcent_section = getattr(self.map_widget.session.project, "subcentroids")
        outlet_sub = None
        if self.project.subcatchments and self.project.subcatchments.value:
            outlet_sub = self.project.subcatchments.find_item(ms.outlet)
            if outlet_sub:
                fcs = self.map_widget.get_features_by_attribute(self.subcentroids, "sub_modelid", ms.outlet)
                if fcs and len(fcs) > 0:
                    outlet_sub = self.project.subcentroids.find_item("subcentroid-" + ms.outlet)
                    isSub2Sub = 1

        link_item = SubLink()
        link_item.name = u'sublink-' + ms.name #self.map_widget.session.new_item_name(type(link_item))
        link_item.inlet_node = fc["name"]
        if outlet_sub:
            link_item.outlet_node = outlet_sub.name
        else:
            link_item.outlet_node = ms.outlet
        inlet_sub = ms.centroid
        f = self.map_widget.line_feature_from_item(link_item,
                                                   self.map_widget.session.project.all_nodes(),
                                                   inlet_sub, outlet_sub)
        added = self.sublinks.dataProvider().addFeatures([f])
        if added[0]:
            sublink_section = getattr(self.map_widget.session.project, "sublinks")
            if len(sublink_section.value) == 0 and not isinstance(sublink_section, list):
                sublink_section.value = IndexedList([], ['name'])
            sublink_section.value.append(link_item)
            # set sublink's attributes
            self.sublinks.startEditing()
            # f.setAttributes([str(added[1][0].id()), 0.0, self.item.inlet_node, self.item.outlet_node, self.isSub2Sub])
            # self.layer.changeAttributeValue(added[1][0].id(), 0, self.item.name)
            # self.layer.changeAttributeValue(added[1][0].id(), 1, 0.0)
            self.sublinks.changeAttributeValue(added[1][0].id(), 2, fc["name"])
            self.sublinks.changeAttributeValue(added[1][0].id(), 3, link_item.outlet_node)
            self.sublinks.changeAttributeValue(added[1][0].id(), 4, isSub2Sub)
            self.sublinks.updateExtents()
            self.sublinks.commitChanges()
            self.sublinks.triggerRepaint()
            self.map_widget.canvas.refresh()
        pass

    def find_layer_by_name(self, aname):
        if not aname:
            return None
        if aname.lower().startswith("junc"):
            return self.junctions
        elif aname.lower().startswith("outfall"):
            return self.outfalls
        elif aname.lower().startswith("divide"):
            return self.dividers
        elif aname.lower().startswith("storage"):
            return self.storage
        elif aname.lower().startswith("rain"):
            return self.raingages
        elif aname.lower().startswith("pump"):
            return self.pumps
        elif aname.lower().startswith("orifice"):
            return self.orifices
        elif aname.lower().startswith("weir"):
            return self.weirs
        elif aname.lower().startswith("conduit"):
            return self.conduits
        elif aname.lower().startswith("subcatch"):
            return self.subcatchments
        elif aname.lower().startswith("map label"):
            return self.labels
        elif aname.lower().startswith("subcent"):
            return self.subcentroids
        elif aname.lower().startswith("sublink"):
            return self.sublinks
        else:
            return None

    def create_spatial_index(self):
        # Add new layers containing objects from this project
        try:
            self.junctions.dataProvider().createSpatialIndex()
            self.conduits.dataProvider().createSpatialIndex()
            self.subcatchments.dataProvider().createSpatialIndex()
            self.subcentroids.dataProvider().createSpatialIndex()
            self.sublinks.dataProvider().createSpatialIndex()
            self.outfalls.dataProvider().createSpatialIndex()
            self.dividers.dataProvider().createSpatialIndex()
            self.storage.dataProvider().createSpatialIndex()
            self.raingages.dataProvider().createSpatialIndex()
            self.labels.dataProvider().createSpatialIndex()
            self.pumps.dataProvider().createSpatialIndex()
            self.orifices.dataProvider().createSpatialIndex()
            self.outlets.dataProvider().createSpatialIndex()
            self.weirs.dataProvider().createSpatialIndex()
        except:
            pass


if __name__ == '__main__':
    print("QApplication")
    application = QtGui.QApplication(sys.argv)

    print("internationalization")
    from ui.settings import internationalization
    lang_setting = internationalization()
    lang_setting.set_language()
    if lang_setting.ui_language != "English":
        application.installTranslator(lang_setting.ui_mTranslator)

    print("frmMainSWMM")
    main_form = frmMainSWMM(application)
    print("show")
    main_form.show()
    sys.exit(application.exec_())
