import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import traceback
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QFileDialog

from ui.model_utility import QString, from_utf8, transl8, process_events

from ui.frmMain import frmMain
from ui.EPANET.frmEnergyOptions import frmEnergyOptions
from ui.EPANET.frmHydraulicsOptions import frmHydraulicsOptions
from ui.EPANET.frmMapBackdropOptions import frmMapBackdropOptions
from ui.EPANET.frmQualityOptions import frmQualityOptions
from ui.EPANET.frmReactionsOptions import frmReactionsOptions
from ui.EPANET.frmReportOptions import frmReportOptions
from ui.EPANET.frmTimesOptions import frmTimesOptions
from ui.EPANET.frmTitle import frmTitle

from ui.EPANET.frmControls import frmControls
from ui.EPANET.frmCurveEditor import frmCurveEditor
from ui.EPANET.frmPatternEditor import frmPatternEditor
from ui.EPANET.frmSourcesQuality import frmSourcesQuality
from ui.EPANET.frmDemands import frmDemands
from ui.EPANET.frmGraph import frmGraph
from ui.EPANET.frmTable import frmTable
from ui.EPANET.frmEnergyReport import frmEnergyReport
from ui.EPANET.frmCalibrationData import frmCalibrationData
from ui.EPANET.frmCalibrationReportOptions import frmCalibrationReportOptions

from core.epanet.project import Project
import core.epanet.reports as reports
from Externals.epanet.model.epanet2 import ENepanet
from Externals.epanet.output import ENOutputWrapper
from frmRunEPANET import frmRunEPANET


