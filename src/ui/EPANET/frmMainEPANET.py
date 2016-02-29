import os, sys
os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
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
from ui.model_utility import *
from core.epanet.project import Project


class frmMainEPANET(frmMain):
    def __init__(self, parent=None, *args):
        frmMain.__init__(self, parent)

        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.std_newproj)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.std_newproj)

        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.std_openproj)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.std_openproj)

        self.model = 'EPANET'
        self.modelenv1 = 'EXE_EPANET'
        assembly_path = os.path.abspath(__file__)
        pp = os.path.dirname(os.path.dirname(os.path.dirname(assembly_path)))
        pexe = os.path.join(pp, r'Externals\epanet2d.exe')
        #pexe = os.path.join(pp, r'Externals\epanet.exe')
        if os.path.exists(pexe):
            os.environ[self.modelenv1] = pexe
        else:
            exename = QtGui.QFileDialog.getOpenFileName(self, 'Locate EPANET Executable', '/',
                                                        'exe files (*.exe)')
            if os.path.exists(exename):
                os.environ[self.modelenv1] = exename
            else:
                os.environ[self.modelenv1] = ''
        self.on_load(model=self.model)

        self._frmEnergyOptions = None
        self._frmHydraulicsOptions = None
        self._frmMapBackdropOptions = None
        self._frmQualityOptions = None
        self._frmReactionsOptions = None
        self._frmReportOptions = None
        self._frmTimesOptions = None
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
        self.project.write_file(self.project.file_name)

    def proj_save_as(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save As...", "", "Inp files (*.inp)")
        if file_name:
            self.project.write_file(file_name)
            self.setWindowTitle(self.model + " - " + os.path.split(file_name)[1])

    def edit_options(self, itm, column):
        if self.project == None:
             return

        if itm.data(0, 0) == 'Energy':
            self._frmEnergyOptions = frmEnergyOptions(self)
            self._frmEnergyOptions.show()
        if itm.data(0, 0) == 'Hydraulics':
            self._frmHydraulicsOptions = frmHydraulicsOptions(self)
            self._frmHydraulicsOptions.show()
        if itm.data(0, 0) == 'Map/Backdrop':
            self._frmMapBackdropOptions = frmMapBackdropOptions(self)
            self._frmMapBackdropOptions.show()
        if itm.data(0, 0) == 'Quality':
            self._frmQualityOptions = frmQualityOptions(self)
            self._frmQualityOptions.show()
        if itm.data(0, 0) == 'Reactions':
            self._frmReactionsOptions = frmReactionsOptions(self)
            self._frmReactionsOptions.show()
        if itm.data(0, 0) == 'Report':
            self._frmReportOptions = frmReportOptions(self)
            self._frmReportOptions.show()
        if itm.data(0, 0) == 'Times':
            self._frmTimesOptions = frmTimesOptions(self)
            self._frmTimesOptions.show()
        if itm.data(0, 0) == 'Title/Notes':
            self._frmTitle = frmTitle(self)
            self._frmTitle.show()

        # mitm = itm
        # if self.project == None or mitm.data(0, 0) != 'Options':
        #     return
        # from ui.frmOptions import frmOptions
        # dlg = frmOptions(self, self.project.options)
        # dlg.show()
        # result = dlg.exec_()
        # if result == 1:
        #    pass
    def proj_run_simulation(self):

        margs=[]
        prog = os.environ[self.modelenv1]
        if not os.path.exists(prog):
            pymsgbox.alert('EPANET Executable is not found.')
            return -1

        filename = ''
        if self.project == None:
            #file_name = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Input file')
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.inp)')
        else:
            #filename = self.project.name
            pass
        if os.path.exists(filename):
            fpre, fext = os.path.splitext(filename)
            margs.append(filename)
            margs.append(fpre + '.txt')
            margs.append(fpre + '.out')
        else:
            pymsgbox.alert('EPANET input file not found.')

        status = StatusMonitor0(prog, margs, self, model='EPANET')
        status.show()

    def on_load(self, **kwargs):
        #self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        #cleaner = QtCore.QObjectCleanupHandler()
        #cleaner.add(self.tabProjMap.layout())
        #try out epanet
        self.obj_tree = ObjectTreeView(model=kwargs['model'])
        #QtCore.QObject.connect(self.obj_tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem, int)'), \
        #                       self.edit_options)
        self.obj_tree.itemDoubleClicked.connect(self.edit_options)
        #self.tabProjMap.addTab(self.obj_tree, 'Project')
        layout = QVBoxLayout(self.tabProject)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.obj_tree)
        self.tabProject.setLayout(layout)
        self.setWindowTitle(self.model)

        self.obj_list = ObjectListView(model=kwargs['model'],ObjRoot='',ObjType='',ObjList=None)
        mlayout = self.dockw_more.layout()
        #mlayout.setContentsMargins(0, 0, 0, 0)
        mlayout.addWidget(self.obj_list)
        #layout1 = QVBoxLayout(self.dockw_more)
        self.dockw_more.setLayout(mlayout)
        #self.actionPan.setEnabled(False)

    def load_model(self, model):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MainApp = frmMainEPANET()
    MainApp.show()
    sys.exit(app.exec_())
