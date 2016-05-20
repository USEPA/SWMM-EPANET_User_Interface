import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import webbrowser
import traceback
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QFileDialog

from ui.model_utility import QString, from_utf8, transl8, process_events, StatusMonitor0
from ui.help import HelpHandler
from ui.frmMain import frmMain
from ui.SWMM.frmDates import frmDates
from ui.SWMM.frmDynamicWave import frmDynamicWave
from ui.SWMM.frmMapBackdropOptions import frmMapBackdropOptions
from ui.SWMM.frmGeneralOptions import frmGeneralOptions
from ui.SWMM.frmInterfaceFiles import frmInterfaceFiles
from ui.SWMM.frmReportOptions import frmReportOptions
from ui.SWMM.frmTimeSteps import frmTimeSteps
from ui.SWMM.frmTitle import frmTitle

from ui.SWMM.frmAquifers import frmAquifers
from ui.SWMM.frmClimatology import frmClimatology
from ui.SWMM.frmControls import frmControls
from ui.SWMM.frmCurveEditor import frmCurveEditor
from ui.SWMM.frmPatternEditor import frmPatternEditor
from ui.SWMM.frmTimeseries import frmTimeseries
from ui.SWMM.frmJunction import frmJunction
from ui.SWMM.frmSubcatchments import frmSubcatchments
from ui.SWMM.frmLID import frmLID
from ui.SWMM.frmSnowPack import frmSnowPack
from ui.SWMM.frmUnitHydrograph import frmUnitHydrograph
from ui.SWMM.frmTransect import frmTransect
from ui.SWMM.frmCrossSection import frmCrossSection
from ui.SWMM.frmInflows import frmInflows
from ui.SWMM.frmLandUses import frmLandUses
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from ui.SWMM.frmCalibrationData import frmCalibrationData
from ui.SWMM.frmSummaryReport import frmSummaryReport

