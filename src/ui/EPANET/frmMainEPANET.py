import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
import traceback
from ui.ui_utility import *

from PyQt4 import QtCore, QtGui
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

from ui.model_utility import *
from core.epanet.project import Project
import Externals.epanet2 as pyepanet
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

    def report_status(self):
        print "report_status"
        # TODO: open ~.rpt
        pass

    def report_energy(self):
        print "report_energy"
        pass

    def report_calibration(self):
        print "report_calibration"
        pass

    def report_reaction(self):
        print "report_reaction"
        pass

    def get_editor(self, edit_name):
        frm = None
        # First handle special cases where forms need more than simply being created

        # if edit_name == 'Simple':
        #     frm = frmControls(self, 'EPANET Simple Controls', "CONTROLS")
        # elif edit_name == 'Rule-Based':
        #     frm = frmControls(self, 'EPANET Rule-Based Controls', "RULES")

        # the following items will respond to a click in the list, not the tree diagram
        # elif edit_name == 'Patterns':
        #    return frmPatternEditor(self)
        # elif edit_name == 'Curves':
        #    return frmCurveEditor(self)

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
        return frm

    def run_simulation(self):
        # Find input file to run
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
                    lib_name = 'libepanet.dylib.dylib'
                    ext = '.dylib'
                elif 'win' in sys.platform:
                    lib_name = 'epanet2_amd64.dll'
                    ext = '.dll'
                else:  # Linux
                    lib_name = 'libepanet2_amd64.so'
                    ext = '.so'

                self.model_path = os.path.join(self.assembly_path, lib_name)
                if not os.path.exists(self.model_path):
                    pp = os.path.dirname(os.path.dirname(self.assembly_path))
                    self.model_path = os.path.join(pp, "Externals", lib_name)
                if not os.path.exists(self.model_path):
                    self.model_path = QtGui.QFileDialog.getOpenFileName(self,
                                                                        'Locate ' + self.model + ' Library',
                                                                        '/', '(*{1})'.format(ext))
            if os.path.exists(self.model_path):
                try:
                    model_api = pyepanet.ENepanet(file_name, prefix + '.rpt', prefix + '.bin', self.model_path)
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
            #     exe_path = QtGui.QFileDialog.getOpenFileName(self, 'Locate EPANET Executable', '/',
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
            # status = StatusMonitor0(program, args, self, model='EPANET')
            # status.show()
        else:
            QMessageBox.information(None, self.model, self.model + " input file not found", QMessageBox.Ok)

if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
    main_form = frmMainEPANET(application)
    main_form.show()
    sys.exit(application.exec_())