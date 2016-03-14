import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from ui.ui_utility import *
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

from ui.SWMM.frmClimatology import  frmClimatology

from ui.SWMM.frmControls import frmControls
from ui.SWMM.frmCurveEditor import frmCurveEditor
from ui.SWMM.frmPatternEditor import frmPatternEditor

from core.swmm.project import Project


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
        pexe = os.path.join(assembly_path, exe_name)
        if not os.path.exists(pexe):
            pp = os.path.dirname(os.path.dirname(assembly_path))
            pexe = os.path.join(pp, "Externals", exe_name)
        if not os.path.exists(pexe):
            pexe = QtGui.QFileDialog.getOpenFileName(self, 'Locate SWMM Executable', '/',
                                                        'exe files (*.exe)')
        if os.path.exists(pexe):
            os.environ[self.modelenv1] = pexe
        else:
            os.environ[self.modelenv1] = ''

        self.on_load(model=self.model)

        self._frmDates = None
        self._frmDynamicWave = None
        self._frmMapBackdropOptions = None
        self._frmGeneralOptions = None
        self._frmInterfaceFiles = None
        self._frmReportOptions = None
        self._frmTimeSteps = None
        self._frmTitle = None

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

        if itm.data(0, 0) == 'Dates':
            self._frmDates = frmDates(self)
            self._frmDates.show()
        if itm.data(0, 0) == 'Dynamic Wave':
            self._frmDynamicWave = frmDynamicWave(self)
            self._frmDynamicWave.show()
        if itm.data(0, 0) == 'Map/Backdrop':
            self._frmMapBackdropOptions = frmMapBackdropOptions(self)
            self._frmMapBackdropOptions.show()
        if itm.data(0, 0) == 'General':
            self._frmGeneralOptions = frmGeneralOptions(self)
            self._frmGeneralOptions.show()
        if itm.data(0, 0) == 'Interface Files':
            self._frmInterfaceFiles = frmInterfaceFiles(self)
            self._frmInterfaceFiles.show()
        if itm.data(0, 0) == 'Reporting':
            self._frmReportOptions = frmReportOptions(self)
            self._frmReportOptions.show()
        if itm.data(0, 0) == 'Time Steps':
            self._frmTimeSteps = frmTimeSteps(self)
            self._frmTimeSteps.show()
        if itm.data(0, 0) == 'Title/Notes':
            self._frmTitle = frmTitle(self)
            self._frmTitle.show()
        if itm.data(0, 0) == 'Controls':
            self._frmControls = frmControls(self)
            self._frmControls.show()

        if itm.data(0, 0) == "Temperature":
            self._frmClimatology = frmClimatology(self)
            self._frmClimatology.set_from(self.project, itm.data(0, 0))
            self._frmClimatology.show()
        elif itm.data(0, 0) == "Evaporation":
            self._frmClimatology = frmClimatology(self)
            self._frmClimatology.set_from(self.project, itm.data(0, 0))
            self._frmClimatology.show()
        elif itm.data(0, 0) == "Wind Speed":
            self._frmClimatology = frmClimatology(self)
            self._frmClimatology.set_from(self.project, itm.data(0, 0))
            self._frmClimatology.show()
        elif itm.data(0, 0) == "Snow Melt":
            self._frmClimatology = frmClimatology(self)
            self._frmClimatology.set_from(self.project, itm.data(0, 0))
            self._frmClimatology.show()
        elif itm.data(0, 0) == "Areal Depletion":
            self._frmClimatology = frmClimatology(self)
            self._frmClimatology.set_from(self.project, itm.data(0, 0))
            self._frmClimatology.show()
        elif itm.data(0, 0) == "Adjustment":
            self._frmClimatology = frmClimatology(self)
            self._frmClimatology.set_from(self.project, itm.data(0, 0))
            self._frmClimatology.show()

        # the following items will respond to a click in the list, not the tree diagram
        if itm.data(0, 0) == 'Time Patterns':
            self._frmPatternEditor = frmPatternEditor(self)
            self._frmPatternEditor.show()
        if itm.data(0, 0) == 'Control Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Control Curves')
            self._frmCurveEditor.set_from(self.project, "CONTROL")
            self._frmCurveEditor.show()
        if itm.data(0, 0) == 'Diversion Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Diversion Curves')
            self._frmCurveEditor.set_from(self.project, "DIVERSION")
            self._frmCurveEditor.show()
        if itm.data(0, 0) == 'Pump Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Pump Curves')
            self._frmCurveEditor.set_from(self.project, "PUMP")
            self._frmCurveEditor.show()
        if itm.data(0, 0) == 'Rating Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Rating Curves')
            self._frmCurveEditor.set_from(self.project, "RATING")
            self._frmCurveEditor.show()
        if itm.data(0, 0) == 'Shape Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Shape Curves')
            self._frmCurveEditor.set_from(self.project, "SHAPE")
            self._frmCurveEditor.show()
        if itm.data(0, 0) == 'Storage Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Storage Curves')
            self._frmCurveEditor.set_from(self.project, "STORAGE")
            self._frmCurveEditor.show()
        if itm.data(0, 0) == 'Tidal Curves':
            self._frmCurveEditor = frmCurveEditor(self)
            self._frmCurveEditor.setWindowTitle('SWMM Tidal Curves')
            self._frmCurveEditor.set_from(self.project, "TIDAL")
            self._frmCurveEditor.show()

    def proj_run_simulation(self):
        run = 0
        inp_dir = ''
        margs=[]

        prog = os.environ[self.modelenv1]
        if not os.path.exists(prog):
            QMessageBox.information(None, "SWMM", "SWMM Executable not found", QMessageBox.Ok)
            return -1

        filename = ''
        if self.project is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.inp)')
        else:
            filename = self.project.file_name
        if os.path.exists(filename):
            fpre, fext = os.path.splitext(filename)
            margs.append(filename)
            margs.append(fpre + '.rpt')
            margs.append(fpre + '.out')
        else:
            QMessageBox.information(None, "SWMM", "SWMM input file not found", QMessageBox.Ok)

        # running the Exe (modified version to rid of the \b printout
        status = StatusMonitor0(prog, margs, self, model='SWMM')
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