from core.swmm.project import Project
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.quality import Pollutant
from core.swmm.hydraulics.node import Junction
from core.swmm.curves import CurveType


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

    tree_hydrology_RainGages       = ["Rain Gages",       None]
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
    tree_nodes_Outfalls     = ["Outfalls",      frmInflows, "1"]
    tree_nodes_Dividers     = ["Dividers",      frmInflows, "1"]
    tree_nodes_StorageUnits = ["Storage Units", frmInflows, "1"]
    tree_nodes_items = [
        tree_nodes_Junctions,
        tree_nodes_Outfalls,
        tree_nodes_Dividers,
        tree_nodes_StorageUnits]

    tree_links_Conduits = ["Conduits", frmCrossSection]
    tree_links_Pumps    = ["Pumps",    None]
    tree_links_Orifices = ["Orifices", None]
    tree_links_Weirs    = ["Weirs",    None]
    tree_links_Outlets  = ["Outlets",  None]
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

    tree_items_using_id = (tree_hydrology_LIDControls,
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
        frmMain.__init__(self, q_application)
        self.model = "SWMM"
        self.model_path = ''  # Set this only if needed later when running model
        self.project_type = Project  # Use the model-specific Project as defined in core.swmm.project
        self.project = Project()
        self.assembly_path = os.path.dirname(os.path.abspath(__file__))
        self.on_load(tree_top_item_list=self.tree_top_items)
        HelpHandler.init_class(os.path.join(self.assembly_path, "swmm.qhc"))
        self.help_topic = ""  # TODO: specify topic to open when Help key is pressed on main form
        self.helper = HelpHandler(self)

        self.actionStatus_ReportMenu = QtGui.QAction(self)
        self.actionStatus_ReportMenu.setObjectName(from_utf8("actionStatus_ReportMenu"))
        self.actionStatus_ReportMenu.setText(transl8("frmMain", "Status", None))
        self.actionStatus_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Status", None))
        self.menuReport.addAction(self.actionStatus_ReportMenu)
        QtCore.QObject.connect(self.actionStatus_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_status)

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

        self.actionGraph_TimeSeriesMenu = QtGui.QAction(self)
        self.actionGraph_TimeSeriesMenu.setObjectName(from_utf8("actionGraph_TimeSeriesMenu"))
        self.actionGraph_TimeSeriesMenu.setText(transl8("frmMain", "Time Series", None))
        self.actionGraph_TimeSeriesMenu.setToolTip(transl8("frmMain", "Display Time Series Plot", None))
        submenuGraph.addAction(self.actionGraph_TimeSeriesMenu)
        QtCore.QObject.connect(self.actionGraph_TimeSeriesMenu, QtCore.SIGNAL('triggered()'), self.report_timeseries)

        self.actionGraph_ScatterMenu = QtGui.QAction(self)
        self.actionGraph_ScatterMenu.setObjectName(from_utf8("actionGraph_ScatterMenu"))
        self.actionGraph_ScatterMenu.setText(transl8("frmMain", "Scatter", None))
        self.actionGraph_ScatterMenu.setToolTip(transl8("frmMain", "Display Scatter Plot", None))
        submenuGraph.addAction(self.actionGraph_ScatterMenu)
        QtCore.QObject.connect(self.actionGraph_ScatterMenu, QtCore.SIGNAL('triggered()'), self.report_scatter)

        menu = QtGui.QMenu()
        submenuTable = QtGui.QMenu(self.menuReport)
        submenuTable.setTitle("Table")
        self.menuReport.addMenu(submenuTable)

        self.actionTable_ObjectMenu = QtGui.QAction(self)
        self.actionTable_ObjectMenu.setObjectName(from_utf8("actionTable_ObjectMenu"))
        self.actionTable_ObjectMenu.setText(transl8("frmMain", "By Object", None))
        self.actionTable_ObjectMenu.setToolTip(transl8("frmMain", "Display Table by Object", None))
        submenuTable.addAction(self.actionTable_ObjectMenu)
        QtCore.QObject.connect(self.actionTable_ObjectMenu, QtCore.SIGNAL('triggered()'), self.report_object)

        self.actionTable_VariableMenu = QtGui.QAction(self)
        self.actionTable_VariableMenu.setObjectName(from_utf8("actionTable_VariableMenu"))
        self.actionTable_VariableMenu.setText(transl8("frmMain", "By Variable", None))
        self.actionTable_VariableMenu.setToolTip(transl8("frmMain", "Display Table by Variable", None))
        submenuTable.addAction(self.actionTable_VariableMenu)
        QtCore.QObject.connect(self.actionTable_VariableMenu, QtCore.SIGNAL('triggered()'), self.report_variable)

        self.actionStatistics_ReportMenu = QtGui.QAction(self)
        self.actionStatistics_ReportMenu.setObjectName(from_utf8("actionStatistics_ReportMenu"))
        self.actionStatistics_ReportMenu.setText(transl8("frmMain", "Statistics", None))
        self.actionStatistics_ReportMenu.setToolTip(transl8("frmMain", "Display Results Statistics", None))
        self.menuReport.addAction(self.actionStatistics_ReportMenu)
        QtCore.QObject.connect(self.actionStatistics_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_statistics)

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
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def report_timeseries(self):
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def report_scatter(self):
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def report_object(self):
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def report_variable(self):
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def report_statistics(self):
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def report_summary(self):
        self._frmSummaryReport = frmSummaryReport(self.parent())
        self._frmSummaryReport.show()
        pass

    def calibration_data(self):
        self._frmCalibrationData = frmCalibrationData(self.parent())
        self._frmCalibrationData.show()
        pass

    def get_editor(self, edit_name):
        frm = None
        # First handle special cases where forms need more than simply being created

        if edit_name == self.tree_quality_Pollutants[0]:
            edit_these = []
            if self.project and self.project.pollutants:
                if not isinstance(self.project.pollutants.value, basestring):
                    if isinstance(self.project.pollutants.value, list):
                        edit_these.extend(self.project.pollutants.value)
                if len(edit_these) == 0:
                    new_item = Pollutant()
                    new_item.name = "NewPollutant"
                    edit_these.append(new_item)
                    self.project.pollutants.value = edit_these
            frm = frmGenericPropertyEditor(self, edit_these, "SWMM Pollutant Editor")
        elif edit_name in [item[0] for item in self.tree_items_using_id]:
            # in these cases the click on the tree diagram populates the lower left list, not directly to an editor
            return None
        # the following items will respond to a click on a conduit form, not the tree diagram
        # elif edit_name == tree_links_Conduits[0]:
        #     frm = frmCrossSection(self)

        # the following items will respond to a click on a node form, not the tree diagram
        # elif edit_name == "Outfalls" or edit_name == "Dividers" or edit_name == "Storage Units":
        #     frm = frmInflows(self)
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)

        return frm

    def get_editor_with_selected_item(self, edit_name, selected_item):
        frm = None
        # First handle special cases where forms need more than simply being created

        if edit_name == "Pollutants":
            edit_these = []
            if self.project and self.project.pollutants:
                if not isinstance(self.project.pollutants.value, basestring):
                    if isinstance(self.project.pollutants.value, list):
                        for value in self.project.pollutants.value:
                            if value.name == selected_item:
                                edit_these.append(value)
            frm = frmGenericPropertyEditor(self, edit_these, "SWMM Pollutant Editor")
        elif edit_name == "Aquifers":
            # do all of these for now, will want to restrict to only selected one
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)
        # the following items will respond to a click on a conduit form, not the tree diagram
        # elif edit_name == "Conduits":
        #     frm = frmCrossSection(self)

        # the following items will respond to a click on a node form, not the tree diagram
        # elif edit_name == "Outfalls" or edit_name == "Dividers" or edit_name == "Storage Units":
        #     frm = frmInflows(self)
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)
            frm.set_from(self.project, selected_item)
        return frm

    def get_object_list(self, category):
        ids = []
        if category == self.tree_hydrology_Subcatchments[0]:
            for i in range(0, len(self.project.subcatchments.value)):
                ids.append(self.project.subcatchments.value[i].name)
        # elif category.lower() == 'rain gages':
            # for i in range(0, len(self.project.raingages.value)):
            #     ids.append(self.project.raingages.value[i].name)
        elif category == self.tree_hydrology_Aquifers[0]:
            for i in range(0, len(self.project.aquifers.value)):
                ids.append(self.project.aquifers.value[i].name)
        elif category == self.tree_hydrology_SnowPacks[0]:
            for i in range(0, len(self.project.snowpacks.value)):
                ids.append(self.project.snowpacks.value[i].name)
        elif category == self.tree_hydrology_UnitHydrographs[0]:
            for i in range(0, len(self.project.hydrographs.value)):
                ids.append(self.project.hydrographs.value[i].group_name)
        elif category == self.tree_hydrology_LIDControls[0]:
            for i in range(0, len(self.project.lid_controls.value)):
                ids.append(self.project.lid_controls.value[i].control_name)
        elif category == self.tree_nodes_Junctions[0]:
            for i in range(0, len(self.project.junctions.value)):
                ids.append(self.project.junctions.value[i].name)
        # elif category == self.tree_nodes_Outfalls[0]:
            # for i in range(0, len(self.project.outfalls.value)):
            #     ids.append(self.project.outfalls.value[i].name)
        # elif category == self.tree_nodes_Dividers[0]:
            # for i in range(0, len(self.project.dividers.value)):
            #     ids.append(self.project.dividers.value[i].name)
        # elif category == self.tree_nodes_StorageUnits[0]:
            # for i in range(0, len(self.project.storage.value)):
            #     ids.append(self.project.storage.value[i].name)
        elif category == self.tree_links_Conduits[0]:
            for i in range(0, len(self.project.conduits.value)):
                ids.append(self.project.conduits.value[i].name)
        elif category == self.tree_links_Pumps:
            for i in range(0, len(self.project.pumps.value)):
                ids.append(self.project.pumps.value[i].name)
        # elif category == self.tree_links_Orifices[0]:
            # for i in range(0, len(self.project.orifices.value)):
            #     ids.append(self.project.orifices.value[i].name)
        # elif category == self.tree_links_Weirs[0]:
            # for i in range(0, len(self.project.weirs.value)):
            #     ids.append(self.project.weirs.value[i].name)
        # elif category == self.tree_links_Outlets[0]:
            # for i in range(0, len(self.project.outlets.value)):
            #     ids.append(self.project.outlets.value[i].name)
        elif category == self.tree_hydraulics_Transects[0]:
            for i in range(0, len(self.project.transects.value)):
                ids.append(self.project.transects.value[i].name)
        elif category == self.tree_quality_Pollutants[0]:
            for i in range(0, len(self.project.pollutants.value)):
                ids.append(self.project.pollutants.value[i].name)
        elif category == self.tree_quality_LandUses[0]:
            for i in range(0, len(self.project.landuses.value)):
                ids.append(self.project.landuses.value[i].land_use_name)
        elif category == self.tree_curves_ControlCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.CONTROL:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_curves_DiversionCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.DIVERSION:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_curves_PumpCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                curve_type = self.project.curves.value[i].curve_type
                if curve_type == CurveType.PUMP1 or curve_type == CurveType.PUMP2 or \
                    curve_type == CurveType.PUMP3 or curve_type == CurveType.PUMP4:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_curves_RatingCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.RATING:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_curves_ShapeCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.SHAPE:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_curves_StorageCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.STORAGE:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_curves_TidalCurves[0]:
            for i in range(0, len(self.project.curves.value)):
                if self.project.curves.value[i].curve_type == CurveType.TIDAL:
                    ids.append(self.project.curves.value[i].curve_id)
        elif category == self.tree_TimeSeries[0]:
            for i in range(0, len(self.project.timeseries.value)):
                ids.append(self.project.timeseries.value[i].name)
        elif category == self.tree_TimePatterns[0]:
            for i in range(0, len(self.project.patterns.value)):
                ids.append(self.project.patterns.value[i].name)
        # elif category == self.tree_MapLabels[0]:
            # for i in range(0, len(self.project.labels.value)):
            #     ids.append(self.project.labels.value[i].label_text)
        return ids

    def run_simulation(self):
        # First find input file to run
        file_name = ''
        use_existing = self.project and self.project.file_name and os.path.exists(self.project.file_name)
        if use_existing:
            file_name = self.project.file_name
            # TODO: save if needed, decide whether to save to temp location as previous version did.
        else:
            directory = QtCore.QSettings(self.model, "GUI").value("ProjectDir", "")
            file_name = QFileDialog.getOpenFileName(self, "Open Project...", directory,
                                                          "Inp files (*.inp);;All files (*.*)")
        if os.path.exists(file_name):

            prefix, extension = os.path.splitext(file_name)
            # if not os.path.exists(self.model_path):
            #     if 'darwin' in sys.platform:
            #         lib_name = 'libswmm.dylib'
            #         ext = '.dylib'
            #     elif 'win' in sys.platform:
            #         lib_name = 'swmm5_x86.dll'
            #         ext = '.dll'
            #
            #     if lib_name:
            #         self.model_path = os.path.join(self.assembly_path, lib_name)
            #         if not os.path.exists(self.model_path):
            #             pp = os.path.dirname(os.path.dirname(self.assembly_path))
            #             self.model_path = os.path.join(pp, "Externals", lib_name)
            #         if not os.path.exists(self.model_path):
            #             self.model_path = QFileDialog.getOpenFileName(self,
            #                                                           'Locate ' + self.model +' Library',
            #                                                           '/', '(*{0})'.format(ext))
            #
            # if os.path.exists(self.model_path):
            #     try:
            #         from Externals.swmm5 import pyswmm
            #         swmm_object = pyswmm(file_name, prefix + '.rpt', prefix + '.out', self.model_path)
            #         swmm_object.swmmExec()
            #         print(swmm_object.swmm_getVersion())
            #         print(swmm_object.swmm_getMassBalErr())
            #
            #         # model_api = pyepanet.ENepanet(file_name, prefix + '.rpt', prefix + '.bin', self.model_path)
            #         # frmRun = frmRunEPANET(model_api, self.project, self)
            #         # self._forms.append(frmRun)
            #         # if not use_existing:
            #         #     # Read this project so we can refer to it while running
            #         #     frmRun.progressBar.setVisible(False)
            #         #     frmRun.lblTime.setVisible(False)
            #         #     frmRun.fraTime.setVisible(False)
            #         #     frmRun.fraBottom.setVisible(False)
            #         #     frmRun.showNormal()
            #         #     frmRun.set_status_text("Reading " + file_name)
            #         #
            #         #     self.project = Project()
            #         #     self.project.read_file(file_name)
            #         #     frmRun.project = self.project
            #         #
            #         # frmRun.Execute()
            #         return
            #     except Exception as e1:
            #         print(str(e1) + '\n' + str(traceback.print_exc()))
            #         QMessageBox.information(None, self.model,
            #                                 "Error running model with library:\n {0}\n{1}\n{2}".format(
            #                                     self.model_path, str(e1), str(traceback.print_exc())),
            #                                 QMessageBox.Ok)
            #     # finally:
            #     #     try:
            #     #         if model_api and model_api.isOpen():
            #     #             model_api.ENclose()
            #     #     except:
            #     #         pass
            #     #     return

            # Could not run with library, try running with executable
            prefix, extension = os.path.splitext(file_name)
            args = []
            exe_name = "swmm5.exe"
            exe_path = os.path.join(self.assembly_path, exe_name)
            if not os.path.isfile(exe_path):
                pp = os.path.dirname(os.path.dirname(self.assembly_path))
                exe_path = os.path.join(pp, "Externals", exe_name)
            if not os.path.isfile(exe_path):
                pp = os.path.dirname(os.path.dirname(self.assembly_path))
                exe_path = os.path.join(pp, "Externals", "swmm", "model", exe_name)
            if not os.path.isfile(exe_path):
                exe_path = QFileDialog.getOpenFileName(self, 'Locate SWMM Executable', '/', 'exe files (*.exe)')
            if os.path.isfile(exe_path):
                args.append(file_name)
                args.append(prefix + '.rpt')
                args.append(prefix + '.out')
                # running the Exe
                status = StatusMonitor0(exe_path, args, self, model='SWMM')
                status.show()
        else:
            QMessageBox.information(None, self.model, self.model + " input file not found", QMessageBox.Ok)

if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
    main_form = frmMainSWMM(application)
    main_form.show()
    sys.exit(application.exec_())