class frmMainEPANET(frmMain):
    """Main form for EPANET user interface, based on frmMain which is shared with SWMM."""

    # Variables used to populate the tree control
    # Each item is a list: label plus either editing form for this section or a child list.
    # Special cases may just have a label and no editing form or children.
    # *_items are a lists of items in a section
    tree_options_Hydraulics = ["Hydraulics", frmHydraulicsOptions]
    tree_options_Quality = ["Quality", frmQualityOptions]
    tree_options_Reactions = ["Reactions", frmReactionsOptions]
    tree_options_Times = ["Times", frmTimesOptions]
    tree_options_Energy = ["Energy", frmEnergyOptions]
    tree_options_Report = ["Report", frmReportOptions]
    tree_options_MapBackdrop = ["Map/Backdrop", frmMapBackdropOptions]
    tree_options_items = [tree_options_Hydraulics,
                          tree_options_Quality,
                          tree_options_Reactions,
                          tree_options_Times,
                          tree_options_Energy,
                          tree_options_Report,
                          tree_options_MapBackdrop]

    tree_controls_Simple = ["Simple", frmControls, ["EPANET Simple Controls", "CONTROLS"]]
    tree_controls_RuleBased = ["Rule-Based", frmControls, ["EPANET Rule-Based Controls", "RULES"]]
    tree_controls_items = [tree_controls_Simple,
                           tree_controls_RuleBased]

    tree_TitleNotes = ["Title/Notes", frmTitle]
    tree_Options = ["Options", tree_options_items]
    tree_Junctions = ["Junctions", None]
    tree_Reservoirs = ["Reservoirs", None]
    tree_Tanks = ["Tanks", None]
    tree_Pipes = ["Pipes", None]
    tree_Pumps = ["Pumps", None]
    tree_Valves = ["Valves", None]
    tree_Labels = ["Labels", None]
    tree_Patterns = ["Patterns", frmPatternEditor]
    tree_Curves = ["Curves", frmCurveEditor]
    tree_Controls = ["Controls", tree_controls_items]
    tree_top_items = [tree_TitleNotes,
                      tree_Options,
                      tree_Junctions,
                      tree_Reservoirs,
                      tree_Tanks,
                      tree_Pipes,
                      tree_Pumps,
                      tree_Valves,
                      tree_Labels,
                      tree_Patterns,
                      tree_Curves,
                      tree_Controls]

    def __init__(self, q_application):
        frmMain.__init__(self, q_application)
        self.model = "EPANET"
        self.model_path = ''  # Set this only if needed later when running model
        self.output = None    # Set this when model output is available
        self.project_type = Project  # Use the model-specific Project as defined in core.epanet.project
        self.project = Project()
        self.assembly_path = os.path.dirname(os.path.abspath(__file__))
        self.on_load(tree_top_item_list=self.tree_top_items)

        self.actionStatus_ReportMenu = QtGui.QAction(self)
        self.actionStatus_ReportMenu.setObjectName(from_utf8("actionStatus_ReportMenu"))
        self.actionStatus_ReportMenu.setText(transl8("frmMain", "Status", None))
        self.actionStatus_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Status", None))
        self.menuReport.addAction(self.actionStatus_ReportMenu)
        QtCore.QObject.connect(self.actionStatus_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_status)

        self.actionEnergy_ReportMenu = QtGui.QAction(self)
        self.actionEnergy_ReportMenu.setObjectName(from_utf8("actionEnergy_ReportMenu"))
        self.actionEnergy_ReportMenu.setText(transl8("frmMain", "Energy", None))
        self.actionEnergy_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Energy", None))
        self.menuReport.addAction(self.actionEnergy_ReportMenu)
        QtCore.QObject.connect(self.actionEnergy_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_energy)

        self.actionCalibration_ReportMenu = QtGui.QAction(self)
        self.actionCalibration_ReportMenu.setObjectName(from_utf8("actionCalibration_ReportMenu"))
        self.actionCalibration_ReportMenu.setText(transl8("frmMain", "Calibration", None))
        self.actionCalibration_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Calibration", None))
        self.menuReport.addAction(self.actionCalibration_ReportMenu)
        QtCore.QObject.connect(self.actionCalibration_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_calibration)

        self.actionReaction_ReportMenu = QtGui.QAction(self)
        self.actionReaction_ReportMenu.setObjectName(from_utf8("actionReaction_ReportMenu"))
        self.actionReaction_ReportMenu.setText(transl8("frmMain", "Reaction", None))
        self.actionReaction_ReportMenu.setToolTip(transl8("frmMain", "Display Simulation Reaction", None))
        self.menuReport.addAction(self.actionReaction_ReportMenu)
        QtCore.QObject.connect(self.actionReaction_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_reaction)

        self.actionFull_ReportMenu = QtGui.QAction(self)
        self.actionFull_ReportMenu.setObjectName(from_utf8("actionFull_ReportMenu"))
        self.actionFull_ReportMenu.setText(transl8("frmMain", "Full...", None))
        self.actionFull_ReportMenu.setToolTip(transl8("frmMain", "Save full report as text file", None))
        self.menuReport.addAction(self.actionFull_ReportMenu)
        QtCore.QObject.connect(self.actionFull_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_full)

        self.actionGraph_ReportMenu = QtGui.QAction(self)
        self.actionGraph_ReportMenu.setObjectName(from_utf8("actionGraph_ReportMenu"))
        self.actionGraph_ReportMenu.setText(transl8("frmMain", "Graph...", None))
        self.actionGraph_ReportMenu.setToolTip(transl8("frmMain", "Display graph selection options", None))
        self.menuReport.addAction(self.actionGraph_ReportMenu)
        QtCore.QObject.connect(self.actionGraph_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_graph)

        self.actionTable_ReportMenu = QtGui.QAction(self)
        self.actionTable_ReportMenu.setObjectName(from_utf8("actionTable_ReportMenu"))
        self.actionTable_ReportMenu.setText(transl8("frmMain", "Table...", None))
        self.actionTable_ReportMenu.setToolTip(transl8("frmMain", "Display table selection options", None))
        self.menuReport.addAction(self.actionTable_ReportMenu)
        QtCore.QObject.connect(self.actionTable_ReportMenu, QtCore.SIGNAL('triggered()'), self.report_table)

    def report_status(self):
        print "report_status"
        # TODO: open ~.rpt
        pass

    def report_energy(self):
        self._frmEnergyReport = frmEnergyReport(self.parent())
        # self._frmEnergyReport.set_data()
        self._frmEnergyReport.show()
        pass

    def report_calibration(self):
        self._frmCalibrationReportOptions = frmCalibrationReportOptions(self.parent())
        self._frmCalibrationReportOptions.show()
        pass

    def report_reaction(self):
        self.reaction_report()
        pass

    def report_full(self):
        if self.output:
            directory = os.path.dirname(self.project.file_name)
            report_file_name = QtGui.QFileDialog.getSaveFileName(self, "Save Full Report As...", directory, "Text files (*.txt)")
            if report_file_name:
                try:
                    reporter = reports.Reports(self.project, self.output)
                    reporter.write_report(report_file_name)
                except Exception as e1:
                    msg = str(e1) + '\n' + str(traceback.print_exc())
                    print(msg)
                    QMessageBox.information(None, self.model,
                                            "Error writing report to \n" + report_file_name + '\n' + msg,
                                            QMessageBox.Ok)

        else:
            QMessageBox.information(None, self.model,
                                    "There is no model output currently open.\n"
                                    "Model output is automatically opened after model is run.",
                                    QMessageBox.Ok)



    def report_graph(self):
        self._frmGraph = frmGraph(self.parent())
        self._frmGraph.show()
        pass

    def report_table(self):
        self._frmTable = frmTable(self.parent())
        self._frmTable.show()
        pass

    def reaction_report(self):

        # TXT_NO_REACTION = 'No reactions occurred'
        # TXT_AVG_RATES = 'Average Reaction Rates (kg/day)'
        # ' Reaction Report'

        # // Find conversion factor to kilograms/day
        # ucf := 1.0e6/24;
        # if Pos('ug', NodeUnits[NODEQUAL].Units) > 0 then ucf := 1.0e9/24;
        #
        # if Chart1.SeriesCount > 0 then with Chart1.Series[0] do
        # begin
        #
        # // Initialize the chart
        # Clear;
        # Active := False;
        # Chart1.Title.Text.Clear;
        # Chart1.Foot.Text.Clear;
        #
        # // Get average reaction rates from output file
        # Uoutput.GetReactRates(r);
        # for i := 0 to 3 do rate[i] := r[i] / ucf;
        #
        # // Check max. rate to see if any reactions occurred
        # maxrate := MaxValue(Slice(rate,3));
        # if maxrate = 0 then
        # begin
        #   Chart1.Foot.Text.Add(TXT_NO_REACTION);
        # end
        #
        # // Add each rate category to chart
        # else
        # begin
        # Chart1.Title.Text.Add(TXT_AVG_RATES);
        # Add(rate[0],TXT_BULK,clBlue);
        # Add(rate[1],TXT_WALL,clRed);
        # Add(rate[2],TXT_TANKS,clGreen);
        #  Active := True;
        # Chart1.Foot.Text.Add(Format(FMT_INFLOW,[rate[3]]));
        # end;
        # end;

        import matplotlib.pyplot as plt

        # The slices will be ordered and plotted counter-clockwise.
        labels = '2.8 Tanks', '0.5 Bulk', '2.1 Wall'
        sizes = [52.49, 8.57, 38.93]
        colors = ['green', 'blue', 'red']
        explode = (0, 0, 0)

        plt.figure("Reaction Report")
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.2f%%', shadow=True, startangle=180)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.suptitle("Average Reaction Rates (kg/day)", fontsize=16)
        plt.text(0.9,-0.9,"Inflow Rate = 6")

        plt.show()

    def calibration_data(self):
        self._frmCalibrationData = frmCalibrationData(self.parent())
        self._frmCalibrationData.show()
        pass

    def get_editor(self, edit_name):
        frm = None
        # First handle special cases where forms need more than simply being created

        # the following items will respond to a click on a node form, not the tree diagram
        if edit_name == 'Reservoirs' or edit_name == 'Tanks':
            # assume we're editing the first node for now
            frm = frmSourcesQuality(self)
            frm.setWindowTitle('EPANET Source Editor for Node ' + '1')
            frm.set_from(self.project, '1')
        elif edit_name == 'Junctions':
            # assume we're editing the first junction for now
            frm = frmDemands(self)
            frm.setWindowTitle('EPANET Demands for Junction ' + '1')
            frm.set_from(self.project, '1')
        elif edit_name == 'Patterns':
            return None
        elif edit_name == 'Curves':
            return None
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)
        return frm

    def get_editor_with_selected_item(self, edit_name, selected_item):
        frm = None

        # the following items will respond to a click on a node form, not the tree diagram
        if edit_name == 'Reservoirs' or edit_name == 'Tanks':
            # assume we're editing the first node for now
            frm = frmSourcesQuality(self)
            frm.setWindowTitle('EPANET Source Editor for Node ' + '1')
            frm.set_from(self.project, '1')
        elif edit_name == 'Junctions':
            # assume we're editing the first junction for now
            frm = frmDemands(self)
            frm.setWindowTitle('EPANET Demands for Junction ' + '1')
            frm.set_from(self.project, '1')
        else:  # General-purpose case finds most editors from tree information
            frm = self.make_editor_from_tree(edit_name, self.tree_top_items)
            frm.set_from(self.project, selected_item)
        return frm

    def get_object_list(self, category):
        ids = []
        if category.lower() == 'junctions':
            for i in range(0, len(self.project.junctions.value)):
                ids.append(self.project.junctions.value[i].node_id)
        elif category.lower() == 'reservoirs':
            for i in range(0, len(self.project.reservoirs.value)):
                ids.append(self.project.reservoirs.value[i].node_id)
        elif category.lower() == 'tanks':
            for i in range(0, len(self.project.tanks.value)):
                ids.append(self.project.tanks.value[i].node_id)
        elif category.lower() == 'pipes':
            for i in range(0, len(self.project.pipes.value)):
                ids.append(self.project.pipes.value[i].id)
        elif category.lower() == 'pumps':
            for i in range(0, len(self.project.pumps.value)):
                ids.append(self.project.pumps.value[i].id)
        elif category.lower() == 'valves':
            for i in range(0, len(self.project.valves.value)):
                ids.append(self.project.valves.value[i].id)
        elif category.lower() == 'labels':
            for i in range(0, len(self.project.labels.value)):
                ids.append(self.project.labels.value[i].label)
        elif category.lower() == 'patterns':
            for i in range(0, len(self.project.patterns.value)):
                ids.append(self.project.patterns.value[i].pattern_id)
        elif category.lower() == 'curves':
            for i in range(0, len(self.project.curves.value)):
                ids.append(self.project.curves.value[i].curve_id)
        return ids

    def run_simulation(self):
        # Find input file to run
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
            if not os.path.exists(self.model_path):
                if 'darwin' in sys.platform:
                    lib_name = 'libepanet.dylib.dylib'
                elif 'win' in sys.platform:
                    lib_name = 'epanet2_amd64.dll'
                else:  # Linux
                    lib_name = 'libepanet2_amd64.so'
                self.model_path = self.find_external(lib_name)
            if os.path.exists(self.model_path):
                try:
                    model_api = ENepanet(file_name, prefix + '.rpt', prefix + '.bin', self.model_path)
                    frmRun = frmRunEPANET(model_api, self.project, self)
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
                    self.output = ENOutputWrapper.OutputObject(prefix + '.bin')
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

            # # Could not run with library, try running with executable
            # # Run executable with StatusMonitor0
            # args = []
            # self.modelenv1 = 'EXE_EPANET'
            # program = os.environ[self.modelenv1]
            #
            # exe_name = "epanet2d.exe"
            # exe_path = os.path.join(self.assembly_path, exe_name)
            # if not os.path.exists(exe_path):
            #     pp = os.path.dirname(os.path.dirname(self.assembly_path))
            #     exe_path = os.path.join(pp, "Externals", exe_name)
            # if not os.path.exists(exe_path):
            #     exe_path = QFileDialog.getOpenFileName(self, 'Locate EPANET Executable', '/',
            #                                              'exe files (*.exe)')
            # if os.path.exists(exe_path):
            #     os.environ[self.modelenv1] = exe_path
            # else:
            #     os.environ[self.modelenv1] = ''
            #
            # if not os.path.exists(program):
            #     QMessageBox.information(None, "EPANET", "EPANET Executable not found", QMessageBox.Ok)
            #     return -1
            #
            # args.append(file_name)
            # args.append(prefix + '.txt')
            # args.append(prefix + '.out')
            # status = model_utility.StatusMonitor0(program, args, self, model='EPANET')
            # status.show()
        else:
            QMessageBox.information(None, self.model, self.model + " input file not found", QMessageBox.Ok)

    def find_external(self, lib_name):
        filename = os.path.join(self.assembly_path, lib_name)
        if not os.path.exists(filename):
            pp = os.path.dirname(os.path.dirname(self.assembly_path))
            filename = os.path.join(pp, "Externals", lib_name)
        if not os.path.exists(filename):
            pp = os.path.dirname(os.path.dirname(self.assembly_path))
            filename = os.path.join(pp, "Externals", "epanet", "model", lib_name)
        if not os.path.exists(filename):
            filename = QFileDialog.getOpenFileName(self,
                                                          'Locate ' + self.model + ' Library',
                                                          '/', '(*{0})'.format(os.path.splitext(lib_name)[1]))
        return filename

if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
    main_form = frmMainEPANET(application)
    main_form.show()
    sys.exit(application.exec_())