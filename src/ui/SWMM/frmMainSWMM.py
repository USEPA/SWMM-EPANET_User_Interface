import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from ui.ui_utility import *
from ui.model_utility import *
from PyQt4 import QtCore, QtGui
from ui.frmMain import frmMain
from ui.SWMM.frmDates import frmDates
from ui.SWMM.frmDynamicWave import frmDynamicWave
from ui.SWMM.frmMapBackdropOptions import frmMapBackdropOptions
from ui.SWMM.frmGeneralOptions import frmGeneralOptions
from ui.SWMM.frmInterfaceFiles import frmInterfaceFiles
from ui.SWMM.frmReportOptions import frmReportOptions
from ui.SWMM.frmTimeSteps import frmTimeSteps
from ui.SWMM.frmTitle import frmTitle
from core.swmm.project import Project


class frmMainSWMM(frmMain):
    def __init__(self, parent=None, *args):
        frmMain.__init__(self, parent)
        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.std_newproj)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.std_newproj)

        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.std_openproj)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.std_openproj)

        self.model = 'SWMM'
        self.modelenv1 = 'EXE_SWMM'
        assembly_path = os.path.abspath(__file__)
        pp = os.path.dirname(os.path.dirname(os.path.dirname(assembly_path)))
        pexe = os.path.join(pp, r'Externals\SWMM5Exe.exe')
        if os.path.exists(pexe):
            os.environ[self.modelenv1] = pexe
        else:
            exename = QtGui.QFileDialog.getOpenFileName(self, 'Locate SWMM Executable', '/',
                                                        'exe files (*.exe)')
            if os.path.exists(exename):
                os.environ[self.modelenv1] = exename
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
        pass

    def std_openproj(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Project...", "", "Inp files (*.inp);;All files (*.*)")
        if file_name:
            self.project = Project()
            try:
               self.project.read_file(file_name)
               self.load_model(self.model)
               self.setWindowTitle(self.model + " - " + os.path.split(file_name)[1])
            except:
               self.project = None
               self.setWindowTitle(self.model)
        pass

    def proj_save(self):
        with open(self.project.file_name, 'w') as writer:
            writer.writelines(self.project.get_text())

    def proj_save_as(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As...", "", "Inp files (*.inp)")
        if file_name:
            with open(file_name, 'w') as writer:
                writer.writelines(self.project.get_text())
                self.project.file_name = file_name
                self.setWindowTitle(self.model + " - " + os.path.split(file_name)[1])

    def edit_options(self, itm, column):
        if self.project == None:
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
    def proj_run_simulation(self):
        run = 0
        inp_dir = ''
        margs=[]

        prog = os.environ[self.modelenv1]
        if not os.path.exists(prog):
            pymsgbox.alert('SWMM Executable is not found.')
            return -1

        filename = ''
        if self.project == None:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.inp)')
        else:
            #filename = self.project.name
            pass
        if os.path.exists(filename):
            fpre, fext = os.path.splitext(filename)
            margs.append(filename)
            margs.append(fpre + '.out')
            margs.append(fpre + '.rpt')
        else:
            pymsgbox.alert('SWMM input file not found.')

        #
        #running the Exe (modified version to rid of the \b printout
        #
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

    def load_model(self, model):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = frmMainSWMM()
    MainApp.show()
    sys.exit(app.exec_())