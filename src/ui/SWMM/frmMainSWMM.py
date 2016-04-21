import os
import sys

os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from ui.model_utility import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QMessageBox
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
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor

from core.swmm.project import Project
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.quality import Pollutant
from core.swmm.hydraulics.node import Junction

class frmMainSWMM(frmMain):
    def __init__(self, parent=None, *args):
        frmMain.__init__(self, parent)
        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.std_newproj)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.std_newproj)

        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.std_openproj)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.std_openproj)

        QtCore.QObject.connect(self.actionStdExit, QtCore.SIGNAL('triggered()'), self.action_exit)

        self.model = 'SWMM'
        self.modelenv1 = 'EXE_SWMM'
        self.project = Project()

        assembly_path = os.path.dirname(os.path.abspath(__file__))
        exe_name = "swmm5.exe"
        exe_path = os.path.join(assembly_path, exe_name)
        if not os.path.exists(exe_path):
            pp = os.path.dirname(os.path.dirname(assembly_path))
            exe_path = os.path.join(pp, "Externals", exe_name)
        if not os.path.exists(exe_path):
            exe_path = QtGui.QFileDialog.getOpenFileName(self, 'Locate SWMM Executable', '/', 'exe files (*.exe)')
        if os.path.exists(exe_path):
            os.environ[self.modelenv1] = exe_path
        else:
            os.environ[self.modelenv1] = ''

        self.on_load(model=self.model)

        self._editors = []
        """List of editor windows used during this session, kept here so they are not automatically closed."""

    def std_newproj(self):
        self.project = Project()
        self.setWindowTitle(self.model + " - New")
        self.project.file_name = "New.inp"

    def std_openproj(self):
        qsettings = QtCore.QSettings(self.model, "GUI")
        directory = qsettings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Project...", directory,
                                                      "Inp files (*.inp);;All files (*.*)")
        if file_name:
            self.project = Project()
            try:
                self.project.read_file(file_name)
                path_only, file_only = os.path.split(file_name)
                self.setWindowTitle(self.model + " - " + file_only)
                if path_only != directory:
                    qsettings.setValue("ProjectDir", path_only)
                    del qsettings
            except:
                self.project = Project()
                self.setWindowTitle(self.model)

    def proj_save(self):
        self.project.write_file(self.project.file_name)

    def proj_save_as(self):
        qsettings = QtCore.QSettings(self.model, "GUI")
        directory = qsettings.value("ProjectDir", "")
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As...", directory, "Inp files (*.inp)")
        if file_name:
            self.project.write_file(file_name)
            path_only, file_only = os.path.split(file_name)
            self.setWindowTitle(self.model + " - " + file_only)
            if path_only != directory:
                qsettings.setValue("ProjectDir", path_only)
                del qsettings

    def edit_options(self, itm, column):
        if not self.project:
            return
        edit_name = itm.data(0, 0)
        if edit_name:
            self.show_edit_window(self.get_editor(edit_name))

    def show_edit_window(self, window):
        if window:
            self._editors.append(window)
            # window.destroyed.connect(lambda s, e, a: self._editors.remove(s))
            # window.destroyed = lambda s, e, a: self._editors.remove(s)
            # window.connect(window, QtCore.SIGNAL('triggered()'), self.editor_closing)
            window.show()

    # def editor_closing(self, event):
    #     print "Editor Closing: " + str(event)
    #     # self._editors.remove(event.)

    def get_editor(self, edit_name):
        if edit_name == "Dates":
            return frmDates(self)
        elif edit_name == "Dynamic Wave":
            return frmDynamicWave(self)
        elif edit_name == "Map/Backdrop":
            return frmMapBackdropOptions(self)
        elif edit_name == "General":
            return frmGeneralOptions(self)
        elif edit_name == "Interface Files":
            return frmInterfaceFiles(self)
        elif edit_name == "Reporting":
            return frmReportOptions(self)
        elif edit_name == "Time Steps":
            return frmTimeSteps(self)
        elif edit_name == "Title/Notes":
            return frmTitle(self)
        elif edit_name == "Controls":
            return frmControls(self)
        elif edit_name in ("Temperature", "Evaporation", "Wind Speed", "Snow Melt", "Areal Depletion", "Adjustment"):
            return frmClimatology(self, edit_name)
        # the following items will respond to a click in the list, not the tree diagram
        elif edit_name == "Time Patterns":
            return frmPatternEditor(self)
        elif edit_name == "Time Series":
            return frmTimeseries(self)
        elif edit_name == "Control Curves":
            return frmCurveEditor(self, 'SWMM Control Curves', "CONTROL")
        elif edit_name == "Diversion Curves":
            return frmCurveEditor(self, 'SWMM Diversion Curves', "DIVERSION")
        elif edit_name == "Pump Curves":
            return frmCurveEditor(self, 'SWMM Pump Curves', "PUMP")
        elif edit_name == "Rating Curves":
            return frmCurveEditor(self, 'SWMM Rating Curves', "RATING")
        elif edit_name == "Shape Curves":
            return frmCurveEditor(self, 'SWMM Shape Curves', "SHAPE")
        elif edit_name == "Storage Curves":
            return frmCurveEditor(self, 'SWMM Storage Curves', "STORAGE")
        elif edit_name == "Tidal Curves":
            return frmCurveEditor(self, 'SWMM Tidal Curves', "TIDAL")
        elif edit_name == "LID Controls":
            return frmLID(self)
        elif edit_name == "Snow Packs":
            return frmSnowPack(self)
        elif edit_name == "Unit Hydrographs":
            return frmUnitHydrograph(self)
        elif edit_name == "Transects":
            return frmTransect(self)
        elif edit_name == "Aquifers":
            return frmAquifers(self)
        elif edit_name == "Pollutants":
            edit_these = []
            if isinstance(self.project.pollutants.value, list):
                if len(self.project.pollutants.value) == 0:
                    new_item = Pollutant()
                    new_item.name = "NewPollutant"
                    self.project.pollutants.value.append(new_item)

            edit_these.extend(self.project.pollutants.value)
            return frmGenericPropertyEditor(self, edit_these, "SWMM Pollutant Editor")

        elif edit_name == "Junctions":
            return frmJunction(self)

        # the following items will respond to a click on a conduit form, not the tree diagram
        elif edit_name == "Conduits":
            return frmCrossSection(self)

        # the following items will respond to a click on a node form, not the tree diagram
        elif edit_name == "Outfalls' or edit_name == 'Dividers' or edit_name == 'Storage Units":
            return frmInflows(self)

        elif edit_name == "Subcatchments":
            return frmSubcatchments(self)

    def run_simulation(self):
        run = 0
        inp_dir = ''
        args=[]

        program = os.environ[self.modelenv1]
        if not os.path.exists(program):
            QMessageBox.information(None, "SWMM", "SWMM Executable not found", QMessageBox.Ok)
            return -1

        filename = ''
        if self.project is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.inp)')
        else:
            filename = self.project.file_name
        if os.path.exists(filename):
            prefix, extension = os.path.splitext(filename)
            args.append(filename)
            args.append(prefix + '.rpt')
            args.append(prefix + '.out')
        else:
            QMessageBox.information(None, "SWMM", "SWMM input file not found", QMessageBox.Ok)

        # running the Exe (modified version to rid of the \b printout
        status = StatusMonitor0(program, args, self, model='SWMM')
        status.show()

    def on_load(self, **kwargs):
        self.obj_tree = ObjectTreeView(model=kwargs['model'])
        self.obj_tree.itemDoubleClicked.connect(self.edit_options)
        layout = QVBoxLayout(self.tabProject)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.obj_tree)
        self.tabProject.setLayout(layout)
        self.setWindowTitle(self.model)

        self.obj_list = ObjectListView(model=kwargs['model'],ObjRoot='',ObjType='',ObjList=None)
        mlayout = self.dockw_more.layout()
        mlayout.addWidget(self.obj_list)
        self.dockw_more.setLayout(mlayout)

    def action_exit(self):
        # TODO: check project status and prompt if there are unsaved changed
        app.quit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = frmMainSWMM()
    MainApp.show()
    sys.exit(app.exec_())