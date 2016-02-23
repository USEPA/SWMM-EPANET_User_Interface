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
from src.ui.EPANET.frmEnergyOptions import frmEnergyOptions
from src.ui.EPANET.frmHydraulicsOptions import frmHydraulicsOptions
from src.ui.EPANET.frmMapBackdropOptions import frmMapBackdropOptions
from src.ui.EPANET.frmQualityOptions import frmQualityOptions
from src.ui.EPANET.frmReactionsOptions import frmReactionsOptions
from src.ui.EPANET.frmReportOptions import frmReportOptions
from src.ui.EPANET.frmTimesOptions import frmTimesOptions
from src.ui.EPANET.frmTitle import frmTitle
from src.ui.model_utility import *
import pymsgbox
from core.coordinates import *
from core.inputfile import *
from core.epanet.project import Project
from core.epanet.title import *
from core.epanet.curves import *
from core.epanet.labels import *
from core.epanet.patterns import *
from core.epanet.vertex import *
from core.epanet.options import *
from core.epanet.hydraulics import *

_frmEnergyOptions = None
_frmHydraulicsOptions = None
_frmMapBackdropOptions = None
_frmQualityOptions = None
_frmReactionsOptions = None
_frmReportOptions = None
_frmTimesOptions = None
_frmTitle = None

class frmMainEPANET(frmMain):
    def __init__(self, parent=None, *args):
        frmMain.__init__(self, parent)

        QtCore.QObject.connect(self.actionStdNewProjectMenu, QtCore.SIGNAL('triggered()'), self.std_newproj)
        QtCore.QObject.connect(self.actionStdNewProject, QtCore.SIGNAL('triggered()'), self.std_newproj)

        QtCore.QObject.connect(self.actionStdOpenProjMenu, QtCore.SIGNAL('triggered()'), self.std_openproj)
        QtCore.QObject.connect(self.actionStdOpenProj, QtCore.SIGNAL('triggered()'), self.std_openproj)

        self.model = 'EPANET'
        self.on_load(model=self.model)

    def std_newproj(self):
        pass

    def std_openproj(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Existing Project', '/', 'Inp files (*.net *.inp)')
        if len(filename) > 0:
            self.project = Project()
            try:
                self.project.read_file(filename)
                self.load_model(self.model)
            except:
                self.project = None
        pass

    def proj_save(self):
        pymsgbox.alert('Saving EPANET')
        pass

    def proj_save_as(self):
        pymsgbox.alert("save as EPANET")
        pass

    def edit_options(self, itm, column):
        global _frmEnergyOptions
        if self.project == None:
             return

        if itm.data(0, 0) == 'Energy':
            _frmEnergyOptions = frmEnergyOptions(self)
            _frmEnergyOptions.show()
        if itm.data(0, 0) == 'Hydraulics':
            _frmHydraulicsOptions = frmHydraulicsOptions(self)
            _frmHydraulicsOptions.show()
        if itm.data(0, 0) == 'Map/Backdrop':
            _frmMapBackdropOptions = frmMapBackdropOptions(self)
            _frmMapBackdropOptions.show()
        if itm.data(0, 0) == 'Quality':
            _frmQualityOptions = frmQualityOptions(self)
            _frmQualityOptions.show()
        if itm.data(0, 0) == 'Reactions':
            _frmReactionsOptions = frmReactionsOptions(self)
            _frmReactionsOptions.show()
        if itm.data(0, 0) == 'Report':
            _frmReportOptions = frmReportOptions(self)
            _frmReportOptions.show()
        if itm.data(0, 0) == 'Times':
            _frmTimesOptions = frmTimesOptions(self)
            _frmTimesOptions.show()
        if itm.data(0, 0) == 'Title/Notes':
            _frmTitle = frmTitle(self)
            _frmTitle.show()

        # mitm = itm
        # if self.project == None or mitm.data(0, 0) != 'Options':
        #     return
        # from src.ui.frmOptions import frmOptions
        # dlg = frmOptions(self, self.project.options)
        # dlg.show()
        # result = dlg.exec_()
        # if result == 1:
        #    pass

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
