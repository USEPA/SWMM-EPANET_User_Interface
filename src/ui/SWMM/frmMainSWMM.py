import os, sys

os.environ['QT_API'] = 'pyqt'
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
from src.ui.embed_ipython_new import EmbedIPython
#from src.ui.ui_utility import EmbedMap
from src.ui.ui_utility import *
from src.ui.model_utility import *
from PyQt4 import QtCore, QtGui
from src.ui.frmMain import frmMain
from src.ui.SWMM.frmDates import frmDates
from src.ui.SWMM.frmDynamicWave import frmDynamicWave
from src.ui.SWMM.frmMapBackdropOptions import frmMapBackdropOptions
from src.ui.SWMM.frmGeneralOptions import frmGeneralOptions
from src.ui.SWMM.frmInterfaceFiles import frmInterfaceFiles
from src.ui.SWMM.frmReportOptions import frmReportOptions
from src.ui.SWMM.frmTimeSteps import frmTimeSteps
from src.ui.SWMM.frmTitle import frmTitle
#from IPython import embed
#from RestrictedPython import compile_restricted
#import py_compile
import pymsgbox
import imp
from qgis.core import *
from qgis.gui import *
from src.core.coordinates import *
from src.core.inputfile import *
from src.core.swmm.project import Project
from src.core.epanet.title import *
from src.core.epanet.curves import *
from src.core.epanet.labels import *
from src.core.epanet.patterns import *
from src.core.epanet.vertex import *
from src.core.epanet.options import *
from src.core.epanet.hydraulics import *

_frmDates = None
_frmDynamicWave = None
_frmMapBackdropOptions = None
_frmGeneralOptions = None
_frmInterfaceFiles = None
_frmReportOptions = None
_frmTimeSteps = None
_frmTitle = None

class frmMainSWMM(frmMain):
    def __init__(self, parent=None, *args):
        frmMain.__init__(self, parent)
        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.std_newproj)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.std_newproj)

        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.std_openproj)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.std_openproj)
        self.model = 'SWMM'
        self.on_load(model=self.model)

    def std_newproj(self):
        pass

    def std_openproj(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.net *.inp)')
        if len(filename) > 0:
           if os.path.splitext(filename)[1] == '.inp':
                self.model = 'SWMM'
           self.project = Project()
           try:
               self.project.read_file(filename)
               self.load_model(self.model)
           except:
               self.project = None
        pass

    def edit_options(self, itm, column):
        # if self.project == None:
        #     return

        if itm.data(0, 0) == 'Dates':
            _frmDates = frmDates(self)
            _frmDates.show()
        if itm.data(0, 0) == 'Dynamic Wave':
            _frmDynamicWave = frmDynamicWave(self)
            _frmDynamicWave.show()
        if itm.data(0, 0) == 'Map/Backdrop':
            _frmMapBackdropOptions = frmMapBackdropOptions(self)
            _frmMapBackdropOptions.show()
        if itm.data(0, 0) == 'General':
            _frmGeneralOptions = frmGeneralOptions(self)
            _frmGeneralOptions.show()
        if itm.data(0, 0) == 'Interface Files':
            _frmInterfaceFiles = frmInterfaceFiles(self)
            _frmInterfaceFiles.show()
        if itm.data(0, 0) == 'Reporting':
            _frmReportOptions = frmReportOptions(self)
            _frmReportOptions.show()
        if itm.data(0, 0) == 'Time Steps':
            _frmTimeSteps = frmTimeSteps(self)
            _frmTimeSteps.show()
        if itm.data(0, 0) == 'Title/Notes':
            _frmTitle = frmTitle(self)
            _frmTitle.show()

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