import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)

from ui.model_utility import *
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

from core.swmm.project import Project
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.quality import Pollutant
from core.swmm.hydraulics.node import Junction


class frmMainSWMM(frmMain):
    """Main form for SWMM user interface, based on frmMain which is shared with EPANET."""

    # Variables used to populate the tree control
    # Each item is a list: label plus either editing form for this section or a child list of tree variables.
    # If an editing form takes additional arguments, they follow the editing form as a list.
    # Special cases may just have a label and no editing form or children.
    # *_items are a lists of items in a section
    tree_options_General = ["General", frmGeneralOptions]
    tree_options_Dates = ["Dates", frmDates]
    tree_options_TimeSteps = ["Time Steps", frmTimeSteps]
    tree_options_DynamicWave = ["Dynamic Wave", frmDynamicWave]
    tree_options_InterfaceFiles = ["Interface Files", frmInterfaceFiles]
    tree_options_Reporting = ["Reporting", frmReportOptions]
    tree_options_MapBackdrop = ["Map/Backdrop", frmMapBackdropOptions]
    tree_options_items = [tree_options_General,
                          tree_options_Dates,
                          tree_options_TimeSteps,
                          tree_options_DynamicWave,
                          tree_options_InterfaceFiles,
                          tree_options_Reporting,
                          tree_options_MapBackdrop]

    tree_climatology_Temperature = ["Temperature", frmClimatology, ["Temperature"]]
    tree_climatology_Evaporation = ["Evaporation", frmClimatology, ["Evaporation"]]
    tree_climatology_WindSpeed = ["Wind Speed", frmClimatology, ["Wind Speed"]]
    tree_climatology_SnowMelt = ["Snow Melt", frmClimatology, ["Snow Melt"]]
    tree_climatology_ArealDepletion = ["Areal Depletion", frmClimatology, ["Areal Depletion"]]
    tree_climatology_Adjustment = ["Adjustment", frmClimatology, ["Adjustment"]]
    tree_climatology_items = [
        tree_climatology_Temperature,
        tree_climatology_Evaporation,
        tree_climatology_WindSpeed,
        tree_climatology_SnowMelt,
        tree_climatology_ArealDepletion,
        tree_climatology_Adjustment]

    tree_hydrology_RainGages = ["Rain Gages", None]
    tree_hydrology_Subcatchments = ["Subcatchments", frmSubcatchments]
    tree_hydrology_Aquifers = ["Aquifers", frmAquifers]
    tree_hydrology_SnowPacks = ["Snow Packs", frmSnowPack]
    tree_hydrology_UnitHydrographs = ["Unit Hydrographs", frmUnitHydrograph]
    tree_hydrology_LIDControls = ["LID Controls", frmLID]
    tree_hydrology_items = [
        tree_hydrology_RainGages,
        tree_hydrology_Subcatchments,
        tree_hydrology_Aquifers,
        tree_hydrology_SnowPacks,
        tree_hydrology_UnitHydrographs,
        tree_hydrology_LIDControls]

    tree_nodes_Junctions = ["Junctions", frmJunction]
    tree_nodes_Outfalls = ["Outfalls", frmInflows, "1"]
    tree_nodes_Dividers = ["Dividers", frmInflows, "1"]
    tree_nodes_StorageUnits = ["Storage Units", frmInflows, "1"]
    tree_nodes_items = [
        tree_nodes_Junctions,
        tree_nodes_Outfalls,
        tree_nodes_Dividers,
        tree_nodes_StorageUnits]

    tree_links_Conduits = ["Conduits", frmCrossSection]
    tree_links_Pumps = ["Pumps", None]
    tree_links_Orifices = ["Orifices", None]
    tree_links_Weirs = ["Weirs", None]
    tree_links_Outlets = ["Outlets", None]
    tree_links_items = [
        tree_links_Conduits,
        tree_links_Pumps,
        tree_links_Orifices,
        tree_links_Weirs,
        tree_links_Outlets]

    tree_hydraulics_Nodes = ["Nodes", tree_nodes_items]
    tree_hydraulics_Links = ["Links", tree_links_items]
    tree_hydraulics_Transects = ["Transects", frmTransect]
    tree_hydraulics_Controls = ["Controls", frmControls]
    tree_hydraulics_items = [
        tree_hydraulics_Nodes,
        tree_hydraulics_Links,
        tree_hydraulics_Transects,
        tree_hydraulics_Controls]

    tree_quality_Pollutants = ["Pollutants", None]
    tree_quality_LandUses = ["Land Uses", frmLandUses]
    tree_quality_items = [
        tree_quality_Pollutants,
        tree_quality_LandUses]

    tree_curves_ControlCurves = ["Control Curves", frmCurveEditor, ["SWMM Control Curves", "CONTROL"]]
    tree_curves_DiversionCurves = ["Diversion Curves", frmCurveEditor, ["SWMM Diversion Curves", "DIVERSION"]]
    tree_curves_PumpCurves = ["Pump Curves", frmCurveEditor, ["SWMM Pump Curves", "PUMP"]]
    tree_curves_RatingCurves = ["Rating Curves", frmCurveEditor, ["SWMM Rating Curves", "RATING"]]
    tree_curves_ShapeCurves = ["Shape Curves", frmCurveEditor, ["SWMM Shape Curves", "SHAPE"]]
    tree_curves_StorageCurves = ["Storage Curves", frmCurveEditor, ["SWMM Storage Curves", "STORAGE"]]
    tree_curves_TidalCurves = ["Tidal Curves", frmCurveEditor, ["SWMM Tidal Curves", "TIDAL"]]
    tree_curves_items = [
        tree_curves_ControlCurves,
        tree_curves_DiversionCurves,
        tree_curves_PumpCurves,
        tree_curves_RatingCurves,
        tree_curves_ShapeCurves,
        tree_curves_StorageCurves,
        tree_curves_TidalCurves]

    tree_TitleNotes = ["Title/Notes", frmTitle]
    tree_Options = ["Options", tree_options_items]
    tree_Climatology = ["Climatology", tree_climatology_items]
    tree_Hydrology = ["Hydrology", tree_hydrology_items]
    tree_Hydraulics = ["Hydraulics", tree_hydraulics_items]
    tree_Quality = ["Quality", tree_quality_items]
    tree_Curves = ["Curves", tree_curves_items]
    tree_TimeSeries = ["Time Series", frmTimeseries]
    tree_TimePatterns = ["Time Patterns", frmPatternEditor]
    tree_MapLabels = ["Map Labels", None]
    tree_top_items = [tree_TitleNotes,
                      tree_Options,
                      tree_Climatology,
                      tree_Hydrology,
                      tree_Hydraulics,
                      tree_Quality,
                      tree_Curves,
                      tree_TimeSeries,
                      tree_TimePatterns,
                      tree_MapLabels]

    def __init__(self, q_application):
        frmMain.__init__(self, q_application)
        self.model = "SWMM"
        self.model_path = ''  # Set this only if needed later when running model
        self.project_type = Project  # Use the model-specific Project as defined in core.swmm.project
        self.project = Project()
        self.assembly_path = os.path.dirname(os.path.abspath(__file__))
        self.on_load(tree_top_item_list=self.tree_top_items)

    def get_editor(self, edit_name):
        frm = None
        # First handle special cases where forms need more than simply being created

        if edit_name == "Pollutants":
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

        # the following items will respond to a click on a conduit form, not the tree diagram
        # elif edit_name == "Conduits":
        #     frm = frmCrossSection(self)

        # the following items will respond to a click on a node form, not the tree diagram
        # elif edit_name == "Outfalls" or edit_name == "Dividers" or edit_name == "Storage Units":
        #     frm = frmInflows(self)
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)

        return frm

    def run_simulation(self):
        # First find input file to run
        file_name = ''
        use_existing = self.project and self.project.file_name and os.path.exists(self.project.file_name)
        if use_existing:
            file_name = self.project.file_name
            # TODO: save if needed, decide whether to save to temp location as previous version did.
        else:
            directory = QtCore.QSettings(self.model, "GUI").value("ProjectDir", "")
            file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Project...", directory,
                                                          "Inp files (*.inp);;All files (*.*)")
        if os.path.exists(file_name):

            prefix, extension = os.path.splitext(file_name)
            if not os.path.exists(self.model_path):
                if 'darwin' in sys.platform:
                    lib_name = 'libswmm.dylib'
                    ext = '.dylib'
                elif 'win' in sys.platform:
                    lib_name = 'swmm5_x86.dll'
                    ext = '.dll'

                if lib_name:
                    self.model_path = os.path.join(self.assembly_path, lib_name)
                    if not os.path.exists(self.model_path):
                        pp = os.path.dirname(os.path.dirname(self.assembly_path))
                        self.model_path = os.path.join(pp, "Externals", lib_name)
                    if not os.path.exists(self.model_path):
                        self.model_path = QtGui.QFileDialog.getOpenFileName(self,
                                                                            'Locate ' + self.model +' Library',
                                                                            '/', '(*{1})'.format(ext))

            if os.path.exists(self.model_path):
                try:
                    from Externals.swmm5 import pyswmm
                    swmm_object = pyswmm(file_name, prefix + '.rpt', prefix + '.out', self.model_path)
                    swmm_object.swmmExec()
                    print(swmm_object.swmm_getVersion())
                    print(swmm_object.swmm_getMassBalErr())

                    # model_api = pyepanet.ENepanet(file_name, prefix + '.rpt', prefix + '.bin', self.model_path)
                    # frmRun = frmRunEPANET(model_api, self.project, self)
                    # self._forms.append(frmRun)
                    # if not use_existing:
                    #     # Read this project so we can refer to it while running
                    #     frmRun.progressBar.setVisible(False)
                    #     frmRun.lblTime.setVisible(False)
                    #     frmRun.fraTime.setVisible(False)
                    #     frmRun.fraBottom.setVisible(False)
                    #     frmRun.showNormal()
                    #     frmRun.set_status_text("Reading " + file_name)
                    #
                    #     self.project = Project()
                    #     self.project.read_file(file_name)
                    #     frmRun.project = self.project
                    #
                    # frmRun.Execute()
                    return
                except Exception as e1:
                    print(str(e1) + '\n' + str(traceback.print_exc()))
                    QMessageBox.information(None, self.model,
                                            "Error running model with library:\n {0}\n{1}\n{2}".format(
                                                self.model_path, str(e1), str(traceback.print_exc())),
                                            QMessageBox.Ok)
                # finally:
                #     try:
                #         if model_api and model_api.isOpen():
                #             model_api.ENclose()
                #     except:
                #         pass
                #     return

            # Could not run with library, try running with executable
            args = []
            exe_name = "swmm5.exe"
            exe_path = os.path.join(self.assembly_path, exe_name)
            if not os.path.isfile(exe_path):
                pp = os.path.dirname(os.path.dirname(self.assembly_path))
                exe_path = os.path.join(pp, "Externals", exe_name)
            if not os.path.isfile(exe_path):
                exe_path = QtGui.QFileDialog.getOpenFileName(self, 'Locate SWMM Executable', '/', 'exe files (*.exe)')
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